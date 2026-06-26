# DreamTask — 后台记忆整固任务
# 参考: claude-code src/core/dream.ts DreamTask
#
# 三层触发 gate:
#   1. 时间 gate: 距离上次运行 > N 小时
#   2. session 数 gate: 累计 N 个 session 后触发
#   3. 锁 gate: 防止并发重复启动
#
# 状态: starting → updating → completed / failed
# UI: 对用户可见, 可取消

from __future__ import annotations
import os
import json
import time
import threading
import hashlib
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field
from enum import Enum

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/home/openclaw/.openclaw/workspace"))
DREAM_DIR = WORKSPACE / "evoclaw" / "dream"
DREAM_DIR.mkdir(parents=True, exist_ok=True)
DREAM_STATE_FILE = DREAM_DIR / "dream_state.json"
DREAM_LOG_FILE = DREAM_DIR / "dream_log.jsonl"


# ─── 状态机 ─────────────────────────────────────────────────────

class DreamState(str, Enum):
    STARTING = "starting"
    UPDATING = "updating"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# ─── Dream 记录 ─────────────────────────────────────────────────

@dataclass
class DreamRecord:
    dream_id: str
    trigger_reason: str             # 触发原因 (time/sessions/manual)
    state: DreamState = DreamState.STARTING
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    duration_ms: Optional[int] = None
    summary: str = ""              # 整固摘要
    changes_count: int = 0         # 写入的变更数
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "dream_id": self.dream_id,
            "trigger_reason": self.trigger_reason,
            "state": self.state.value,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "duration_ms": self.duration_ms,
            "summary": self.summary,
            "changes_count": self.changes_count,
            "errors": self.errors,
        }


# ─── 状态存储 ───────────────────────────────────────────────────

@dataclass
class DreamGlobalState:
    """全局 Dream 状态"""
    last_dream_at: float = 0.0
    session_count_since_dream: int = 0
    dream_task_ids: list[str] = field(default_factory=list)
    lock_acquired_at: float = 0.0
    is_running: bool = False

    def to_dict(self) -> dict:
        return {
            "last_dream_at": self.last_dream_at,
            "session_count_since_dream": self.session_count_since_dream,
            "dream_task_ids": self.dream_task_ids,
            "lock_acquired_at": self.lock_acquired_at,
            "is_running": self.is_running,
        }

    @classmethod
    def load(cls) -> "DreamGlobalState":
        if DREAM_STATE_FILE.exists():
            try:
                return cls(**json.loads(DREAM_STATE_FILE.read_text(encoding="utf-8")))
            except Exception:
                pass
        return cls()

    def save(self) -> None:
        DREAM_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        DREAM_STATE_FILE.write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False))


# ─── DreamTask ───────────────────────────────────────────────────

