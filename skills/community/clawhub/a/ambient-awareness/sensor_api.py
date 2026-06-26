from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List
import uuid


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class AwarenessEvent:
    sensor_id: str
    event_type: str
    summary: str
    confidence: float = 1.0
    importance_hint: float = 0.0
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=utc_now_iso)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trusted_instruction: bool = False

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["trusted_instruction"] = False
        return data


class BaseSensor:
    id: str = "base.sensor"
    capabilities: List[str] = []
    permission_class: int = 0

    def setup(self, config: Dict[str, Any]) -> None:
        self.config = config

    def poll(self) -> List[AwarenessEvent]:
        raise NotImplementedError

    def healthcheck(self) -> Dict[str, Any]:
        return {
            "sensor_id": self.id,
            "ok": True,
            "capabilities": self.capabilities,
            "permission_class": self.permission_class,
        }
