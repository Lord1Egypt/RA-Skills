#!/usr/bin/env python3
"""Run a fixed eval suite from JSON and record results.

python3 eval_suite.py --tasks state/evals/tasks.json

Each task: {id, name, kind: file_exists|command, path|cmd, expect_contains?, timeout?}
Results: state/evals/last-run.json (+ a trace row when TRACE_DB is available).
"""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_task(t):
    t0 = time.time()
    if t["kind"] == "file_exists":
        p = os.path.expanduser(t["path"])
        ok = os.path.exists(p)
        out = p if ok else "missing: " + p
    else:
        p = subprocess.run(t["cmd"], shell=True, text=True, capture_output=True,
                           timeout=t.get("timeout", 20), cwd=t.get("cwd"))
        out = (p.stdout or "") + (p.stderr or "")
        ok = p.returncode == 0
        if ok and t.get("expect_contains"):
            ok = t["expect_contains"] in out
        if ok and t.get("expect_not_contains"):
            ok = t["expect_not_contains"] not in out
    return ok, out.strip()[:400], int((time.time() - t0) * 1000)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", default="state/evals/tasks.json")
    ap.add_argument("--out", default="state/evals/last-run.json")
    a = ap.parse_args()

    tasks = json.load(open(a.tasks, encoding="utf-8"))
    results = []
    for t in tasks:
        try:
            ok, out, ms = run_task(t)
        except Exception as e:
            ok, out, ms = False, "EXC: " + str(e), 0
        results.append({"id": t["id"], "name": t.get("name", ""), "ok": ok, "output": out, "duration_ms": ms})

    passed = sum(1 for r in results if r["ok"])
    payload = {
        "run_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "total": len(results), "passed": passed,
        "failed": [r["id"] for r in results if not r["ok"]],
        "results": results,
    }
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    json.dump(payload, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    try:
        import trace_store
        try:
            trace_store.add(type("A", (), {
                "task_id": "eval-" + payload["run_at"], "type": "eval", "source": "eval_suite",
                "started_at": payload["run_at"], "duration_ms": sum(r["duration_ms"] for r in results),
                "tools": ["eval_suite"], "retries": 0, "tokens_in": 0, "tokens_out": 0,
                "outcome": "success" if passed == len(results) else "failure",
                "error_class": "" if passed == len(results) else "assert",
                "artifact": a.tasks, "notes": "%d/%d" % (passed, len(results)),
                "constraint_fail": 0,
            })())
        except Exception:
            pass
    except Exception:
        pass

    print(json.dumps({"total": len(results), "passed": passed, "failed": payload["failed"], "out": a.out}))
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
