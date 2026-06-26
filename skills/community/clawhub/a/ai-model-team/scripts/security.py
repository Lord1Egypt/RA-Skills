"""
Security Module
P2: API key rotation, least privilege, sensitive data masking
"""
import os
import json
import hmac
import hashlib
import base64
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, List
from dataclasses import dataclass
from pathlib import Path
import secrets

# ============ Configuration ============
KEY_ROTATION_DAYS = 90  # Rotate API keys every 90 days
ALLOW_WITHDRAWAL = False  # Default to false for security
MIN_KEY_LENGTH = 32


@dataclass
class APIKeyMetadata:
    """API密钥元数据"""
    key_id: str
    created_at: str
    expires_at: str
    last_used: Optional[str]
    permissions: List[str]
    status: str  # active/rotated/expired/revoked
    rotation_count: int


class SecureKeyStorage:
    """安全密钥存储"""
    
    def __init__(self, storage_path: str = None):
        self.storage_path = Path(storage_path or 
            os.path.expanduser("~/.agents/ai-model-team/secrets.json"))
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.keys: Dict[str, APIKeyMetadata] = {}
        self._load()
    
    def _load(self):
        """加载密钥存储"""
        if self.storage_path.exists():
            with open(self.storage_path) as f:
                data = json.load(f)
                for key_id, key_data in data.items():
                    self.keys[key_id] = APIKeyMetadata(**key_data)
    
    def _save(self):
        """保存密钥存储"""
        data = {
            key_id: {
                "key_id": km.key_id,
                "created_at": km.created_at,
                "expires_at": km.expires_at,
                "last_used": km.last_used,
                "permissions": km.permissions,
                "status": km.status,
                "rotation_count": km.rotation_count
            }
            for key_id, km in self.keys.items()
        }
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def generate_key_id(self) -> str:
        """生成密钥ID"""
        return f"key_{secrets.token_hex(8)}"
    
    def create_key(
        self,
        permissions: List[str],
        ttl_days: int = KEY_ROTATION_DAYS
    ) -> tuple[str, str]:
        """
        创建新密钥
        
        Returns:
            (key_id, secret_key)
        """
        key_id = self.generate_key_id()
        secret_key = secrets.token_urlsafe(MIN_KEY_LENGTH)
        
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(days=ttl_days)
        
        metadata = APIKeyMetadata(
            key_id=key_id,
            created_at=now.isoformat(),
            expires_at=expires_at.isoformat(),
            last_used=None,
            permissions=permissions,
            status="active",
            rotation_count=0
        )
        
        self.keys[key_id] = metadata
        self._save()
        
        return key_id, secret_key
    
    def rotate_key(self, key_id: str) -> tuple[str, str]:
        """
        轮换密钥
        
        1. 将旧密钥标记为rotated
        2. 生成新密钥
        3. 返回新密钥
        """
        if key_id not in self.keys:
            raise ValueError(f"Key {key_id} not found")
        
        old_metadata = self.keys[key_id]
        old_metadata.status = "rotated"
        old_metadata.rotation_count += 1
        
        # 生成新密钥
        new_key_id, new_secret = self.create_key(
            permissions=old_metadata.permissions
        )
        
        self._save()
        return new_key_id, new_secret
    
    def revoke_key(self, key_id: str):
        """撤销密钥"""
        if key_id in self.keys:
            self.keys[key_id].status = "revoked"
            self._save()
    
    def get_active_keys(self) -> List[APIKeyMetadata]:
        """获取活跃密钥"""
        return [k for k in self.keys.values() if k.status == "active"]
    
    def check_expiration(self) -> List[APIKeyMetadata]:
        """检查过期密钥"""
        now = datetime.now(timezone.utc)
        expiring = []
        
        for key in self.keys.values():
            if key.status != "active":
                continue
            
            exp_date = datetime.fromisoformat(key.expires_at)
            if exp_date < now:
                key.status = "expired"
                expiring.append(key)
            elif (exp_date - now).days < 7:  # 7天内过期
                expiring.append(key)
        
        if expiring:
            self._save()
        
        return expiring


