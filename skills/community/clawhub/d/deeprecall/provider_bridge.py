"""
Provider Bridge — Reads OpenClaw's configuration to resolve API keys,
base URLs, and model settings for RLM.

Supports all major OpenClaw providers:
- Anthropic (API key or setup-token)
- OpenAI (API key)
- Google / Gemini (API key, including native Gemini API)
- GitHub Copilot (OAuth token)
- OpenRouter (API key)
- Ollama / local models
- Any provider configured in OpenClaw

The bridge reads from:
1. OpenClaw config: ~/.openclaw/openclaw.json
2. Auth profiles: ~/.openclaw/agents/main/agent/auth-profiles.json
3. Model config: ~/.openclaw/agents/main/agent/models.json
4. Credentials: derived from config or ~/.openclaw/credentials/
5. Environment variables (fallback)
"""

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional


# Default OpenClaw paths
OPENCLAW_DIR = Path(os.environ.get("OPENCLAW_DIR", os.path.expanduser("~/.openclaw")))
CONFIG_FILE = OPENCLAW_DIR / "openclaw.json"
AUTH_PROFILES_FILE = OPENCLAW_DIR / "agents" / "main" / "agent" / "auth-profiles.json"
MODELS_FILE = OPENCLAW_DIR / "agents" / "main" / "agent" / "models.json"
CREDENTIALS_DIR = OPENCLAW_DIR / "credentials"

# Gemini native API base
GEMINI_NATIVE_URL = "https://generativelanguage.googleapis.com/v1beta"

# Provider → OpenAI-compatible base URL mapping
PROVIDER_BASE_URLS = {
    "anthropic": "https://api.anthropic.com/v1",
    "openai": "https://api.openai.com/v1",
    "github-copilot": "https://api.individual.githubcopilot.com",
    "openrouter": "https://openrouter.ai/api/v1",
    "google": "https://generativelanguage.googleapis.com/v1beta/openai",
    "ollama": "http://localhost:11434/v1",
    "minimax": "https://api.minimax.chat/v1",
    "deepseek": "https://api.deepseek.com/v1",
    "zhipu": "https://open.bigmodel.cn/api/paas/v4",
    "moonshot": "https://api.moonshot.cn/v1",
    "qwen": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "mistral": "https://api.mistral.ai/v1",
    "together": "https://api.together.xyz/v1",
    "groq": "https://api.groq.com/openai/v1",
    "fireworks": "https://api.fireworks.ai/inference/v1",
    "cohere": "https://api.cohere.com/v1",
    "perplexity": "https://api.perplexity.ai",
    "sambanova": "https://api.sambanova.ai/v1",
    "cerebras": "https://api.cerebras.ai/v1",
    "xai": "https://api.x.ai/v1",
}

# Provider → environment variable for API key
PROVIDER_ENV_KEYS = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "google": "GOOGLE_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "minimax": "MINIMAX_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "zhipu": "ZHIPU_API_KEY",
    "moonshot": "MOONSHOT_API_KEY",
    "qwen": "DASHSCOPE_API_KEY",
    "mistral": "MISTRAL_API_KEY",
    "together": "TOGETHER_API_KEY",
    "groq": "GROQ_API_KEY",
    "fireworks": "FIREWORKS_API_KEY",
    "cohere": "COHERE_API_KEY",
    "perplexity": "PERPLEXITY_API_KEY",
    "sambanova": "SAMBANOVA_API_KEY",
    "cerebras": "CEREBRAS_API_KEY",
    "xai": "XAI_API_KEY",
    "ollama": None,  # Ollama typically doesn't need a key
}


