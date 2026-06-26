#!/usr/bin/env python3
"""
点点数据安卓渠道榜单爬虫 - 国内安卓榜单版
导航：国内安卓榜单 → 选择渠道 → 免费榜/付费榜 → 上下架数据
"""

import asyncio
import sys
import yaml
from pathlib import Path
from datetime import datetime
from typing import List, Dict

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from playwright.async_api import async_playwright
from rankers.base import NewApp, OfflineApp, RankApp

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('DiandianAndroidRank')


class DiandianAndroidRankFetcher:
    """点点数据国内安卓榜单爬虫"""
    
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
    
    async def fetch_rank_data(self, channel: str, rank_type: str = 'free', limit: int = 100) -> Dict:
        """
        获取指定渠道的榜单数据
        
        Args:
            channel: 渠道名称 (huawei/xiaomi/etc.)
            rank_type: 榜单类型 ('free' 免费榜，'paid' 付费榜，'top' 畅销榜)
            limit: 数量限制
        """
        rank_type_map = {'free': '免费榜', 'paid': '付费榜', 'top': '畅销榜'}
        logger.info(f"📱 开始获取 {self.CHANNELS[channel]} 渠道 {rank_type_map.get(rank_type, rank_type)} 数据...")
        
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
                
                # Step 3: 点击"国内安卓榜单"
                logger.info("📖 点击'国内安卓榜单'...")
                
                js_code = """() => {
                    const btn = Array.from(document.querySelectorAll('*')).find(el => 
                        el.textContent.includes('国内安卓榜单')
                    );
                    if (btn) {
                        btn.click();
                        console.log('已点击国内安卓榜单');
                    }
                }"""
                await page.evaluate(js_code)
                await asyncio.sleep(3)
                logger.info("✅ 已点击国内安卓榜单")
                
                # Step 4: 选择渠道
                channel_name = self.CHANNELS[channel]
                logger.info(f"📖 选择渠道 '{channel_name}'...")
                
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
                
                # Step 5: 选择榜单类型（免费榜/付费榜/畅销榜）
                logger.info(f"📖 选择榜单类型 '{rank_type_map.get(rank_type, rank_type)}'...")
                
                # 点击"免费榜"或"付费榜"或"畅销榜"标签
                tab_text = rank_type_map.get(rank_type, '免费榜')
                try:
                    tab_btn = await page.wait_for_selector(f'text="{tab_text}"', timeout=10000)
                    await tab_btn.click()
                    await asyncio.sleep(5)
                    logger.info(f"✅ 已点击 {tab_text}")
                except Exception as e:
                    logger.warning(f"⚠️ 未找到 {tab_text} 标签：{e}")
                
                # 滚动加载
                logger.info("📜 滚动加载更多...")
                for i in range(5):
                    await page.evaluate("window.scrollBy(0, 1000)")
                    await asyncio.sleep(2)
                
                # Step 6: 截图
                screenshot_path = Path(__file__).parent.parent / f"debug_{channel}_rank.png"
                await page.screenshot(path=str(screenshot_path), full_page=True)
                logger.info(f"📸 截图：{screenshot_path}")
                
                # Step 7: 保存 HTML
                html_path = Path(__file__).parent.parent / f"debug_{channel}_rank.html"
                with open(html_path, 'w', encoding='utf-8') as f:
                    html = await page.content()
                    f.write(html)
                logger.info(f"📄 HTML: {html_path}")
                
                # Step 8: 提取榜单数据
                logger.info("📊 提取榜单数据...")
                apps = await self._extract_rank_data(page, limit)
                logger.info(f"✅ 提取到 {len(apps)} 个应用")
                
                await context.close()
                
                return {
                    "channel": channel,
                    "channel_name": channel_name,
                    "rank_type": rank_type,
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
                    "rank_type": rank_type,
                    "apps": [],
                    "error": str(e),
                }
    
    async def _extract_rank_data(self, page, limit: int = 100) -> List:
        """提取榜单数据"""
        try:
            apps_data = await page.evaluate('''() => {
                const apps = [];
                
                // 查找所有应用行
                const rows = document.querySelectorAll('[class*="dd-data-table-row"], tr[class*="row"]');
                console.log(`找到 ${rows.length} 行`);
                
                for (const row of rows) {
                    // 提取排名
                    const rankEl = row.querySelector('[class*="rank"], td:first-child');
                    const rank = rankEl ? rankEl.textContent.trim() : '';
                    
                    // 提取应用名称
                    const nameEl = row.querySelector('.app-name-text, [class*="app-name"]');
                    const name = nameEl ? nameEl.textContent.trim() : '';
                    
                    // 跳过无效数据
                    if (!name || name.length < 2 || name.length > 100) continue;
                    if (name.includes('排名') || name.includes('应用') || name.includes('监控')) continue;
                    
                    // 提取开发者信息
                    let developer = '';
                    const descEl = row.querySelector('.desc, [class*="developer"]');
                    if (descEl) {
                        developer = descEl.textContent.trim();
                    }
                    
                    // 提取分类
                    let category = '';
                    const categoryEl = row.querySelectorAll('td')[3];
                    if (categoryEl) {
                        category = categoryEl.textContent.trim();
                    }
                    
                    apps.push({
                        rank: rank,
                        name: name,
                        developer: developer,
                        category: category
                    });
                    
                    console.log(`提取到：${rank}. ${name}`);
                    
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
            
            # 返回 RankApp 数据类
            return [
                RankApp(
                    rank=int(app['rank']) if app['rank'].isdigit() else 0,
                    app_name=app['name'],
                    package_name='',
                    developer=app.get('developer', ''),
                    category=app.get('category', ''),
                    change=0
                )
                for app in unique_apps if app['rank'] and app['name']
            ]
            
        except Exception as e:
            logger.error(f"❌ 提取失败：{e}")
            import traceback
            traceback.print_exc()
            return []


async def test_android_rank():
    """测试安卓榜单"""
    fetcher = DiandianAndroidRankFetcher()
    
    print("\n📱 测试华为渠道（国内安卓榜单）...\n")
    
    # 测试免费榜
    print("="*60)
    print("测试免费榜")
    print("="*60)
    free_data = await fetcher.fetch_rank_data('huawei', 'free', limit=50)
    
    print(f"\n华为渠道 - 免费榜:")
    print(f"  获取到：{len(free_data.get('apps', []))} 个应用")
    
    if free_data.get('apps'):
        print(f"\n  前 20 个应用:")
        for i, app in enumerate(free_data['apps'][:20], 1):
            print(f"    {i}. {app.app_name} - {app.developer}")
    
    # 测试付费榜
    print("\n" + "="*60)
    print("测试付费榜")
    print("="*60)
    paid_data = await fetcher.fetch_rank_data('huawei', 'paid', limit=50)
    
    print(f"\n华为渠道 - 付费榜:")
    print(f"  获取到：{len(paid_data.get('apps', []))} 个应用")
    
    if paid_data.get('apps'):
        print(f"\n  前 20 个应用:")
        for i, app in enumerate(paid_data['apps'][:20], 1):
            print(f"    {i}. {app.app_name} - {app.developer}")
    



if __name__ == "__main__":
    asyncio.run(test_android_rank())
