# -*- coding: utf-8 -*-
"""
Auto-Claw 配置模块

集中管理所有配置项，支持：
- 环境变量加载 (.env)
- 配置文件 (YAML/JSON)
- Vault动态密钥
"""
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()


@dataclass
class VaultConfig:
    """Vault密钥库配置"""
    enabled: bool = False
    url: str = "http://localhost:8200"
    token: Optional[str] = None
    mount_point: str = "secret"
    
    def __post_init__(self):
        # 从环境变量覆盖
        self.enabled = os.getenv("VAULT_ENABLED", "false").lower() == "true"
        self.url = os.getenv("VAULT_URL", self.url)
        self.token = os.getenv("VAULT_TOKEN", self.token)


@dataclass
class WordPressSite:
    """单个WordPress站点配置"""
    name: str
    url: str
    username: str = ""
    # 密码从Vault或环境变量获取，不硬编码
    password_env_key: str = ""
    
    @property
    def has_credentials(self) -> bool:
        return bool(self.username and self.password_env_key)


@dataclass
class PipelineConfig:
    """Pipeline配置"""
    require_approval: bool = True  # 是否需要人工审批
    auto_retry: bool = True        # 失败自动重试
    max_retries: int = 3


@dataclass
class AuditConfig:
    """审计日志配置"""
    enabled: bool = True
    log_dir: Path = field(default_factory=lambda: Path("logs/audit"))
    retention_days: int = 90
    verbose: bool = True  # 详细模式，记录请求/响应body


@dataclass
class Settings:
    """主配置类"""
    env: str = "development"
    debug: bool = False
    
    vault: VaultConfig = field(default_factory=VaultConfig)
    pipeline: PipelineConfig = field(default_factory=PipelineConfig)
    audit: AuditConfig = field(default_factory=AuditConfig)
    
    # WordPress站点列表
    sites: list[WordPressSite] = field(default_factory=list)
    
    @classmethod
    def from_env(cls) -> "Settings":
        """从环境变量构建配置"""
        settings = cls()
        settings.env = os.getenv("APP_ENV", "development")
        settings.debug = os.getenv("DEBUG", "false").lower() == "true"
        
        # 从环境变量加载站点配置 (逗号分隔: name:url,name:url)
        sites_raw = os.getenv("WP_SITES", "")
        if sites_raw:
            for site_spec in sites_raw.split(","):
                if ":" in site_spec:
                    name, url = site_spec.split(":", 1)
                    settings.sites.append(WordPressSite(
                        name=name.strip(),
                        url=url.strip()
                    ))
        
        return settings


# 全局配置实例
settings = Settings.from_env()
