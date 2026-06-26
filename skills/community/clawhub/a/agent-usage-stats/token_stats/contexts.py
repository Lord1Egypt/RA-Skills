"""Model context-window lookup."""

from __future__ import annotations


MODEL_CONTEXT_MAP = {
    # ── Anthropic / Claude (all 200K) ──
    "claude-opus-4-7": 200_000,
    "claude-opus-4-5": 200_000,
    "claude-opus-4": 200_000,
    "claude-sonnet-4-6": 200_000,
    "claude-sonnet-4-5": 200_000,
    "claude-sonnet-4": 200_000,
    "claude-haiku-4-5": 200_000,
    "claude-haiku-4-5-20251001": 200_000,
    "claude-haiku-3.5": 200_000,
    "claude-3.5-sonnet": 200_000,
    "claude-3.5-haiku": 200_000,
    "claude-3-opus": 200_000,
    "claude-3-sonnet": 200_000,
    "claude-3-haiku": 200_000,

    # ── OpenAI / GPT ──
    "gpt-4.1": 1_048_576,
    "gpt-4.1-mini": 1_048_576,
    "gpt-4.1-nano": 1_048_576,
    "gpt-4o": 131_072,
    "gpt-4o-mini": 131_072,
    "gpt-4-turbo": 131_072,
    "gpt-4": 131_072,
    "o4-mini": 200_000,
    "o3": 200_000,
    "o3-mini": 200_000,
    "o1": 200_000,
    "o1-pro": 200_000,

    # ── Google / Gemini (all 1M) ──
    "gemini-2.5-pro": 1_048_576,
    "gemini-2.5-flash": 1_048_576,
    "gemini-2.5-flash-lite": 1_048_576,
    "gemini-2.0-flash": 1_048_576,

    # ── DeepSeek ──
    "deepseek-v4-flash": 1_048_576,
    "deepseek-v4-pro": 1_048_576,
    "deepseek-v4": 1_048_576,
    "deepseek-chat": 1_048_576,
    "deepseek-reasoner": 1_048_576,
    "deepseek-r1": 1_048_576,
    "deepseek-v3": 131_072,

    # ── Meta / Llama ──
    "llama-4": 131_072,
    "llama-3.1": 131_072,
    "llama-3": 131_072,

    # ── Mistral ──
    "mistral-large-2": 131_072,
    "mistral-large": 131_072,
    "mistral-small": 131_072,

    # ── 通义千问 / Qwen ──
    "qwen3.6-plus": 1_048_576,
    "qwen3": 131_072,
    "qwen3-coder": 131_072,
    "qwen2.5-coder": 131_072,
    "qwen-plus": 131_072,
    "qwen-max": 131_072,
    "qwen-turbo": 131_072,

    # ── Kimi / 月之暗面 (Moonshot) ──
    "moonshot-v1-128k": 131_072,
    "moonshot-v1-32k": 32_768,
    "moonshot-v1-8k": 8_192,
    "kimi-latest": 131_072,

    # ── GLM / 智谱 ──
    "glm-4-plus": 131_072,
    "glm-4-long": 1_048_576,
    "glm-4-air": 131_072,
    "glm-4-flash": 131_072,
    "glm-4": 131_072,
    "glm-3-turbo": 131_072,

    # ── Doubao / 字节豆包 ──
    "doubao-pro-128k": 131_072,
    "doubao-pro-32k": 32_768,
    "doubao-lite-32k": 32_768,

    # ── 文心 / 百度 (ERNIE) ──
    "ernie-4.0-turbo": 131_072,
    "ernie-4.0": 8_192,
    "ernie-3.5": 8_192,

    # ── 零一万物 / Yi ──
    "yi-large": 32_768,
    "yi-lightning": 16_384,

    # ── xAI / Grok ──
    "grok-3": 131_072,
    "grok-2": 131_072,
}

DEFAULT_CONTEXT = 131_072


def detect_context(model_name: str) -> int:
    if not model_name:
        return DEFAULT_CONTEXT
    m = model_name.lower().strip()
    if m in MODEL_CONTEXT_MAP:
        return MODEL_CONTEXT_MAP[m]
    for key, val in sorted(MODEL_CONTEXT_MAP.items(), key=lambda x: -len(x[0])):
        if m.startswith(key):
            return val
    return DEFAULT_CONTEXT
