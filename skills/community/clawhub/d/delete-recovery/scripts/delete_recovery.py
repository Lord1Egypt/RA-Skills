#!/usr/bin/env python3
"""
delete_recovery.py - delete-recovery skill core script v0.9.0

v0.9.0 Security fixes (addressing security audit findings 2 & 3):
- Finding 2 fix: allowed_roots now defaults to [WORKSPACE_ROOT] in safe_path.py.
  safe_path.py SafePathValidator now defaults to workspace root (was previously [] meaning no restriction).
  This makes the documented default safety boundary actually enforced, restores cannot
  be redirected to arbitrary filesystem locations even when path metadata is attacker-influenced.
- Finding 3 fix: full_restore_check() now passes dest_path through to verify_integrity_and_path()
  instead of silently ignoring it. Callers using the documented single entry point were not
  validating the actual restore destination; now dest_path is fully validated.
- Finding 1 fix: --force documentation unified; only bypasses SHA256 existence check.
- Finding 4 fix: confirm-first-run token mechanism added (workspace_cleaner.py).
- Finding 5 fix: broad trigger phrases removed (SKILL.md).

v0.8.1 security fixes (addressing ASI02 risk analysis):
- workspace_cleaner default disabled (enabled=False); opt-in required
- First run requires dry-run + token confirm-first-run
- Backup failure blocks deletion (skipped_backup_failed tracking)
"""

import os
import sys
import json
import shutil
import tempfile
import hashlib
import hmac
import base64
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

# Import security validation module v0.3.0
try:
    from safe_path import SafePathValidator, SafePathError
    HAS_SAFE_PATH = True
except ImportError:
    try:
        from .safe_path import SafePathValidator, SafePathError
        HAS_SAFE_PATH = True
    except ImportError:
        HAS_SAFE_PATH = False
        SafePathError = Exception

# Workspace root: scripts/ → skill/ → skills/ → workspace/
# __file__ = C:\Users\user\.openclaw\workspace2\skills\delete-recovery\scripts\delete_recovery.py
#   .parent     = delete-recovery/scripts/
#   .parent     = delete-recovery/          (.parent.parent)
#   .parent     = skills/                           (.parent.parent.parent)
#   .parent     = workspace2/                        (.parent.parent.parent.parent)
WORKSPACE_ROOT = Path(__file__).parent.parent.parent.parent.resolve()
# Skill directory: scripts/ → skill/
SKILL_DIR = Path(__file__).parent.parent.resolve()

# All data lives under {workspace}/.delete_recovery/  (not inside the skill folder)
# This ensures backups/config survive even if the skill folder is removed
_DATA_DIR = WORKSPACE_ROOT / ".delete_recovery"
_DATA_DIR.mkdir(parents=True, exist_ok=True)
BACKUP_ROOT = _DATA_DIR / "delete_backup"
BACKUP_ROOT.mkdir(exist_ok=True)
LOG_DIR = _DATA_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
MANIFEST_FILE = BACKUP_ROOT / "manifest.jsonl"
LOG_FILE = LOG_DIR / "log.txt"

# ─── v0.6.0 Performance constants ────────────────────────────────────
# 时间触发清理间隔（小时）：两次 full cleanup 之间至少间隔这么多小时
CLEANUP_INTERVAL_HOURS = 24
# 触发 manifest 压缩的已删除条目数阈值
MANIFEST_COMPACT_THRESHOLD = 100
# 触发 manifest 压缩的文件大小阈值（字节）
MANIFEST_COMPACT_SIZE_BYTES = 100 * 1024  # 100 KB
# 定时器文件（存储上次清理时间）
_TIMER_FILE = _DATA_DIR / ".cleanup_timer"


# ─────────────────────────────────────────────────────────────────
# v0.7.0 Security hardening:
# - allowed_roots now defaults to [WORKSPACE_ROOT] — restores confined to workspace
# - manifest paths are encrypted with HMAC-SHA256 (prevents path disclosure)
# ─────────────────────────────────────────────────────────────────

