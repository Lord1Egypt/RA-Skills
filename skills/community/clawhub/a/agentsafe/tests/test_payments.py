"""x402 payment integration tests (Phase 12).

Flows verified against the pinned official SDK (x402==2.25.0) with the
facilitator HTTP API mocked via respx (GET /supported, POST /verify,
POST /settle - the endpoints used by x402.http.HTTPFacilitatorClient).

Settlement ordering note: this integration follows the official
x402.mcp wrapper flow - verification happens BEFORE tool execution
(dispatch) and settlement AFTER successful execution. A failed dispatch
therefore never calls /settle: no funds move and no refund is owed.
"""

import io
import json
import zipfile
from datetime import UTC

import httpx
import pytest
import respx
from fastmcp import Client

from agentsafe.config import Settings, validate_runtime_settings
from agentsafe.payment.x402_adapter import X402PaymentAdapter
from agentsafe.server import build_server

ADDR = "0x" + "ab" * 20
PAYER = "0x" + "cd" * 20
GH = "https://api.github.com"
RPC = "https://rpc.test"
ETH = "https://api.etherscan.test/v2/api"
FAC = "https://facilitator.test"

SUPPORTED = {
    "kinds": [{"x402Version": 2, "scheme": "exact", "network": "eip155:84532", "extra": None}],
    "extensions": [],
}

# Verified-source fixture used for tiered pricing: N non-blank source lines.
SOURCE_LINES = 10
TIER_PRICE = "$0.50"  # <=100 lines
TIER_AMOUNT = "500000"  # $0.50 at 6 decimals


def _etherscan_source_response(lines: int) -> dict:
    return {
        "status": "1",
        "message": "OK",
        "result": [
            {
                "SourceCode": "pragma solidity ^0.8.20;\n" + "uint256 v;\n" * (lines - 1),
                "ContractName": "C",
                "CompilerVersion": "v0.8.20+commit.a1b79de6",
                "OptimizationUsed": "0",
                "Runs": "",
                "ABI": "[]",
                "Proxy": "0",
                "Implementation": "",
            }
        ],
    }


def _mock_source(lines: int = SOURCE_LINES) -> None:
    respx.get(ETH).mock(return_value=httpx.Response(200, json=_etherscan_source_response(lines)))


def _settings(**kw) -> Settings:
    base = {
        "INFURA_ETH_ENDPOINT": RPC,
        "ETHERSCAN_API_KEY": "k",
        "ETHERSCAN_BASE_URL": ETH,
        "GITHUB_TOKEN": "ghp-t",
        "GITHUB_REPO": "owner/repo",
        "LLM_PROVIDERS_JSON": json.dumps(
            [
                {
                    "name": "p",
                    "base_url": "https://llm.test/v1",
                    "api_key": "sk",
                    "model": "m",
                    "rpm_limit": 60,
                }
            ]
        ),
        "TASK_STORE": "memory",
        "PAYMENTS_ENABLED": True,
        "X402_PAY_TO": "0x" + "ef" * 20,
        "X402_NETWORK": "eip155:84532",
        "X402_SDK_VERSION": "2.25.0",
        "X402_FACILITATOR_URL": FAC,
        "X402_PRICE": "$0.01",
    }
    base.update(kw)
    return Settings(_env_file=None, **base)


def _mock_facilitator():
    """Mock Etherscan source + /supported, /verify, /settle. Returns the routes."""
    _mock_source()
    routes = {
        "supported": respx.get(f"{FAC}/supported").mock(
            return_value=httpx.Response(200, json=SUPPORTED)
        ),
        "verify": respx.post(f"{FAC}/verify").mock(
            return_value=httpx.Response(200, json={"isValid": True, "payer": PAYER})
        ),
        "settle": respx.post(f"{FAC}/settle").mock(
            return_value=httpx.Response(
                200,
                json={
                    "success": True,
                    "payer": PAYER,
                    "transaction": "0x" + "11" * 32,
                    "network": "eip155:84532",
                },
            )
        ),
    }
    return routes


