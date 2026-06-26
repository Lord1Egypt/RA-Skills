"""
Model Pairs — Maps primary models to cheaper sub-agent models.

When running the manager→workers→synthesis RLM loop, workers use a cheaper
model to keep costs low while the manager and synthesis steps use the
primary (smarter) model.
"""

from __future__ import annotations

# Primary model → cheap sub-agent model
MODEL_PAIRS: dict[str, str] = {
    # Anthropic
    "claude-opus-4": "claude-sonnet-4",
    "claude-opus-4.6": "claude-sonnet-4",
    "claude-sonnet-4": "claude-haiku-3.5",
    "claude-sonnet-4.5": "claude-haiku-3.5",
    "claude-sonnet-3.5": "claude-haiku-3.5",
    "claude-haiku-3.5": "claude-haiku-3.5",
    # OpenAI
    "gpt-4o": "gpt-4o-mini",
    "gpt-4": "gpt-4o-mini",
    "gpt-4-turbo": "gpt-4o-mini",
    "gpt-4o-mini": "gpt-4o-mini",
    "gpt-5": "gpt-5-mini",
    "o3": "gpt-4o-mini",
    "o3-mini": "gpt-4o-mini",
    # Google
    "gemini-2.5-pro": "gemini-2.0-flash",
    "gemini-2.0-pro": "gemini-2.0-flash",
    "gemini-2.0-flash": "gemini-2.0-flash-lite",
    "gemini-1.5-pro": "gemini-1.5-flash",
    # DeepSeek
    "deepseek-chat": "deepseek-chat",
    "deepseek-reasoner": "deepseek-chat",
    # Mistral
    "mistral-large": "mistral-small",
    "mistral-medium": "mistral-small",
    # Open-source / local
    "llama-3.1-70b": "llama-3.1-8b",
    "llama-3.1-405b": "llama-3.1-70b",
    "qwen-2.5-72b": "qwen-2.5-7b",
}


def get_sub_agent_model(primary: str) -> str:
    """Return the cheaper sub-agent model for *primary*.

    Matching strategy:

    1. Strip provider prefix (e.g. ``anthropic/claude-opus-4`` → ``claude-opus-4``)
    2. Exact match (case-insensitive) against MODEL_PAIRS
    3. Longest-prefix match (handles version suffixes like ``-20250514``)
    4. Fallback: return the bare model name unchanged
    """
    if not primary:
        return primary

    bare = primary.split("/")[-1]
    lower = bare.lower()

    # Exact match (case-insensitive)
    for key, value in MODEL_PAIRS.items():
        if key.lower() == lower:
            return value

    # Longest-prefix match (case-insensitive)
    best_key = ""
    best_value = bare
    for key, value in MODEL_PAIRS.items():
        if lower.startswith(key.lower()) and len(key) > len(best_key):
            best_key = key
            best_value = value

    return best_value


def get_model_pair(primary: str) -> dict[str, str]:
    """Return ``{"primary": ..., "sub_agent": ...}`` for a model.

    The provider prefix (e.g. ``anthropic/``) is stripped from the primary
    name in the returned dict.
    """
    bare = primary.split("/")[-1]
    return {
        "primary": bare,
        "sub_agent": get_sub_agent_model(primary),
    }
