"""Rewind retriever: generates tool definitions and handles retrieval calls.

Part of claw-compactor. License: MIT.
"""
from __future__ import annotations
from typing import Any
from .store import RewindStore


TOOL_NAME = "rewind_retrieve"
TOOL_DESCRIPTION = (
    "Retrieve the original uncompressed content for a compressed section. "
    "Use this when you need more detail from a section marked with a retrieval hash."
)


def rewind_tool_def(provider: str = "openai") -> dict[str, Any]:
    """Generate a tool/function definition for the given provider format."""
    params = {
        "type": "object",
        "properties": {
            "hash_id": {
                "type": "string",
                "description": "The 24-character hash ID from the compression marker.",
            },
            "keywords": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Optional keywords to filter the retrieved content.",
            },
        },
        "required": ["hash_id"],
    }

    if provider == "anthropic":
        return {
            "name": TOOL_NAME,
            "description": TOOL_DESCRIPTION,
            "input_schema": params,
        }
    # OpenAI / default
    return {
        "type": "function",
        "function": {
            "name": TOOL_NAME,
            "description": TOOL_DESCRIPTION,
            "parameters": params,
        },
    }


def handle_rewind(store: RewindStore, tool_call: dict[str, Any]) -> dict[str, Any]:
    """Process a rewind_retrieve tool call and return the result."""
    args = tool_call.get("arguments", tool_call.get("input", {}))
    if isinstance(args, str):
        import json
        args = json.loads(args)

    hash_id = args.get("hash_id", "")
    keywords = args.get("keywords", [])

    if keywords:
        content = store.search(hash_id, keywords)
    else:
        content = store.retrieve(hash_id)

    if content is None:
        return {
            "status": "not_found",
            "message": f"No content found for hash={hash_id}. It may have expired.",
        }
    return {
        "status": "ok",
        "content": content,
    }
