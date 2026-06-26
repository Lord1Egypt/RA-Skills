"""
测试报告相关数据模型
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class TestReport(Base):
    """测试报告表"""

    __tablename__ = "test_reports"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    record_id = Column(Integer, ForeignKey("execute_records.id"), nullable=False, comment="执行记录ID")
    script_id = Column(Integer, ForeignKey("auto_scripts.id"), nullable=False, comment="脚本ID")
    script_name = Column(String(255), comment="脚本名称")
    script_type = Column(String(10), comment="脚本类型：api/ui")
    result = Column(String(10), nullable=False, comment="结果：success/fail")
    total_tests = Column(Integer, default=0, comment="总测试数")
    passed_tests = Column(Integer, default=0, comment="通过测试数")
    failed_tests = Column(Integer, default=0, comment="失败测试数")
    duration = Column(Integer, default=0, comment="执行耗时（秒）")
    report_content = Column(Text, comment="报告内容（HTML）")
    report_path = Column(String(255), comment="报告文件路径")
    log_content = Column(Text, comment="执行日志")
    ai_analysis = Column(Text, comment="AI分析结果")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "record_id": self.record_id,
            "script_id": self.script_id,
            "script_name": self.script_name,
            "script_type": self.script_type,
            "result": self.result,
            "total_tests": self.total_tests,
            "passed_tests": self.passed_tests,
            "failed_tests": self.failed_tests,
            "duration": self.duration,
            "report_content": self.report_content,
            "report_path": self.report_path,
            "log_content": self.log_content,
            "ai_analysis": self.ai_analysis,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S") if self.create_time else None
        }
