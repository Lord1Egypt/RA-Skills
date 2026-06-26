#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import deque
from pathlib import Path
from typing import Any

DEFAULT_FIELDS = {
    "task": "任务：",
    "status": "状态：",
    "result": "结果：",
    "risk": "风险：",
}

STATUS_MAP = {
    "已完成": "completed",
    "完成": "completed",
    "completed": "completed",
    "done": "completed",
    "有阻塞": "blocked",
    "阻塞": "blocked",
    "blocked": "blocked",
    "卡住": "blocked",
    "已接收": "accepted",
    "接收": "accepted",
    "accepted": "accepted",
    "进行中": "in-progress",
    "处理中": "in-progress",
    "in-progress": "in-progress",
    "进行": "in-progress",
    "失败": "failed",
    "错误": "error",
    "error": "error",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="check_agent_task_status.py",
        description=(
            "Inspect OpenClaw agent session transcripts and summarize the latest assignment/report status. "
            "Supports configurable agent roots, agent lists, session key templates, keywords, filters, and output formats."
        ),
    )
    parser.add_argument(
        "--base",
        default=os.environ.get("OPENCLAW_AGENTS_BASE", str(Path.home() / ".openclaw" / "agents")),
        help="Agents root directory (default: ~/.openclaw/agents or OPENCLAW_AGENTS_BASE)",
    )
    parser.add_argument(
        "--agents",
        default=os.environ.get("OPENCLAW_AGENT_IDS", ""),
        help="Comma-separated agent IDs. If omitted, use --agent-file or --discover.",
    )
    parser.add_argument("--agent-file", help="Read agent IDs from file (one per line).")
    parser.add_argument("--discover", action="store_true", help="Auto-discover agents under --base when agent list is omitted.")
    parser.add_argument(
        "--session-key-template",
        default=os.environ.get("OPENCLAW_SESSION_KEY_TEMPLATE", "agent:{agent}:main"),
        help="Template for target session key (default: agent:{agent}:main)",
    )
    parser.add_argument(
        "--assign-keyword",
        default=os.environ.get("OPENCLAW_ASSIGN_KEYWORD", "正式任务分配："),
        help="Keyword that identifies an assignment in user messages.",
    )
    parser.add_argument("--task-prefix", default=os.environ.get("OPENCLAW_TASK_PREFIX", DEFAULT_FIELDS["task"]))
    parser.add_argument("--status-prefix", default=os.environ.get("OPENCLAW_STATUS_PREFIX", DEFAULT_FIELDS["status"]))
    parser.add_argument("--result-prefix", default=os.environ.get("OPENCLAW_RESULT_PREFIX", DEFAULT_FIELDS["result"]))
    parser.add_argument("--risk-prefix", default=os.environ.get("OPENCLAW_RISK_PREFIX", DEFAULT_FIELDS["risk"]))
    parser.add_argument("--format", choices=["table", "summary", "json", "jsonl"], default=os.environ.get("OPENCLAW_OUTPUT_FORMAT", "table"))
    parser.add_argument("--tail", type=int, default=0, help="Only scan the last N lines of each transcript (0 = full file).")
    parser.add_argument("--strict", action="store_true", help="Return exit code 1 when any agent is missing assignment/report/error.")
    parser.add_argument("--verbose", action="store_true", help="Print extra diagnostics to stderr.")
    parser.add_argument(
        "--only-status",
        help="Filter results by normalized status. Comma-separated values like completed,blocked,accepted,no-assignment,assigned-no-report,error.",
    )
    parser.add_argument(
        "--contains",
        help="Filter results by keyword match across assignment text, task, result, risk, and raw report text.",
    )
    parser.add_argument(
        "--output-file",
        help="Write final output to file instead of stdout.",
    )
    return parser.parse_args()


def extract_text(content: Any) -> str:
    if not isinstance(content, list):
        return ""
    parts = []
    for item in content:
        if isinstance(item, dict) and item.get("type") == "text":
            parts.append(item.get("text", ""))
    return "\n".join(x for x in parts if x)


def parse_report(text: str, fields: dict[str, str]) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        for key, prefix in fields.items():
            if line.startswith(prefix):
                data[key] = line.split(prefix, 1)[1].strip()
    return data


def normalize_status(raw: str | None) -> str:
    if not raw:
        return "unknown"
    s = raw.strip()
    return STATUS_MAP.get(s, s.lower().replace(" ", "-"))