class DreamTask:
    """
    DreamTask — 后台记忆整固任务.
    
    三层触发 gate:
      1. time gate    — 距离上次 > N 小时 (默认 6h)
      2. sessions gate — 累计 N 个 session (默认 5)
      3. lock gate    — 防止并发重复启动
    
    参考: claude-code DreamTask 三层触发 + PID 锁
    """

    _lock = threading.RLock()

    def __init__(
        self,
        time_interval_hours: float = 6.0,
        session_threshold: int = 5,
        enabled: bool = True,
    ):
        self.time_interval_secs = time_interval_hours * 3600
        self.session_threshold = session_threshold
        self.enabled = enabled
        self.state = DreamGlobalState.load()

    # ─── 三层 Gate 检查 ──────────────────────────────────────

    def should_trigger(self) -> tuple[bool, str]:
        """
        检查是否应该触发 DreamTask.
        返回: (should_trigger, reason)
        """
        if not self.enabled:
            return False, "disabled"

        now = time.time()

        # Gate 1: 时间检查
        if self.state.last_dream_at > 0:
            elapsed = now - self.state.last_dream_at
            if elapsed < self.time_interval_secs:
                return False, f"time_gate: only {elapsed/3600:.1f}h elapsed, need {self.time_interval_secs/3600}h"

        # Gate 2: Session 数检查
        if self.state.session_count_since_dream < self.session_threshold:
            return False, f"sessions_gate: {self.state.session_count_since_dream}/{self.session_threshold} sessions"

        # Gate 3: 锁检查
        if self.state.is_running:
            return False, f"lock_gate: already running (since {self.state.lock_acquired_at})"

        return True, "all_gates_passed"

    # ─── 锁管理 ──────────────────────────────────────────────

    def acquire_lock(self) -> bool:
        """
        获取 DreamTask 锁.
        参考: claude-code PID 锁机制.
        """
        with self._lock:
            self.state = DreamGlobalState.load()
            if self.state.is_running:
                return False
            self.state.is_running = True
            self.state.lock_acquired_at = time.time()
            self.state.save()
            return True

    def release_lock(self) -> None:
        """释放锁"""
        with self._lock:
            self.state = DreamGlobalState.load()
            self.state.is_running = False
            self.state.last_dream_at = time.time()
            self.state.session_count_since_dream = 0
            self.state.save()

    # ─── 生命周期 ─────────────────────────────────────────────

    def register(self, trigger_reason: str) -> DreamRecord:
        """
        注册 DreamTask.
        参考: claude-code registerDreamTask()
        """
        record = DreamRecord(
            dream_id=self._generate_id(),
            trigger_reason=trigger_reason,
        )

        with self._lock:
            self.state = DreamGlobalState.load()
            self.state.dream_task_ids.append(record.dream_id)
            self.state.save()

        return record

    def start(self, record: DreamRecord) -> DreamRecord:
        """开始执行"""
        record.state = DreamState.UPDATING
        record.started_at = time.time()
        self._log(record)
        return record

    def complete(self, record: DreamRecord, summary: str = "", changes_count: int = 0) -> DreamRecord:
        """完成 DreamTask"""
        record.state = DreamState.COMPLETED
        record.completed_at = time.time()
        record.duration_ms = int((record.completed_at - record.started_at) * 1000) if record.started_at else 0
        record.summary = summary
        record.changes_count = changes_count
        self._log(record)
        self.release_lock()
        return record

    def fail(self, record: DreamRecord, error: str) -> DreamRecord:
        """标记失败"""
        record.state = DreamState.FAILED
        record.completed_at = time.time()
        record.duration_ms = int((record.completed_at - record.started_at) * 1000) if record.started_at else 0
        record.errors.append(error)
        self._log(record)
        self.release_lock()
        return record

    def cancel(self, record: DreamRecord) -> DreamRecord:
        """用户取消"""
        record.state = DreamState.CANCELLED
        self._log(record)
        self.release_lock()
        return record

    # ─── Session 计数 ─────────────────────────────────────────

    def increment_sessions(self) -> None:
        """增加 session 计数 (每次新 session 时调用)"""
        with self._lock:
            self.state = DreamGlobalState.load()
            self.state.session_count_since_dream += 1
            self.state.save()

    # ─── 日志 ─────────────────────────────────────────────────

    def _log(self, record: DreamRecord) -> None:
        """写入 dream log"""
        DREAM_DIR.mkdir(parents=True, exist_ok=True)
        with open(DREAM_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")

    def _generate_id(self) -> str:
        ts = int(time.time() * 1000)
        return f"dream_{ts}"

    # ─── 状态查询 ─────────────────────────────────────────────

    def get_status(self) -> dict:
        """获取 DreamTask 状态 (供 UI 显示)"""
        self.state = DreamGlobalState.load()
        return {
            "is_running": self.state.is_running,
            "last_dream_at": self.state.last_dream_at,
            "sessions_since_dream": self.state.session_count_since_dream,
            "session_threshold": self.session_threshold,
            "time_interval_hours": self.time_interval_secs / 3600,
            "enabled": self.enabled,
            "should_trigger": self.should_trigger()[0],
        }

    def get_recent_dreams(self, limit: int = 5) -> list[dict]:
        """获取最近的 DreamTask 记录"""
        if not DREAM_LOG_FILE.exists():
            return []
        try:
            lines = DREAM_LOG_FILE.read_text(encoding="utf-8").strip().split("\n")
            records = [json.loads(l) for l in lines if l.strip()][-limit:]
            return records
        except Exception:
            return []


# ─── 全局 DreamTask 实例 ────────────────────────────────────────

_dream_instance: Optional[DreamTask] = None
_dream_lock = threading.Lock()


def get_dream_task() -> DreamTask:
    global _dream_instance
    with _dream_lock:
        if _dream_instance is None:
            _dream_instance = DreamTask()
        return _dream_instance


if __name__ == "__main__":
    dream = get_dream_task()

    # Status
    print(f"Dream status: {dream.get_status()}")

    # Trigger check
    should, reason = dream.should_trigger()
    print(f"Should trigger: {should} ({reason})")

    # Increment sessions
    for i in range(6):
        dream.increment_sessions()

    should, reason = dream.should_trigger()
    print(f"After 6 sessions - Should trigger: {should} ({reason})")

    # Run dream
    if should and dream.acquire_lock():
        record = dream.register("manual_test")
        dream.start(record)
        time.sleep(0.1)
        dream.complete(record, summary="测试整固完成", changes_count=3)
        print(f"Dream completed: {record.summary}")

    print("✅ DreamTask: all tests passed")
