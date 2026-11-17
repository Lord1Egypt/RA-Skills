#!/usr/bin/env python3
"""
Export a Codex app/CLI session to Markdown.

Usage: python3 scripts/export.py --list
       python3 scripts/export.py <session-id> [output.md] [--brief]
       python3 scripts/export.py <session-id> [output.md] [options]

Options:
  -b, --brief           Only user + assistant messages (no tool calls/outputs).
  -r, --redact          Mask emails, tokens, and absolute paths for safe sharing.
  --since <datetime>    Only include entries at/after this time (ISO 8601 or YYYY-MM-DD).
  --until <datetime>    Only include entries at/before this time.
  --grep <text>         Only include messages whose text contains <text> (case-insensitive);
                        a matched user message pulls in its full turn (reply + tool calls).
  -a, --append          Incremental export: append only messages newer than the last
                        export. Progress is tracked in "<output>.state.json", so manual
                        edits to the Markdown file are preserved.
  --format <fmt>        Output format: md (default), html, or obsidian.
  --sessions <ids>      Merge several sessions into one document (comma-separated ids).
  -i, --interactive     Interactive picker: choose exact messages to export.
  --watch [seconds]     Auto-incremental: poll the session and append new messages.
  -l, --list            List recent sessions.

Environment:
  CODEX_HOME            Codex data root (sessions, archived_sessions, state_5.sqlite).
                        Defaults to ~/.codex.
"""

import hashlib
import html
import json
import os
import re
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def get_codex_home():
    """Return the Codex data root, honoring the $CODEX_HOME environment variable."""
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")

def find_rollouts(session_id):
    """Find every rollout file belonging to a session (sessions + archived)."""
    codex_home = get_codex_home()
    roots = [codex_home / "sessions", codex_home / "archived_sessions"]
    matches = []
    for root in roots:
        if root.is_dir():
            matches.extend(root.glob(f"**/*{session_id}*.jsonl"))
    # Newest file last: continuations usually live in newer rollout files.
    return sorted(set(matches), key=lambda p: p.stat().st_mtime)


