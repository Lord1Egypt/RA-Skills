#!/usr/bin/env python3
"""
Parser for Feishu chat history JSON exports.
Reads feishu_chat_YYYYMMDD.json, normalizes messages, emits JSON lines.
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def extract_text_content(body_content: str) -> str:
    """Extract readable text from Feishu message body.content (JSON string)."""
    try:
        obj = json.loads(body_content)
    except (json.JSONDecodeError, TypeError):
        return body_content.strip()

    # text type: {"text": "..."}
    if isinstance(obj, dict):
        if "text" in obj:
            return obj["text"].strip()
        # post type: {"title": "", "content": [[{"tag": "text", "text": "..."}]]}
        content = obj.get("content", [])
        if isinstance(content, list):
            texts = []
            for section in content:
                if isinstance(section, list):
                    for item in section:
                        if isinstance(item, dict) and item.get("tag") == "text":
                            texts.append(item.get("text", ""))
            return "".join(texts).strip()
    return ""


def parse_feishu_messages(json_path: Path) -> list[dict]:
    """
    Parse a feishu_chat_YYYYMMDD.json file and return a list of normalized messages.
    Each message: {role, content, timestamp, message_id, chat_id}
    """
    with open(json_path, encoding="utf-8") as f:
        messages = json.load(f)

    parsed = []
    for msg in messages:
        if msg.get("deleted") or msg.get("updated"):
            continue

        sender_type = msg.get("sender", {}).get("sender_type", "user")
        role = "assistant" if sender_type == "app" else "user"

        # Extract content
        body = msg.get("body", {})
        raw_content = body.get("content", "")
        content = extract_text_content(raw_content)

        if not content:
            continue

        # Parse timestamp (milliseconds)
        ts_ms = msg.get("create_time", "")
        try:
            ts_sec = int(ts_ms) / 1000
            dt = datetime.fromtimestamp(ts_sec)
            ts_str = dt.strftime("%Y-%m-%dT%H:%M:%S")
        except (ValueError, TypeError):
            ts_str = ts_ms

        parsed.append({
            "role": role,
            "content": content,
            "timestamp": ts_str,
            "message_id": msg.get("message_id", ""),
            "chat_id": msg.get("chat_id", ""),
            "sender_id": msg.get("sender", {}).get("id", ""),
        })

    # Sort by timestamp
    parsed.sort(key=lambda m: m["timestamp"])
    return parsed


def group_by_date(messages: list[dict]) -> dict[str, list[dict]]:
    """Group messages by YYYY-MM-DD date."""
    by_date = {}
    for msg in messages:
        date = msg["timestamp"][:10]  # "2026-03-19"
        if date not in by_date:
            by_date[date] = []
        by_date[date].append(msg)
    return by_date


def build_episodic_entry(date: str, messages: list[dict], source_file: str) -> str:
    """Build a markdown episodic entry for a single day."""
    lines = [
        f"## Feishu Chat Export ({date})",
        f"- Source: `{source_file}`",
        f"- Total messages: {len(messages)}",
    ]

    # Group by chat_id
    by_chat = {}
    for msg in messages:
        cid = msg["chat_id"]
        if cid not in by_chat:
            by_chat[cid] = []
        by_chat[cid].append(msg)

    for chat_id, chat_msgs in by_chat.items():
        lines.append(f"\n### Chat: {chat_id}")
        for msg in chat_msgs:
            role_label = "user" if msg["role"] == "user" else "assistant"
            ts = msg["timestamp"][11:]  # just HH:MM:SS
            content = msg["content"]
            # Truncate very long messages
            if len(content) > 500:
                content = content[:500] + "..."
            lines.append(f"- **{role_label}** [{ts}]: {content}")

    return "\n".join(lines) + "\n"


def main():
    if len(sys.argv) < 2:
        print("Usage: parse_feishu.py <feishu_chat_file.json>", file=sys.stderr)
        sys.exit(1)

    json_path = Path(sys.argv[1])
    if not json_path.exists():
        print(f"File not found: {json_path}", file=sys.stderr)
        sys.exit(1)

    messages = parse_feishu_messages(json_path)
    by_date = group_by_date(messages)

    for date, msgs in by_date.items():
        entry = build_episodic_entry(date, msgs, json_path.name)
        # Output as JSON line: {date, content}
        output = {
            "date": date,
            "source": json_path.name,
            "message_count": len(msgs),
            "content": entry
        }
        print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
