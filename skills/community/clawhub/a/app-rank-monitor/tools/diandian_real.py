#!/usr/bin/env python3
"""
点点数据安卓渠道榜单爬虫 - 真正完成版
关键：访问正确的 URL 路径获取真实的上下架数据
"""

import asyncio
import sys
import yaml
from pathlib import Path
from datetime import datetime
from typing import List, Dict

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from playwright.async_api import async_playwright
from rankers.base import NewApp, OfflineApp

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('DiandianReal')


class DiandianRealFetcher:
    """点点数据真正完成版爬虫"""
    
    CHANNELS = {
        "huawei": "华为",
        "xiaomi": "小米",
        "tencent": "应用宝",
        "oppo": "OPPO",
        "vivo": "vivo",
        "baidu": "百度",
        "qihoo360": "360",
        "wandoujia": "豌豆荚",
    }
    
    def __init__(self):
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        config_path = Path(__file__).parent.parent / "config" / "diandian.yaml"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {"token": ""}
    
    async def fetch_channel_data(self, channel: str, app_type: str = 'new', limit: int = 100) -> Dict:
        """获取指定渠道的数据"""
        logger.info(f"📱 开始获取 {self.CHANNELS[channel]} 渠道 {'新上架' if app_type == 'new' else '下架'} 数据...")
        
        async with async_playwright() as p:
            try:
                user_data_dir = Path(__file__).parent.parent / ".browser_data" / "diandian"
                user_data_dir.mkdir(parents=True, exist_ok=True)
                
                context = await p.chromium.launch_persistent_context(
                    user_data_dir=str(user_data_dir),
                    headless=False,
                    channel='chrome',
                    args=['--disable-blink-features=AutomationControlled', '--no-sandbox']
                )
                
                page = context.pages[0] if context.pages else await context.new_page()
                await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                # Step 1: 访问并登录
                await page.goto("https://app.diandian.com/", wait_until="domcontentloaded", timeout=60000)
                await asyncio.sleep(3)
                
                is_logged = '退出' in await page.content() or '账号设置' in await page.content()
                if not is_logged:
                    logger.error("❌ 未登录！")
                    await context.close()
                    return {"error": "未登录"}
                
                logger.info("✅ 已登录")
                
                # Step 2: 直接访问正确的 URL
                # 上架监控：/zh/list/new
                # 下架监控：/zh/list/offline
                if app_type == 'new':
                    url = "https://app.diandian.com/zh/list/new"
                else:
                    url = "https://app.diandian.com/zh/list/offline"
                
                logger.info(f"📖 直接访问：{url}")
                await page.goto(url, wait_until="domcontentloaded", timeout=60000)
                await asyncio.sleep(5)
                logger.info("✅ 已导航到上下架监控页面")
                
                # Step 3: 选择渠道
                channel_name = self.CHANNELS[channel]
                logger.info(f"📖 选择渠道 '{channel_name}'...")
                
                # 等待渠道按钮出现并点击
                try:
                    channel_btn = await page.wait_for_selector(f'text="{channel_name}"', timeout=10000)
                    await channel_btn.click()
                    await asyncio.sleep(5)
                    logger.info(f"✅ 已选择 {channel_name}")
                except Exception as e:
                    logger.warning(f"⚠️ 未找到渠道按钮：{e}")
                
                # Step 4: 滚动加载
                logger.info("📜 滚动加载更多...")
                for i in range(3):
                    await page.evaluate("window.scrollBy(0, 1000)")
                    await asyncio.sleep(2)
                
                # Step 5: 截图
                screenshot_path = Path(__file__).parent.parent / f"debug_{channel}_{app_type}_real.png"
                await page.screenshot(path=str(screenshot_path), full_page=True)
                logger.info(f"📸 截图：{screenshot_path}")
                
                # Step 6: 保存 HTML
                html_path = Path(__file__).parent.parent / f"debug_{channel}_{app_type}_real.html"
                with open(html_path, 'w', encoding='utf-8') as f:
                    html = await page.content()
                    f.write(html)
                logger.info(f"📄 HTML: {html_path}")
                
                # Step 7: 提取应用数据
                logger.info("📊 提取应用数据...")
                apps = await self._extract_apps_real(page, limit)
                logger.info(f"✅ 提取到 {len(apps)} 个应用")
                
                await context.close()
                
                return {
                    "channel": channel,
                    "channel_name": self.CHANNELS[channel],
                    "type": app_type,
                    "apps": apps,
                    "fetch_time": datetime.now().isoformat(),
                }
                
            except Exception as e:
                logger.error(f"❌ 失败：{e}")
                import traceback
                traceback.print_exc()
                return {
                    "channel": channel,
                    "channel_name": self.CHANNELS.get(channel, channel),
                    "type": app_type,
                    "apps": [],
                    "error": str(e),
                }
    
    async def _extract_apps_real(self, page, limit: int = 100, app_type: str = 'new') -> List:
        """提取应用数据"""
        try:
            apps_data = await page.evaluate('''() => {
                const apps = [];
                
                // 查找所有应用行
                const rows = document.querySelectorAll('[class*="dd-data-table-row"], tr[class*="row"]');
                console.log(`找到 ${rows.length} 行`);
                
                for (const row of rows) {
                    // 提取应用名称
                    const nameEl = row.querySelector('.app-name-text, [class*="app-name"]');
                    const name = nameEl ? nameEl.textContent.trim() : '';
                    
                    // 跳过无效数据
                    if (!name || name.length < 2 || name.length > 100) continue;
                    if (name.includes('监控') || name.includes('排名') || name.includes('应用/游戏')) continue;
                    
                    // 提取开发者信息
                    let developer = '';
                    const descEl = row.querySelector('.desc, [class*="developer"], [class*="company"]');
                    if (descEl) {
                        developer = descEl.textContent.trim();
                    }
                    
                    apps.push({
                        name: name,
                        developer: developer,
                        date: new Date().toISOString().split('T')[0]
                    });
                    
                    console.log(`提取到：${name}`);
                    
                    if (apps.length >= 100) break;
                }
                
                console.log(`总共提取到 ${apps.length} 个应用`);
                return apps.slice(0, 100);
            }''')
            
            # 去重
            seen = set()
            unique_apps = []
            for app in apps_data:
                if app['name'] not in seen and len(app['name']) > 1 and len(app['name']) < 100:
                    seen.add(app['name'])
                    unique_apps.append(app)
            
            # 返回数据类
            result_apps = []
            for app in unique_apps:
                if app_type == 'new':
                    result_apps.append(NewApp(
                        app_name=app['name'],
                        package_name='',
                        developer=app.get('developer', ''),
                        category='',
                        release_date=app.get('date', datetime.now().strftime('%Y-%m-%d'))
                    ))
                else:
                    result_apps.append(OfflineApp(
                        app_name=app['name'],
                        package_name='',
                        developer=app.get('developer', ''),
                        category='',
                        offline_date=app.get('date', datetime.now().strftime('%Y-%m-%d'))
                    ))
            
            return result_apps
            
        except Exception as e:
            logger.error(f"❌ 提取失败：{e}")
            return []


async def test_real():
    """测试真正完成版"""
    fetcher = DiandianRealFetcher()
    
    print("\n📱 测试华为渠道（真正完成版）...\n")
    
    # 测试新上架
    print("="*60)
    print("测试新上架应用")
    print("="*60)
    new_data = await fetcher.fetch_channel_data('huawei', 'new', limit=50)
    
    print(f"\n华为渠道 - 新上架:")
    print(f"  获取到：{len(new_data.get('apps', []))} 个应用")
    
    if new_data.get('apps'):
        print(f"\n  前 20 个新上架应用:")
        for i, app in enumerate(new_data['apps'][:20], 1):
            print(f"    {i}. {app.app_name} - {app.developer}")
    
    if new_data.get('error'):
        print(f"\n  错误：{new_data['error']}")


if __name__ == "__main__":
    asyncio.run(test_real())
