"""
苹果 App Store 榜单爬虫
使用苹果官方 RSS API 获取中国区应用榜单

策略:
1. 爬取总榜 (前 200)

API 文档:
- 免费榜: https://rss.appstore.apple.com/api/rss/iosapplications/topfreeapplications/limit=200/genre=0/json
- 付费榜: https://rss.appstore.apple.com/api/rss/iosapplications/toppaidapplications/limit=200/genre=0/json
- 新上架: https://rss.appstore.apple.com/api/rss/iosapplications/newapplications/limit=200/genre=0/json

无需 API Key，完全免费！
"""

import httpx
from typing import List, Dict, Optional, Set
from datetime import datetime
import structlog

logger = structlog.get_logger()


class AppleRanker:
    """苹果 App Store 榜单爬虫"""
    
    # 中国区基础 URL
    # 使用 iTunes API (rss.appstore.apple.com DNS 解析有问题)
    BASE_URL = "https://itunes.apple.com/cn/rss"
    COUNTRY = "cn"  # 中国区
    
    # 榜单类型
    CHART_TYPES = {
        "top_free": "topfreeapplications",
        "top_paid": "toppaidapplications",
        "new_free": "newfreeapplications",
        "new_paid": "newpaidapplications",
    }
    
    # 所有分类 ID（中国区）
    ALL_CATEGORIES = {
        "all": 0,                    # 总榜
        # 商务
        "business": 6000,
        # 天气
        "weather": 6001,
        # 工具
        "utilities": 6002,
        # 旅游
        "travel": 6003,
        # 体育
        "sports": 6004,
        # 社交
        "social_networking": 6005,
        # 参考
        "reference": 6006,
        # 效率
        "productivity": 6007,
        # 摄影与录像
        "photo_video": 6008,
        # 新闻
        "news": 6009,
        # 导航
        "navigation": 6010,
        # 音乐
        "music": 6011,
        # 生活
        "lifestyle": 6012,
        # 游戏
        "games": 6014,
        # 财务
        "finance": 6015,
        # 娱乐
        "entertainment": 6016,
        # 教育
        "education": 6017,
        # 图书
        "books": 6018,
        # 健康健美
        "health_fitness": 6013,
        # 杂志与报纸
        "magazines_newspapers": 6021,
        # 图形与设计
        "graphics_design": 6027,
        # 食品与饮料
        "food_drink": 6023,
        # 医疗
        "medical": 6020,
        # 儿童
        "kids": 6016,  # 实际是娱乐的子分类
    }
    
    def __init__(self, limit: int = 200, fetch_all_categories: bool = False):
        """
        Args:
            limit: 每个分类获取榜单数量上限 (最大 200)
            fetch_all_categories: 是否爬取所有分类（默认 False，只爬总榜）
        """
        self.limit = min(limit, 200)  # 苹果限制最大 200
        self.fetch_all_categories = fetch_all_categories
        self.client = httpx.AsyncClient(timeout=30.0)
        
    async def fetch_chart(self, chart_type: str, genre: int = 0) -> List[Dict]:
        """
        获取指定榜单
        
        Args:
            chart_type: 榜单类型 (top_free, top_paid, new_free, new_paid)
            genre: 分类 ID (0=全部，6014=财务，6017=工具 等)
            
        Returns:
            应用列表，每个应用包含：
            - app_id: 应用 ID
            - name: 应用名称
            - developer: 开发者
            - icon: 图标 URL
            - price: 价格
            - rank: 排名
            - category: 分类
        """
        if chart_type not in self.CHART_TYPES:
            raise ValueError(f"不支持的榜单类型：{chart_type}")
        
        # iTunes API URL 格式
        url = f"{self.BASE_URL}/{self.CHART_TYPES[chart_type]}/limit={self.limit}/genre={genre}/json"
        
        try:
            logger.info("正在获取苹果榜单", chart_type=chart_type, url=url)
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()
            
            apps = []
            entries = data.get("feed", {}).get("entry", [])
            
            for idx, entry in enumerate(entries):
                # iTunes API: 所有条目都是应用（包括第一个）
                if "im:name" not in entry:
                    continue
                
                # 获取 bundle_id（在 id.attributes.im:bundleId 中）
                id_attrs = entry.get("id", {}).get("attributes", {})
                bundle_id = id_attrs.get("im:bundleId", "")
                
                # 获取开发者（可能在 im:artist 中）
                developer = entry.get("im:artist", {})
                if isinstance(developer, dict):
                    developer = developer.get("label", "")
                
                # 获取图标（im:image 是列表）
                images = entry.get("im:image", [])
                icon = images[-1].get("label", "") if images else ""
                
                # 获取价格
                price_obj = entry.get("im:price", {})
                price = price_obj.get("attributes", {}).get("amount", "0") if isinstance(price_obj, dict) else "0"
                
                # 获取分类
                category_obj = entry.get("category", {})
                category = category_obj.get("attributes", {}).get("label", "") if isinstance(category_obj, dict) else ""
                
                # 获取 URL（link 可能是列表或字典）
                link_obj = entry.get("link", {})
                if isinstance(link_obj, list):
                    url = link_obj[0].get("attributes", {}).get("href", "") if link_obj else ""
                else:
                    url = link_obj.get("attributes", {}).get("href", "") if isinstance(link_obj, dict) else ""
                
                app_data = {
                    "app_id": bundle_id,
                    "name": entry.get("im:name", {}).get("label", ""),
                    "developer": developer,
                    "icon": icon,
                    "price": price,
                    "rank": idx + 1,
                    "category": category,
                    "url": url,
                    "chart_type": chart_type,
                    "fetched_at": datetime.now().isoformat(),
                }
                apps.append(app_data)
            
            logger.info(f"成功获取榜单数据", chart_type=chart_type, count=len(apps))
            return apps
            
        except httpx.HTTPError as e:
            logger.error("获取苹果榜单失败", chart_type=chart_type, error=str(e))
            return []
        except Exception as e:
            logger.error("解析榜单数据失败", chart_type=chart_type, error=str(e))
            return []
    
    async def fetch_all_charts(self, genres: Optional[List[int]] = None) -> Dict[str, List[Dict]]:
        """
        获取所有榜单（全量爬取）
        
        Args:
            genres: 分类 ID 列表，None 表示爬取所有分类
            
        Returns:
            字典：{chart_type_genre: [apps]}
        """
        all_charts = {}
        
        # 确定要爬取的分类
        if genres is None and self.fetch_all_categories:
            # 爬取所有分类
            target_categories = list(self.ALL_CATEGORIES.values())
            logger.info("🍎 开始全量爬取所有分类", category_count=len(target_categories))
        elif genres is None:
            # 只爬取总榜
            target_categories = [0]
        else:
            target_categories = genres
        
        # 爬取每个分类
        for chart_type in self.CHART_TYPES.keys():
            for genre in target_categories:
                try:
                    apps = await self.fetch_chart(chart_type, genre)
                    key = f"{chart_type}_g{genre}"
                    all_charts[key] = apps
                    logger.debug(f"爬取完成：{key}, 应用数：{len(apps)}")
                except Exception as e:
                    logger.error(f"爬取失败：{key}", error=str(e))
                    all_charts[key] = []
        
        # 统计总数
        total_apps = sum(len(apps) for apps in all_charts.values())
        logger.info(f"🍎 全量爬取完成", total_apps=total_apps, chart_count=len(all_charts))
        
        return all_charts
    
    async def fetch_all_unique_apps(self) -> List[Dict]:
        """
        获取所有不重复的应用（合并所有榜单）
        
        Returns:
            不重复的应用列表
        """
        all_charts = await self.fetch_all_charts()
        
        # 使用 bundle_id 去重
        seen_apps: Set[str] = set()
        unique_apps = []
        
        for chart_key, apps in all_charts.items():
            for app in apps:
                app_id = app.get("app_id", "")
                if app_id and app_id not in seen_apps:
                    seen_apps.add(app_id)
                    # 添加榜单来源信息
                    app["chart_sources"] = [chart_key]
                    unique_apps.append(app)
                elif app_id in seen_apps:
                    # 如果已存在，追加榜单来源
                    for existing in unique_apps:
                        if existing.get("app_id") == app_id:
                            existing["chart_sources"].append(chart_key)
                            break
        
        logger.info(f"🍎 去重完成", unique_count=len(unique_apps), total_count=sum(len(apps) for apps in all_charts.values()))
        return unique_apps
    
    async def close(self):
        """关闭 HTTP 客户端"""
        await self.client.aclose()


# 常用分类 ID
CATEGORIES = {
    "all": 0,
    "business": 6000,
    "weather": 6001,
    "utilities": 6002,
    "travel": 6003,
    "sports": 6004,
    "social_networking": 6005,
    "reference": 6006,
    "productivity": 6007,
    "photo_video": 6008,
    "news": 6009,
    "navigation": 6010,
    "music": 6011,
    "lifestyle": 6012,
    "games": 6014,
    "finance": 6015,
    "entertainment": 6016,
    "education": 6017,
    "books": 6018,
    "health_fitness": 6013,
    "magazines_newspapers": 6021,
}
