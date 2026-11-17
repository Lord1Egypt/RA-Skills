#!/usr/bin/env python3
"""Reproduce Gemini cached_content_token_count=None bug."""

from datetime import datetime
from types import SimpleNamespace

from agentscope.model._gemini._model import GeminiChatModel
from agentscope.message._base import Usage


def main() -> int:
    model = object.__new__(GeminiChatModel)
    metadata = SimpleNamespace(
        prompt_token_count=10,
        total_token_count=15,
        candidates_token_count=5,
        cached_content_token_count=None,
    )
    usage = model._extract_usage(metadata, datetime.now())
    assert usage is not None
    print(f"cache_input_tokens={usage.cache_input_tokens!r}")
    try:
        Usage(**dict(usage))
    except Exception as exc:
        print(f"FAIL: {type(exc).__name__}: {exc}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
