"""
授权服务模块

处理授权码的加密、解密、验证和管理
"""

import time
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.auth import AuthCode
from app.core.config import settings
from app.schemas.auth import AuthCodeCreate, AuthVerifyResponse
from typing import Optional


class AuthCodeService:
    """授权码服务类"""

    def __init__(self, db: Session):
        self.db = db

    def _generate_encryption_key(self) -> bytes:
        """
        生成AES加密密钥
        格式: "yanghua" + 当前时间戳 + "360sb"
        """
        encryption_key = f"{settings.AES_KEY_PREFIX}{int(time.time())}{settings.AES_KEY_SUFFIX}"
        # 确保密钥长度为32字节（AES-256）
        encryption_key = encryption_key[:32].ljust(32, '0')[:32]
        return encryption_key.encode('utf-8')

    def encrypt_auth_code(self, code: str, key: bytes) -> str:
        """
        使用AES加密授权码

        Args:
            code: 原始授权码字符串
            key: AES加密密钥

        Returns:
            加密后的授权码（base64编码）
        """
        cipher = AES.new(key, AES.MODE_ECB)
        encrypted = cipher.encrypt(pad(code.encode('utf-8'), AES.block_size))
        return base64.b64encode(encrypted).decode('utf-8')

    def decrypt_auth_code(self, encrypted_code: str, key: bytes) -> str:
        """
        使用AES解密授权码

        Args:
            encrypted_code: 加密后的授权码
            key: AES加密密钥

        Returns:
            原始授权码字符串
        """
        try:
            cipher = AES.new(key, AES.MODE_ECB)
            decrypted = unpad(cipher.decrypt(base64.b64decode(encrypted_code)), AES.block_size)
            return decrypted.decode('utf-8')
        except Exception as e:
            raise ValueError(f"解密失败: {str(e)}")

    def generate_random_code(self, length: int = 16) -> str:
        """
        生成随机授权码

        Args:
            length: 授权码长度

        Returns:
            随机生成的原始授权码
        """
        import secrets
        import string
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    def create_auth_code(self, permission: str, max_days: int = 365, max_count: int = 100) -> dict:
        """
        创建授权码

        Args:
            permission: 权限类型 (all/generate/execute)
            max_days: 有效期（天）
            max_count: 最大使用次数

        Returns:
            包含授权码信息的字典
        """
        # 生成加密密钥
        key = self._generate_encryption_key()

        # 生成原始授权码
        original_code = self.generate_random_code(16)

        # 加密授权码
        encrypted_code = self.encrypt_auth_code(original_code, key)

        # 计算过期时间
        expire_time = datetime.now() + timedelta(days=max_days)

        # 创建数据库记录
        auth_code = AuthCode(
            code=encrypted_code,
            permission=permission,
            expire_time=expire_time,
            max_count=max_count,
            is_active=1
        )
        self.db.add(auth_code)
        self.db.commit()
        self.db.refresh(auth_code)

        return {
            "original_code": original_code,
            "encrypted_code": encrypted_code,
            "permission": permission,
            "expire_time": expire_time,
            "max_count": max_count,
            "encrypt_key": key.decode('utf-8')  # 只用于显示，实际使用时应该安全存储
        }

    def verify_auth_code(self, auth_code: str, required_permission: Optional[str] = None) -> AuthVerifyResponse:
        """
        验证授权码

        Args:
            auth_code: 授权码（加密后的）
            required_permission: 需要的权限类型

        Returns:
            验证结果
        """
        try:
            # 查询授权码
            db_auth_code = self.db.query(AuthCode).filter(AuthCode.code == auth_code).first()

            if not db_auth_code:
                return AuthVerifyResponse(
                    valid=False,
                    message="授权码不存在",
                    permission=None,
                    remaining_count=None
                )

            # 检查授权码是否有效
            is_valid, error_msg = db_auth_code.is_valid(required_permission)

            if not is_valid:
                return AuthVerifyResponse(
                    valid=False,
                    message=error_msg,
                    permission=db_auth_code.permission,
                    remaining_count=db_auth_code.max_count - db_auth_code.use_count
                )

            # 增加使用次数
            db_auth_code.increment_usage()
            self.db.commit()

            return AuthVerifyResponse(
                valid=True,
                message="授权成功",
                permission=db_auth_code.permission,
                remaining_count=db_auth_code.max_count - db_auth_code.use_count
            )

        except Exception as e:
            return AuthVerifyResponse(
                valid=False,
                message=f"验证失败: {str(e)}",
                permission=None,
                remaining_count=None
            )

    def get_auth_code(self, auth_code_id: int) -> Optional[AuthCode]:
        """
        根据ID获取授权码
        """
        return self.db.query(AuthCode).filter(AuthCode.id == auth_code_id).first()

    def get_all_auth_codes(self):
        """
        获取所有授权码
        """
        return self.db.query(AuthCode).all()

    def disable_auth_code(self, auth_code_id: int) -> bool:
        """
        禁用授权码
        """
        auth_code = self.get_auth_code(auth_code_id)
        if auth_code:
            auth_code.is_active = 0
            self.db.commit()
            return True
        return False

    def enable_auth_code(self, auth_code_id: int) -> bool:
        """
        启用授权码
        """
        auth_code = self.get_auth_code(auth_code_id)
        if auth_code:
            auth_code.is_active = 1
            self.db.commit()
            return True
        return False