class ProviderConfig:
    """Resolved provider configuration for RLM."""

    def __init__(self, provider: str, api_key: str, base_url: str,
                 primary_model: str, default_headers: Optional[dict] = None):
        self.provider = provider
        self.api_key = api_key
        self.base_url = base_url
        self.primary_model = primary_model
        self.default_headers = default_headers or {}

    def __repr__(self):
        if not self.api_key:
            key_preview = "[NOT SET]"
        elif len(self.api_key) > 8:
            key_preview = self.api_key[:4] + "..." + self.api_key[-4:]
        else:
            key_preview = "***"
        return (f"ProviderConfig(provider={self.provider}, key={key_preview}, "
                f"base_url={self.base_url}, model={self.primary_model})")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _load_json(path: Path) -> dict:
    """Safely load a JSON file, returning empty dict on failure."""
    try:
        if path.exists():
            with open(path) as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        pass
    return {}


def _get_primary_model(config: dict) -> Optional[str]:
    """Extract the primary model from OpenClaw config."""
    return (config
            .get("agents", {})
            .get("defaults", {})
            .get("model", {})
            .get("primary"))


def _get_provider_from_model(model_id: str) -> Optional[str]:
    """Extract provider name from a model ID like 'anthropic/claude-opus-4'."""
    if "/" in model_id:
        return model_id.split("/")[0]
    return None


def _get_api_key_from_env(provider: str) -> Optional[str]:
    """Try to get API key from environment variables."""
    env_key = PROVIDER_ENV_KEYS.get(provider)
    if env_key:
        return os.environ.get(env_key)
    return None


def _get_api_key_from_config(config: dict, provider: str) -> Optional[str]:
    """Try to get API key from OpenClaw config (env section or provider config)."""
    env_section = config.get("env", {})
    env_key = PROVIDER_ENV_KEYS.get(provider)
    if env_key and env_key in env_section:
        return env_section[env_key]

    providers = config.get("models", {}).get("providers", {})
    provider_conf = providers.get(provider, {})
    return provider_conf.get("apiKey")


def _get_copilot_token(openclaw_config: Optional[dict] = None) -> Optional[str]:
    """Read GitHub Copilot API token, deriving credentials path from config."""
    try:
        config = openclaw_config if openclaw_config is not None else _load_json(CONFIG_FILE)

        # Derive credentials directory from config, fall back to module default.
        # Relative paths are resolved relative to OPENCLAW_DIR.
        creds_dir_override = config.get("credentialsDir")
        if creds_dir_override:
            p = Path(creds_dir_override)
            creds_dir = p if p.is_absolute() else OPENCLAW_DIR / p
        else:
            creds_dir = CREDENTIALS_DIR

        token_file = creds_dir / "github-copilot.token.json"
        if not token_file.exists():
            return None

        with open(token_file) as f:
            data = json.load(f)

        token = data.get("token")
        expires_at = data.get("expiresAt", 0)

        if expires_at:
            now = time.time()
            # Auto-detect seconds vs milliseconds
            if expires_at > 1e12:
                expired = now * 1000 > expires_at
            else:
                expired = now > expires_at
            if expired:
                return None

        return token
    except Exception:
        return None


def _get_base_url(provider: str, models_config: dict) -> str:
    """Get base URL for a provider, checking models.json first."""
    providers = models_config.get("providers", {})
    provider_conf = providers.get(provider, {})
    custom_url = provider_conf.get("baseUrl") or provider_conf.get("baseURL")
    if custom_url:
        return custom_url

    if provider not in PROVIDER_BASE_URLS:
        raise ValueError(
            f"Unknown provider '{provider}'. Configure a baseUrl in models.json "
            f"or use a known provider: {', '.join(sorted(PROVIDER_BASE_URLS))}."
        )

    return PROVIDER_BASE_URLS[provider]


# ---------------------------------------------------------------------------
# HTTP / LLM request functions
# ---------------------------------------------------------------------------

def make_request(url: str, headers: dict, body: dict,
                 timeout: int = 60) -> dict:
    """
    Send a JSON POST request and return the parsed response.

    Args:
        url: The endpoint URL.
        headers: HTTP headers dict.
        body: JSON-serializable request body.
        timeout: Request timeout in seconds.

    Returns:
        Parsed JSON response as a dict.

    Raises:
        RuntimeError: On HTTP errors or connection failures.
    """
    data = json.dumps(body).encode("utf-8")
    merged_headers = {**headers, "Content-Type": "application/json"}
    req = urllib.request.Request(url, data=data, headers=merged_headers,
                                method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"LLM request failed ({e.code}): {error_body}"
        ) from e
    except urllib.error.URLError as e:
        raise RuntimeError(
            f"LLM request connection error: {e.reason}"
        ) from e


