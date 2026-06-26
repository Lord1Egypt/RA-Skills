"""配置管理模块"""

import os
import re
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

# .env 加载（默认禁用，需显式 opt-in）
def _load_dotenv():
    """从项目根目录的 .env 文件加载环境变量（默认不加载，需设置 CLOUD_DOC_MONITOR_LOAD_DOTENV=1 启用）"""
    # 默认不加载，必须显式启用
    if os.environ.get("CLOUD_DOC_MONITOR_LOAD_DOTENV", "").lower() not in ("1", "true", "yes"):
        return
    
    for search_dir in [Path.cwd(), Path(__file__).parent.parent]:
        env_file = search_dir / ".env"
        if env_file.exists():
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, _, value = line.partition("=")
                        key, value = key.strip(), value.strip()
                        if not os.environ.get(key):
                            os.environ[key] = value
            break

_load_dotenv()


CONFIG_PATH_ENV = "CLOUD_DOC_MONITOR_CONFIG"


class ConfigError(Exception):
    pass


class Config:
    DEFAULT_CONFIG: Dict[str, Any] = {
        "crawler": {
            "base_url": "https://help.aliyun.com",
            "request_delay": 1.0,
            "max_retries": 3,
            "timeout": 30,
        },
        "monitor_clouds": {
            "aliyun": {"enabled": True, "products": ["/vpc"]},
            "tencent": {"enabled": False, "products": []},
            "baidu": {"enabled": False, "products": []},
            "volcano": {"enabled": False, "products": []},
        },
        "notifications": [
            {"type": "file", "enabled": True, "output_dir": "./notifications"},
        ],
        "storage": {
            "type": "sqlite",
            "database": "./data/cloud_docs.db",
            "keep_versions": 10,
        },
        "logging": {"level": "INFO"},
    }

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = resolve_config_path(config_path)
        self._config: Dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        if not Path(self.config_path).exists():
            import copy
            self._config = self._replace_env_vars(copy.deepcopy(self.DEFAULT_CONFIG))
            return
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                raw_config = yaml.safe_load(f)
            self._config = self._replace_env_vars(raw_config)
            self.validate()
        except yaml.YAMLError as e:
            raise ConfigError(f"配置文件格式错误: {e}")
        except ConfigError:
            raise
        except Exception as e:
            raise ConfigError(f"加载配置文件失败: {e}")

    def _replace_env_vars(self, obj: Any) -> Any:
        """递归替换配置中的环境变量
        
        支持语法：
        - ${VAR} - 使用环境变量 VAR，如果不存在则为空字符串
        - ${VAR:default} - 使用环境变量 VAR，如果不存在则使用 default
        - ${VAR1:${VAR2}} - 嵌套：优先使用 VAR1，如果不存在则使用 VAR2
        """
        if isinstance(obj, dict):
            return {k: self._replace_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._replace_env_vars(item) for item in obj]
        elif isinstance(obj, str):
            # 支持嵌套环境变量替换，最多递归 3 次
            result = obj
            for _ in range(3):
                pattern = r'\$\{([^}:]+)(?::([^}]*))?\}'
                def replacer(match):
                    var_name = match.group(1)
                    default_value = match.group(2) if match.group(2) is not None else ""
                    return os.environ.get(var_name, default_value)
                new_result = re.sub(pattern, replacer, result)
                if new_result == result:  # 没有更多替换
                    break
                result = new_result
            return result
        return obj

    def validate(self) -> None:
        for section in ['crawler', 'notifications', 'storage']:
            if section not in self._config:
                raise ConfigError(f"缺少必需的配置节: {section}")

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def set(self, key: str, value: Any) -> None:
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value

    def get_all(self) -> Dict[str, Any]:
        return self._config.copy()


_config_instance: Optional[Config] = None


def resolve_config_path(config_path: Optional[str] = None) -> str:
    explicit = str(config_path or "").strip()
    if explicit:
        return explicit
    env_path = str(os.environ.get(CONFIG_PATH_ENV, "") or "").strip()
    if env_path:
        return env_path
    return "config.yaml"


def reset_config() -> None:
    global _config_instance
    _config_instance = None


def get_config(config_path: Optional[str] = None, reload: bool = False) -> Config:
    global _config_instance
    resolved_path = resolve_config_path(config_path)
    if reload or _config_instance is None or _config_instance.config_path != resolved_path:
        _config_instance = Config(resolved_path)
    return _config_instance
