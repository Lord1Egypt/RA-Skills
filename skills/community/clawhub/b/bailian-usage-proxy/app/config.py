"""
配置管理（简化版，无外部依赖）
"""

import os
from functools import lru_cache


class Settings:
    """应用配置"""
    
    def __init__(self):
        # 阿里百炼配置
        self.bailian_api_key = os.getenv("BAILIAN_API_KEY", "")
        self.bailian_base_url = os.getenv("BAILIAN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        
        # 代理服务配置
        self.proxy_host = os.getenv("PROXY_HOST", "0.0.0.0")
        self.proxy_port = int(os.getenv("PROXY_PORT", "8080"))
        self.admin_port = int(os.getenv("ADMIN_PORT", "8081"))
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        
        # 数据库配置（默认SQLite）
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./data/bailian_proxy.db")
        
        # Redis配置（可选）
        self.redis_url = os.getenv("REDIS_URL", None)
        
        # 安全配置
        self.secret_key = os.getenv("SECRET_KEY", "change-me-in-production")
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        
        # 日志配置
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_file = os.getenv("LOG_FILE", None)


@lru_cache()
def get_settings():
    """获取配置（单例）"""
    return Settings()
