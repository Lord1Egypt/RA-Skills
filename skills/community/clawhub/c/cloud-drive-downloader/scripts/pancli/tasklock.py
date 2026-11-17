"""网盘通 · 单实例任务锁（v0.16.0）

教训来源（2026-10-15）：同一批文件被多个 BaiduPCS-Go 进程同时下载，
彼此抢带宽、互相覆盖断点，表现为"跑了几十分钟没有进展"。

规则：
- 同一 (drive, source, target) 同一时刻只允许一个下载进程。
- 锁文件是 JSON（pid/started/drive/source/target），放在可写目录里。
- pid 已死 → 视为陈旧锁，自动接管。
- 加锁失败要给出明确原因和处置方式，不静默失败。
"""

from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_here = _boot_os.path.dirname(_boot_os.path.abspath(__file__))
    _boot_parent = _boot_os.path.dirname(_boot_here)
    for _boot_dir in (_boot_here, _boot_parent):
        if _boot_dir not in _boot_sys.path:
            _boot_sys.path.insert(0, _boot_dir)
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass


import hashlib
import json
import os
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from pancli.engine import STATE_DIR
except Exception:  # 允许独立导入（自测/单测）
    STATE_DIR = Path(os.environ.get("PAN_STATE_DIR") or (Path.home() / ".local" / "share" / "pan-downloader"))


def lock_dir() -> Path:
    """返回可写的锁目录；优先环境变量，其次 STATE_DIR，最后系统临时目录。"""
    candidates = []
    env_dir = os.environ.get("PAN_LOCK_DIR")
    if env_dir:
        candidates.append(Path(env_dir))
    candidates.append(Path(STATE_DIR) / "locks")
    candidates.append(Path(tempfile.gettempdir()) / "pan-downloader-locks")
    for cand in candidates:
        try:
            cand.mkdir(parents=True, exist_ok=True)
            probe = cand / ".write-probe"
            probe.write_text("ok", encoding="utf-8")
            probe.unlink()
            return cand
        except Exception:
            continue
    return Path(tempfile.gettempdir()) / "pan-downloader-locks"


def lock_key(drive: str, source: str, target: str) -> str:
    raw = "|".join([(drive or "").strip().lower(), (source or "").strip(), str(Path(target or "."))])
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def pid_alive(pid: int) -> bool:
    """判断 pid 是否仍然存活。EPERM 说明进程存在但无权限发信号 → 仍算存活。"""
    if not pid or pid <= 0:
        return False
    try:
        os.kill(int(pid), 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except Exception:
        return True
    return True


def read_lock(path: Path) -> Optional[Dict[str, Any]]:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return None


class TaskLock:
    """一个 (drive, source, target) 的单实例锁。"""

    def __init__(self, drive: str, source: str, target: str, *, note: str = ""):
        self.drive = drive or ""
        self.source = source or ""
        self.target = str(target or "")
        self.note = note
        self.key = lock_key(self.drive, self.source, self.target)
        self.path = lock_dir() / (self.key + ".lock")
        self.acquired = False
        self.held_by: Dict[str, Any] = {}

    # -- 查询 ------------------------------------------------------------
    def current(self) -> Optional[Dict[str, Any]]:
        return read_lock(self.path)

    def _is_stale(self, rec: Dict[str, Any]) -> bool:
        pid = int(rec.get("pid") or 0)
        if pid == os.getpid():
            return False
        return not pid_alive(pid)

    # -- 加锁 ------------------------------------------------------------
    def acquire(self) -> bool:
        existing = self.current()
        if existing and not self._is_stale(existing):
            self.held_by = existing
            return False
        payload = {
            "schema": 1,
            "key": self.key,
            "drive": self.drive,
            "source": self.source,
            "target": self.target,
            "pid": os.getpid(),
            "note": self.note,
            "started": datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
            "started_ts": int(time.time()),
        }
        tmp = self.path.with_suffix(".lock.tmp")
        try:
            tmp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            os.replace(tmp, self.path)
        except Exception:
            return False
        self.acquired = True
        return True

    def release(self) -> None:
        if not self.acquired:
            return
        rec = self.current()
        if rec and int(rec.get("pid") or 0) == os.getpid():
            try:
                self.path.unlink()
            except Exception:
                pass
        self.acquired = False

    def __enter__(self) -> "TaskLock":
        self.acquire()
        return self

    def __exit__(self, *exc: Any) -> None:
        self.release()


def active_locks() -> List[Dict[str, Any]]:
    """列出所有锁；陈旧锁标记 stale=True。"""
    out: List[Dict[str, Any]] = []
    for path in sorted(lock_dir().glob("*.lock")):
        rec = read_lock(path)
        if not rec:
            continue
        pid = int(rec.get("pid") or 0)
        rec["stale"] = not pid_alive(pid)
        rec["lock_file"] = str(path)
        out.append(rec)
    return out


def cleanup_stale() -> List[str]:
    """删除 pid 已死的陈旧锁，返回被删掉的 key 列表。"""
    removed: List[str] = []
    for rec in active_locks():
        if rec.get("stale"):
            try:
                Path(rec["lock_file"]).unlink()
                removed.append(rec.get("key") or Path(rec["lock_file"]).stem)
            except Exception:
                pass
    return removed


def acquire_for_step(step: Dict[str, Any]) -> Dict[str, Any]:
    """给计划步骤加锁。返回 {'ok':bool,'lock':TaskLock,'message':str}。"""
    spec = step.get("lock") or {}
    lock = TaskLock(spec.get("drive", ""), spec.get("source", ""), spec.get("target", ""), note=step.get("note", ""))
    if lock.acquire():
        return {"ok": True, "lock": lock, "message": ""}
    held = lock.held_by or {}
    msg = ("同一来源已有下载进程在跑（pid=%s，开始于 %s）。"
           "网盘通只允许单实例，避免多进程抢同一批文件互相覆盖；"
           "先等它跑完，或执行 `pan guard clean` 清理陈旧锁后再重试。" % (held.get("pid"), held.get("started")))
    return {"ok": False, "lock": lock, "message": msg}
