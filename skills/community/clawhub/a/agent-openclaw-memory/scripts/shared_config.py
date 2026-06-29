"""
shared_config.py — Centralized configuration (single source of truth)

All scripts read paths, URLs, and keys from here.
Config priority: environment variables > config.json > defaults.

Usage:
    from shared_config import VAULT_DIR, LMSTUDIO_EMBED_URL, LMSTUDIO_KEY, QDRANT_URL
"""

import json
import os
from pathlib import Path

# ── Paths ──
SCRIPTS_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPTS_DIR.parent
CONFIG_FILE = SCRIPTS_DIR / "config.json"
WORKSPACE_DIR = SKILL_DIR.parent.parent  # ~/.openclaw/workspace
DATA_DIR = SKILL_DIR / "data"
MEMORY_DIR = WORKSPACE_DIR / "memory"

# ── Load config.json ──
_config_cache = None

def _load_config():
    global _config_cache
    if _config_cache is not None:
        return _config_cache
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8-sig") as f:
            _config_cache = json.load(f)
    else:
        _config_cache = {}
    return _config_cache

# ── Also try loading openclaw.json for provider configs ──
_openclaw_config_cache = None

def _load_openclaw_config():
    global _openclaw_config_cache
    if _openclaw_config_cache is not None:
        return _openclaw_config_cache
    openclaw_json = Path.home() / ".openclaw" / "openclaw.json"
    if openclaw_json.exists():
        try:
            with open(openclaw_json, "r", encoding="utf-8-sig") as f:
                _openclaw_config_cache = json.load(f)
        except Exception:
            _openclaw_config_cache = {}
    else:
        _openclaw_config_cache = {}
    return _openclaw_config_cache

def _get_provider_config(provider_name: str) -> dict:
    cfg = _load_openclaw_config()
    return cfg.get("models", {}).get("providers", {}).get(provider_name, {})

# ── Vault path ──
VAULT_DIR = Path(
    os.environ.get("OPENCLAW_VAULT_DIR")
    or _load_config().get("vault_dir")
    or _load_openclaw_config().get("vaultDir")
    or str(Path.home() / "vault")
)

# ── LM Studio / Embedding server config ──
_cfg = _load_config()
_lm_cfg = _cfg.get("embedder", {})

# Try openclaw.json lmstudio provider first, then config.json embedder
_lm_provider = _get_provider_config("lmstudio")

LMSTUDIO_BASE_URL = (
    os.environ.get("OPENCLAW_LMSTUDIO_URL")
    or _lm_cfg.get("baseUrl")
    or _lm_provider.get("baseUrl", "http://localhost:1234/v1")
)
LMSTUDIO_KEY = (
    os.environ.get("OPENCLAW_LMSTUDIO_KEY")
    or _lm_cfg.get("apiKey")
    or _lm_provider.get("apiKey", "")
)
# Ensure /v1 prefix for OpenAI-compatible endpoints
_base = LMSTUDIO_BASE_URL.rstrip("/")
if not _base.endswith("/v1"):
    _base = _base + "/v1"
LMSTUDIO_MODELS_URL = f"{_base}/models"
LMSTUDIO_EMBED_URL = f"{_base}/embeddings"
LMSTUDIO_CHAT_URL = f"{_base}/chat/completions"

# ── Embedding model ──
EMBED_MODEL = (
    os.environ.get("OPENCLAW_EMBED_MODEL")
    or _lm_cfg.get("model", "text-embedding-nomic-embed-text-v1.5")
)

# ── LLM config ──
_llm_cfg = _cfg.get("llm", {})
LLM_BASE_URL = (
    os.environ.get("OPENCLAW_LLM_URL")
    or _llm_cfg.get("baseUrl", "https://api.deepseek.com/v1")
)
LLM_API_KEY = (
    os.environ.get("OPENCLAW_LLM_KEY")
    or _llm_cfg.get("apiKey", "")
)
LLM_MODEL = (
    os.environ.get("OPENCLAW_LLM_MODEL")
    or _llm_cfg.get("model", "deepseek-chat")
)

# ── Qdrant config ──
_qdrant_cfg = _cfg.get("qdrant", {})
QDRANT_HOST = os.environ.get("OPENCLAW_QDRANT_HOST", _qdrant_cfg.get("host", "localhost"))
QDRANT_PORT = int(os.environ.get("OPENCLAW_QDRANT_PORT", _qdrant_cfg.get("port", 6333)))
QDRANT_URL = f"http://{QDRANT_HOST}:{QDRANT_PORT}"
KB_COLLECTION = os.environ.get("OPENCLAW_QDRANT_COLLECTION", _qdrant_cfg.get("collection", "knowledge_base"))

# ── Sync config ──
SYNC_DIRS = _cfg.get("sync_dirs", ["01-日记", "02-知识", "04-教训", "07-项目"])
MAX_FILE_SIZE_KB = _cfg.get("max_file_size_kb", 50)
EMBEDDING_WORKERS = _cfg.get("embedding_workers", 4)


def validate():
    """Check if key configs are set. Returns list of issues."""
    issues = []
    if not CONFIG_FILE.exists():
        issues.append(f"config.json not found at {CONFIG_FILE} (copy from config.template.json)")
    if not LMSTUDIO_KEY:
        issues.append("Embedding server API key not configured")
    if not LLM_API_KEY:
        issues.append("LLM API key not configured")
    if VAULT_DIR and not Path(VAULT_DIR).exists():
        issues.append(f"VAULT_DIR does not exist: {VAULT_DIR}")
    return issues


if __name__ == "__main__":
    print(f"VAULT_DIR:       {VAULT_DIR}")
    print(f"LMSTUDIO_URL:    {LMSTUDIO_EMBED_URL}")
    print(f"EMBED_MODEL:     {EMBED_MODEL}")
    print(f"LLM_URL:         {LLM_BASE_URL}")
    print(f"LLM_MODEL:       {LLM_MODEL}")
    print(f"QDRANT_URL:      {QDRANT_URL}")
    print(f"KB_COLLECTION:   {KB_COLLECTION}")
    print(f"SYNC_DIRS:       {SYNC_DIRS}")
    print(f"CONFIG_FILE:     {CONFIG_FILE}")

    issues = validate()
    if issues:
        print(f"\n⚠️  Configuration issues:")
        for i in issues:
            print(f"  - {i}")
    else:
        print(f"\n✅ Configuration complete")
