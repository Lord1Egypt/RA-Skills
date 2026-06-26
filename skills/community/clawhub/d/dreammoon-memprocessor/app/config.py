"""配置管理"""
from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用信息
    APP_NAME: str = "DreamMoon Memory Processor"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    WORKERS: int = 1
    
    # 存储路径
    BASE_DIR: Path = Path("/root/.openclaw")
    DATA_DIR: Path = BASE_DIR / "data"
    
    # L1 - Redis (热存储)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    REDIS_TTL_SECONDS: int = 3600  # 1小时TTL
    
    # L2 - SQLite (温存储)
    SQLITE_PATH: Path = DATA_DIR / "l2_warm.db"
    
    # L3 - 文件系统 (冷存储)
    L3_MEMORY_DIR: Path = BASE_DIR / "workspace" / "memory"
    L3_DAILY_DIR: Path = L3_MEMORY_DIR / "daily"
    L3_PROJECTS_DIR: Path = L3_MEMORY_DIR / "projects"
    L3_DECISIONS_DIR: Path = L3_MEMORY_DIR / "decisions"
    
    # L4 - FAISS + 归档
    L4_ARCHIVE_DIR: Path = BASE_DIR / "archive" / "l4_cold"
    L4_VECTOR_INDEX_PATH: Path = DATA_DIR / "l4_vectors.faiss"
    L4_METADATA_PATH: Path = DATA_DIR / "l4_metadata.json"
    
    # 向量模型
    EMBEDDING_MODEL: str = "paraphrase-multilingual-MiniLM-L12-v2"
    EMBEDDING_DIMENSION: int = 384
    
    # 沉淀配置
    IMPORTANCE_IMMEDIATE: int = 70
    IMPORTANCE_DAILY: int = 40
    ARCHIVE_DAYS: int = 90
    
    # 存储限制配置 - 超过阈值时提醒用户
    L1_MAX_SIZE_MB: int = 100          # Redis 热存储限制 (100MB)
    L2_MAX_ENTRIES: int = 10000        # SQLite 条目数限制
    L2_MAX_SIZE_MB: int = 500          # SQLite 数据库大小限制 (500MB)
    L3_MAX_SIZE_MB: int = 1000         # Markdown 文件总大小限制 (1GB)
    L3_MAX_FILES: int = 1000           # Markdown 文件数量限制
    L4_MAX_SIZE_MB: int = 2000         # 向量索引大小限制 (2GB)
    L4_MAX_VECTORS: int = 500000       # 向量数量限制
    ARCHIVE_MAX_SIZE_MB: int = 5000    # L4 归档总大小限制 (5GB)
    
    # 告警阈值 (百分比，超过此比例触发提醒)
    STORAGE_WARNING_THRESHOLD: int = 80    # 80% 时警告
    STORAGE_CRITICAL_THRESHOLD: int = 95   # 95% 时严重告警
    
    # 调度配置
    DAILY_PERSISTENCE_HOUR: int = 23
    DAILY_PERSISTENCE_MINUTE: int = 50
    WEEKLY_ARCHIVE_DAY: int = 6  # 周日 (0=周一, 6=周日)
    WEEKLY_ARCHIVE_HOUR: int = 0
    
    # 日志
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # 安全
    API_KEY: str = ""  # 可选的API密钥
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()


# 全局配置对象
settings = get_settings()
