#!/usr/bin/env python3
"""
workspace_cleaner.py — delete-recovery skill extension v0.11.0

v0.11.0 security fixes (addressing new security audit findings 1 & 2):
  - new-Finding (97%): Cleanup scope narrowed — only temp-pattern files (`_is_temp_file()`
    and `_is_temp_dir()`) are deletion candidates. Non-temp files are always skipped
    regardless of age, preventing accidental deletion of valuable workspace content.
  - new-Finding (96%): Chinese triggers '临时文件清理' and '自动清理' removed from SKILL.md;
    only `workspace_cleaner` explicitly activates workspace cleanup.

v0.9.0 security fixes (addressing security audit findings 4 & 5):
  - Finding 4 fix: confirm_first_run() now requires a prior dry-run to have been
    executed. A dry_run_token is generated on each dry-run and must be presented
    at confirm-first-run time, preventing the bypass where cleanup could be enabled
    without ever reviewing the dry-run preview.
  - Finding 5 fix: Overly broad trigger phrases removed from SKILL.md.
    Only specific, unambiguous triggers like 'workspace_cleaner' remain active.
    Generic housekeeping phrases like 'clean workspace' or '定时清理' no longer
    auto-activate deletion-oriented behaviour.

v0.8.1 security fixes (addressing ASI02 risk analysis):
  - workspace_cleaner 默认 disabled（enabled=False），需显式 opt-in
  - 首次运行必须先 dry-run 预览并 confirm-first-run 确认
  - 备份失败时阻断删除：backup_failed_skipped 错误类型，文件不被删除
  - 新增 enable / disable / confirm-first-run 命令

定时清理 workspace 下的临时文件和过期文件，被删除的文件自动备份到 delete_backup/。
支持白名单配置，白名单内的文件/文件夹不会被清理。

功能特性：
- 每 24 小时自动运行一次（时间触发）
- 支持文件扩展名、文件名、文件夹名白名单
- 删除前自动备份到 delete_backup/（复用 delete_recovery.py）
- 支持手动触发清理（python workspace_cleaner.py run）
- 配置通过 workspace_cleaner_whitelist.json 管理

文件结构：
{workspace}/
├── workspace_cleaner_whitelist.json   ← 白名单配置（用户编辑）
├── workspace_cleaner_config.json       ← 运行配置（自动管理）
└── skills/delete-recovery/scripts/
    ├── delete_recovery.py              ← 核心备份恢复脚本
    └── workspace_cleaner.py            ← 本脚本

用法：
    python workspace_cleaner.py run              # 手动触发一次清理
    python workspace_cleaner.py show-whitelist   # 查看当前白名单
    python workspace_cleaner.py add-whitelist <path> [--type file|folder|ext]  # 添加白名单项
    python workspace_cleaner.py remove-whitelist <path>  # 移除白名单项
    python workspace_cleaner.py set-interval <hours>     # 设置清理间隔（小时）
    python workspace_cleaner.py set-expire-days <days>   # 设置过期天数
    python workspace_cleaner.py dry-run                   # 预览哪些文件会被删除（不实际删除）
    python workspace_cleaner.py status                   # 查看定时器状态
"""

import os
import sys
import json
import shutil
import tempfile
import hashlib
import hmac
import base64
import subprocess
import secrets
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

# ─── Paths ────────────────────────────────────────────────────────────────────
# Workspace root: scripts/ → skill/ → skills/ → workspace2/
# __file__ = C:\Users\user\.openclaw\workspace2\skills\delete-recovery\scripts\workspace_cleaner.py
#   .parent     = delete-recovery/scripts/
#   .parent     = delete-recovery/          (.parent.parent)
#   .parent     = skills/                           (.parent.parent.parent)
#   .parent     = workspace2/                        (.parent.parent.parent.parent)
WORKSPACE_ROOT = Path(__file__).parent.parent.parent.parent.resolve()
SKILL_DIR = Path(__file__).parent.parent.resolve()
SCRIPTS_DIR = Path(__file__).parent.resolve()
DELETE_RECOVERY_SCRIPT = SCRIPTS_DIR / "delete_recovery.py"

