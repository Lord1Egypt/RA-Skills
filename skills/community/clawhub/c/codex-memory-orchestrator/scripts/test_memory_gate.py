#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""memory_gate 自测：五条件、JSON、dry-run、幂等、精确轮数、无关会话隔离。"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import memory_gate  # noqa: E402
import monitor_dialogs  # noqa: E402

PY = sys.executable
THREAD = "11111111-2222-4333-8444-555555555555"
FIXTURE = {
    "sessions": [{
        "id": THREAD,
        "providers": ["fixture"],
        "requests": 1,
        "input": 1,
        "output": 1,
        "cache_input": 0,
        "peak_input": 1,
        "peak_cache_input": 0,
        "first_request_input": 1,
        "first_request_cache_input": 0,
        "first_timestamp": 1,
        "last_timestamp": 1,
        "actual_input_plus_output": 2,
        "over_gate": False,
        "gate_reasons": [],
    }]
}


def base_metrics(**overrides):
    data = {
        "turns": 1,
        "cumulative_token": 1000,
        "request_peak_input": 1000,
        "requests": 1,
        "input_total": 1000,
    }
    data.update(overrides)
    return data


def assert_only(reason, metrics):
    decision = memory_gate.evaluate_gate(metrics)
    assert decision["trigger"] is True, decision
    assert decision["reasons"] == [reason], decision


def main():
    checks = []
    # 五个硬条件各用固定样例触发一次；基线不触发。
    assert memory_gate.evaluate_gate(base_metrics())["trigger"] is False
    assert_only("turns", base_metrics(turns=8))
    assert_only("tokens", base_metrics(cumulative_token=150000))
    assert_only("request_peak", base_metrics(request_peak_input=100000))
    assert_only("requests", base_metrics(requests=120))
    assert_only("input_total", base_metrics(input_total=8000000))
    checks.append("five_conditions")

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        state = root / "state.json"
        fixture = root / "usage.json"
        fixture.write_text(json.dumps(FIXTURE, ensure_ascii=False), encoding="utf-8")
        env = dict(os.environ, CODEX_MEMORY_STATE=str(state), MEMORY_AGENT="codex")
        before = sorted(p.name for p in root.iterdir())
        dry = subprocess.run([
            PY, str(HERE / "memory_gate.py"), "--thread-id", THREAD,
            "--active-project", "fixture", "--fixture-usage", str(fixture),
            "--fixture-turns", "1", "--dry-run", "--json",
        ], capture_output=True, text=True, env=env, timeout=30)
        assert dry.returncode == 0, dry.stderr
        dry_obj = json.loads(dry.stdout)
        assert dry_obj["dry_run"] is True and dry_obj["state_written"] is False
        assert not state.exists(), "dry-run 不得写 state"
        assert sorted(p.name for p in root.iterdir()) == before
        checks.append("dry_run_no_write_json")

        # 把固定样例改成只触发单请求峰值，再真实写入；重复运行必须不重复提醒。
        trig = json.loads(json.dumps(FIXTURE))
        trig["sessions"][0]["peak_input"] = 100000
        fixture.write_text(json.dumps(trig, ensure_ascii=False), encoding="utf-8")
        cmd = [
            PY, str(HERE / "memory_gate.py"), "--thread-id", THREAD,
            "--active-project", "fixture", "--fixture-usage", str(fixture),
            "--fixture-turns", "1", "--json",
        ]
        first = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=30)
        assert first.returncode == 0, first.stderr
        first_obj = json.loads(first.stdout)
        assert first_obj["state"]["forced"] is True, first_obj
        assert "恢复包" in first_obj["state"]["message"], first_obj
        second = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=30)
        assert second.returncode == 0, second.stderr
        second_obj = json.loads(second.stdout)
        assert second_obj["state"]["already_forced"] is True
        assert second_obj["state"]["message"] == ""
        saved = json.loads(state.read_text(encoding="utf-8"))
        dialogs = [v for v in saved["dialogs"].values() if v.get("thread_id") == THREAD]
        assert len(dialogs) == 1, dialogs
        assert dialogs[0]["turn_count"] == 1, dialogs[0]
        checks.append("idempotent_exact_turns")

        # 只读取文件名包含目标 thread_id 的 rollout，无关文件即使损坏也不能被打开。
        sessions = root / "sessions"
        sessions.mkdir()
        target = sessions / f"rollout-2026-01-01T00-00-00-{THREAD}.jsonl"
        target.write_text("\n".join([
            json.dumps({"type": "session_meta", "payload": {"session_id": THREAD}}),
            json.dumps({"type": "response_item", "payload": {"type": "message", "role": "user", "id": "u1"}}),
            json.dumps({"type": "response_item", "payload": {"type": "message", "role": "user", "id": "u1"}}),
            json.dumps({"type": "response_item", "payload": {"type": "message", "role": "developer", "id": "d1"}}),
            json.dumps({"type": "response_item", "payload": {"type": "message", "role": "user", "id": "u2"}}),
        ]) + "\n", encoding="utf-8")
        (sessions / "rollout-2026-01-01T00-00-00-99999999-2222-4333-8444-555555555555.jsonl").write_text(
            "NOT JSON\n", encoding="utf-8")
        found = memory_gate.find_rollout(THREAD, cli_dir=str(sessions))
        assert found == target, (found, target)
        tid, turns, _ = monitor_dialogs.read_rollout(target)
        assert tid == THREAD and turns == 2, (tid, turns)
        checks.append("no_unrelated_rollout_read_modern_turns")

    source = (HERE / "memory_gate.py").read_text(encoding="utf-8")
    for forbidden in ("import requests", "import urllib", "http://", "https://"):
        assert forbidden not in source, forbidden
    checks.append("local_only")

    print("PASS memory-gate checks=" + ",".join(checks))
    print(json.dumps({"ok": True, "checks": checks, "count": len(checks)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
