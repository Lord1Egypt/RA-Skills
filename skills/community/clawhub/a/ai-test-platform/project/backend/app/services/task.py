"""
任务进度服务

管理AI生成任务和测试执行任务的进度追踪
"""

import uuid
import json
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.task import TaskProgress
import logging

logger = logging.getLogger(__name__)


class TaskProgressService:
    """任务进度服务类"""

    def __init__(self, db: Session):
        self.db = db

    def create_task(self, task_type: str) -> str:
        """
        创建新任务

        Args:
            task_type: 任务类型（generate/execute）

        Returns:
            任务ID
        """
        task_id = str(uuid.uuid4())
        task = TaskProgress(
            task_id=task_id,
            task_type=task_type,
            status="pending",
            progress=0,
            message="任务已创建，等待处理"
        )
        self.db.add(task)
        self.db.commit()
        logger.info(f"创建任务: {task_id}, 类型: {task_type}")
        return task_id

    def update_task(self, task_id: str, status: str = None, progress: int = None,
                    message: str = None, result_data: dict = None):
        """
        更新任务进度

        Args:
            task_id: 任务ID
            status: 任务状态
            progress: 进度百分比
            message: 进度消息
            result_data: 结果数据
        """
        task = self.get_task(task_id)
        if not task:
            logger.error(f"任务不存在: {task_id}")
            return

        if status:
            task.status = status
        if progress is not None:
            task.progress = progress
        if message:
            task.message = message
        if result_data:
            task.result_data = json.dumps(result_data, ensure_ascii=False)

        self.db.commit()
        logger.info(f"更新任务 {task_id}: status={status}, progress={progress}%, message={message}")

    def get_task(self, task_id: str) -> Optional[TaskProgress]:
        """
        获取任务详情

        Args:
            task_id: 任务ID

        Returns:
            任务对象
        """
        return self.db.query(TaskProgress).filter(TaskProgress.task_id == task_id).first()

    def get_task_status(self, task_id: str) -> Optional[dict]:
        """
        获取任务状态

        Args:
            task_id: 任务ID

        Returns:
            任务状态字典
        """
        task = self.get_task(task_id)
        if not task:
            return None

        return task.to_dict()

    def delete_task(self, task_id: str) -> bool:
        """
        删除任务

        Args:
            task_id: 任务ID

        Returns:
            是否删除成功
        """
        task = self.get_task(task_id)
        if not task:
            return False

        self.db.delete(task)
        self.db.commit()
        logger.info(f"删除任务: {task_id}")
        return True

    def cleanup_old_tasks(self, hours: int = 24):
        """
        清理旧任务（超过指定小时数）

        Args:
            hours: 小时数
        """
        from datetime import timedelta
        cutoff_time = datetime.now() - timedelta(hours=hours)

        old_tasks = self.db.query(TaskProgress).filter(
            TaskProgress.create_time < cutoff_time,
            TaskProgress.status.in_(["completed", "failed"])
        ).all()

        for task in old_tasks:
            self.db.delete(task)

        self.db.commit()
        logger.info(f"清理了 {len(old_tasks)} 个旧任务")
