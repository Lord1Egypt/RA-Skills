#!/usr/bin/env python3
"""
点点数据安卓渠道榜单爬虫 - 终极版
关键突破：点击"上架监控"获取真实应用列表
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
logger = logging.getLogger('DiandianUltimate')


class DiandianUltimateFetcher:
    """点点数据终极版爬虫"""
    
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
        """
        获取指定渠道的数据
        
        Args:
            channel: 渠道名称
            app_type: 'new' 新上架，'offline' 下架
            limit: 数量限制
        """
        monitor_text = "上架监控" if app_type == 'new' else "下架监控"
        logger.info(f"📱 开始获取 {self.CHANNELS[channel]} 渠道 {monitor_text} 数据...")
        
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
                
                # Step 2: 点击"市场情报"
                logger.info("📖 点击'市场情报'...")
                market_btn = await page.wait_for_selector('text="市场情报"', timeout=10000)
                await market_btn.click()
                await asyncio.sleep(2)
                logger.info("✅ 已点击市场情报")
                
                # Step 3: 点击"上架监控"或"下架监控"
                logger.info(f"📖 点击'{monitor_text}'...")
                
                await page.evaluate(f'''() => {{
                    const btn = Array.from(document.querySelectorAll('*')).find(el => 
                        el.textContent.includes('{monitor_text}')
                    );
                    if (btn) {{
                        btn.click();
                        console.log('已点击 {monitor_text}');
                    }} else {{
                        console.log('未找到 {monitor_text} 按钮');
                    }}
                }}''')
                
                await asyncio.sleep(5)  # 等待页面加载
                logger.info(f"✅ 已点击 {monitor_text}")
                
                # Step 4: 选择渠道
                logger.info(f"📖 选择渠道 '{self.CHANNELS[channel]}'...")
                channel_name = self.CHANNELS[channel]
                
                # 查找渠道选择器
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
                await asyncio.sleep(5)
                
                logger.info(f"✅ 已选择 {channel_name}")
                
                # Step 5: 截图
                screenshot_path = Path(__file__).parent.parent / f"debug_{channel}_{app_type}_ultimate.png"
                await page.screenshot(path=str(screenshot_path), full_page=True)
                logger.info(f"📸 截图：{screenshot_path}")
                
                # Step 6: 保存 HTML
                html_path = Path(__file__).parent.parent / f"debug_{channel}_{app_type}_ultimate.html"
                with open(html_path, 'w', encoding='utf-8') as f:
                    html = await page.content()
                    f.write(html)
                logger.info(f"📄 HTML: {html_path}")
                
                # Step 7: 提取应用数据
                logger.info("📊 提取应用数据...")
                apps = await self._extract_apps_ultimate(page, limit, app_type)
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
    
    async def _extract_apps_ultimate(self, page, limit: int = 100, app_type: str = 'new') -> List:
        """终极版数据提取"""
        try:
            apps_data = await page.evaluate('''() => {
                const apps = [];
                
                // 查找表格
                const tables = document.querySelectorAll('table');
                console.log(`找到 ${tables.length} 个表格`);
                
                for (const table of tables) {
                    const rows = table.querySelectorAll('tr');
                    console.log(`表格有 ${rows.length} 行`);
                    
                    for (let i = 1; i < rows.length && apps.length < 100; i++) {
                        const row = rows[i];
                        const cells = row.querySelectorAll('td');
                        
                        if (cells.length >= 2) {
                            const rank = cells[0]?.textContent.trim() || '';
                            const name = cells[1]?.textContent.trim() || '';
                            const developer = cells[2]?.textContent.trim() || '';
                            const category = cells[3]?.textContent.trim() || '';
                            const date = cells[4]?.textContent.trim() || '';
                            
                            // 验证应用名
                            if (name && 
                                name.length > 1 && 
                                name.length < 100 && 
                                !/^[\\d\\s]+$/.test(name) &&
                                !name.includes('排名') &&
                                !name.includes('应用') &&
                                !name.includes('监控')
                            ) {
                                apps.push({
                                    rank, name, developer, category, date: date || new Date().toISOString().split('T')[0]
                                });
                            }
                        }
                    }
                }
                
                // 如果表格没数据，尝试其他方式
                if (apps.length === 0) {
                    const allDivs = document.querySelectorAll('[class*="app"], [class*="list"], tr');
                    for (const div of allDivs) {
                        const text = div.textContent.trim();
                        if (text && text.length > 5 && text.length < 100) {
                            apps.push({
                                rank: '',
                                name: text.split('\\n')[0],
                                developer: text.split('\\n')[1] || '',
                                category: '',
                                date: new Date().toISOString().split('T')[0]
                            });
                        }
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
            
            # 根据类型返回不同的数据类
            result_apps = []
            for app in unique_apps:
                if app_type == 'new':
                    result_apps.append(NewApp(
                        app_name=app['name'],
                        package_name='',
                        developer=app.get('developer', ''),
                        category=app.get('category', ''),
                        release_date=app.get('date', datetime.now().strftime('%Y-%m-%d'))
                    ))
                else:
                    result_apps.append(OfflineApp(
                        app_name=app['name'],
                        package_name='',
                        developer=app.get('developer', ''),
                        category=app.get('category', ''),
                        offline_date=app.get('date', datetime.now().strftime('%Y-%m-%d'))
                    ))
            
            return result_apps
            
        except Exception as e:
            logger.error(f"❌ 提取失败：{e}")
            import traceback
            traceback.print_exc()
            return []


async def test_ultimate():
    """测试终极版"""
    fetcher = DiandianUltimateFetcher()
    
    print("\n📱 测试华为渠道（终极版）...\n")
    
    # 测试新上架
    print("="*60)
    print("测试新上架应用")
    print("="*60)
    new_data = await fetcher.fetch_channel_data('huawei', 'new', limit=20)
    
    print(f"\n华为渠道 - 新上架:")
    print(f"  获取到：{len(new_data.get('apps', []))} 个应用")
    
    if new_data.get('apps'):
        print(f"\n  前 10 个新上架应用:")
        for i, app in enumerate(new_data['apps'][:10], 1):
            print(f"    {i}. {app.app_name} - {app.developer}")
    
    if new_data.get('error'):
        print(f"\n  错误：{new_data['error']}")
    
    # 等待一下
    await asyncio.sleep(2)
    
    # 测试下架
    print("\n" + "="*60)
    print("测试下架应用")
    print("="*60)
    offline_data = await fetcher.fetch_channel_data('huawei', 'offline', limit=20)
    
    print(f"\n华为渠道 - 下架:")
    print(f"  获取到：{len(offline_data.get('apps', []))} 个应用")
    
    if offline_data.get('apps'):
        print(f"\n  前 10 个下架应用:")
        for i, app in enumerate(offline_data['apps'][:10], 1):
            print(f"    {i}. {app.app_name} - {app.developer}")
    
    if offline_data.get('error'):
        print(f"\n  错误：{offline_data['error']}")


if __name__ == "__main__":
    asyncio.run(test_ultimate())
