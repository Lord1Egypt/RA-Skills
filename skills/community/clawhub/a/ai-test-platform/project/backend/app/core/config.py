"""
配置管理模块
"""

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """应用配置"""

    # 应用基础配置
    APP_NAME: str = "AI 自动化测试平台"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://root:root123@localhost:3306/ai_test_platform"

    # DeepSeek API 配置
    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com"

    # 安全配置
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    AES_KEY_PREFIX: str = "yanghua"
    AES_KEY_SUFFIX: str = "360sb"

    # AI 配置
    AI_MAX_RETRIES: int = 2
    AI_TIMEOUT: int = 30

    # 测试执行配置
    EXECUTE_TIMEOUT: int = 300  # 5分钟
    MAX_CONCURRENT_TESTS: int = 5

    class Config:
        env_file = ".env"
        case_sensitive = True

# 创建全局配置实例
settings = Settings()