class PermissionManager:
    """权限管理器"""
    
    # 权限定义
    PERMISSIONS = {
        "read_market": ["market_data", "klines", "orderbook"],
        "read_account": ["account", "positions", "balances"],
        "trade": ["spot", "swap", "futures"],
        "withdraw": ["internal_transfer", "external_withdrawal"]
    }
    
    @classmethod
    def check_permission(
        cls,
        required: List[str],
        granted: List[str]
    ) -> bool:
        """检查是否有所需权限"""
        for req in required:
            if req not in granted:
                return False
        return True
    
    @classmethod
    def get_least_privilege_keys(
        cls,
        task: str
    ) -> List[str]:
        """
        获取最小权限密钥
        
        Args:
            task: 任务类型
                - "prediction": 只需要读市场数据
                - "monitoring": 读市场数据 + 账户
                - "trading": 读市场数据 + 账户 + 交易
                - "admin": 所有权限
        """
        task_permissions = {
            "prediction": ["read_market"],
            "monitoring": ["read_market", "read_account"],
            "trading": ["read_market", "read_account", "trade"],
            "admin": list(cls.PERMISSIONS.keys())
        }
        
        return task_permissions.get(task, ["read_market"])


class AuditLogger:
    """审计日志"""
    
    def __init__(self, log_path: str = None):
        self.log_path = Path(log_path or 
            os.path.expanduser("~/.agents/ai-model-team/audit.log"))
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def log(
        self,
        action: str,
        user: str = "system",
        resource: str = "",
        result: str = "success",
        details: Dict = None
    ):
        """记录审计日志"""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            "user": user,
            "resource": resource,
            "result": result,
            "details": details or {}
        }
        
        with open(self.log_path, 'a') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    def get_recent(self, limit: int = 100) -> List[Dict]:
        """获取最近的审计日志"""
        if not self.log_path.exists():
            return []
        
        with open(self.log_path) as f:
            lines = f.readlines()
        
        entries = []
        for line in lines[-limit:]:
            try:
                entries.append(json.loads(line))
            except:
                continue
        
        return entries


class SensitiveDataMasker:
    """敏感数据脱敏"""
    
    @staticmethod
    def mask_api_key(key: str, visible: int = 4) -> str:
        """脱敏API密钥，只显示前N位"""
        if not key or len(key) <= visible:
            return "***"
        return key[:visible] + "***"
    
    @staticmethod
    def mask_balance(balance: float) -> str:
        """脱敏余额"""
        return "***"
    
    @staticmethod
    def mask_dict(data: Dict, sensitive_keys: List[str] = None) -> Dict:
        """脱敏字典中的敏感字段"""
        if sensitive_keys is None:
            sensitive_keys = [
                "api_key", "secret", "password", "token",
                "secret_key", "api_password", "authorization",
                "balance", "equity", "margin"
            ]
        
        result = {}
        for k, v in data.items():
            k_lower = k.lower()
            
            if any(s in k_lower for s in sensitive_keys):
                if isinstance(v, str):
                    result[k] = SensitiveDataMasker.mask_api_key(v)
                elif isinstance(v, (int, float)):
                    result[k] = SensitiveDataMasker.mask_balance(v)
                else:
                    result[k] = "***"
            elif isinstance(v, dict):
                result[k] = SensitiveDataMasker.mask_dict(v, sensitive_keys)
            else:
                result[k] = v
        
        return result


# Global instances
_key_storage: Optional[SecureKeyStorage] = None
_audit_logger: Optional[AuditLogger] = None

def get_key_storage() -> SecureKeyStorage:
    global _key_storage
    if _key_storage is None:
        _key_storage = SecureKeyStorage()
    return _key_storage

def get_audit_logger() -> AuditLogger:
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger


def check_key_expiration_and_rotate():
    """检查密钥过期并自动轮换"""
    storage = get_key_storage()
    expiring = storage.check_expiration()
    
    for key in expiring:
        if key.status == "active":
            # 需要轮换
            try:
                new_id, new_secret = storage.rotate_key(key.key_id)
                get_audit_logger().log(
                    action="key_rotation",
                    resource=f"api_key:{key.key_id}",
                    result="success",
                    details={"new_key_id": new_id}
                )
            except Exception as e:
                get_audit_logger().log(
                    action="key_rotation",
                    resource=f"api_key:{key.key_id}",
                    result="failed",
                    details={"error": str(e)}
                )
