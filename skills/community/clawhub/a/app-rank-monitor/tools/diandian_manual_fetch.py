#!/usr/bin/env python3
"""
点点数据安卓渠道榜单爬虫 - 人工模拟版
完全模拟人工操作：登录 → 市场情报 → 安卓榜单 → 选择渠道 → 获取数据
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
logger = logging.getLogger('DiandianManual')


class DiandianManualFetcher:
    """点点数据人工模拟爬虫"""
    
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
            channel: 渠道名称 (huawei/xiaomi/etc.)
            app_type: 数据类型 ('new' 新上架，'offline' 下架)
            limit: 数量限制
        """
        logger.info(f"📱 开始获取 {self.CHANNELS[channel]} 渠道 {'新上架' if app_type == 'new' else '下架'} 数据...")
        
        async with async_playwright() as p:
            try:
                user_data_dir = Path(__file__).parent.parent / ".browser_data" / "diandian"
                user_data_dir.mkdir(parents=True, exist_ok=True)
                
                context = await p.chromium.launch_persistent_context(
                    user_data_dir=str(user_data_dir),
                    headless=False,  # 显示窗口，方便调试
                    channel='chrome',
                    args=['--disable-blink-features=AutomationControlled', '--no-sandbox']
                )
                
                page = context.pages[0] if context.pages else await context.new_page()
                await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                # ========== Step 1: 访问并登录 ==========
                logger.info("📖 Step 1: 访问主页...")
                await page.goto("https://app.diandian.com/", wait_until="domcontentloaded", timeout=60000)
                await asyncio.sleep(3)
                
                # 检查登录状态
                page_content = await page.content()
                is_logged = '退出' in page_content or '账号设置' in page_content
                
                if not is_logged:
                    logger.error("❌ 未登录！请先运行：python tools/diandian_auto_login.py")
                    # 保存截图
                    await page.screenshot(path=str(Path(__file__).parent.parent / "debug_not_logged_in.png"))
                    await context.close()
                    return {"error": "未登录"}
                
                logger.info("✅ 已登录")
                
                # ========== Step 2: 点击市场情报 ==========
                logger.info("📖 Step 2: 点击'市场情报'...")
                
                # 等待并点击市场情报
                try:
                    market_intel = await page.wait_for_selector('text="市场情报"', timeout=10000)
                    await market_intel.click()
                    await asyncio.sleep(2)
                    logger.info("✅ 已点击市场情报")
                except Exception as e:
                    logger.error(f"❌ 未找到市场情报按钮：{e}")
                    await context.close()
                    return {"error": "未找到市场情报"}
                
                # ========== Step 3: 点击国内安卓榜单 ==========
                logger.info("📖 Step 3: 点击'国内安卓榜单'...")
                
                try:
                    android_rank = await page.wait_for_selector('text="国内安卓榜单"', timeout=10000)
                    await android_rank.click()
                    await asyncio.sleep(3)
                    logger.info("✅ 已点击国内安卓榜单")
                except Exception as e:
                    logger.error(f"❌ 未找到国内安卓榜单：{e}")
                    await context.close()
                    return {"error": "未找到安卓榜单"}
                
                # ========== Step 4: 选择渠道 ==========
                logger.info(f"📖 Step 4: 选择渠道 '{self.CHANNELS[channel]}'...")
                
                try:
                    # 查找渠道按钮（可能是文本或图片）
                    channel_btn = await page.wait_for_selector(f'text="{self.CHANNELS[channel]}"', timeout=10000)
                    await channel_btn.click()
                    await asyncio.sleep(3)
                    logger.info(f"✅ 已选择 {self.CHANNELS[channel]}")
                except Exception as e:
                    logger.error(f"❌ 未找到渠道按钮：{e}")
                    await context.close()
                    return {"error": f"未找到渠道 {channel}"}
                
                # ========== Step 5: 点击新上架/下架标签 ==========
                tab_text = "新上架" if app_type == "new" else "下架"
                logger.info(f"📖 Step 5: 点击'{tab_text}'...")
                
                try:
                    tab = await page.wait_for_selector(f'text="{tab_text}"', timeout=10000)
                    await tab.click()
                    await asyncio.sleep(3)  # 等待数据加载
                    logger.info(f"✅ 已点击 {tab_text}")
                except Exception as e:
                    logger.error(f"❌ 未找到 {tab_text} 标签：{e}")
                    # 继续尝试提取，可能默认就是该标签
                
                # ========== Step 6: 截图保存证据 ==========
                screenshot_path = Path(__file__).parent.parent / f"debug_{channel}_{app_type}.png"
                await page.screenshot(path=str(screenshot_path), full_page=True)
                logger.info(f"📸 截图已保存：{screenshot_path}")
                
                # ========== Step 7: 提取表格数据 ==========
                logger.info("📊 Step 7: 提取应用数据...")
                apps = await self._extract_table_data(page, limit)
                logger.info(f"✅ 提取到 {len(apps)} 个应用")
                
                # ========== Step 8: 保存 HTML 用于调试 ==========
                html_path = Path(__file__).parent.parent / f"debug_{channel}_{app_type}.html"
                html_content = await page.content()
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html_content[:100000])  # 保存前 100KB
                logger.info(f"📄 HTML 已保存：{html_path}")
                
                await context.close()
                
                return {
                    "channel": channel,
                    "channel_name": self.CHANNELS[channel],
                    "type": app_type,
                    "apps": apps,
                    "fetch_time": datetime.now().isoformat(),
                }
                
            except Exception as e:
                logger.error(f"❌ 获取失败：{e}")
                import traceback
                traceback.print_exc()
                return {
                    "channel": channel,
                    "channel_name": self.CHANNELS.get(channel, channel),
                    "type": app_type,
                    "apps": [],
                    "error": str(e),
                }
    
    async def _extract_table_data(self, page, limit: int = 100) -> List:
        """
        从表格中提取应用数据
        关键：找到正确的表格选择器
        """
        try:
            # 等待表格出现
            try:
                await page.wait_for_selector('table, [class*="table"], [class*="list"]', timeout=5000)
                await asyncio.sleep(2)
            except:
                logger.warning("⚠️ 未找到表格，尝试直接提取")
            
            # 使用 JavaScript 提取数据
            apps_data = await page.evaluate('''() => {
                const apps = [];
                
                // 策略 1: 查找表格行
                let rows = document.querySelectorAll('table tr');
                
                // 策略 2: 如果表格没找到，尝试列表
                if (rows.length < 5) {
                    rows = document.querySelectorAll('[class*="row"], [class*="item"], .list-item');
                }
                
                console.log(`找到 ${rows.length} 行`);
                
                for (let i = 0; i < rows.length; i++) {
                    const row = rows[i];
                    const text = row.textContent.trim();
                    
                    // 跳过空行和表头
                    if (!text || text.length < 5 || text.length > 300) continue;
                    if (text.includes('排名') || text.includes('应用') || text.includes('开发者')) continue;
                    
                    // 获取所有单元格
                    const cells = row.querySelectorAll('td, div, span');
                    
                    let rank = '';
                    let name = '';
                    let developer = '';
                    let package_name = '';
                    let category = '';
                    let date = '';
                    
                    // 尝试从单元格提取
                    if (cells.length >= 3) {
                        // 假设有排名、应用名、开发者等列
                        rank = cells[0]?.textContent.trim() || '';
                        name = cells[1]?.textContent.trim() || '';
                        developer = cells[2]?.textContent.trim() || '';
                        
                        // 如果有更多列
                        if (cells.length >= 4) {
                            category = cells[3]?.textContent.trim() || '';
                        }
                        if (cells.length >= 5) {
                            date = cells[4]?.textContent.trim() || '';
                        }
                    } else {
                        // 从文本行提取
                        const lines = text.split('\\n').filter(l => l.trim());
                        if (lines.length >= 2) {
                            if (/^\\d+$/.test(lines[0])) {
                                rank = lines[0];
                                name = lines[1];
                                developer = lines[2] || '';
                            } else {
                                name = lines[0];
                                developer = lines[1] || '';
                            }
                        }
                    }
                    
                    // 清理数据
                    name = name.replace(/[\\(\\（].*[\\)\\）]/, '').trim(); // 移除包名
                    if (name && name.length > 1 && name.length < 100 && !/^[\\d\\s]+$/.test(name)) {
                        apps.push({
                            rank: rank,
                            name: name,
                            developer: developer,
                            package: package_name,
                            category: category,
                            date: date || new Date().toISOString().split('T')[0]
                        });
                    }
                }
                
                console.log(`提取到 ${apps.length} 个应用`);
                return apps.slice(0, 100);
            }''')
            
            # 转换为数据类
            return [
                NewApp(
                    app_name=app['name'],
                    package_name=app.get('package', ''),
                    developer=app.get('developer', ''),
                    category=app.get('category', ''),
                    release_date=app.get('date', datetime.now().strftime('%Y-%m-%d'))
                )
                for app in apps_data if app.get('name')
            ]
            
        except Exception as e:
            logger.error(f"❌ 提取失败：{e}")
            return []
    
    async def fetch_all_channels(self, limit: int = 50) -> Dict:
        """获取所有渠道的数据"""
        results = {}
        
        for channel in self.CHANNELS.keys():
            # 获取新上架
            new_data = await self.fetch_channel_data(channel, 'new', limit)
            
            # 等待一下
            await asyncio.sleep(2)
            
            # 获取下架
            offline_data = await self.fetch_channel_data(channel, 'offline', limit)
            
            results[channel] = {
                "new_apps": new_data.get('apps', []),
                "offline_apps": offline_data.get('apps', []),
            }
            
            logger.info(f"✅ {channel} 完成：新上架 {len(new_data.get('apps', []))} 个，下架 {len(offline_data.get('apps', []))} 个")
            await asyncio.sleep(2)
        
        return results


# 测试函数
async def test_manual():
    """测试人工模拟爬虫"""
    fetcher = DiandianManualFetcher()
    
    print("\n📱 测试华为渠道（人工模拟）...")
    print("⚠️  将显示浏览器窗口，请观察操作过程\n")
    
    # 获取新上架
    data = await fetcher.fetch_channel_data('huawei', 'new', limit=20)
    
    print(f"\n华为渠道 - 新上架:")
    print(f"  获取到：{len(data.get('apps', []))} 个应用")
    
    if data.get('apps'):
        print(f"\n  前 10 个应用:")
        for i, app in enumerate(data['apps'][:10], 1):
            print(f"    {i}. {app.app_name} - {app.developer}")
    
    if data.get('error'):
        print(f"\n  错误：{data['error']}")
    
    print(f"\n📸 查看截图：debug_huawei_new.png")
    print(f"📄 查看 HTML: debug_huawei_new.html")


if __name__ == "__main__":
    asyncio.run(test_manual())
