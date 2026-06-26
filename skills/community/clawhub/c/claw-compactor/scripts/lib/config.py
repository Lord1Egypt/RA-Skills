"""Configuration management for claw-compactor.

Loads settings from claw-compactor-config.json in the workspace root,
falling back to sensible defaults.

Also provides load_engram_config() for the Engram (Layer 6) subsystem,
reading engram.yaml (or engram.json as fallback) with env-var overrides
and .env file fallback.

Part of claw-compactor. License: MIT.
"""

import json
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger("claw-compactor.config")

DEFAULT_CONFIG: Dict[str, Any] = {
    "chars_per_token": 4,
    "level0_max_tokens": 200,
    "level1_max_tokens": 500,
    "dedup_similarity_threshold": 0.6,
    "dedup_shingle_size": 3,
    "dedup_max_results": 50,
    "dedup_min_line_length": 20,
    "compress_min_tokens": 50,
    "compress_target_ratio": 0.4,
    "date_format": "%Y-%m-%d",
    "memory_dir": "memory",
    "memory_file": "MEMORY.md",
    "summary_tiers_file": "memory/summary-tiers.md",
    "compressed_suffix": ".compressed.md",
    "log_level": "INFO",
}

CONFIG_FILENAME = "claw-compactor-config.json"


@dataclass
class MemCompressConfig:
    """Runtime configuration for claw-compactor."""

    chars_per_token: int = DEFAULT_CONFIG["chars_per_token"]
    level0_max_tokens: int = DEFAULT_CONFIG["level0_max_tokens"]
    level1_max_tokens: int = DEFAULT_CONFIG["level1_max_tokens"]
    dedup_similarity_threshold: float = DEFAULT_CONFIG["dedup_similarity_threshold"]
    dedup_shingle_size: int = DEFAULT_CONFIG["dedup_shingle_size"]
    dedup_max_results: int = DEFAULT_CONFIG["dedup_max_results"]
    dedup_min_line_length: int = DEFAULT_CONFIG["dedup_min_line_length"]
    compress_min_tokens: int = DEFAULT_CONFIG["compress_min_tokens"]
    compress_target_ratio: float = DEFAULT_CONFIG["compress_target_ratio"]
    date_format: str = DEFAULT_CONFIG["date_format"]
    memory_dir: str = DEFAULT_CONFIG["memory_dir"]
    memory_file: str = DEFAULT_CONFIG["memory_file"]
    summary_tiers_file: str = DEFAULT_CONFIG["summary_tiers_file"]
    compressed_suffix: str = DEFAULT_CONFIG["compressed_suffix"]
    log_level: str = DEFAULT_CONFIG["log_level"]


