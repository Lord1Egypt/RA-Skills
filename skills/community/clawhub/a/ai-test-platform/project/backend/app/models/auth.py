"""
授权码数据模型
"""

from sqlalchemy import Column, Integer, String, DateTime, TinyInt
from sqlalchemy.sql import func
from app.core.database import Base


class AuthCode(Base):
    """授权码表"""

    __tablename__ = "auth_codes"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    code = Column(String(100), unique=True, nullable=False, comment="授权码（加密后）")
    permission = Column(String(20), nullable=False, comment="权限类型：all/generate/execute")
    expire_time = Column(DateTime, nullable=False, comment="过期时间")
    use_count = Column(Integer, default=0, comment="已使用次数")
    max_count = Column(Integer, nullable=False, comment="最大使用次数")
    is_active = Column(TinyInt, default=1, comment="启用状态：1启用/0禁用")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "code": self.code,
            "permission": self.permission,
            "expire_time": self.expire_time.strftime("%Y-%m-%d %H:%M:%S") if self.expire_time else None,
            "use_count": self.use_count,
            "max_count": self.max_count,
            "is_active": self.is_active,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S") if self.create_time else None,
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S") if self.update_time else None
        }

    def is_valid(self, required_permission=None):
        """
        检查授权码是否有效

        Args:
            required_permission: 需要的权限类型

        Returns:
            tuple: (是否有效, 错误消息)
        """
        # 检查是否启用
        if not self.is_active:
            return False, "授权码已被禁用"

        # 检查是否过期
        from datetime import datetime
        if self.expire_time and datetime.now() > self.expire_time:
            return False, "授权码已过期"

        # 检查使用次数
        if self.use_count >= self.max_count:
            return False, "授权码使用次数已达上限"

        # 检查权限
        if required_permission:
            # 全功能权限可以访问所有功能
            if self.permission == "all":
                return True, None

            # 仅生成权限只能访问生成功能
            if self.permission == "generate" and required_permission not in ["generate", "case"]:
                return False, "权限不足，仅支持生成功能"

            # 仅执行权限只能访问执行功能
            if self.permission == "execute" and required_permission != "execute":
                return False, "权限不足，仅支持执行功能"

        return True, None

    def increment_usage(self):
        """增加使用次数"""
        self.use_count += 1
