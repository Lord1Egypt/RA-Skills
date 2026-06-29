"""In-process memory and session management for the voice-agent bridge.

Stores caller sessions, long-term memory (facts), and daily notes as JSON
files under ``DATA_DIR``.  All functions are synchronous and file-backed so
the bridge can run without an external database.

Data at rest is encrypted with Fernet when ``DATA_ENCRYPTION_KEY`` is set.
"""

from __future__ import annotations

import fcntl
import json
import logging
import os
import time
from pathlib import Path
from typing import TypedDict

from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DATA_DIR: Path = Path(os.getenv("DATA_DIR", "./data"))
_DATA_ENCRYPTION_KEY: str | None = os.getenv("DATA_ENCRYPTION_KEY")
_fernet: Fernet | None = Fernet(_DATA_ENCRYPTION_KEY.encode()) if _DATA_ENCRYPTION_KEY else None


# ── Type definitions ────────────────────────────────────────────────────────


class Session(TypedDict, total=False):
    """Represents a single caller session."""

    session_id: str
    phone_hash: str
    caller_name: str
    call_count: int
    first_seen: float
    last_seen: float
    last_call_sid: str
    active: bool


class MemoryStore(TypedDict, total=False):
    """Long-term facts stored per caller."""

    phone_hash: str
    facts: list[str]


class Note(TypedDict):
    """A daily / global context note."""

    timestamp: float
    note: str
    phone_hash: str | None


# ── Helpers ─────────────────────────────────────────────────────────────────


def _sessions_path() -> Path:
    """Return the path to the sessions JSON file."""
    return DATA_DIR / "sessions.json"


def _memories_path() -> Path:
    """Return the path to the memories JSON file."""
    return DATA_DIR / "memories.json"


def _notes_path() -> Path:
    """Return the path to the notes JSON file."""
    return DATA_DIR / "notes.json"


def _read_json(path: Path) -> dict | list:
    """Read and return parsed JSON from *path*, or an empty dict on failure."""
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            # Acquire shared lock for reading
            fcntl.flock(f, fcntl.LOCK_SH)
            try:
                content = f.read()
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
        return json.loads(content)
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Failed to read %s: %s", path, exc)
        return {}


def _write_json(path: Path, data: dict | list) -> None:
    """Atomically write *data* as JSON to *path*.

    Locks the target file (not the temp) so concurrent writers serialize
    on the same lock target during the full read-modify-write cycle.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    # Ensure the target file exists so we can lock it
    path.touch(exist_ok=True)
    tmp = path.with_suffix(".tmp")
    try:
        with open(path, "a+", encoding="utf-8") as lockf:
            # Acquire exclusive lock on the target file
            fcntl.flock(lockf, fcntl.LOCK_EX)
            try:
                with open(tmp, "w", encoding="utf-8") as f:
                    f.write(json.dumps(data, indent=2))
                    f.flush()
                    os.fsync(f.fileno())
                tmp.replace(path)
                # Set restrictive permissions on the written file
                os.chmod(path, 0o600)
            finally:
                fcntl.flock(lockf, fcntl.LOCK_UN)
    except OSError as exc:
        logger.warning("Failed to write %s: %s", path, exc)


# ── Public API ──────────────────────────────────────────────────────────────


def ensure_data_dir() -> None:
    """Create the data directory tree if it does not exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    # Set restrictive permissions: owner read/write/execute only
    os.chmod(DATA_DIR, 0o700)
    logger.info("Data directory ready: %s", DATA_DIR.resolve())


def _encrypt(data: str) -> str:
    """Encrypt *data* with Fernet if a key is configured."""
    if not _fernet:
        return data
    return _fernet.encrypt(data.encode("utf-8")).decode("utf-8")


def _decrypt(data: str) -> str:
    """Decrypt *data* with Fernet if a key is configured."""
    if not _fernet:
        return data
    try:
        return _fernet.decrypt(data.encode("utf-8")).decode("utf-8")
    except Exception:
        logger.error("Failed to decrypt data — key mismatch or corruption")
        return "[DECRYPTION_FAILED]"