# All data lives under {workspace}/.delete_recovery/
_DATA_DIR = WORKSPACE_ROOT / ".delete_recovery"
_DATA_DIR.mkdir(parents=True, exist_ok=True)

BACKUP_ROOT = _DATA_DIR / "delete_backup"
_EXTENSION_DIR = _DATA_DIR / "workspace_cleaner"
_EXTENSION_DIR.mkdir(parents=True, exist_ok=True)

WHITELIST_FILE = _EXTENSION_DIR / "workspace_cleaner_whitelist.json"
CONFIG_FILE = _EXTENSION_DIR / "workspace_cleaner_config.json"
TIMER_FILE = _EXTENSION_DIR / "workspace_cleaner_timer.json"
DRYRUN_TOKEN_FILE = _EXTENSION_DIR / ".dry_run_token"  # v0.9.0: per-session token

# ─── Default config ───────────────────────────────────────────────────────────
DEFAULT_INTERVAL_HOURS = 24
DEFAULT_EXPIRE_DAYS = 7

# ─── Built-in always-protected paths (hardcoded — cannot be overridden) ─────────
ALWAYS_PROTECTED = {
    "AGENTS.md", "SOUL.md", "TOOLS.md", "IDENTITY.md", "USER.md",
    "HEARTBEAT.md", "BOOTSTRAP.md",
    "skills", ".learnings",
    "workspace_cleaner_whitelist.json",
    "workspace_cleaner_config.json",
    "workspace_cleaner_timer.json",
    ".cleanup_timer",
    ".delete_recovery",   # protect the entire data directory
}

# ─── Default whitelist (applied if whitelist file doesn't exist) ────────────────
DEFAULT_WHITELIST = {
    "files":  [],   # exact filenames to protect, e.g. ["good.py", "README.md"]
    "folders": [],  # folder names to protect, e.g. ["log", "temp"]
    "exts":   [],   # extensions to protect, e.g. [".xlsx", ".docx"]
}


# ─── Config helpers ────────────────────────────────────────────────────────────

def _default_config() -> dict:
    return {
        "workspace": str(WORKSPACE_ROOT),
        "interval_hours": DEFAULT_INTERVAL_HOURS,
        "expire_days": DEFAULT_EXPIRE_DAYS,
        "auto_backup": True,
        "last_cleanup": None,
        # v0.8.1: disabled by default — must opt-in explicitly
        "enabled": False,
        # v0.8.1: first run requires dry-run confirmation gate
        "first_run_confirmed": False,
    }


def _load_config() -> dict:
    if not CONFIG_FILE.exists():
        return _default_config()
    try:
        cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        # v0.8.1: ensure new keys exist even when upgrading from older config
        for k, v in _default_config().items():
            cfg.setdefault(k, v)
        return cfg
    except (json.JSONDecodeError, OSError):
        return _default_config()


def _save_config(cfg: dict) -> None:
    CONFIG_FILE.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")


def _atomic_write(file_path: Path, content: str) -> None:
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(file_path.parent), prefix=".tmp_", suffix=".atomic")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp, file_path)
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def _load_whitelist() -> dict:
    """Load whitelist from JSON file, return DEFAULT_WHITELIST if missing."""
    if not WHITELIST_FILE.exists():
        return dict(DEFAULT_WHITELIST)
    try:
        w = json.loads(WHITELIST_FILE.read_text(encoding="utf-8"))
        return {
            "files":   list(w.get("files",   DEFAULT_WHITELIST["files"])),
            "folders": list(w.get("folders", DEFAULT_WHITELIST["folders"])),
            "exts":    list(w.get("exts",    DEFAULT_WHITELIST["exts"])),
        }
    except (json.JSONDecodeError, OSError):
        return dict(DEFAULT_WHITELIST)


def _save_whitelist(wl: dict) -> None:
    content = json.dumps(wl, ensure_ascii=False, indent=2)
    _atomic_write(WHITELIST_FILE, content)


