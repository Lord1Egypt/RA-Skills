"""
Claw-News Configuration Manager
配置管理模块
"""

import os
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Optional


def _load_dotenv():
    """从 .env 文件加载环境变量"""
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and value and key not in os.environ:
                        os.environ[key] = value


# 模块加载时执行
_load_dotenv()


@dataclass
class Interest:
    """关注项数据结构"""
    id: str
    type: str  # 'topic', 'person', 'keyword'
    value: str
    keywords: List[str] = field(default_factory=list)
    priority: str = "medium"  # 'high', 'medium', 'low'
    sources: List[str] = field(default_factory=lambda: ["all"])
    created_at: Optional[str] = None
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)


@dataclass
class Settings:
    """全局设置"""
    daily_digest_time: str = "09:00"
    timezone: str = "Asia/Shanghai"
    max_results_per_interest: int = 10
    search_lookback_hours: int = 24
    delivery_channel: str = "slack"
    slack_channel: str = "#general"
    api_timeout: int = 30
    enable_fallback: bool = True
    
    def to_dict(self):
        return asdict(self)


class Config:
    """配置管理器"""
    
    # 路径配置
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    INTEREST_FILE = DATA_DIR / "interest_list.json"
    CACHE_FILE = DATA_DIR / "search_cache.json"
    
    # API 优先级（依次尝试）
    API_PRIORITY = ["minimax", "tavily"]
    
    def __init__(self):
        self._ensure_dirs()
        self._api_keys = self._load_api_keys()
        self._settings = self._load_settings()
    
    def _ensure_dirs(self):
        """确保目录存在"""
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    def _load_api_keys(self) -> dict:
        """从环境变量加载 API Keys"""
        return {
            "minimax": os.getenv("MINIMAX_API_KEY", ""),
            "tavily": os.getenv("TAVILY_API_KEY", ""),
        }
    
    def _load_settings(self) -> Settings:
        """从环境变量加载设置"""
        return Settings(
            daily_digest_time=os.getenv("DAILY_DIGEST_TIME", "09:00"),
            timezone=os.getenv("TIMEZONE", "Asia/Shanghai"),
            max_results_per_interest=int(os.getenv("MAX_RESULTS", "10")),
            search_lookback_hours=int(os.getenv("LOOKBACK_HOURS", "24")),
            delivery_channel=os.getenv("DELIVERY_CHANNEL", "slack"),
            slack_channel=os.getenv("SLACK_CHANNEL", "#general"),
        )
    
    @property
    def api_keys(self) -> dict:
        """获取 API Keys"""
        return self._api_keys
    
    @property
    def settings(self) -> Settings:
        """获取设置"""
        return self._settings
    
    def get_available_apis(self) -> List[str]:
        """获取可用的 API 列表"""
        return [name for name, key in self._api_keys.items() if key]
    
    def load_interests(self) -> dict:
        """加载关注列表"""
        if not self.INTEREST_FILE.exists():
            return self._create_default_interests()
        
        try:
            with open(self.INTEREST_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return self._create_default_interests()
    
    def save_interests(self, data: dict):
        """保存关注列表"""
        with open(self.INTEREST_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _create_default_interests(self) -> dict:
        """创建默认关注列表"""
        import uuid
        from datetime import datetime
        
        default_data = {
            "version": "1.0",
            "updated_at": datetime.now().isoformat(),
            "interests": [
                {
                    "id": str(uuid.uuid4())[:8],
                    "type": "topic",
                    "value": "人工智能",
                    "keywords": ["AI", "大模型", "AGI", "机器学习"],
                    "priority": "high",
                    "sources": ["tech", "news"],
                    "created_at": datetime.now().isoformat()
                },
                {
                    "id": str(uuid.uuid4())[:8],
                    "type": "topic",
                    "value": "科技动态",
                    "keywords": ["科技", "互联网", "初创公司", "融资"],
                    "priority": "medium",
                    "sources": ["tech"],
                    "created_at": datetime.now().isoformat()
                }
            ],
            "settings": self._settings.to_dict()
        }
        self.save_interests(default_data)
        return default_data
    
    def load_cache(self) -> dict:
        """加载搜索缓存"""
        if not self.CACHE_FILE.exists():
            return {"version": "1.0", "searches": {}}
        
        try:
            with open(self.CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {"version": "1.0", "searches": {}}
    
    def save_cache(self, data: dict):
        """保存搜索缓存"""
        with open(self.CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


# 全局配置实例
config = Config()
