#!/usr/bin/env python3
"""
claw-reliability: Main monitoring CLI.
Usage: python3 monitor.py {start|summary|tools|costs|anomalies|alerts|configure-alerts|test-alerts}
"""

import sys, os, time, signal, argparse, yaml
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from store import MetricsStore
from parser import EventParser
from analyzer import AnomalyDetector
from alerts import AlertManager, Alert, Severity, AlertType
from alerts.discord_alerter import DiscordAlerter
from alerts.logfile_alerter import LogFileAlerter


def load_config(path=None):
    p = Path(path) if path else Path(__file__).parent.parent / "config.yaml"
    if p.exists():
        with open(p) as f:
            return yaml.safe_load(f) or {}
    return {}


def setup_alerts(config):
    mgr = AlertManager()
    dests = config.get("alert_destinations", {})
    lf = dests.get("logfile", {})
    if lf.get("enabled", True):
        base = Path(__file__).parent.parent
        mgr.add_destination(LogFileAlerter(str(base / lf.get("path", "data/alerts.log"))))
    dc = dests.get("discord", {})
    if dc.get("enabled") and dc.get("webhook_url"):
        mgr.add_destination(DiscordAlerter(dc["webhook_url"]))
    return mgr


def estimate_cost(model, tokens_in, tokens_out, cost_models):
    costs = cost_models.get(model, {})
    if not costs:
        for k, v in cost_models.items():
            if k in model or model in k:
                costs = v
                break
    if not costs:
        return 0.0
    return round((tokens_in / 1e6) * costs.get("input", 0) + (tokens_out / 1e6) * costs.get("output", 0), 6)


class Monitor:
    def __init__(self, config):
        self.config = config
        mc = config.get("monitoring", {})
        base = Path(__file__).parent.parent
        self.store = MetricsStore(str(base / mc.get("db_path", "data/metrics.db")))
        self.parser = EventParser(mc.get("openclaw_state_dir", "~/.openclaw"))
        self.alert_manager = setup_alerts(config)
        self.detector = AnomalyDetector(self.store, self.alert_manager, config.get("alerts", {}))
        self.cost_models = config.get("cost_models", {})
        self.poll_interval = mc.get("poll_interval", 5)
        self._running = False
        self._pending = {}

    def process_event(self, event):
        et = event.get("event_type")
        if et == "tool_call_start":
            tid = event.get("tool_id")
            if tid:
                self._pending[tid] = {"tool_name": event["tool_name"], "start": time.time(),
                    "session_id": event.get("session_id"), "agent_id": event.get("agent_id"),
                    "params": event.get("params_summary")}
            self.detector.check_unusual_tool(event["tool_name"])

        elif et == "tool_call_end":
            p = self._pending.pop(event.get("tool_id"), None)
            name = event.get("tool_name") or (p["tool_name"] if p else "unknown")
            dur = (time.time() - p["start"]) * 1000 if p else None
            sid = event.get("session_id") or (p["session_id"] if p else None)
            aid = event.get("agent_id") or (p["agent_id"] if p else None)
            self.store.record_tool_invocation(name, event.get("success", True), dur, sid, aid,
                event.get("error_message"), p["params"] if p else None)
            if not event.get("success", True):
                self.detector.check_tool_failure(name)
            self.detector.check_loop(name, sid)

        elif et == "llm_call":
            ti, to = event.get("tokens_in", 0), event.get("tokens_out", 0)
            model = event.get("model", "unknown")
            cost = event.get("total_cost") or estimate_cost(model, ti, to, self.cost_models)
            self.store.record_llm_call(model, ti, to, estimated_cost_usd=cost,
                session_id=event.get("session_id"), agent_id=event.get("agent_id"))
            self.detector.check_cost_spike()

        elif et == "session_start":
            self.store.upsert_session(event.get("session_id", "unknown"),
                event.get("agent_id"), started_at=event.get("timestamp"))
            self.detector.reset_turn_counts()

        elif et == "session_end":
            self.store.upsert_session(event.get("session_id", "unknown"),
                event.get("agent_id"), ended_at=event.get("timestamp"))

    def run(self):
        self._running = True
        print(f"[claw-reliability] Monitor started. Polling every {self.poll_interval}s")
        print(f"[claw-reliability] Destinations: {len(self.alert_manager.destinations)}")
        print("[claw-reliability] Ctrl+C to stop.\n")
        signal.signal(signal.SIGINT, lambda *_: setattr(self, '_running', False))
        signal.signal(signal.SIGTERM, lambda *_: setattr(self, '_running', False))
        while self._running:
            try:
                n = sum(1 for e in self.parser.scan_all() if (self.process_event(e) or True))
                if n:
                    print(f"[claw-reliability] Processed {n} events")
                self.detector.run_all_checks()
            except Exception as e:
                print(f"[claw-reliability] Error: {e}")
            time.sleep(self.poll_interval)
        self.store.close()
        print("[claw-reliability] Stopped.")


def _get_store(config):
    mc = config.get("monitoring", {})
    base = Path(__file__).parent.parent
    return MetricsStore(str(base / mc.get("db_path", "data/metrics.db")))


