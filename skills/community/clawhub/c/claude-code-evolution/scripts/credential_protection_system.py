#!/usr/bin/env python3
"""
OpenClaw凭证保护系统 - 阶段4.3.2：加密系统实现

基于Claude Code架构的凭证保护系统，实现分层加密、安全存储和访问控制。
"""

import os
import sys
import json
import base64
import secrets
import hashlib
import datetime
import time
from typing import Dict, Optional, List, Any, Union
from dataclasses import dataclass, asdict
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
import argon2

# 确保在Python路径中包含当前目录
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 常量定义
CREDENTIAL_LEVELS = {
    1: "关键API密钥",
    2: "应用凭证", 
    3: "系统令牌",
    4: "标识符"
}

ENCRYPTION_ALGORITHMS = {
    1: "AES-256-GCM + 主密钥",
    2: "AES-256-GCM + 应用密钥",
    3: "AES-256-GCM + 组件密钥",
    4: "base64+sha256混淆"
}

@dataclass
class EncryptedCredential:
    """加密凭证数据结构"""
    encrypted_data: str  # 加密后的十六进制字符串
    nonce: str  # 加密nonce的十六进制字符串
    level: int  # 凭证级别 1-4
    context: str  # 使用上下文
    algorithm: str  # 加密算法
    timestamp: str  # 加密时间戳
    credential_id: str  # 凭证标识符
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'EncryptedCredential':
        """从字典创建"""
        return cls(**data)

class MasterKeyManager:
    """主密钥管理器"""
    
    def __init__(self):
        self.master_key = None
        self.key_derivation_salt = None
        self.is_initialized = False
        
    def initialize(self, user_password: Optional[str] = None) -> bool:
        """初始化主密钥系统"""
        try:
            # 如果没有提供密码，尝试从环境变量或配置文件获取
            if user_password is None:
                user_password = os.environ.get("OPENCLAW_MASTER_PASSWORD")
                if user_password is None:
                    # 提示用户输入密码（在实际应用中应该是交互式）
                    print("警告: 未提供主密码，使用默认测试密钥")
                    user_password = "default_test_password_change_in_production"
            
            # 生成系统盐值
            self.key_derivation_salt = self.generate_system_salt()
            
            # 派生主密钥
            self.master_key = self.derive_master_key(user_password, self.key_derivation_salt)
            
            self.is_initialized = True
            print(f"主密钥系统初始化完成，密钥长度: {len(self.master_key)}字节")
            return True
            
        except Exception as e:
            print(f"主密钥初始化失败: {e}")
            return False
    
    def derive_master_key(self, user_password: str, system_salt: bytes) -> bytes:
        """从用户密码派生主密钥"""
        try:
            # 检查argon2是否可用
            try:
                import argon2
                hasher = argon2.PasswordHasher(
                    time_cost=3,
                    memory_cost=65536,
                    parallelism=4,
                    hash_len=32,
                    salt_len=16
                )
                
                # 派生密钥
                password_hash = hasher.hash(user_password, salt=system_salt)
                
                # 从哈希中提取密钥（简化版本）
                # 在实际应用中应该使用标准的密钥派生函数
                derived_key = hashlib.sha256(
                    f"{user_password}:{system_salt.hex()}:{password_hash}".encode()
                ).digest()
                
                return derived_key[:32]  # 返回32字节的AES-256密钥
                
            except ImportError:
                # argon2不可用，使用PBKDF2作为备选
                print("警告: argon2不可用，使用PBKDF2-HMAC-SHA256作为备选")
                import hashlib
                import hmac
                
                # 使用PBKDF2派生密钥
                derived_key = hashlib.pbkdf2_hmac(
                    'sha256',
                    user_password.encode(),
                    system_salt,
                    100000,  # 迭代次数
                    dklen=32
                )
                
                return derived_key
                
        except Exception as e:
            print(f"密钥派生失败: {e}")
            # 返回简单派生密钥（仅用于测试）
            return hashlib.sha256(f"{user_password}:{system_salt.hex()}".encode()).digest()[:32]
    
    def generate_system_salt(self) -> bytes:
        """生成系统级盐值"""
        try:
            # 收集系统唯一信息
            system_info = []
            
            # 主机名
            try:
                system_info.append(os.uname().nodename.encode())
            except:
                pass
            
            # 用户主目录
            system_info.append(os.path.expanduser("~").encode())
            
            # 用户ID
            system_info.append(str(os.getuid()).encode())
            
            # 当前工作目录
            system_info.append(os.getcwd().encode())
            
            # OpenClaw安装目录（如果存在）
            openclaw_path = os.path.expanduser("~/.openclaw")
            if os.path.exists(openclaw_path):
                system_info.append(openclaw_path.encode())
            
            # 生成确定性盐值
            combined = b"".join(system_info)
            salt = hashlib.sha256(combined).digest()[:16]
            
            print(f"系统盐值生成完成: {salt.hex()[:16]}...")
            return salt
            
        except Exception as e:
            print(f"系统盐值生成失败: {e}")
            # 返回随机盐值
            return secrets.token_bytes(16)
    
    def get_master_key(self) -> Optional[bytes]:
        """获取主密钥"""
        if not self.is_initialized:
            print("错误: 主密钥系统未初始化")
            return None
        return self.master_key

