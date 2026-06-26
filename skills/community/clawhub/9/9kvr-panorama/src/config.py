"""配置管理模块"""

import json
import os
from typing import Any, Dict, Optional


class ConfigService:
    """配置服务类（仅认证与超时）"""

    def __init__(self):
        # 不再维护域名配置，域名仅由 VRAPI 网络服务器内置控制
        self._config: Dict[str, Any] = {
            "api": {
                "timeout": 5000,
            },
            "auth": {
                "token": None,
                "uid": None,
            },
        }

        self._load_from_session()
        self._load_from_env()

    def _load_from_env(self) -> None:
        """从环境变量加载配置（最高优先级）"""
        if os.getenv("API_TIMEOUT"):
            try:
                self._config["api"]["timeout"] = int(os.getenv("API_TIMEOUT"))
            except ValueError:
                pass

        if os.getenv("AUTH_TOKEN"):
            self._config["auth"]["token"] = os.getenv("AUTH_TOKEN")
        if os.getenv("AUTH_UID"):
            self._config["auth"]["uid"] = os.getenv("AUTH_UID")

    def _load_from_session(self) -> None:
        """从 vr-api session 文件加载认证信息"""
        session_path = os.path.join(self.auth_dir, "vr-session.json")
        if not os.path.exists(session_path):
            return
        try:
            with open(session_path, "r", encoding="utf-8") as f:
                session = json.load(f)
                if not self._config["auth"]["uid"] and session.get("uid"):
                    self._config["auth"]["uid"] = session["uid"]
                if not self._config["auth"]["token"] and session.get("token"):
                    self._config["auth"]["token"] = session["token"]
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    @property
    def timeout(self) -> int:
        """请求超时时间（毫秒）"""
        return self._config.get("api", {}).get("timeout", 5000)

    @property
    def token(self) -> Optional[str]:
        """认证 Token"""
        return self._config.get("auth", {}).get("token")

    @property
    def uid(self) -> Optional[str]:
        """用户 UID"""
        return self._config.get("auth", {}).get("uid")

    @property
    def cache_dir(self) -> str:
        """Skills/MCP 缓存目录 - ~/.9kvr/skills/cache"""
        return os.path.expanduser("~/.9kvr/skills/cache")

    @property
    def client_dir(self) -> str:
        """VRAPI 网络服务器目录 - ~/.9kvr/client"""
        return os.path.expanduser("~/.9kvr/client")

    @property
    def auth_dir(self) -> str:
        """认证信息目录 - ~/.9kvr/auth"""
        return os.path.expanduser("~/.9kvr/auth")

    def get(self, *keys: str, default: Any = None) -> Any:
        """获取配置值"""
        value = self._config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def set(self, value: Any, *keys: str) -> None:
        """设置配置值（仅运行时内存生效）"""
        if len(keys) == 0:
            return
        target = self._config
        for key in keys[:-1]:
            if key not in target:
                target[key] = {}
            target = target[key]
        target[keys[-1]] = value

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self._config.copy()


_config_instance: Optional[ConfigService] = None


def get_config() -> ConfigService:
    """获取全局配置实例"""
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigService()
    return _config_instance


def reset_config() -> None:
    """重置全局配置"""
    global _config_instance
    _config_instance = None