def _wire_dispatch_and_runs():
    from datetime import datetime, timedelta

    state: dict = {}
    created_at = (datetime.now(UTC) + timedelta(seconds=5)).isoformat()

    def capture_dispatch(request):
        state["task_id"] = json.loads(request.read())["inputs"]["task_id"]
        return httpx.Response(204)

    def runs(request):
        tid = state.get("task_id", "unknown")
        return httpx.Response(
            200,
            json={
                "workflow_runs": [
                    {
                        "id": 5,
                        "name": f"audit-{tid}",
                        "created_at": created_at,
                        "status": "in_progress",
                        "conclusion": None,
                    }
                ]
            },
        )

    respx.post(f"{GH}/repos/owner/repo/actions/workflows/audit.yml/dispatches").mock(
        side_effect=capture_dispatch
    )
    respx.get(f"{GH}/repos/owner/repo/actions/workflows/audit.yml/runs").mock(side_effect=runs)
    return state


def _client_payload(adapter: X402PaymentAdapter, **overrides) -> dict:
    """Build a client x402/payment meta payload echoing advertised terms."""
    accepted = adapter.accepts[0].model_dump(by_alias=True, exclude_none=True)
    accepted.update(overrides)
    return {
        "x402Version": 2,
        "payload": {"kind": "exact/eip3009", "data": {"signature": "0x" + "22" * 32}},
        "accepted": accepted,
        "resource": {"url": "mcp://tool/audit_contract"},
    }


def _unwrap_result(result):
    """Return (is_error, structured_content_or_data)."""
    return bool(result.is_error), (
        result.structured_content if result.structured_content is not None else result.data
    )


class TestAdapterConstruction:
    @respx.mock
    def test_enabled_adapter_builds_official_requirements(self):
        routes = _mock_facilitator()
        adapter = X402PaymentAdapter(
            enabled=True,
            sdk_version="2.25.0",
            network="eip155:84532",
            pay_to="0x" + "ef" * 20,
            facilitator_url=FAC,
            price="$0.01",
        )
        assert routes["supported"].call_count == 1
        req = adapter.accepts[0]
        assert req.scheme == "exact"
        assert req.network == "eip155:84532"
        # Base Sepolia test USDC is the SDK's default asset for this network
        assert req.asset == "0x036CbD53842c5426634e7929541eC2318f3dCF7e"
        assert req.pay_to == "0x" + "ef" * 20
        assert req.amount == "10000"  # $0.01 at 6 decimals
        # dynamic tiered pricing: requirements for an arbitrary price
        tier = adapter.requirements_for_price("$25.00")
        assert tier[0].amount == "25000000"  # $25.00 at 6 decimals


