#!/usr/bin/env python3
"""Run all catalog effects with max parallelism and preserve raw records."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = Path(__file__).resolve().parent
REPORTS_DIR = ROOT / "reports"
RAW_DIR = REPORTS_DIR / "catalog-effects-raw"
MAX_WORKERS = 3
TIMEOUT_SECONDS = 1200
INPUT_URL = (
    "https://object.pixocial.com/aibiz/BeautyPlusTemp/20260414170437/"
    "BFF9D46240B340CB93F03603F2A042B3/demo.jpg"
)

TASKS = [
    "breast_natural_strong",
    "breast_natural_medium",
    "breast_natural_weak",
    "teardrop_breast_strong",
    "teardrop_breast_medium",
    "teardrop_breast_weak",
    "breast_round_strong",
    "breast_round_medium",
    "breast_round_weak",
    "breast_outward_strong",
    "breast_outward_medium",
    "breast_outward_weak",
    "butt_peach_strong",
    "butt_peach_medium",
    "butt_peach_weak",
    "butt_o_shape_strong",
    "butt_o_shape_medium",
    "butt_o_shape_weak",
    "hair_black",
    "hair_blonde",
    "hair_brown_highlights",
    "hair_platinum",
    "hair_silver_platinum",
    "hair_teddy_brown",
    "hair_glossy",
    "hair_high_layer",
    "hair_soft_waves",
    "hair_latino_curls",
    "dress_yellow_gown",
    "dress_arctic_allure",
    "dress_ostrich_feather",
    "dress_muse_goddess",
    "suit_tartan_eve",
    "suit_red_carpet",
    "accessory_bunny_ear",
    "dress_butter_moonlight",
    "dress_pink_puffy",
    "dress_gold_hoodie",
    "dress_lace_corset",
    "dress_chiffon_cake",
    "dress_sheer_bikini",
    "cosplay_carnival",
    "cosplay_bunny_cop",
    "cosplay_fox_boyfriend",
    "cosplay_deer_girl",
    "cosplay_grinch",
    "photo_restoration_v3",
    "ai_ultra_hd_v3",
]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_env_file() -> None:
    """Apply scripts/.env into this process (and child subprocesses).

    Keys present in the file always override existing os.environ values so
    credential changes in .env take effect without restarting the shell.
    """
    env_file = SCRIPTS_DIR / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        key, val = s.split("=", 1)
        key = key.strip()
        val = val.strip().strip("\"'")
        if key:
            os.environ[key] = val


def _parse_stdout_json(stdout: str) -> dict[str, Any] | None:
    text = (stdout or "").strip()
    if not text.startswith("{"):
        return None
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def _effective_ok(parsed: dict[str, Any] | None, exit_code: int, timed_out: bool) -> tuple[bool, list[str]]:
    """
    Stricter than CLI exit code: some jobs exit 0 with skill_status=completed
    but API code != 0 and no output URLs (e.g. IMAGE_DECODE_ERROR).
    """
    reasons: list[str] = []
    if timed_out:
        return False, ["timed_out"]
    if exit_code != 0:
        return False, [f"exit_code_{exit_code}"]
    if not parsed:
        return False, ["no_stdout_json"]
    if parsed.get("skill_status") != "completed":
        return False, [f"skill_status_{parsed.get('skill_status')!r}"]
    code = parsed.get("code")
    errc = parsed.get("error_code")
    if code not in (None, 0) or errc not in (None, 0):
        msg = parsed.get("message") or parsed.get("error") or ""
        reasons.append(f"api_code={code!r} error_code={errc!r} message={msg!r}")
        return False, reasons
    ours = parsed.get("output_urls")
    primary = parsed.get("primary_result_url")
    primary_s = primary.strip() if isinstance(primary, str) else ""
    if isinstance(ours, list) and len(ours) == 0 and not primary_s:
        return False, ["no_output_urls_and_no_primary_result_url"]
    return True, []


def _run_one(task: str) -> dict[str, Any]:
    start_ts = time.time()
    start_iso = _now_iso()
    cmd = [
        sys.executable,
        str(SCRIPTS_DIR / "beautyplus_ai.py"),
        "run-task",
        "--task",
        task,
        "--input",
        INPUT_URL,
    ]
    timed_out = False
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(SCRIPTS_DIR),
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
        exit_code = proc.returncode
        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
    except subprocess.TimeoutExpired as ex:
        timed_out = True
        exit_code = -1
        stdout = ex.stdout or ""
        stderr = (ex.stderr or "") + f"\nTIMEOUT after {TIMEOUT_SECONDS}s"
    end_ts = time.time()
    end_iso = _now_iso()
    elapsed_ms = int((end_ts - start_ts) * 1000)
    parsed = _parse_stdout_json(stdout)
    skill_status = parsed.get("skill_status") if parsed else None
    ok, ok_reasons = _effective_ok(parsed, exit_code, timed_out)
    task_id = parsed.get("task_id") if parsed else None

    raw_file = RAW_DIR / f"{task}.json"
    raw_payload = {
        "task": task,
        "started_at": start_iso,
        "ended_at": end_iso,
        "elapsed_ms": elapsed_ms,
        "command": cmd,
        "exit_code": exit_code,
        "timed_out": timed_out,
        "stdout": stdout,
        "stderr": stderr,
        "parsed_json": parsed,
        "skill_status": skill_status,
        "task_id": task_id,
        "ok": ok,
        "ok_reasons": ok_reasons,
    }
    raw_file.write_text(
        json.dumps(raw_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return {
        "task": task,
        "ok": ok,
        "exit_code": exit_code,
        "skill_status": skill_status,
        "timed_out": timed_out,
        "task_id": task_id,
        "elapsed_ms": elapsed_ms,
        "raw_record": str(raw_file.relative_to(ROOT)),
        "ok_reasons": ok_reasons,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--only",
        default="",
        help="Comma-separated effect KEYs to run (default: full catalog)",
    )
    ap.add_argument(
        "--summary-out",
        default="",
        help="Path for summary JSON (default: audit or retry path under reports/)",
    )
    args = ap.parse_args()

    _load_env_file()
    if not os.environ.get("BP_AK") or not os.environ.get("BP_SK"):
        print("BP_AK/BP_SK missing; set env or scripts/.env", file=sys.stderr)
        return 2

    if args.only.strip():
        tasks = [x.strip() for x in args.only.split(",") if x.strip()]
        unknown = [t for t in tasks if t not in TASKS]
        if unknown:
            print(f"Unknown --only task(s): {unknown}", file=sys.stderr)
            return 2
        summary_path = (
            Path(args.summary_out).expanduser()
            if args.summary_out.strip()
            else REPORTS_DIR / "catalog-effects-retry-summary.json"
        )
    else:
        tasks = list(TASKS)
        summary_path = (
            Path(args.summary_out).expanduser()
            if args.summary_out.strip()
            else REPORTS_DIR / "catalog-effects-audit-summary.json"
        )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    run_started = _now_iso()
    wall_start = time.time()

    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futs = {pool.submit(_run_one, t): t for t in tasks}
        for fut in as_completed(futs):
            results.append(fut.result())

    order = {name: i for i, name in enumerate(tasks)}
    results.sort(key=lambda x: order[x["task"]])

    passed = sum(1 for r in results if r["ok"])
    failed = len(results) - passed
    wall_ms = int((time.time() - wall_start) * 1000)
    run_ended = _now_iso()

    summary = {
        "meta": {
            "title": "BeautyPlus AI catalog effects audited batch test",
            "started_at": run_started,
            "ended_at": run_ended,
            "parallel_max": MAX_WORKERS,
            "input_url": INPUT_URL,
            "total": len(tasks),
            "passed": passed,
            "failed": failed,
            "wall_clock_ms": wall_ms,
            "pass_criteria": (
                "exit_code==0 and not timed_out and skill_status==completed "
                "and code/error_code in {0,None} and (output_urls non-empty or primary_result_url)"
            ),
            "raw_dir": str(RAW_DIR.relative_to(ROOT)),
            "tasks_subset": tasks if len(tasks) != len(TASKS) else None,
        },
        "results": results,
    }

    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {"summary": str(summary_path), "passed": passed, "failed": failed},
            ensure_ascii=False,
        )
    )
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
