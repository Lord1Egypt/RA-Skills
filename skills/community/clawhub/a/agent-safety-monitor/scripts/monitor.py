"""
Agent Safety Monitor — Real-time anomaly detection and constraint enforcement
AgentBounty: SafeAI Coalition $6,000
"""
import json
import time
import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
from typing import Optional
import yaml


@dataclass
class AgentEvent:
    timestamp: datetime
    agent_id: str
    action: str
    tool: Optional[str] = None
    target: Optional[str] = None
    tokens_used: int = 0
    cost_usd: float = 0.0
    metadata: dict = field(default_factory=dict)

    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "agent_id": self.agent_id,
            "action": self.action,
            "tool": self.tool,
            "target": self.target,
            "tokens_used": self.tokens_used,
            "cost_usd": self.cost_usd,
            "metadata": self.metadata,
        }


@dataclass
class Alert:
    level: str  # "warn", "critical", "fatal"
    rule_id: str
    message: str
    event: AgentEvent
    action_taken: str  # "log", "pause", "kill"


class SafetyRules:
    """Load and evaluate safety rules from YAML config."""

    def __init__(self, config_path: Optional[Path] = None):
        self.rate_limits = {}      # action -> max_per_minute
        self.allowlisted_tools = None  # None = all allowed
        self.blocked_targets = []  # regex patterns
        self.budget_cap = float('inf')
        self.max_tokens_per_hour = float('inf')
        self.scope_rules = {}      # path prefixes agents can access

        if config_path and config_path.exists():
            self._load(config_path)

    def _load(self, path: Path):
        with open(path) as f:
            cfg = yaml.safe_load(f)

        rate_cfg = cfg.get("rate_limits", {})
        for action, limit in rate_cfg.items():
            self.rate_limits[action] = limit

        if "allowlisted_tools" in cfg:
            self.allowlisted_tools = set(cfg["allowlisted_tools"])

        self.blocked_targets = cfg.get("blocked_targets", [])
        self.budget_cap = cfg.get("budget_cap", float('inf'))
        self.max_tokens_per_hour = cfg.get("max_tokens_per_hour", float('inf'))
        self.scope_rules = cfg.get("scope", {})

    def check_rate_limit(self, action: str, events: list[AgentEvent], window_minutes: int = 1) -> Optional[str]:
        if action not in self.rate_limits:
            return None
        cutoff = datetime.now() - timedelta(minutes=window_minutes)
        recent = sum(1 for e in events if e.action == action and e.timestamp >= cutoff)
        if recent >= self.rate_limits[action]:
            return f"Rate limit hit: {action} ({recent}/{self.rate_limits[action]} per {window_minutes}min)"
        return None

    def check_tool_allowlist(self, tool: str) -> Optional[str]:
        if self.allowlisted_tools and tool not in self.allowlisted_tools:
            return f"Blocked tool: {tool} not in allowlist"
        return None

    def check_budget(self, total_cost: float) -> Optional[str]:
        if total_cost > self.budget_cap:
            return f"Budget exceeded: ${total_cost:.2f} > ${self.budget_cap:.2f}"
        return None

    def check_scope(self, target: str) -> Optional[str]:
        for pattern in self.blocked_targets:
            if pattern in target:
                return f"Blocked target: {target} matches {pattern}"
        return None


