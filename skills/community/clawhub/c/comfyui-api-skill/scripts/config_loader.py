#!/usr/bin/env python3
"""
配置加载器

功能：
1. 从 config/config.yaml 加载配置
2. 支持配置优先级：命令行参数 > 配置文件 > 环境变量 > 默认值
3. 提供配置验证和默认值填充

使用示例：
    from config_loader import ConfigLoader
    
    config = ConfigLoader()
    server_url = config.get('server.url')
    timeout = config.get('execution.timeout', default=300)
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import yaml
except ImportError:
    print("警告：缺少 pyyaml 库，将使用默认配置")
    print("建议运行：pip install pyyaml>=6.0")
    yaml = None


class ConfigLoader:
    """配置加载器"""
    
    def __init__(self, config_path: str = None):
        """
        初始化配置加载器
        
        Args:
            config_path: 配置文件路径（默认：config/config.yaml）
        """
        # 确定配置文件路径
        if config_path:
            self.config_path = Path(config_path)
        else:
            # 相对于脚本所在目录
            script_dir = Path(__file__).parent
            self.config_path = script_dir.parent / "config" / "config.yaml"
        
        # 加载配置
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        加载配置文件
        
        Returns:
            配置字典
        """
        if not self.config_path.exists():
            print(f"警告：配置文件不存在: {self.config_path}")
            print("将使用默认配置")
            return self._get_default_config()
        
        if yaml is None:
            print("将使用默认配置")
            return self._get_default_config()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
                return config
        except Exception as e:
            print(f"错误：无法读取配置文件: {str(e)}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        获取默认配置
        
        Returns:
            默认配置字典
        """
        return {
            "server": {
                "url": "http://127.0.0.1:8188",
                "api_key": None
            },
            "execution": {
                "timeout": 300,
                "video_timeout": 900,
                "poll_interval": 2,
                "max_retries": 3
            },
            "paths": {
                "workflows_dir": "workflows",
                "output_dir": "output",
                "temp_dir": "temp"
            },
            "logging": {
                "level": "INFO",
                "file": None
            }
        }
    
    def get(
        self,
        key: str,
        default: Any = None,
        env_var: str = None,
        cli_value: Any = None
    ) -> Any:
        """
        获取配置值（支持优先级）
        
        Args:
            key: 配置键（支持点号分隔，如 'server.url'）
            default: 默认值
            env_var: 环境变量名
            cli_value: 命令行参数值
            
        Returns:
            配置值（优先级：cli_value > 配置文件 > env_var > default）
        """
        # 1. 优先使用命令行参数
        if cli_value is not None:
            return cli_value
        
        # 2. 从配置文件读取
        value = self._get_nested_value(self.config, key)
        if value is not None:
            return value
        
        # 3. 从环境变量读取
        if env_var:
            env_value = os.getenv(env_var)
            if env_value is not None:
                return env_value
        
        # 4. 返回默认值
        return default
    
    def _get_nested_value(self, config: Dict[str, Any], key: str) -> Any:
        """
        获取嵌套配置值
        
        Args:
            config: 配置字典
            key: 配置键（支持点号分隔）
            
        Returns:
            配置值
        """
        keys = key.split('.')
        value = config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None
        
        return value
    
    def get_server_url(self, cli_value: str = None) -> str:
        """
        获取 ComfyUI 服务地址
        
        Args:
            cli_value: 命令行参数值
            
        Returns:
            服务地址
        """
        return self.get(
            'server.url',
            default='http://127.0.0.1:8188',
            env_var='COMFYUI_SERVER_URL',
            cli_value=cli_value
        )
    
    def get_api_key(self, cli_value: str = None) -> Optional[str]:
        """
        获取 API 密钥
        
        Args:
            cli_value: 命令行参数值
            
        Returns:
            API 密钥
        """
        return self.get(
            'server.api_key',
            default=None,
            env_var='COMFYUI_API_KEY',
            cli_value=cli_value
        )
    
    def get_timeout(self, cli_value: int = None, for_video: bool = False) -> int:
        """
        获取超时时间
        
        Args:
            cli_value: 命令行参数值
            for_video: 是否用于视频生成
            
        Returns:
            超时时间（秒）
        """
        if for_video:
            return self.get(
                'execution.video_timeout',
                default=900,
                cli_value=cli_value
            )
        else:
            return self.get(
                'execution.timeout',
                default=300,
                cli_value=cli_value
            )
    
    def get_workflows_dir(self) -> Path:
        """
        获取工作流目录路径
        
        Returns:
            工作流目录路径
        """
        workflows_dir = self.get('paths.workflows_dir', default='workflows')
        
        # 转换为绝对路径
        script_dir = Path(__file__).parent
        return (script_dir.parent / workflows_dir).resolve()
    
    def get_output_dir(self) -> Path:
        """
        获取输出目录路径
        
        Returns:
            输出目录路径
        """
        output_dir = self.get('paths.output_dir', default='output')
        
        # 转换为绝对路径
        script_dir = Path(__file__).parent
        return (script_dir.parent / output_dir).resolve()
    
    def ensure_directories(self):
        """
        确保必要的目录存在
        """
        dirs = [
            self.get_workflows_dir(),
            self.get_output_dir()
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)


# 全局配置实例
_config_instance = None


def get_config(config_path: str = None) -> ConfigLoader:
    """
    获取全局配置实例
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        配置加载器实例
    """
    global _config_instance
    
    if _config_instance is None:
        _config_instance = ConfigLoader(config_path)
    
    return _config_instance


if __name__ == "__main__":
    # 测试配置加载
    config = get_config()
    
    print("配置文件路径:", config.config_path)
    print("服务地址:", config.get_server_url())
    print("API 密钥:", config.get_api_key())
    print("超时时间:", config.get_timeout())
    print("工作流目录:", config.get_workflows_dir())
    print("输出目录:", config.get_output_dir())
    
    # 确保目录存在
    config.ensure_directories()
    print("✓ 目录已创建")
