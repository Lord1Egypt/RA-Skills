#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""agent-slim 自测：七块对账、gate 正反例、状态机 check/DRIFT、看板求和、token 观测。

全部 PASS 退出 0；任一 FAIL 退出 1。只读真实文件；测试产物写临时目录。
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SCRIPTS = BASE / "scripts"
BASELINE = BASE / "references" / "baseline-20261109.json"
MEASURE = SCRIPTS / "measure_prompt.py"
STATE = SCRIPTS / "injection_state.py"
DASH = SCRIPTS / "budget_dashboard.py"
TOKEN = SCRIPTS / "token_experiment.py"

RESULTS: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f"  {detail}" if detail else ""))


def run(cmd: list[str], timeout: int = 180) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)


def load_json(text: str) -> dict:
    return json.loads(text.lstrip("\ufeff"))


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="agent-slim-selftest-"))
    measure_json = tmp / "measure.json"

    # 1 七块对账 + 文本块闸门
    proc = run([sys.executable, str(MEASURE), "--json", "--baseline", str(BASELINE)])
    if proc.returncode not in (0, 1):
        record("measure 对账", False, f"rc={proc.returncode} stderr={proc.stderr.strip()[:200]}")
        m = {}
    else:
        m = load_json(proc.stdout)
        ids = [b.get("id") for b in m.get("blocks", [])]
        expected_ids = ["memory", "base", "skills", "permissions", "AGENTS", "mcp", "env"]
        rows_sum = sum(int(b["bytes"]) for b in m.get("blocks", []))
        text_total = int(m.get("text_blocks_total", m["total"] - 3900))
        mcp_bytes = next((int(b["bytes"]) for b in m["blocks"] if b["id"] == "mcp"), 0)
        ok = (
            m.get("reconciliation") == "PASS"
            and ids == expected_ids
            and rows_sum == int(m["total"])
            and text_total == int(m["total"]) - mcp_bytes
            and m.get("overall_status") == "UNMEASURED"
        )
        record(
            "measure 对账",
            ok,
            f"total={m.get('total')} text={text_total} gate={m.get('gate_status')} overall={m.get('overall_status')}",
        )
        measure_json.write_text(proc.stdout, encoding="utf-8")

    if m:
        text_total = int(m.get("text_blocks_total", int(m["total"]) - 3900))
        # 2 gate 正反例：闸门只对文本块生效，用动态闸门隔离 pass/fail 逻辑
        pos_gate = text_total + 1024
        proc_pos = run([sys.executable, str(MEASURE), "--json", "--gate", str(pos_gate)])
        pos_ok = proc_pos.returncode == 0 and load_json(proc_pos.stdout).get("gate_status") == "PASS"
        record("gate 正例", pos_ok, f"gate={pos_gate} rc={proc_pos.returncode}")

        neg_gate = max(1024, text_total - 1024)
        proc_neg = run([sys.executable, str(MEASURE), "--json", "--gate", str(neg_gate)])
        neg_ok = proc_neg.returncode == 1 and load_json(proc_neg.stdout).get("gate_status") == "FAIL"
        record("gate 反例", neg_ok, f"gate={neg_gate} rc={proc_neg.returncode}")

        # 3 真实闸门如实记录（不要求 PASS，但必须与数字一致）
        actual_gate = int(m.get("gate_bytes", 57344))
        expected = "PASS" if int(m.get("text_blocks_total", 0)) <= actual_gate else "FAIL"
        record(
            "真实文本块闸门一致",
            m.get("gate_status") == expected,
            f"{m.get('text_blocks_total')}/{actual_gate} -> {m.get('gate_status')}",
        )
    else:
        record("gate 正例", False, "measure 未产出 JSON")
        record("gate 反例", False, "measure 未产出 JSON")
        record("真实文本块闸门一致", False, "measure 未产出 JSON")

    # 4 状态机真实 check（只读）+ 副本 DRIFT
    proc_check = run([sys.executable, str(STATE), "--check", "--json"])
    check_data = {}
    try:
        check_data = load_json(proc_check.stdout)
    except Exception:
        pass
    real_ok = (
        proc_check.returncode == 0
        and check_data.get("overall") == "OK"
        and (check_data.get("injection") or {}).get("overall_status") == "UNMEASURED"
        and ((check_data.get("injection") or {}).get("blocks", {}).get("mcp") or {}).get("status") == "UNKNOWN"
    )
    record(
        "状态机真实 check",
        real_ok,
        f"rc={proc_check.returncode} overall={check_data.get('overall')} "
        f"injection={check_data.get('injection_status')}",
    )

    drift_ok = False
    drift_detail = "状态文件缺失"
    try:
        state_path = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "memory" / "injection-state.json"
        if state_path.exists():
            copy = tmp / "state-copy.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state.setdefault("files", {}).setdefault("memory", {})["sha256"] = "0" * 64
            copy.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            proc_drift = run([sys.executable, str(STATE), "--check", "--state", str(copy), "--json"])
            d = load_json(proc_drift.stdout)
            drift_ok = (
                proc_drift.returncode == 1
                and d.get("overall") == "FAIL"
                and d.get("files", {}).get("memory", {}).get("status") == "DRIFT"
            )
            drift_detail = (
                f"rc={proc_drift.returncode} memory={d.get('files', {}).get('memory', {}).get('status')} "
                f"overall={d.get('overall')}"
            )
    except Exception as exc:  # noqa: BLE001
        drift_detail = f"{type(exc).__name__}: {exc}"
    record("状态机副本 DRIFT", drift_ok, drift_detail)

    # 5 看板求和 + 口径一致性
    dash_json = tmp / "dashboard.json"
    proc_dash = run([
        sys.executable, str(DASH), "--no-measure",
        "--out", str(tmp / "dashboard.md"), "--json-out", str(dash_json),
    ])
    dash_ok = False
    dash_detail = f"rc={proc_dash.returncode}"
    try:
        dp = load_json(dash_json.read_text(encoding="utf-8"))
        a = dp["assertions"]
        rows_sum = sum(int(r["bytes"]) for r in dp["rows"] if r["id"] != "total")
        total = next(int(r["bytes"]) for r in dp["rows"] if r["id"] == "total")
        dash_ok = (
            proc_dash.returncode == 0
            and a.get("sum_matches") is True
            and rows_sum == total
            and a.get("overall_upper_total") == a.get("text_blocks_total") + 2400 + 12400
            and a.get("overall_app_injection_status") == "UNMEASURED"
        )
        dash_detail += f" sum={rows_sum}/{total} text={a.get('text_blocks_total')} upper={a.get('overall_upper_total')}"
    except Exception as exc:  # noqa: BLE001
        dash_detail += f" {type(exc).__name__}: {exc}"
    record("看板求和与口径", dash_ok, dash_detail)

    # 5b 用实测 JSON 再看板，确认“求和 PASS 但与 s1 有差异”不误报失败
    if measure_json.exists():
        proc_dash2 = run([
            sys.executable, str(DASH), "--measure-json", str(measure_json),
            "--out", str(tmp / "dashboard2.md"), "--json-out", str(tmp / "dashboard2.json"),
        ])
        try:
            dp2 = load_json((tmp / "dashboard2.json").read_text(encoding="utf-8"))
            a2 = dp2["assertions"]
            dash2_ok = (
                proc_dash2.returncode == 0
                and a2.get("sum_matches") is True
                and a2.get("overall_app_injection_status") == "UNMEASURED"
            )
            record("看板实测 JSON", dash2_ok, f"rc={proc_dash2.returncode} text={a2.get('text_blocks_total')} upper={a2.get('overall_upper_total')}")
        except Exception as exc:  # noqa: BLE001
            record("看板实测 JSON", False, f"rc={proc_dash2.returncode} {type(exc).__name__}: {exc}")

    # 6 token 观测（合成样本，验证中位数/均值/过滤/样本不足）
    base_day = 1762617600  # 2026-11-08 00:00 CST 附近，具体值不影响过滤测试
    # 直接用 2026-11-08 / 11-13 的时间戳，避免依赖手算
    from datetime import datetime
    try:
        from zoneinfo import ZoneInfo
        tz = ZoneInfo("Asia/Shanghai")
    except Exception:
        tz = None
    def ts(day: str) -> int:
        return int(datetime.strptime(day, "%Y-%m-%d").replace(tzinfo=tz).timestamp())

    fake = {"days": 30, "sessions": []}
    for i, val in enumerate([10000, 11000, 12000, 13000, 14000, 15000], 1):
        fake["sessions"].append({
            "id": f"base{i}", "providers": ["直连/test-model"], "requests": 2,
            "first_request_input": val, "first_timestamp": ts("2026-11-08") + i,
            "cwd": "/tmp/demo-project", "peak_input": val,
        })
    for i, val in enumerate([9000, 9500, 10000, 10500, 11000, 11500], 7):
        fake["sessions"].append({
            "id": f"after{i}", "providers": ["直连/test-model"], "requests": 2,
            "first_request_input": val, "first_timestamp": ts("2026-11-13") + i,
            "cwd": "/tmp/demo-project", "peak_input": val,
        })
    fake_path = tmp / "token-fake.json"
    fake_path.write_text(json.dumps(fake), encoding="utf-8")
    proc_tok = run([
        sys.executable, str(TOKEN), "--input-json", str(fake_path), "--start", "2026-11-01",
        "--project", "demo-project", "--baseline-start", "2026-11-08", "--baseline-end", "2026-11-08",
        "--after-start", "2026-11-13", "--min-samples", "5", "--json",
    ])
    try:
        tp = load_json(proc_tok.stdout)
        g = tp["groups"]
        tok_ok = (
            proc_tok.returncode == 0
            and tp.get("billing_claim") is False
            and g["baseline"]["sample_count"] == 6
            and g["after"]["sample_count"] == 6
            and g["baseline"]["median_first_request_input"] == 12500
            and g["after"]["mean_first_request_input"] == 10250
            and tp.get("status") == "OBSERVATION_ONLY"
        )
        record(
            "token 观测与过滤",
            tok_ok,
            f"base_n={g['baseline']['sample_count']} after_n={g['after']['sample_count']} "
            f"median={g['baseline']['median_first_request_input']} delta={tp.get('observed_delta_pct'):.2f}%",
        )
    except Exception as exc:  # noqa: BLE001
        record("token 观测与过滤", False, f"rc={proc_tok.returncode} {type(exc).__name__}: {exc}")

    # 7 样本不足必须明说
    fake_small = {"days": 30, "sessions": fake["sessions"][:2]}
    small_path = tmp / "token-small.json"
    small_path.write_text(json.dumps(fake_small), encoding="utf-8")
    proc_small = run([
        sys.executable, str(TOKEN), "--input-json", str(small_path), "--start", "2026-11-01",
        "--baseline-start", "2026-11-08", "--baseline-end", "2026-11-08",
        "--after-start", "2026-11-13", "--min-samples", "5", "--json",
    ])
    try:
        sp = load_json(proc_small.stdout)
        small_ok = (
            proc_small.returncode == 0
            and sp.get("status") == "INSUFFICIENT_SAMPLES"
            and sp.get("observed_delta_pct") is None
            and "样本不足" in sp.get("conclusion", "")
        )
        record("样本不足不报节省", small_ok, sp.get("conclusion", "")[:80])
    except Exception as exc:  # noqa: BLE001
        record("样本不足不报节省", False, f"rc={proc_small.returncode} {type(exc).__name__}: {exc}")

    failed = [r for r in RESULTS if not r[1]]
    print("")
    print(f"SUMMARY: {len(RESULTS) - len(failed)}/{len(RESULTS)} PASS")
    if failed:
        print("FAILED: " + ", ".join(r[0] for r in failed))
        return 1
    print("ALL PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
