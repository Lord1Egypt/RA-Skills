---
name: agentscope-gemini-usage-fix
description: Work around a Gemini usage normalization bug in AgentScope where cached_content_token_count=None causes Usage validation to fail. Use this whenever the user uses GeminiChatModel and sees ValidationError on cache_input_tokens.
version: 0.1.0
metadata:
  openclaw:
    requires:
      env:
        - GOOGLE_API_KEY
      bins:
        - python3
    primaryEnv: GOOGLE_API_KEY
    envVars:
      - name: GOOGLE_API_KEY
        required: true
        description: Google Generative AI API key.
    emoji: "\U0001F41E"
    homepage: https://github.com/agentscope-ai/agentscope
---

# AgentScope Gemini Usage Fix

This skill documents a known bug and a runtime workaround for `GeminiChatModel` usage extraction.

## Bug

`GeminiChatModel._extract_usage` uses `getattr(..., "cached_content_token_count", 0)`, which returns `None` when the attribute exists but is `None`. `ChatUsage` validates `cache_input_tokens` as `int`, so `None` raises a pydantic `ValidationError`.

## Workaround

Apply this patch before using Gemini models:

```python
from agentscope.model._gemini._model import GeminiChatModel

_original = GeminiChatModel._extract_usage

def _patched_extract_usage(self, usage_metadata, start_datetime):
    if not usage_metadata:
        return None
    usage = _original(self, usage_metadata, start_datetime)
    if usage and getattr(usage, "cache_input_tokens", None) is None:
        usage.cache_input_tokens = 0
    return usage

GeminiChatModel._extract_usage = _patched_extract_usage
```

## Upstream Fix

The upstream fix is a one-line change:

```python
cache_input_tokens=getattr(
    usage_metadata,
    "cached_content_token_count",
    0,
) or 0,
```

Reference: https://github.com/agentscope-ai/agentscope/issues/3077
