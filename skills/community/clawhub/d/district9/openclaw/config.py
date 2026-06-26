"""Configuration loading and validation for OpenClaw."""

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml

# Default config location
DEFAULT_CONFIG_DIR = Path.home() / ".openclaw-agent"
DEFAULT_CONFIG_PATH = DEFAULT_CONFIG_DIR / "config.yaml"


@dataclass
class WalletConfig:
    private_key: str  # resolved from env var


@dataclass
class LLMConfig:
    provider: str  # "openai" | "anthropic" | "openrouter"
    model: str
    api_key: str  # resolved from env var
    base_url: str | None = None


@dataclass
class StrategyConfig:
    sources: list[str]
    prompt: str
    style: str
    risk_level: str
    max_daily_launches: int
    llm: LLMConfig


@dataclass
class LaunchConfig:
    platform: str
    initial_buy: str
    auto_generate_logo: bool


@dataclass
class OpenClawConfig:
    agent_name: str
    chain: str
    wallet: WalletConfig
    strategy: StrategyConfig
    launch: LaunchConfig
    scan_interval: int
    testnet: bool = False
    log_level: str = "info"


def _resolve_env(env_name: str, label: str) -> str:
    """Resolve an environment variable, raising if not set."""
    value = os.environ.get(env_name)
    if not value:
        raise ValueError(
            f"Environment variable '{env_name}' not set ({label}).\n"
            f"Set it with: export {env_name}=<value>"
        )
    return value


def load_config(path: str | Path | None = None) -> OpenClawConfig:
    """Load and validate config from YAML, resolving env vars."""
    config_path = Path(path) if path else DEFAULT_CONFIG_PATH

    if not config_path.exists():
        raise FileNotFoundError(
            f"Config file not found: {config_path}\n"
            f"Run 'openclaw init' to create one."
        )

    with open(config_path) as f:
        raw = yaml.safe_load(f)

    # Resolve wallet private key
    wallet_key_env = raw["agent"]["wallet"]["private_key_env"]
    wallet_key = _resolve_env(wallet_key_env, "wallet private key")

    # Resolve LLM API key
    llm_cfg = raw["strategy"]["llm"]
    llm_key_env = llm_cfg["api_key_env"]
    llm_key = _resolve_env(llm_key_env, "LLM API key")

    return OpenClawConfig(
        agent_name=raw["agent"]["name"],
        chain=raw["agent"].get("chain", "bnb"),
        wallet=WalletConfig(private_key=wallet_key),
        strategy=StrategyConfig(
            sources=raw["strategy"].get("sources", ["crypto"]),
            prompt=raw["strategy"].get("prompt", ""),
            style=raw["strategy"].get("style", "cultural"),
            risk_level=raw["strategy"].get("risk_level", "medium"),
            max_daily_launches=raw["strategy"].get("max_daily_launches", 3),
            llm=LLMConfig(
                provider=llm_cfg.get("provider", "openai"),
                model=llm_cfg.get("model", "gpt-4o-mini"),
                api_key=llm_key,
                base_url=llm_cfg.get("base_url"),
            ),
        ),
        launch=LaunchConfig(
            platform=raw.get("launch", {}).get("platform", "flap"),
            initial_buy=raw.get("launch", {}).get("initial_buy", "0.01"),
            auto_generate_logo=raw.get("launch", {}).get("auto_generate_logo", True),
        ),
        scan_interval=raw.get("runtime", {}).get("scan_interval", 1800),
        testnet=raw.get("runtime", {}).get("testnet", False),
        log_level=raw.get("runtime", {}).get("log_level", "info"),
    )
