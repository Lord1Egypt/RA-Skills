"""
测试执行管理服务

提供执行器管理、任务队列和智能调度功能
"""

import uuid
import json
from datetime import datetime
from typing import Optional, List, Dict
import logging

from sqlalchemy.orm import Session
from app.models.execution import Executor, ExecutionQueue
from app.schemas.execution import (
    ExecutorCreate, TaskScheduleRequest,
    ExecutionStats
)

logger = logging.getLogger(__name__)


class ExecutionManagementService:
    """测试执行管理服务类"""

    def __init__(self, db: Session):
        self.db = db

    # ==================== 执行器管理 ====================

    def create_executor(self, executor_data: ExecutorCreate) -> Executor:
        """
        创建执行器

        Args:
            executor_data: 执行器数据

        Returns:
            创建的执行器
        """
        executor = Executor(
            name=executor_data.name,
            type=executor_data.type,
            capacity=executor_data.capacity,
            max_tasks=executor_data.max_tasks,
            config=json.dumps(executor_data.config, ensure_ascii=False)
        )
        self.db.add(executor)
        self.db.commit()
        self.db.refresh(executor)

        logger.info(f"创建执行器: {executor.name}, 类型={executor.type}, 容量={executor.capacity}")
        return executor

    def get_executor(self, executor_id: int) -> Optional[Executor]:
        """获取执行器"""
        return self.db.query(Executor).filter(Executor.id == executor_id).first()

    def get_executor_by_name(self, name: str) -> Optional[Executor]:
        """根据名称获取执行器"""
        return self.db.query(Executor).filter(Executor.name == name).first()

    def list_executors(self, type: str = None, status: str = None) -> List[Executor]:
        """列出执行器"""
        query = self.db.query(Executor)

        if type:
            query = query.filter(Executor.type == type)

        if status:
            query = query.filter(Executor.status == status)

        return query.all()

    def update_executor_status(self, executor_id: int, status: str) -> bool:
        """更新执行器状态"""
        executor = self.get_executor(executor_id)
        if not executor:
            return False

        executor.status = status
        executor.last_heartbeat = datetime.now()
        self.db.commit()

        logger.info(f"更新执行器状态: ID={executor_id}, status={status}")
        return True

    def delete_executor(self, executor_id: int) -> bool:
        """删除执行器"""
        executor = self.get_executor(executor_id)
        if not executor:
            return False

        self.db.delete(executor)
        self.db.commit()

        logger.info(f"删除执行器: ID={executor_id}")
        return True

    def heartbeat(self, executor_id: int, current_load: int = None) -> bool:
        """
        执行器心跳

        Args:
            executor_id: 执行器ID
            current_load: 当前负载

        Returns:
            是否成功
        """
        executor = self.get_executor(executor_id)
        if not executor:
            return False

        executor.last_heartbeat = datetime.now()

        if current_load is not None:
            executor.current_load = current_load

            # 自动更新状态
            if current_load >= executor.capacity:
                executor.status = "busy"
            elif current_load > 0:
                executor.status = "busy"
            else:
                executor.status = "idle"

        self.db.commit()
        return True

    # ==================== 任务队列管理 ====================

    def schedule_task(self, request: TaskScheduleRequest, auth_code: str = None) -> ExecutionQueue:
        """
        调度任务

        Args:
            request: 任务调度请求
            auth_code: 授权码

        Returns:
            创建的任务
        """
        task_id = str(uuid.uuid4())

        task = ExecutionQueue(
            task_id=task_id,
            script_id=request.script_id,
            script_type=request.script_type,
            priority=request.priority,
            scheduled_time=request.scheduled_time or datetime.now(),
            max_retries=request.max_retries,
            auth_code=auth_code,
            config=json.dumps(request.config, ensure_ascii=False) if request.config else None
        )

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        logger.info(f"调度任务: task_id={task_id}, script_id={request.script_id}, priority={request.priority}")
        return task

    def get_task(self, task_id: str) -> Optional[ExecutionQueue]:
        """获取任务"""
        return self.db.query(ExecutionQueue).filter(ExecutionQueue.task_id == task_id).first()

    def list_tasks(self, status: str = None, script_type: str = None, limit: int = 100) -> List[ExecutionQueue]:
        """列出任务"""
        query = self.db.query(ExecutionQueue)

        if status:
            query = query.filter(ExecutionQueue.status == status)

        if script_type:
            query = query.filter(ExecutionQueue.script_type == script_type)

        return query.order_by(ExecutionQueue.priority, ExecutionQueue.create_time).limit(limit).all()

    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        task = self.get_task(task_id)
        if not task or task.status != "pending":
            return False

        self.db.delete(task)
        self.db.commit()

        logger.info(f"取消任务: task_id={task_id}")
        return True

    def get_next_task(self, executor_type: str) -> Optional[ExecutionQueue]:
        """
        获取下一个待执行任务（按优先级）

        Args:
            executor_type: 执行器类型

        Returns:
            下一个任务
        """
        task = self.db.query(ExecutionQueue).filter(
            ExecutionQueue.status == "pending",
            ExecutionQueue.script_type == executor_type
        ).order_by(
            ExecutionQueue.priority,
            ExecutionQueue.create_time
        ).first()

        return task

    def assign_task_to_executor(self, task_id: str, executor_id: int) -> bool:
        """将任务分配给执行器"""
        task = self.get_task(task_id)
        if not task or task.status != "pending":
            return False

        executor = self.get_executor(executor_id)
        if not executor or executor.status == "offline":
            return False

        if executor.current_load >= executor.capacity:
            return False

        # 分配任务
        task.executor_id = executor_id
        task.status = "running"
        task.started_time = datetime.now()

        # 更新执行器负载
        executor.current_load += 1
        executor.status = "busy"

        self.db.commit()

        logger.info(f"分配任务: task_id={task_id}, executor_id={executor_id}")
        return True

    def complete_task(self, task_id: str, success: bool = True) -> bool:
        """完成任务"""
        task = self.get_task(task_id)
        if not task or task.status != "running":
            return False

        task.status = "completed" if success else "failed"
        task.completed_time = datetime.now()

        # 更新执行器负载
        if task.executor_id:
            executor = self.get_executor(task.executor_id)
            if executor:
                executor.current_load = max(0, executor.current_load - 1)
                executor.completed_tasks += 1

                if executor.current_load == 0:
                    executor.status = "idle"

        self.db.commit()

        logger.info(f"完成任务: task_id={task_id}, success={success}")
        return True

    def retry_task(self, task_id: str) -> bool:
        """重试任务"""
        task = self.get_task(task_id)
        if not task or task.retry_count >= task.max_retries:
            return False

        task.status = "pending"
        task.retry_count += 1
        task.executor_id = None
        task.started_time = None
        task.completed_time = None

        self.db.commit()

        logger.info(f"重试任务: task_id={task_id}, retry_count={task.retry_count}")
        return True

    # ==================== 执行统计 ====================

    def get_execution_stats(self) -> ExecutionStats:
        """获取执行统计"""
        # 执行器统计
        total_executors = self.db.query(Executor).count()
        active_executors = self.db.query(Executor).filter(Executor.status != "offline").count()
        idle_executors = self.db.query(Executor).filter(Executor.status == "idle").count()
        busy_executors = self.db.query(Executor).filter(Executor.status == "busy").count()
        offline_executors = self.db.query(Executor).filter(Executor.status == "offline").count()

        # 任务统计
        total_tasks = self.db.query(ExecutionQueue).count()
        pending_tasks = self.db.query(ExecutionQueue).filter(ExecutionQueue.status == "pending").count()
        running_tasks = self.db.query(ExecutionQueue).filter(ExecutionQueue.status == "running").count()
        completed_tasks = self.db.query(ExecutionQueue).filter(ExecutionQueue.status == "completed").count()
        failed_tasks = self.db.query(ExecutionQueue).filter(ExecutionQueue.status == "failed").count()

        return ExecutionStats(
            total_executors=total_executors,
            active_executors=active_executors,
            idle_executors=idle_executors,
            busy_executors=busy_executors,
            offline_executors=offline_executors,
            total_tasks=total_tasks,
            pending_tasks=pending_tasks,
            running_tasks=running_tasks,
            completed_tasks=completed_tasks,
            failed_tasks=failed_tasks
        )

    # ==================== 智能调度 ====================

    def auto_schedule(self) -> int:
        """
        自动调度：将待执行任务分配给空闲执行器

        Returns:
            成功调度的任务数量
        """
        # 获取所有空闲执行器
        idle_executors = self.db.query(Executor).filter(
            Executor.status == "idle",
            Executor.current_load < Executor.capacity
        ).all()

        if not idle_executors:
            return 0

        scheduled_count = 0

        for executor in idle_executors:
            # 获取该执行器类型的下一个任务
            task = self.get_next_task(executor.type)

            if task:
                success = self.assign_task_to_executor(task.task_id, executor.id)
                if success:
                    scheduled_count += 1

        if scheduled_count > 0:
            logger.info(f"自动调度完成: 分配了{scheduled_count}个任务")

        return scheduled_count

    def cleanup_expired_tasks(self, hours: int = 24) -> int:
        """
        清理过期任务（超过指定小时数的已完成/失败任务）

        Args:
            hours: 小时数

        Returns:
            清理的任务数量
        """
        from datetime import timedelta

        cutoff_time = datetime.now() - timedelta(hours=hours)

        expired_tasks = self.db.query(ExecutionQueue).filter(
            ExecutionQueue.completed_time < cutoff_time,
            ExecutionQueue.status.in_(["completed", "failed"])
        ).all()

        count = len(expired_tasks)

        for task in expired_tasks:
            self.db.delete(task)

        self.db.commit()

        if count > 0:
            logger.info(f"清理了{count}个过期任务")

        return count
