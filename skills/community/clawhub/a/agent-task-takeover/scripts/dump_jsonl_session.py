#!/usr/bin/env python3
"""Dump user/assistant text from a JSONL agent transcript.

Handles the known rollout formats:
  - Codex CLI:  ~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl
    records {"type": "user_message"|"response_item"|...,"payload": {...}}
  - Claude Code: ~/.claude/projects/<dir>/<session>.jsonl
    records {"type": "user"|"assistant", "message": {"role":..., "content":[...]}}
  - ZCode rollout: ~/.zcode/cli/rollout/model-io-session_*.jsonl
    each line is one API request; the last VALID line whose request.messages
    is a list holds the whole conversation (auto-detected and exploded).

Stdlib only. Read-only. Secrets are redacted unless --show-sensitive is used.

Usage:
  python dump_jsonl_session.py <file.jsonl> [--role assistant --last 1 --chars 0]
  python dump_jsonl_session.py <file.jsonl> --user-only --chars 800
"""
import argparse
import datetime
import json
import sys
from collections import deque

from session_utils import blocks_text, ensure_utf8_stdout, redact_text, truncate_text

_STRUCTURAL_TYPES = {
    "session_meta",
    "user_message",
    "response_item",
    "event_msg",
    "turn_context",
    "summary",
    "user",
    "assistant",
    "system",
}


def fmt_ts(ts):
    if not ts:
        return "?"
    try:
        if isinstance(ts, (int, float)):
            divisor = 1000 if ts > 1e11 else 1
            return datetime.datetime.fromtimestamp(ts / divisor).strftime("%Y-%m-%d %H:%M")
        return str(ts)[:16].replace("T", " ")
    except Exception:
        return str(ts)


def rec_to_msg(rec):
    """Map one JSONL record to (role, text, ts) or None."""
    t = rec.get("type")
    ts = rec.get("timestamp") or rec.get("time")

    # Claude Code
    if t in ("user", "assistant") and isinstance(rec.get("message"), dict):
        message = rec["message"]
        txt = blocks_text(message.get("content"))
        if txt.strip():
            return (message.get("role") or t, txt, ts)
        return None
    if t == "summary" and rec.get("summary"):
        return ("summary", rec["summary"], ts)

    # Codex CLI
    payload = rec.get("payload") or {}
    if t == "user_message":
        txt = blocks_text(payload.get("content"))
        if txt.strip():
            return ("user", txt, ts)
        return None
    if t == "response_item" and payload.get("type") == "message":
        txt = blocks_text(payload.get("content"))
        if txt.strip():
            return (payload.get("role") or "assistant", txt, ts)
        return None
    return None


def iter_records(path, stats):
    """Yield valid JSON objects without retaining the whole rollout."""
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                stats["malformed"] += 1
                continue
            if not isinstance(rec, dict):
                stats["malformed"] += 1
                continue
            yield rec


def is_zcode_record(rec):
    request = rec.get("request")
    return isinstance(request, dict) and isinstance(request.get("messages"), list)


def collect(path, args):
    stats = {"malformed": 0, "api_requests": 0, "unknown": 0}
    is_zcode = None
    last_zcode = None
    meta = None
    kept = []
    bounded = deque(maxlen=args.last) if args.last else None
    role_filter = "user" if args.user_only else args.role

    def keep(role):
        return role_filter == "all" or role == role_filter

    def add(message):
        if bounded is not None:
            bounded.append(message)
        else:
            kept.append(message)

    for rec in iter_records(path, stats):
        if is_zcode is None:
            if is_zcode_record(rec):
                is_zcode = True
            elif rec.get("type") in _STRUCTURAL_TYPES:
                is_zcode = False
            else:
                stats["unknown"] += 1
                continue

        if is_zcode:
            if rec.get("request") is not None:
                stats["api_requests"] += 1
            if is_zcode_record(rec):
                last_zcode = rec
            continue

        if rec.get("type") == "session_meta" and meta is None:
            meta = rec.get("payload") or {}
        message = rec_to_msg(rec)
        if message and keep(message[0]):
            add(message)

    if is_zcode and last_zcode is not None:
        request = last_zcode["request"]
        for message in request["messages"]:
            if not isinstance(message, dict) or message.get("role") == "system":
                continue
            role = message.get("role") or "?"
            txt = blocks_text(message.get("content"))
            if txt.strip() and keep(role):
                add((role, txt, ""))

    messages = list(bounded) if bounded is not None else kept
    return messages, meta, stats, is_zcode, last_zcode


_GEMINI_ROLE_MAP = {"user": "user", "gemini": "assistant", "model": "assistant"}


