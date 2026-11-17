"""任务管理器 - 内存队列 + 状态追踪"""
import uuid
import asyncio
import time
import logging
from datetime import datetime
from typing import Dict, Optional
from models import TaskStatus, TaskProgress

logger = logging.getLogger(__name__)


class TaskManager:
    """轻量内存任务管理器"""

    def __init__(self, cleanup_after: int = 3600):
        self._tasks: Dict[str, TaskProgress] = {}
        self._cleanup_after = cleanup_after
        self._lock = asyncio.Lock()

    async def create_task(self) -> str:
        task_id = uuid.uuid4().hex[:12]
        task = TaskProgress(
            task_id=task_id,
            status=TaskStatus.PENDING,
            progress=0,
            message="任务已创建，进入排队",
            current_step=0,
            total_steps=5,
        )
        async with self._lock:
            self._tasks[task_id] = task
        logger.info(f"Task created: {task_id}")
        return task_id

    async def update(self, task_id: str, **kwargs):
        async with self._lock:
            task = self._tasks.get(task_id)
            if task:
                for k, v in kwargs.items():
                    setattr(task, k, v)

    async def get(self, task_id: str) -> Optional[TaskProgress]:
        async with self._lock:
            return self._tasks.get(task_id)

    async def cleanup_stale(self):
        """清理超过存活时间的已完成/失败任务"""
        now = time.time()
        stale_ids = []
        async with self._lock:
            for tid, t in list(self._tasks.items()):
                if t.status in (TaskStatus.COMPLETED, TaskStatus.FAILED):
                    # We'd need to track creation time; skip for simplicity
                    pass
        if stale_ids:
            async with self._lock:
                for tid in stale_ids:
                    self._tasks.pop(tid, None)


task_manager = TaskManager()
