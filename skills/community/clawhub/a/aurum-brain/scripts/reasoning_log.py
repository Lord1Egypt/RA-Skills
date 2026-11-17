#!/usr/bin/env python3
"""aurum-brain: structured reasoning / self-check logger.

Usage:
    python3 reasoning_log.py --task "fix login bug" --plan "A->B->C"
    python3 reasoning_log.py --self-check "answer covers question? no contradiction?"

Reads nothing from the network and writes nothing except a local log line.
Helps operationalize the aurum-brain loop (understand -> plan -> act -> verify ->
correct -> finish) and the self-correction / anti-repetition gates.

The log is written next to this script as reasoning_log.jsonl (one JSON object
per line). Set REASONING_LOG_PATH to override. No secrets are ever written.
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

DEFAULT_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reasoning_log.jsonl")


def _now():
    return datetime.now(timezone.utc).isoformat()


def log_entry(kind, payload, log_path):
    record = {"ts": _now(), "skill": "aurum-brain", "kind": kind, "payload": payload}
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError as e:
        print(f"[reasoning_log] WARNING could not write log: {e}", file=sys.stderr)
    return record


def cmd_task(args):
    rec = log_entry("task", {"task": args.task, "plan": args.plan}, args.log)
    print(f"[task logged] {rec['ts']}")
    if args.plan:
        print("Plan steps:")
        for i, step in enumerate([s.strip() for s in args.plan.split("->")], 1):
            print(f"  {i}. {step}")


def cmd_check(args):
    """Record a yes/no self-check item and report an overall verdict."""
    items = [s.strip() for s in args.self_check.split(";") if s.strip()]
    results = []
    for it in items:
        low = it.lower()
        # crude classification: if the item ends with a "?" and a negative word, flag it
        negative = any(w in low for w in ["no ", "not ", "fail", "missing", "contradiction"])
        passed = not negative
        results.append({"check": it, "passed": passed})
    rec = log_entry("self_check", {"checks": results}, args.log)
    failed = [r for r in results if not r["passed"]]
    verdict = "PASS - safe to send" if not failed else f"FAIL - {len(failed)} issue(s), fix before sending"
    print(f"[self-check] {verdict}")
    for r in results:
        mark = "OK " if r["passed"] else "XX "
        print(f"  {mark}{r['check']}")
    # exit non-zero on failure so it can gate a pipeline
    return 1 if failed else 0


def main(argv=None):
    p = argparse.ArgumentParser(description="aurum-brain reasoning logger")
    p.add_argument("--log", default=os.environ.get("REASONING_LOG_PATH", DEFAULT_LOG),
                   help="path to jsonl log file")
    sub = p.add_subparsers(dest="cmd", required=True)

    pt = sub.add_parser("task", help="log a task + plan")
    pt.add_argument("--task", required=True)
    pt.add_argument("--plan", help="steps separated by ->")
    pt.set_defaults(func=cmd_task)

    pc = sub.add_parser("self-check", help="record self-correction checks")
    pc.add_argument("--self-check", required=True, help="checks separated by ; (use 'no'/'fail' to flag)")
    pc.set_defaults(func=cmd_check)

    args = p.parse_args(argv)
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
