"""AgentPathfinder v2 — Tamper-evident audit trail (Phase 4 cleanup)."""
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional

from .pathfinder_core import hmac_sign, verify_hmac


class AuditTrail:
    """Append-only, HMAC-signed audit log (JSON Lines).

    Phase 4: The signing_key should be a *derived* audit key, never the
    raw master key.  Callers are responsible for deriving it via
    TaskEngine._derive_audit_key(master_key).
    """

    def __init__(self, log_path: Path, signing_key: bytes):
        """
        Args:
            log_path: Path to the JSONL audit file.
            signing_key: HMAC signing key (should be derived audit key,
                         NOT the raw master key).
        """
        self.log_path = Path(log_path)
        self.signing_key = signing_key
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    # Keep backward-compatible property so any code using .master_key still works
    @property
    def master_key(self):
        return self.signing_key

    def _sign_event(self, event: Dict[str, Any]) -> str:
        """Sign event with HMAC(signing_key, serialized_event)."""
        canonical = json.dumps(event, sort_keys=True, default=str)
        return hmac_sign(self.signing_key, canonical)

    def log(self, event_type: str, task_id: str, **kwargs) -> Dict[str, Any]:
        """Append signed event to audit trail."""
        event = {
            "event": event_type,
            "task_id": task_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "seq": self._next_seq(),
            **kwargs,
        }
        event["hmac"] = self._sign_event(event)

        with open(self.log_path, "a") as f:
            f.write(json.dumps(event, default=str) + "\n")

        return event

    def _next_seq(self) -> int:
        """Get next sequence number."""
        if not self.log_path.exists():
            return 0
        with open(self.log_path) as f:
            lines = f.readlines()
        return len(lines)

    def read_trail(self, task_id: Optional[str] = None) -> list:
        """Read audit trail, optionally filtered by task_id."""
        if not self.log_path.exists():
            return []

        events = []
        with open(self.log_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    events.append({"corrupted": True, "raw": line})
                    continue

                if task_id and event.get("task_id") != task_id:
                    continue

                # Verify HMAC
                stored_hmac = event.pop("hmac", None)
                event["tamper_ok"] = verify_hmac(
                    self.signing_key,
                    json.dumps(event, sort_keys=True, default=str),
                    stored_hmac or "",
                )
                # Preserve truncated HMAC for display
                if stored_hmac:
                    event["hmac_truncated"] = stored_hmac[:16] + "..."
                events.append(event)

        return events

    def verify_integrity(self) -> Dict[str, Any]:
        """Verify entire audit trail. Returns tamper report."""
        events = self.read_trail()
        total = len(events)
        tampered = sum(1 for e in events if not e.get("tamper_ok", True))
        corrupted = sum(1 for e in events if e.get("corrupted", False))

        return {
            "total_events": total,
            "tampered": tampered,
            "corrupted": corrupted,
            "integrity_ok": tampered == 0 and corrupted == 0,
        }
