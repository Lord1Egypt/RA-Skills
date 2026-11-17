#!/usr/bin/env python3
"""Run a guard test matrix against a classifier without executing the commands.

Usage:
    matrix_run.py --classifier ./classifier.sh --matrix cases.json

Classifier contract: receives the command as argv, prints "allow" or "deny",
exits 0. This runner never executes the case command itself.
"""
import argparse
import json
import subprocess
import sys


def run_case(classifier, case):
    argv = [classifier] + [str(x) for x in case["cmd"]]
    p = subprocess.run(argv, capture_output=True, text=True, timeout=20)
    out = (p.stdout or "").strip().splitlines()
    decision = out[0].strip().lower() if out else ""
    return decision, p.returncode, (p.stderr or "").strip()[:200]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--classifier", required=True)
    ap.add_argument("--matrix", required=True)
    a = ap.parse_args()

    data = json.load(open(a.matrix, encoding="utf-8"))
    cases = data["cases"]
    results, failures = [], 0
    for c in cases:
        decision, rc, err = run_case(a.classifier, c)
        ok = decision == c["expect"].lower() and rc == 0
        if not ok:
            failures += 1
        results.append({
            "id": c.get("id"),
            "cmd": c["cmd"],
            "expect": c["expect"],
            "actual": decision or "(no output)",
            "exit": rc,
            "ok": ok,
            "stderr": err,
            "class": c.get("class", "unspecified"),
        })

    by_class = {}
    for r in results:
        s = by_class.setdefault(r["class"], {"total": 0, "ok": 0})
        s["total"] += 1
        s["ok"] += 1 if r["ok"] else 0

    print(json.dumps({
        "classifier": a.classifier,
        "cases": len(results),
        "failures": failures,
        "by_class": by_class,
        "results": results,
        "note": "Classification only. No case command was executed.",
    }, ensure_ascii=False, indent=2))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
