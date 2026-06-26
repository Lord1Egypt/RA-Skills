#!/usr/bin/env python3
"""
Parse Anthropic Claude export file (conversations.json) into normalized chat objects.

Anthropic export format:
- Top-level list of conversations
- Fields: uuid, name, summary, created_at, updated_at, account, chat_messages
- Messages: uuid, text, content (list of {type, text, citations...}), sender (human/assistant), created_at

Output format (one JSON object per chat, newline-delimited):
{
  "id": "chat_<uuid>",
  "title": "Chat title",
  "date": "YYYY-MM-DD",
  "messages": [
    { "role": "user" | "assistant", "content": "text...", "timestamp": "ISO" }
  ]
}
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def extract_message_text(msg: dict) -> str:
    """Extract text from an Anthropic message (handles content list or plain text field)."""
    # Try content list first (array of {type, text, ...} blocks)
    content = msg.get("content", [])
    if isinstance(content, list) and content:
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", "").strip())
        if parts:
            return "\n".join(parts)
    # Fall back to plain text field
    return msg.get("text", "").strip()


def normalize_role(sender: str) -> str:
    """Normalize Anthropic sender to standard role."""
    if sender == "human":
        return "user"
    elif sender == "assistant":
        return "assistant"
    return sender or "unknown"


def parse(file_path: str):
    """Parse Anthropic conversations.json and yield normalized chat dicts."""
    with open(file_path, "r") as f:
        data = json.load(f)

    if not isinstance(data, list):
        print(f"Error: expected a list at top level, got {type(data)}", file=sys.stderr)
        sys.exit(1)

    for conv in data:
        chat_id = f"anthropic_{conv.get('uuid', 'unknown')}"
        title = conv.get("name") or conv.get("summary") or "Untitled"

        # Parse ISO timestamp
        created_at = conv.get("created_at", "")
        try:
            dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        except Exception:
            dt = datetime.now(timezone.utc)
        date_str = dt.strftime("%Y-%m-%d")

        messages = []
        for msg in conv.get("chat_messages", []):
            role = normalize_role(msg.get("sender"))
            content = extract_message_text(msg)
            if not content:
                continue

            msg_ts = msg.get("created_at", created_at)
            try:
                msg_dt = datetime.fromisoformat(msg_ts.replace("Z", "+00:00"))
                msg_iso = msg_dt.isoformat()
            except Exception:
                msg_iso = dt.isoformat()

            messages.append({
                "role": role,
                "content": content,
                "timestamp": msg_iso
            })

        yield {
            "id": chat_id,
            "title": title,
            "date": date_str,
            "messages": messages,
            "source": "anthropic"
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: parse_anthropic.py <path/to/conversations.json>")
        sys.exit(1)

    for chat in parse(sys.argv[1]):
        print(json.dumps(chat))
