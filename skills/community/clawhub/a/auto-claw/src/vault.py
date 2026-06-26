"""
Vault Manager - 密钥管理
支持 HashiCorp Vault / 1Password Business / 环境变量 fallback
"""
import os
import json
import subprocess
from typing import Optional, Dict, Any

class VaultManager:
    def __init__(self, mode: str = None):
        self.mode = mode or os.environ.get("VAULT_MODE", "disabled")
        self.vault_addr = os.environ.get("VAULT_ADDR", "")
        self.vault_token = os.environ.get("VAULT_TOKEN", "")
        self._cache: Dict[str, str] = {}
    
    def get_secret(self, path: str, key: str = None) -> Optional[str]:
        """
        获取密钥。
        优先级：1. Vault   2. 环境变量   3. 禁用模式
        """
        if self.mode == "hashicorp":
            return self._get_hashicorp(path, key)
        elif self.mode == "1password":
            return self._get_1password(path, key)
        else:
            return self._env_fallback(path, key)
    
    def _get_hashicorp(self, path: str, key: str) -> Optional[str]:
        try:
            result = subprocess.run(
                ["vault", "kv", "get", "-field", key, path],
                capture_output=True, text=True, timeout=10
            )
            return result.stdout.strip()
        except Exception:
            return self._env_fallback(path, key)
    
    def _get_1password(self, path: str, key: str) -> Optional[str]:
        try:
            result = subprocess.run(
                ["op", "read", f"op://{path}/{key}"],
                capture_output=True, text=True, timeout=10
            )
            return result.stdout.strip()
        except Exception:
            return self._env_fallback(path, key)
    
    def _env_fallback(self, path: str, key: str) -> Optional[str]:
        """环境变量 fallback。path=secret/wordpress/site1 -> WP_SECRET_SITE1"""
        parts = path.split("/")
        site = parts[-1].upper().replace("-", "_")
        env_key = f"WP_{key.upper()}_{site}"
        val = os.environ.get(env_key) or os.environ.get(key.upper())
        return val
    
    def store(self, path: str, key: str, value: str):
        """存储密钥（仅支持 HashiCorp Vault）"""
        if self.mode == "hashicorp":
            subprocess.run(
                ["vault", "kv", "put", path, f"{key}={value}"],
                capture_output=True, timeout=10
            )
