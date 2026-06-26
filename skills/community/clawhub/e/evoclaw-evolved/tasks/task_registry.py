# Task Registry — 统一任务类型注册表
# 参考: claude-code/src/services/tasks.ts TaskType 体系
#
# 设计原则:
#   1. 所有任务类型统一注册, 各类型自行实现 start/stop/status
#   2. stopTask() 统一入口, 按类型分发 kill
#   3. 任务状态追踪 (running/Stopped/failed)
#   4. Bash 噪声抑制 (exit code 137 = SIGKILL, 对用户无意义)

import os
import signal
import json
import time
import threading
from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Optional, Callable, Any
from pathlib import Path

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/home/openclaw/.openclaw/workspace"))
REGISTRY_FILE = WORKSPACE / "evoclaw" / "tasks" / "task_registry.json"
REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)


class TaskType(str, Enum):
    SUBAGENT = "subagent"           # sessions_spawn 子代理
    EXEC = "exec"                   # exec 进程
    CRON = "cron"                   # 定时任务
    WORKFLOW = "workflow"           # 工作流
    # DreamTask 由 dream module 独立管理


class TaskStatus(str, Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    FAILED = "failed"


@dataclass
class TaskRecord:
    task_id: str
    task_type: TaskType
    label: str                      # 人类可读标签
    status: TaskStatus = TaskStatus.RUNNING
    pid: Optional[int] = None      # 进程 ID (exec 任务)
    created_at: float = field(default_factory=time.time)
    stopped_at: Optional[float] = None
    exit_code: Optional[int] = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["task_type"] = self.task_type.value
        d["status"] = self.status.value
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "TaskRecord":
        d["task_type"] = TaskType(d["task_type"])
        d["status"] = TaskStatus(d["status"])
        return cls(**d)


class TaskRegistry:
    """全局任务注册表, 线程安全"""

    _lock = threading.RLock()
    _tasks: dict[str, TaskRecord] = {}

    @classmethod
    def _load(cls) -> None:
        if REGISTRY_FILE.exists():
            try:
                data = json.loads(REGISTRY_FILE.read_text())
                cls._tasks = {k: TaskRecord.from_dict(v) for k, v in data.items()}
            except Exception:
                cls._tasks = {}

    @classmethod
    def _save(cls) -> None:
        data = {k: v.to_dict() for k, v in cls._tasks.items()}
        REGISTRY_FILE.write_text(json.dumps(data, indent=2))

    @classmethod
    def register(cls, task_id: str, task_type: TaskType, label: str,
                 pid: Optional[int] = None, metadata: Optional[dict] = None) -> TaskRecord:
        with cls._lock:
            cls._load()
            record = TaskRecord(
                task_id=task_id,
                task_type=task_type,
                label=label,
                pid=pid,
                metadata=metadata or {}
            )
            cls._tasks[task_id] = record
            cls._save()
            return record

    @classmethod
    def unregister(cls, task_id: str) -> Optional[TaskRecord]:
        with cls._lock:
            cls._load()
            record = cls._tasks.pop(task_id, None)
            if record:
                cls._save()
            return record

    @classmethod
    def get(cls, task_id: str) -> Optional[TaskRecord]:
        with cls._lock:
            cls._load()
            return cls._tasks.get(task_id)

    @classmethod
    def list_by_type(cls, task_type: TaskType) -> list[TaskRecord]:
        with cls._lock:
            cls._load()
            return [v for v in cls._tasks.values() if v.task_type == task_type]

    @classmethod
    def list_running(cls) -> list[TaskRecord]:
        with cls._lock:
            cls._load()
            return [v for v in cls._tasks.values() if v.status == TaskStatus.RUNNING]

    @classmethod
    def update_status(cls, task_id: str, status: TaskStatus,
                      exit_code: Optional[int] = None) -> Optional[TaskRecord]:
        with cls._lock:
            cls._load()
            record = cls._tasks.get(task_id)
            if record:
                record.status = status
                record.stopped_at = time.time()
                if exit_code is not None:
                    record.exit_code = exit_code
                cls._save()
            return record


# ─── 统一 stopTask ────────────────────────────────────────────────

def stop_task(task_id: str) -> dict:
    """
    统一停止任务入口.
    参考: claude-code/src/services/tasks.ts stopTask()

    Returns:
        {"result": True}  或 {"result": False, "message": "...", "errorCode": 1}
    """
    record = TaskRegistry.get(task_id)
    if not record:
        return {"result": False, "message": f"Task {task_id} not found", "errorCode": 1}

    if record.status != TaskStatus.RUNNING:
        return {"result": False, "message": f"Task {task_id} is not running", "errorCode": 2}

    task_type = record.task_type
    pid = record.pid

    try:
        if task_type == TaskType.EXEC and pid:
            # SIGKILL 噪声抑制: exit code 137 是 SIGKILL, 对用户无意义
            _kill_process(pid)
            TaskRegistry.update_status(task_id, TaskStatus.STOPPED, exit_code=137)
            return {"result": True}

        elif task_type == TaskType.SUBAGENT:
            # 子代理由 sessions_spawn 管理, 这里只更新状态
            # 实际 kill 由 subagents tool 处理
            TaskRegistry.update_status(task_id, TaskStatus.STOPPED, exit_code=0)
            return {"result": True}

        elif task_type == TaskType.CRON:
            # Cron 任务标记为 stopped, 由 cron scheduler 实际取消
            TaskRegistry.update_status(task_id, TaskStatus.STOPPED, exit_code=0)
            return {"result": True}

        else:
            TaskRegistry.update_status(task_id, TaskStatus.STOPPED, exit_code=0)
            return {"result": True}

    except Exception as e:
        TaskRegistry.update_status(task_id, TaskStatus.FAILED)
        return {"result": False, "message": str(e), "errorCode": 3}


def _kill_process(pid: int) -> None:
    """Kill 进程, 吞掉 ProcessLookupError"""
    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(0.1)
        try:
            os.kill(pid, 0)  # 检查进程是否还在
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass  # 进程已退出
    except ProcessLookupError:
        pass  # 进程不存在


def stop_all_tasks() -> dict:
    """停止所有运行中的任务 (用于 shutdown)"""
    running = TaskRegistry.list_running()
    results = {}
    for record in running:
        results[record.task_id] = stop_task(record.task_id)
    return results


if __name__ == "__main__":
    # Demo
    r = TaskRegistry.register("demo-1", TaskType.EXEC, "测试进程", pid=12345)
    print(f"Registered: {r.task_id}")
    print(f"List running: {[t.label for t in TaskRegistry.list_running()]}")
    stop_task("demo-1")
    print(f"After stop: {TaskRegistry.get('demo-1')}")
    TaskRegistry.unregister("demo-1")
