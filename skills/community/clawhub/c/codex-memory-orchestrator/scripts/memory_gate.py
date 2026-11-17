#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统一记忆闸门：token-usage 实测指标 + memory-orchestrator 轮数/token 判定。

只读取指定 thread_id 的 rollout 文件名与用量记录，不读取无关会话正文，不联网。
默认调用 agent_hook.sh；不加 --dry-run 时只把计数和判定写入本机 state.json。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import monitor_dialogs  # noqa: E402

TURN_THRESHOLD = int(os.environ.get("TURN_THRESHOLD", "8"))
TURN_WARN_AT = int(os.environ.get("TURN_WARN_AT", "7"))
TOKEN_THRESHOLD = int(os.environ.get("TOKEN_THRESHOLD", "150000"))
TOKEN_WARN_AT = int(os.environ.get("TOKEN_WARN_AT", "130000"))
REQUEST_PEAK_THRESHOLD = int(os.environ.get("REQUEST_PEAK_THRESHOLD", "100000"))
REQUEST_COUNT_THRESHOLD = int(os.environ.get("REQUEST_COUNT_THRESHOLD", "120"))
INPUT_TOTAL_THRESHOLD = int(os.environ.get("INPUT_TOTAL_THRESHOLD", "8000000"))
DEFAULT_TOKEN_USAGE = Path.home() / ".codex" / "scripts" / "token-usage.sh"
DEFAULT_STATE = HERE / "state.py"


def evaluate_gate(metrics):
    """纯函数：任一硬条件满足即返回 trigger=True；提前线只提醒，不触发恢复包。"""
    turns = int(metrics.get("turns") or 0)
    token_count = int(metrics.get("cumulative_token") or 0)
    peak = int(metrics.get("request_peak_input") or 0)
    requests = int(metrics.get("requests") or 0)
    input_total = int(metrics.get("input_total") or 0)
    gates = {
        "turns": turns >= TURN_THRESHOLD,
        "tokens": token_count >= TOKEN_THRESHOLD,
        "request_peak": peak >= REQUEST_PEAK_THRESHOLD,
        "requests": requests >= REQUEST_COUNT_THRESHOLD,
        "input_total": input_total >= INPUT_TOTAL_THRESHOLD,
    }
    reasons = [
        name for name, passed in gates.items()
        if passed
    ]
    warning = not any(gates.values()) and (
        turns >= TURN_WARN_AT or token_count >= TOKEN_WARN_AT
    )
    return {
        "trigger": any(gates.values()),
        "warning": warning,
        "gates": gates,
        "reasons": reasons,
        "thresholds": {
            "turns": TURN_THRESHOLD,
            "turns_warn": TURN_WARN_AT,
            "tokens": TOKEN_THRESHOLD,
            "tokens_warn": TOKEN_WARN_AT,
            "request_peak_input": REQUEST_PEAK_THRESHOLD,
            "requests": REQUEST_COUNT_THRESHOLD,
            "input_total": INPUT_TOTAL_THRESHOLD,
        },
    }


def _session_from_usage(payload, thread_id):
    if not isinstance(payload, dict):
        return None
    sessions = payload.get("sessions") or []
    for row in sessions:
        if str(row.get("id") or "") == thread_id:
            return row
    # 测试夹具也可直接给单个 session 对象。
    if str(payload.get("id") or "") == thread_id:
        return payload
    return None


def load_usage(thread_id, days, fixture=None):
    if fixture:
        row = _session_from_usage(json.loads(Path(fixture).read_text(encoding="utf-8")), thread_id)
        if not row:
            raise ValueError(f"fixture 中找不到 thread_id={thread_id}")
        return row, "fixture"
    usage_bin = Path(os.environ.get("TOKEN_USAGE_BIN", str(DEFAULT_TOKEN_USAGE)))
    proc = subprocess.run(
        ["bash", str(usage_bin), "--session-id", thread_id, "--days", str(days), "--json"],
        capture_output=True, text=True, timeout=120,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"token-usage 失败 rc={proc.returncode}: {proc.stderr[-500:]}")
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"token-usage JSON 不可解析: {exc}") from exc
    row = _session_from_usage(payload, thread_id)
    return (row, "token-usage") if row else (None, "token-usage-empty")


def _session_roots(cli_dir=None):
    if cli_dir:
        return [Path(cli_dir)]
    raw = os.environ.get("MEMORY_GATE_SESSIONS_DIRS", "")
    roots = [Path(p) for p in raw.split(os.pathsep) if p]
    if roots:
        return roots
    home = Path.home()
    return [home / ".codex" / "sessions", home / ".codex" / "archived_sessions"]


def find_rollout(thread_id, cli_dir=None):
    """只检查文件名含目标 thread_id 的 rollout；不打开其他会话文件。"""
    candidates = []
    for root in _session_roots(cli_dir):
        if not root.exists():
            continue
        for path in root.rglob(f"*{thread_id}*.jsonl"):
            try:
                candidates.append((path.stat().st_mtime, path))
            except OSError:
                continue
    for _, path in sorted(candidates, reverse=True):
        try:
            actual_id, _, _ = monitor_dialogs.read_rollout(path)
            # fork 文件名可能含 parent_child；session_meta 的显式 ID 已在 read_rollout 中优先。
            if actual_id == thread_id:
                return path
        except OSError:
            continue
    return sorted(candidates, reverse=True)[0][1] if candidates else None


