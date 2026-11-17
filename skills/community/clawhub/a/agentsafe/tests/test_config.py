"""Phase 1 tests: configuration validation and fail-fast startup rules."""

import json

import pytest
from pydantic import ValidationError

from agentsafe.config import (
    LLMProviderConfig,
    Settings,
    SettingsError,
    mask_secret,
    validate_runtime_settings,
)

VALID_PROVIDER = {
    "name": "prov-a",
    "base_url": "https://api.example.com/v1",
    "api_key": "sk-test-123",
    "model": "test-model",
    "rpm_limit": 5,
}


def _settings(**overrides) -> Settings:
    base = {
        "INFURA_ETH_ENDPOINT": "https://mainnet.infura.io/v3/test",
        "ETHERSCAN_API_KEY": "test-key",
        "GITHUB_TOKEN": "ghp-test",
        "GITHUB_REPO": "owner/repo",
        "LLM_PROVIDERS_JSON": json.dumps([VALID_PROVIDER]),
    }
    base.update(overrides)
    # _env_file=None: tests must be hermetic - never read the operator's .env
    return Settings(_env_file=None, **base)


class TestSettingsDefaults:
    def test_payments_disabled_by_default(self):
        s = Settings(_env_file=None)
        assert s.PAYMENTS_ENABLED is False

    def test_numeric_ranges_defaults(self):
        s = Settings(_env_file=None)
        assert 1 <= s.LLM_GLOBAL_RPM <= 1000
        assert s.AUDIT_TIMEOUT_SECONDS >= 30
        assert s.ARTIFACT_RETENTION_DAYS >= 1

    def test_invalid_log_level_rejected(self):
        with pytest.raises(ValidationError):
            Settings.model_validate({"LOG_LEVEL": "VERBOSE"})

    def test_invalid_repo_format_rejected(self):
        with pytest.raises(ValidationError):
            Settings.model_validate({"GITHUB_REPO": "not-a-repo"})

    def test_workflow_file_path_traversal_rejected(self):
        with pytest.raises(ValidationError):
            Settings.model_validate({"GITHUB_WORKFLOW_FILE": "../evil.yml"})
        with pytest.raises(ValidationError):
            Settings.model_validate({"GITHUB_WORKFLOW_FILE": "/abs/audit.yml"})


class TestLLMProviderParsing:
    def test_valid_provider_list(self):
        s = _settings()
        providers = s.llm_providers()
        assert len(providers) == 1
        assert providers[0].name == "prov-a"
        assert providers[0].rpm_limit == 5

    def test_invalid_json_rejected(self):
        s = _settings(LLM_PROVIDERS_JSON="{not json")
        with pytest.raises(SettingsError, match="not valid JSON"):
            s.llm_providers()

    def test_missing_required_field_rejected(self):
        bad = dict(VALID_PROVIDER)
        del bad["api_key"]
        s = _settings(LLM_PROVIDERS_JSON=json.dumps([bad]))
        with pytest.raises(SettingsError, match="api_key"):
            s.llm_providers()

    def test_duplicate_provider_names_rejected(self):
        s = _settings(LLM_PROVIDERS_JSON=json.dumps([VALID_PROVIDER, VALID_PROVIDER]))
        with pytest.raises(SettingsError, match="unique"):
            s.llm_providers()

    def test_provider_base_url_must_be_http(self):
        bad = dict(VALID_PROVIDER, base_url="ftp://nope")
        with pytest.raises(ValidationError):
            LLMProviderConfig.model_validate(bad)


class TestSecretHygiene:
    def test_mask_secret_never_leaks_value(self):
        masked = mask_secret("sk-super-secret-key")
        assert "super-secret" not in masked
        assert masked.startswith("<redacted:")

    def test_provider_repr_has_no_api_key(self):
        p = LLMProviderConfig.model_validate(VALID_PROVIDER)
        r = repr(p)
        assert "sk-test-123" not in r
        assert "<redacted>" in r

    def test_secrets_report_masks_everything(self):
        s = _settings()
        report = s.secrets_report()
        assert "test-key" not in report["ETHERSCAN_API_KEY"]
        assert "ghp-test" not in report["GITHUB_TOKEN"]


