"""
Idempotency support for state-changing ClawTrader commands.

The daemon uses this module as an at-most-once request journal.  A request
without an explicit key receives a deterministic key derived from its
canonical payload, so retrying the same command cannot create a second
side effect.  The journal is persisted atomically because a process restart
must not turn a timed-out order request into a duplicate order.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import threading
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


# Commands below can change broker state, daemon state, or local scheduled
# state.  Queries and event polling intentionally remain uncached.
MUTATING_COMMANDS = frozenset(
    {
        "stop",
        "subscribe",
        "unsubscribe",
        "order",
        "cancel",
        "cancel_all",
        "add_alert",
        "remove_alert",
        "add_schedule",
        "remove_schedule",
    }
)


def is_mutating_command(command: str) -> bool:
    return command in MUTATING_COMMANDS


def _normalise(value: Any) -> Any:
    """Return a JSON-safe, deterministic representation of a request."""
    if isinstance(value, dict):
        return {
            str(key): _normalise(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
            if key != "idempotency_key"
        }
    if isinstance(value, (list, tuple)):
        return [_normalise(item) for item in value]
    if isinstance(value, float):
        # JSON's representation is stable for the finite values accepted by
        # the CLI and avoids treating 1 and 1.0 as different requests.
        return float(value)
    return value


def canonical_request(command: Dict[str, Any]) -> str:
    """Canonical request payload used for fingerprints and derived keys."""
    normalised = _normalise(command)
    # Subscription order is not semantically meaningful.  Canonicalising it
    # prevents "IF2505,rb2510" and "rb2510,IF2505" from creating two writes.
    if isinstance(normalised, dict) and normalised.get("cmd") in {
        "subscribe",
        "unsubscribe",
    }:
        raw = normalised.get("instruments", "")
        if isinstance(raw, str):
            instruments = sorted({part.strip() for part in raw.split(",") if part.strip()})
            normalised["instruments"] = ",".join(instruments)
    return json.dumps(
        normalised,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def request_fingerprint(command: Dict[str, Any]) -> str:
    payload = canonical_request(command).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def request_key(command: Dict[str, Any]) -> str:
    supplied = str(command.get("idempotency_key") or "").strip()
    if supplied:
        return "explicit:" + supplied
    return "derived:" + request_fingerprint(command)


class IdempotencyConflict(ValueError):
    """Raised when one key is reused for a different request payload."""


class IdempotencyStore:
    """Small durable request journal for local daemon writes.

    Records are written before the side effect is attempted.  A record left
    in ``pending`` state after a crash is deliberately not retried: for a
    real order, the external system may have accepted the request even when
    the local process did not receive a response.  The caller must reconcile
    broker state before intentionally issuing a new request key.
    """

    def __init__(self, path: Path, max_records: Optional[int] = None):
        self._path = Path(path)
        self._max_records = max_records
        self._lock = threading.RLock()
        self._records: Dict[str, Dict[str, Any]] = self._load()

    def _load(self) -> Dict[str, Dict[str, Any]]:
        try:
            raw = self._path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return {}
        except OSError as exc:
            raise RuntimeError(f"无法读取幂等日志: {self._path}") from exc
        try:
            data = json.loads(raw)
        except (ValueError, TypeError) as exc:
            raise RuntimeError(f"幂等日志损坏，拒绝执行写操作: {self._path}") from exc
        if not isinstance(data, dict):
            raise RuntimeError(f"幂等日志格式无效，拒绝执行写操作: {self._path}")
        records = data.get("records", data)
        if not isinstance(records, dict):
            raise RuntimeError(f"幂等日志记录无效，拒绝执行写操作: {self._path}")
        parsed: Dict[str, Dict[str, Any]] = {}
        for key, value in records.items():
            if not isinstance(value, dict) or not isinstance(value.get("fingerprint"), str):
                raise RuntimeError(f"幂等日志记录损坏，拒绝执行写操作: {self._path}")
            status = value.get("status")
            if status not in {"pending", "completed"}:
                raise RuntimeError(f"幂等日志状态无效，拒绝执行写操作: {self._path}")
            if status == "completed" and not isinstance(value.get("response"), dict):
                raise RuntimeError(f"幂等日志响应损坏，拒绝执行写操作: {self._path}")
            parsed[str(key)] = value
        return parsed

    def _flush(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"version": 1, "records": self._records}
        fd, temp_name = tempfile.mkstemp(
            prefix=self._path.name + ".",
            suffix=".tmp",
            dir=str(self._path.parent),
        )
        try:
            os.fchmod(fd, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, ensure_ascii=False, indent=2)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_name, self._path)
        finally:
            try:
                os.unlink(temp_name)
            except FileNotFoundError:
                pass

    def begin(self, command: Dict[str, Any]) -> Tuple[str, Optional[Dict[str, Any]]]:
        """Reserve a request key.

        Returns ``(key, record)``.  ``record`` is ``None`` for a new request;
        an existing completed/pending record is returned for a replay.  A key
        reused with a different payload raises :class:`IdempotencyConflict`.
        """
        key = request_key(command)
        fingerprint = request_fingerprint(command)
        now = time.time()
        with self._lock:
            existing = self._records.get(key)
            if existing is not None:
                if existing.get("fingerprint") != fingerprint:
                    raise IdempotencyConflict(
                        f"幂等键已用于另一条请求: {key}"
                    )
                existing["last_seen"] = now
                self._flush()
                return key, dict(existing)

            self._records[key] = {
                "fingerprint": fingerprint,
                "status": "pending",
                "created_at": now,
                "last_seen": now,
            }
            self._trim_completed()
            self._flush()
            return key, None

    def complete(self, key: str, response: Dict[str, Any]) -> None:
        with self._lock:
            record = self._records.get(key)
            if record is None:
                return
            record["status"] = "completed"
            record["response"] = response
            record["last_seen"] = time.time()
            self._flush()

    def _trim_completed(self) -> None:
        # The default journal is unbounded: evicting an old key could turn a
        # late retry into a second broker mutation.  A bounded journal remains
        # available for deployments that explicitly accept that trade-off.
        if self._max_records is None:
            return
        if len(self._records) <= self._max_records:
            return
        completed = sorted(
            (
                (float(record.get("last_seen", 0)), key)
                for key, record in self._records.items()
                if record.get("status") == "completed"
            ),
            key=lambda item: item[0],
        )
        remove_count = len(self._records) - self._max_records
        for _, key in completed[:remove_count]:
            self._records.pop(key, None)


def replay_response(key: str, record: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a journal record into a safe API response."""
    if record.get("status") == "completed" and isinstance(record.get("response"), dict):
        response = dict(record["response"])
        response["idempotent_replay"] = True
        response["idempotency_key"] = key
        return response
    return {
        "ok": False,
        "error": "幂等请求正在执行或上次执行状态未知，请先查询状态后再使用新的请求键",
        "idempotent_replay": True,
        "idempotency_key": key,
    }
