# -*- coding: utf-8 -*-
"""
Vault密钥管理器

职责：
1. 从HashiCorp Vault安全存储/获取密钥
2. 支持本地加密存储作为Vault的替代方案
3. 对接Pipeline的密钥注入

设计思路（DHH风格）：
- 密钥管理必须可靠，但实现可以简单
- 先跑起来，再考虑复杂的安全方案
"""
import os
import json
from pathlib import Path
from typing import Optional, Dict, Any
from lib.audit.logger import AuditLogger


class VaultManager:
    """
    密钥管理器 - MVP版本
    
    支持两种模式：
    1. Vault模式 (production): 连接HashiCorp Vault
    2. Env模式 (development): 从环境变量/本地文件读取
    """
    
    def __init__(self, config, audit_logger: AuditLogger):
        self.config = config
        self.audit = audit_logger
        self._cache: Dict[str, str] = {}
        self._client = None
        
        if config.vault.enabled:
            self._init_vault_client()
    
    def _init_vault_client(self):
        """初始化Vault客户端"""
        try:
            import hvac
            self._client = hvac.Client(url=self.config.vault.url)
            if self.config.vault.token:
                self._client.token = self.config.vault.token
            self.audit.log("vault", "connected", {"url": self.config.vault.url})
        except ImportError:
            self.audit.log("vault", "error", {"msg": "hvac not installed, falling back to env mode"})
            self._client = None
    
    def get(self, key: str, site_name: Optional[str] = None) -> Optional[str]:
        """
        获取密钥值
        
        Args:
            key: 密钥名称 (如 "wp_password" )
            site_name: 站点名称，用于构建Vault路径
            
        Returns:
            密钥值，失败返回None
        """
        # 缓存命中
        cache_key = f"{site_name}:{key}" if site_name else key
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # Vault模式
        if self._client:
            try:
                mount_point = self.config.vault.mount_point
                # 路径格式: secret/wp/{site_name}/{key}
                path = f"wp/{site_name}/{key}" if site_name else f"wp/{key}"
                response = self._client.secrets.kv.v2.read_secret_version(
                    path=path,
                    mount_point=mount_point
                )
                value = response["data"]["data"].get(key)
                self._cache[cache_key] = value
                self.audit.log("vault", "get", {"key": key, "site": site_name, "found": bool(value)})
                return value
            except Exception as e:
                self.audit.log("vault", "error", {"key": key, "error": str(e)})
                return None
        
        # Env回退模式
        env_key = f"WP_{site_name.upper()}_{key.upper()}" if site_name else f"WP_{key.upper()}"
        value = os.getenv(env_key)
        if value:
            self._cache[cache_key] = value
            self.audit.log("vault", "env_fallback", {"key": env_key})
        return value
    
    def set(self, key: str, value: str, site_name: Optional[str] = None) -> bool:
        """设置密钥（仅Vault模式有效）"""
        if not self._client:
            self.audit.log("vault", "set_skipped", {"reason": "vault_disabled"})
            return False
        
        try:
            mount_point = self.config.vault.mount_point
            path = f"wp/{site_name}/{key}" if site_name else f"wp/{key}"
            self._client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret={key: value},
                mount_point=mount_point
            )
            cache_key = f"{site_name}:{key}" if site_name else key
            self._cache[cache_key] = value
            self.audit.log("vault", "set", {"key": key, "site": site_name})
            return True
        except Exception as e:
            self.audit.log("vault", "error", {"key": key, "error": str(e)})
            return False