def entry_key(entry):
    """Stable identity for a rollout entry, used for cross-file dedup."""
    etype = entry.get("type")
    payload = entry.get("payload") or {}
    if etype == "response_item" and payload.get("id"):
        return ("response_item", payload["id"])
    if etype == "session_meta":
        return ("session_meta", payload.get("session_id") or payload.get("id") or "")
    digest = hashlib.sha256(
        json.dumps(entry, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    return (etype or "", digest)


def load_entries(paths):
    """Read and merge rollout files: dedup by identity, sort by timestamp."""
    entries = []
    seen = set()
    for path in paths:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue  # tolerate a truncated tail line
                key = entry_key(obj)
                if key in seen:
                    continue
                seen.add(key)
                entries.append(obj)
    entries.sort(key=lambda e: str(e.get("timestamp") or ""))
    return entries

def load_entries_tail(paths, offsets=None):
    """Read only the new parts of rollout files based on recorded byte offsets.

    Returns (entries, new_offsets). Files smaller than their recorded offset
    (replaced or truncated) are read in full and re-indexed.
    """
    offsets = offsets or {}
    entries = []
    seen = set()
    new_offsets = {}
    for path in paths:
        size = path.stat().st_size
        offset = offsets.get(str(path))
        if offset is None or offset < 0 or offset > size:
            offset = 0  # unknown or stale offset -> full read
        with open(path, encoding="utf-8") as f:
            if offset > 0:
                f.seek(offset)
                first = f.readline()
                if first and not first.endswith("\n"):
                    first = ""  # partial line at the boundary: discard
            else:
                first = ""
            lines = [first] if first else []
            lines.extend(f)
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            key = entry_key(obj)
            if key in seen:
                continue
            seen.add(key)
            entries.append(obj)
        new_offsets[str(path)] = size
    entries.sort(key=lambda e: str(e.get("timestamp") or ""))
    return entries, new_offsets

def parse_dt(value):
    """Parse a --since/--until value; naive values are treated as local time."""
    v = str(value).strip()
    try:
        dt = datetime.fromisoformat(v.replace("Z", "+00:00"))
    except ValueError:
        dt = datetime.strptime(v, "%Y-%m-%d").astimezone()
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.now().astimezone().tzinfo)
    return dt

def parse_entry_ts(value):
    """Parse a rollout entry timestamp; returns None if unparseable."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (ValueError, TypeError, OverflowError):
        return None


_INJECTED_TAGS = (
    "app-context",
    "in-app-browser-context",
    "environment_context",
    "permissions instructions",
    "user_instructions",
    "system-reminder",
)

_INJECTED_BLOCK_RE = re.compile(
    r"<(?P<tag>" + "|".join(map(re.escape, _INJECTED_TAGS)) + r")[^>]*>.*?</(?P=tag)>",
    re.DOTALL | re.IGNORECASE,
)

_UNCLOSED_PREFIXES = (
    "<permissions instructions>",
    "<environment_context>",
    "<app-context>",
    "<in-app-browser-context",
    "# AGENTS.md instructions",
)


def strip_injected_blocks(text):
    """Remove injected system blocks (e.g. <app-context>...</app-context>)."""
    return _INJECTED_BLOCK_RE.sub("", text)


_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_TOKEN_ASSIGN_RE = re.compile(
    r"(?i)\b(access_token|api[_-]?key|token|secret|password|authorization)\b"
    r"[=:]\s*[A-Za-z0-9._\-]{6,}"
)
_SK_TOKEN_RE = re.compile(r"(?i)\bsk-[A-Za-z0-9_-]{8,}\b")
_BEARER_RE = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._\-]{8,}")
_HEX_RUN_RE = re.compile(r"\b[0-9a-f]{32,}\b")
_BASE64_RUN_RE = re.compile(r"\b[A-Za-z0-9+/]{40,}={0,2}\b")
_WINDOWS_PATH_RE = re.compile(r"(?i)([A-Za-z]:\\)([^\s<>\"']+)")
_UNIX_PATH_RE = re.compile(r"(?<![A-Za-z0-9])((?:/|~/)(?:[^\s<>\"']+/)+[^\s<>\"']+)")


def _mask_windows_path(m):
    drive, rest = m.group(1), m.group(2)
    parts = [p for p in rest.split("\\") if p]
    tail = parts[-1] if len(parts) > 1 else "***"
    return f"{drive}***\\{tail}"


def _mask_unix_path(m):
    path = m.group(1)
    prefix = "~/" if path.startswith("~/") else "/"
    parts = [p for p in path[len(prefix):].split("/") if p]
    tail = parts[-1] if len(parts) > 1 else "***"
    return f"{prefix}***/{tail}"


def redact_text(text):
    """Mask emails, tokens, and absolute paths for safe sharing."""
    text = _TOKEN_ASSIGN_RE.sub(lambda m: m.group(1) + "=***", text)
    text = _SK_TOKEN_RE.sub("sk-***", text)
    text = _BEARER_RE.sub("Bearer ***", text)
    text = _HEX_RUN_RE.sub("***", text)
    text = _BASE64_RUN_RE.sub("***", text)
    text = _EMAIL_RE.sub("***@***", text)
    text = _WINDOWS_PATH_RE.sub(_mask_windows_path, text)
    text = _UNIX_PATH_RE.sub(_mask_unix_path, text)
    return text


def md_fragment_to_html(fragment):
    """Convert the small Markdown subset we emit into HTML."""
    parts = re.split(r"(```[^\n]*\n.*?```)", fragment, flags=re.DOTALL)
    out = []
    for part in parts:
        if part.startswith("```"):
            lines = part.strip().splitlines()
            lang = lines[0][3:].strip() if lines else ""
            code = "\n".join(lines[1:-1])
            cls = f' class="language-{html.escape(lang)}"' if lang else ""
            out.append(f"<pre><code{cls}>{html.escape(code)}</code></pre>")
        else:
            for para in part.split("\n\n"):
                para = para.strip()
                if not para:
                    continue
                escaped = html.escape(para).replace("\n", "<br>")
                escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
                out.append(f"<p>{escaped}</p>")
    return "\n".join(out)


def render_html(header_lines, sections, title="Codex Session Export"):
    """Render header + sections into a standalone HTML document."""
    body = []
    for line in header_lines:
        line = line.rstrip()
        if not line or line == "---":
            continue
        if line.startswith("# "):
            body.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("- **"):
            m = re.match(r"- \*\*(.+?)\*\*: (.*)", line)
            if m:
                body.append(f"<li><b>{html.escape(m.group(1))}:</b> {md_fragment_to_html(m.group(2))}</li>")
            else:
                body.append(f"<li>{md_fragment_to_html(line[2:])}</li>")
        else:
            body.append(md_fragment_to_html(line))
    if body:
        body.insert(0, '<ul class="meta">')
        body.insert(0, "<h2>会话信息</h2>")
        body.append("</ul>")
    for section in sections:
        section = section.rstrip("\n")
        lines = section.split("\n", 1)
        heading = lines[0]
        rest = lines[1] if len(lines) > 1 else ""
        level = heading.count("#")
        tag = "h3" if level >= 3 else "h2"
        if "👤 User" in heading:
            body.append(f'<{tag} class="role user">👤 用户</{tag}>')
        elif "🤖 Codex" in heading:
            body.append(f'<{tag} class="role assistant">🤖 Codex</{tag}>')
        elif "Tool Call" in heading:
            body.append("<h3>🔧 工具调用</h3>")
        elif "Tool Output" in heading:
            body.append("<h3>📤 工具输出</h3>")
        elif "📁 Session" in heading:
            body.append(f'<{tag} class="session">📁 {html.escape(heading.split("📁", 1)[1].strip())}</{tag}>')
        else:
            body.append(f"<{tag}>{html.escape(heading.lstrip('#').strip())}</{tag}>")
        body.append(md_fragment_to_html(rest))

    return (
        "<!doctype html>\n<html lang=\"zh-CN\">\n<head>\n"
        "<meta charset=\"utf-8\">\n"
        f"<title>{html.escape(title)}</title>\n"
        "<style>\n"
        "body{font-family:system-ui,'Microsoft YaHei',sans-serif;max-width:860px;"
        "margin:0 auto;padding:24px;line-height:1.7;color:#1f2937;background:#fff;}\n"
        "h1{font-size:24px;border-bottom:2px solid #e2e8f0;padding-bottom:8px;}\n"
        "h2.role{font-size:15px;padding:6px 10px;border-radius:6px;margin-top:24px;}\n"
        "h2.user{background:#eff6ff;color:#1d4ed8;}\n"
        "h2.assistant{background:#f0fdf4;color:#15803d;}\n"
        "h3{font-size:14px;color:#64748b;margin-top:16px;}\n"
        "pre{background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;"
        "padding:12px;overflow-x:auto;}\n"
        "code{font-family:ui-monospace,Consolas,monospace;font-size:13px;}\n"
        "p{white-space:pre-wrap;margin:8px 0;}\n"
        ".meta{list-style:none;padding:0;color:#475569;font-size:14px;}\n"
        "</style>\n</head>\n<body>\n"
        + "\n".join(body)
        + "\n</body>\n</html>\n"
    )


def render_obsidian(header_lines, sections, session_id):
    """Render header + sections with Obsidian YAML frontmatter."""
    frontmatter = (
        "---\n"
        f'title: "Codex Session {session_id}"\n'
        f'session_id: "{session_id}"\n'
        "tags:\n  - codex\n  - session\n"
        "---\n\n"
    )
    return frontmatter + "\n".join(header_lines + sections)


def entry_preview(entry, index):
    """Human-readable one-line preview for the interactive picker."""
    p = entry.get("payload") or {}
    ptype = p.get("type")
    role = p.get("role")
    ts = str(entry.get("timestamp") or "")[11:19]
    if ptype == "message":
        label = "👤" if role == "user" else "🤖"
        text = get_text(p.get("content")).replace("\n", " ")
        preview = text[:60]
    elif ptype == "function_call":
        label = "🔧"
        preview = p.get("name", "tool")
    else:
        label = "📤"
        preview = str(p.get("output") or "")[:60].replace("\n", " ")
    return f"[{index:>3}] {label} {ts} {preview}"


def entry_search_text(entry):
    p = entry.get("payload") or {}
    ptype = p.get("type")
    if ptype == "message":
        return get_text(p.get("content"))
    if ptype == "function_call":
        return p.get("name", "") + " " + p.get("arguments", "")
    return str(p.get("output") or "")


def interactive_select(entries, input_fn=input, print_fn=print):
    """Lightweight interactive picker: choose messages to export."""
    selectable = [
        e for e in entries
        if e.get("type") == "response_item"
        and (e.get("payload") or {}).get("type")
        in ("message", "function_call", "function_call_output")
    ]
    if not selectable:
        print_fn("没有可选择的导出消息。")
        return []

    selected = set()
    view = list(range(len(selectable)))

    def toggle(i):
        if i in selected:
            selected.discard(i)
        else:
            selected.add(i)

    while True:
        print_fn("\n=== 可导出消息 ===")
        for i in view:
            marker = "✓" if i in selected else " "
            print_fn(f"{marker} {entry_preview(selectable[i], i + 1)}")
        print_fn(
            "命令: 序号/范围(1,3,5-8)切换 | a全选 | /词过滤 | *重置过滤 | d完成"
        )
        raw = input_fn("> ").strip()
        if raw in ("d", "D", ""):
            break
        if raw.lower() == "a":
            selected = set(view)
        elif raw == "*":
            view = list(range(len(selectable)))
        elif raw.startswith("/"):
            kw = raw[1:].lower()
            view = [
                i for i in range(len(selectable))
                if kw in entry_search_text(selectable[i]).lower()
            ]
        else:
            for token in re.split(r"[,\s]+", raw):
                if not token:
                    continue
                if "-" in token:
                    try:
                        lo_s, hi_s = token.split("-", 1)
                        lo, hi = int(lo_s), int(hi_s)
                        for x in range(lo, hi + 1):
                            if 1 <= x <= len(selectable):
                                toggle(x - 1)
                    except ValueError:
                        pass
                else:
                    try:
                        x = int(token)
                        if 1 <= x <= len(selectable):
                            toggle(x - 1)
                    except ValueError:
                        pass

    return [selectable[i] for i in sorted(selected)]


def get_text(content):
    """Extract readable text from content list."""
    if not isinstance(content, list):
        return ""
    parts = []
    for c in content:
        t = c.get("type", "")
        if t in ("input_text", "output_text", "text"):
            text = strip_injected_blocks(c.get("text", "")).strip()
            if not text:
                continue
            # drop messages that are entirely an unclosed injected block
            if text.startswith(_UNCLOSED_PREFIXES):
                continue
            if text:
                parts.append(text)
    return "\n\n".join(parts)

def format_tool_call(payload):
    name = payload.get("name", "tool")
    args = payload.get("arguments", "")
    try:
        args_fmt = json.dumps(json.loads(args), ensure_ascii=False, indent=2)
    except (ValueError, TypeError):
        args_fmt = args
    return f"`{name}`\n```json\n{args_fmt}\n```"

def format_tool_output(payload):
    output = payload.get("output", "")
    try:
        out_fmt = json.dumps(json.loads(output), ensure_ascii=False, indent=2)
    except (ValueError, TypeError):
        out_fmt = output
    # truncate long outputs
    if len(out_fmt) > 2000:
        out_fmt = out_fmt[:2000] + "\n... (truncated)"
    return f"```\n{out_fmt}\n```"

def _fmt_duration(seconds):
    if seconds is None:
        return ""
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds} 秒"
    minutes, sec = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes} 分 {sec} 秒"
    hours, minutes = divmod(minutes, 60)
    return f"{hours} 小时 {minutes} 分"

def compute_stats(entries):
    """Count messages/tool calls and measure duration for the session."""
    user = assistant = tools = 0
    timestamps = []
    for entry in entries:
        if entry.get("type") != "response_item":
            continue
        payload = entry.get("payload") or {}
        ptype = payload.get("type")
        if ptype == "message":
            if payload.get("role") == "user":
                user += 1
            elif payload.get("role") == "assistant":
                assistant += 1
        elif ptype == "function_call":
            tools += 1
        ts = parse_entry_ts(entry.get("timestamp"))
        if ts is not None:
            timestamps.append(ts)
    duration = None
    if len(timestamps) >= 2:
        duration = (max(timestamps) - min(timestamps)).total_seconds()
    return {
        "user": user,
        "assistant": assistant,
        "tools": tools,
        "duration": duration,
        "duration_str": _fmt_duration(duration),
    }

def build_header(entries, session_id):
    meta = next((e for e in entries if e.get("type") == "session_meta"), {})
    meta_p = meta.get("payload", {})
    cwd = meta_p.get("cwd", "")
    model = meta_p.get("model_provider", "")
    originator = meta_p.get("originator", "")
    ts_raw = meta_p.get("timestamp", "")
    try:
        ts = (
            datetime.fromisoformat(str(ts_raw).replace("Z", "+00:00"))
            .astimezone()
            .strftime("%Y-%m-%d %H:%M %Z")
        )
    except (ValueError, TypeError, OverflowError):
        ts = str(ts_raw)
    lines = [
        "# Codex Session Export\n",
        f"- **Session ID:** `{session_id}`",
        f"- **Time:** {ts}",
    ]
    if originator:
        lines.append(f"- **Source:** {originator}")
    if cwd:
        lines.append(f"- **Workspace:** `{cwd}`")
    if model:
        lines.append(f"- **Model:** {model}")
    stats = compute_stats(entries)
    lines.append(f"- **Messages:** {stats['user']} 用户 / {stats['assistant']} 助手")
    if stats["tools"]:
        lines.append(f"- **Tool calls:** {stats['tools']}")
    if stats["duration_str"]:
        lines.append(f"- **Duration:** {stats['duration_str']}")
    lines.append("")
    lines.append("---\n")
    return lines


def generate_sections(entries, brief=False, since=None, until=None, grep=None, redact=False,
                      heading_level=2):
    """Render exportable entries to Markdown sections.

    - since/until: keep only entries inside the time window.
    - grep: keep only messages whose text contains the keyword (case-insensitive);
      a matched user message pulls in its full turn (reply + tool calls).
    """
    grep_lower = grep.lower() if grep else None
    in_turn = False
    sections = []

    def in_window(entry):
        dt = parse_entry_ts(entry.get("timestamp"))
        if dt is None:
            return True
        if since is not None and dt < since:
            return False
        return not (until is not None and dt > until)

    for entry in entries:
        if entry.get("type") != "response_item":
            continue
        p = entry.get("payload") or {}
        role = p.get("role")
        ptype = p.get("type")

        if not in_window(entry):
            in_turn = False
            continue

        if ptype == "message":
            text = get_text(p.get("content"))
            if not text:
                continue
            if redact:
                text = redact_text(text)
            matched = bool(grep_lower and grep_lower in text.lower())
            if role == "user":
                keep = (not grep_lower) or matched
                in_turn = matched
                if keep:
                    sections.append(f"{'#' * heading_level} 👤 User\n\n{text}\n")
            elif role == "assistant":
                if (not grep_lower) or matched or in_turn:
                    sections.append(f"{'#' * heading_level} 🤖 Codex\n\n{text}\n")
            # developer / system messages are intentionally skipped

        elif ptype == "function_call" and not brief:
            if not grep_lower or in_turn:
                text = format_tool_call(p)
                if redact:
                    text = redact_text(text)
                sections.append(f"{'#' * (heading_level + 1)} 🔧 Tool Call\n\n" + text + "\n")
        elif ptype == "function_call_output" and not brief:
            if not grep_lower or in_turn:
                text = format_tool_output(p)
                if redact:
                    text = redact_text(text)
                sections.append(f"{'#' * (heading_level + 1)} 📤 Tool Output\n\n" + text + "\n")

    return sections


def last_position_of(entries):
    """Return (max_timestamp, [ids]) of the newest response_item entries."""
    max_ts = None
    max_ids = []
    for entry in entries:
        if entry.get("type") != "response_item":
            continue
        ts_str = str(entry.get("timestamp") or "")
        if max_ts is None or ts_str > max_ts:
            max_ts = ts_str
            max_ids = []
        if ts_str == max_ts:
            eid = (entry.get("payload") or {}).get("id")
            if eid:
                max_ids.append(eid)
    return max_ts, max_ids


def read_state(path):
    """Read a checkpoint state file; returns None when missing or invalid."""
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, ValueError, TypeError):
        return None


def write_state(path, state):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def export(session_id, out_path=None, brief=False, since=None, until=None, grep=None,
           append=False, redact=False, fmt="md", interactive=False, input_fn=None):
    paths = find_rollouts(session_id)
    if not paths:
        print(
            f"ERROR: session {session_id} not found under {get_codex_home()} "
            "(sessions/ or archived_sessions/)",
            file=sys.stderr,
        )
        sys.exit(1)

    if interactive:
        if append:
            print("ERROR: --interactive cannot be combined with --append", file=sys.stderr)
            sys.exit(1)
        entries = interactive_select(
            load_entries(paths), input_fn=input_fn or input, print_fn=print
        )
        # selection is explicit: disable automatic filters for the chosen entries
        brief, since, until, grep = False, None, None, None

    if append:
        if not out_path:
            print("ERROR: --append requires an output file path", file=sys.stderr)
            sys.exit(1)
        out = Path(out_path)
        state_path = out.with_name(out.name + ".state.json")
        state = read_state(state_path)
        if state and state.get("session_id") == session_id and out.exists():
            offsets = state.get("file_offsets") or {}
        else:
            offsets = {}
        entries, new_offsets = load_entries_tail(paths, offsets)
        last_ts = None
        last_ids = set()

        def after_checkpoint(entry):
            if entry.get("type") != "response_item":
                return False
            ts_str = str(entry.get("timestamp") or "")
            if not last_ts or ts_str > last_ts:
                return True
            if ts_str == last_ts:
                eid = (entry.get("payload") or {}).get("id")
                return eid not in last_ids
            return False

        if state and state.get("session_id") == session_id:
            last_ts = state.get("last_timestamp")
            last_ids = set(state.get("last_ids") or [])
            entries_filtered = [e for e in entries if after_checkpoint(e)]
        elif out.exists():
            if since is not None:
                last_ts = since.astimezone(timezone.utc).strftime(
                    "%Y-%m-%dT%H:%M:%S.%f"
                )[:-3] + "Z"
                print(
                    f"Using --since {since.isoformat()} as the initial checkpoint "
                    f"for the existing file.",
                    file=sys.stderr,
                )
                entries_filtered = [e for e in entries if after_checkpoint(e)]
            else:
                print(
                    "WARNING: no checkpoint for this file; assuming it is up to date "
                    "and recording the current position. Re-run without --append "
                    "to regenerate the file with the latest messages.",
                    file=sys.stderr,
                )
                entries_filtered = []
        else:
            entries_filtered = entries

        sections = generate_sections(
            entries_filtered, brief=brief, since=since, until=until, grep=grep,
            redact=redact,
        )
        header = build_header(entries, session_id)
        if fmt == "html" and out.exists():
            print(
                "ERROR: --append is not supported for HTML format; "
                "re-export the full file instead.",
                file=sys.stderr,
            )
            sys.exit(1)
        if sections:
            body = "\n".join(sections)
            if fmt == "html":
                text = render_html(header, sections)
            elif out.exists():
                existing = out.read_text(encoding="utf-8")
                text = existing.rstrip("\n") + "\n\n" + body + "\n"
            elif fmt == "obsidian":
                text = render_obsidian(header, sections, session_id)
            else:
                text = "\n".join(header) + "\n" + body + "\n"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(text, encoding="utf-8")
            print(f"Incremental export appended {len(sections)} section(s) to: {out}")
        else:
            print(f"Incremental export: no new messages for session {session_id}")

        max_ts, max_ids = last_position_of(entries)
        write_state(state_path, {
            "session_id": session_id,
            "out_path": str(out),
            "brief": brief,
            "format": fmt,
            "last_timestamp": max_ts,
            "last_ids": max_ids,
            "file_offsets": new_offsets,
            "updated_at": datetime.now().astimezone().isoformat(),
        })
        return

    if not interactive:
        entries = load_entries(paths)
    sections = generate_sections(
        entries, brief=brief, since=since, until=until, grep=grep, redact=redact
    )
    header = build_header(entries, session_id)
    if fmt == "html":
        result = render_html(header, sections)
    elif fmt == "obsidian":
        result = render_obsidian(header, sections, session_id)
    else:
        result = "\n".join(header + sections)

    if out_path:
        out = Path(out_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(result + "\n", encoding="utf-8")
        print(f"Exported to: {out_path}")
    else:
        print(result)


def export_merged(session_ids, out_path=None, brief=False, since=None, until=None,
                  grep=None, redact=False, fmt="md"):
    """Export several sessions into a single document."""
    blocks = []
    for sid in session_ids:
        paths = find_rollouts(sid)
        if not paths:
            print(
                f"ERROR: session {sid} not found under {get_codex_home()} "
                "(sessions/ or archived_sessions/)",
                file=sys.stderr,
            )
            sys.exit(1)
        entries = load_entries(paths)
        sections = generate_sections(
            entries, brief=brief, since=since, until=until, grep=grep,
            redact=redact, heading_level=3,
        )
        header = build_header(entries, sid)
        meta = [
            line for line in header
            if line.strip() and not line.startswith("# ") and line.strip() != "---"
        ]
        blocks.append([f"## 📁 Session {sid}"] + meta + ["---"] + sections)

    flat = [line for block in blocks for line in block]
    overview = [
        "# Codex Sessions Export（合并）",
        f"- **Sessions:** {len(session_ids)}",
        "",
        "---\n",
    ]
    if fmt == "html":
        result = render_html(overview, flat, title="Codex Sessions Export（合并）")
    elif fmt == "obsidian":
        frontmatter = (
            "---\n"
            'title: "Codex Sessions Export（合并）"\n'
            "session_id: merged\n"
            "tags:\n  - codex\n  - session\n  - merged\n"
            "---\n\n"
        )
        result = frontmatter + "\n".join(overview + flat)
    else:
        result = "\n".join(overview + flat)

    if out_path:
        out = Path(out_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(result + "\n", encoding="utf-8")
        print(f"Exported to: {out_path}")
    else:
        print(result)


def watch_loop(session_id, out_path, interval=30, brief=False, since=None, until=None,
               grep=None, redact=False, fmt="md", sleep_fn=time.sleep):
    """Poll the session periodically and append new messages (Ctrl+C to stop)."""
    print(f"Watch mode: polling session {session_id} every {interval}s (Ctrl+C 停止)")
    while True:
        try:
            export(
                session_id, out_path, brief=brief, since=since, until=until,
                grep=grep, append=True, redact=redact, fmt=fmt,
            )
        except KeyboardInterrupt:
            print("\nWatch mode stopped.")
            break
        try:
            sleep_fn(interval)
        except KeyboardInterrupt:
            print("\nWatch mode stopped.")
            break


def list_sessions(limit=15):
    db = get_codex_home() / "state_5.sqlite"
    if not db.exists():
        print(f"No {db} found.")
        return
    con = sqlite3.connect(str(db))
    rows = con.execute(
        "SELECT id, title, source, created_at FROM threads ORDER BY created_at DESC LIMIT ?",
        (limit,)
    ).fetchall()
    con.close()
    print(f"{'#':<3} {'Source':<8} {'Date':<17} Title")
    print("-" * 80)
    for i, (sid, title, source, ts) in enumerate(rows):
        try:
            dt = datetime.fromtimestamp(ts / 1000, timezone.utc).astimezone().strftime(
                "%m-%d %H:%M"
            )
        except (ValueError, OverflowError, OSError, TypeError):
            dt = "?"
        short_title = (title or "")[:55].replace("\n", " ")
        if len(title or "") > 55:
            short_title += "…"
        print(f"{i+1:<3} {source:<8} {dt:<17} {short_title}")
        print(f"    id: {sid}")


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    argv = list(sys.argv[1:] if argv is None else argv)
    positionals = []
    flags = []
    values = {}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--since", "--until", "--grep", "--format", "--sessions"):
            if i + 1 >= len(argv):
                print(f"ERROR: {a} requires a value", file=sys.stderr)
                sys.exit(1)
            values[a] = argv[i + 1]
            i += 2
        elif a == "--watch":
            flags.append(a)
            if i + 1 < len(argv) and argv[i + 1].isdigit():
                values["--watch"] = int(argv[i + 1])
                i += 2
            else:
                i += 1
        elif a.startswith("-"):
            flags.append(a)
            i += 1
        else:
            positionals.append(a)
            i += 1

    brief = "--brief" in flags or "-b" in flags
    append = "--append" in flags or "-a" in flags
    redact = "--redact" in flags or "-r" in flags
    interactive = "--interactive" in flags or "-i" in flags

    if "--list" in flags or "-l" in flags:
        list_sessions()
        sys.exit(0)

    if len(positionals) < 1:
        print("Usage:")
        print("  python3 scripts/export.py --list")
        print("  python3 scripts/export.py <session-id> [output.md] [options]")
        print("Options: --brief, --redact, --since <datetime>, --until <datetime>, --grep <text>, --append")
        sys.exit(1)

    session_id = positionals[0]
    out_path = positionals[1] if len(positionals) > 1 else None
    since = parse_dt(values["--since"]) if "--since" in values else None
    until = parse_dt(values["--until"]) if "--until" in values else None
    grep = values.get("--grep")
    fmt = values.get("--format", "md").lower()
    if fmt not in ("md", "html", "obsidian"):
        print(f"ERROR: unsupported --format '{fmt}' (use md, html, or obsidian)", file=sys.stderr)
        sys.exit(1)

    if "--sessions" in values:
        session_ids = [s.strip() for s in values["--sessions"].split(",") if s.strip()]
        if len(session_ids) < 2:
            print("ERROR: --sessions requires at least two session ids", file=sys.stderr)
            sys.exit(1)
        merged_out = positionals[0] if positionals else None
        export_merged(
            session_ids, merged_out, brief=brief, since=since, until=until,
            grep=grep, redact=redact, fmt=fmt,
        )
        sys.exit(0)

    if "--watch" in flags:
        if not out_path:
            print("ERROR: --watch requires an output file path", file=sys.stderr)
            sys.exit(1)
        watch_loop(
            session_id, out_path,
            interval=values.get("--watch", 30),
            brief=brief, since=since, until=until, grep=grep,
            redact=redact, fmt=fmt,
        )
        sys.exit(0)

    export(session_id, out_path, brief=brief, since=since, until=until, grep=grep,
           append=append, redact=redact, fmt=fmt, interactive=interactive)
    return 0


if __name__ == "__main__":
    sys.exit(main())