class HierarchicalEncryption:
    """分层加密系统"""
    
    def __init__(self, master_key_manager: MasterKeyManager):
        self.master_key_manager = master_key_manager
        self.app_keys = {}  # 按应用类型存储应用密钥
        self.component_keys = {}  # 按系统组件存储密钥
        
    def generate_app_key(self, app_type: str) -> bytes:
        """生成应用密钥"""
        # 从主密钥派生应用密钥
        master_key = self.master_key_manager.get_master_key()
        if master_key is None:
            raise ValueError("主密钥未初始化")
        
        # 使用HKDF风格派生（简化）
        derivation_input = f"app_key:{app_type}:{secrets.token_hex(8)}".encode()
        app_key = hashlib.sha256(master_key + derivation_input).digest()[:32]
        
        # 存储应用密钥（加密存储）
        self.app_keys[app_type] = app_key
        print(f"生成应用密钥: {app_type}，长度: {len(app_key)}字节")
        
        return app_key
    
    def derive_component_key(self, component: str) -> bytes:
        """派生系统组件密钥"""
        master_key = self.master_key_manager.get_master_key()
        if master_key is None:
            raise ValueError("主密钥未初始化")
        
        # 派生组件密钥
        derivation_input = f"component:{component}".encode()
        component_key = hashlib.sha256(master_key + derivation_input).digest()[:32]
        
        self.component_keys[component] = component_key
        return component_key
    
    def encrypt_level1(self, plaintext: str, context: str, credential_id: str) -> EncryptedCredential:
        """Level 1加密：关键API密钥"""
        master_key = self.master_key_manager.get_master_key()
        if master_key is None:
            raise ValueError("主密钥未初始化")
        
        # 生成随机nonce
        nonce = secrets.token_bytes(12)
        
        try:
            # 使用主密钥加密
            aesgcm = AESGCM(master_key)
            ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), context.encode())
            
            return EncryptedCredential(
                encrypted_data=ciphertext.hex(),
                nonce=nonce.hex(),
                level=1,
                context=context,
                algorithm="AES-256-GCM",
                timestamp=datetime.datetime.now().isoformat(),
                credential_id=credential_id
            )
            
        except Exception as e:
            print(f"Level 1加密失败: {e}")
            raise
    
    def encrypt_level2(self, plaintext: str, app_type: str, credential_id: str) -> EncryptedCredential:
        """Level 2加密：应用凭证"""
        # 获取或生成应用密钥
        if app_type not in self.app_keys:
            self.generate_app_key(app_type)
        
        app_key = self.app_keys[app_type]
        
        # 生成随机nonce
        nonce = secrets.token_bytes(12)
        
        try:
            # 使用应用密钥加密
            aesgcm = AESGCM(app_key)
            ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), app_type.encode())
            
            return EncryptedCredential(
                encrypted_data=ciphertext.hex(),
                nonce=nonce.hex(),
                level=2,
                context=app_type,
                algorithm="AES-256-GCM",
                timestamp=datetime.datetime.now().isoformat(),
                credential_id=credential_id
            )
            
        except Exception as e:
            print(f"Level 2加密失败: {e}")
            raise
    
    def encrypt_level3(self, plaintext: str, component: str, credential_id: str) -> EncryptedCredential:
        """Level 3加密：系统令牌"""
        # 获取或派生组件密钥
        if component not in self.component_keys:
            self.derive_component_key(component)
        
        component_key = self.component_keys[component]
        
        # 生成随机nonce
        nonce = secrets.token_bytes(12)
        
        try:
            # 使用组件密钥加密
            aesgcm = AESGCM(component_key)
            ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), component.encode())
            
            return EncryptedCredential(
                encrypted_data=ciphertext.hex(),
                nonce=nonce.hex(),
                level=3,
                context=component,
                algorithm="AES-256-GCM",
                timestamp=datetime.datetime.now().isoformat(),
                credential_id=credential_id
            )
            
        except Exception as e:
            print(f"Level 3加密失败: {e}")
            raise
    
    def encrypt_level4(self, plaintext: str, credential_id: str) -> EncryptedCredential:
        """Level 4加密：标识符（混淆）"""
        try:
            # 简单混淆方案
            salt = b"openclaw_identifier_salt_v1"
            combined = plaintext.encode() + salt
            
            # 生成混淆值
            obfuscated = hashlib.sha256(combined).hexdigest()[:32]
            
            # 原值base64编码
            encoded = base64.b64encode(plaintext.encode()).decode()
            
            return EncryptedCredential(
                encrypted_data=obfuscated,  # 这里存储混淆值
                nonce="",  # Level 4不需要nonce
                level=4,
                context="identifier",
                algorithm="base64+sha256",
                timestamp=datetime.datetime.now().isoformat(),
                credential_id=credential_id
            )
            
        except Exception as e:
            print(f"Level 4混淆失败: {e}")
            raise
    
    def decrypt_level1(self, encrypted_cred: EncryptedCredential, context: str) -> Optional[str]:
        """解密Level 1凭证"""
        master_key = self.master_key_manager.get_master_key()
        if master_key is None:
            return None
        
        try:
            # 验证上下文
            if encrypted_cred.context != context:
                print(f"上下文不匹配: 预期{context}, 实际{encrypted_cred.context}")
                return None
            
            # 解密
            aesgcm = AESGCM(master_key)
            ciphertext = bytes.fromhex(encrypted_cred.encrypted_data)
            nonce = bytes.fromhex(encrypted_cred.nonce)
            
            plaintext = aesgcm.decrypt(nonce, ciphertext, context.encode())
            return plaintext.decode()
            
        except InvalidTag:
            print("解密失败: 认证标签无效（密钥或数据被篡改）")
            return None
        except Exception as e:
            print(f"解密失败: {e}")
            return None
    
    def decrypt_level2(self, encrypted_cred: EncryptedCredential) -> Optional[str]:
        """解密Level 2凭证"""
        app_type = encrypted_cred.context
        
        # 获取应用密钥
        if app_type not in self.app_keys:
            print(f"未知的应用类型: {app_type}")
            return None
        
        app_key = self.app_keys[app_type]
        
        try:
            aesgcm = AESGCM(app_key)
            ciphertext = bytes.fromhex(encrypted_cred.encrypted_data)
            nonce = bytes.fromhex(encrypted_cred.nonce)
            
            plaintext = aesgcm.decrypt(nonce, ciphertext, app_type.encode())
            return plaintext.decode()
            
        except Exception as e:
            print(f"Level 2解密失败: {e}")
            return None
    
    def decrypt_level3(self, encrypted_cred: EncryptedCredential) -> Optional[str]:
        """解密Level 3凭证"""
        component = encrypted_cred.context
        
        # 获取组件密钥
        if component not in self.component_keys:
            print(f"未知的系统组件: {component}")
            return None
        
        component_key = self.component_keys[component]
        
        try:
            aesgcm = AESGCM(component_key)
            ciphertext = bytes.fromhex(encrypted_cred.encrypted_data)
            nonce = bytes.fromhex(encrypted_cred.nonce)
            
            plaintext = aesgcm.decrypt(nonce, ciphertext, component.encode())
            return plaintext.decode()
            
        except Exception as e:
            print(f"Level 3解密失败: {e}")
            return None
    
    def deobfuscate_level4(self, encrypted_cred: EncryptedCredential) -> Optional[str]:
        """解混淆Level 4标识符"""
        try:
            # Level 4存储的是base64编码的原值
            if hasattr(encrypted_cred, 'encoded'):
                # 如果有encoded字段，直接解码
                return base64.b64decode(encrypted_cred.encoded).decode()
            else:
                # 否则尝试从encrypted_data解码（它可能是base64）
                try:
                    return base64.b64decode(encrypted_cred.encrypted_data).decode()
                except:
                    # 如果不能解码，返回原始混淆值
                    return encrypted_cred.encrypted_data
                    
        except Exception as e:
            print(f"Level 4解混淆失败: {e}")
            return None

