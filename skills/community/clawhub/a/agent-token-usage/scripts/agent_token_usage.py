#!/usr/bin/env python3
"""Aggregate per-agent token usage for one day from OpenClaw session JSONL files.

Usage:
  agent_token_usage.py                # today (UTC by default, matches pew)
  agent_token_usage.py --date 2026-05-20
  agent_token_usage.py --date 2026-05-20 --tz local
  agent_token_usage.py --date 2026-05-20 --agents-dir ~/.openclaw/agents
  agent_token_usage.py --date 2026-05-20 --format json
  agent_token_usage.py --date 2026-05-20 --billable

Source of truth:
  ~/.openclaw/agents/<agent>/sessions/<sessionId>.jsonl

  Each LLM call appears as exactly one record:
    {"type":"message","timestamp":"...Z","message":{"role":"assistant",
     "model":"...","usage":{"input","output","cacheRead","cacheWrite",...}}}

  We deliberately DO NOT read *.trajectory.jsonl. Trajectory files emit several
  events per LLM call (prompt.submitted / context.compiled / model.completed /
  trace.artifacts ...), each carrying the SAME usage snapshot, which causes
  ~2.6× over-counting if naively summed.

Token field semantics:
  input       - new prompt tokens (not cached)
  output      - generated tokens
  cacheRead   - prompt tokens served from prompt cache (~10% of normal price)
  cacheWrite  - prompt tokens written to cache (~125% of normal price)

Billable-equivalent (approx, Anthropic/OpenAI ballpark):
  billable = input + output + cacheRead * 0.1 + cacheWrite * 1.25
"""
from __future__ import annotations
import argparse, json, os, sys, glob
from collections import defaultdict
from datetime import datetime, date, timezone


def fmt(n: float) -> str:
    if n >= 1e6:
        return f"{n/1e6:.2f}M"
    if n >= 1e3:
        return f"{n/1e3:.1f}k"
    return f"{int(n)}"


def is_session_file(path: str) -> bool:
    """Only canonical session jsonl: <id>.jsonl. Exclude trajectory/deleted/bak."""
    name = os.path.basename(path)
    if not name.endswith(".jsonl"):
        return False
    bad = (".trajectory.", ".deleted", ".bak", ".tmp")
    return not any(b in name for b in bad)


def ts_to_date(ts: str, tz_mode: str) -> str:
    """Convert ISO ts to YYYY-MM-DD in chosen tz. tz_mode: 'utc'|'local'."""
    if not ts:
        return ""
    if tz_mode == "utc":
        return ts[:10]  # ISO already UTC (...Z)
    # local
    try:
        # python's fromisoformat needs '+00:00', not 'Z'
        s = ts.replace("Z", "+00:00")
        dt = datetime.fromisoformat(s).astimezone()
        return dt.date().isoformat()
    except Exception:
        return ts[:10]


