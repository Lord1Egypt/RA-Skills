#!/usr/bin/env python3
"""
点点数据安卓渠道榜单爬虫 - 成功版
使用正确的选择器：.rank-item 和 .rank-name
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
logger = logging.getLogger('DiandianSuccess')


class DiandianSuccessFetcher:
    """点点数据成功版爬虫"""
    
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
    
    async def fetch_channel_data(self, channel: str, limit: int = 100) -> Dict:
        """获取指定渠道的数据"""
        logger.info(f"📱 开始获取 {self.CHANNELS[channel]} 渠道数据...")
        
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
                
                # Step 2: 导航到安卓榜单
                logger.info("📖 导航到安卓榜单...")
                
                # 点击市场情报
                market_btn = await page.wait_for_selector('text="市场情报"', timeout=10000)
                await market_btn.click()
                await asyncio.sleep(2)
                
                # 点击国内安卓榜单（使用 JavaScript）
                await page.evaluate('''() => {
                    const btn = Array.from(document.querySelectorAll('*')).find(el => 
                        el.textContent.includes('国内安卓榜单')
                    );
                    if (btn) btn.click();
                }''')
                await asyncio.sleep(3)
                
                logger.info("✅ 已导航到安卓榜单")
                
                # Step 3: 选择渠道
                logger.info(f"📖 选择 {self.CHANNELS[channel]}...")
                channel_name = self.CHANNELS[channel]
                
                # 使用 JavaScript 强制点击（不等待可见性）
                js_code = f"""() => {{
                    const btns = Array.from(document.querySelectorAll('*')).filter(el => 
                        el.textContent.trim() === '{channel_name}' &&
                        el.tagName === 'DIV'
                    );
                    console.log('找到 ' + btns.length + ' 个按钮');
                    if (btns.length > 0) {{
                        btns[0].click();
                        console.log('已点击');
                    }}
                }}"""
                await page.evaluate(js_code)
                await asyncio.sleep(3)
                
                logger.info(f"✅ 已选择 {channel_name}")
                
                # Step 4: 等待榜单加载
                await asyncio.sleep(2)
                
                # Step 5: 截图
                screenshot_path = Path(__file__).parent.parent / f"debug_{channel}_success.png"
                await page.screenshot(path=str(screenshot_path), full_page=True)
                logger.info(f"📸 截图：{screenshot_path}")
                
                # Step 6: 提取应用数据（使用正确的选择器）
                logger.info("📊 提取应用数据...")
                apps = await self._extract_apps_correct(page, limit)
                logger.info(f"✅ 提取到 {len(apps)} 个应用")
                
                await context.close()
                
                return {
                    "channel": channel,
                    "channel_name": self.CHANNELS[channel],
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
                    "apps": [],
                    "error": str(e),
                }
    
    async def _extract_apps_correct(self, page, limit: int = 100) -> List:
        """使用正确的选择器提取应用数据"""
        try:
            apps_data = await page.evaluate('''() => {
                const apps = [];
                
                // 使用正确的选择器：.rank-item
                const rankItems = document.querySelectorAll('.rank-item');
                console.log(`找到 ${rankItems.length} 个 rank-item`);
                
                for (const item of rankItems) {
                    try {
                        // 查找排名
                        const rankEl = item.querySelector('.rank-num, [class*="rank"]');
                        const rank = rankEl ? rankEl.textContent.trim() : '';
                        
                        // 查找应用名
                        const nameEl = item.querySelector('.rank-name, [class*="name"]');
                        const name = nameEl ? nameEl.textContent.trim() : '';
                        
                        // 查找开发者
                        const devEl = item.querySelectorAll('span, div')[2];
                        const developer = devEl ? devEl.textContent.trim() : '';
                        
                        // 验证
                        if (name && name.length > 1 && name.length < 100) {
                            apps.push({
                                rank: rank,
                                name: name,
                                developer: developer,
                                date: new Date().toISOString().split('T')[0]
                            });
                        }
                    } catch (e) {
                        console.error('提取单个 item 失败:', e);
                    }
                }
                
                console.log(`提取到 ${apps.length} 个应用`);
                return apps.slice(0, 100);
            }''')
            
            # 去重
            seen = set()
            unique_apps = []
            for app in apps_data:
                if app['name'] not in seen and len(app['name']) > 1 and len(app['name']) < 100:
                    seen.add(app['name'])
                    unique_apps.append(app)
            
            return [
                NewApp(
                    app_name=app['name'],
                    package_name='',
                    developer=app.get('developer', ''),
                    category='',
                    release_date=app.get('date', datetime.now().strftime('%Y-%m-%d'))
                )
                for app in unique_apps
            ]
            
        except Exception as e:
            logger.error(f"❌ 提取失败：{e}")
            import traceback
            traceback.print_exc()
            return []


async def test_success():
    """测试成功版"""
    fetcher = DiandianSuccessFetcher()
    
    print("\n📱 测试华为渠道（成功版）...\n")
    data = await fetcher.fetch_channel_data('huawei', limit=20)
    
    print(f"\n华为渠道:")
    print(f"  获取到：{len(data.get('apps', []))} 个应用")
    
    if data.get('apps'):
        print(f"\n  前 10 个应用:")
        for i, app in enumerate(data['apps'][:10], 1):
            print(f"    {i}. {app.app_name} - {app.developer}")
    
    if data.get('error'):
        print(f"\n  错误：{data['error']}")


if __name__ == "__main__":
    asyncio.run(test_success())