def load_session(phone_hash: str) -> Session:
    """Load an existing session or create a new one for *phone_hash*.

    Returns a ``Session`` dict.  The ``call_count`` is incremented each time
    this function is called (i.e., per inbound call).
    """
    sessions: dict[str, Session] = _read_json(_sessions_path())  # type: ignore[assignment]
    now = time.time()

    if phone_hash in sessions:
        session = sessions[phone_hash]
        session["call_count"] = session.get("call_count", 0) + 1
        session["last_seen"] = now
        session["active"] = True
        logger.info(
            "Returning caller %s — call #%d",
            phone_hash[:8],
            session["call_count"],
        )
    else:
        session = Session(
            session_id=f"{phone_hash[:12]}_{int(now)}",
            phone_hash=phone_hash,
            caller_name="",
            call_count=1,
            first_seen=now,
            last_seen=now,
            last_call_sid="",
            active=True,
        )
        logger.info("New caller %s", phone_hash[:8])

    sessions[phone_hash] = session
    _write_json(_sessions_path(), sessions)
    return session


def end_session(phone_hash: str, call_sid: str) -> None:
    """Mark the session for *phone_hash* as inactive after a call ends."""
    sessions: dict[str, Session] = _read_json(_sessions_path())  # type: ignore[assignment]
    if phone_hash in sessions:
        sessions[phone_hash]["active"] = False
        sessions[phone_hash]["last_call_sid"] = call_sid
        _write_json(_sessions_path(), sessions)


def get_memories(phone_hash: str) -> list[str]:
    """Return the list of stored facts for *phone_hash*."""
    memories: dict[str, MemoryStore] = _read_json(_memories_path())  # type: ignore[assignment]
    store = memories.get(phone_hash, {})
    facts = store.get("facts", [])
    # Decrypt facts if encryption is enabled
    if _fernet:
        decrypted = []
        for fact in facts:
            try:
                decrypted.append(_decrypt(fact))
            except Exception:
                # Fallback: fact was stored unencrypted
                decrypted.append(fact)
        return decrypted
    return facts


def add_memory(phone_hash: str, fact: str) -> list[str]:
    """Append *fact* to long-term memory for *phone_hash*.

    Returns the updated list of facts.
    """
    memories: dict[str, MemoryStore] = _read_json(_memories_path())  # type: ignore[assignment]
    if phone_hash not in memories:
        memories[phone_hash] = MemoryStore(phone_hash=phone_hash, facts=[])
    # Encrypt fact if encryption is enabled
    stored_fact = _encrypt(fact) if _fernet else fact
    memories[phone_hash].setdefault("facts", []).append(stored_fact)
    _write_json(_memories_path(), memories)
    logger.info("Stored fact for %s (total: %d)", phone_hash[:8], len(memories[phone_hash]["facts"]))
    return memories[phone_hash]["facts"]


def get_notes(phone_hash: str | None = None) -> list[Note]:
    """Return notes, optionally filtered by *phone_hash*.

    Global notes (``phone_hash is None``) are always included.
    """
    all_notes: list[Note] = _read_json(_notes_path()) or []  # type: ignore[assignment]
    notes = [
        n
        for n in all_notes
        if n.get("phone_hash") is None or n.get("phone_hash") == phone_hash
    ]
    # Decrypt note content if encryption is enabled
    if _fernet:
        for note in notes:
            if "note" in note:
                note["note"] = _decrypt(note["note"])
    return notes


def add_note(note: str, phone_hash: str | None = None) -> Note:
    """Create a new note and persist it.

    If *phone_hash* is provided the note is scoped to that caller; otherwise
    it is a global/daily note visible to all callers.
    """
    all_notes: list[Note] = _read_json(_notes_path()) or []  # type: ignore[assignment]
    # Encrypt note content if encryption is enabled
    stored_note = _encrypt(note) if _fernet else note
    entry = Note(timestamp=time.time(), note=stored_note, phone_hash=phone_hash)
    all_notes.append(entry)
    _write_json(_notes_path(), all_notes)
    logger.info("Added note (global=%s)", phone_hash is None)
    # Return decrypted version for display
    if _fernet:
        entry["note"] = note
    return entry