def _load_timer() -> dict:
    if not TIMER_FILE.exists():
        return {"last_run": None}
    try:
        return json.loads(TIMER_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"last_run": None}


def _save_timer(data: dict) -> None:
    _atomic_write(TIMER_FILE, json.dumps(data, ensure_ascii=False, indent=2))


def _should_run() -> bool:
    """Check if enough time has passed since last cleanup."""
    cfg = _load_config()
    timer = _load_timer()
    last = timer.get("last_run")
    if last is None:
        return True
    try:
        last_time = datetime.strptime(last, "%Y-%m-%d %H:%M:%S")
        elapsed = datetime.now() - last_time
        return elapsed >= timedelta(hours=cfg.get("interval_hours", DEFAULT_INTERVAL_HOURS))
    except (ValueError, TypeError):
        return True


def _is_enabled() -> bool:
    """Check if workspace_cleaner is explicitly enabled (v0.8.1+)."""
    cfg = _load_config()
    return cfg.get("enabled", False)


def _is_first_run_confirmed() -> bool:
    """Check if the first-run dry-run confirmation gate has been passed."""
    cfg = _load_config()
    return cfg.get("first_run_confirmed", False)


# ─── v0.9.0: dry-run token mechanism ──────────────────────────────────────────
# Finding 4 fix: confirm_first_run() must verify a dry-run was actually executed.
# Each dry-run generates a cryptographically random token stored to DRYRUN_TOKEN_FILE.
# confirm-first-run requires a matching token. Tokens expire after 24 hours.

def _generate_dry_run_token() -> str:
    """Generate and persist a dry-run token, return the token string."""
    token = secrets.token_hex(16)
    DRYRUN_TOKEN_FILE.write_text(json.dumps({
        "token": token,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "used": False,
    }, ensure_ascii=False), encoding="utf-8")
    return token