def cmd_start(args, config):
    Monitor(config).run()


def cmd_summary(args, config):
    s = _get_store(config)
    d = s.get_dashboard_summary()
    print("=" * 60)
    print("  🦞 claw-reliability — Metrics Summary")
    print("=" * 60)
    print("\n📊 Tool Usage (24h)\n" + "-" * 40)
    for t in d["tool_stats_24h"] or []:
        rate = (t["successes"] / t["total_calls"] * 100) if t["total_calls"] else 0
        print(f"  {t['tool_name']}: {t['total_calls']} calls | {rate:.0f}% success | {t['avg_duration_ms'] or 0:.0f}ms avg")
    if not d["tool_stats_24h"]:
        print("  No tool calls recorded yet.")
    c = d["cost_summary_24h"]
    print(f"\n💰 Cost (24h)\n" + "-" * 40)
    print(f"  Total: ${c['total_cost_usd']:.4f} | Tokens: {c['total_tokens']:,}")
    print(f"\n🔔 Alerts\n" + "-" * 40)
    for a in (d["recent_alerts"] or [])[:5]:
        icon = {"info": "ℹ️", "warning": "⚠️", "critical": "🚨"}.get(a["severity"], "📢")
        print(f"  {icon} {a['message']}")
    if not d["recent_alerts"]:
        print("  All clear!")
    print()
    s.close()


def cmd_tools(args, config):
    s = _get_store(config)
    stats = s.get_tool_stats(args.hours)
    print(f"\n🔧 Tool Report ({args.hours}h)\n" + "=" * 60)
    if stats:
        print(f"  {'Tool':<25} {'Calls':<8} {'OK':<8} {'Fail':<8} {'Rate':<8}")
        print("  " + "-" * 50)
        for t in stats:
            rate = (t["successes"] / t["total_calls"] * 100) if t["total_calls"] else 0
            print(f"  {t['tool_name']:<25} {t['total_calls']:<8} {t['successes']:<8} {t['failures']:<8} {rate:.0f}%")
    else:
        print("  No data.")
    print()
    s.close()


def cmd_costs(args, config):
    s = _get_store(config)
    c = s.get_cost_summary(args.hours)
    print(f"\n💰 Cost Report ({args.hours}h)\n" + "=" * 60)
    print(f"  Total: ${c['total_cost_usd']:.4f} | Tokens: {c['total_tokens']:,}")
    for m in c["by_model"]:
        print(f"  {m['model']}: {m['call_count']} calls, ${m['total_cost'] or 0:.4f}")
    print()
    s.close()


def cmd_anomalies(args, config):
    s = _get_store(config)
    det = AnomalyDetector(s, setup_alerts(config), config.get("alerts", {}))
    print("\n🔍 Running anomaly detection...")
    det.run_all_checks()
    print("  Done.\n")
    s.close()


def cmd_alerts(args, config):
    s = _get_store(config)
    for a in s.get_recent_alerts(20):
        icon = {"info": "ℹ️", "warning": "⚠️", "critical": "🚨"}.get(a["severity"], "📢")
        print(f"  {icon} [{a['timestamp'][:19]}] {a['message']}")
    if not s.get_recent_alerts(1):
        print("  No alerts.")
    print()
    s.close()


def cmd_configure_alerts(args, config):
    if args.destination == "discord" and args.webhook_url:
        p = Path(__file__).parent.parent / "config.yaml"
        cfg = {}
        if p.exists():
            with open(p) as f:
                cfg = yaml.safe_load(f) or {}
        cfg.setdefault("alert_destinations", {})["discord"] = {"enabled": True, "webhook_url": args.webhook_url}
        with open(p, 'w') as f:
            yaml.dump(cfg, f, default_flow_style=False)
        print("  ✅ Discord alerts configured.")
    else:
        print("  Usage: monitor.py configure-alerts --destination discord --webhook-url <URL>")


def cmd_test_alerts(args, config):
    mgr = setup_alerts(config)
    print("\n🧪 Testing alerts...")
    for name, ok in mgr.test_all().items():
        print(f"  {'✅' if ok else '❌'} {name}")
    print()


def main():
    p = argparse.ArgumentParser(description="🦞 claw-reliability")
    p.add_argument("--config", default=None)
    sub = p.add_subparsers(dest="command")
    sub.add_parser("start")
    sub.add_parser("summary")
    s = sub.add_parser("tools"); s.add_argument("--hours", type=int, default=24)
    s = sub.add_parser("costs"); s.add_argument("--hours", type=int, default=24)
    sub.add_parser("anomalies")
    sub.add_parser("alerts")
    s = sub.add_parser("configure-alerts"); s.add_argument("--destination", required=True); s.add_argument("--webhook-url", default="")
    sub.add_parser("test-alerts")
    args = p.parse_args()
    config = load_config(args.config)
    cmds = {"start": cmd_start, "summary": cmd_summary, "tools": cmd_tools, "costs": cmd_costs,
            "anomalies": cmd_anomalies, "alerts": cmd_alerts, "configure-alerts": cmd_configure_alerts,
            "test-alerts": cmd_test_alerts}
    if args.command in cmds:
        cmds[args.command](args, config)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