def read_turns(thread_id, cli_dir=None):
    path = find_rollout(thread_id, cli_dir=cli_dir)
    if not path:
        return None, 0, path
    actual_id, turns, tokens = monitor_dialogs.read_rollout(path)
    if actual_id != thread_id:
        return None, 0, path
    return turns, tokens, path


def metrics_from(usage_row, turns, rollout_tokens):
    row = usage_row or {}
    input_total = int(row.get("input") or 0)
    output_total = int(row.get("output") or 0)
    cumulative = int(row.get("actual_input_plus_output") or (input_total + output_total))
    # 拿不到 token-usage 时，rollout 的最大累计 total_tokens 是唯一可用的本机实测兜底。
    if not row and rollout_tokens:
        cumulative = int(rollout_tokens)
    return {
        "turns": int(turns or 0),
        "cumulative_token": cumulative,
        "request_peak_input": int(row.get("peak_input") or 0),
        "request_peak_cache_input": int(row.get("peak_cache_input") or 0),
        "requests": int(row.get("requests") or 0),
        "input_total": input_total,
        "output_total": output_total,
        "cache_input": int(row.get("cache_input") or 0),
        "first_request_input": int(row.get("first_request_input") or 0),
        "first_request_cache_input": int(row.get("first_request_cache_input") or 0),
        "first_timestamp": int(row.get("first_timestamp") or 0),
        "last_timestamp": int(row.get("last_timestamp") or 0),
    }


def call_state(thread_id, project, agent, metrics, turns_known):
    cmd = [
        sys.executable, str(DEFAULT_STATE), "bump",
        f"active_project={project or 'default'}",
        f"thread_id={thread_id}",
        f"agent={agent}",
        f"token_count={metrics['cumulative_token']}",
        f"request_peak={metrics['request_peak_input']}",
        f"request_count={metrics['requests']}",
        f"input_total={metrics['input_total']}",
    ]
    if turns_known:
        cmd.append(f"turn_count={metrics['turns']}")
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if proc.returncode != 0:
        raise RuntimeError(f"state.py 失败 rc={proc.returncode}: {proc.stderr[-500:]}")
    return json.loads(proc.stdout)


def _parse_kv(argv):
    kv, rest = {}, []
    for item in argv:
        if "=" in item and not item.startswith("--"):
            key, value = item.split("=", 1)
            kv[key] = value
        else:
            rest.append(item)
    return kv, rest


def main():
    kv, rest = _parse_kv(sys.argv[1:])
    ap = argparse.ArgumentParser(description="memory-orchestrator 统一本机闸门")
    ap.add_argument("--thread-id", default=kv.get("thread_id"))
    ap.add_argument("--active-project", default=kv.get("active_project", ""))
    ap.add_argument("--agent", default=kv.get("agent") or os.environ.get("MEMORY_AGENT") or "codex")
    ap.add_argument("--days", type=int, default=3650)
    ap.add_argument("--fixture-usage", default=None)
    ap.add_argument("--fixture-turns", type=int, default=None)
    ap.add_argument("--sessions-dir", default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(rest)

    if not args.thread_id:
        ap.error("thread_id 必填")
    if args.fixture_turns is not None:
        turns, rollout_tokens, rollout_path = args.fixture_turns, 0, None
        turns_known = True
    else:
        turns, rollout_tokens, rollout_path = read_turns(args.thread_id, cli_dir=args.sessions_dir)
        turns_known = turns is not None
    try:
        usage_row, usage_source = load_usage(args.thread_id, args.days, fixture=args.fixture_usage)
    except Exception as exc:
        usage_row, usage_source = None, f"unavailable: {exc}"
    metrics = metrics_from(usage_row, turns, rollout_tokens)
    decision = evaluate_gate(metrics)
    result = {
        "ok": True,
        "dry_run": bool(args.dry_run),
        "thread_id": args.thread_id,
        "active_project": args.active_project,
        "agent": args.agent,
        "usage_source": usage_source,
        "rollout_path": str(rollout_path) if rollout_path else None,
        "metrics": metrics,
        "decision": decision,
    }
    if args.dry_run:
        result["state_written"] = False
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    try:
        state = call_state(args.thread_id, args.active_project, args.agent, metrics, turns_known)
    except Exception as exc:
        result.update({"ok": False, "state_written": False, "error": str(exc)})
        print(json.dumps(result, ensure_ascii=False, indent=2))
        raise SystemExit(2)
    result["state_written"] = True
    result["state"] = state
    # 兼容旧 agent_hook 调用方：把 state 的核心字段同时放到顶层。
    for key in ("agent", "thread_id", "active_project", "turn_count", "token_count",
                "warned", "forced", "already_forced", "message", "gate_reasons"):
        if key in state:
            result[key] = state[key]
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