def collect_gemini(path, args):
    """Gemini CLI sessions (~/.gemini/tmp/<hash>/chats/session-*.json) are one
    JSON document, not JSONL: {"sessionId":..., "messages":[{"type":"user"|
    "gemini", "content":...}]}. Returns (messages, meta) or None if the file
    does not look like that shape."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            doc = json.load(handle)
    except Exception:
        return None
    if not isinstance(doc, dict) or not isinstance(doc.get("messages"), list):
        return None
    role_filter = "user" if args.user_only else args.role
    messages = []
    for item in doc["messages"]:
        if not isinstance(item, dict):
            continue
        role = _GEMINI_ROLE_MAP.get(str(item.get("type", "")).lower())
        if role is None:
            continue
        txt = blocks_text(item.get("content"))
        if txt.strip() and (role_filter == "all" or role == role_filter):
            messages.append((role, txt, item.get("timestamp") or ""))
    if args.last:
        messages = messages[-args.last:]
    meta = {"id": doc.get("sessionId"), "cwd": doc.get("projectHash"), "originator": "gemini-cli"}
    return messages, meta


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("file")
    parser.add_argument("--last", type=int, default=0,
                        help="only the last N messages AFTER role filtering")
    parser.add_argument("--user-only", action="store_true",
                        help="legacy alias for --role user")
    parser.add_argument("--role", choices=("all", "user", "assistant", "summary"),
                        default="all", help="only print this role (default: all)")
    parser.add_argument(
        "--final-assistant",
        action="store_true",
        help="shorthand for --role assistant --last 1 --chars 0",
    )
    parser.add_argument("--chars", type=int, default=2000,
                        help="max chars per message; 0 means unlimited")
    parser.add_argument("--show-sensitive", action="store_true",
                        help="disable secret redaction (only for explicit local inspection)")
    args = parser.parse_args()
    if args.last < 0 or args.chars < 0:
        parser.error("--last and --chars must be >= 0")

    if args.final_assistant:
        args.role = "assistant"
        args.last = 1
        args.chars = 0
    if args.user_only:
        args.role = "user"

    ensure_utf8_stdout()

    if str(args.file).lower().endswith(".json"):
        gemini = collect_gemini(args.file, args)
        if gemini is not None:
            messages, meta = gemini
            print(f"# gemini-cli session: {meta.get('id')}")
            if args.show_sensitive:
                print("# WARNING: sensitive redaction disabled")
            print(f"# {len(messages)} messages\n")
            redactions = 0
            for role, txt, ts in messages:
                if not args.show_sensitive:
                    txt, n = redact_text(txt)
                    redactions += n
                print(f"\n=== {role.upper()} [{fmt_ts(ts)}] ===")
                print(truncate_text(txt, args.chars))
            if redactions:
                print(
                    f"\n# redacted {redactions} sensitive value(s); "
                    "use --show-sensitive only when explicitly required"
                )
            return

    try:
        messages, meta, stats, is_zcode, last_zcode = collect(args.file, args)
    except OSError as exc:
        sys.exit(f"cannot read {args.file}: {exc}")

    printed_roles = "user" if args.user_only else args.role
    print(f"# role filter: {printed_roles}; last: {args.last or 'all'}")
    if is_zcode:
        request = last_zcode["request"] if last_zcode else {}
        model = (request.get("body") or {}).get("model")
        session_id = last_zcode.get("sessionId") if last_zcode else None
        print(
            f"# zcode rollout: {stats['api_requests']} API requests; "
            "conversation from the last valid request"
        )
        print(f"# model: {model}  session: {session_id}")
    elif meta is not None:
        print(
            f"# session {meta.get('id')}  cwd: {meta.get('cwd')}  "
            f"originator: {meta.get('originator')}"
        )
    if stats["malformed"] or stats["unknown"]:
        print(
            f"# skipped {stats['malformed']} malformed line(s), "
            f"{stats['unknown']} unrecognized leading record(s)"
        )
    if args.show_sensitive:
        print("# WARNING: sensitive redaction disabled")

    print(f"# {len(messages)} messages\n")
    redactions = 0
    for role, txt, ts in messages:
        if not args.show_sensitive:
            txt, n = redact_text(txt)
            redactions += n
        txt = truncate_text(txt, args.chars)
        print(f"\n=== {role.upper()} [{fmt_ts(ts)}] ===")
        print(txt)

    if redactions:
        print(
            f"\n# redacted {redactions} sensitive value(s); "
            "use --show-sensitive only when explicitly required"
        )


if __name__ == "__main__":
    main()
