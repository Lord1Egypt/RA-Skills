#!/usr/bin/env python3
"""
Parse chat export files into normalized JSON messages.

Usage:
    python3 extract_messages.py <file> [--speaker NAME] [--format auto|wechat|whatsapp|telegram|simple|json]

Output: JSON array of {speaker, text, time?} to stdout.
"""

import sys
import re
import json
import argparse
from pathlib import Path


def detect_format(lines: list[str]) -> str:
    """Auto-detect chat export format."""
    sample = "\n".join(lines[:50])

    # JSON array
    stripped = sample.strip()
    if stripped.startswith("[") or stripped.startswith("{"):
        return "json"

    # WeChat: timestamp + name (same line or next line)
    wechat_same = re.compile(r"^\d{4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}:\d{2}(:\d{2})?\s+\S+[:\s]")
    wechat_next = re.compile(r"^\d{4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}:\d{2}(:\d{2})?\s+\S+\s*$")
    for line in lines[:30]:
        if wechat_same.match(line):
            return "wechat"
        if wechat_next.match(line):
            return "wechat"

    # WhatsApp: "DD/MM/YYYY, HH:MM - Name: msg"
    wa = re.compile(r"^\d{1,2}/\d{1,2}/\d{2,4},\s+\d{1,2}:\d{2}\s*-\s*.+?:")
    if any(wa.match(l) for l in lines[:30]):
        return "whatsapp"

    # Telegram: "Name [Date Time]"
    tg = re.compile(r"^.+?\[\d{1,2}\s+\w+\s+\d{4}\s+\d{1,2}:\d{2}:\d{2}\]")
    if any(tg.match(l) for l in lines[:30]):
        return "telegram"

    # Simple: "Name: msg"
    simple = re.compile(r"^\S+:\s+.+")
    if sum(1 for l in lines[:30] if simple.match(l)) >= 3:
        return "simple"

    return "unknown"


def parse_wechat(lines: list[str]) -> list[dict]:
    """Parse WeChat export (both same-line and next-line variants)."""
    messages = []
    ts_name_re = re.compile(
        r"^(\d{4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}:\d{2}(?::\d{2})?)\s+(.+?)$"
    )
    same_line_re = re.compile(
        r"^(\d{4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}:\d{2}(?::\d{2})?)\s+(.+?):\s*(.*)$"
    )
    system_patterns = [
        "撤回了一条消息", "加入了群聊", "退出了群聊",
        "修改群名", "邀请", "你已添加了", "开启了朋友验证",
    ]

    current = None
    for line in lines:
        line = line.rstrip("\n")

        # Check for system messages
        if any(p in line for p in system_patterns):
            continue

        # Same-line format: "2024-01-15 10:30 张三: hello"
        m = same_line_re.match(line)
        if m:
            if current:
                messages.append(current)
            current = {"speaker": m.group(2).strip(), "text": m.group(3).strip(), "time": m.group(1)}
            continue

        # Two-line format: "2024-01-15 10:30 张三" on one line, message on next
        m = ts_name_re.match(line)
        if m:
            if current:
                messages.append(current)
            current = {"speaker": m.group(2).strip(), "text": "", "time": m.group(1)}
            continue

        # Continuation of current message
        if current:
            if current["text"]:
                current["text"] += "\n" + line.strip()
            else:
                current["text"] = line.strip()

    if current:
        messages.append(current)

    # Filter empty and media-only messages
    media_re = re.compile(r"^\[(图片|视频|语音|表情|文件|位置|名片|链接|合并转发|转账|红包)\]$")
    messages = [m for m in messages if m["text"] and not media_re.match(m["text"])]

    return messages


def parse_json(content: str) -> list[dict]:
    """Parse JSON chat log."""
    data = json.loads(content)
    if isinstance(data, dict):
        data = data.get("messages", data.get("data", [data]))

    messages = []
    key_map = {
        "speaker": ["speaker", "sender", "name", "from", "nickname", "user"],
        "text": ["text", "content", "message", "msg", "body"],
        "time": ["time", "timestamp", "date", "datetime", "created_at"],
    }

    for item in data:
        msg = {}
        for target, candidates in key_map.items():
            for c in candidates:
                if c in item:
                    msg[target] = str(item[c])
                    break
        if "speaker" in msg and "text" in msg:
            messages.append(msg)

    return messages


