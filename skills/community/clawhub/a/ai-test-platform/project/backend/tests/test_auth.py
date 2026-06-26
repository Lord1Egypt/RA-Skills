"""
授权管理模块测试
"""

import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.auth import AuthCodeService
from app.core.database import SessionLocal, Base, engine


class TestAuthService:
    """授权服务测试类"""

    def setup_method(self):
        """测试前准备"""
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        # 创建数据库会话
        self.db = SessionLocal()
        self.auth_service = AuthCodeService(self.db)

    def teardown_method(self):
        """测试后清理"""
        self.db.close()
        # 删除所有表
        Base.metadata.drop_all(bind=engine)

    def test_generate_random_code(self):
        """测试随机授权码生成"""
        code = self.auth_service.generate_random_code(16)
        assert len(code) == 16
        assert code.isalnum()

    def test encrypt_decrypt_auth_code(self):
        """测试授权码加密解密"""
        original_code = "test_auth_code_123"
        key = self.auth_service._generate_encryption_key()

        # 加密
        encrypted = self.auth_service.encrypt_auth_code(original_code, key)
        assert encrypted != original_code
        assert len(encrypted) > len(original_code)

        # 解密
        decrypted = self.auth_service.decrypt_auth_code(encrypted, key)
        assert decrypted == original_code

    def test_create_auth_code(self):
        """测试创建授权码"""
        result = self.auth_service.create_auth_code(
            permission="all",
            max_days=365,
            max_count=100
        )

        assert "encrypted_code" in result
        assert "original_code" in result
        assert result["permission"] == "all"
        assert result["max_count"] == 100

    def test_verify_valid_auth_code(self):
        """测试验证有效授权码"""
        # 创建授权码
        create_result = self.auth_service.create_auth_code("all", 365, 100)
        encrypted_code = create_result["encrypted_code"]

        # 验证授权码
        verify_result = self.auth_service.verify_auth_code(encrypted_code)

        assert verify_result.valid is True
        assert verify_result.message == "授权成功"
        assert verify_result.permission == "all"
        assert verify_result.remaining_count == 99  # 使用了一次

    def test_verify_invalid_auth_code(self):
        """测试验证无效授权码"""
        verify_result = self.auth_service.verify_auth_code("invalid_code")

        assert verify_result.valid is False
        assert "不存在" in verify_result.message

    def test_verify_expired_auth_code(self):
        """测试验证过期授权码"""
        from datetime import datetime, timedelta

        # 创建过期的授权码
        result = self.auth_service.create_auth_code("all", -1, 100)  # 使用-1天使其立即过期
        encrypted_code = result["encrypted_code"]

        # 验证授权码
        verify_result = self.auth_service.verify_auth_code(encrypted_code)

        assert verify_result.valid is False
        assert "过期" in verify_result.message

    def test_verify_max_count_reached(self):
        """测试验证达到使用次数限制的授权码"""
        # 创建只能使用1次的授权码
        result = self.auth_service.create_auth_code("all", 365, 1)
        encrypted_code = result["encrypted_code"]

        # 第一次使用
        verify_result_1 = self.auth_service.verify_auth_code(encrypted_code)
        assert verify_result_1.valid is True

        # 第二次使用
        verify_result_2 = self.auth_service.verify_auth_code(encrypted_code)
        assert verify_result_2.valid is False
        assert "已达上限" in verify_result_2.message

    def test_permission_check(self):
        """测试权限检查"""
        # 创建仅生成权限的授权码
        result = self.auth_service.create_auth_code("generate", 365, 100)
        encrypted_code = result["encrypted_code"]

        # 尝试访问需要全功能权限的接口
        verify_result = self.auth_service.verify_auth_code(encrypted_code, "all")
        assert verify_result.valid is False

        # 访问需要生成权限的接口
        verify_result = self.auth_service.verify_auth_code(encrypted_code, "generate")
        assert verify_result.valid is True