def make_gemini_native_request(config: ProviderConfig, messages: list[dict],
                               temperature: float = 0.7,
                               max_tokens: int = 1024,
                               timeout: int = 60) -> dict:
    """
    Call Gemini using its native REST API (not OpenAI-compatible).

    Converts OpenAI-style messages to Gemini format and calls
    the ``generateContent`` endpoint directly.

    Args:
        config: A ProviderConfig for a Google/Gemini provider.
        messages: OpenAI-style messages (role/content dicts).
        temperature: Sampling temperature.
        max_tokens: Maximum output tokens.
        timeout: Request timeout in seconds.

    Returns:
        Raw Gemini API response dict.
    """
    model_name = config.primary_model
    if "/" in model_name:
        model_name = model_name.split("/", 1)[1]

    url = f"{GEMINI_NATIVE_URL}/models/{model_name}:generateContent"
    # Pass the key in a header rather than a URL query parameter so it is
    # never inadvertently recorded in access logs or tracebacks.
    headers = {"x-goog-api-key": config.api_key}

    contents: list[dict] = []
    system_instruction = None
    for msg in messages:
        role = msg.get("role", "user")
        text = msg.get("content", "")
        if role == "system":
            system_instruction = {"parts": [{"text": text}]}
        else:
            gemini_role = "model" if role == "assistant" else "user"
            contents.append({"role": gemini_role, "parts": [{"text": text}]})

    body: dict = {
        "contents": contents,
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens,
        },
    }
    if system_instruction:
        body["systemInstruction"] = system_instruction

    return make_request(url, headers, body, timeout=timeout)


def call_llm(messages: list[dict],
             config: Optional[ProviderConfig] = None,
             temperature: float = 0.7,
             max_tokens: int = 1024,
             native_gemini: bool = False,
             timeout: int = 60) -> str:
    """
    High-level function to call an LLM provider.

    Automatically resolves the provider if *config* is not supplied,
    and routes to the correct API format (OpenAI-compatible, Anthropic
    native, or Gemini native).

    Args:
        messages: List of message dicts with ``role`` and ``content`` keys.
        config: ProviderConfig (resolved automatically if *None*).
        temperature: Sampling temperature.
        max_tokens: Maximum tokens to generate.
        native_gemini: If *True* and provider is ``google``, use the Gemini
            native REST API instead of the OpenAI-compatible wrapper.
        timeout: HTTP request timeout in seconds (default 60).

    Returns:
        The assistant's response text.
    """
    if config is None:
        config = resolve_provider()

    # Gemini native path
    if config.provider == "google" and native_gemini:
        result = make_gemini_native_request(
            config, messages, temperature=temperature, max_tokens=max_tokens,
            timeout=timeout,
        )
        candidates = result.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                return parts[0].get("text", "")
        return ""

    # Anthropic native path
    if config.provider == "anthropic":
        return _call_anthropic(config, messages, temperature, max_tokens, timeout)

    # OpenAI-compatible path (default)
    return _call_openai_compatible(config, messages, temperature, max_tokens, timeout)


