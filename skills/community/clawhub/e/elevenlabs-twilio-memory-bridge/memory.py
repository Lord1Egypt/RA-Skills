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
from contextlib import ExitStack, contextmanager
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


def _lock_path(path: Path) -> Path:
    return path.with_name(path.name + ".lock")


@contextmanager
def _file_lock(path: Path, exclusive: bool = True):
    """Hold a lock on a sidecar file for *path*.

    The sidecar keeps the same inode while *path* is replaced atomically, so
    every reader and writer serializes on one lock.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(_lock_path(path), "a+", encoding="utf-8") as lockf:
        fcntl.flock(lockf, fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)
        try:
            yield
        finally:
            fcntl.flock(lockf, fcntl.LOCK_UN)


def _load_unlocked(path: Path) -> dict | list:
    if not path.exists():
        return {}
    content = path.read_text(encoding="utf-8")
    if not content.strip():
        return {}
    return json.loads(content)


def _replace_unlocked(path: Path, data: dict | list) -> None:
    tmp = path.with_suffix(".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with open(fd, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=2))
        f.flush()
        os.fsync(f.fileno())
    os.chmod(tmp, 0o600)
    tmp.replace(path)
    dir_fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(dir_fd)
    finally:
        os.close(dir_fd)


def _read_json(path: Path) -> dict | list:
    """Read and return parsed JSON from *path*, or an empty dict on failure."""
    try:
        with _file_lock(path, exclusive=False):
            return _load_unlocked(path)
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Failed to read %s: %s", path, exc)
        return {}


class StorageError(RuntimeError):
    """A data file could not be read or written, so the change was not saved."""


def _update_json(path: Path, update, default=dict):
    """Read, modify and write *path* under one exclusive lock.

    *update* mutates the loaded data in place and returns the caller's result.
    Raises ``StorageError`` without touching the file if it can't be read, so a
    damaged file is kept for recovery, or if the write fails.
    """
    with ExitStack() as stack:
        try:
            stack.enter_context(_file_lock(path))
        except OSError as exc:
            raise StorageError(f"Failed to lock {path}: {exc}") from exc
        try:
            data = _load_unlocked(path)
        except (json.JSONDecodeError, OSError) as exc:
            raise StorageError(f"Failed to read {path}: {exc}") from exc
        empty = default()
        if data == {}:
            data = empty
        if not isinstance(data, type(empty)):
            raise StorageError(
                f"{path} holds a JSON {type(data).__name__}, expected {type(empty).__name__}"
            )
        try:
            result = update(data)
        except (AttributeError, KeyError, TypeError, ValueError) as exc:
            raise StorageError(f"{path} has a malformed record: {exc!r}") from exc
        try:
            _replace_unlocked(path, data)
        except OSError as exc:
            raise StorageError(f"Failed to write {path}: {exc}") from exc
        return result


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


_FERNET_TOKEN_PREFIX = "gAAAAA"


def _decrypt(data: str) -> str:
    """Decrypt *data* with Fernet if a key is configured."""
    if not _fernet:
        return data
    if not data.startswith(_FERNET_TOKEN_PREFIX):
        # Written before encryption was enabled; Fernet tokens always carry this prefix.
        return data
    try:
        return _fernet.decrypt(data.encode("utf-8")).decode("utf-8")
    except Exception:
        logger.error("Failed to decrypt data — key mismatch or corruption")
        return "[DECRYPTION_FAILED]"


def _seal_session(session: dict) -> dict:
    """Encrypt a whole session record when a key is configured."""
    if not _fernet:
        return session
    return {"enc": _encrypt(json.dumps(session))}


def _is_sealed(value) -> bool:
    return isinstance(value, dict) and set(value) == {"enc"}


def _open_session(value) -> dict | None:
    if not _is_sealed(value):
        return value
    try:
        return json.loads(_decrypt(value["enc"]))
    except json.JSONDecodeError:
        logger.error("Failed to decrypt a session record — key mismatch or corruption")
        return None


def _encrypt_file_in_place(path: Path, encrypt_entries) -> int:
    """Encrypt plaintext entries of one JSON file under its exclusive lock.

    Errors propagate, including unreadable JSON, so startup fails rather than
    leaving plaintext behind.
    """
    if not path.exists():
        return 0
    with ExitStack() as stack:
        try:
            stack.enter_context(_file_lock(path))
        except OSError as exc:
            raise StorageError(f"Failed to lock {path}: {exc}") from exc
        try:
            data = _load_unlocked(path)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"{path} is not valid JSON, so its contents cannot be encrypted. "
                "Restore it from a backup or move it out of DATA_DIR, then restart."
            ) from exc
        if not data:
            return 0
        migrated = encrypt_entries(data)
        if migrated:
            _replace_unlocked(path, data)
        return migrated


def _encrypt_session_entries(sessions: dict) -> int:
    migrated = 0
    for key, value in sessions.items():
        if not _is_sealed(value):
            sessions[key] = _seal_session(value)
            migrated += 1
    return migrated


def _encrypt_memory_facts(memories: dict) -> int:
    migrated = 0
    for store in memories.values():
        facts = store.get("facts", [])
        for i, fact in enumerate(facts):
            if not fact.startswith(_FERNET_TOKEN_PREFIX):
                facts[i] = _encrypt(fact)
                migrated += 1
    return migrated


def _encrypt_note_entries(all_notes: list) -> int:
    migrated = 0
    for entry in all_notes:
        if not str(entry.get("note", "")).startswith(_FERNET_TOKEN_PREFIX):
            entry["note"] = _encrypt(entry["note"])
            migrated += 1
    return migrated


def encrypt_plaintext_entries() -> int:
    """Encrypt sessions, facts and notes written before encryption was enabled.

    Runs at startup when a key is configured. Values already carrying the Fernet
    prefix are left alone. Returns the number of entries encrypted; raises if a
    file cannot be read or rewritten.
    """
    if not _fernet:
        return 0
    return (
        _encrypt_file_in_place(_sessions_path(), _encrypt_session_entries)
        + _encrypt_file_in_place(_memories_path(), _encrypt_memory_facts)
        + _encrypt_file_in_place(_notes_path(), _encrypt_note_entries)
    )


def load_session(phone_hash: str) -> Session:
    """Load an existing session or create a new one for *phone_hash*.

    Returns a ``Session`` dict.  The ``call_count`` is incremented each time
    this function is called (i.e., per inbound call).
    """
    try:
        return _update_json(_sessions_path(), lambda sessions: _touch_session(sessions, phone_hash))
    except StorageError as exc:
        # The call still goes ahead, without persisted history.
        logger.error("%s; using a temporary session", exc)
        return _touch_session({}, phone_hash)


def _touch_session(sessions: dict, phone_hash: str) -> Session:
    now = time.time()
    session = _open_session(sessions.get(phone_hash)) if phone_hash in sessions else None
    unreadable = phone_hash in sessions and session is None
    if unreadable:
        logger.warning(
            "Session record for %s can't be decrypted (wrong or missing key); "
            "keeping it and using a temporary session",
            phone_hash[:8],
        )

    if session is not None:
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

    if not unreadable:
        # Leave an undecryptable record alone so restoring the right key recovers it.
        sessions[phone_hash] = _seal_session(session)
    return session


def end_session(phone_hash: str, call_sid: str) -> None:
    """Mark the session for *phone_hash* as inactive after a call ends."""

    def update(sessions: dict) -> None:
        session = _open_session(sessions.get(phone_hash))
        if session is not None:
            session["active"] = False
            session["last_call_sid"] = call_sid
            sessions[phone_hash] = _seal_session(session)

    try:
        _update_json(_sessions_path(), update)
    except StorageError as exc:
        logger.error("%s; session end not recorded", exc)


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
    stored_fact = _encrypt(fact) if _fernet else fact

    def update(memories: dict) -> list[str]:
        store = memories.setdefault(phone_hash, MemoryStore(phone_hash=phone_hash, facts=[]))
        store.setdefault("facts", []).append(stored_fact)
        return store["facts"]

    facts = _update_json(_memories_path(), update)
    logger.info("Stored fact for %s (total: %d)", phone_hash[:8], len(facts))
    return facts


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
    stored_note = _encrypt(note) if _fernet else note
    entry = Note(timestamp=time.time(), note=stored_note, phone_hash=phone_hash)
    _update_json(_notes_path(), lambda all_notes: all_notes.append(dict(entry)), default=list)
    logger.info("Added note (global=%s)", phone_hash is None)
    # Return decrypted version for display
    if _fernet:
        entry["note"] = note
    return entry
