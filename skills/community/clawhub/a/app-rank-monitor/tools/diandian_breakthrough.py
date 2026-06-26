#!/usr/bin/env python3
"""
点点数据安卓渠道榜单爬虫 - 突破版
策略：不依赖特定文本，直接提取页面所有可能的应用数据
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
logger = logging.getLogger('DiandianBreakthrough')


class DiandianBreakthroughFetcher:
    """点点数据突破版爬虫"""
    
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
                    headless=False,  # 显示窗口
                    channel='chrome',
                    args=['--disable-blink-features=AutomationControlled', '--no-sandbox']
                )
                
                page = context.pages[0] if context.pages else await context.new_page()
                await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                # Step 1: 访问并登录
                await page.goto("https://app.diandian.com/", wait_until="domcontentloaded", timeout=60000)
                await asyncio.sleep(3)
                
                # 检查登录
                is_logged = '退出' in await page.content() or '账号设置' in await page.content()
                if not is_logged:
                    logger.error("❌ 未登录！")
                    await context.close()
                    return {"error": "未登录"}
                
                logger.info("✅ 已登录")
                
                # Step 2: 导航到安卓榜单
                logger.info("📖 导航到安卓榜单...")
                
                # 使用 JavaScript 强制导航
                await page.evaluate('''() => {
                    // 尝试点击市场情报
                    const marketBtn = Array.from(document.querySelectorAll('*')).find(el => el.textContent.includes('市场情报'));
                    if (marketBtn) marketBtn.click();
                }''')
                await asyncio.sleep(2)
                
                # 点击国内安卓榜单
                await page.evaluate('''() => {
                    const androidBtn = Array.from(document.querySelectorAll('*')).find(el => el.textContent.includes('国内安卓榜单'));
                    if (androidBtn) androidBtn.click();
                }''')
                await asyncio.sleep(3)
                
                logger.info("✅ 已导航到安卓榜单")
                
                # Step 3: 选择渠道
                logger.info(f"📖 选择 {self.CHANNELS[channel]}...")
                channel_name = self.CHANNELS[channel]
                
                await page.evaluate(f'''() => {{
                    const channelBtn = Array.from(document.querySelectorAll('*')).find(el => 
                        el.textContent.includes('{channel_name}') && 
                        !el.textContent.includes('榜单')
                    );
                    if (channelBtn) channelBtn.click();
                }}''')
                await asyncio.sleep(3)
                
                logger.info(f"✅ 已选择 {channel_name}")
                
                # Step 4: 截图
                screenshot_path = Path(__file__).parent.parent / f"debug_{channel}_breakthrough.png"
                await page.screenshot(path=str(screenshot_path), full_page=True)
                logger.info(f"📸 截图：{screenshot_path}")
                
                # Step 5: 保存完整 HTML
                html_path = Path(__file__).parent.parent / f"debug_{channel}_breakthrough.html"
                with open(html_path, 'w', encoding='utf-8') as f:
                    html = await page.content()
                    f.write(html)
                logger.info(f"📄 HTML: {html_path}")
                
                # Step 6: 提取所有文本块，分析结构
                logger.info("🔍 分析页面结构...")
                text_blocks = await page.evaluate('''() => {
                    const blocks = [];
                    const allElements = document.querySelectorAll('*');
                    
                    for (const el of allElements) {
                        const text = el.textContent.trim();
                        const rect = el.getBoundingClientRect();
                        
                        // 只收集可见的、有意义的文本块
                        if (text && 
                            text.length > 5 && 
                            text.length < 200 && 
                            rect.width > 100 && 
                            rect.height > 20 &&
                            !text.includes('市场情报') &&
                            !text.includes('榜单') &&
                            !text.includes('监控')
                        ) {
                            blocks.push({
                                text: text,
                                tag: el.tagName,
                                class: el.className,
                                width: rect.width,
                                height: rect.height
                            });
                        }
                    }
                    
                    return blocks.slice(0, 50);
                }''')
                
                logger.info(f"📊 找到 {len(text_blocks)} 个文本块")
                for i, block in enumerate(text_blocks[:10], 1):
                    logger.info(f"  {i}. [{block['tag']}] {block['text'][:80]}")
                
                # Step 7: 尝试提取应用数据
                logger.info("📊 提取应用数据...")
                apps = await self._extract_apps_v3(page, limit)
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
    
    async def _extract_apps_v3(self, page, limit: int = 100) -> List:
        """增强版数据提取"""
        try:
            apps_data = await page.evaluate('''() => {
                const apps = [];
                
                // 策略：查找所有表格行
                const tables = document.querySelectorAll('table');
                console.log(`找到 ${tables.length} 个表格`);
                
                for (const table of tables) {
                    const rows = table.querySelectorAll('tr');
                    console.log(`表格有 ${rows.length} 行`);
                    
                    for (let i = 0; i < rows.length && apps.length < 100; i++) {
                        const row = rows[i];
                        const cells = row.querySelectorAll('td');
                        
                        if (cells.length >= 2) {
                            const rank = cells[0]?.textContent.trim() || '';
                            const name = cells[1]?.textContent.trim() || '';
                            const developer = cells[2]?.textContent.trim() || '';
                            const category = cells[3]?.textContent.trim() || '';
                            
                            // 验证
                            if (name && 
                                name.length > 1 && 
                                name.length < 100 && 
                                !/^[\\d\\s]+$/.test(name) &&
                                !name.includes('排名') &&
                                !name.includes('应用')
                            ) {
                                apps.push({
                                    rank, name, developer, category,
                                    date: new Date().toISOString().split('T')[0]
                                });
                            }
                        }
                    }
                }
                
                // 如果表格没找到，尝试其他方式
                if (apps.length === 0) {
                    const allDivs = document.querySelectorAll('div, span, a');
                    for (const div of allDivs) {
                        const text = div.textContent.trim();
                        if (text && text.length > 3 && text.length < 50 && !/[\\(\\)\\(\\)]/.test(text)) {
                            // 可能是应用名
                            apps.push({
                                rank: '',
                                name: text,
                                developer: '',
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
                if app['name'] not in seen and app['name'].length > 1:
                    seen.add(app['name'])
                    unique_apps.append(app)
            
            return [
                NewApp(
                    app_name=app['name'],
                    package_name='',
                    developer=app.get('developer', ''),
                    category=app.get('category', ''),
                    release_date=app.get('date', datetime.now().strftime('%Y-%m-%d'))
                )
                for app in unique_apps if len(app['name']) > 1 and len(app['name']) < 100
            ]
            
        except Exception as e:
            logger.error(f"❌ 提取失败：{e}")
            return []


async def test_breakthrough():
    """测试突破版"""
    fetcher = DiandianBreakthroughFetcher()
    
    print("\n📱 测试华为渠道（突破版）...\n")
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
    asyncio.run(test_breakthrough())