class TestPaymentFlow:
    @respx.mock
    async def test_missing_payment_returns_official_402_body(self):
        _mock_facilitator()
        server = build_server(_settings())
        async with Client(server) as client:
            result = await client.call_tool(
                "audit_contract",
                {"address": ADDR},
                raise_on_error=False,
            )
        is_error, body = _unwrap_result(result)
        assert is_error is True
        assert body["x402Version"] == 2
        assert body["accepts"][0]["network"] == "eip155:84532"
        # the 402 body quotes the TIER price, not the startup default price
        assert body["accepts"][0]["amount"] == TIER_AMOUNT
        assert body["error"] == "Payment Required"
        assert "mcp://tool/audit_contract" in body["resource"]["url"]

    @respx.mock
    async def test_valid_payment_dispatches_and_settles_after_execution(self):
        routes = _mock_facilitator()
        gh_state = _wire_dispatch_and_runs()
        server = build_server(_settings())
        async with Client(server) as client:
            adapter_probe = X402PaymentAdapter(
                enabled=True,
                sdk_version="2.25.0",
                network="eip155:84532",
                pay_to="0x" + "ef" * 20,
                facilitator_url=FAC,
                price="$0.50",
            )
            payload = _client_payload(adapter_probe)
            result = await client.call_tool(
                "audit_contract",
                {"address": ADDR},
                meta={"x402/payment": payload},
                raise_on_error=False,
            )
        is_error, body = _unwrap_result(result)
        assert is_error is False
        assert body["ok"] is True
        assert body["state"] == "running"
        assert gh_state["task_id"] == body["task_id"]
        # verify-before-execution, settle-after-execution
        assert routes["verify"].call_count == 1
        assert routes["settle"].call_count == 1

    @respx.mock
    async def test_insufficient_amount_is_rejected(self):
        routes = _mock_facilitator()
        _wire_dispatch_and_runs()
        server = build_server(_settings())
        async with Client(server) as client:
            probe = X402PaymentAdapter(
                enabled=True,
                sdk_version="2.25.0",
                network="eip155:84532",
                pay_to="0x" + "ef" * 20,
                facilitator_url=FAC,
                price="$0.50",
            )
            payload = _client_payload(probe, amount="1")  # underpayment
            result = await client.call_tool(
                "audit_contract",
                {"address": ADDR},
                meta={"x402/payment": payload},
                raise_on_error=False,
            )
        is_error, body = _unwrap_result(result)
        assert is_error is True
        assert "No matching payment requirements" in body["error"]
        # unpaid request must not dispatch and must not verify
        assert routes["verify"].call_count == 0
        assert routes["settle"].call_count == 0

    @respx.mock
    async def test_wrong_network_is_rejected(self):
        _mock_facilitator()
        _wire_dispatch_and_runs()
        server = build_server(_settings())
        async with Client(server) as client:
            probe = X402PaymentAdapter(
                enabled=True,
                sdk_version="2.25.0",
                network="eip155:84532",
                pay_to="0x" + "ef" * 20,
                facilitator_url=FAC,
                price="$0.50",
            )
            payload = _client_payload(probe, network="eip155:8453")  # mainnet
            result = await client.call_tool(
                "audit_contract",
                {"address": ADDR},
                meta={"x402/payment": payload},
                raise_on_error=False,
            )
        is_error, body = _unwrap_result(result)
        assert is_error is True
        assert "No matching payment requirements" in body["error"]

    @respx.mock
    async def test_wrong_asset_is_rejected(self):
        _mock_facilitator()
        _wire_dispatch_and_runs()
        server = build_server(_settings())
        async with Client(server) as client:
            probe = X402PaymentAdapter(
                enabled=True,
                sdk_version="2.25.0",
                network="eip155:84532",
                pay_to="0x" + "ef" * 20,
                facilitator_url=FAC,
                price="$0.50",
            )
            payload = _client_payload(probe, asset="0x" + "99" * 20)
            result = await client.call_tool(
                "audit_contract",
                {"address": ADDR},
                meta={"x402/payment": payload},
                raise_on_error=False,
            )
        is_error, body = _unwrap_result(result)
        assert is_error is True
        assert "No matching payment requirements" in body["error"]

    @respx.mock
    async def test_replayed_payment_is_rejected(self):
        routes = _mock_facilitator()
        _wire_dispatch_and_runs()
        server = build_server(_settings())
        probe = X402PaymentAdapter(
            enabled=True,
            sdk_version="2.25.0",
            network="eip155:84532",
            pay_to="0x" + "ef" * 20,
            facilitator_url=FAC,
            price="$0.50",
        )
        payload = _client_payload(probe)
        async with Client(server) as client:
            first = await client.call_tool(
                "audit_contract",
                {"address": ADDR},
                meta={"x402/payment": payload},
                raise_on_error=False,
            )
            second = await client.call_tool(
                "audit_contract",
                {"address": ADDR},
                meta={"x402/payment": payload},  # same payment again
                raise_on_error=False,
            )
        assert _unwrap_result(first)[0] is False
        is_error, body = _unwrap_result(second)
        assert is_error is True
        assert "replay" in body["error"].lower()
        # only one verify + one settle ever happened
        assert routes["verify"].call_count == 1
        assert routes["settle"].call_count == 1

    @respx.mock
    async def test_replayed_payment_rejected_across_restart(self):
        """Regression: the replay ledger must survive a restart by seeding
        from the persisted task store (payment_ref column)."""
        import tempfile
        from pathlib import Path

        routes = _mock_facilitator()
        _wire_dispatch_and_runs()
        probe = X402PaymentAdapter(
            enabled=True,
            sdk_version="2.25.0",
            network="eip155:84532",
            pay_to="0x" + "ef" * 20,
            facilitator_url=FAC,
            price="$0.50",
        )
        payload = _client_payload(probe)
        with tempfile.TemporaryDirectory() as tmp:
            db = str(Path(tmp) / "tasks.db")
            first = build_server(_settings(TASK_STORE="sqlite", TASK_DB_PATH=db))
            async with Client(first) as client:
                ok = await client.call_tool(
                    "audit_contract",
                    {"address": ADDR},
                    meta={"x402/payment": payload},
                    raise_on_error=False,
                )
            assert _unwrap_result(ok)[0] is False

            # "restart": a fresh server over the same persisted task store
            restarted = build_server(_settings(TASK_STORE="sqlite", TASK_DB_PATH=db))
            async with Client(restarted) as client:
                replay = await client.call_tool(
                    "audit_contract",
                    {"address": ADDR},
                    meta={"x402/payment": payload},
                    raise_on_error=False,
                )
        is_error, body = _unwrap_result(replay)
        assert is_error is True
        assert "replay" in body["error"].lower()
        assert routes["verify"].call_count == 1  # only the original payment verified
        assert routes["settle"].call_count == 1

    @respx.mock
    async def test_verification_failure_blocks_dispatch(self):
        routes = _mock_facilitator()
        routes["verify"].mock(
            return_value=httpx.Response(
                200, json={"isValid": False, "invalidReason": "invalid_signature"}
            )
        )
        gh = _wire_dispatch_and_runs()
        server = build_server(_settings())
        probe = X402PaymentAdapter(
            enabled=True,
            sdk_version="2.25.0",
            network="eip155:84532",
            pay_to="0x" + "ef" * 20,
            facilitator_url=FAC,
            price="$0.50",
        )
        async with Client(server) as client:
            result = await client.call_tool(
                "audit_contract",
                {"address": ADDR},
                meta={"x402/payment": _client_payload(probe)},
                raise_on_error=False,
            )
        is_error, body = _unwrap_result(result)
        assert is_error is True
        assert body["error"] == "invalid_signature"
        assert "task_id" not in gh  # nothing was dispatched
        assert routes["settle"].call_count == 0

    @respx.mock
    async def test_settlement_failure_surfaces_official_error(self):
        routes = _mock_facilitator()
        routes["settle"].mock(
            return_value=httpx.Response(
                200,
                json={
                    "success": False,
                    "errorReason": "transfer_already_completed",
                    "payer": PAYER,
                    "transaction": "",
                    "network": "eip155:84532",
                },
            )
        )
        gh_state = _wire_dispatch_and_runs()
        server = build_server(_settings())
        probe = X402PaymentAdapter(
            enabled=True,
            sdk_version="2.25.0",
            network="eip155:84532",
            pay_to="0x" + "ef" * 20,
            facilitator_url=FAC,
            price="$0.50",
        )
        async with Client(server) as client:
            result = await client.call_tool(
                "audit_contract",
                {"address": ADDR},
                meta={"x402/payment": _client_payload(probe)},
                raise_on_error=False,
            )
        is_error, body = _unwrap_result(result)
        assert is_error is True
        assert "Payment settlement failed: transfer_already_completed" in body["error"]
        assert body["x402/payment-response"]["success"] is False
        # execution already happened; the audit was dispatched
        assert "task_id" in gh_state

    @respx.mock
    async def test_dispatch_failure_never_settles(self):
        routes = _mock_facilitator()
        # GitHub API hard-fails: dispatch never succeeds
        respx.post(f"{GH}/repos/owner/repo/actions/workflows/audit.yml/dispatches").mock(
            return_value=httpx.Response(500)
        )
        server = build_server(_settings())
        probe = X402PaymentAdapter(
            enabled=True,
            sdk_version="2.25.0",
            network="eip155:84532",
            pay_to="0x" + "ef" * 20,
            facilitator_url=FAC,
            price="$0.50",
        )
        async with Client(server) as client:
            result = await client.call_tool(
                "audit_contract",
                {"address": ADDR},
                meta={"x402/payment": _client_payload(probe)},
                raise_on_error=False,
            )
        is_error, body = _unwrap_result(result)
        assert is_error is False
        assert body["ok"] is False
        assert body["error_code"] == "dispatch_failed"
        # verify happened, settlement did NOT: no funds moved, no refund owed
        assert routes["verify"].call_count == 1
        assert routes["settle"].call_count == 0


