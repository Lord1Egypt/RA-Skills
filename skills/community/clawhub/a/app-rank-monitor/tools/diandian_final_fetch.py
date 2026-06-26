#!/usr/bin/env python3
"""
点点数据安卓渠道榜单爬虫 - 最终优化版
修复：国内安卓榜单按钮需要 hover 或特殊点击方式
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
logger = logging.getLogger('DiandianFinal')


class DiandianFinalFetcher:
    """点点数据最终版爬虫"""
    
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
                
                # Step 1: 访问主页
                await page.goto("https://app.diandian.com/", wait_until="domcontentloaded", timeout=60000)
                await asyncio.sleep(3)
                
                # 检查登录
                page_content = await page.content()
                is_logged = '退出' in page_content or '账号设置' in page_content
                if not is_logged:
                    logger.error("❌ 未登录！")
                    await context.close()
                    return {"error": "未登录"}
                
                logger.info("✅ 已登录")
                
                # Step 2: 点击市场情报
                logger.info("📖 点击'市场情报'...")
                market_intel = await page.wait_for_selector('text="市场情报"', timeout=10000)
                await market_intel.click()
                await asyncio.sleep(2)
                logger.info("✅ 已点击市场情报")
                
                # Step 3: 点击国内安卓榜单（使用 JavaScript 强制点击）
                logger.info("📖 点击'国内安卓榜单'...")
                
                # 尝试多种方式
                android_clicked = False
                
                # 方式 1: 直接文本选择
                try:
                    android_btns = await page.query_selector_all('text="国内安卓榜单"')
                    if android_btns:
                        # 使用 JavaScript 点击
                        await page.evaluate('''() => {
                            const btns = document.querySelectorAll('span.rank-name');
                            for (const btn of btns) {
                                if (btn.textContent.includes('国内安卓榜单')) {
                                    btn.click();
                                    return true;
                                }
                            }
                            return false;
                        }''')
                        await asyncio.sleep(3)
                        android_clicked = True
                        logger.info("✅ (JS 点击) 已点击国内安卓榜单")
                except Exception as e:
                    logger.warning(f"方式 1 失败：{e}")
                
                # 方式 2: 如果还没成功，尝试访问已知 URL
                if not android_clicked:
                    logger.info("📖 尝试直接访问安卓榜单 URL...")
                    await page.goto("https://app.diandian.com/zh/list/android", wait_until="domcontentloaded", timeout=30000)
                    await asyncio.sleep(3)
                    logger.info("✅ 已导航到安卓榜单页面")
                
                # Step 4: 截图
                screenshot_path = Path(__file__).parent.parent / f"debug_{channel}_final.png"
                await page.screenshot(path=str(screenshot_path), full_page=True)
                logger.info(f"📸 截图：{screenshot_path}")
                
                # Step 5: 选择渠道
                logger.info(f"📖 选择渠道 '{self.CHANNELS[channel]}'...")
                try:
                    channel_btn = await page.wait_for_selector(f'text="{self.CHANNELS[channel]}"', timeout=10000)
                    await channel_btn.click()
                    await asyncio.sleep(3)
                    logger.info(f"✅ 已选择 {self.CHANNELS[channel]}")
                except Exception as e:
                    logger.warning(f"⚠️ 未找到渠道按钮，可能已在当前页面：{e}")
                
                # Step 6: 点击新上架/下架标签
                tab_text = "新上架" if app_type == "new" else "下架"
                logger.info(f"📖 点击'{tab_text}'...")
                try:
                    tab = await page.wait_for_selector(f'text="{tab_text}"', timeout=10000)
                    await tab.click()
                    await asyncio.sleep(3)
                    logger.info(f"✅ 已点击 {tab_text}")
                except Exception as e:
                    logger.warning(f"⚠️ 未找到标签：{e}")
                
                # Step 7: 提取数据
                logger.info("📊 提取应用数据...")
                apps = await self._extract_apps(page, limit)
                logger.info(f"✅ 提取到 {len(apps)} 个应用")
                
                # Step 8: 保存 HTML
                html_path = Path(__file__).parent.parent / f"debug_{channel}_final.html"
                with open(html_path, 'w', encoding='utf-8') as f:
                    html = await page.content()
                    f.write(html[:100000])
                logger.info(f"📄 HTML: {html_path}")
                
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
    
    async def _extract_apps(self, page, limit: int = 100) -> List:
        """提取应用数据"""
        try:
            # 等待表格
            try:
                await page.wait_for_selector('table', timeout=5000)
                await asyncio.sleep(2)
            except:
                pass
            
            apps_data = await page.evaluate('''() => {
                const apps = [];
                
                // 查找表格行
                const rows = document.querySelectorAll('table tr');
                console.log(`找到 ${rows.length} 行`);
                
                for (let i = 1; i < rows.length && apps.length < 100; i++) { // 跳过表头
                    const row = rows[i];
                    const cells = row.querySelectorAll('td');
                    
                    if (cells.length >= 2) {
                        const rank = cells[0]?.textContent.trim() || '';
                        const name = cells[1]?.textContent.trim() || '';
                        const developer = cells[2]?.textContent.trim() || '';
                        const category = cells[3]?.textContent.trim() || '';
                        const date = cells[4]?.textContent.trim() || new Date().toISOString().split('T')[0];
                        
                        // 验证
                        if (name && name.length > 1 && name.length < 100) {
                            apps.push({
                                rank, name, developer, category, date
                            });
                        }
                    }
                }
                
                console.log(`提取到 ${apps.length} 个应用`);
                return apps;
            }''')
            
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
            
        except Exception as e:
            logger.error(f"❌ 提取失败：{e}")
            return []


async def test_final():
    """测试最终版"""
    fetcher = DiandianFinalFetcher()
    
    print("\n📱 测试华为渠道（最终版）...\n")
    data = await fetcher.fetch_channel_data('huawei', 'new', limit=20)
    
    print(f"\n华为渠道 - 新上架:")
    print(f"  获取到：{len(data.get('apps', []))} 个应用")
    
    if data.get('apps'):
        print(f"\n  前 10 个应用:")
        for i, app in enumerate(data['apps'][:10], 1):
            print(f"    {i}. {app.app_name} - {app.developer}")
    
    if data.get('error'):
        print(f"\n  错误：{data['error']}")


if __name__ == "__main__":
    asyncio.run(test_final())
