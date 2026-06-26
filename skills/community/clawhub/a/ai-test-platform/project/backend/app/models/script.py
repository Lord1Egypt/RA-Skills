"""
自动化脚本相关数据模型
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base


class AutoScript(Base):
    """自动化脚本表"""

    __tablename__ = "auto_scripts"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    name = Column(String(255), nullable=False, comment="脚本名称")
    content = Column(Text, nullable=False, comment="脚本代码")
    type = Column(String(10), nullable=False, comment="类型：api/ui")
    status = Column(String(10), default="active", comment="状态：active/archived")
    created_by = Column(String(50), comment="创建者")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "content": self.content,
            "type": self.type,
            "status": self.status,
            "created_by": self.created_by,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S") if self.create_time else None,
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S") if self.update_time else None
        }
