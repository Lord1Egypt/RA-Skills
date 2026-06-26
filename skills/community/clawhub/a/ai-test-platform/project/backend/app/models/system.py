"""
系统管理相关数据模型
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class AIModelConfig(Base):
    """AI模型配置表"""

    __tablename__ = "ai_model_configs"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    name = Column(String(100), unique=True, nullable=False, comment="模型配置名称")
    model_type = Column(String(20), nullable=False, comment="模型类型：online/local")
    provider = Column(String(50), comment="提供商：deepseek/openai/local")
    model_name = Column(String(100), comment="模型名称")
    api_key = Column(String(255), comment="API密钥（加密存储）")
    api_base_url = Column(String(255), comment="API基础URL")
    max_tokens = Column(Integer, default=2000, comment="最大token数")
    temperature = Column(Integer, default=70, comment="温度参数（0-100）")
    timeout = Column(Integer, default=30, comment="超时时间（秒）")
    max_retries = Column(Integer, default=2, comment="最大重试次数")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_default = Column(Boolean, default=False, comment="是否默认配置")
    config_data = Column(Text, comment="额外配置（JSON）")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "model_type": self.model_type,
            "provider": self.provider,
            "model_name": self.model_name,
            "api_base_url": self.api_base_url,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "is_active": self.is_active,
            "is_default": self.is_default,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S") if self.create_time else None,
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S") if self.update_time else None
        }


class TestEnvironment(Base):
    """测试环境表"""

    __tablename__ = "test_environments"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    name = Column(String(100), unique=True, nullable=False, comment="环境名称")
    env_type = Column(String(20), nullable=False, comment="环境类型：dev/test/staging/prod")
    base_url = Column(String(255), nullable=False, comment="基础URL")
    description = Column(Text, comment="环境描述")
    headers = Column(Text, comment="全局请求头（JSON）")
    params = Column(Text, comment="全局参数（JSON）")
    variables = Column(Text, comment="环境变量（JSON）")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_default = Column(Boolean, default=False, comment="是否默认环境")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "env_type": self.env_type,
            "base_url": self.base_url,
            "description": self.description,
            "is_active": self.is_active,
            "is_default": self.is_default,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S") if self.create_time else None,
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S") if self.update_time else None
        }


class OperationLog(Base):
    """操作日志表"""

    __tablename__ = "operation_logs"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    user_id = Column(String(50), comment="用户ID（授权码）")
    operation_type = Column(String(50), nullable=False, comment="操作类型")
    operation_module = Column(String(50), comment="操作模块")
    operation_desc = Column(Text, comment="操作描述")
    request_method = Column(String(10), comment="请求方法")
    request_url = Column(String(255), comment="请求URL")
    request_params = Column(Text, comment="请求参数")
    response_status = Column(Integer, comment="响应状态码")
    response_data = Column(Text, comment="响应数据")
    ip_address = Column(String(50), comment="IP地址")
    user_agent = Column(String(255), comment="用户代理")
    duration = Column(Integer, comment="执行耗时（毫秒）")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "operation_type": self.operation_type,
            "operation_module": self.operation_module,
            "operation_desc": self.operation_desc,
            "request_method": self.request_method,
            "request_url": self.request_url,
            "response_status": self.response_status,
            "ip_address": self.ip_address,
            "duration": self.duration,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S") if self.create_time else None
        }


class DataBackup(Base):
    """数据备份表"""

    __tablename__ = "data_backups"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    name = Column(String(100), nullable=False, comment="备份名称")
    backup_type = Column(String(20), nullable=False, comment="备份类型：full/incremental")
    backup_scope = Column(String(20), nullable=False, comment="备份范围：database/files/all")
    file_path = Column(String(255), comment="备份文件路径")
    file_size = Column(Integer, comment="文件大小（字节）")
    status = Column(String(20), default="pending", comment="状态：pending/completed/failed")
    error_message = Column(Text, comment="错误信息")
    backup_config = Column(Text, comment="备份配置（JSON）")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")
    complete_time = Column(DateTime, comment="完成时间")

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "backup_type": self.backup_type,
            "backup_scope": self.backup_scope,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "status": self.status,
            "error_message": self.error_message,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S") if self.create_time else None,
            "complete_time": self.complete_time.strftime("%Y-%m-%d %H:%M:%S") if self.complete_time else None
        }
