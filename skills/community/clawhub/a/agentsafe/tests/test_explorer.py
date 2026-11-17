"""Phase 2 tests: Etherscan client + multi-file source preservation (respx-mocked)."""

import json

import httpx
import pytest
import respx

from agentsafe.explorer import (
    ContractNotVerifiedError,
    EtherscanClient,
    ExplorerAuthError,
    ExplorerError,
    ExplorerRateLimitError,
    parse_source_code,
)

ADDR = "0x" + "cd" * 20
BASE = "https://api.etherscan.test/v2/api"


async def _nosleep(_: float) -> None:
    return None


def _client(**kw) -> EtherscanClient:
    kw.setdefault("sleeper", _nosleep)
    return EtherscanClient("test-key", base_url=BASE, **kw)


def _verified_payload(source: str, **overrides) -> dict:
    rec = {
        "SourceCode": source,
        "ABI": '[{"type":"function","name":"foo"}]',
        "ContractName": "Vault",
        "CompilerVersion": "v0.8.19+commit.7dd6d404",
        "OptimizationUsed": "1",
        "Runs": "200",
        "EVMVersion": "Default",
        "Proxy": "0",
        "Implementation": "",
    }
    rec.update(overrides)
    return {"status": "1", "message": "OK", "result": [rec]}


class TestParseSourceCode:
    def test_plain_single_file(self):
        files, settings, lang = parse_source_code("pragma solidity ^0.8.0;")
        assert len(files) == 1
        assert files[0].path == "contract.sol"
        assert files[0].content.startswith("pragma")
        assert settings is None
        assert lang == "Solidity"

    def test_standard_json_multi_file_preserves_paths(self):
        std = {
            "language": "Solidity",
            "sources": {
                "contracts/Vault.sol": {"content": "// vault"},
                "contracts/lib/SafeMath.sol": {"content": "// lib"},
            },
            "settings": {"optimizer": {"enabled": True, "runs": 200}},
        }
        files, settings, lang = parse_source_code(json.dumps(std))
        assert [f.path for f in files] == ["contracts/Vault.sol", "contracts/lib/SafeMath.sol"]
        assert settings == {"optimizer": {"enabled": True, "runs": 200}}
        assert lang == "Solidity"

    def test_etherscan_double_brace_escaping(self):
        std = {
            "language": "Solidity",
            "sources": {"src/A.sol": {"content": "// a"}, "src/B.sol": {"content": "// b"}},
            "settings": {"evmVersion": "paris"},
        }
        raw = "{" + json.dumps(std) + "}"  # Etherscan wraps Standard JSON in extra braces
        files, settings, _ = parse_source_code(raw)
        assert len(files) == 2
        assert files[0].path == "src/A.sol"
        assert settings == {"evmVersion": "paris"}

    def test_braced_non_json_treated_as_plain_source(self):
        files, settings, _ = parse_source_code("{ // comment starts with brace\ncontract X{}")
        assert len(files) == 1
        assert settings is None

    def test_empty_source(self):
        files, _, _ = parse_source_code("")
        assert files == []

    def test_corrupted_multifile_raises(self):
        with pytest.raises(ExplorerError, match="unbalanced"):
            parse_source_code("{{ broken json")
        with pytest.raises(ExplorerError, match="Standard JSON"):
            parse_source_code("{{ not valid json }}")


