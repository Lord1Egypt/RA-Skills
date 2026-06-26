"""
榜单爬虫 - 抽象基类
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class RankApp:
    """榜单 App 数据"""
    rank: int  # 排名
    app_name: str  # 应用名称
    package_name: str  # 包名
    developer: str  # 开发者
    category: str  # 分类
    change: int = 0  # 排名变化 (正数=上升，负数=下降)
    
    def __dict__(self):
        return {
            "rank": self.rank,
            "app_name": self.app_name,
            "package_name": self.package_name,
            "developer": self.developer,
            "category": self.category,
            "change": self.change,
        }


@dataclass
class NewApp:
    """新上架 App"""
    app_name: str
    package_name: str
    developer: str
    category: str
    release_date: str  # 上架日期


@dataclass
class OfflineApp:
    """新下架 App"""
    app_name: str
    package_name: str
    developer: str
    category: str
    offline_date: str  # 下架日期


class BaseRanker(ABC):
    """榜单爬虫基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.base_url = ""
    
    @abstractmethod
    async def fetch_rising_list(self, limit: int = 100) -> List[RankApp]:
        """获取上升榜"""
        pass
    
    @abstractmethod
    async def fetch_new_apps(self, limit: int = 100) -> List[NewApp]:
        """获取新上架 App"""
        pass
    
    @abstractmethod
    async def fetch_offline_apps(self, limit: int = 100) -> List[OfflineApp]:
        """获取新下架 App"""
        pass
    
    async def fetch_all(self, rising_limit: int = 100, new_limit: int = 100) -> dict:
        """获取全部数据"""
        rising = await self.fetch_rising_list(rising_limit)
        new_apps = await self.fetch_new_apps(new_limit)
        offline_apps = await self.fetch_offline_apps(new_limit)
        
        return {
            "platform": self.name,
            "fetch_time": datetime.now().isoformat(),
            "rising_list": rising,
            "new_apps": new_apps,
            "offline_apps": offline_apps,
        }
