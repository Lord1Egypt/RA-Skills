"""
执行器管理相关数据模型
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base


class Executor(Base):
    """执行器表"""

    __tablename__ = "executors"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    name = Column(String(100), unique=True, nullable=False, comment="执行器名称")
    type = Column(String(20), nullable=False, comment="执行器类型：api/ui")
    status = Column(String(20), default="idle", comment="状态：idle/busy/offline")
    capacity = Column(Integer, default=5, comment="并发容量")
    current_load = Column(Integer, default=0, comment="当前负载")
    max_tasks = Column(Integer, default=100, comment="最大任务数")
    completed_tasks = Column(Integer, default=0, comment="已完成任务数")
    last_heartbeat = Column(DateTime, comment="最后心跳时间")
    config = Column(Text, comment="执行器配置（JSON）")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "status": self.status,
            "capacity": self.capacity,
            "current_load": self.current_load,
            "max_tasks": self.max_tasks,
            "completed_tasks": self.completed_tasks,
            "last_heartbeat": self.last_heartbeat.strftime("%Y-%m-%d %H:%M:%S") if self.last_heartbeat else None,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S") if self.create_time else None,
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S") if self.update_time else None
        }


class ExecutionQueue(Base):
    """执行队列表"""

    __tablename__ = "execution_queue"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    task_id = Column(String(100), unique=True, nullable=False, comment="任务ID")
    script_id = Column(Integer, nullable=False, comment="脚本ID")
    script_type = Column(String(10), nullable=False, comment="脚本类型：api/ui")
    priority = Column(Integer, default=5, comment="优先级（1-10，数字越小优先级越高）")
    status = Column(String(20), default="pending", comment="状态：pending/running/completed/failed")
    executor_id = Column(Integer, comment="执行器ID")
    retry_count = Column(Integer, default=0, comment="重试次数")
    max_retries = Column(Integer, default=2, comment="最大重试次数")
    scheduled_time = Column(DateTime, comment="计划执行时间")
    started_time = Column(DateTime, comment="实际开始时间")
    completed_time = Column(DateTime, comment="完成时间")
    auth_code = Column(String(50), comment="授权码")
    config = Column(Text, comment="执行配置（JSON）")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "task_id": self.task_id,
            "script_id": self.script_id,
            "script_type": self.script_type,
            "priority": self.priority,
            "status": self.status,
            "executor_id": self.executor_id,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "scheduled_time": self.scheduled_time.strftime("%Y-%m-%d %H:%M:%S") if self.scheduled_time else None,
            "started_time": self.started_time.strftime("%Y-%m-%d %H:%M:%S") if self.started_time else None,
            "completed_time": self.completed_time.strftime("%Y-%m-%d %H:%M:%S") if self.completed_time else None,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S") if self.create_time else None
        }
