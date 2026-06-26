"""
测试用例相关数据模型
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base


class TestCase(Base):
    """测试用例表"""

    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    title = Column(String(255), nullable=False, comment="用例标题")
    content = Column(Text, nullable=False, comment="用例详情")
    type = Column(String(10), nullable=False, comment="类型：api/ui")
    created_by = Column(String(50), comment="创建者（授权码）")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "type": self.type,
            "created_by": self.created_by,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S") if self.create_time else None
        }
