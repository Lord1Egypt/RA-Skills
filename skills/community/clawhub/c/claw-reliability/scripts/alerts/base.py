"""
claw-reliability: Pluggable alert system.
Extend BaseAlerter to add your own destination.
Built-in: DiscordAlerter, LogFileAlerter
"""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from enum import Enum


class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertType(str, Enum):
    TOOL_FAILURE = "tool_failure"
    COST_SPIKE = "cost_spike"
    LOOP_DETECTED = "loop_detected"
    UNUSUAL_ACTIVITY = "unusual_activity"


class Alert:
    def __init__(self, severity, alert_type, message, details=None):
        self.severity = severity
        self.alert_type = alert_type
        self.message = message
        self.details = details or {}
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_dict(self):
        return {"severity": self.severity.value, "alert_type": self.alert_type.value,
                "message": self.message, "details": self.details, "timestamp": self.timestamp}

    def format_short(self):
        icon = {"info": "ℹ️", "warning": "⚠️", "critical": "🚨"}
        return f"{icon.get(self.severity.value, '📢')} [{self.severity.value.upper()}] {self.message}"

    def format_full(self):
        lines = [self.format_short()]
        for k, v in self.details.items():
            lines.append(f"  {k}: {v}")
        lines.append(f"  Time: {self.timestamp}")
        return "\n".join(lines)


class BaseAlerter(ABC):
    """Extend this to create custom alert destinations."""

    @abstractmethod
    def send_alert(self, alert: Alert) -> bool:
        pass

    def test_connection(self) -> bool:
        test_alert = Alert(Severity.INFO, AlertType.UNUSUAL_ACTIVITY,
                           "🦞 claw-reliability test — alerts are working!")
        return self.send_alert(test_alert)


class AlertManager:
    def __init__(self):
        self.destinations = []

    def add_destination(self, alerter):
        self.destinations.append(alerter)

    def dispatch(self, alert):
        for dest in self.destinations:
            try:
                dest.send_alert(alert)
            except Exception as e:
                print(f"[claw-reliability] Alert destination failed: {e}")

    def test_all(self):
        results = {}
        for dest in self.destinations:
            name = dest.__class__.__name__
            try:
                results[name] = dest.test_connection()
            except Exception:
                results[name] = False
        return results