def _consume_dry_run_token(token: str) -> bool:
    """
    Validate and consume a dry-run token.
    Returns True if token is valid, un-used, and not expired (24h).
    On success, marks the token as used.
    Returns False if token is missing, already used, or expired.
    """
    if not DRYRUN_TOKEN_FILE.exists():
        return False
    try:
        data = json.loads(DRYRUN_TOKEN_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False

    stored_token = data.get("token", "")
    created_str = data.get("created", "")
    used = data.get("used", False)

    if stored_token != token:
        return False
    if used:
        return False  # already consumed

    # Check expiry (24 hours)
    if created_str:
        try:
            created_time = datetime.strptime(created_str, "%Y-%m-%d %H:%M:%S")
            if datetime.now() - created_time > timedelta(hours=24):
                return False  # expired
        except (ValueError, TypeError):
            return False

    # Mark as used
    data["used"] = True
    DRYRUN_TOKEN_FILE.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return True


def _peek_dry_run_token() -> Optional[str]:
    """Return the current valid token if one exists and is un-used, else None."""
    if not DRYRUN_TOKEN_FILE.exists():
        return None
    try:
        data = json.loads(DRYRUN_TOKEN_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    token = data.get("token", "")
    used = data.get("used", False)
    created_str = data.get("created", "")

    if not token or used:
        return None
    # Check expiry
    if created_str:
        try:
            created_time = datetime.strptime(created_str, "%Y-%m-%d %H:%M:%S")
            if datetime.now() - created_time > timedelta(hours=24):
                return None
        except (ValueError, TypeError):
            return None
    return token


# ─── Whitelist matching ────────────────────────────────────────────────────────

def _is_whitelisted(rel_path: str, wl: dict) -> bool:
    """
    Returns True if rel_path is protected by the whitelist.
    rel_path: relative path from workspace root (e.g. "log/test.txt" or "temp/")
    """
    name = Path(rel_path).name
    parent = str(Path(rel_path).parent)

    # 1. Exact filename match
    if name in wl.get("files", []):
        return True
    # 2. Folder name match (if path refers to a directory or parent dir matches)
    for folder in wl.get("folders", []):
        if folder in parent.split(os.sep) or folder in rel_path.split(os.sep):
            return True
    # 3. Extension match
    for ext in wl.get("exts", []):
        if name.endswith(ext):
            return True
    return False


def _is_always_protected(name: str) -> bool:
    """Check against hardcoded always-protected list."""
    return name in ALWAYS_PROTECTED


def _is_temp_file(name: str) -> bool:
    """Check if filename looks like a common temp file pattern."""
    temp_patterns = [
        ".tmp", ".temp", ".bak", ".backup",
        "~", ".swp", ".swo", ".cache",
        "__pycache__",
        ".pyc", ".pyo",
        ".DS_Store", "Thumbs.db",
        "._", ".goutputstream",
    ]
    name_lower = name.lower()
    for p in temp_patterns:
        if name_lower == p.lower() or name_lower.endswith(p.lower()):
            return True
    return False


def _is_temp_dir(name: str) -> bool:
    """Check if directory name looks like a temp/cache directory."""
    name_lower = name.lower()
    # Only treat __pycache__, .pytest_cache, etc. as temp dirs
    temp_only = ["__pycache__", ".pytest_cache", ".mypy_cache", ".nox"]
    for d in temp_only:
        if name_lower == d.lower():
            return True
    if name_lower.endswith(".pyc") or name_lower.endswith(".pyo"):
        return True
    return False


# ─── Backup via delete_recovery.py ───────────────────────────────────────────

def _backup_file_using_delete_recovery(file_path: Path, original_path_str: str) -> bool:
    """
    Use the existing delete_recovery.py to back up a file before deletion.
    Returns True if backup succeeded, False otherwise.
    """
    if not DELETE_RECOVERY_SCRIPT.exists():
        return False
    try:
        encoded = str(file_path).replace("\\", "/")
        original = original_path_str.replace("\\", "/")
        result = subprocess.run(
            [sys.executable, str(DELETE_RECOVERY_SCRIPT),
             "backup", encoded, original, "workspace_cleaner"],
            capture_output=True, text=True, timeout=60,
            cwd=str(WORKSPACE_ROOT),
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, OSError):
        return False


# ─── Core cleanup logic ────────────────────────────────────────────────────────

def _scan_workspace(workspace: Path, wl: dict, expire_days: int) -> dict:
    """
    Scan workspace and return files eligible for cleanup.
    Returns {"files": [(rel_path, mtime_ts), ...], "skipped": [reasons...]}
    """
    cutoff = datetime.now() - timedelta(days=expire_days)
    candidates = []
    skipped_reasons = {"protected": [], "whitelisted": [], "recent": [], "errors": []}

    try:
        for root, dirs, files in os.walk(workspace):
            root_path = Path(root)
            rel_root = root_path.relative_to(workspace)

            rel_str = str(rel_root).replace("\\", "/")
            if rel_root.name and (_is_always_protected(rel_root.name) or _is_whitelisted(rel_str, wl)):
                dirs[:] = []
                skipped_reasons["protected"].append(str(rel_root))
                continue

            for d in dirs[:]:
                rel_d = f"{rel_str}/{d}" if rel_str else d
                if _is_always_protected(d) or _is_whitelisted(rel_d, wl):
                    dirs.remove(d)
                    skipped_reasons["protected"].append(rel_d)
                    continue
                if _is_temp_dir(d):
                    try:
                        dir_path = root_path / d
                        mtime = datetime.fromtimestamp(dir_path.stat().st_mtime)
                        if mtime < cutoff:
                            candidates.append((rel_d, dir_path.stat().st_mtime))
                            dirs.remove(d)
                        else:
                            skipped_reasons["recent"].append(rel_d)
                            dirs.remove(d)
                    except OSError:
                        dirs.remove(d)
                    continue

            for fname in files:
                file_path = root_path / fname
                rel_path_obj = file_path.relative_to(workspace)
                rel_str = str(rel_path_obj).replace("\\", "/")

                if _is_always_protected(fname):
                    skipped_reasons["protected"].append(rel_str)
                    continue
                if _is_whitelisted(rel_str, wl):
                    skipped_reasons["whitelisted"].append(rel_str)
                    continue
                if _is_temp_file(fname):
                    try:
                        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                        if mtime < cutoff:
                            candidates.append((rel_str, file_path.stat().st_mtime))
                        else:
                            skipped_reasons["recent"].append(rel_str)
                    except OSError:
                        pass
                    continue

                # v0.11.0 fix (security audit Finding new1, 97% confidence):
                # ONLY temp-pattern files are eligible for cleanup.
                # Non-temp files (even if old) are NOT deleted — they are skipped.
                # Users may keep valuable old files in the workspace; the cleaner
                # must NOT delete them just because they are past expire_days.
                try:
                    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if mtime < cutoff:
                        skipped_reasons["recent"].append(rel_str)
                    else:
                        skipped_reasons["recent"].append(rel_str)
                except OSError:
                    skipped_reasons["errors"].append(rel_str)
    except PermissionError as e:
        skipped_reasons["errors"].append(f"PermissionError: {e}")

    return {"files": candidates, "skipped": skipped_reasons}


def run_cleanup(dry_run: bool = False, force: bool = False) -> dict:
    """
    Main cleanup entrypoint.

    dry_run: if True, scan and return what would be deleted without deleting
    force:   if True, ignore the 24-hour timer and run immediately

    v0.11.0 security gates:
      - enabled flag must be True (opt-in by default)
      - first_run_confirmed must be True unless force=True (first run requires dry-run confirmation)
      - v0.11.0: a valid dry-run token is required for first_run_confirmed
      - backup failure BLOCKS deletion (files are NOT deleted if backup fails)
      - v0.11.0: ONLY temp-pattern files are deletion candidates; non-temp files are skipped

    Returns dict with stats.
    """
    cfg = _load_config()
    wl = _load_whitelist()
    workspace = Path(cfg.get("workspace", str(WORKSPACE_ROOT)))

    # v0.9.0: on dry-run, generate a fresh token so confirm-first-run can verify it
    if dry_run:
        token = _generate_dry_run_token()
        result = _scan_workspace(workspace, wl, cfg.get("expire_days", DEFAULT_EXPIRE_DAYS))
        candidates = result["files"]
        skipped = result["skipped"]
        return {
            "ok": True,
            "dry_run": True,
            "dry_run_token": token,
            "dry_run_token_expires_hours": 24,
            "candidates": sorted(candidates, key=lambda x: x[1]),
            "skipped": skipped,
            "candidate_count": len(candidates),
            "expire_days": cfg.get("expire_days", DEFAULT_EXPIRE_DAYS),
            "workspace": str(workspace),
            "enabled": cfg.get("enabled", False),
            "first_run_confirmed": cfg.get("first_run_confirmed", False),
            "message": (
                "dry-run 预览完成。请核对将被清理的文件列表，"
                "然后使用 confirm-first-run <token> 命令确认启用清理功能。"
            ),
        }

    # v0.8.1: require explicit opt-in
    if not cfg.get("enabled", False) and not force:
        return {
            "ok": False,
            "reason": "not_enabled",
            "message": (
                "workspace_cleaner 默认禁用（enabled=False）。"
                "请先运行 `python workspace_cleaner.py dry-run` 预览清理范围，"
                "然后用 `python workspace_cleaner.py confirm-first-run <token>` 确认启用。"
            ),
            "hint": "用 `python workspace_cleaner.py enable` 启用定时清理功能。",
        }

    # v0.8.1: first-run gate — must see dry-run results before first actual cleanup
    if not cfg.get("first_run_confirmed", False) and not force:
        return {
            "ok": False,
            "reason": "first_run_not_confirmed",
            "message": (
                "首次运行前必须先执行 dry-run 并确认。"
                "请先运行 `python workspace_cleaner.py dry-run` 查看哪些文件将被清理，"
                "然后用 `python workspace_cleaner.py confirm-first-run <token>` 确认开始清理。"
            ),
        }

    if not force and not _should_run():
        timer = _load_timer()
        return {
            "ok": False,
            "reason": "timer_not_due",
            "message": "清理尚未到时间间隔，上次运行: "
                       f"{timer.get('last_run', '从未')}",
            "interval_hours": cfg.get("interval_hours", DEFAULT_INTERVAL_HOURS),
        }

    expire_days = cfg.get("expire_days", DEFAULT_EXPIRE_DAYS)
    result = _scan_workspace(workspace, wl, expire_days)
    candidates = result["files"]
    skipped = result["skipped"]

    deleted = []
    errors = []
    backed_up = []
    skipped_backup_failed = []

    for rel_str, mtime in candidates:
        file_path = workspace / rel_str
        if not file_path.exists():
            continue
        if _is_always_protected(file_path.name):
            continue
        if _is_whitelisted(rel_str, wl):
            skipped["whitelisted"].append(rel_str)
            continue

        original_path_str = str(file_path.resolve())

        # v0.8.1: backup is MANDATORY — failure blocks deletion entirely
        backup_ok = False
        if cfg.get("auto_backup", True):
            backup_ok = _backup_file_using_delete_recovery(file_path, original_path_str)
            if not backup_ok:
                backup_ok = _manual_backup(file_path, rel_str)

        if not backup_ok:
            skipped_backup_failed.append(rel_str)
            errors.append({
                "file": rel_str,
                "error": "backup_failed_skipped",
                "detail": "备份失败，拒绝删除该文件。请手动检查 backup 机制。"
            })
            continue

        backed_up.append(rel_str)

        try:
            if file_path.is_dir():
                shutil.rmtree(file_path)
            else:
                file_path.unlink()
            deleted.append(rel_str)
        except OSError as e:
            errors.append({"file": rel_str, "error": str(e)})

    # Update timer
    _save_timer({"last_run": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

    return {
        "ok": True,
        "dry_run": False,
        "deleted": deleted,
        "backed_up": backed_up,
        "errors": errors,
        "skipped_backup_failed": skipped_backup_failed,
        "skipped": skipped,
        "deleted_count": len(deleted),
        "backed_up_count": len(backed_up),
        "skipped_backup_failed_count": len(skipped_backup_failed),
        "expire_days": expire_days,
        "workspace": str(workspace),
        "run_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def _manual_backup(src: Path, rel_str: str) -> bool:
    """
    v0.11.0: Fixed to handle directories (Finding newB, 91% confidence).

    Fallback: manually copy file or directory to delete_backup/timestamp/ when
    delete_recovery.py is unavailable or fails. Mirrors the backup format.

    For files: uses shutil.copy2 with SHA256 + .path record.
    For directories: uses shutil.copytree, records only .path (no SHA256 for dirs).
    If any step fails, returns False — the file/dir will NOT be deleted.
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_dir = BACKUP_ROOT / timestamp
        backup_dir.mkdir(exist_ok=True)
        safe_name = rel_str.replace("/", "__").replace("\\", "__").replace(":", "")
        dest = backup_dir / safe_name

        if src.is_dir():
            # Directory backup: copytree preserves structure
            shutil.copytree(src, dest)
            path_file = backup_dir / (safe_name + ".path")
            path_file.write_text(str(src.resolve()), encoding="utf-8")
            # No SHA256 for directories (not a file)
            return True
        else:
            # File backup: copy2 + SHA256 + path record
            shutil.copy2(src, dest)
            path_file = backup_dir / (safe_name + ".path")
            path_file.write_text(str(src.resolve()), encoding="utf-8")
            h = hashlib.sha256()
            with open(src, "rb") as f_read:
                for chunk in iter(lambda: f_read.read(8192), b""):
                    h.update(chunk)
            sha256_file = backup_dir / (safe_name + ".sha256")
            sha256_file.write_text(
                f"SHA256:{h.hexdigest()}\nPATH:{src.resolve()}\n",
                encoding="utf-8"
            )
            return True
    except Exception:
        return False


# ─── Whitelist management ─────────────────────────────────────────────────────

def show_whitelist() -> dict:
    wl = _load_whitelist()
    return {
        "ok": True,
        "whitelist": wl,
        "protected_always": sorted(ALWAYS_PROTECTED),
        "whitelist_file": str(WHITELIST_FILE),
        "config_file": str(CONFIG_FILE),
        "timer_file": str(TIMER_FILE),
        "extension_dir": str(_EXTENSION_DIR),
    }


def add_whitelist_entry(path: str, entry_type: str = "file") -> dict:
    wl = _load_whitelist()
    if entry_type == "file":
        if path not in wl["files"]:
            wl["files"].append(path)
    elif entry_type == "folder":
        if path not in wl["folders"]:
            wl["folders"].append(path)
    elif entry_type == "ext":
        if not path.startswith("."):
            path = "." + path
        if path not in wl["exts"]:
            wl["exts"].append(path)
    else:
        return {"ok": False, "error": f"Unknown entry_type: {entry_type}"}
    _save_whitelist(wl)
    return {"ok": True, "whitelist": wl}


def remove_whitelist_entry(path: str) -> dict:
    wl = _load_whitelist()
    removed = False
    if path in wl["files"]:
        wl["files"].remove(path)
        removed = True
    if path in wl["folders"]:
        wl["folders"].remove(path)
        removed = True
    if not path.startswith("."):
        alt = "." + path
    else:
        alt = path
    if alt in wl["exts"]:
        wl["exts"].remove(alt)
        removed = True
    if not removed:
        return {"ok": False, "error": f"'{path}' not found in whitelist"}
    _save_whitelist(wl)
    return {"ok": True, "whitelist": wl}


def set_interval(hours: int) -> dict:
    cfg = _load_config()
    cfg["interval_hours"] = max(1, hours)
    _save_config(cfg)
    return {"ok": True, "interval_hours": cfg["interval_hours"]}


def set_expire_days(days: int) -> dict:
    cfg = _load_config()
    cfg["expire_days"] = max(0, days)
    _save_config(cfg)
    return {"ok": True, "expire_days": cfg["expire_days"]}


def show_status() -> dict:
    cfg = _load_config()
    timer = _load_timer()
    wl = _load_whitelist()
    current_token = _peek_dry_run_token()
    return {
        "ok": True,
        "workspace": str(WORKSPACE_ROOT),
        "extension_dir": str(_EXTENSION_DIR),
        "interval_hours": cfg.get("interval_hours", DEFAULT_INTERVAL_HOURS),
        "expire_days": cfg.get("expire_days", DEFAULT_EXPIRE_DAYS),
        "auto_backup": cfg.get("auto_backup", True),
        "last_run": timer.get("last_run"),
        "timer_due": _should_run(),
        "enabled": cfg.get("enabled", False),
        "first_run_confirmed": cfg.get("first_run_confirmed", False),
        "current_dry_run_token_active": current_token is not None,
        "whitelist": wl,
        "always_protected_count": len(ALWAYS_PROTECTED),
    }


def enable_cleaner() -> dict:
    """Enable workspace_cleaner (v0.8.1 opt-in)."""
    cfg = _load_config()
    cfg["enabled"] = True
    _save_config(cfg)
    return {
        "ok": True,
        "enabled": True,
        "message": "workspace_cleaner 已启用。请先运行 dry-run 预览清理范围。",
    }


def disable_cleaner() -> dict:
    """Disable workspace_cleaner (v0.8.1 opt-out)."""
    cfg = _load_config()
    cfg["enabled"] = False
    _save_config(cfg)
    return {
        "ok": True,
        "enabled": False,
        "message": "workspace_cleaner 已禁用。",
    }


def confirm_first_run(token: str = None) -> dict:
    """
    Acknowledge the first-run dry-run results and unlock actual cleanup.
    v0.9.0: requires a valid dry-run token from the most recent dry-run.
    Token is consumed on use — each dry-run produces one consumable token.
    Token expires after 24 hours if not used.

    NOTE: Once first_run_confirmed is True in config, subsequent calls to confirm-first-run
    are no-ops (return ok=True without requiring a token), because the user has already
    completed the first-run confirmation flow. The token gate only applies to the FIRST
    time first_run_confirmed becomes True.
    """
    cfg = _load_config()
    already_confirmed = cfg.get("first_run_confirmed", False)

    # Must be enabled before we can confirm anything
    if not cfg.get("enabled", False):
        return {
            "ok": False,
            "reason": "not_enabled",
            "message": "请先运行 `python workspace_cleaner.py enable` 启用功能。",
        }

    # Once confirmed, subsequent calls are no-ops (no token required)
    if already_confirmed:
        return {
            "ok": True,
            "first_run_confirmed": True,
            "message": "首次运行已确认，无需重复确认。",
        }

    # Not yet confirmed — token is mandatory
    if not token:
        return {
            "ok": False,
            "reason": "missing_token",
            "message": (
                "confirm-first-run 需要提供 dry-run 返回的 token。\n"
                "请先运行 `python workspace_cleaner.py dry-run` 获取 token，"
                "然后用 `python workspace_cleaner.py confirm-first-run <token>` 确认。"
            ),
        }

    if not _consume_dry_run_token(token):
        return {
            "ok": False,
            "reason": "invalid_token",
            "message": (
                "token 无效或已过期。请重新运行 `python workspace_cleaner.py dry-run` 获取新的 token。"
            ),
        }


    cfg["first_run_confirmed"] = True
    _save_config(cfg)
    return {
        "ok": True,
        "first_run_confirmed": True,
        "message": "已确认首次运行。现在可以用 `run` 命令执行实际清理。",
    }


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Missing action argument. Try: run, dry-run, status, show-whitelist, "
                    "add-whitelist, remove-whitelist, set-interval, set-expire-days, "
                    "enable, disable, confirm-first-run"
        }))
        sys.exit(1)

    action = sys.argv[1]

    try:
        if action == "run":
            result = run_cleanup(dry_run=False, force=False)
            print(json.dumps(result, ensure_ascii=False, indent=2))

        elif action == "dry-run":
            result = run_cleanup(dry_run=True, force=True)
            print(json.dumps(result, ensure_ascii=False, indent=2))

        elif action == "status":
            result = show_status()
            print(json.dumps(result, ensure_ascii=False, indent=2))

        elif action == "show-whitelist":
            result = show_whitelist()
            print(json.dumps(result, ensure_ascii=False, indent=2))

        elif action == "add-whitelist":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "Missing path argument"}))
                sys.exit(1)
            path = sys.argv[2]
            entry_type = "file"
            if len(sys.argv) > 3:
                if sys.argv[3] == "--type" and len(sys.argv) > 4:
                    entry_type = sys.argv[4]
            result = add_whitelist_entry(path, entry_type)
            print(json.dumps(result, ensure_ascii=False, indent=2))

        elif action == "remove-whitelist":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "Missing path argument"}))
                sys.exit(1)
            result = remove_whitelist_entry(sys.argv[2])
            print(json.dumps(result, ensure_ascii=False, indent=2))

        elif action == "set-interval":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "Missing hours argument"}))
                sys.exit(1)
            try:
                hours = int(sys.argv[2])
            except ValueError:
                print(json.dumps({"error": "Hours must be an integer"}))
                sys.exit(1)
            result = set_interval(hours)
            print(json.dumps(result, ensure_ascii=False, indent=2))

        elif action == "set-expire-days":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "Missing days argument"}))
                sys.exit(1)
            try:
                days = int(sys.argv[2])
            except ValueError:
                print(json.dumps({"error": "Days must be an integer"}))
                sys.exit(1)
            result = set_expire_days(days)
            print(json.dumps(result, ensure_ascii=False, indent=2))

        elif action == "enable":
            result = enable_cleaner()
            print(json.dumps(result, ensure_ascii=False, indent=2))

        elif action == "disable":
            result = disable_cleaner()
            print(json.dumps(result, ensure_ascii=False, indent=2))

        elif action == "confirm-first-run":
            # Token is the 3rd argument if provided
            token = sys.argv[2] if len(sys.argv) > 2 else None
            result = confirm_first_run(token=token)
            print(json.dumps(result, ensure_ascii=False, indent=2))

        else:
            print(json.dumps({"error": f"Unknown action: {action}"}))
            sys.exit(1)

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()