# HMAC key derived from workspace root — used to hide paths in manifest
_MANIFEST_HMAC_KEY = hmac.new(
    b"delete-recovery-manifest-v1",
    str(WORKSPACE_ROOT).encode("utf-8"),
    hashlib.sha256
).digest()


def _manifest_encrypt_path(path: str) -> str:
    """
    v0.7.0: Hide original paths in manifest using HMAC-SHA256.
    Returns a Base64-encoded hash prefix + HMAC tag so paths are no longer
    readable in manifest.jsonl, while still enabling filename-based search.
    Format: HASH_PREFIX:HMAC_TAG  (both base64url, no / or +)
    """
    path_bytes = path.encode("utf-8")
    h = hmac.new(_MANIFEST_HMAC_KEY, path_bytes, hashlib.sha256)
    hmac_tag = base64.urlsafe_b64encode(h.digest()).decode("ascii").rstrip("=")
    # Store a truncated hash prefix so we can still hint at the path length/category
    full_digest = hashlib.sha256(path_bytes).digest()
    hash_prefix = base64.urlsafe_b64encode(full_digest).decode("ascii").rstrip("=")[:8]
    return f"{hash_prefix}:{hmac_tag}"


def _manifest_decrypt_path(encrypted: str) -> Optional[str]:
    """
    v0.7.0: Verify and return the original path from an encrypted manifest entry.
    Since HMAC is one-way, we can't reverse it — but we CAN verify a candidate
    path by recomputing the HMAC and comparing.
    Returns None (verification-only; original path must come from .path file at restore time).
    This function is kept for API symmetry; actual path retrieval for restore uses .path file.
    """
    return None  # HMAC is one-way; original path always from .path file on disk


# v0.7.0: allowed_roots now defaults to workspace root (restores confined to workspace)
SAFE_VALIDATOR = SafePathValidator(BACKUP_ROOT, allowed_roots=[WORKSPACE_ROOT]) if HAS_SAFE_PATH else None


# ─────────────────────────────────────────────────────────────────
# Helper: Atomic file write (for timer and manifest compaction)
# ─────────────────────────────────────────────────────────────────

def _atomic_write_text(file_path: Path, content: str, encoding: str = "utf-8") -> None:
    """
    Atomically write text to a file by writing to a temp file then renaming.
    On Windows this is atomic for files on the same filesystem.
    """
    file_path = Path(file_path)
    parent = file_path.parent
    parent.mkdir(parents=True, exist_ok=True)
    # Write to a temp file in the same directory (same filesystem → atomic rename)
    fd, tmp_path = tempfile.mkstemp(dir=str(parent), prefix=".tmp_", suffix=".atomic")
    try:
        with os.fdopen(fd, "w", encoding=encoding) as f:
            f.write(content)
        os.replace(tmp_path, file_path)  # atomic on Windows NTFS
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


# ─────────────────────────────────────────────────────────────────
# v0.6.0 方案一：时间触发清理
# ─────────────────────────────────────────────────────────────────

def _load_timer() -> dict:
    """Load last cleanup timestamps from timer file."""
    if not _TIMER_FILE.exists():
        return {"last_backup_cleanup": None, "last_log_cleanup": None}
    try:
        return json.loads(_TIMER_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"last_backup_cleanup": None, "last_log_cleanup": None}


def _save_timer(data: dict) -> None:
    """Save cleanup timestamps atomically."""
    _atomic_write_text(_TIMER_FILE, json.dumps(data, ensure_ascii=False))


def _should_run_backup_cleanup() -> bool:
    """Check if 7-day backup cleanup should run based on elapsed time."""
    timer = _load_timer()
    last = timer.get("last_backup_cleanup")
    if last is None:
        return True
    try:
        last_time = datetime.strptime(last, "%Y-%m-%d %H:%M:%S")
        elapsed = datetime.now() - last_time
        return elapsed >= timedelta(hours=CLEANUP_INTERVAL_HOURS)
    except (ValueError, TypeError):
        return True