class TestReportPaymentBinding:
    @respx.mock
    async def test_unpaid_task_cannot_retrieve_paid_report(self):
        _mock_facilitator()
        _wire_dispatch_and_runs()
        # Share a sqlite task store between a dev-mode server (creates an
        # UNPAID task) and a payments-enabled server (must withhold report).
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmp:
            db = str(Path(tmp) / "tasks.db")
            dev_server = build_server(
                _settings(PAYMENTS_ENABLED=False, TASK_STORE="sqlite", TASK_DB_PATH=db)
            )
            paid_server = build_server(_settings(TASK_STORE="sqlite", TASK_DB_PATH=db))

            async with Client(dev_server) as client:
                created = await client.call_tool("audit_contract", {"address": ADDR})
                task_id = created.data["task_id"]

            respx.get(f"{GH}/repos/owner/repo/actions/runs/5").mock(
                return_value=httpx.Response(
                    200, json={"id": 5, "status": "completed", "conclusion": "success"}
                )
            )
            report = {
                "address": ADDR,
                "chain": "ethereum-mainnet",
                "findings": [],
                "summary": {"total_findings": 0},
                "disclaimer": "AI-assisted risk screening, not a formal audit.",
            }
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w") as zf:
                zf.writestr("report.json", json.dumps(report))
            respx.get(f"{GH}/repos/owner/repo/actions/runs/5/artifacts").mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "artifacts": [
                            {
                                "id": 9,
                                "name": f"audit-report-{task_id}",
                                "expired": False,
                                "run_id": 5,
                            }
                        ]
                    },
                ),
            )
            respx.get(f"{GH}/repos/owner/repo/actions/artifacts/9/zip").mock(
                return_value=httpx.Response(200, content=buf.getvalue())
            )

            async with Client(paid_server) as client:
                status = await client.call_tool(
                    "check_audit_status", {"task_id": task_id}, raise_on_error=False
                )
            assert status.data["ok"] is False
            assert status.data["error_code"] == "payment_required"
            assert "report" not in status.data

    @respx.mock
    async def test_paid_task_can_retrieve_report(self):
        _mock_facilitator()
        gh_state = _wire_dispatch_and_runs()
        server = build_server(_settings())
        probe = X402PaymentAdapter(
            enabled=True,
            sdk_version="2.25.0",
            network="eip155:84532",
            pay_to="0x" + "ef" * 20,
            facilitator_url=FAC,
            price="$0.50",
        )
        async with Client(server) as client:
            created = await client.call_tool(
                "audit_contract",
                {"address": ADDR},
                meta={"x402/payment": _client_payload(probe)},
                raise_on_error=False,
            )
            task_id = created.data["task_id"]

            respx.get(f"{GH}/repos/owner/repo/actions/runs/5").mock(
                return_value=httpx.Response(
                    200, json={"id": 5, "status": "completed", "conclusion": "success"}
                )
            )
            report = {
                "address": ADDR,
                "chain": "ethereum-mainnet",
                "findings": [],
                "summary": {"total_findings": 0},
                "disclaimer": "AI-assisted risk screening, not a formal audit.",
            }
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w") as zf:
                zf.writestr("report.json", json.dumps(report))
            respx.get(f"{GH}/repos/owner/repo/actions/runs/5/artifacts").mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "artifacts": [
                            {
                                "id": 9,
                                "name": f"audit-report-{task_id}",
                                "expired": False,
                                "run_id": 5,
                            }
                        ]
                    },
                )
            )
            respx.get(f"{GH}/repos/owner/repo/actions/artifacts/9/zip").mock(
                return_value=httpx.Response(200, content=buf.getvalue())
            )

            status = await client.call_tool("check_audit_status", {"task_id": task_id})
            assert status.data["ok"] is True
            assert status.data["report"]["address"] == ADDR
            assert gh_state["task_id"] == task_id

    @respx.mock
    async def test_dev_mode_remains_free(self):
        _mock_facilitator()
        _wire_dispatch_and_runs()
        server = build_server(_settings(PAYMENTS_ENABLED=False))
        async with Client(server) as client:
            result = await client.call_tool("audit_contract", {"address": ADDR})
        assert result.data["ok"] is True
        assert result.data["state"] == "running"