def _call_anthropic(config: ProviderConfig, messages: list[dict],
                    temperature: float, max_tokens: int,
                    timeout: int = 60) -> str:
    """Call Anthropic Messages API."""
    model_name = config.primary_model
    if "/" in model_name:
        model_name = model_name.split("/", 1)[1]

    url = f"{config.base_url}/messages"
    headers = {
        "x-api-key": config.api_key,
        "anthropic-version": "2023-06-01",
        **config.default_headers,
    }

    system_text = None
    filtered: list[dict] = []
    for msg in messages:
        if msg.get("role") == "system":
            system_text = msg.get("content", "")
        else:
            filtered.append(msg)

    body: dict = {
        "model": model_name,
        "messages": filtered,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if system_text:
        body["system"] = system_text

    result = make_request(url, headers, body, timeout=timeout)
    for block in result.get("content", []):
        if block.get("type") == "text":
            return block.get("text", "")
    return ""


def _call_openai_compatible(config: ProviderConfig, messages: list[dict],
                            temperature: float, max_tokens: int,
                            timeout: int = 60) -> str:
    """Call an OpenAI-compatible chat completions endpoint."""
    model_name = config.primary_model
    if "/" in model_name:
        model_name = model_name.split("/", 1)[1]

    url = f"{config.base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {config.api_key}",
        **config.default_headers,
    }

    body = {
        "model": model_name,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    result = make_request(url, headers, body, timeout=timeout)
    choices = result.get("choices", [])
    if choices:
        return choices[0].get("message", {}).get("content", "")
    return ""


# ---------------------------------------------------------------------------
# Main resolver
# ---------------------------------------------------------------------------

def resolve_provider() -> ProviderConfig:
    """
    Resolve the current OpenClaw provider configuration.

    Reads OpenClaw config files to determine:
    1. What provider/model the user has configured
    2. Where to find the API key
    3. What base URL to use

    Returns:
        ProviderConfig with all fields populated

    Raises:
        RuntimeError: If no valid provider configuration can be resolved
    """
    config = _load_json(CONFIG_FILE)
    models_config = _load_json(MODELS_FILE)

    # Step 1: Find primary model
    primary_model = _get_primary_model(config)
    if not primary_model:
        raise RuntimeError(
            "No primary model configured in OpenClaw. "
            "Run 'openclaw onboard' to set up a provider."
        )

    # Step 2: Determine provider
    provider = _get_provider_from_model(primary_model)
    if not provider:
        raise RuntimeError(
            f"Cannot determine provider from model '{primary_model}'. "
            "Expected format: 'provider/model-name'."
        )

    # Step 3: Get API key (try multiple sources)
    api_key = None
    default_headers = {}

    if provider == "github-copilot":
        api_key = _get_copilot_token(openclaw_config=config)
        if not api_key:
            raise RuntimeError(
                "GitHub Copilot token expired or not found. "
                "Run 'openclaw models auth login-github-copilot' to refresh."
            )
        default_headers = {
            "Editor-Version": "vscode/1.107.0",
            "Editor-Plugin-Version": "copilot-chat/0.35.0",
            "Copilot-Integration-Id": "vscode-chat",
            "User-Agent": "GitHubCopilotChat/0.35.0",
        }
    elif provider == "ollama":
        api_key = "ollama-local"  # Ollama doesn't need a real key
    else:
        api_key = (
            _get_api_key_from_env(provider) or
            _get_api_key_from_config(config, provider)
        )

    if not api_key:
        env_var = PROVIDER_ENV_KEYS.get(provider, f"{provider.upper()}_API_KEY")
        raise RuntimeError(
            f"No API key found for provider '{provider}'. "
            f"Set {env_var} environment variable or configure it in OpenClaw."
        )

    # Step 4: Get base URL
    base_url = _get_base_url(provider, models_config)

    return ProviderConfig(
        provider=provider,
        api_key=api_key,
        base_url=base_url,
        primary_model=primary_model,
        default_headers=default_headers,
    )


if __name__ == "__main__":
    try:
        cfg = resolve_provider()
        print(f"✅ Provider resolved: {cfg}")
        print(f"   Provider:  {cfg.provider}")
        print(f"   Base URL:  {cfg.base_url}")
        print(f"   Model:     {cfg.primary_model}")
        if cfg.api_key:
            masked = (cfg.api_key[:4] + "..." + cfg.api_key[-4:]
                      if len(cfg.api_key) > 8
                      else "***")
        else:
            masked = "[NOT SET]"
        print(f"   Key:       {masked}")
        print(f"   Headers:   {list(cfg.default_headers.keys()) if cfg.default_headers else 'none'}")
    except RuntimeError as e:
        print(f"❌ {e}")
