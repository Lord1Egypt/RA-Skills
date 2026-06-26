#!/usr/bin/env python3
"""
点点数据安卓渠道榜单爬虫 - 最终版
使用已验证的导航方式 + 改进的数据提取
"""

import asyncio
import sys
import yaml
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from playwright.async_api import async_playwright

sys.path.insert(0, str(Path(__file__).parent.parent))

from rankers.base import NewApp, OfflineApp
from utils.logger import setup_logger

logger = setup_logger()


class DiandianAndroidWebRankerFinal:
    """点点数据安卓渠道网页爬虫（最终版）"""
    
    CHANNELS = {
        "huawei": {"name": "华为"},
        "xiaomi": {"name": "小米"},
        "tencent": {"name": "应用宝"},
        "oppo": {"name": "OPPO"},
        "vivo": {"name": "vivo"},
        "baidu": {"name": "百度"},
        "qihoo360": {"name": "360"},
        "wandoujia": {"name": "豌豆荚"},
    }
    
    def __init__(self):
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        config_path = Path(__file__).parent.parent.parent / "config" / "diandian.yaml"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {"token": ""}
    
    async def fetch_channel_data(self, channel: str, app_type: str = 'new', limit: int = 100) -> Dict:
        """获取指定渠道的数据"""
        logger.info(f"📱 开始获取 {self.CHANNELS[channel]['name']} {app_type} 数据...")
        
        async with async_playwright() as p:
            try:
                user_data_dir = Path(__file__).parent.parent.parent / ".browser_data" / "diandian"
                user_data_dir.mkdir(parents=True, exist_ok=True)
                
                context = await p.chromium.launch_persistent_context(
                    user_data_dir=str(user_data_dir),
                    headless=True,
                    channel='chrome',
                    args=['--disable-blink-features=AutomationControlled', '--no-sandbox']
                )
                
                page = context.pages[0] if context.pages else await context.new_page()
                await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                # Step 1: 访问主页
                await page.goto("https://app.diandian.com/", wait_until="domcontentloaded", timeout=60000)
                await asyncio.sleep(3)
                
                # Step 2: 检查登录
                page_content = await page.content()
                is_logged = '退出' in page_content or '账号设置' in page_content
                if not is_logged:
                    logger.error("❌ 未登录")
                    await context.close()
                    return {"apps": [], "error": "未登录"}
                
                logger.info("✅ 已登录")
                
                # Step 3: 点击市场情报
                logger.info("📖 点击'市场情报'...")
                market_intel_btn = await page.query_selector('text=市场情报')
                if market_intel_btn:
                    await market_intel_btn.click()
                    await asyncio.sleep(3)
                    logger.info("✅ 已点击'市场情报'")
                else:
                    logger.error("❌ 未找到'市场情报'按钮")
                    await context.close()
                    return {"apps": [], "error": "未找到市场情报"}
                
                # Step 4: 点击上架监控/下架监控
                menu_text = "上架监控" if app_type == "new" else "下架监控"
                logger.info(f"📖 点击'{menu_text}'...")
                menu_btn = await page.query_selector(f'text={menu_text}')
                if menu_btn:
                    await menu_btn.click()
                    await asyncio.sleep(5)
                    logger.info(f"✅ 已点击'{menu_text}'")
                else:
                    logger.error(f"❌ 未找到'{menu_text}'按钮")
                    await context.close()
                    return {"apps": [], "error": f"未找到{menu_text}"}
                
                # Step 5: 选择渠道
                logger.info(f"📖 选择渠道 '{self.CHANNELS[channel]['name']}'...")
                try:
                    # 尝试多种选择器
                    channel_btn = None
                    selectors = [
                        f'text="{self.CHANNELS[channel]["name"]}"',
                        f'[text*="{self.CHANNELS[channel]["name"]}"]',
                    ]
                    for selector in selectors:
                        try:
                            channel_btn = await page.wait_for_selector(selector, timeout=5000)
                            if channel_btn:
                                break
                        except:
                            continue
                    
                    if channel_btn:
                        await channel_btn.click()
                        await asyncio.sleep(3)
                        logger.info(f"✅ 已选择 {self.CHANNELS[channel]['name']}")
                    else:
                        logger.warning(f"⚠️ 未找到渠道按钮，使用默认渠道")
                except Exception as e:
                    logger.warning(f"⚠️ 选择渠道失败：{e}")
                
                # Step 6: 等待数据加载
                await asyncio.sleep(3)
                
                # Step 7: 提取数据
                apps = await self._extract_apps_from_table(page, app_type, limit)
                logger.info(f"✅ {self.CHANNELS[channel]['name']} {app_type} 获取到 {len(apps)} 个应用")
                
                await context.close()
                
                return {
                    "apps": apps,
                    "channel": channel,
                    "channel_name": self.CHANNELS.get(channel, {}).get('name', channel),
                    "fetch_time": datetime.now().isoformat(),
                }
                
            except Exception as e:
                logger.error(f"❌ {channel} 失败：{e}")
                return {
                    "channel": channel,
                    "channel_name": self.CHANNELS.get(channel, {}).get('name', channel),
                    "new_apps": [],
                    "offline_apps": [],
                    "fetch_time": datetime.now().isoformat(),
                    "error": str(e),
                }
    
    async def _extract_apps_from_table(self, page, app_type: str = "new", limit: int = 100) -> List:
        """从表格提取应用数据"""
        try:
            js_code = '''() => {
                const apps = [];
                
                // 查找表格行
                const rows = document.querySelectorAll('table tr');
                console.log(`找到 ${rows.length} 行`);
                
                for (let i = 1; i < rows.length && apps.length < LIMIT; i++) { // 跳过表头
                    const row = rows[i];
                    const cells = row.querySelectorAll('td');
                    
                    if (cells.length >= 2) {
                        let rank = cells[0]?.textContent.trim() || '';
                        let name = cells[1]?.textContent.trim() || '';
                        let developer = cells[2]?.textContent.trim() || '';
                        let category = cells[3]?.textContent.trim() || '';
                        let date = cells[4]?.textContent.trim() || new Date().toISOString().split('T')[0];
                        
                        // 验证应用名
                        if (name && name.length > 1 && name.length < 100 && !/^\\d+$/.test(name)) {
                            // 清理开发者名称（移除包名）
                            developer = developer.replace(/[\\(\\（].*[\\)\\）]/g, '').trim();
                            
                            apps.push({
                                rank: rank,
                                name: name,
                                developer: developer,
                                category: category,
                                date: date
                            });
                        }
                    }
                }
                
                return apps;
            }'''.replace('LIMIT', str(limit))
            
            apps_data = await page.evaluate(js_code)
            
            if app_type == "new":
                return [
                    NewApp(
                        app_name=app['name'],
                        package_name='',
                        developer=app.get('developer', ''),
                        category=app.get('category', ''),
                        release_date=app.get('date', datetime.now().strftime('%Y-%m-%d'))
                    )
                    for app in apps_data if app.get('name')
                ]
            else:
                return [
                    OfflineApp(
                        app_name=app['name'],
                        package_name='',
                        developer=app.get('developer', ''),
                        category=app.get('category', ''),
                        offline_date=app.get('date', datetime.now().strftime('%Y-%m-%d'))
                    )
                    for app in apps_data if app.get('name')
                ]
            
        except Exception as e:
            logger.error(f"提取失败：{e}")
            import traceback
            traceback.print_exc()
            return []
    
    async def fetch_all_for_channel(self, channel: str, limit: int = 100) -> Dict:
        """
        获取指定渠道的所有数据（新上架 + 下架）
        
        Args:
            channel: 渠道名称
            limit: 数量限制
        
        Returns:
            Dict: {new_apps: [], offline_apps: []}
        """
        logger.info(f"📱 开始爬取 {channel} 渠道（新上架 + 下架）...")
        
        # 先获取新上架
        result_new = await self.fetch_channel_data(channel, 'new', limit)
        new_apps = result_new.get('apps', [])
        
        # 再获取下架
        result_off = await self.fetch_channel_data(channel, 'offline', limit)
        offline_apps = result_off.get('apps', [])
        
        return {
            "new_apps": new_apps,
            "offline_apps": offline_apps,
        }
    
    async def fetch_all(self) -> Dict:
        """
        获取所有渠道的数据（符合接口规范）
        
        Returns:
            Dict: {channel_name: {new_apps: [], offline_apps: []}}
        """
        all_result = {}
        
        for channel in self.CHANNELS.keys():
            result = await self.fetch_all_for_channel(channel, limit=100)
            all_result[channel] = result
        
        return all_result


async def test_final():
    """测试最终版"""
    ranker = DiandianAndroidWebRankerFinal()
    
    print("\n📱 测试华为渠道（最终版）...")
    data = await ranker.fetch_channel_data('huawei', limit=20)
    
    print(f"\n华为渠道:")
    print(f"  获取到：{len(data['new_apps'])} 个应用")
    
    if data['new_apps']:
        print(f"\n  前 10 个应用:")
        for i, app in enumerate(data['new_apps'][:10], 1):
            print(f"    {i}. {app.app_name} - {app.developer}")
    
    if data.get('error'):
        print(f"\n  错误：{data['error']}")


if __name__ == "__main__":
    asyncio.run(test_final())
