"""
任务进度相关数据模型
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base


class TaskProgress(Base):
    """任务进度表"""

    __tablename__ = "task_progress"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    task_id = Column(String(100), unique=True, nullable=False, comment="任务ID")
    task_type = Column(String(20), nullable=False, comment="任务类型：generate/execute")
    status = Column(String(20), nullable=False, comment="状态：pending/processing/completed/failed")
    progress = Column(Integer, default=0, comment="进度百分比")
    message = Column(String(255), comment="进度消息")
    result_data = Column(Text, comment="结果数据（JSON）")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "task_id": self.task_id,
            "task_type": self.task_type,
            "status": self.status,
            "progress": self.progress,
            "message": self.message,
            "result_data": self.result_data,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S") if self.create_time else None,
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S") if self.update_time else None
        }
