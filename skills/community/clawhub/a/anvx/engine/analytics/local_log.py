"""JSON-lines local event logger — fallback when analytics endpoint is unavailable."""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_DEFAULT_LOG_PATH = Path.home() / ".token-economy-intel" / "events.jsonl"


class LocalEventLog:
    """Append-only JSON-lines logger for analytics events."""

    def __init__(self, path: str | Path | None = None) -> None:
        self._path = Path(path) if path else _DEFAULT_LOG_PATH

    def write(self, event: dict[str, Any]) -> None:
        """Append a single event as a JSON line. Creates file/dirs if needed."""
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            entry = {
                "logged_at": datetime.now().isoformat(),
                **event,
            }
            with self._path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry, default=str) + "\n")
        except OSError as exc:
            logger.error("Failed to write local event log: %s", exc)

    def read_all(self) -> list[dict[str, Any]]:
        """Read all logged events (for debugging/testing)."""
        if not self._path.exists():
            return []
        events: list[dict[str, Any]] = []
        try:
            with self._path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        events.append(json.loads(line))
        except (OSError, json.JSONDecodeError) as exc:
            logger.error("Failed to read local event log: %s", exc)
        return events

    def clear(self) -> None:
        """Delete the log file (for testing)."""
        if self._path.exists():
            self._path.unlink()