def _deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge *override* into *base* (non-destructive)."""
    result = dict(base)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def _load_dotenv(env_path: Path) -> None:
    """Load KEY=VALUE pairs from *env_path* into os.environ (skips if exists)."""
    if not env_path.exists():
        return
    try:
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip())
    except OSError:
        pass


def load_engram_config(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """Load Engram configuration with priority: env vars > YAML/JSON > .env > defaults.

    Search order for the config file (when *config_path* is not given):
      1. $ENGRAM_CONFIG env var
      2. ./engram.yaml  (relative to claw-compactor root, auto-detected)
      3. ./engram.json

    Returns a flat-ish dict that EngramEngine / engram_auto.py can consume.
    All path values are expanded (~ / $HOME).

    Env-var overrides (any of these set → take precedence over YAML):
      ENGRAM_MODEL         → llm.model
      ENGRAM_MAX_TOKENS    → llm.max_tokens
      OPENAI_BASE_URL      → llm.base_url  (for openai-compatible provider)
      ENGRAM_PROVIDER      → llm.provider
      ENGRAM_OBSERVER_THRESHOLD   → threads.default.observer_threshold
      ENGRAM_REFLECTOR_THRESHOLD  → threads.default.reflector_threshold
      ENGRAM_MAX_WORKERS   → concurrency.max_workers
      ENGRAM_SCAN_DIR      → sessions.scan_dir
      ENGRAM_STORAGE_DIR   → storage.base_dir
    """
    # ------------------------------------------------------------------ #
    # 0. Locate claw-compactor root                                       #
    # ------------------------------------------------------------------ #
    here = Path(__file__).resolve().parent.parent.parent  # scripts/lib → root

    # ------------------------------------------------------------------ #
    # 1. Load .env first (lowest priority, sets env vars for everything)  #
    # ------------------------------------------------------------------ #
    _load_dotenv(here / ".env")

    # ------------------------------------------------------------------ #
    # 2. Defaults                                                         #
    # ------------------------------------------------------------------ #
    defaults: Dict[str, Any] = {
        "llm": {
            "provider": "openai-compatible",
            "base_url": "https://api.openai.com",
            "api_key_env": "OPENAI_API_KEY",
            "model": "gpt-4o",
            "max_tokens": 4096,
        },
        "threads": {
            "default": {
                "observer_threshold": 30000,
                "reflector_threshold": 40000,
            }
        },
        "sessions": {
            "scan_dir": "~/.openclaw/agents/main/sessions",
            "max_age_hours": 48,
        },
        "storage": {
            "base_dir": "~/.openclaw/workspace/memory/engram",
        },
        "concurrency": {
            "max_workers": 4,
        },
        "logging": {
            "level": "INFO",
        },
    }

    # ------------------------------------------------------------------ #
    # 3. Find and load config file                                        #
    # ------------------------------------------------------------------ #
    cfg: Dict[str, Any] = dict(defaults)

    if config_path is None:
        env_cfg = os.environ.get("ENGRAM_CONFIG", "")
        if env_cfg:
            config_path = Path(env_cfg).expanduser()
        else:
            for candidate in [here / "engram.yaml", here / "engram.json"]:
                if candidate.exists():
                    config_path = candidate
                    break

    if config_path and config_path.exists():
        try:
            text = config_path.read_text(encoding="utf-8")
            if config_path.suffix in (".yaml", ".yml"):
                try:
                    import yaml  # type: ignore[import]
                    file_cfg = yaml.safe_load(text) or {}
                except ImportError:
                    logger.warning(
                        "PyYAML not available; ignoring %s. "
                        "Install pyyaml or rename to engram.json.",
                        config_path,
                    )
                    file_cfg = {}
            else:
                file_cfg = json.loads(text) if text.strip() else {}

            if isinstance(file_cfg, dict):
                cfg = _deep_merge(defaults, file_cfg)
                logger.debug("Engram config loaded from %s", config_path)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to load Engram config %s: %s — using defaults", config_path, exc)
    else:
        logger.debug("No engram.yaml / engram.json found; using defaults + env vars")

    # ------------------------------------------------------------------ #
    # 4. Env-var overrides (highest priority)                             #
    # ------------------------------------------------------------------ #
    _env = os.environ

    if _env.get("ENGRAM_PROVIDER"):
        cfg["llm"]["provider"] = _env["ENGRAM_PROVIDER"]
    if _env.get("OPENAI_BASE_URL"):
        cfg["llm"]["base_url"] = _env["OPENAI_BASE_URL"]
    if _env.get("ENGRAM_MODEL"):
        cfg["llm"]["model"] = _env["ENGRAM_MODEL"]
    if _env.get("ENGRAM_MAX_TOKENS"):
        try:
            cfg["llm"]["max_tokens"] = int(_env["ENGRAM_MAX_TOKENS"])
        except ValueError:
            pass
    if _env.get("ENGRAM_OBSERVER_THRESHOLD"):
        try:
            cfg["threads"]["default"]["observer_threshold"] = int(_env["ENGRAM_OBSERVER_THRESHOLD"])
        except ValueError:
            pass
    if _env.get("ENGRAM_REFLECTOR_THRESHOLD"):
        try:
            cfg["threads"]["default"]["reflector_threshold"] = int(_env["ENGRAM_REFLECTOR_THRESHOLD"])
        except ValueError:
            pass
    if _env.get("ENGRAM_MAX_WORKERS"):
        try:
            cfg["concurrency"]["max_workers"] = int(_env["ENGRAM_MAX_WORKERS"])
        except ValueError:
            pass
    if _env.get("ENGRAM_SCAN_DIR"):
        cfg["sessions"]["scan_dir"] = _env["ENGRAM_SCAN_DIR"]
    if _env.get("ENGRAM_STORAGE_DIR"):
        cfg["storage"]["base_dir"] = _env["ENGRAM_STORAGE_DIR"]

    # Expand ~ in paths
    cfg["sessions"]["scan_dir"] = str(Path(cfg["sessions"]["scan_dir"]).expanduser())
    cfg["storage"]["base_dir"] = str(Path(cfg["storage"]["base_dir"]).expanduser())

    return cfg


def engram_engine_kwargs(engram_cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Convert load_engram_config() output into EngramEngine constructor kwargs."""
    llm = engram_cfg.get("llm", {})
    thread_defaults = engram_cfg.get("threads", {}).get("default", {})

    # Resolve API key from the named env var
    api_key_env = llm.get("api_key_env", "OPENAI_API_KEY")
    api_key = os.environ.get(api_key_env, "")

    provider = llm.get("provider", "openai-compatible")
    if provider == "anthropic":
        anthropic_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        openai_key = ""
        openai_url = ""
    else:
        anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
        openai_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        openai_url = llm.get("base_url", "")

    return {
        "observer_threshold": thread_defaults.get("observer_threshold", 30000),
        "reflector_threshold": thread_defaults.get("reflector_threshold", 40000),
        "model": llm.get("model"),
        "max_tokens": llm.get("max_tokens", 4096),
        "anthropic_api_key": anthropic_key,
        "openai_api_key": openai_key,
        "openai_base_url": openai_url,
    }


def load_config(workspace: Path) -> MemCompressConfig:
    """Load configuration from *workspace*/claw-compactor-config.json.

    Returns default config if the file is missing, empty, or invalid.
    """
    config_path = workspace / CONFIG_FILENAME
    if not config_path.exists():
        return MemCompressConfig()
    try:
        text = config_path.read_text(encoding="utf-8").strip()
        if not text:
            return MemCompressConfig()
        data = json.loads(text)
        if not isinstance(data, dict):
            logger.warning("Config is not a JSON object, using defaults")
            return MemCompressConfig()
        # Filter to known fields only
        known = {f.name for f in MemCompressConfig.__dataclass_fields__.values()}
        filtered = {k: v for k, v in data.items() if k in known}
        return MemCompressConfig(**filtered)
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        logger.warning("Invalid config %s: %s — using defaults", config_path, exc)
        return MemCompressConfig()