def load_agents(args: argparse.Namespace, base: Path) -> list[str]:
    agents: list[str] = []
    if args.agents:
        agents.extend([a.strip() for a in args.agents.split(",") if a.strip()])
    if args.agent_file:
        fp = Path(args.agent_file)
        agents.extend([line.strip() for line in fp.read_text(encoding="utf-8").splitlines() if line.strip() and not line.strip().startswith("#")])
    if not agents:
        if args.discover and base.exists():
            agents.extend(sorted(p.name for p in base.iterdir() if p.is_dir()))
        else:
            agents = ["xiaocheng", "xiaowen", "xiaobian"]
    seen = set()
    ordered = []
    for a in agents:
        if a not in seen:
            ordered.append(a)
            seen.add(a)
    return ordered


def iter_lines(path: Path, tail: int):
    if tail > 0:
        with path.open("r", encoding="utf-8") as f:
            for line in deque(f, maxlen=tail):
                yield line
    else:
        with path.open("r", encoding="utf-8") as f:
            yield from f


def load_session(index_path: Path, session_key: str):
    obj = json.loads(index_path.read_text(encoding="utf-8"))
    sess = obj.get(session_key)
    if not sess:
        return None, f"session key not found: {session_key}"
    session_file = sess.get("sessionFile")
    if not session_file:
        return None, f"session file missing in index for: {session_key}"
    return {
        "sessionKey": session_key,
        "sessionFile": Path(session_file),
        "updatedAt": sess.get("updatedAt"),
    }, None


def inspect_agent(agent_id: str, args: argparse.Namespace, base: Path, fields: dict[str, str]) -> dict[str, Any]:
    result: dict[str, Any] = {"agent": agent_id, "indexFile": str(base / agent_id / "sessions" / "sessions.json")}
    index_path = Path(result["indexFile"])
    if not index_path.exists():
        result["error"] = f"index file not found: {index_path}"
        result["status"] = "error"
        result["status_raw"] = "error"
        return result

    session_key = args.session_key_template.format(agent=agent_id)
    session_meta, err = load_session(index_path, session_key)
    if err:
        result.update({"sessionKey": session_key, "error": err, "status": "error", "status_raw": "error"})
        return result
    result.update(session_meta)
    session_file = session_meta["sessionFile"]
    if not session_file.exists():
        result["error"] = f"session file not found: {session_file}"
        result["status"] = "error"
        result["status_raw"] = "error"
        return result

    last_assignment = None
    last_report = None
    for raw in iter_lines(session_file, args.tail):
        raw = raw.strip()
        if not raw:
            continue
        try:
            obj = json.loads(raw)
        except Exception:
            continue
        if obj.get("type") != "message":
            continue
        msg = obj.get("message", {})
        role = msg.get("role")
        text = extract_text(msg.get("content", []))
        ts = obj.get("timestamp")
        if role == "user" and args.assign_keyword in text:
            last_assignment = {"timestamp": ts, "text": text}
            last_report = None
        elif role == "assistant" and last_assignment and any(prefix in text for prefix in fields.values()):
            parsed = parse_report(text, fields)
            if parsed:
                last_report = {"timestamp": ts, "text": text, "parsed": parsed}

    if last_assignment:
        result["assignment"] = last_assignment
    if last_report:
        parsed = dict(last_report["parsed"])
        parsed["status_raw"] = parsed.get("status", "")
        parsed["status_normalized"] = normalize_status(parsed.get("status"))
        last_report["parsed"] = parsed
        result["report"] = last_report
        result["status_raw"] = parsed["status_raw"]
        result["status"] = parsed["status_normalized"]
    elif last_assignment:
        result["status_raw"] = "assigned-no-report"
        result["status"] = "assigned-no-report"
    else:
        result["status_raw"] = "no-assignment"
        result["status"] = "no-assignment"
    return result


def match_contains(result: dict[str, Any], keyword: str | None) -> bool:
    if not keyword:
        return True
    needle = keyword.lower()
    pool = [
        result.get("agent", ""),
        result.get("status", ""),
        result.get("status_raw", ""),
        result.get("error", ""),
    ]
    if result.get("assignment"):
        pool.append(result["assignment"].get("text", ""))
    if result.get("report"):
        pool.append(result["report"].get("text", ""))
        parsed = result["report"].get("parsed", {})
        for key in ["task", "result", "risk", "status_raw", "status_normalized"]:
            pool.append(parsed.get(key, ""))
    haystack = "\n".join(str(x) for x in pool if x)
    return needle in haystack.lower()


