"""
点点数据安卓榜单爬虫
获取安卓各渠道的上架榜和下架榜
https://app.diandian.com/
"""

import httpx
from typing import List, Dict, Optional
from pathlib import Path
import yaml
from datetime import datetime

from .base import BaseRanker, RankApp, NewApp, OfflineApp
from utils.logger import setup_logger

logger = setup_logger()


class DiandianAndroidRanker(BaseRanker):
    """点点数据安卓榜单爬虫"""
    
    # 安卓渠道映射
    CHANNELS = {
        "huawei": {"name": "华为", "id": "huawei"},
        "xiaomi": {"name": "小米", "id": "xiaomi"},
        "tencent": {"name": "应用宝", "id": "yingyongbao"},
        "oppo": {"name": "OPPO", "id": "oppo"},
        "vivo": {"name": "vivo", "id": "vivo"},
        "baidu": {"name": "百度", "id": "baidu"},
        "qihoo360": {"name": "360", "id": "360"},
        "wandoujia": {"name": "豌豆荚", "id": "wandoujia"},
    }
    
    def __init__(self, channel: str = "huawei"):
        """
        初始化
        
        Args:
            channel: 渠道名称 (huawei/xiaomi/tencent/oppo/vivo/baidu/qihoo360/wandoujia)
        """
        super().__init__(f"点点数据 - {self.CHANNELS.get(channel, {}).get('name', channel)}")
        self.channel = channel
        self.base_url = "https://app.diandian.com/api"
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """加载配置"""
        config_path = Path(__file__).parent.parent.parent / "config" / "diandian.yaml"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {"token": ""}
    
    async def fetch_rising_list(self, limit: int = 100) -> List[RankApp]:
        """
        获取上升榜（暂时返回空列表）
        
        Args:
            limit: 数量限制
            
        Returns:
            上升榜 App 列表
        """
        # 点点数据安卓渠道暂不支持上升榜
        logger.info(f"⚠️ {self.channel} 上升榜暂不支持")
        return []
    
    async def fetch_new_apps(self, limit: int = 100) -> List[NewApp]:
        """
        获取新上架 App
        
        Args:
            limit: 数量限制
            
        Returns:
            新上架 App 列表
        """
        channel_id = self.CHANNELS.get(self.channel, {}).get("id", self.channel)
        
        url = f"{self.base_url}/rank/new"
        params = {
            "platform": "android",
            "channel": channel_id,
            "limit": limit,
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Authorization": f"Bearer {self.config.get('token', '')}",
            "Accept": "application/json",
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    apps = self._parse_new_apps(data.get("data", []))
                    logger.info(f"✅ {self.channel} 新上架：{len(apps)} 个")
                    return apps
                
                logger.warning(f"❌ {self.channel} 新上架 HTTP {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ {self.channel} 新上架异常：{e}")
            return []
    
    async def fetch_offline_apps(self, limit: int = 100) -> List[OfflineApp]:
        """
        获取新下架 App
        
        Args:
            limit: 数量限制
            
        Returns:
            下架 App 列表
        """
        channel_id = self.CHANNELS.get(self.channel, {}).get("id", self.channel)
        
        url = f"{self.base_url}/rank/offline"
        params = {
            "platform": "android",
            "channel": channel_id,
            "limit": limit,
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Authorization": f"Bearer {self.config.get('token', '')}",
            "Accept": "application/json",
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    apps = self._parse_offline_apps(data.get("data", []))
                    logger.info(f"✅ {self.channel} 下架：{len(apps)} 个")
                    return apps
                
                logger.warning(f"❌ {self.channel} 下架 HTTP {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ {self.channel} 下架异常：{e}")
            return []
    
    def _parse_new_apps(self, data: list) -> List[NewApp]:
        """解析新上架数据"""
        result = []
        for item in data[:100]:
            app = NewApp(
                app_name=item.get("name", ""),
                package_name=item.get("bundle_id", "") or item.get("package_name", ""),
                developer=item.get("developer", ""),
                category=item.get("category", ""),
                release_date=item.get("release_date", "") or item.get("publish_date", ""),
            )
            result.append(app)
        return result
    
    def _parse_offline_apps(self, data: list) -> List[OfflineApp]:
        """解析下架数据"""
        result = []
        for item in data[:100]:
            app = OfflineApp(
                app_name=item.get("name", ""),
                package_name=item.get("bundle_id", "") or item.get("package_name", ""),
                developer=item.get("developer", ""),
                category=item.get("category", ""),
                offline_date=item.get("offline_date", "") or datetime.now().strftime("%Y-%m-%d"),
            )
            result.append(app)
        return result
    
    async def fetch_all_channels_new_apps(self, limit: int = 50) -> Dict[str, List[NewApp]]:
        """
        获取所有渠道的新上架 App
        
        Args:
            limit: 每个渠道的数量限制
            
        Returns:
            {渠道名：[新上架 App]}
        """
        result = {}
        
        for channel in self.CHANNELS.keys():
            self.channel = channel
            apps = await self.fetch_new_apps(limit)
            result[channel] = apps
            logger.info(f"📊 {self.CHANNELS[channel]['name']} 新上架：{len(apps)} 个")
        
        return result
    
    async def fetch_all_channels_offline_apps(self, limit: int = 50) -> Dict[str, List[OfflineApp]]:
        """
        获取所有渠道的下架 App
        
        Args:
            limit: 每个渠道的数量限制
            
        Returns:
            {渠道名：[下架 App]}
        """
        result = {}
        
        for channel in self.CHANNELS.keys():
            self.channel = channel
            apps = await self.fetch_offline_apps(limit)
            result[channel] = apps
            logger.info(f"📊 {self.CHANNELS[channel]['name']} 下架：{len(apps)} 个")
        
        return result
