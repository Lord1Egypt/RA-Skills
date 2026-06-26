"""JSON storage helpers for chatgpt-skill."""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from config import AUTH_INFO_FILE, CONVERSATIONS_FILE, DATA_DIR


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json_file(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception:
        return default


def save_json_file(path: Path, payload: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", delete=False, dir=str(path.parent), encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.flush()
        os.fsync(handle.fileno())
        tmp_path = Path(handle.name)
    os.replace(tmp_path, path)


class AuthInfoStore:
    def load(self) -> Dict[str, Any]:
        return load_json_file(AUTH_INFO_FILE, {})

    def save(self, payload: Dict[str, Any]):
        save_json_file(AUTH_INFO_FILE, payload)


class ConversationStore:
    def __init__(self, path: Path = CONVERSATIONS_FILE):
        self.path = path
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    def _default(self) -> Dict[str, Any]:
        return {
            "version": 1,
            "updated_at": None,
            "current_conversation_id": None,
            "last_opened": None,
            "conversations": {},
        }

    def load(self) -> Dict[str, Any]:
        payload = load_json_file(self.path, self._default())
        if not isinstance(payload, dict):
            return self._default()
        payload.setdefault("version", 1)
        payload.setdefault("updated_at", None)
        payload.setdefault("current_conversation_id", None)
        payload.setdefault("last_opened", None)
        payload.setdefault("conversations", {})
        return payload

    def save(self, payload: Dict[str, Any]):
        payload["updated_at"] = utcnow_iso()
        save_json_file(self.path, payload)

    def upsert(
        self,
        *,
        conversation_id: Optional[str],
        final_url: str,
        title: Optional[str] = None,
        status: str = "ready",
        conversation_id_source: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = self.load()
        record = {
            "conversation_id": conversation_id,
            "conversation_id_source": conversation_id_source,
            "final_url": final_url,
            "title": title,
            "status": status,
            "last_used_at": utcnow_iso(),
        }
        if conversation_id:
            existing = payload["conversations"].get(conversation_id, {})
            if not existing.get("created_at"):
                record["created_at"] = utcnow_iso()
            else:
                record["created_at"] = existing["created_at"]
            payload["conversations"][conversation_id] = {**existing, **record}
            payload["current_conversation_id"] = conversation_id
            payload["last_opened"] = payload["conversations"][conversation_id]
            saved = payload["conversations"][conversation_id]
        else:
            payload["last_opened"] = {**record, "created_at": utcnow_iso()}
            saved = payload["last_opened"]
        self.save(payload)
        return saved

    def list(self) -> List[Dict[str, Any]]:
        payload = self.load()
        records = list(payload.get("conversations", {}).values())
        records.sort(key=lambda item: item.get("last_used_at", ""), reverse=True)
        return records

    def current(self) -> Optional[Dict[str, Any]]:
        payload = self.load()
        current_id = payload.get("current_conversation_id")
        if current_id:
            return payload.get("conversations", {}).get(current_id)
        return payload.get("last_opened")

    def get(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        return self.load().get("conversations", {}).get(conversation_id)