class TestGetVerifiedSource:
    @respx.mock
    async def test_verified_single_file(self):
        respx.get(BASE).mock(
            return_value=httpx.Response(200, json=_verified_payload("pragma solidity ^0.8.0;"))
        )
        bundle = await _client().get_verified_source(ADDR)
        assert bundle.is_verified
        assert bundle.contract_name == "Vault"
        assert bundle.compiler_version == "v0.8.19+commit.7dd6d404"
        assert bundle.optimization_used is True
        assert bundle.runs == 200
        assert bundle.is_proxy is False
        assert len(bundle.files) == 1

    @respx.mock
    async def test_verified_multi_file(self):
        std = {
            "language": "Solidity",
            "sources": {
                "contracts/Vault.sol": {"content": "// v"},
                "contracts/interfaces/IVault.sol": {"content": "// i"},
            },
            "settings": {"optimizer": {"enabled": False}},
        }
        raw = "{" + json.dumps(std) + "}"
        respx.get(BASE).mock(return_value=httpx.Response(200, json=_verified_payload(raw)))
        bundle = await _client().get_verified_source(ADDR)
        assert bundle.is_verified
        assert [f.path for f in bundle.files] == [
            "contracts/Vault.sol",
            "contracts/interfaces/IVault.sol",
        ]
        assert bundle.settings == {"optimizer": {"enabled": False}}

    @respx.mock
    async def test_proxy_contract_flags(self):
        respx.get(BASE).mock(
            return_value=httpx.Response(
                200,
                json=_verified_payload(
                    "pragma solidity ^0.8.0;", Proxy="1", Implementation="0x" + "ef" * 20
                ),
            )
        )
        bundle = await _client().get_verified_source(ADDR)
        assert bundle.is_proxy is True
        assert bundle.implementation == "0x" + "ef" * 20

    @respx.mock
    async def test_not_verified_contract(self):
        rec = {
            "SourceCode": "",
            "ABI": "Contract source code not verified",
            "ContractName": "",
            "CompilerVersion": "",
        }
        respx.get(BASE).mock(
            return_value=httpx.Response(200, json={"status": "1", "message": "OK", "result": [rec]})
        )
        with pytest.raises(ContractNotVerifiedError):
            await _client().get_verified_source(ADDR)

    @respx.mock
    async def test_api_level_rate_limit_message(self):
        respx.get(BASE).mock(
            return_value=httpx.Response(
                200, json={"status": "0", "message": "NOTOK", "result": "Max rate limit reached"}
            )
        )
        with pytest.raises(ExplorerRateLimitError):
            await _client().get_verified_source(ADDR)

    @respx.mock
    async def test_invalid_api_key(self):
        respx.get(BASE).mock(
            return_value=httpx.Response(
                200, json={"status": "0", "message": "NOTOK", "result": "Invalid API Key"}
            )
        )
        with pytest.raises(ExplorerAuthError):
            await _client().get_verified_source(ADDR)

    @respx.mock
    async def test_generic_api_error(self):
        respx.get(BASE).mock(
            return_value=httpx.Response(
                200, json={"status": "0", "message": "NOTOK", "result": "Something else"}
            )
        )
        with pytest.raises(ExplorerError):
            await _client().get_verified_source(ADDR)

    @respx.mock
    async def test_http_429_retries_then_gives_up(self):
        route = respx.get(BASE).mock(return_value=httpx.Response(429, json={}))
        with pytest.raises(ExplorerRateLimitError, match="giving up"):
            await _client(max_retries=1).get_verified_source(ADDR)
        assert route.call_count == 2

    @respx.mock
    async def test_timeout_retries_then_success(self):
        route = respx.get(BASE)
        std = {"language": "Solidity", "sources": {"A.sol": {"content": "// a"}}, "settings": {}}
        route.side_effect = [
            httpx.ReadTimeout("t/o"),
            httpx.Response(200, json=_verified_payload(json.dumps(std))),
        ]
        bundle = await _client(max_retries=2).get_verified_source(ADDR)
        assert bundle.is_verified

    @respx.mock
    async def test_api_key_sent_but_not_logged(self):
        route = respx.get(BASE).mock(
            return_value=httpx.Response(200, json=_verified_payload("pragma solidity ^0.8.0;"))
        )
        await _client().get_verified_source(ADDR)
        assert "apikey=test-key" in str(route.calls.last.request.url)

    async def test_invalid_address_rejected_without_http(self):
        with pytest.raises(ValueError, match="invalid EVM address"):
            await _client().get_verified_source("0xnope")

    async def test_missing_api_key_rejected(self):
        with pytest.raises(ValueError):
            EtherscanClient("")
