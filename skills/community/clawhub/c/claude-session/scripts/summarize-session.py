#!/usr/bin/env python3
"""
Session summarizer - extracts user/assistant messages with timestamps for user messages only
Usage: summarize-session.py <project_name> <session_id> [limit]

Output format:
  user [14:30]: request content...
  assistant: response content...
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path


def summarize_session(project_name: str, session_id: str, limit: int = 50):
    session_file = Path.home() / ".claude" / "projects" / project_name / f"{session_id}.jsonl"

    if not session_file.exists():
        print(f"Error: Session file not found: {session_file}", file=sys.stderr)
        sys.exit(1)

    count = 0
    with open(session_file, "r") as f:
        for line in f:
            if count >= limit:
                break
            try:
                obj = json.loads(line)
                msg_type = obj.get("type")

                if msg_type in ("user", "human"):
                    # Get timestamp
                    timestamp = obj.get("timestamp", "")
                    time_str = ""
                    if timestamp:
                        try:
                            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                            time_str = dt.strftime("%m-%d %H:%M")
                        except (ValueError, TypeError):
                            pass

                    # Get message content
                    content = obj.get("message", {}).get("content", "")
                    text = extract_text(content)

                    if text:
                        text = truncate(text, 100)
                        if time_str:
                            print(f"user [{time_str}]: {text}")
                        else:
                            print(f"user: {text}")
                        count += 1

                elif msg_type == "assistant":
                    content = obj.get("message", {}).get("content", "")
                    text = extract_text(content)

                    if text:
                        text = truncate(text, 100)
                        print(f"assistant: {text}")
                        count += 1

            except json.JSONDecodeError:
                continue
            except Exception:
                continue


def extract_text(content) -> str:
    """Extract text from message content (handles list or string)."""
    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                return item.get("text", "")
    elif isinstance(content, str):
        return content
    return ""


def truncate(text: str, max_len: int) -> str:
    """Truncate text and replace newlines with spaces."""
    text = text.replace("\n", " ")
    if len(text) > max_len:
        return text[:max_len] + "..."
    return text


def main():
    if len(sys.argv) < 3:
        print("Usage: summarize-session.py <project_name> <session_id> [limit]")
        sys.exit(1)

    project_name = sys.argv[1]
    session_id = sys.argv[2]
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 50

    summarize_session(project_name, session_id, limit)


if __name__ == "__main__":
    main()