def parse_whatsapp(lines: list[str]) -> list[dict]:
    """Parse WhatsApp export."""
    pattern = re.compile(
        r"^(\d{1,2}/\d{1,2}/\d{2,4},\s+\d{1,2}:\d{2})\s*-\s*(.+?):\s*(.*)$"
    )
    messages = []
    current = None

    for line in lines:
        line = line.rstrip("\n")
        m = pattern.match(line)
        if m:
            if current:
                messages.append(current)
            current = {"speaker": m.group(2).strip(), "text": m.group(3).strip(), "time": m.group(1)}
        elif current:
            current["text"] += "\n" + line.strip()

    if current:
        messages.append(current)

    return messages


def parse_telegram(lines: list[str]) -> list[dict]:
    """Parse Telegram desktop export."""
    header_re = re.compile(r"^(.+?)\[(\d{1,2}\s+\w+\s+\d{4}\s+\d{1,2}:\d{2}:\d{2})\]\s*$")
    messages = []
    current = None

    for line in lines:
        line = line.rstrip("\n")
        m = header_re.match(line)
        if m:
            if current:
                messages.append(current)
            current = {"speaker": m.group(1).strip(), "text": "", "time": m.group(2)}
        elif current:
            if current["text"]:
                current["text"] += "\n" + line.strip()
            else:
                current["text"] = line.strip()

    if current:
        messages.append(current)

    return messages


def parse_simple(lines: list[str]) -> list[dict]:
    """Parse simple 'Name: msg' format."""
    pattern = re.compile(r"^(\S+?):\s+(.*)$")
    messages = []
    current = None

    for line in lines:
        line = line.rstrip("\n")
        m = pattern.match(line)
        if m:
            if current:
                messages.append(current)
            current = {"speaker": m.group(1), "text": m.group(2).strip()}
        elif current:
            current["text"] += "\n" + line.strip()

    if current:
        messages.append(current)

    return messages


PARSERS = {
    "wechat": parse_wechat,
    "json": lambda lines: parse_json("\n".join(lines)),
    "whatsapp": parse_whatsapp,
    "telegram": parse_telegram,
    "simple": parse_simple,
}


def main():
    parser = argparse.ArgumentParser(description="Extract messages from chat exports")
    parser.add_argument("file", help="Path to chat export file")
    parser.add_argument("--speaker", help="Filter to specific speaker only")
    parser.add_argument("--format", default="auto", choices=list(PARSERS.keys()) + ["auto"],
                        help="Chat format (default: auto-detect)")
    args = parser.parse_args()

    filepath = Path(args.file)
    if not filepath.exists():
        print(f"Error: {filepath} not found", file=sys.stderr)
        sys.exit(1)

    # Read with encoding fallback
    for enc in ("utf-8", "gbk", "gb2312", "latin-1"):
        try:
            lines = filepath.read_text(encoding=enc).splitlines()
            break
        except UnicodeDecodeError:
            continue
    else:
        print("Error: Could not decode file", file=sys.stderr)
        sys.exit(1)

    # Detect or use specified format
    fmt = args.format
    if fmt == "auto":
        fmt = detect_format(lines)
        if fmt == "unknown":
            print("Error: Could not detect chat format. Use --format to specify.", file=sys.stderr)
            sys.exit(1)
        print(f"# Detected format: {fmt}", file=sys.stderr)

    # Parse
    messages = PARSERS[fmt](lines)

    # Filter by speaker
    if args.speaker:
        messages = [m for m in messages if m["speaker"] == args.speaker]

    # Output
    json.dump(messages, sys.stdout, ensure_ascii=False, indent=2)
    print(f"\n# Extracted {len(messages)} messages", file=sys.stderr)


if __name__ == "__main__":
    main()
