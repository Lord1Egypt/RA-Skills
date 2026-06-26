"""claw-reliability: Anomaly detection engine."""

from datetime import datetime, timezone
from store import MetricsStore
from alerts import Alert, AlertManager, Severity, AlertType


class AnomalyDetector:
    def __init__(self, store, alert_manager, config=None):
        self.store = store
        self.alert_manager = alert_manager
        c = config or {}
        self.tool_failure_threshold = c.get("tool_failure_threshold", 3)
        self.cost_spike_multiplier = c.get("cost_spike_multiplier", 2.0)
        self.loop_detection_threshold = c.get("loop_detection_threshold", 10)
        self.unusual_tool_alert = c.get("unusual_tool_alert", True)
        self.cooldown_seconds = c.get("cooldown_seconds", 300)
        self._turn_tool_counts = {}

    def check_tool_failure(self, tool_name):
        consecutive = self.store.get_consecutive_failures(tool_name)
        if consecutive >= self.tool_failure_threshold and self._should_alert(AlertType.TOOL_FAILURE):
            failures = self.store.get_recent_tool_failures(tool_name, 5)
            last_error = failures[0]["error_message"][:200] if failures else "Unknown"
            alert = Alert(
                Severity.CRITICAL if consecutive >= 5 else Severity.WARNING,
                AlertType.TOOL_FAILURE,
                f"Tool `{tool_name}` has failed {consecutive} times consecutively",
                {"tool": tool_name, "consecutive_failures": consecutive, "last_error": last_error})
            self.store.record_alert(alert.severity.value, alert.alert_type.value,
                                     alert.message, alert.details)
            self.alert_manager.dispatch(alert)

    def check_cost_spike(self):
        current = self.store.get_hourly_cost(1)
        rolling = self.store.get_hourly_cost(6) / 6
        if rolling > 0 and current > (rolling * self.cost_spike_multiplier) and self._should_alert(AlertType.COST_SPIKE):
            alert = Alert(Severity.WARNING, AlertType.COST_SPIKE,
                f"Cost spike: ${current:.4f}/hr (avg: ${rolling:.4f}/hr)",
                {"current_hour": f"${current:.4f}", "avg_hourly": f"${rolling:.4f}",
                 "multiplier": f"{current/rolling:.1f}x"})
            self.store.record_alert(alert.severity.value, alert.alert_type.value,
                                     alert.message, alert.details)
            self.alert_manager.dispatch(alert)

    def check_loop(self, tool_name, session_id=None):
        key = f"{session_id or 'unknown'}:{tool_name}"
        self._turn_tool_counts[key] = self._turn_tool_counts.get(key, 0) + 1
        if self._turn_tool_counts[key] == self.loop_detection_threshold and self._should_alert(AlertType.LOOP_DETECTED):
            alert = Alert(Severity.CRITICAL, AlertType.LOOP_DETECTED,
                f"Possible loop: `{tool_name}` called {self._turn_tool_counts[key]}+ times",
                {"tool": tool_name, "call_count": self._turn_tool_counts[key], "session_id": session_id or "unknown"})
            self.store.record_alert(alert.severity.value, alert.alert_type.value,
                                     alert.message, alert.details)
            self.alert_manager.dispatch(alert)

    def check_unusual_tool(self, tool_name):
        if self.unusual_tool_alert and not self.store.is_tool_known(tool_name) and self._should_alert(AlertType.UNUSUAL_ACTIVITY):
            alert = Alert(Severity.INFO, AlertType.UNUSUAL_ACTIVITY,
                f"First-ever use of tool `{tool_name}`", {"tool": tool_name})
            self.store.record_alert(alert.severity.value, alert.alert_type.value,
                                     alert.message, alert.details)
            self.alert_manager.dispatch(alert)

    def reset_turn_counts(self):
        self._turn_tool_counts.clear()

    def run_all_checks(self):
        self.check_cost_spike()
        for stat in self.store.get_tool_stats(1):
            if stat["failures"] > 0:
                self.check_tool_failure(stat["tool_name"])

    def _should_alert(self, alert_type):
        last = self.store.get_last_alert_time(alert_type.value)
        if not last:
            return True
        try:
            return (datetime.now(timezone.utc) - datetime.fromisoformat(last)).total_seconds() > self.cooldown_seconds
        except ValueError:
            return True
