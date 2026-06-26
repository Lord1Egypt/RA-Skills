#!/usr/bin/env python3
"""Parse Claude's stream-json output, extract text and session ID.

Stdout returns only the ---CHAT_SUMMARY--- section Claude wrote (plus tool
progress and completion footer) — kept small enough for chat channels.
The full output is mirrored to --log-out for reference.

Note: --mode receives EFFECTIVE_MODE from launch.sh, always "discuss" or "execute".
"""
import os
import sys
import json
import argparse

SUMMARY_START = "---CHAT_SUMMARY_START---"
SUMMARY_END   = "---CHAT_SUMMARY_END---"

parser = argparse.ArgumentParser()
parser.add_argument("--mode",        default="execute")
parser.add_argument("--session-out", required=True)
parser.add_argument("--project",     default="")
parser.add_argument("--log-out",     default="")
parser.add_argument("--notify-out",  default="",
                    help="Path to write completion JSON for notifier.py")
args = parser.parse_args()

PROJECT_PART = f" · {args.project}" if args.project else ""
HEADER = f"\n─── 🤖 Claude Code{PROJECT_PART} [{args.mode}] ───\n"

# ── Open log file ──────────────────────────────────────────────────
log_file = None
if args.log_out:
    try:
        log_file = open(args.log_out, "w", encoding="utf-8")
        log_file.write(HEADER + "\n")
    except OSError as e:
        print(f"⚠️  Could not open log file: {e}", file=sys.stderr)

def to_log(text: str):
    if log_file:
        log_file.write(text)
        log_file.flush()

# ── Collect full text and tool lines ──────────────────────────────
has_error  = False
session_id = ""
full_text  = []   # all assistant text, written to log
tool_lines = []   # tool progress lines, always shown in stdout
footer     = ""

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    try:
        event = json.loads(line)
    except json.JSONDecodeError:
        to_log(line + "\n")
        continue

    etype = event.get("type", "")

    if etype == "system":
        sid = event.get("session_id", "")
        if sid:
            session_id = sid

    elif etype == "assistant":
        for block in event.get("message", {}).get("content", []):
            if block.get("type") == "text":
                full_text.append(block["text"])
                to_log(block["text"])
            elif block.get("type") == "tool_use":
                tool_name  = block.get("name", "unknown")
                tool_input = block.get("input", {})
                hint = ""
                for key in ("path", "file_path", "command", "pattern", "url"):
                    if key in tool_input:
                        hint = f": {tool_input[key]}"
                        break
                line_str = f"\n🔧 [{tool_name}{hint}]"
                tool_lines.append(line_str)
                to_log(line_str)

    elif etype == "result":
        if event.get("is_error"):
            has_error = True
            err = event.get("error", "unknown error")
            if isinstance(err, dict):
                err = err.get("message", str(err))
            elif not isinstance(err, str):
                err = str(err)
            footer = f"\n\n❌ Error: {err}"
        else:
            turns  = event.get("num_turns", 0)
            label  = "Discussion complete" if args.mode == "discuss" else "Execution complete"
            footer = f"\n\n✅ {label} ({turns} turns) · by Claude Code"
        to_log(footer + "\n")

if log_file:
    log_file.close()

# ── Extract the chat summary Claude wrote ─────────────────────────
combined = "".join(full_text)
summary  = ""

start_idx = combined.find(SUMMARY_START)
end_idx   = combined.find(SUMMARY_END)
if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
    summary = combined[start_idx + len(SUMMARY_START):end_idx].strip()

# ── Build stdout (what OpenClaw AI receives as the exec result) ───
print(HEADER, flush=True)

for tl in tool_lines:
    print(tl, end="", flush=True)

if summary:
    print(f"\n\n{summary}", flush=True)
else:
    # No summary marker found — fall back to last 2000 chars of text
    fallback = combined.strip()[-2000:]
    if fallback:
        print(f"\n\n{fallback}", flush=True)
    print("\n⚠️  (No structured summary found — showing tail of output)", flush=True)

print(footer, flush=True)

if args.log_out:
    print(f"\n📄 Full log: {args.log_out}", flush=True)

# ── Write notify JSON for notifier.py ────────────────────────────
if args.notify_out:
    notify_data = {
        "status":   "error" if has_error else "done",
        "mode":     args.mode,
        "project":  args.project,
        "summary":  summary if summary else combined.strip()[-2000:],
        "log_path": args.log_out,
    }
    tmp = args.notify_out + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(notify_data, f, ensure_ascii=False)
        os.replace(tmp, args.notify_out)
    except OSError as e:
        print(f"⚠️  Could not write notify file: {e}", file=sys.stderr)

# ── Write session ID atomically ────────────────────────────────────
if session_id:
    tmp = args.session_out + ".tmp"
    try:
        with open(tmp, "w") as f:
            f.write(session_id)
        os.replace(tmp, args.session_out)
    except OSError as e:
        print(f"⚠️  Could not write session ID: {e}", file=sys.stderr)
else:
    print("⚠️  No session ID received — session will not be saved", file=sys.stderr)

sys.exit(1 if has_error else 0)