def filter_results(results: list[dict[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
    filtered = list(results)
    if args.only_status:
        allowed = {x.strip().lower() for x in args.only_status.split(",") if x.strip()}
        filtered = [r for r in filtered if str(r.get("status", "")).lower() in allowed]
    if args.contains:
        filtered = [r for r in filtered if match_contains(r, args.contains)]
    return filtered


def render_table(results: list[dict[str, Any]]) -> str:
    lines = ["Agent task status", "=" * 88]
    for r in results:
        lines.append(f"Agent: {r['agent']}")
        if r.get("error"):
            lines.append(f"  Error      : {r['error']}")
            lines.append("-" * 88)
            continue
        lines.append(f"  sessionKey : {r['sessionKey']}")
        lines.append(f"  sessionFile: {r['sessionFile']}")
        lines.append(f"  updatedAt  : {r.get('updatedAt')}")
        lines.append(f"  status     : {r.get('status')} (raw: {r.get('status_raw')})")
        if not r.get("assignment"):
            lines.append("  assignment : not found")
            lines.append("-" * 88)
            continue
        lines.append(f"  assignedAt : {r['assignment']['timestamp']}")
        assign_line = next((ln.strip() for ln in r['assignment']['text'].splitlines() if ln.strip()), "")
        lines.append(f"  assignText : {assign_line[:200]}")
        if r.get("report"):
            parsed = r['report']['parsed']
            lines.append(f"  reportAt   : {r['report']['timestamp']}")
            lines.append(f"  task       : {parsed.get('task', '(not parsed)')}")
            lines.append(f"  reportStat : {parsed.get('status_normalized', '(not parsed)')} (raw: {parsed.get('status_raw', '(not parsed)')})")
            lines.append(f"  result     : {parsed.get('result', '(not parsed)')}")
            lines.append(f"  risk       : {parsed.get('risk', '(not parsed)')}")
        else:
            lines.append("  report     : not found")
        lines.append("-" * 88)
    return "\n".join(lines)


def render_summary(results: list[dict[str, Any]]) -> str:
    lines = []
    for r in results:
        if r.get("error"):
            lines.append(f"{r['agent']}: ERROR | {r['error']}")
            continue
        if r.get("report"):
            p = r['report']['parsed']
            lines.append(f"{r['agent']}: {p.get('status_normalized', r.get('status'))} | {p.get('task', '-') } | {p.get('result', '-')}")
        elif r.get("assignment"):
            lines.append(f"{r['agent']}: assigned-no-report | assignment found but no report")
        else:
            lines.append(f"{r['agent']}: no-assignment")
    return "\n".join(lines)


def render_output(results: list[dict[str, Any]], fmt: str) -> str:
    if fmt == "json":
        return json.dumps(results, ensure_ascii=False, indent=2, default=str)
    if fmt == "jsonl":
        return "\n".join(json.dumps(r, ensure_ascii=False, default=str) for r in results)
    if fmt == "summary":
        return render_summary(results)
    return render_table(results)


def write_output(text: str, output_file: str | None):
    if output_file:
        out = Path(output_file).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + ("" if text.endswith("\n") else "\n"), encoding="utf-8")
        print(f"saved output to {out}", file=sys.stderr)
    else:
        print(text)


def main() -> int:
    args = parse_args()
    base = Path(args.base).expanduser()
    fields = {
        "task": args.task_prefix,
        "status": args.status_prefix,
        "result": args.result_prefix,
        "risk": args.risk_prefix,
    }
    agents = load_agents(args, base)
    if not agents:
        print("No agents resolved. Provide --agents, --agent-file, or --discover.", file=sys.stderr)
        return 2
    if args.verbose:
        print(f"[debug] base={base}", file=sys.stderr)
        print(f"[debug] agents={agents}", file=sys.stderr)
        print(f"[debug] session_key_template={args.session_key_template}", file=sys.stderr)
        print(f"[debug] assign_keyword={args.assign_keyword}", file=sys.stderr)
        print(f"[debug] fields={fields}", file=sys.stderr)
        if args.only_status:
            print(f"[debug] only_status={args.only_status}", file=sys.stderr)
        if args.contains:
            print(f"[debug] contains={args.contains}", file=sys.stderr)
    results = [inspect_agent(agent_id, args, base, fields) for agent_id in agents]
    results = filter_results(results, args)
    write_output(render_output(results, args.format), args.output_file)
    if args.strict:
        for r in results:
            if r.get("error") or r.get("status") in {"no-assignment", "assigned-no-report", "error"}:
                return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
