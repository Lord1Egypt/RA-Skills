"""claw-reliability: Log file alerter. Always-on fallback."""

from pathlib import Path
from alerts.base import BaseAlerter, Alert


class LogFileAlerter(BaseAlerter):
    def __init__(self, path="data/alerts.log"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def send_alert(self, alert):
        try:
            with open(self.path, "a") as f:
                f.write(alert.format_full() + "\n---\n")
            return True
        except Exception as e:
            print(f"[claw-reliability] Log file alert failed: {e}")
            return False
