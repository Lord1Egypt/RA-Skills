#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""behavior-observability: 智能体行为可观测性 — 结构化追踪每一次动作，便于事后审计/归因/调优。

能力：
  - 结构化事件日志：emit(type, input, output, status, agent, risk, parent, duration_ms)
  - 多维查询：query(type/status/agent/since)
  - 指标聚合：总量 / 按类型 / 按状态 / 错误率 / 平均时延 / P95 时延
  - 时间线：按发生顺序回放行为轨迹
  - 置信自检：selftest 覆盖 入链 / 查询过滤 / 错误率 / 指标聚合 / 时间线

用法：
  python observability.py --selftest
  python observability.py --emit '{"type":"tool_call","action":"read file","status":"ok","agent":"agent-7"}'
  python observability.py --query '{"status":"error"}'
  python observability.py --metrics
  python observability.py --timeline
"""
import argparse
import json
import sys
import datetime
import uuid


def now_iso():
    return datetime.datetime.now().isoformat(timespec="milliseconds")


class EventLog:
    def __init__(self):
        self.events = []

    def emit(self, etype, action="", status="ok", agent="agent",
             risk="low", parent=None, duration_ms=None, payload=None):
        ev = {
            "id": uuid.uuid4().hex[:8],
            "ts": now_iso(),
            "type": etype,
            "action": action,
            "status": status,
            "agent": agent,
            "risk": risk,
            "parent": parent,
            "duration_ms": duration_ms,
            "payload": payload or {},
        }
        self.events.append(ev)
        return ev["id"]

    def query(self, type=None, status=None, agent=None, since=None):
        out = self.events
        if type:
            out = [e for e in out if e["type"] == type]
        if status:
            out = [e for e in out if e["status"] == status]
        if agent:
            out = [e for e in out if e["agent"] == agent]
        if since:
            out = [e for e in out if e["ts"] >= since]
        return out

    def metrics(self):
        total = len(self.events)
        by_type = {}
        by_status = {}
        durations = [e["duration_ms"] for e in self.events
                     if isinstance(e["duration_ms"], (int, float))]
        errors = sum(1 for e in self.events if e["status"] == "error")
        for e in self.events:
            by_type[e["type"]] = by_type.get(e["type"], 0) + 1
            by_status[e["status"]] = by_status.get(e["status"], 0) + 1
        avg = (sum(durations) / len(durations)) if durations else 0.0
        p95 = 0.0
        if durations:
            sd = sorted(durations)
            idx = min(len(sd) - 1, max(0, int(round(0.95 * (len(sd) - 1)))))
            p95 = sd[idx]
        return {
            "total": total,
            "by_type": by_type,
            "by_status": by_status,
            "error_rate": (errors / total) if total else 0.0,
            "avg_duration_ms": avg,
            "p95_duration_ms": p95,
        }

    def timeline(self):
        return [{"ts": e["ts"], "type": e["type"], "status": e["status"],
                 "agent": e["agent"]} for e in self.events]


def selftest():
    log = EventLog()

    # 1) 入链
    log.emit("tool_call", "read /etc/hosts", "ok", "agent-7", "low", duration_ms=12)
    log.emit("tool_call", "write /tmp/x", "ok", "agent-7", "low", duration_ms=30)
    log.emit("tool_call", "delete /data", "error", "agent-7", "critical", duration_ms=5)
    log.emit("llm_call", "plan next", "ok", "planner", "low", duration_ms=420)
    assert len(log.events) == 4
    print("[1] 入链 4 条事件 ✓")

    # 2) 查询过滤
    errs = log.query(status="error")
    assert len(errs) == 1 and errs[0]["action"] == "delete /data"
    print("[2] 查询 status=error -> 1 条 ✓")

    # 3) 错误率
    m = log.metrics()
    assert abs(m["error_rate"] - 0.25) < 1e-9, m["error_rate"]
    print(f"[3] 错误率 = {m['error_rate']:.2f} ✓")

    # 4) 指标聚合
    assert m["total"] == 4 and m["by_type"].get("tool_call") == 3
    assert m["avg_duration_ms"] == (12 + 30 + 5 + 420) / 4
    print(f"[4] 指标聚合 total={m['total']} avg={m['avg_duration_ms']:.1f}ms ✓")

    # 5) 时间线
    tl = log.timeline()
    assert len(tl) == 4 and "ts" in tl[0] and tl[0]["agent"] == "agent-7"
    print("[5] 时间线回放 4 步 ✓")

    # 6) P95 时延
    assert m["p95_duration_ms"] == max(12, 30, 5, 420), m["p95_duration_ms"]
    print(f"[6] P95 时延 = {m['p95_duration_ms']}ms ✓")

    print("\n✅ behavior-observability selftest 全部通过")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--emit")
    ap.add_argument("--query", default="{}")
    ap.add_argument("--metrics", action="store_true")
    ap.add_argument("--timeline", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return 0 if selftest() else 1

    log = EventLog()
    if args.emit:
        d = json.loads(args.emit)
        eid = log.emit(d.get("type", "event"), d.get("action", ""),
                       d.get("status", "ok"), d.get("agent", "agent"),
                       d.get("risk", "low"), d.get("parent"),
                       d.get("duration_ms"), d.get("payload"))
        print(json.dumps({"event_id": eid}, ensure_ascii=False))
        return 0
    if args.query:
        f = json.loads(args.query)
        print(json.dumps(log.query(**f), ensure_ascii=False, indent=2))
        return 0
    if args.metrics:
        print(json.dumps(log.metrics(), ensure_ascii=False))
        return 0
    if args.timeline:
        print(json.dumps(log.timeline(), ensure_ascii=False, indent=2))
        return 0
    print("用法见 --selftest 或 --emit/--query/--metrics/--timeline")
    return 0


if __name__ == "__main__":
    sys.exit(main())