def _should_run_log_cleanup() -> bool:
    """Check if 30-day log cleanup should run based on elapsed time."""
    timer = _load_timer()
    last = timer.get("last_log_cleanup")
    if last is None:
        return True
    try:
        last_time = datetime.strptime(last, "%Y-%m-%d %H:%M:%S")
        elapsed = datetime.now() - last_time
        return elapsed >= timedelta(hours=CLEANUP_INTERVAL_HOURS)
    except (ValueError, TypeError):
        return True


def _touch_backup_cleanup() -> None:
    """Record that a 7-day backup cleanup just ran."""
    timer = _load_timer()
    timer["last_backup_cleanup"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _save_timer(timer)


def _touch_log_cleanup() -> None:
    """Record that a 30-day log cleanup just ran."""
    timer = _load_timer()
    timer["last_log_cleanup"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _save_timer(timer)


# ─────────────────────────────────────────────────────────────────
# Manifest index (v0.5.0, optimized for v0.6.0)
# ─────────────────────────────────────────────────────────────────

def _load_manifest() -> list:
    """Load all manifest entries as a list of dicts, skipping tombstone lines."""
    if not MANIFEST_FILE.exists():
        return []
    entries = []
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                entries.append(obj)
            except json.JSONDecodeError:
                pass
    return entries


def _save_manifest(entries: list) -> None:
    """Rewrite manifest file with the given entries list atomically."""
    if not entries:
        # Fast path: empty manifest
        if MANIFEST_FILE.exists():
            MANIFEST_FILE.unlink()
        return
    content = "\n".join(json.dumps(e, ensure_ascii=False) for e in entries) + "\n"
    _atomic_write_text(MANIFEST_FILE, content)


def _append_manifest_entry(folder, safe_name, original_path, description=None):
    """
    Append a new entry to manifest.jsonl (append-only, no rewrite).
    v0.7.0: original path is now HMAC-encrypted in the 'path' field to prevent
    disclosure; 'filename' (plaintext) and 'description' (plaintext) remain searchable.
    """
    filename = Path(original_path).name
    entry = {
        "ts": datetime.now().strftime("%Y%m%d%H%M%S"),
        "folder": folder,
        "safe_name": safe_name,
        "filename": filename,
        "description": description if description else filename,
        "path": _manifest_encrypt_path(original_path),  # v0.7.0: encrypted
    }
    with open(MANIFEST_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())
    return entry


# ─── v0.6.0 方案二：manifest 增量操作 ────────────────────────────────

def _count_manifest_entries() -> tuple:
    """
    Returns (active_count, removed_count, total_size).
    Active = entries without _removed marker.
    """
    if not MANIFEST_FILE.exists():
        return 0, 0, 0
    active = 0
    removed = 0
    size = MANIFEST_FILE.stat().st_size
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if obj.get("_removed"):
                    removed += 1
                else:
                    active += 1
            except json.JSONDecodeError:
                pass
    return active, removed, size


def _compact_manifest() -> int:
    """
    Physically remove tombstone entries from manifest.jsonl.
    Returns number of entries removed.
    """
    if not MANIFEST_FILE.exists():
        return 0
    entries = _load_manifest()
    original_count = len(entries)
    surviving = [e for e in entries if not e.get("_removed")]
    removed_count = original_count - len(surviving)
    if removed_count > 0:
        _save_manifest(surviving)
    return removed_count


def _maybe_compact_manifest() -> None:
    """
    v0.6.0: Compact manifest if it exceeds size or tombstone thresholds.
    Called during non-critical commands to keep manifest lean.
    """
    active, removed, size = _count_manifest_entries()
    if removed >= MANIFEST_COMPACT_THRESHOLD or size >= MANIFEST_COMPACT_SIZE_BYTES:
        pruned = _compact_manifest()
        if pruned > 0:
            log("ManifestCompact", "CLEANUP", f"Compacted {pruned} removed entries from manifest")


def _mark_manifest_entries_removed(folder: str, safe_names: list) -> None:
    """
    Mark multiple entries as removed in manifest without rewriting entire file.
    Appends tombstone lines — actual physical removal happens in _compact_manifest().
    """
    for sn in safe_names:
        tombstone = {
            "_removed": True,
            "folder": folder,
            "safe_name": sn,
            "ts": datetime.now().strftime("%Y%m%d%H%M%S"),
        }
        with open(MANIFEST_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(tombstone, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())


def _remove_manifest_entry(folder, safe_name):
    """
    v0.6.0: Remove the entry matching (folder, safe_name) from manifest.jsonl.
    
    Strategy:
    - If total entries ≤ MANIFEST_COMPACT_THRESHOLD: load → filter → save (simple rewrite)
    - If entries > threshold: append tombstone (fast), let _maybe_compact_manifest() handle compaction later
    """
    if not MANIFEST_FILE.exists():
        return None
    
    active, removed, size = _count_manifest_entries()
    
    if active <= MANIFEST_COMPACT_THRESHOLD:
        # Small manifest: full rewrite (fast, no bloat)
        entries = _load_manifest()
        new_entries = [e for e in entries
                       if not (e.get("folder") == folder and e.get("safe_name") == safe_name)
                       and not e.get("_removed")]
        removed_entry = next(
            (e for e in entries if e.get("folder") == folder and e.get("safe_name") == safe_name),
            None
        )
        if len(new_entries) < len(entries):
            _save_manifest(new_entries)
        return removed_entry
    else:
        # Large manifest: append tombstone (O(1)), defer physical deletion
        tombstone = {
            "_removed": True,
            "folder": folder,
            "safe_name": safe_name,
            "ts": datetime.now().strftime("%Y%m%d%H%M%S"),
        }
        with open(MANIFEST_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(tombstone, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())
        # Return a dummy removed entry (caller doesn't need to distinguish)
        return {"folder": folder, "safe_name": safe_name}


def _prune_stale_manifest_entries() -> int:
    """
    Remove manifest entries whose backup folder no longer exists.
    Also removes any orphan tombstone entries for non-existent folders.
    Called during cleanup and on every script invocation.
    """
    if not MANIFEST_FILE.exists():
        return 0
    entries = _load_manifest()
    original_count = len([e for e in entries if not e.get("_removed")])
    # Keep active entries whose backup folder still exists
    surviving = [
        e for e in entries
        if not e.get("_removed") and (BACKUP_ROOT / e["folder"]).exists()
    ]
    # Also keep all tombstone entries (they don't hurt and are cleaned up by compaction)
    surviving += [e for e in entries if e.get("_removed")]
    pruned_count = original_count - len([e for e in surviving if not e.get("_removed")])
    if len(surviving) < len(entries):
        _save_manifest(surviving)
    return pruned_count


def _search_manifest(keyword: str) -> list:
    """
    Return all active manifest entries whose filename, description, or path
    contains the keyword (case-insensitive substring match).
    Tombstone (_removed) entries are excluded.
    """
    k = keyword.lower()
    return [
        e for e in _load_manifest()
        if not e.get("_removed")
        and (
            k in e.get("filename", "").lower()
            or k in e.get("description", "").lower()
            or k in e.get("path", "").lower()
        )
    ]


# ─────────────────────────────────────────────────────────────────
# Logging utilities
# ─────────────────────────────────────────────────────────────────

def cleanup_old_logs():
    """Delete logs older than 30 days. Caller must call _touch_log_cleanup() after."""
    if not LOG_FILE.exists():
        return []

    cutoff = datetime.now() - timedelta(days=30)
    deleted = []
    remaining = []

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        try:
            ts_str = line.split("] [")[0].strip("[")
            log_time = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
            if log_time >= cutoff:
                remaining.append(line)
            else:
                deleted.append(line.strip())
        except (ValueError, IndexError):
            remaining.append(line)

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.writelines(remaining)

    return deleted


def log(action, status, detail=""):
    """
    Write a log entry.
    Security: strips newlines, carriage returns, and log-format delimiters from
    detail to prevent log-injection attacks.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    level_map = {
        "SUCCESS": "INFO",
        "FAIL": "ERROR",
        "CLEANUP": "CLEANUP",
        "SECURITY": "SECURITY",
    }
    level = level_map.get(status, "INFO")
    if detail:
        detail = detail.replace("\r", "").replace("\n", "")
        detail = detail.replace("[", "")
    record = f"[{timestamp}] [{level}] [{action}] {status}"
    if detail:
        record += f" | {detail}"
    record += "\n"
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(record)


def get_timestamp():
    """Get current timestamp as folder name (YYYYMMDDHHMM)"""
    return datetime.now().strftime("%Y%m%d%H%M")


def cleanup_old_backups():
    """Delete backups older than 7 days. Caller must call _touch_backup_cleanup() after."""
    if not BACKUP_ROOT.exists():
        return []

    cutoff = datetime.now() - timedelta(days=7)
    deleted = []

    for folder in BACKUP_ROOT.iterdir():
        if folder.is_dir():
            try:
                folder_time = datetime.strptime(folder.name, "%Y%m%d%H%M")
                if folder_time < cutoff:
                    shutil.rmtree(folder)
                    deleted.append(folder.name)
                    log("AutoCleanup", "CLEANUP", f"Removed expired backup: {folder.name}")
            except ValueError:
                pass

    return deleted


def list_backups():
    """List all backups, sorted newest first"""
    if not BACKUP_ROOT.exists():
        return []

    backups = []
    for folder in sorted(BACKUP_ROOT.iterdir(), key=lambda x: x.name, reverse=True):
        if folder.is_dir():
            files = [
                f.name for f in folder.iterdir()
                if f.name not in (".restored")
                and not f.name.endswith(".path")
                and not f.name.endswith(".sha256")
            ]
            backups.append({
                "folder": folder.name,
                "time": folder.name,
                "files": files,
                "count": len(files)
            })
    return backups


# ─────────────────────────────────────────────────────────────────
# Core: backup & restore (with security validation)
# ─────────────────────────────────────────────────────────────────

def backup_file(file_path, original_path, description=None):
    """
    Back up a file to a timestamped folder.
    v0.6.0: No functional change — manifest append is already O(1).

    file_path:     Full path of the file to back up
    original_path: Original file path (used to locate target during restore)
    description:   Brief note ≤6 chars (defaults to filename)
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    timestamp = get_timestamp()
    backup_dir = BACKUP_ROOT / timestamp
    backup_dir.mkdir(exist_ok=True)

    safe_name = str(file_path).replace("/", "__").replace("\\", "__").replace(":", "")
    backup_path = backup_dir / safe_name

    shutil.copy2(file_path, backup_path)

    path_file = backup_dir / (safe_name + ".path")
    path_file.write_text(original_path, encoding="utf-8")

    sha256_file = backup_dir / (safe_name + ".sha256")
    if HAS_SAFE_PATH:
        file_hash = SafePathValidator.compute_sha256(backup_path)
        SafePathValidator.write_sha256_file(sha256_file, file_hash, original_path)
        integrity_note = f" (SHA256: {file_hash[:16]}..., PATH bound)"
    else:
        sha256_file.write_text(f"PATH:{original_path}\n", encoding="utf-8")
        integrity_note = " (safe_path.py not found, integrity check limited)"

    # v0.5.0: index in manifest (append-only, no rewrite)
    manifest_entry = _append_manifest_entry(timestamp, safe_name, original_path, description)

    log("Backup", "SUCCESS",
        f"Backed up: {original_path} -> {timestamp}/ | description: {manifest_entry['description']}"
        f" | {integrity_note}")
    return backup_dir.name, safe_name, manifest_entry["description"]


def restore_file(backup_folder, safe_name, delete_backup_after=True, force=False):
    """
    Restore a file from backup to its original location.
    v0.6.0: Uses _remove_manifest_entry() with threshold-based rewrite strategy.

    v0.3.0: Integrates full safe_path validation (integrity + path cross-check +
            allowed_roots enforcement). SHA256 record is STRICTLY REQUIRED.

    delete_backup_after: Whether to delete the backup folder after restore (default True)
    force:               Bypass SHA256 existence check (pre-v0.3.0 backups only)
    """
    backup_dir = BACKUP_ROOT / backup_folder
    if not backup_dir.exists():
        raise FileNotFoundError(f"Backup folder not found: {backup_folder}")

    backup_path = backup_dir / safe_name
    if not backup_path.exists():
        raise FileNotFoundError(f"Backup file not found: {safe_name}")

    path_file = backup_dir / (safe_name + ".path")
    if not path_file.exists():
        raise ValueError(f"Original path record not found: {safe_name}.path")

    original_path = path_file.read_text(encoding="utf-8").strip()
    dest = Path(original_path)

    sha256_file = backup_dir / (safe_name + ".sha256")

    if HAS_SAFE_PATH:
        try:
            SAFE_VALIDATOR.full_restore_check(
                backup_path=backup_path,
                sha256_file=sha256_file,
                original_path=original_path,
                dest_path=dest,
                force=force,
            )
        except SafePathError as e:
            log("Restore", "SECURITY", f"SECURITY BLOCK — {e}")
            raise SafePathError(
                f"Security validation failed, restore blocked!\n"
                f"Reason: {e}\n"
                f"If this backup was created before v0.3.0 and lacks a SHA256 record,\n"
                f"use --force to bypass the SHA256 existence check (path validation still applies)."
            ) from e

    dest.parent.mkdir(parents=True, exist_ok=True)

    if dest.exists():
        temp_dir = BACKUP_ROOT / "temp_existing"
        temp_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dest, temp_dir / dest.name)
        os.remove(dest)

    shutil.copy2(backup_path, dest)

    if delete_backup_after:
        manifest_file = backup_dir / ".restored"
        restored_set = set()
        if manifest_file.exists():
            restored_set = set(manifest_file.read_text(encoding="utf-8").strip().splitlines())
        restored_set.add(safe_name)
        manifest_file.write_text("\n".join(restored_set), encoding="utf-8")

        all_files = {
            f.name for f in backup_dir.iterdir()
            if f.name not in (".restored")
            and not f.name.endswith(".path")
            and not f.name.endswith(".sha256")
        }
        pending = all_files - restored_set

        if not pending:
            shutil.rmtree(backup_dir)
            log("Restore", "SUCCESS",
                f"All files restored from {backup_folder}, backup cleaned up")
        else:
            log("Restore", "SUCCESS",
                f"{original_path} restored, {len(pending)} file(s) still pending "
                f"in {backup_folder}, backup kept")
    else:
        log("Restore", "SUCCESS",
            f"{original_path} restored, backup {backup_folder} kept")

    # v0.6.0: remove from manifest using threshold-based strategy
    removed = _remove_manifest_entry(backup_folder, safe_name)
    manifest_note = f", removed from manifest" if removed else ", not in manifest"

    return original_path


def verify_backup(backup_folder, safe_name):
    """
    Verify backup integrity without restoring.
    v0.3.0: Reads and validates the SHA256 record format.
    """
    backup_dir = BACKUP_ROOT / backup_folder
    if not backup_dir.exists():
        raise FileNotFoundError(f"Backup folder not found: {backup_folder}")

    backup_path = backup_dir / safe_name
    if not backup_path.exists():
        raise FileNotFoundError(f"Backup file not found: {safe_name}")

    sha256_file = backup_dir / (safe_name + ".sha256")
    path_file = backup_dir / (safe_name + ".path")

    if not HAS_SAFE_PATH:
        return {
            "ok": False,
            "error": "safe_path.py not available — cannot perform integrity check",
            "integrity_check": False,
        }

    original_path = ""
    if path_file.exists():
        original_path = path_file.read_text(encoding="utf-8").strip()

    try:
        file_hash, stored_path = SafePathValidator.read_sha256_file(sha256_file)
    except SafePathError as e:
        return {
            "ok": False,
            "error": str(e),
            "integrity_check": False,
            "suggestion": "This backup may have been created before v0.3.0. "
                         "Use 'restore --force' to attempt recovery (path checks still apply).",
        }

    actual_sha256 = SafePathValidator.compute_sha256(backup_path)
    hash_match = (actual_sha256 == file_hash.lower())

    path_match = True
    path_check_done = False
    if original_path and stored_path:
        path_match = (stored_path == original_path)
        path_check_done = True

    log("Verify", "SUCCESS" if (hash_match and path_match) else "SECURITY",
        f"Integrity: {'PASS' if hash_match else 'FAIL'}, "
        f"Path cross-check: {'PASS' if path_match else 'FAIL'} "
        f"for {backup_folder}/{safe_name}")

    return {
        "ok": True,
        "hash_match": hash_match,
        "path_match": path_match if path_check_done else None,
        "path_check_done": path_check_done,
        "expected_sha256": file_hash,
        "actual_sha256": actual_sha256,
        "stored_path": stored_path if 'stored_path' in dir() else None,
        "original_path_from_pathfile": original_path or None,
        "integrity_check": hash_match,
        "backup_file": str(backup_path),
    }


def delete_backup_folder(backup_folder):
    """Delete a specific backup folder manually; also removes its manifest entries."""
    backup_dir = BACKUP_ROOT / backup_folder
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
        # v0.6.0: remove all manifest entries for this folder
        # Use tombstone approach for large manifest
        removed = _remove_manifest_entry(backup_folder, None)
        # If safe_name is None, we need to mark all entries for this folder
        # Re-load and mark all matching entries as removed
        if MANIFEST_FILE.exists():
            active, _, _ = _count_manifest_entries()
            if active <= MANIFEST_COMPACT_THRESHOLD:
                entries = _load_manifest()
                new_entries = [
                    e for e in entries
                    if e.get("folder") != backup_folder and not e.get("_removed")
                ]
                # Also collect remaining tombstones for this folder
                remaining = [
                    e for e in entries
                    if e.get("folder") != backup_folder or e.get("_removed")
                ]
                # Keep tombstones for other folders
                surviving = [e for e in remaining if not (e.get("folder") == backup_folder and e.get("_removed"))]
                if len(surviving) < len(entries):
                    _save_manifest(surviving)
            else:
                # Large manifest: mark all entries for this folder as removed
                entries = _load_manifest()
                safe_names = [
                    e["safe_name"] for e in entries
                    if e.get("folder") == backup_folder and not e.get("_removed")
                ]
                if safe_names:
                    _mark_manifest_entries_removed(backup_folder, safe_names)
        log("DeleteBackup", "SUCCESS", f"Manually deleted backup folder: {backup_folder}")
        return True
    return False


def view_log(lines=50):
    """View the last N lines of the operation log"""
    if not LOG_FILE.exists():
        return []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        all_lines = f.readlines()
    return all_lines[-lines:]


# ─────────────────────────────────────────────────────────────────
# Main entry point
# ─────────────────────────────────────────────────────────────────

def main():
    # v0.6.0 方案一：
    # - 只在每次调用时执行轻量的 manifest stale entry 清理
    # - 7天备份清理和30天日志清理改为时间触发，不在每个命令里都跑
    _prune_stale_manifest_entries()

    if len(sys.argv) < 2:
        print(json.dumps({"error": "Missing action argument"}))
        sys.exit(1)

    action = sys.argv[1]

    try:
        if action == "cleanup":
            # cleanup 命令：立即执行全量清理（不检查时间）
            deleted_backups = cleanup_old_backups()
            _touch_backup_cleanup()
            deleted_logs = cleanup_old_logs()
            _touch_log_cleanup()
            pruned = _prune_stale_manifest_entries()
            compacted = _compact_manifest()
            print(json.dumps({
                "deleted_backups": deleted_backups,
                "deleted_logs": deleted_logs,
                "pruned_manifest_entries": pruned,
                "compacted_manifest_entries": compacted,
                "backup_count": len(deleted_backups),
                "log_count": len(deleted_logs),
            }))

        elif action == "list":
            # list：触发增量压缩检查
            _maybe_compact_manifest()
            backups = list_backups()
            print(json.dumps({"backups": backups}))

        elif action == "search":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "Missing search keyword"}))
                sys.exit(1)
            # search：触发增量压缩检查（保持 manifest 搜索速度）
            _maybe_compact_manifest()
            keyword = sys.argv[2]
            results = _search_manifest(keyword)
            print(json.dumps({
                "keyword": keyword,
                "results": results,
                "count": len(results),
            }))

        elif action == "backup":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "Missing file path"}))
                sys.exit(1)
            file_path = sys.argv[2]
            original_path = sys.argv[3] if len(sys.argv) > 3 else file_path
            description = sys.argv[4] if len(sys.argv) > 4 else None
            
            # v0.6.0 方案一：backup 时判断是否需要触发备份清理
            if _should_run_backup_cleanup():
                cleanup_old_backups()
                _touch_backup_cleanup()
            if _should_run_log_cleanup():
                cleanup_old_logs()
                _touch_log_cleanup()
            
            folder, safe_name, desc = backup_file(file_path, original_path, description)
            print(json.dumps({
                "ok": True,
                "folder": folder,
                "file": safe_name,
                "description": desc,
            }))

        elif action == "restore":
            if len(sys.argv) < 4:
                print(json.dumps({"error": "Missing parameters"}))
                sys.exit(1)
            folder = sys.argv[2]
            safe_name = sys.argv[3]
            delete_backup_after = "--keep-backup" not in sys.argv
            force = "--force" in sys.argv
            restored = restore_file(folder, safe_name, delete_backup_after=delete_backup_after, force=force)
            # v0.6.0 方案二：restore 后触发增量压缩检查
            _maybe_compact_manifest()
            print(json.dumps({
                "ok": True,
                "restored_to": restored,
                "backup_deleted": delete_backup_after,
                "force_used": force,
            }))

        elif action == "delete_backup":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "Missing backup folder name"}))
                sys.exit(1)
            folder = sys.argv[2]
            deleted = delete_backup_folder(folder)
            # v0.6.0 方案二：delete_backup 后触发增量压缩检查
            _maybe_compact_manifest()
            print(json.dumps({"ok": deleted}))

        elif action == "verify":
            if len(sys.argv) < 4:
                print(json.dumps({"error": "Missing parameters"}))
                sys.exit(1)
            folder = sys.argv[2]
            safe_name = sys.argv[3]
            result = verify_backup(folder, safe_name)
            print(json.dumps(result))

        elif action == "log":
            lines = 50
            if len(sys.argv) > 2:
                try:
                    lines = int(sys.argv[2])
                except ValueError:
                    pass
            # log：触发增量压缩检查
            _maybe_compact_manifest()
            log_lines = view_log(lines)
            print(json.dumps({"log": log_lines, "count": len(log_lines)}))

        else:
            print(json.dumps({"error": f"Unknown action: {action}"}))
            sys.exit(1)

    except SafePathError as e:
        print(json.dumps({"error": str(e), "security_error": True}))
        sys.exit(1)
    except Exception as e:
        log(action if "action" in dir() else "Unknown", "FAIL", str(e))
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
