#!/usr/bin/env python3
"""Behavior audit over a JSONL event log.

Event fields (one JSON object per line):
  ts            ISO-8601 string or epoch milliseconds (required)
  session       string (required)
  tool          string (optional; absent = no tool call)
  ok            boolean (optional, default true)
  duration_ms   number (optional)
  checkpoint    boolean (optional) — a progress/acknowledgement event
  outcome       "ok" | "error" (optional)
  user_visible  boolean (optional) — did the user see a message
  claims        boolean (optional) — did this task assert facts

Checks are predicates over task segments, never over intent.
"""
import json, sys
from datetime import datetime

GAP_S = 1800          # task segmentation gap
LONG_TASK_MS = 300000  # 5 minutes
RETRY_N = 3


def ts_of(e):
    v = e.get("ts")
    if isinstance(v, (int, float)):
        return float(v) / 1000.0
    return datetime.fromisoformat(str(v).replace("Z", "+00:00")).timestamp()


def load(path):
    ev = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                ev.append(json.loads(line))
    for e in ev:
        e["_ts"] = ts_of(e)
    return sorted(ev, key=lambda x: (x.get("session", ""), x["_ts"]))


def segment(ev):
    tasks, cur = [], []
    for e in ev:
        if cur and (e.get("session") != cur[-1].get("session") or e["_ts"] - cur[-1]["_ts"] > GAP_S):
            tasks.append(cur)
            cur = []
        cur.append(e)
    if cur:
        tasks.append(cur)
    return tasks


def summarize(t):
    tools = [e for e in t if e.get("tool")]
    return {
        "session": t[0].get("session"),
        "start": t[0]["_ts"],
        "duration_ms": int((t[-1]["_ts"] - t[0]["_ts"]) * 1000),
        "tool_calls": len(tools),
        "has_checkpoint": any(e.get("checkpoint") for e in t),
        "has_error": any(e.get("outcome") == "error" or e.get("ok") is False for e in t),
        "user_visible": any(e.get("user_visible") for e in t),
        "claims": any(e.get("claims") for e in t),
        "events": t,
    }


def retry_storm(summary):
    t = summary["events"]
    run, prev = 0, None
    for e in t:
        if not e.get("tool"):
            continue
        bad = e.get("ok") is False or e.get("outcome") == "error"
        if bad and e["tool"] == prev:
            run += 1
            if run >= RETRY_N - 1:
                return True
        else:
            run = 0
        prev = e["tool"]
    return False


def main(path):
    ev = load(path)
    tasks = [summarize(t) for t in segment(ev)]
    checks = {}

    def add(name, pred, base_filter=lambda s: True):
        base = [s for s in tasks if base_filter(s)]
        hits = [s for s in base if pred(s)]
        checks[name] = {
            "hits": len(hits),
            "base": len(base),
            "rate": round(len(hits) / len(base), 3) if base else None,
            "samples": [{"session": s["session"], "start": s["start"]} for s in hits[:3]],
        }

    add("long_task_without_checkpoint", lambda s: s["duration_ms"] > LONG_TASK_MS and not s["has_checkpoint"])
    add("retry_storm", retry_storm, lambda s: s["tool_calls"] > 0)
    add("silent_failure", lambda s: s["has_error"] and not s["user_visible"], lambda s: s["has_error"])
    add("claims_without_tools", lambda s: s["claims"] and s["tool_calls"] == 0, lambda s: s["claims"])

    out = {
        "window": {
            "from": min((e["_ts"] for e in ev), default=None),
            "to": max((e["_ts"] for e in ev), default=None),
            "events": len(ev),
            "tasks": len(tasks),
        },
        "thresholds": {"gap_s": GAP_S, "long_task_ms": LONG_TASK_MS, "retry_n": RETRY_N},
        "checks": checks,
        "note": "Segmentation and thresholds are judgement calls. Calibrate on a period with a known answer before trusting rates.",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: audit_events.py <events.jsonl>")
        raise SystemExit(2)
    main(sys.argv[1])
