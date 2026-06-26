from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from uuid import uuid4

VALID_MODES = ("compact", "full", "rag", "replay", "jsonl")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--mode", choices=VALID_MODES, default="full")
    parser.add_argument("--output")
    return parser.parse_args()


def load_json(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def normalize_messages(messages):
    normalized = []

    for m in messages:
        normalized.append({
            "role": m.get("role", "unknown"),
            "content": str(m.get("content", "")).strip(),
            "tool": m.get("tool"),
            "tool_result": m.get("tool_result"),
            "timestamp": m.get("timestamp"),
        })

    return normalized


def render_markdown(payload, mode):
    messages = normalize_messages(payload.get("messages", []))

    session_id = str(uuid4())[:8]
    exported = datetime.utcnow().isoformat()

    lines = []

    title = payload.get("title", "Agent Conversation Export")

    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"> Exported: {exported}")
    lines.append(f"> Session: {session_id}")
    lines.append(f"> Mode: {mode}")
    lines.append("")

    if len(messages) > 20:
        lines.append("## Table of Contents")
        lines.append("")

        for idx, msg in enumerate(messages, 1):
            preview = msg["content"][:40].replace("\n", " ")
            lines.append(f"- [Turn {idx}](#turn-{idx}) - {preview}")

        lines.append("")

    tool_counter = Counter()

    for idx, msg in enumerate(messages, 1):
        role = msg["role"].title()

        lines.append(f'<a id="turn-{idx}"></a>')
        lines.append(f"## Turn {idx} — {role}")
        lines.append("")

        content = msg["content"] or "_No content_"

        if mode == "rag":
            lines.append(f"<!-- chunk:start id={idx} -->")

        lines.append(content)
        lines.append("")

        if msg["tool"]:
            tool_counter[msg["tool"]] += 1

            lines.append("<details>")
            lines.append(f"<summary>Tool: {msg['tool']}</summary>")
            lines.append("")

            if msg["tool_result"]:
                result = str(msg["tool_result"])

                if len(result) > 3000:
                    result = result[:3000] + "\\n...[truncated]..."

                lines.append("```")
                lines.append(result)
                lines.append("```")

            lines.append("</details>")
            lines.append("")

        if mode == "rag":
            lines.append("<!-- chunk:end -->")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Tool Statistics")
    lines.append("")

    if tool_counter:
        for tool, count in tool_counter.items():
            lines.append(f"- {tool}: {count}")
    else:
        lines.append("- No tools detected")

    return "\n".join(lines)


def render_jsonl(payload):
    messages = normalize_messages(payload.get("messages", []))

    output = []

    for msg in messages:
        output.append(json.dumps(msg, ensure_ascii=False))

    return "\n".join(output)


def main():
    args = parse_args()

    payload = load_json(args.input)

    output = args.output

    if not output:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        suffix = "jsonl" if args.mode == "jsonl" else "md"

        output = f"agent-archive-{args.mode}-{stamp}.{suffix}"

    output_path = Path(output)

    if args.mode == "jsonl":
        content = render_jsonl(payload)
    else:
        content = render_markdown(payload, args.mode)

    output_path.write_text(content, encoding="utf-8")

    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
