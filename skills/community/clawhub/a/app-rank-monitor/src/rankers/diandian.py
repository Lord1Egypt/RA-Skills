"""
点点数据榜单爬虫 (增强版)
https://app.diandian.com/
"""

import httpx
from typing import List
from pathlib import Path
import yaml

from .base import BaseRanker, RankApp, NewApp, OfflineApp
from utils.logger import setup_logger

logger = setup_logger()


class DiandianRanker(BaseRanker):
    """点点数据榜单爬虫"""
    
    def __init__(self):
        super().__init__("点点数据")
        self.base_url = "https://app.diandian.com/api"
        self.web_url = "https://www.diandian.com"
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """加载配置"""
        config_path = Path(__file__).parent.parent.parent / "config" / "diandian.yaml"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {"token": ""}
    
    async def fetch_rising_list(self, limit: int = 100) -> List[RankApp]:
        """获取上升榜"""
        # 点点数据网页版榜单
        url = f"{self.web_url}/zh/list/ios-rank/US/iphone/free/total"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Cookie": self.config.get('token', ''),
            "Referer": f"{self.web_url}/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=30)
                if response.status_code == 200:
                    # 解析 HTML
                    return await self._parse_rising_html(response.text)
                logger.warning(f"点点上升榜 HTTP {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"点点上升榜异常：{e}")
            return []
    
    async def _parse_rising_html(self, html: str) -> List[RankApp]:
        """解析 HTML 榜单数据"""
        result = []
        
        try:
            # 尝试使用 BeautifulSoup 解析
            from bs4 import BeautifulSoup
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # 查找榜单列表
            # 尝试多种可能的选择器
            selectors = [
                '.rank-list tr',
                '.list-item',
                '[class*="rank"] tr',
                'table tr',
                '.app-item',
            ]
            
            items = []
            for selector in selectors:
                items = soup.select(selector)
                if items:
                    logger.debug(f"使用选择器：{selector}")
                    break
            
            if not items:
                # 尝试用正则提取
                return self._parse_with_regex(html)
            
            for idx, item in enumerate(items[:100]):
                try:
                    # 提取排名
                    rank_el = item.select_one('.rank') or item.select_one('[class*="rank"]') or item.select_one('td:first-child')
                    rank = int(rank_el.get_text(strip=True)) if rank_el else idx + 1
                    
                    # 提取应用名称
                    name_el = item.select_one('.name') or item.select_one('.title') or item.select_one('a')
                    app_name = name_el.get_text(strip=True) if name_el else ''
                    
                    # 提取包名
                    package_name = ''
                    if name_el and name_el.has_attr('href'):
                        href = name_el['href']
                        if 'id=' in href:
                            package_name = href.split('id=')[-1].split('&')[0]
                    
                    # 提取开发者
                    dev_el = item.select_one('.developer') or item.select_one('.company')
                    developer = dev_el.get_text(strip=True) if dev_el else ''
                    
                    # 提取变化
                    change_el = item.select_one('.change') or item.select_one('.rise') or item.select_one('.fall')
                    change = 0
                    if change_el:
                        change_text = change_el.get_text(strip=True)
                        if '+' in change_text:
                            change = int(change_text.replace('+', ''))
                        elif '-' in change_text:
                            change = -int(change_text.replace('-', ''))
                    
                    if app_name:
                        result.append(RankApp(
                            rank=rank,
                            app_name=app_name,
                            package_name=package_name,
                            developer=developer,
                            category='',
                            change=change
                        ))
                except Exception as e:
                    logger.debug(f"解析单项失败：{e}")
                    continue
            
            logger.info(f"点点上升榜解析成功：{len(result)} 条")
            
        except ImportError:
            logger.warning("BeautifulSoup 未安装，使用正则解析")
            return self._parse_with_regex(html)
        except Exception as e:
            logger.error(f"点点 HTML 解析失败：{e}")
            return self._parse_with_regex(html)
        
        return result
    
    def _parse_with_regex(self, html: str) -> List[RankApp]:
        """使用正则表达式解析 HTML (降级方案)"""
        import re
        result = []
        
        # 匹配应用列表项
        pattern = r'<div[^>]*class="[^"]*app[^"]*"[^>]*>.*?</div>'
        matches = re.findall(pattern, html, re.DOTALL)
        
        for match in matches[:100]:
            try:
                # 提取名称
                name_match = re.search(r'class="name"[^>]*>([^<]+)<', match)
                app_name = name_match.group(1).strip() if name_match else ''
                
                # 提取排名
                rank_match = re.search(r'class="rank"[^>]*>(\d+)<', match)
                rank = int(rank_match.group(1)) if rank_match else len(result) + 1
                
                if app_name:
                    result.append(RankApp(
                        rank=rank,
                        app_name=app_name,
                        package_name='',
                        developer='',
                        category='',
                        change=0
                    ))
            except:
                continue
        
        return result
    
    async def fetch_new_apps(self, limit: int = 100) -> List[NewApp]:
        """获取新上架 App"""
        url = f"{self.base_url}/rank/new"
        params = {
            "platform": "ios",
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
                    return self._parse_new_apps(data.get("data", []))
                logger.warning(f"点点新上架 HTTP {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"点点新上架异常：{e}")
            return []
    
    def _parse_new_apps(self, data: list) -> List[NewApp]:
        """解析新上架数据"""
        result = []
        for item in data[:100]:
            app = NewApp(
                app_name=item.get("name", ""),
                package_name=item.get("bundle_id", ""),
                developer=item.get("developer", ""),
                category=item.get("category", ""),
                release_date=item.get("release_date", ""),
            )
            result.append(app)
        return result
    
    async def fetch_offline_apps(self, limit: int = 100) -> List[OfflineApp]:
        """获取新下架 App"""
        url = f"{self.base_url}/rank/offline"
        params = {
            "platform": "ios",
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
                    return self._parse_offline_apps(data.get("data", []))
                logger.warning(f"点点下架榜 HTTP {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"点点下架榜异常：{e}")
            return []
    
    def _parse_offline_apps(self, data: list) -> List[OfflineApp]:
        """解析下架数据"""
        result = []
        for item in data[:100]:
            app = OfflineApp(
                app_name=item.get("name", ""),
                package_name=item.get("bundle_id", ""),
                developer=item.get("developer", ""),
                category=item.get("category", ""),
                offline_date=item.get("offline_date", ""),
            )
            result.append(app)
        return result