class TestTieredPricing:
    """Dynamic per-contract quoting (AgentLISA tier table) - closes the
    fixed-$0.01 loophole where any audit cost one cent."""

    @respx.mock
    async def test_old_fixed_cent_payment_no_longer_accepted(self):
        """Regression: a $0.01 payload (the old fixed price) must NOT pass
        for a 10-line contract quoted at $0.50."""
        routes = _mock_facilitator()
        _wire_dispatch_and_runs()
        server = build_server(_settings())
        cheap_probe = X402PaymentAdapter(
            enabled=True,
            sdk_version="2.25.0",
            network="eip155:84532",
            pay_to="0x" + "ef" * 20,
            facilitator_url=FAC,
            price="$0.01",
        )
        async with Client(server) as client:
            result = await client.call_tool(
                "audit_contract",
                {"address": ADDR},
                meta={"x402/payment": _client_payload(cheap_probe)},
                raise_on_error=False,
            )
        is_error, body = _unwrap_result(result)
        assert is_error is True
        assert "No matching payment requirements" in body["error"]
        # the 402 body re-quotes the correct tier price
        assert body["accepts"][0]["amount"] == TIER_AMOUNT
        assert routes["verify"].call_count == 0
        assert routes["settle"].call_count == 0

    @respx.mock
    async def test_mid_tier_contract_quoted_at_5_dollars(self):
        _mock_facilitator()
        _mock_source(lines=600)  # 501-1,000 tier -> $5.00
        _wire_dispatch_and_runs()
        server = build_server(_settings())
        async with Client(server) as client:
            result = await client.call_tool(
                "audit_contract",
                {"address": ADDR},
                raise_on_error=False,
            )
        is_error, body = _unwrap_result(result)
        assert is_error is True
        assert body["accepts"][0]["amount"] == "5000000"  # $5.00 at 6 decimals

    @respx.mock
    async def test_oversized_contract_requires_enterprise_inquiry(self):
        routes = _mock_facilitator()
        _mock_source(lines=5001)
        _wire_dispatch_and_runs()
        server = build_server(_settings())
        async with Client(server) as client:
            result = await client.call_tool(
                "audit_contract",
                {"address": ADDR},
                raise_on_error=False,
            )
        is_error, body = _unwrap_result(result)
        assert is_error is False
        assert body["ok"] is False
        assert body["error_code"] == "ENTERPRISE_INQUIRY_REQUIRED"
        assert body["error"] == "ENTERPRISE_INQUIRY_REQUIRED"
        assert "5,000-line limit" in body["message"]
        assert "enterprise" in body["message"].lower()
        assert body["inquiryUrl"] == "https://tally.so/r/laby7B"
        # no payment challenge and nothing dispatched
        assert routes["verify"].call_count == 0
        assert routes["settle"].call_count == 0

    @respx.mock
    async def test_unverified_contract_cannot_be_priced_or_audited(self):
        routes = _mock_facilitator()
        respx.get(ETH).mock(
            return_value=httpx.Response(
                200,
                json={
                    "status": "1",
                    "message": "OK",
                    "result": [
                        {
                            "SourceCode": "",
                            "ContractName": "",
                            "ABI": "Contract source code not verified",
                            "CompilerVersion": "",
                        }
                    ],
                },
            )
        )
        _wire_dispatch_and_runs()
        server = build_server(_settings())
        async with Client(server) as client:
            result = await client.call_tool(
                "audit_contract",
                {"address": ADDR},
                raise_on_error=False,
            )
        is_error, body = _unwrap_result(result)
        assert is_error is False
        assert body["ok"] is False
        assert body["error_code"] == "source_not_verified"
        assert routes["verify"].call_count == 0


class TestConfigGuardrails:
    def test_default_payments_disabled(self):
        s = _settings(PAYMENTS_ENABLED=False)
        validate_runtime_settings(s)

    def test_mainnet_requires_explicit_opt_in(self):
        s = _settings(X402_NETWORK="eip155:8453")
        with pytest.raises(Exception, match="X402_ALLOW_MAINNET"):
            validate_runtime_settings(s)
