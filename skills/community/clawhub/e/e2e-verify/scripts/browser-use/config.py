"""
browser-use LLM configuration — provider agnostic.

Auto-detects your LLM provider from standard environment variables.
Override anything with BROWSER_USE_LLM_* env vars.

Supported providers (set the standard env var and it just works):
  ┌──────────────────────┬──────────────────────────┬───────────────────────────────────────────────────┐
  │ Provider             │ Env var                  │ Default model                                     │
  ├──────────────────────┼──────────────────────────┼───────────────────────────────────────────────────┤
  │ OpenAI               │ OPENAI_API_KEY           │ gpt-4o                                            │
  │ Anthropic            │ ANTHROPIC_API_KEY        │ claude-sonnet-4-20250514                          │
  │ Google Gemini        │ GEMINI_API_KEY           │ gemini-2.5-flash                                  │
  │ Alibaba DashScope    │ DASHSCOPE_API_KEY        │ qwen-max                                          │
  │ Groq                 │ GROQ_API_KEY             │ llama-3.3-70b-versatile                           │
  │ OpenRouter           │ OPENROUTER_API_KEY       │ openai/gpt-4o                                     │
  │ Ollama (local, free) │ (none needed)            │ llama3.1                                          │
  │ Any OpenAI-compat    │ BROWSER_USE_LLM_KEY +    │ (set via BROWSER_USE_LLM_MODEL)                   │
  │                      │ BROWSER_USE_LLM_BASE_URL │                                                   │
  └──────────────────────┴──────────────────────────┴───────────────────────────────────────────────────┘

Priority order (first match wins):
  1. Explicit override: BROWSER_USE_LLM_KEY + BROWSER_USE_LLM_BASE_URL
  2. Single provider key set in environment
  3. If multiple provider keys are set, use BROWSER_USE_LLM_MODEL or BROWSER_USE_LLM_KEY to disambiguate
  4. Ollama local fallback (no key needed)

To use: set one provider's env var in your shell or .env, then import this module.
"""
import os
from pathlib import Path


def _load_dotenv():
    """Load .env file from CWD or home if present (minimal, no deps)."""
    for env_path in [Path.cwd() / ".env", Path.home() / ".env"]:
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip("'\""))


_load_dotenv()

# --- Provider definitions ---
# Each entry: (env_var_name, default_base_url, default_model)
_PROVIDERS = [
    ("OPENAI_API_KEY",     "https://api.openai.com/v1",                               "gpt-4o"),
    ("ANTHROPIC_API_KEY",  "https://api.anthropic.com/v1",                            "claude-sonnet-4-20250514"),
    ("GEMINI_API_KEY",     "https://generativelanguage.googleapis.com/v1beta/openai",  "gemini-2.5-flash"),
    ("DASHSCOPE_API_KEY",  "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",  "qwen-max"),
    ("GROQ_API_KEY",       "https://api.groq.com/openai/v1",                          "llama-3.3-70b-versatile"),
    ("OPENROUTER_API_KEY", "https://openrouter.ai/api/v1",                            "openai/gpt-4o"),
]

_OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
_OLLAMA_MODEL = "llama3.1"


def _detect_provider():
    """Return (api_key, base_url, model) based on environment variables."""
    # 1. Explicit override wins absolutely
    explicit_key = os.environ.get("BROWSER_USE_LLM_KEY")
    explicit_url = os.environ.get("BROWSER_USE_LLM_BASE_URL")
    explicit_model = os.environ.get("BROWSER_USE_LLM_MODEL")

    if explicit_key and explicit_url:
        return explicit_key, explicit_url, explicit_model or "gpt-4o"

    # 2. Find which provider keys are actually set
    available = [
        (os.environ.get(var), url, model)
        for var, url, model in _PROVIDERS
        if os.environ.get(var)
    ]

    # 3. If exactly one provider key is set, use it
    if len(available) == 1:
        key, url, default_model = available[0]
        return key, url, explicit_model or default_model

    # 4. If multiple keys are set, we need a disambiguator.
    #    If BROWSER_USE_LLM_MODEL is set, try to match it to a known provider
    #    by checking if the model name appears in any provider's default model.
    if len(available) > 1 and explicit_model:
        for key, url, default_model in available:
            # Match by checking if either model contains the other's core identifier
            # e.g. "gpt-4o-mini" matches provider default "gpt-4o" (OpenAI)
            model_core = default_model.split("/")[-1].split("-")[0]
            requested_core = explicit_model.split("/")[-1].split("-")[0]
            if model_core == requested_core:
                return key, url, explicit_model
        # Model didn't match any provider — use the first available with the explicit model
        key, url, _ = available[0]
        return key, url, explicit_model

    # 5. If multiple keys are set with no disambiguator, warn and use the first (priority order)
    if len(available) > 1:
        import warnings

        set_vars = [var for var, _, _ in _PROVIDERS if os.environ.get(var)]
        warnings.warn(
            f"Multiple LLM provider keys detected: {', '.join(set_vars)}. "
            f"Using {set_vars[0]} (priority order). To choose a specific provider, "
            f"set BROWSER_USE_LLM_KEY + BROWSER_USE_LLM_BASE_URL, or unset the keys you don't want."
        )
        key, url, default_model = available[0]
        return key, url, explicit_model or default_model

    # 6. No provider keys set — try Ollama (local, free)
    return "ollama", _OLLAMA_BASE_URL, explicit_model or _OLLAMA_MODEL


API_KEY, BASE_URL, MODEL = _detect_provider()

# Sanity check — only warn if NO provider key was set AND Ollama isn't reachable.
# Ollama needs no API key, so the "ollama" fallback is intentional, not an error.
if API_KEY == "ollama":
    import urllib.request
    import urllib.error

    try:
        urllib.request.urlopen(f"{_OLLAMA_BASE_URL.replace('/v1', '')}/api/tags", timeout=1)
    except (urllib.error.URLError, ConnectionError, OSError):
        import warnings

        warnings.warn(
            "No LLM API key detected and Ollama is not reachable at "
            f"{_OLLAMA_BASE_URL}. Set one of: OPENAI_API_KEY, ANTHROPIC_API_KEY, "
            "GEMINI_API_KEY, DASHSCOPE_API_KEY, GROQ_API_KEY, OPENROUTER_API_KEY, "
            "or BROWSER_USE_LLM_KEY + BROWSER_USE_LLM_BASE_URL.\n"
            "Or install Ollama: https://ollama.com"
        )