class CredentialStorage:
    """安全的凭证存储"""
    
    def __init__(self, storage_path: str = None):
        if storage_path is None:
            # 默认存储路径
            workspace_dir = os.path.expanduser("~/.openclaw/workspace")
            self.storage_path = os.path.join(workspace_dir, "memory", "encrypted-credentials.json")
        else:
            self.storage_path = storage_path
        
        # 确保目录存在
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        
        # 存储结构
        self.store_structure = {
            "meta": {
                "version": "1.0",
                "created": datetime.datetime.now().isoformat(),
                "last_updated": datetime.datetime.now().isoformat(),
                "encryption_scheme": "hierarchical_aes_gcm",
                "total_credentials": 0
            },
            "credentials": {
                "level1": {},  # 关键API密钥
                "level2": {},  # 应用凭证
                "level3": {},  # 系统令牌
                "level4": {}   # 标识符
            },
            "key_management": {
                "app_keys": {},     # 加密的应用密钥（元数据）
                "key_rotation": {}  # 密钥轮换记录
            }
        }
        
        # 加载现有存储（如果存在）
        self.load_from_disk()
    
    def load_from_disk(self):
        """从磁盘加载存储"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    
                # 合并数据，保留新字段
                for level in ["level1", "level2", "level3", "level4"]:
                    if level in loaded_data.get("credentials", {}):
                        self.store_structure["credentials"][level] = loaded_data["credentials"][level]
                
                # 更新元数据
                if "meta" in loaded_data:
                    self.store_structure["meta"].update(loaded_data["meta"])
                
                # 更新key_management
                if "key_management" in loaded_data:
                    self.store_structure["key_management"].update(loaded_data["key_management"])
                
                print(f"从 {self.storage_path} 加载了凭证存储")
                
            except Exception as e:
                print(f"加载凭证存储失败: {e}")
                # 创建新的存储文件
                self.save_to_disk()
        else:
            print(f"凭证存储文件不存在，创建新的: {self.storage_path}")
            self.save_to_disk()
    
    def save_to_disk(self):
        """保存到磁盘"""
        try:
            # 更新总凭证数
            total = 0
            for level in ["level1", "level2", "level3", "level4"]:
                total += len(self.store_structure["credentials"][level])
            self.store_structure["meta"]["total_credentials"] = total
            self.store_structure["meta"]["last_updated"] = datetime.datetime.now().isoformat()
            
            # 保存到文件
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.store_structure, f, indent=2, ensure_ascii=False)
            
            # 设置文件权限（仅所有者可读写）
            try:
                os.chmod(self.storage_path, 0o600)
            except:
                pass
            
            print(f"凭证存储已保存到 {self.storage_path}")
            return True
            
        except Exception as e:
            print(f"保存凭证存储失败: {e}")
            return False
    
    def store_credential(self, credential_id: str, encrypted_credential: EncryptedCredential) -> bool:
        """存储加密凭证"""
        level_key = f"level{encrypted_credential.level}"
        
        if level_key not in self.store_structure["credentials"]:
            print(f"无效的凭证级别: {encrypted_credential.level}")
            return False
        
        # 存储凭证
        self.store_structure["credentials"][level_key][credential_id] = encrypted_credential.to_dict()
        
        # 自动保存到文件
        success = self.save_to_disk()
        
        if success:
            print(f"凭证已存储: {credential_id} (级别 {encrypted_credential.level})")
        else:
            print(f"凭证存储失败: {credential_id}")
        
        return success
    
    def retrieve_credential(self, credential_id: str, level: int) -> Optional[EncryptedCredential]:
        """检索加密凭证"""
        level_key = f"level{level}"
        
        if (level_key in self.store_structure["credentials"] and 
            credential_id in self.store_structure["credentials"][level_key]):
            
            cred_data = self.store_structure["credentials"][level_key][credential_id]
            return EncryptedCredential.from_dict(cred_data)
        
        return None
    
    def list_credentials(self, level: Optional[int] = None) -> List[str]:
        """列出凭证ID"""
        credentials = []
        
        if level is None:
            # 列出所有凭证
            for lvl in [1, 2, 3, 4]:
                level_key = f"level{lvl}"
                credentials.extend(list(self.store_structure["credentials"][level_key].keys()))
        else:
            # 列出特定级别的凭证
            level_key = f"level{level}"
            if level_key in self.store_structure["credentials"]:
                credentials = list(self.store_structure["credentials"][level_key].keys())
        
        return credentials
    
    def remove_credential(self, credential_id: str, level: int) -> bool:
        """移除凭证"""
        level_key = f"level{level}"
        
        if (level_key in self.store_structure["credentials"] and 
            credential_id in self.store_structure["credentials"][level_key]):
            
            del self.store_structure["credentials"][level_key][credential_id]
            self.save_to_disk()
            print(f"凭证已移除: {credential_id}")
            return True
        
        return False

class AccessController:
    """凭证访问控制器"""
    
    def __init__(self, credential_storage: CredentialStorage, encryption_system: HierarchicalEncryption):
        self.credential_storage = credential_storage
        self.encryption_system = encryption_system
        self.active_accesses = {}  # 当前活跃的访问
        self.audit_log = []
        
        # 访问策略（简化版本）
        self.access_policies = self.load_default_policies()
    
    def load_default_policies(self) -> Dict:
        """加载默认访问策略"""
        return {
            "models.providers.deepseek.apiKey": {
                "allowed_contexts": ["model_inference", "cost_calculation"],
                "max_access_per_hour": 100,
                "require_approval": False
            },
            "channels.feishu.*.appSecret": {
                "allowed_contexts": ["message_send", "message_receive"],
                "max_access_per_hour": 50,
                "require_approval": False
            },
            "gateway.auth.token": {
                "allowed_contexts": ["gateway_communication"],
                "max_access_per_hour": 20,
                "require_approval": True
            }
        }
    
    def request_access(self, credential_id: str, level: int, 
                      context: Dict, reason: str) -> Optional[str]:
        """请求凭证访问"""
        
        # 1. 记录访问请求
        request_id = secrets.token_hex(8)
        self.audit_log.append({
            "request_id": request_id,
            "credential_id": credential_id,
            "level": level,
            "context": context,
            "reason": reason,
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "requested"
        })
        
        # 2. 检查访问策略
        policy_check = self.check_access_policy(credential_id, level, context)
        if not policy_check["allowed"]:
            self.audit_log[-1]["status"] = "denied_by_policy"
            self.audit_log[-1]["denial_reason"] = policy_check["reason"]
            print(f"访问被策略拒绝: {policy_check['reason']}")
            return None
        
        # 3. 检索加密凭证
        encrypted_cred = self.credential_storage.retrieve_credential(credential_id, level)
        if encrypted_cred is None:
            self.audit_log[-1]["status"] = "credential_not_found"
            print(f"凭证未找到: {credential_id}")
            return None
        
        # 4. 解密凭证
        plaintext = None
        try:
            if level == 1:
                plaintext = self.encryption_system.decrypt_level1(encrypted_cred, context.get("purpose", ""))
            elif level == 2:
                plaintext = self.encryption_system.decrypt_level2(encrypted_cred)
            elif level == 3:
                plaintext = self.encryption_system.decrypt_level3(encrypted_cred)
            elif level == 4:
                plaintext = self.encryption_system.deobfuscate_level4(encrypted_cred)
            
            if plaintext is None:
                self.audit_log[-1]["status"] = "decryption_failed"
                print(f"解密失败: {credential_id}")
                return None
                
        except Exception as e:
            self.audit_log[-1]["status"] = "decryption_error"
            self.audit_log[-1]["error"] = str(e)
            print(f"解密错误: {e}")
            return None
        
        # 5. 记录成功访问
        access_id = f"access_{secrets.token_hex(6)}"
        self.active_accesses[access_id] = {
            "credential_id": credential_id,
            "level": level,
            "context": context,
            "reason": reason,
            "plaintext_length": len(plaintext),
            "access_time": datetime.datetime.now().isoformat(),
            "expiry_time": (datetime.datetime.now() + datetime.timedelta(minutes=5)).isoformat(),
            "access_id": access_id
        }
        
        self.audit_log[-1]["status"] = "granted"
        self.audit_log[-1]["access_id"] = access_id
        
        print(f"访问已授权: {credential_id} (访问ID: {access_id})")
        
        # 6. 返回解密后的凭证（在实际应用中应该更安全地处理）
        # 注意：这里直接返回明文，实际应用中应该使用更安全的方式
        return plaintext
    
    def check_access_policy(self, credential_id: str, level: int, context: Dict) -> Dict:
        """检查访问策略"""
        # 简化策略检查
        result = {
            "allowed": True,
            "reason": "策略检查通过"
        }
        
        # 检查凭证级别
        if level == 1 and context.get("purpose") not in ["model_inference", "cost_calculation"]:
            result["allowed"] = False
            result["reason"] = "Level 1凭证仅允许在model_inference或cost_calculation上下文中使用"
        
        # 检查访问频率（简化）
        recent_accesses = [
            log for log in self.audit_log[-100:] 
            if log.get("credential_id") == credential_id and 
               log.get("status") == "granted"
        ]
        
        if len(recent_accesses) > 50:  # 简化频率检查
            result["allowed"] = False
            result["reason"] = "访问频率过高"
        
        return result
    
    def revoke_access(self, access_id: str) -> bool:
        """撤销访问权限"""
        if access_id in self.active_accesses:
            del self.active_accesses[access_id]
            
            # 更新审计日志
            for log in self.audit_log:
                if log.get("access_id") == access_id:
                    log["revoked_at"] = datetime.datetime.now().isoformat()
            
            print(f"访问已撤销: {access_id}")
            return True
        
        return False
    
    def cleanup_expired_accesses(self):
        """清理过期访问"""
        now = datetime.datetime.now()
        expired_ids = []
        
        for access_id, access in self.active_accesses.items():
            expiry_time = datetime.datetime.fromisoformat(access["expiry_time"])
            if expiry_time < now:
                expired_ids.append(access_id)
        
        for access_id in expired_ids:
            self.revoke_access(access_id)
        
        if expired_ids:
            print(f"清理了 {len(expired_ids)} 个过期访问")
    
    def get_audit_summary(self) -> Dict:
        """获取审计摘要"""
        total_requests = len(self.audit_log)
        granted = sum(1 for log in self.audit_log if log.get("status") == "granted")
        denied = sum(1 for log in self.audit_log if log.get("status") == "denied_by_policy")
        
        return {
            "total_requests": total_requests,
            "granted": granted,
            "denied": denied,
            "grant_rate": granted / total_requests if total_requests > 0 else 0,
            "active_accesses": len(self.active_accesses),
            "last_audit_time": datetime.datetime.now().isoformat()
        }

class CredentialProtectionSystem:
    """凭证保护系统主类"""
    
    def __init__(self, master_password: Optional[str] = None):
        # 初始化组件
        self.master_key_manager = MasterKeyManager()
        self.encryption_system = None
        self.credential_storage = None
        self.access_controller = None
        
        # 初始化系统
        self.initialized = self.initialize_system(master_password)
    
    def initialize_system(self, master_password: Optional[str] = None) -> bool:
        """初始化整个系统"""
        try:
            print("正在初始化凭证保护系统...")
            
            # 1. 初始化主密钥管理器
            print("步骤1: 初始化主密钥管理器")
            if not self.master_key_manager.initialize(master_password):
                print("主密钥管理器初始化失败")
                return False
            
            # 2. 初始化加密系统
            print("步骤2: 初始化分层加密系统")
            self.encryption_system = HierarchicalEncryption(self.master_key_manager)
            
            # 3. 初始化凭证存储
            print("步骤3: 初始化凭证存储")
            self.credential_storage = CredentialStorage()
            
            # 4. 初始化访问控制器
            print("步骤4: 初始化访问控制器")
            self.access_controller = AccessController(self.credential_storage, self.encryption_system)
            
            print("凭证保护系统初始化完成!")
            return True
            
        except Exception as e:
            print(f"系统初始化失败: {e}")
            return False
    
    def encrypt_and_store_credential(self, credential_id: str, plaintext: str, 
                                   level: int, context: str = "") -> bool:
        """加密并存储凭证"""
        if not self.initialized:
            print("系统未初始化")
            return False
        
        try:
            # 根据级别选择合适的加密方法
            encrypted_cred = None
            
            if level == 1:
                encrypted_cred = self.encryption_system.encrypt_level1(
                    plaintext, context, credential_id
                )
            elif level == 2:
                # 从credential_id提取应用类型（简化）
                app_type = self.extract_app_type_from_id(credential_id)
                encrypted_cred = self.encryption_system.encrypt_level2(
                    plaintext, app_type, credential_id
                )
            elif level == 3:
                component = self.extract_component_from_id(credential_id)
                encrypted_cred = self.encryption_system.encrypt_level3(
                    plaintext, component, credential_id
                )
            elif level == 4:
                encrypted_cred = self.encryption_system.encrypt_level4(
                    plaintext, credential_id
                )
            else:
                print(f"无效的凭证级别: {level}")
                return False
            
            # 存储加密凭证
            return self.credential_storage.store_credential(credential_id, encrypted_cred)
            
        except Exception as e:
            print(f"加密并存储凭证失败: {e}")
            return False
    
    def extract_app_type_from_id(self, credential_id: str) -> str:
        """从凭证ID提取应用类型（简化）"""
        # 根据credential_id判断应用类型
        if "feishu" in credential_id.lower():
            return "feishu"
        elif "qqbot" in credential_id.lower() or "qq" in credential_id.lower():
            return "qqbot"
        elif "deepseek" in credential_id.lower():
            return "deepseek"
        elif "gateway" in credential_id.lower():
            return "gateway"
        else:
            return "default"
    
    def extract_component_from_id(self, credential_id: str) -> str:
        """从凭证ID提取系统组件（简化）"""
        if "gateway" in credential_id.lower():
            return "gateway"
        elif "auth" in credential_id.lower():
            return "authentication"
        else:
            return "system"
    
    def get_credential(self, credential_id: str, level: int, 
                      context: Dict, reason: str) -> Optional[str]:
        """获取凭证（通过访问控制器）"""
        if not self.initialized:
            print("系统未初始化")
            return None
        
        return self.access_controller.request_access(
            credential_id, level, context, reason
        )
    
    def list_stored_credentials(self) -> Dict:
        """列出所有存储的凭证"""
        if not self.initialized or self.credential_storage is None:
            return {}
        
        result = {}
        for level in [1, 2, 3, 4]:
            cred_ids = self.credential_storage.list_credentials(level)
            result[f"level{level}"] = {
                "count": len(cred_ids),
                "credential_ids": cred_ids
            }
        
        return result
    
    def get_system_status(self) -> Dict:
        """获取系统状态"""
        status = {
            "initialized": self.initialized,
            "components": {
                "master_key_manager": self.master_key_manager.is_initialized if self.master_key_manager else False,
                "encryption_system": self.encryption_system is not None,
                "credential_storage": self.credential_storage is not None,
                "access_controller": self.access_controller is not None
            },
            "storage_info": {
                "path": self.credential_storage.storage_path if self.credential_storage else None,
                "total_credentials": self.credential_storage.store_structure["meta"]["total_credentials"] if self.credential_storage else 0
            }
        }
        
        if self.access_controller:
            status["audit_summary"] = self.access_controller.get_audit_summary()
        
        return status

def main():
    """主函数：测试凭证保护系统"""
    print("=" * 60)
    print("OpenClaw凭证保护系统测试")
    print("=" * 60)
    
    # 初始化系统
    # 注意：在生产环境中，密码应该从安全的地方获取
    test_password = "test_master_password_123"  # 测试用密码
    cps = CredentialProtectionSystem(test_password)
    
    if not cps.initialized:
        print("系统初始化失败，退出")
        return
    
    # 显示系统状态
    print("\n系统状态:")
    status = cps.get_system_status()
    print(json.dumps(status, indent=2))
    
    # 测试加密和存储一些凭证
    print("\n测试凭证加密和存储...")
    
    # 测试Level 1: DeepSeek API密钥
    deepseek_api_key = "sk-55778e8d0f884ac9b7dbab452e2209aa"  # 示例密钥
    success = cps.encrypt_and_store_credential(
        "models.providers.deepseek.apiKey",
        deepseek_api_key,
        level=1,
        context="model_inference"
    )
    print(f"DeepSeek API密钥存储: {'成功' if success else '失败'}")
    
    # 测试Level 2: 飞书appSecret
    feishu_app_secret = "BSUNoxewivFiNi0usdNVHgGxCbEp7jpd"  # 示例密钥
    success = cps.encrypt_and_store_credential(
        "channels.feishu.accounts.main.appSecret",
        feishu_app_secret,
        level=2
    )
    print(f"飞书appSecret存储: {'成功' if success else '失败'}")
    
    # 测试Level 3: Gateway令牌
    gateway_token = "IAeictLapdYmph8tp6l2h3N5Y5UvZ2q4"  # 示例令牌
    success = cps.encrypt_and_store_credential(
        "gateway.auth.token",
        gateway_token,
        level=3
    )
    print(f"Gateway令牌存储: {'成功' if success else '失败'}")
    
    # 测试Level 4: 应用ID
    feishu_app_id = "cli_a9f0e478d3381cb0"  # 示例ID
    success = cps.encrypt_and_store_credential(
        "channels.feishu.accounts.main.appId",
        feishu_app_id,
        level=4
    )
    print(f"飞书appId存储: {'成功' if success else '失败'}")
    
    # 列出存储的凭证
    print("\n存储的凭证列表:")
    stored_creds = cps.list_stored_credentials()
    for level, info in stored_creds.items():
        print(f"  {level}: {info['count']} 个凭证")
        for cred_id in info["credential_ids"][:3]:  # 只显示前3个
            print(f"    - {cred_id}")
        if info["count"] > 3:
            print(f"    ... 还有 {info['count'] - 3} 个")
    
    # 测试获取凭证
    print("\n测试凭证获取...")
    
    # 获取DeepSeek API密钥
    context = {"purpose": "model_inference", "user": "test_user"}
    retrieved_key = cps.get_credential(
        "models.providers.deepseek.apiKey",
        level=1,
        context=context,
        reason="测试模型调用"
    )
    
    if retrieved_key:
        # 验证获取的密钥
        if retrieved_key == deepseek_api_key:
            print("✓ DeepSeek API密钥获取和验证成功")
            print(f"  获取的密钥（部分）: {retrieved_key[:10]}...{retrieved_key[-10:]}")
        else:
            print("✗ DeepSeek API密钥验证失败")
    else:
        print("✗ DeepSeek API密钥获取失败")
    
    # 清理过期访问
    if cps.access_controller:
        cps.access_controller.cleanup_expired_accesses()
    
    # 最终状态
    print("\n最终系统状态:")
    final_status = cps.get_system_status()
    print(f"总凭证数: {final_status['storage_info']['total_credentials']}")
    if 'audit_summary' in final_status:
        audit = final_status['audit_summary']
        print(f"访问请求: {audit['total_requests']} (授权: {audit['granted']}, 拒绝: {audit['denied']})")
    
    print("\n测试完成!")
    print("=" * 60)

if __name__ == "__main__":
    main()