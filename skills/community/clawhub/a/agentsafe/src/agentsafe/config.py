"""Typed, validated settings. Missing required settings must fail loudly,
never silently fall back to fake values. API keys are never logged.
"""

from __future__ import annotations

import json
import logging
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from agentsafe.schemas import normalize_address

logger = logging.getLogger("agentSAFE.config")


class SettingsError(ValueError):
    """Raised when configuration is missing or out of allowed range."""


def mask_secret(value: str | None) -> str:
    """Log-safe representation of any secret. Never emits the value."""
    if not value:
        return "<empty>"
    return f"<redacted:{len(value)} chars>"


class LLMProviderConfig(BaseModel):
    """One OpenAI-compatible provider. Actual endpoints/model IDs/quotas must be
    verified at deployment time; this config makes no capacity promises."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=64)
    base_url: str = Field(min_length=1)
    api_key: str = Field(min_length=1)
    model: str = Field(min_length=1)
    rpm_limit: int = Field(ge=1, le=10_000)
    max_output_tokens: int | None = Field(default=None, ge=100, le=200_000)

    @field_validator("base_url")
    @classmethod
    def _validate_base_url(cls, v: str) -> str:
        if not v.startswith(("http://", "https://")):
            raise ValueError(f"base_url must be an http(s) URL, got {v!r}")
        return v.rstrip("/")

    def safe_repr(self) -> dict[str, Any]:
        """Representation safe for logs: never includes api_key."""
        return {
            "name": self.name,
            "base_url": self.base_url,
            "model": self.model,
            "rpm_limit": self.rpm_limit,
            "api_key": "<redacted>",
        }

    def __repr__(self) -> str:  # pragma: no cover - repr safety guard
        return f"LLMProviderConfig({self.safe_repr()})"

    __str__ = __repr__


class Settings(BaseSettings):
    """All runtime settings. Loaded from environment and optional .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    # --- Ethereum Mainnet ---
    INFURA_ETH_ENDPOINT: str = ""
    ETHERSCAN_API_KEY: str = ""
    ETHERSCAN_BASE_URL: str = "https://api.etherscan.io/v2/api"

    # --- LLM ---
    LLM_PROVIDERS_JSON: str = "[]"
    LLM_GLOBAL_RPM: int = Field(default=10, ge=1, le=1_000)
    LLM_MAX_CALLS_PER_AUDIT: int = Field(default=12, ge=1, le=1_000)
    LLM_MAX_RETRIES_PER_CALL: int = Field(default=2, ge=0, le=10)
    LLM_REQUEST_TIMEOUT_SECONDS: float = Field(default=90.0, ge=1.0, le=600.0)
    LLM_MAX_OUTPUT_TOKENS: int = Field(default=3_000, ge=100, le=100_000)

    # --- GitHub Actions worker ---
    GITHUB_TOKEN: str = ""
    GITHUB_REPO: str = ""
    GITHUB_WORKFLOW_FILE: str = "audit.yml"
    GITHUB_REF: str = "main"
    GITHUB_API_TIMEOUT_SECONDS: float = Field(default=20.0, ge=1.0, le=300.0)
    GITHUB_POLL_INTERVAL_SECONDS: float = Field(default=10.0, ge=1.0, le=600.0)
    AUDIT_TIMEOUT_SECONDS: int = Field(default=900, ge=30, le=7_200)
    MAX_CONCURRENT_AUDITS: int = Field(default=1, ge=1, le=64)

    # --- Artifacts ---
    ARTIFACT_RETENTION_DAYS: int = Field(default=2, ge=1, le=90)

    # --- Task persistence (Prompt 8) ---
    # 'sqlite' only if durable writable storage is guaranteed; otherwise
    # 'memory' + GitHub-side state reconstruction after restarts.
    # 'redis' (Upstash) for serverless deployments like Vercel — persistent
    # across cold starts. '' (default) auto-selects: 'redis' when a Redis URL
    # is detectable in the environment, else 'sqlite' (see resolved_task_store).
    TASK_STORE: str = ""
    TASK_DB_PATH: str = "data/tasks.db"

    # Redis/Upstash configuration for serverless (Vercel) deployments. The
    # Upstash integration injects several layouts depending on version; all
    # are detected by effective_redis_url below. Only RESP (TCP) credentials
    # work with the redis-py client used by RedisTaskStore:
    #   1. REDIS_URL / KV_URL / STORAGE_URL — direct redis:// or rediss:// URL
    #   2. REDIS_HOST + REDIS_PORT + REDIS_PASSWORD — assembled, TLS enforced
    # REST-only credentials (UPSTASH_REDIS_REST_* / KV_REST_API_*) cannot
    # authenticate a TCP connection and are rejected with clear guidance.
    REDIS_URL: str = ""
    KV_URL: str = ""
    STORAGE_URL: str = ""
    REDIS_HOST: str = ""
    REDIS_PORT: str = ""
    REDIS_PASSWORD: str = ""
    UPSTASH_REDIS_REST_URL: str = ""
    UPSTASH_REDIS_REST_TOKEN: str = ""
    KV_REST_API_URL: str = ""
    KV_REST_API_TOKEN: str = ""

    @property
    def effective_redis_url(self) -> str:
        """Resolve a RESP connection URL from every known Vercel/Upstash
        env-var layout. Assembled URLs always use ``rediss://`` (TLS) because
        Upstash endpoints require TLS transport."""
        # Priority 1: direct URLs (any redis:// / rediss:// form).
        for url in (self.REDIS_URL, self.KV_URL, self.STORAGE_URL):
            if url.strip():
                return url.strip()
        # Priority 2: component vars from the Upstash integration.
        host = self.REDIS_HOST.strip()
        if host:
            port = self.REDIS_PORT.strip() or "6379"
            password = self.REDIS_PASSWORD.strip()
            creds = f"default:{password}@" if password else ""
            return f"rediss://{creds}{host}:{port}"
        # Priority 3: REST-only credentials are a hard error - the REST token
        # is NOT the TCP password, so fabricating a rediss:// URL from them
        # would fail authentication at ping time. Fail loudly with guidance.
        rest_pairs = (
            (self.UPSTASH_REDIS_REST_URL, self.UPSTASH_REDIS_REST_TOKEN),
            (self.KV_REST_API_URL, self.KV_REST_API_TOKEN),
        )
        if any(url.strip() and token.strip() for url, token in rest_pairs):
            raise SettingsError(
                "Only Redis REST credentials were found (UPSTASH_REDIS_REST_* / "
                "KV_REST_API_*). REST tokens cannot authenticate the TCP client "
                "used by the task store. Set REDIS_URL to a redis:// or rediss:// "
                "connection string (Vercel's Upstash integration injects it, or "
                "copy it from the Upstash console)."
            )
        return ""

    @property
    def resolved_task_store(self) -> str:
        """Explicit TASK_STORE, or auto-selected backend: 'redis' (serverless-
        safe, survives cold starts) when a Redis URL is detectable, else
        'sqlite' for durable local state."""
        if self.TASK_STORE:
            return self.TASK_STORE
        return "redis" if self.effective_redis_url else "sqlite"

    # --- HTTP access log (PRIVACY_POLICY.md: IP + time, 30-day retention) ---
    ACCESS_LOG_DB_PATH: str = "data/access_log.db"

    # --- Payments (x402, pinned SDK; fail-closed) ---
    # Default: Base Sepolia TESTNET (CAIP-2 eip155:84532). Mainnet payments
    # require X402_ALLOW_MAINNET=true and are only enabled after the
    # end-to-end testnet test suite passes.
    PAYMENTS_ENABLED: bool = False
    X402_NETWORK: str = "eip155:84532"
    X402_PAY_TO: str = ""
    X402_SDK_VERSION: str = "2.25.0"
    X402_FACILITATOR_URL: str = "https://x402.org/facilitator"
    X402_PRICE: str = "$0.01"
    # Flat price advertised by the x402 REST discovery endpoint (POST
    # /api/audit, documented in openapi.json for x402scan indexing). This is
    # the endpoint's own flat fee, separate from the MCP tool's tiered
    # pricing; the REST path only serves contracts up to REST_AUDIT_MAX_LINES
    # (see server.py) so it can never undercut the higher MCP tiers.
    X402_REST_PRICE: str = "$3.00"
    X402_ASSET: str = ""
    X402_MAX_TIMEOUT_SECONDS: int = Field(default=300, ge=1, le=3600)
    X402_ALLOW_MAINNET: bool = False

    # Known x402 networks: testnet first; mainnet is opt-in only.
    X402_NETWORK_TESTNET: ClassVar[str] = "eip155:84532"  # Base Sepolia
    X402_NETWORK_MAINNET: ClassVar[str] = "eip155:8453"  # Base

    # --- Logging ---
    LOG_LEVEL: str = "INFO"

    @field_validator("LOG_LEVEL")
    @classmethod
    def _validate_log_level(cls, v: str) -> str:
        v = v.strip().upper()
        if v not in {"DEBUG", "INFO", "WARNING", "ERROR"}:
            raise ValueError(f"LOG_LEVEL must be DEBUG/INFO/WARNING/ERROR, got {v!r}")
        return v

    @field_validator("GITHUB_REPO")
    @classmethod
    def _validate_repo(cls, v: str) -> str:
        v = v.strip()
        if v and ("/" not in v or v.startswith("/") or v.endswith("/") or len(v.split("/")) != 2):
            raise ValueError(f"GITHUB_REPO must look like 'owner/repo', got {v!r}")
        return v

    @field_validator("GITHUB_WORKFLOW_FILE")
    @classmethod
    def _validate_workflow_file(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("GITHUB_WORKFLOW_FILE must not be empty")
        if v.startswith(("/", "\\")) or ".." in v:
            raise ValueError("GITHUB_WORKFLOW_FILE must be a plain filename like 'audit.yml'")
        return v

    @field_validator("TASK_STORE")
    @classmethod
    def _validate_task_store(cls, v: str) -> str:
        v = v.strip().lower()
        if v not in {"", "sqlite", "memory", "redis"}:
            raise ValueError(
                f"TASK_STORE must be '', 'sqlite', 'memory', or 'redis', got {v!r}"
            )
        return v

    def llm_providers(self) -> list[LLMProviderConfig]:
        """Parse LLM_PROVIDERS_JSON; raise SettingsError on invalid content."""
        raw = (self.LLM_PROVIDERS_JSON or "").strip()
        if not raw:
            return []
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise SettingsError(f"LLM_PROVIDERS_JSON is not valid JSON: {exc}") from exc
        if not isinstance(data, list):
            raise SettingsError("LLM_PROVIDERS_JSON must be a JSON array of provider objects")
        providers: list[LLMProviderConfig] = []
        for i, item in enumerate(data):
            try:
                providers.append(LLMProviderConfig.model_validate(item))
            except Exception as exc:
                raise SettingsError(f"LLM_PROVIDERS_JSON[{i}] invalid: {exc}") from exc
        names = [p.name for p in providers]
        if len(names) != len(set(names)):
            raise SettingsError("LLM provider names must be unique")
        return providers

    def secrets_report(self) -> dict[str, str]:
        """For startup logs: show presence of secrets, never their values."""
        return {
            "ETHERSCAN_API_KEY": mask_secret(self.ETHERSCAN_API_KEY),
            "GITHUB_TOKEN": mask_secret(self.GITHUB_TOKEN),
            "INFURA_ETH_ENDPOINT": "<set>" if self.INFURA_ETH_ENDPOINT else "<empty>",
            "X402_PAY_TO": mask_secret(self.X402_PAY_TO),
        }


def validate_runtime_settings(
    settings: Settings,
    *,
    require_rpc: bool = True,
    require_etherscan: bool = True,
    require_llm: bool = True,
    require_github: bool = True,
) -> None:
    """Fail-fast startup validation. Collects ALL problems, not just the first.

    PAYMENTS_ENABLED=true is only allowed once the pinned-version x402 adapter
    has passed its integration tests (Phase 12); until then startup refuses.
    """
    errors: list[str] = []

    if require_rpc and not settings.INFURA_ETH_ENDPOINT.strip():
        errors.append("INFURA_ETH_ENDPOINT is required (Ethereum Mainnet JSON-RPC endpoint)")
    if require_etherscan and not settings.ETHERSCAN_API_KEY.strip():
        errors.append("ETHERSCAN_API_KEY is required to resolve verified sources")
    if require_llm and not settings.llm_providers():
        errors.append(
            "LLM_PROVIDERS_JSON must contain at least one provider record "
            "(name, base_url, api_key, model, rpm_limit)"
        )
    if require_github:
        if not settings.GITHUB_TOKEN.strip():
            errors.append("GITHUB_TOKEN is required to dispatch audit workflows")
        if not settings.GITHUB_REPO.strip():
            errors.append("GITHUB_REPO is required (owner/repo)")

    if settings.PAYMENTS_ENABLED:
        # Fail-closed: the pinned x402 SDK must be installed and the recorded
        # pin must match the imported version, otherwise startup refuses.
        try:
            import x402  # noqa: PLC0415

            installed_sdk = x402.__version__
        except ImportError:
            installed_sdk = ""
            errors.append(
                "PAYMENTS_ENABLED=true requires the pinned x402 SDK "
                "(pip install 'x402[evm]==2.25.0')"
            )
        if installed_sdk and settings.X402_SDK_VERSION.strip() != installed_sdk:
            errors.append(
                f"X402_SDK_VERSION={settings.X402_SDK_VERSION!r} does not match installed "
                f"x402=={installed_sdk!r}; pin and installed version must agree"
            )
        if not settings.X402_PAY_TO.strip():
            errors.append("PAYMENTS_ENABLED=true requires X402_PAY_TO (payment recipient)")
        else:
            try:
                normalize_address(settings.X402_PAY_TO)
            except ValueError:
                errors.append("X402_PAY_TO must be a valid EVM address")
        network = settings.X402_NETWORK.strip()
        if network != Settings.X402_NETWORK_TESTNET:
            if network != Settings.X402_NETWORK_MAINNET:
                errors.append(
                    f"X402_NETWORK {network!r} is not supported; use Base Sepolia "
                    f"({Settings.X402_NETWORK_TESTNET}) or Base ({Settings.X402_NETWORK_MAINNET})"
                )
            elif not settings.X402_ALLOW_MAINNET:
                errors.append(
                    "X402_NETWORK=Base mainnet requires X402_ALLOW_MAINNET=true and is only "
                    "enabled after end-to-end Base Sepolia tests pass"
                )
        if not settings.X402_PRICE.strip().startswith("$"):
            errors.append("X402_PRICE must be a USD price string like '$0.01'")
        if not settings.X402_FACILITATOR_URL.strip():
            errors.append("PAYMENTS_ENABLED=true requires X402_FACILITATOR_URL")

    if errors:
        raise SettingsError("Invalid configuration:\n- " + "\n- ".join(errors))
