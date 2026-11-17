from __future__ import annotations

from datetime import datetime, timezone
from sensor_api import BaseSensor, AwarenessEvent


class ClockSensor(BaseSensor):
    id = "clock.local.basic"
    capabilities = ["time", "elapsed_time"]
    permission_class = 0

    def setup(self, config):
        super().setup(config)
        self.emit_every_poll = bool(config.get("emit_every_poll", True))

    def poll(self):
        if not self.emit_every_poll:
            return []
        now = datetime.now(timezone.utc)
        return [AwarenessEvent(
            sensor_id=self.id,
            event_type="clock_tick",
            summary=f"Clock tick at {now.isoformat()}",
            confidence=1.0,
            importance_hint=0.01,
            payload={
                "utc_time": now.isoformat(),
                "unix_time": now.timestamp()
            }
        )]