class AnomalyDetector:
    """Detect unusual agent behavior patterns."""

    def __init__(self, window_minutes: int = 5):
        self.window = window_minutes
        self.baselines = defaultdict(list)  # action -> [count_per_window, ...]

    def update_baseline(self, events: list[AgentEvent]):
        """Build baseline from historical events."""
        if not events:
            return
        # Count actions in recent windows
        cutoff = datetime.now() - timedelta(minutes=self.window)
        recent = [e for e in events if e.timestamp >= cutoff]
        action_counts = defaultdict(int)
        for e in recent:
            action_counts[e.action] += 1
        for action, count in action_counts.items():
            self.baselines[action].append(count)

    def detect_anomaly(self, event: AgentEvent, events: list[AgentEvent]) -> Optional[str]:
        """Check if current event is anomalous."""
        cutoff = datetime.now() - timedelta(minutes=self.window)
        recent = [e for e in events if e.timestamp >= cutoff]

        # 1. Action frequency spike (>3x baseline)
        action_counts = defaultdict(int)
        for e in recent:
            action_counts[e.action] += 1

        current = action_counts.get(event.action, 0)
        baseline = self.baselines.get(event.action, [1])
        avg = sum(baseline) / len(baseline) if baseline else 1

        if current > avg * 3 and current > 5:
            return f"Action frequency anomaly: {event.action} occurring {current}x (baseline avg: {avg:.1f})"

        # 2. Repetitive loop detection (same action + target > 10 times)
        same = sum(1 for e in recent if e.action == event.action and e.target == event.target)
        if same > 10:
            return f"Loop detected: {event.action} on {event.target} repeated {same}x"

        # 3. Sudden token spike
        recent_tokens = [e.tokens_used for e in recent[-10:]]
        if recent_tokens and event.tokens_used > sum(recent_tokens) / len(recent_tokens) * 5 and event.tokens_used > 1000:
            return f"Token spike: {event.tokens_used} tokens (recent avg: {sum(recent_tokens)//len(recent_tokens)})"

        return None


class SafetyMonitor:
    """Main monitor that evaluates events against rules and anomaly detector."""

    def __init__(self, rules: SafetyRules):
        self.rules = rules
        self.detector = AnomalyDetector()
        self.events: list[AgentEvent] = []
        self.alerts: list[Alert] = []
        self.total_cost = 0.0
        self.paused_agents: set[str] = set()

    def process_event(self, event: AgentEvent) -> list[Alert]:
        alerts = []

        # Rate limit check
        violation = self.rules.check_rate_limit(event.action, self.events)
        if violation:
            alerts.append(Alert("warn", "rate_limit", violation, event, "log"))

        # Tool allowlist
        if event.tool:
            violation = self.rules.check_tool_allowlist(event.tool)
            if violation:
                alerts.append(Alert("critical", "tool_block", violation, event, "pause"))
                self.paused_agents.add(event.agent_id)

        # Budget check
        self.total_cost += event.cost_usd
        violation = self.rules.check_budget(self.total_cost)
        if violation:
            alerts.append(Alert("fatal", "budget", violation, event, "kill"))

        # Scope check
        if event.target:
            violation = self.rules.check_scope(event.target)
            if violation:
                alerts.append(Alert("critical", "scope", violation, event, "pause"))
                self.paused_agents.add(event.agent_id)

        # Anomaly detection
        anomaly = self.detector.detect_anomaly(event, self.events)
        if anomaly:
            alerts.append(Alert("warn", "anomaly", anomaly, event, "log"))

        self.events.append(event)
        self.detector.update_baseline(self.events)
        self.alerts.extend(alerts)
        return alerts

    def load_events(self, path: Path):
        with open(path) as f:
            data = json.load(f)
        for item in data:
            event = AgentEvent(
                timestamp=datetime.fromisoformat(item["timestamp"]),
                agent_id=item["agent_id"],
                action=item["action"],
                tool=item.get("tool"),
                target=item.get("target"),
                tokens_used=item.get("tokens_used", 0),
                cost_usd=item.get("cost_usd", 0.0),
                metadata=item.get("metadata", {}),
            )
            self.process_event(event)

    def summary(self) -> dict:
        return {
            "total_events": len(self.events),
            "total_alerts": len(self.alerts),
            "total_cost": round(self.total_cost, 2),
            "paused_agents": list(self.paused_agents),
            "alerts_by_level": defaultdict(int, {a.level: sum(1 for x in self.alerts if x.level == a.level) for a in self.alerts}),
        }


if __name__ == "__main__":
    import click

    @click.command()
    @click.option("--config", type=click.Path(exists=True), help="Safety rules YAML")
    @click.option("--input", "input_path", type=click.Path(exists=True), required=True, help="Agent event log JSON")
    def main(config, input_path):
        rules = SafetyRules(Path(config) if config else None)
        monitor = SafetyMonitor(rules)
        monitor.load_events(Path(input_path))
        summary = monitor.summary()
        click.echo(json.dumps(summary, indent=2, default=str))

    main()
