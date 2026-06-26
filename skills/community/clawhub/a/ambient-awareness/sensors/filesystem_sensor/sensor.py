from __future__ import annotations

import fnmatch
import json
from pathlib import Path
from typing import Dict, Any, Iterable

from sensor_api import BaseSensor, AwarenessEvent

ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT_PATH = ROOT / "state" / "filesystem_snapshot.json"


class FilesystemSensor(BaseSensor):
    id = "filesystem.local.watch"
    capabilities = ["filesystem", "file_created", "file_modified", "file_deleted"]
    permission_class = 0

    def setup(self, config: Dict[str, Any]) -> None:
        super().setup(config)
        self.paths = [Path(p) if Path(p).is_absolute() else ROOT / p for p in config.get("paths", ["./watched"])]
        self.recursive = bool(config.get("recursive", True))
        self.include_patterns = config.get("include_patterns", ["*"])
        self.exclude_patterns = config.get("exclude_patterns", [])
        self.max_events_per_poll = int(config.get("max_events_per_poll", 50))
        SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)

    def _load_snapshot(self) -> Dict[str, Any]:
        if SNAPSHOT_PATH.exists():
            with SNAPSHOT_PATH.open("r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_snapshot(self, snapshot: Dict[str, Any]) -> None:
        tmp = SNAPSHOT_PATH.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2)
        tmp.replace(SNAPSHOT_PATH)

    def _iter_files(self) -> Iterable[Path]:
        for base in self.paths:
            if not base.exists():
                base.mkdir(parents=True, exist_ok=True)
            iterator = base.rglob("*") if self.recursive else base.glob("*")
            for path in iterator:
                if path.is_file() and self._matches(path):
                    yield path

    def _matches(self, path: Path) -> bool:
        name = path.name
        included = any(fnmatch.fnmatch(name, pat) for pat in self.include_patterns)
        excluded = any(fnmatch.fnmatch(name, pat) for pat in self.exclude_patterns)
        return included and not excluded

    def _scan(self) -> Dict[str, Any]:
        snapshot = {}
        for path in self._iter_files():
            stat = path.stat()
            rel = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)
            snapshot[rel] = {
                "mtime": stat.st_mtime,
                "size": stat.st_size,
            }
        return snapshot

    def poll(self):
        old = self._load_snapshot()
        new = self._scan()
        events = []

        old_keys = set(old.keys())
        new_keys = set(new.keys())

        for path in sorted(new_keys - old_keys):
            events.append(AwarenessEvent(
                sensor_id=self.id,
                event_type="file_created",
                summary=f"File created: {path}",
                confidence=1.0,
                importance_hint=0.65,
                payload={"path": path, "metadata": new[path]}
            ))

        for path in sorted(old_keys - new_keys):
            events.append(AwarenessEvent(
                sensor_id=self.id,
                event_type="file_deleted",
                summary=f"File deleted: {path}",
                confidence=1.0,
                importance_hint=0.6,
                payload={"path": path, "previous_metadata": old[path]}
            ))

        for path in sorted(old_keys & new_keys):
            if old[path] != new[path]:
                events.append(AwarenessEvent(
                    sensor_id=self.id,
                    event_type="file_modified",
                    summary=f"File modified: {path}",
                    confidence=1.0,
                    importance_hint=0.55,
                    payload={"path": path, "old": old[path], "new": new[path]}
                ))

        self._save_snapshot(new)
        return events[:self.max_events_per_poll]
