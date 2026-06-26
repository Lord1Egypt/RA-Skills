#!/usr/bin/env python3
"""
Lightweight task debug report generator for OpenClaw agents.

Reads the most recent session JSONL, extracts execution data for a given task_id,
and outputs a JSON report compatible with POST /api/lobster/tasks/{id}/debug-report.

Usage:
    python3 local_debugger.py <task_id>
    python3 local_debugger.py <task_id> --session <session_file>

Exit codes:
    0 — report printed to stdout (JSON)
    1 — task not found or parse error (message on stderr)
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

OPENCLAW_DIR = os.path.expanduser("~/.openclaw")
SESSIONS_DIR = os.path.join(OPENCLAW_DIR, "agents", "main", "sessions")

TASK_ID_RE = re.compile(
    r"/tasks/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"
)

CURL_RE = re.compile(
    r'curl\s+.*?(-X\s+(GET|POST|PUT|PATCH|DELETE))?\s*'
    r'["\']?(https?://[^\s"\'\\]+)["\']?',
    re.IGNORECASE,
)


def _parse_ts(ts_str: str) -> Optional[datetime]:
    if not ts_str:
        return None
    try:
        return datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def _call_type(method: str, endpoint: str) -> str:
    ep = endpoint.lower()
    if "heartbeat" in ep:
        return "heartbeat"
    if "/claim" in ep:
        return "claim"
    if "/artifact" in ep:
        return "submit"
    if "/tasks" in ep and method == "GET":
        return "poll"
    if "/tasks" in ep and method in ("PATCH", "PUT"):
        return "status_update"
    return "other"


def _task_id_from_endpoint(endpoint: str) -> Optional[str]:
    m = TASK_ID_RE.search(endpoint)
    return m.group(1) if m else None


def _extract_api_calls(cmd: str, ts: datetime):
    calls = []
    for m in CURL_RE.finditer(cmd):
        url = m.group(3) or ""
        method = m.group(2) or ("POST" if "-X POST" in cmd or "-d " in cmd else "GET")
        if "/api/" in url or "lobster" in url:
            endpoint = re.sub(r"https?://[^/]+", "", url).split("?")[0]
            calls.append({
                "ts": ts, "method": method.upper(), "endpoint": endpoint,
                "url": url, "tool_name": "exec/curl",
                "response": "", "duration_ms": 0,
            })
    return calls


_UUID_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")


def _extract_api_calls_from_result(result_text: str, ts: datetime):
    """Fallback: extract API calls from toolResult text when command URLs
    use bash variables (e.g. $BASE/api/lobster/tasks/$TASK_ID/claim).
    Uses keyword heuristics on the result text instead of JSON parsing."""
    calls = []
    text_lower = result_text.lower()

    # Detect claim: various patterns from poll.sh or LLM-generated scripts
    # "Claiming Task: <uuid>", "Attempting to Claim: <uuid>", "Claim: <uuid>"
    claim_match = re.search(
        r"(?:[Cc]laiming [Tt]ask|[Aa]ttempting to [Cc]laim|[Cc]laim):\s*(" + _UUID_RE.pattern + r")",
        result_text,
    )
    if claim_match:
        tid = claim_match.group(1)
        resp = ""
        resp_match = re.search(r"Result:\s*\{", result_text[claim_match.end():])
        if resp_match:
            raw = result_text[claim_match.end() + resp_match.start() + len("Result: "):]
            cleaned = raw.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
            try:
                obj, _ = json.JSONDecoder().raw_decode(cleaned)
                resp = json.dumps(obj, ensure_ascii=False)
            except (json.JSONDecodeError, ValueError):
                pass
        calls.append({
            "ts": ts, "method": "POST",
            "endpoint": f"/api/lobster/tasks/{tid}/claim",
            "url": "", "tool_name": "exec/inferred",
            "response": resp, "duration_ms": 0,
        })

    # Detect submit: look for "Submit:" (the output echo from poll.sh).
    # If claim was found, reuse its task ID (since bash vars obscure the UUID).
    submit_marker = re.search(r"\bSubmit:\s", result_text)
    if submit_marker:
        # Determine task ID: from explicit UUID near submit, or fallback to claim tid
        submit_tid = None
        submit_patterns = [
            re.compile(r"[Ss]ubmit\S*\s+.*?(" + _UUID_RE.pattern + r")"),
            re.compile(r"artifact\S*\s+.*?(" + _UUID_RE.pattern + r")"),
        ]
        for pat in submit_patterns:
            m = pat.search(result_text, submit_marker.start())
            if m:
                submit_tid = m.group(1)
                break
        if not submit_tid and claim_match:
            submit_tid = claim_match.group(1)
        if submit_tid:
            resp = ""
            after_submit = result_text[submit_marker.end():]
            cleaned = after_submit.replace("\n", "\\n").replace("\r", "\\r")
            json_start = cleaned.find("{")
            if json_start >= 0:
                try:
                    obj, _ = json.JSONDecoder().raw_decode(cleaned, json_start)
                    resp = json.dumps(obj, ensure_ascii=False)[:3000]
                except (json.JSONDecodeError, ValueError):
                    pass
            calls.append({
                "ts": ts, "method": "POST",
                "endpoint": f"/api/lobster/tasks/{submit_tid}/artifacts",
                "url": "", "tool_name": "exec/inferred",
                "response": resp, "duration_ms": 0,
            })

    return calls


def _tool_summary(name: str, args: dict) -> str:
    if name == "exec":
        cmd = args.get("command", "")
        return cmd[:120] + "..." if len(cmd) > 120 else cmd
    if name == "browser":
        return f"{args.get('action', '')} {args.get('targetUrl', '')}".strip()
    if name == "web_fetch":
        return args.get("url", "")
    if name == "read":
        return args.get("file_path", "")
    if name == "write":
        fp = args.get("file_path", "")
        content = args.get("content", "")
        return f"{fp} ({len(content)} chars)"
    return str(args)[:100]


def _check_submit(text: str) -> Optional[bool]:
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            if data.get("status") in ("received", "accepted"):
                return True
            if "artifact_id" in data:
                return True
            if "error" in data or "detail" in data:
                return False
    except (json.JSONDecodeError, ValueError):
        pass
    if "500" in text[:50] or "error" in text[:100].lower():
        return False
    return None


def _extract_error_msg(text: str) -> str:
    if len(text) <= 200:
        return text
    for pat in [r'"error"\s*:\s*"([^"]+)"', r"Error:\s*(.+?)(?:\n|$)"]:
        m = re.search(pat, text)
        if m:
            return m.group(1)[:200]
    return text[:200]


def _parse_task_meta(text: str) -> dict:
    try:
        data = json.loads(text)
        if isinstance(data, dict) and "id" in data:
            spec = data.get("structured_spec", {}) or {}
            return {
                "title": data.get("title", ""),
                "task_type": data.get("task_type", ""),
                "budget": str(data.get("budget_max", "")),
                "target_url": spec.get("target_url", ""),
                "skill_id": data.get("resolved_skill_id", ""),
            }
    except (json.JSONDecodeError, ValueError):
        pass
    return {}


def _link_responses(api_calls, result_text, duration_ms):
    if len(api_calls) == 1:
        api_calls[0]["response"] = result_text[:3000]
        api_calls[0]["duration_ms"] = duration_ms
        return
    depth = 0
    start = None
    jsons = []
    for i, ch in enumerate(result_text):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                jsons.append(result_text[start : i + 1])
                start = None
    if not jsons:
        jsons = [result_text]
    for idx, ac in enumerate(api_calls):
        if idx < len(jsons):
            ac["response"] = jsons[idx]
            ac["duration_ms"] = duration_ms


def analyze_session_for_task(jsonl_path: str, target_task_id: str) -> Optional[dict]:
    """Parse a session JSONL and extract the execution trace for target_task_id."""

    events = []
    with open(jsonl_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    session_id = ""
    if events and events[0].get("type") == "session":
        session_id = events[0].get("id", "")

    all_api_calls = []
    all_tool_calls = []
    all_thinking = []
    all_costs = []
    pending = {}
    tc_to_apis = {}
    start_time = None
    end_time = None

    for ev in events:
        ts_str = ev.get("timestamp", "")
        ts = _parse_ts(ts_str)
        if ts:
            if start_time is None:
                start_time = ts
            end_time = ts

        if ev.get("type") != "message":
            continue

        msg = ev.get("message", {})
        role = msg.get("role", "")
        content = msg.get("content", [])

        if role == "assistant":
            usage = msg.get("usage", {})
            if usage:
                cost_info = usage.get("cost", {})
                all_costs.append({
                    "ts": ts,
                    "cost": cost_info.get("total", 0),
                    "input": usage.get("input", 0),
                    "output": usage.get("output", 0),
                })

            for part in content:
                if part.get("type") == "thinking":
                    text = part.get("thinking", "").strip()
                    if text:
                        all_thinking.append({"ts": ts_str, "text": text[:300]})
                elif part.get("type") == "toolCall":
                    tool_id = part.get("id", "")
                    name = part.get("name", "")
                    args = part.get("arguments", {})
                    pending[tool_id] = {"ts": ts, "name": name, "arguments": args}
                    if name == "exec" and "command" in args:
                        extracted = _extract_api_calls(args["command"], ts)
                        if extracted:
                            tc_to_apis[tool_id] = extracted
                            all_api_calls.extend(extracted)

        elif role == "toolResult":
            tool_id = msg.get("toolCallId", "")
            is_error = msg.get("isError", False)
            details = msg.get("details", {})
            duration_ms = details.get("durationMs", 0)
            result_text = ""
            for part in content:
                if part.get("type") == "text":
                    result_text += part.get("text", "")

            p = pending.pop(tool_id, {})
            tc = {
                "ts": p.get("ts", ts),
                "name": p.get("name", msg.get("toolName", "")),
                "arguments": p.get("arguments", {}),
                "result": result_text,
                "is_error": is_error or "error" in result_text.lower()[:100],
                "duration_ms": duration_ms,
            }
            all_tool_calls.append(tc)

            linked = tc_to_apis.pop(tool_id, [])
            if linked:
                _link_responses(linked, result_text, duration_ms)
            elif p.get("name") == "exec" and tool_id not in tc_to_apis:
                inferred = _extract_api_calls_from_result(result_text, p.get("ts", ts))
                if inferred:
                    all_api_calls.extend(inferred)

    timeline = []
    for ac in all_api_calls:
        if ac["ts"]:
            timeline.append((ac["ts"], "api", ac))
    for tc in all_tool_calls:
        if tc["ts"]:
            timeline.append((tc["ts"], "tool", tc))
    for th in all_thinking:
        ts = _parse_ts(th["ts"])
        if ts:
            timeline.append((ts, "thinking", th))
    for ci in all_costs:
        if ci["ts"]:
            timeline.append((ci["ts"], "cost", ci))
    timeline.sort(key=lambda x: x[0])

    # Segment by task — find the one matching target_task_id
    class Task:
        def __init__(self, tid):
            self.task_id = tid
            self.title = ""
            self.task_type = ""
            self.budget = ""
            self.target_url = ""
            self.skill_id = ""
            self.start_time = None
            self.end_time = None
            self.api_calls = []
            self.tool_calls = []
            self.thinking = []
            self.errors = []
            self.llm_cost = 0.0
            self.llm_input_tokens = 0
            self.llm_output_tokens = 0
            self.submitted = False
            self.submit_success = None

        @property
        def outcome(self):
            if self.submitted and self.submit_success:
                return "success"
            if self.submitted and self.submit_success is False:
                return "submit_failed"
            if self.submitted:
                return "submitted"
            if self.errors:
                return "error"
            return "incomplete"

        @property
        def duration(self):
            if self.start_time and self.end_time:
                return (self.end_time - self.start_time).total_seconds()
            return None

    tasks = []
    current = None
    orphan_api = []

    for ts, kind, obj in timeline:
        if kind == "api":
            tid = _task_id_from_endpoint(obj["endpoint"])
            ct = _call_type(obj["method"], obj["endpoint"])

            if ct == "claim" and tid:
                if current:
                    current.end_time = ts
                    tasks.append(current)
                current = Task(tid)
                current.start_time = ts
                reattach = []
                for oa in reversed(orphan_api):
                    oact = _call_type(oa["method"], oa["endpoint"])
                    if oact in ("heartbeat", "poll"):
                        reattach.insert(0, oa)
                    else:
                        break
                for oa in reattach:
                    orphan_api.remove(oa)
                    current.api_calls.append(oa)
                    if oa["ts"] and (not current.start_time or oa["ts"] < current.start_time):
                        current.start_time = oa["ts"]
                current.api_calls.append(obj)
                if obj.get("response"):
                    meta = _parse_task_meta(obj["response"])
                    if meta:
                        current.title = meta.get("title", "")
                        current.task_type = meta.get("task_type", "")
                        current.budget = meta.get("budget", "")
                        current.target_url = meta.get("target_url", "")
                        current.skill_id = meta.get("skill_id", "")
            elif current and tid and tid == current.task_id:
                current.api_calls.append(obj)
                if ct == "submit":
                    current.submitted = True
                    current.submit_success = _check_submit(obj.get("response", ""))
            elif current and ct in ("heartbeat", "poll") and not tid:
                current.api_calls.append(obj)
            elif current and not tid:
                current.api_calls.append(obj)
            else:
                orphan_api.append(obj)

        elif kind == "tool":
            if current:
                current.tool_calls.append(obj)
                if obj["is_error"]:
                    current.errors.append({
                        "ts": ts.isoformat() if ts else "",
                        "tool": obj["name"],
                        "error": _extract_error_msg(obj["result"]),
                    })

        elif kind == "thinking":
            if current:
                current.thinking.append(obj)

        elif kind == "cost":
            if current:
                current.llm_cost += obj.get("cost", 0)
                current.llm_input_tokens += obj.get("input", 0)
                current.llm_output_tokens += obj.get("output", 0)

    if current:
        current.end_time = end_time
        tasks.append(current)

    found = None
    for t in tasks:
        if t.task_id == target_task_id:
            found = t
            break

    if not found:
        return None

    return {
        "task_id": found.task_id,
        "session_id": session_id,
        "title": found.title,
        "task_type": found.task_type,
        "budget": found.budget,
        "target_url": found.target_url,
        "skill_id": found.skill_id,
        "outcome": found.outcome,
        "submitted": found.submitted,
        "submit_success": found.submit_success,
        "start_time": found.start_time.isoformat() if found.start_time else None,
        "end_time": found.end_time.isoformat() if found.end_time else None,
        "duration_seconds": found.duration,
        "llm_cost": found.llm_cost,
        "llm_input_tokens": found.llm_input_tokens,
        "llm_output_tokens": found.llm_output_tokens,
        "api_calls": [
            {
                "ts": (ac["ts"].isoformat() if isinstance(ac["ts"], datetime) else ac["ts"]) if ac.get("ts") else None,
                "type": _call_type(ac["method"], ac["endpoint"]),
                "method": ac["method"],
                "endpoint": ac["endpoint"],
                "duration_ms": ac.get("duration_ms", 0),
            }
            for ac in found.api_calls
        ],
        "tool_calls": [
            {
                "ts": (tc["ts"].isoformat() if isinstance(tc["ts"], datetime) else tc["ts"]) if tc.get("ts") else None,
                "name": tc["name"],
                "summary": _tool_summary(tc["name"], tc.get("arguments", {})),
                "is_error": tc["is_error"],
                "duration_ms": tc.get("duration_ms", 0),
            }
            for tc in found.tool_calls
        ],
        "errors": found.errors,
        "thinking": found.thinking,
        "report_phase": 2,
    }


def find_latest_session() -> Optional[str]:
    """Find the most recently modified session JSONL file."""
    sessions_dir = Path(SESSIONS_DIR)
    if not sessions_dir.exists():
        return None
    jsonl_files = sorted(
        sessions_dir.glob("*.jsonl"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return str(jsonl_files[0]) if jsonl_files else None


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 local_debugger.py <task_id> [--session <file>]", file=sys.stderr)
        sys.exit(1)

    task_id = sys.argv[1]
    session_file = None

    if "--session" in sys.argv:
        idx = sys.argv.index("--session")
        if idx + 1 < len(sys.argv):
            session_file = sys.argv[idx + 1]

    if session_file and os.path.isfile(session_file):
        files_to_search = [session_file]
    else:
        sessions_dir = Path(SESSIONS_DIR)
        if not sessions_dir.exists():
            print(f"Sessions directory not found: {SESSIONS_DIR}", file=sys.stderr)
            sys.exit(1)
        all_jsonl = list(sessions_dir.glob("*.jsonl"))
        # Sort by size desc first (task sessions are larger), then by mtime desc
        files_to_search = sorted(
            all_jsonl,
            key=lambda p: (-p.stat().st_size, -p.stat().st_mtime),
        )

    for f in files_to_search:
        # Quick pre-check: grep for task_id before full parse
        with open(f, "r", encoding="utf-8", errors="replace") as fh:
            content = fh.read()
        if task_id not in content:
            continue
        result = analyze_session_for_task(str(f), task_id)
        if result:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            sys.exit(0)

    print(f"Task {task_id} not found in recent sessions", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
