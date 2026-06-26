"""
执行记录数据模型
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class ExecuteRecord(Base):
    """执行记录表"""

    __tablename__ = "execute_records"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    script_id = Column(Integer, ForeignKey("auto_scripts.id"), nullable=False, comment="脚本ID")
    auth_code = Column(String(50), comment="执行者授权码")
    result = Column(String(10), nullable=False, comment="结果：success/fail")
    log = Column(Text, comment="执行日志")
    execute_time = Column(DateTime, server_default=func.now(), comment="执行时间")
    duration = Column(Integer, comment="执行耗时（秒）")

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "script_id": self.script_id,
            "auth_code": self.auth_code,
            "result": self.result,
            "log": self.log,
            "execute_time": self.execute_time.strftime("%Y-%m-%d %H:%M:%S") if self.execute_time else None,
            "duration": self.duration
        }