def aggregate(agents_dir: str, target_date: str, tz_mode: str):
    """Walk */sessions/*.jsonl (excluding trajectory/deleted), sum usage for
    type=='message' & role=='assistant' rows whose date matches target_date."""
    agg = defaultdict(lambda: {
        "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0,
        "calls": 0, "models": set(), "sessions": set(),
    })
    pattern = os.path.join(agents_dir, "*", "sessions", "*.jsonl")
    target_dt = datetime.strptime(target_date, "%Y-%m-%d")

    for path in glob.glob(pattern):
        if not is_session_file(path):
            continue
        agent = path.split(os.sep + "agents" + os.sep)[1].split(os.sep)[0]
        # cheap mtime filter: skip files clearly outside the day
        try:
            mtime = os.path.getmtime(path)
            if mtime < target_dt.timestamp() - 86400:
                continue
        except Exception:
            pass
        try:
            f = open(path, "rb")
        except Exception:
            continue
        with f:
            for line in f:
                # cheap pre-filter
                if b'"type":"message"' not in line or b'"usage"' not in line:
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                if rec.get("type") != "message":
                    continue
                msg = rec.get("message") or {}
                if msg.get("role") != "assistant":
                    continue
                u = msg.get("usage") or {}
                if not isinstance(u, dict):
                    continue
                ts = rec.get("timestamp") or ""
                if ts_to_date(ts, tz_mode) != target_date:
                    continue
                a = agg[agent]
                a["input"] += int(u.get("input", 0) or 0)
                a["output"] += int(u.get("output", 0) or 0)
                a["cacheRead"] += int(u.get("cacheRead", 0) or 0)
                a["cacheWrite"] += int(u.get("cacheWrite", 0) or 0)
                a["calls"] += 1
                m = msg.get("model") or rec.get("modelId")
                if m:
                    a["models"].add(m)
                sid = rec.get("sessionId") or os.path.basename(path).rsplit(".jsonl", 1)[0]
                if sid:
                    a["sessions"].add(sid)
    return agg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=None,
                    help="YYYY-MM-DD (default: today in chosen --tz)")
    ap.add_argument("--tz", choices=["utc", "local"], default="utc",
                    help="Match timestamps in UTC (default, aligns with pew) or local date.")
    ap.add_argument("--agents-dir", default=os.path.expanduser("~/.openclaw/agents"))
    ap.add_argument("--format", choices=["text", "json"], default="text")
    ap.add_argument("--billable", action="store_true",
                    help="Also show equivalent-billable token (cacheRead*0.1 + cacheWrite*1.25)")
    ap.add_argument("--top", type=int, default=20)
    args = ap.parse_args()

    if args.date is None:
        if args.tz == "utc":
            args.date = datetime.now(timezone.utc).date().isoformat()
        else:
            args.date = date.today().isoformat()

    if not os.path.isdir(args.agents_dir):
        print(f"ERR: agents dir not found: {args.agents_dir}", file=sys.stderr)
        sys.exit(2)

    agg = aggregate(args.agents_dir, args.date, args.tz)
    rows = []
    for agent, v in agg.items():
        total = v["input"] + v["output"] + v["cacheRead"] + v["cacheWrite"]
        billable = v["input"] + v["output"] + v["cacheRead"] * 0.1 + v["cacheWrite"] * 1.25
        rows.append({
            "agent": agent,
            "calls": v["calls"],
            "sessions": len(v["sessions"]),
            "input": v["input"],
            "output": v["output"],
            "cacheRead": v["cacheRead"],
            "cacheWrite": v["cacheWrite"],
            "total": total,
            "billable": billable,
            "models": sorted(v["models"]),
        })
    rows.sort(key=lambda r: -r["total"])
    rows = rows[: args.top]

    if args.format == "json":
        print(json.dumps({"date": args.date, "tz": args.tz, "agents": rows},
                         indent=2, ensure_ascii=False))
        return

    print(f"\n📊 OpenClaw agent token usage — {args.date} ({args.tz})")
    print(f"   source: {args.agents_dir}/*/sessions/*.jsonl  (type=message, role=assistant)")
    print()
    if args.billable:
        header = f"{'agent':<12}{'sess':>5}{'calls':>6}{'input':>9}{'output':>9}{'cacheR':>10}{'cacheW':>9}{'TOTAL':>10}{'~bill':>9}  models"
    else:
        header = f"{'agent':<12}{'sess':>5}{'calls':>6}{'input':>9}{'output':>9}{'cacheR':>10}{'cacheW':>9}{'TOTAL':>10}  models"
    print(header)
    print("-" * len(header))
    grand = defaultdict(float)
    for r in rows:
        models = ",".join(r["models"])
        if len(models) > 38:
            models = models[:35] + "..."
        line = (f"{r['agent']:<12}{r['sessions']:>5}{r['calls']:>6}"
                f"{fmt(r['input']):>9}{fmt(r['output']):>9}{fmt(r['cacheRead']):>10}"
                f"{fmt(r['cacheWrite']):>9}{fmt(r['total']):>10}")
        if args.billable:
            line += f"{fmt(r['billable']):>9}"
        line += f"  {models}"
        print(line)
        for k in ("input", "output", "cacheRead", "cacheWrite", "total", "billable"):
            grand[k] += r[k]
    print("-" * len(header))
    line = (f"{'TOTAL':<12}{'':>5}{'':>6}"
            f"{fmt(grand['input']):>9}{fmt(grand['output']):>9}{fmt(grand['cacheRead']):>10}"
            f"{fmt(grand['cacheWrite']):>9}{fmt(grand['total']):>10}")
    if args.billable:
        line += f"{fmt(grand['billable']):>9}"
    print(line)
    print()
    print("notes:")
    print("  - cacheRead 通常按 ~10% 价格计费；cacheWrite ~125%。")
    print("  - 仅统计 session.jsonl 中 type=message & role=assistant 的真实 LLM 调用。")
    print("  - 不读 *.trajectory.jsonl（每次调用会重复 ~2.6×）。")


if __name__ == "__main__":
    main()
