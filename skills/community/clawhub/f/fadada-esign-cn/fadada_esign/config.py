#!/usr/bin/env python3
"""
配置文件管理

支持从以下位置加载配置（优先级从高到低）：
1. 显式传入的参数
2. 环境变量
3. 配置文件（~/.fadada/config.json 或项目目录下的 .fadada.json）
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any


class Config:
    """配置管理器"""
    
    # 默认配置文件路径
    GLOBAL_CONFIG_PATH = Path.home() / ".fadada" / "config.json"
    LOCAL_CONFIG_FILES = [".fadada.json", "fadada_config.json"]
    
    # 环境变量前缀
    ENV_PREFIX = "FADADA_"
    
    def __init__(
        self,
        app_id: Optional[str] = None,
        app_secret: Optional[str] = None,
        open_corp_id: Optional[str] = None,
        server_url: Optional[str] = None,
        sandbox: bool = False
    ):
        """
        初始化配置
        
        配置优先级：
        1. 显式传入的参数
        2. 环境变量
        3. 配置文件
        """
        self._config = {}
        
        # 1. 加载配置文件
        self._load_from_file()
        
        # 2. 加载环境变量
        self._load_from_env()
        
        # 3. 应用显式传入的参数
        if app_id:
            self._config["app_id"] = app_id
        if app_secret:
            self._config["app_secret"] = app_secret
        if open_corp_id:
            self._config["open_corp_id"] = open_corp_id
        if server_url:
            self._config["server_url"] = server_url
        if sandbox:
            self._config["sandbox"] = sandbox
    
    def _load_from_file(self):
        """从配置文件加载"""
        # 检查全局配置
        if self.GLOBAL_CONFIG_PATH.exists():
            try:
                with open(self.GLOBAL_CONFIG_PATH, 'r', encoding='utf-8') as f:
                    self._config.update(json.load(f))
            except Exception:
                pass
        
        # 检查本地配置（当前目录及父目录）
        current_dir = Path.cwd()
        for config_file in self.LOCAL_CONFIG_FILES:
            config_path = current_dir / config_file
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        self._config.update(json.load(f))
                except Exception:
                    pass
                break
    
    def _load_from_env(self):
        """从环境变量加载"""
        env_mapping = {
            "APP_ID": "app_id",
            "APP_SECRET": "app_secret",
            "OPEN_CORP_ID": "open_corp_id",
            "SERVER_URL": "server_url",
            "SANDBOX": "sandbox"
        }
        
        for env_key, config_key in env_mapping.items():
            env_value = os.getenv(f"{self.ENV_PREFIX}{env_key}")
            if env_value:
                if config_key == "sandbox":
                    self._config[config_key] = env_value.lower() in ("true", "1", "yes")
                else:
                    self._config[config_key] = env_value
    
    @property
    def app_id(self) -> Optional[str]:
        return self._config.get("app_id")
    
    @property
    def app_secret(self) -> Optional[str]:
        return self._config.get("app_secret")
    
    @property
    def open_corp_id(self) -> Optional[str]:
        return self._config.get("open_corp_id")
    
    @property
    def server_url(self) -> Optional[str]:
        return self._config.get("server_url")
    
    @property
    def sandbox(self) -> bool:
        return self._config.get("sandbox", False)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "app_id": self.app_id,
            "app_secret": self.app_secret,
            "open_corp_id": self.open_corp_id,
            "server_url": self.server_url,
            "sandbox": self.sandbox
        }
    
    def is_valid(self) -> bool:
        """检查配置是否完整"""
        return all([
            self.app_id,
            self.app_secret,
            self.open_corp_id
        ])
    
    def save(self, path: Optional[str] = None):
        """
        保存配置到文件
        
        Args:
            path: 保存路径（默认保存到全局配置）
        """
        if path is None:
            path = self.GLOBAL_CONFIG_PATH
        
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # 只保存非敏感配置
        save_config = {
            "app_id": self.app_id,
            "open_corp_id": self.open_corp_id,
            "server_url": self.server_url,
            "sandbox": self.sandbox
        }
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(save_config, f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load(cls, path: Optional[str] = None) -> "Config":
        """
        从文件加载配置
        
        Args:
            path: 配置文件路径
            
        Returns:
            Config 实例
        """
        if path:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return cls(**data)
        return cls()


def setup_config_interactive() -> Config:
    """
    交互式配置设置
    
    引导用户输入配置信息
    """
    print("=" * 50)
    print("法大大电子签 - 配置设置")
    print("=" * 50)
    print()
    
    app_id = input("请输入 App ID: ").strip()
    app_secret = input("请输入 App Secret: ").strip()
    open_corp_id = input("请输入 Open Corp ID: ").strip()
    
    use_sandbox = input("是否使用沙箱环境? (y/N): ").strip().lower() == 'y'
    
    config = Config(
        app_id=app_id,
        app_secret=app_secret,
        open_corp_id=open_corp_id,
        sandbox=use_sandbox
    )
    
    # 保存配置
    save_global = input("是否保存为全局配置? (Y/n): ").strip().lower() != 'n'
    if save_global:
        config.save()
        print(f"\n配置已保存到: {Config.GLOBAL_CONFIG_PATH}")
    
    return config