class TestStartupValidation:
    def test_full_config_passes(self):
        validate_runtime_settings(_settings())

    def test_missing_multiple_settings_reports_all(self):
        s = Settings(
            _env_file=None,
            INFURA_ETH_ENDPOINT="",
            ETHERSCAN_API_KEY="",
            GITHUB_TOKEN="",
            GITHUB_REPO="",
            LLM_PROVIDERS_JSON="[]",
        )
        with pytest.raises(SettingsError) as exc:
            validate_runtime_settings(s)
        msg = str(exc.value)
        assert "INFURA_ETH_ENDPOINT" in msg
        assert "ETHERSCAN_API_KEY" in msg
        assert "GITHUB_TOKEN" in msg
        assert "LLM_PROVIDERS_JSON" in msg

    def test_payments_enabled_without_sdk_fails_closed(self):
        s = _settings(PAYMENTS_ENABLED=True, X402_SDK_VERSION="")
        with pytest.raises(SettingsError, match="X402_SDK_VERSION"):
            validate_runtime_settings(s)

    def test_payments_enabled_with_wrong_pinned_version_fails_closed(self):
        s = _settings(
            PAYMENTS_ENABLED=True,
            X402_SDK_VERSION="0.0.0",
            X402_PAY_TO="0x" + "ab" * 20,
        )
        with pytest.raises(SettingsError, match="does not match installed x402"):
            validate_runtime_settings(s)

    def test_payments_enabled_requires_pay_to(self):
        s = _settings(PAYMENTS_ENABLED=True)  # default pin matches installed SDK
        with pytest.raises(SettingsError, match="X402_PAY_TO"):
            validate_runtime_settings(s)

    def test_payments_enabled_testnet_only_by_default(self):
        s = _settings(
            PAYMENTS_ENABLED=True,
            X402_SDK_VERSION="2.25.0",
            X402_PAY_TO="0x" + "ab" * 20,
            X402_NETWORK="eip155:8453",  # Base mainnet
        )
        with pytest.raises(SettingsError, match="X402_ALLOW_MAINNET"):
            validate_runtime_settings(s)
        ok = _settings(
            PAYMENTS_ENABLED=True,
            X402_SDK_VERSION="2.25.0",
            X402_PAY_TO="0x" + "ab" * 20,
            X402_NETWORK="eip155:84532",  # Base Sepolia testnet
        )
        validate_runtime_settings(ok)

    def test_payments_enabled_mainnet_opt_in_allowed(self):
        s = _settings(
            PAYMENTS_ENABLED=True,
            X402_SDK_VERSION="2.25.0",
            X402_PAY_TO="0x" + "ab" * 20,
            X402_NETWORK="eip155:8453",
            X402_ALLOW_MAINNET=True,
        )
        validate_runtime_settings(s)

    def test_optional_groups_can_be_relaxed(self):
        s = Settings(
            _env_file=None,
            INFURA_ETH_ENDPOINT="",
            ETHERSCAN_API_KEY="",
            LLM_PROVIDERS_JSON="[]",
            GITHUB_TOKEN="",
            GITHUB_REPO="",
        )
        # LLM+GitHub not required in this profile; RPC/Etherscan still required.
        with pytest.raises(SettingsError, match="INFURA"):
            validate_runtime_settings(s, require_llm=False, require_github=False)
        with pytest.raises(SettingsError, match="ETHERSCAN"):
            validate_runtime_settings(s, require_llm=False, require_github=False)


class TestRedisUrlResolution:
    """effective_redis_url must detect every Vercel/Upstash env layout."""

    def test_direct_redis_url_wins(self):
        s = _settings(
            REDIS_URL="rediss://default:secret@upstash.example:6379",
            KV_URL="redis://other:6379",
        )
        assert s.effective_redis_url == "rediss://default:secret@upstash.example:6379"

    def test_kv_url_fallback(self):
        s = _settings(KV_URL="redis://kv.example:6379/0")
        assert s.effective_redis_url == "redis://kv.example:6379/0"

    def test_storage_url_fallback(self):
        s = _settings(STORAGE_URL="rediss://default:p@storage.example:6379")
        assert s.effective_redis_url == "rediss://default:p@storage.example:6379"

    def test_component_vars_assembled_with_tls(self):
        s = _settings(REDIS_HOST="smart-mammuth-12345.upstash.io", REDIS_PORT="6379", REDIS_PASSWORD="topsecret")
        assert s.effective_redis_url == (
            "rediss://default:topsecret@smart-mammuth-12345.upstash.io:6379"
        )

    def test_component_vars_default_port(self):
        s = _settings(REDIS_HOST="h.example", REDIS_PASSWORD="pw")
        assert s.effective_redis_url == "rediss://default:pw@h.example:6379"

    def test_rest_only_credentials_rejected_with_guidance(self):
        # REST tokens cannot authenticate the TCP client; must fail loudly.
        s = _settings(
            UPSTASH_REDIS_REST_URL="https://smart-mammuth-12345.upstash.io",
            UPSTASH_REDIS_REST_TOKEN="AX-rest-token",
        )
        with pytest.raises(SettingsError, match="REDIS_URL"):
            _ = s.effective_redis_url

    def test_kv_rest_only_credentials_rejected(self):
        s = _settings(
            KV_REST_API_URL="https://kv.example",
            KV_REST_API_TOKEN="kv-rest-token",
        )
        with pytest.raises(SettingsError, match="REDIS_URL"):
            _ = s.effective_redis_url

    def test_no_redis_config_yields_empty(self):
        assert _settings().effective_redis_url == ""


class TestResolvedTaskStore:
    """Auto-selection: redis when a Redis URL exists, else sqlite."""

    def test_explicit_sqlite_wins_even_with_redis(self):
        s = _settings(TASK_STORE="sqlite", REDIS_URL="redis://h:6379")
        assert s.resolved_task_store == "sqlite"

    def test_explicit_redis_wins(self):
        s = _settings(TASK_STORE="redis", REDIS_URL="redis://h:6379")
        assert s.resolved_task_store == "redis"

    def test_auto_redis_when_url_present(self):
        s = _settings(REDIS_URL="rediss://default:p@h:6379")
        assert s.resolved_task_store == "redis"

    def test_auto_sqlite_when_no_redis(self):
        assert _settings().resolved_task_store == "sqlite"

    def test_invalid_explicit_store_rejected(self):
        with pytest.raises(ValidationError, match="TASK_STORE"):
            _settings(TASK_STORE="memcached")
