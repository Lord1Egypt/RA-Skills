#!/usr/bin/env python3
"""
点点数据安卓渠道榜单爬虫 - 网页版（优化版）
支持渠道：华为、小米、应用宝、OPPO、vivo、百度、360、豌豆荚
获取数据：新上架榜单、下架榜单
"""

import asyncio
import sys
import yaml
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from playwright.async_api import async_playwright

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from rankers.base import NewApp, OfflineApp
from utils.logger import setup_logger

logger = setup_logger()


class DiandianAndroidWebRanker:
    """点点数据安卓渠道网页爬虫（优化版）"""
    
    # 安卓渠道映射
    CHANNELS = {
        "huawei": {"name": "华为", "keywords": ["华为", "huawei"]},
        "xiaomi": {"name": "小米", "keywords": ["小米", "xiaomi"]},
        "tencent": {"name": "应用宝", "keywords": ["应用宝", "腾讯"]},
        "oppo": {"name": "OPPO", "keywords": ["OPPO", "oppo"]},
        "vivo": {"name": "vivo", "keywords": ["vivo", "VIVO"]},
        "baidu": {"name": "百度", "keywords": ["百度", "baidu"]},
        "qihoo360": {"name": "360", "keywords": ["360", "三六零"]},
        "wandoujia": {"name": "豌豆荚", "keywords": ["豌豆荚", "wandoujia"]},
    }
    
    def __init__(self):
        """初始化"""
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """加载配置"""
        config_path = Path(__file__).parent.parent.parent / "config" / "diandian.yaml"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {"token": ""}
    
    async def fetch_channel_data(self, channel: str, limit: int = 100) -> Dict:
        """
        获取指定渠道的数据
        
        Args:
            channel: 渠道名称
            limit: 数量限制
            
        Returns:
            包含新上架和下架数据的字典
        """
        logger.info(f"📱 开始获取 {channel} 渠道数据...")
        
        async with async_playwright() as p:
            try:
                # 启动浏览器
                user_data_dir = Path(__file__).parent.parent.parent / ".browser_data" / "diandian"
                user_data_dir.mkdir(parents=True, exist_ok=True)
                
                context = await p.chromium.launch_persistent_context(
                    user_data_dir=str(user_data_dir),
                    headless=True,
                    channel='chrome',
                    args=['--disable-blink-features=AutomationControlled', '--no-sandbox']
                )
                
                page = context.pages[0] if context.pages else await context.new_page()
                
                # 防检测
                await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                # Step 1: 访问主页
                logger.info("📖 访问点点数据主页...")
                await page.goto("https://app.diandian.com/", wait_until="domcontentloaded", timeout=60000)
                await asyncio.sleep(3)
                
                # Step 2: 检查登录状态
                page_content = await page.content()
                is_logged = '退出' in page_content or '账号设置' in page_content
                
                if not is_logged:
                    logger.error("❌ 未登录，请先运行 tools/diandian_auto_login.py")
                    await context.close()
                    return {
                        "channel": channel,
                        "channel_name": self.CHANNELS.get(channel, {}).get('name', channel),
                        "new_apps": [],
                        "offline_apps": [],
                        "fetch_time": datetime.now().isoformat(),
                        "error": "未登录",
                    }
                
                logger.info("✅ 已登录状态")
                
                # Step 3: 尝试访问安卓榜单页面
                # 直接构造 URL（如果知道的话）
                # 或者通过导航
                logger.info("📖 导航到安卓榜单页面...")
                
                # 尝试点击"市场情报"
                try:
                    market_intel = await page.wait_for_selector('text=市场情报', timeout=5000)
                    if market_intel:
                        await market_intel.click()
                        await asyncio.sleep(2)
                        logger.info("✅ 已点击市场情报")
                except:
                    logger.warning("⚠️ 未找到市场情报按钮")
                
                # 尝试点击"国内安卓榜单"
                try:
                    android_rank = await page.wait_for_selector('text=国内安卓榜单', timeout=5000)
                    if android_rank:
                        await android_rank.click()
                        await asyncio.sleep(3)
                        logger.info("✅ 已点击国内安卓榜单")
                except:
                    logger.warning("⚠️ 未找到国内安卓榜单按钮")
                
                # Step 4: 截图调试
                screenshot_path = Path(__file__).parent.parent.parent / "debug_android_page.png"
                await page.screenshot(path=str(screenshot_path))
                logger.info(f"📸 截图已保存：{screenshot_path}")
                
                # Step 5: 获取页面 HTML 分析结构
                html = await page.content()
                html_path = Path(__file__).parent.parent.parent / "debug_android_page.html"
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html[:50000])  # 只保存前 50KB
                logger.info(f"📄 HTML 已保存：{html_path}")
                
                # Step 6: 尝试提取数据
                new_apps = await self._extract_apps(page, 'new', limit)
                offline_apps = await self._extract_apps(page, 'offline', limit)
                
                logger.info(f"✅ {channel} 完成：新上架 {len(new_apps)} 个，下架 {len(offline_apps)} 个")
                
                await context.close()
                
                return {
                    "channel": channel,
                    "channel_name": self.CHANNELS.get(channel, {}).get('name', channel),
                    "new_apps": new_apps,
                    "offline_apps": offline_apps,
                    "fetch_time": datetime.now().isoformat(),
                }
                
            except Exception as e:
                logger.error(f"❌ {channel} 渠道获取失败：{e}")
                import traceback
                traceback.print_exc()
                
                return {
                    "channel": channel,
                    "channel_name": self.CHANNELS.get(channel, {}).get('name', channel),
                    "new_apps": [],
                    "offline_apps": [],
                    "fetch_time": datetime.now().isoformat(),
                    "error": str(e),
                }
    
    async def _extract_apps(self, page, app_type: str, limit: int = 100) -> List:
        """
        提取应用数据
        
        Args:
            page: Playwright page
            app_type: 'new' 或 'offline'
            limit: 数量限制
            
        Returns:
            应用列表
        """
        try:
            # 尝试点击对应的标签
            tab_text = "新上架" if app_type == "new" else "下架"
            try:
                tab = await page.wait_for_selector(f'text={tab_text}', timeout=3000)
                if tab:
                    await tab.click()
                    await asyncio.sleep(2)
            except:
                logger.warning(f"⚠️ 未找到 {tab_text} 标签")
            
            # 使用 JavaScript 提取数据
            apps_data = await page.evaluate('''() => {
                const apps = [];
                
                // 尝试多种选择器
                const selectors = [
                    'tr',
                    '[class*="app"]',
                    '[class*="rank"]',
                    '[class*="list"]',
                    '.row',
                    '.item',
                    '[role="row"]',
                ];
                
                let items = [];
                for (const selector of selectors) {
                    items = document.querySelectorAll(selector);
                    if (items.length > 5) {
                        break;
                    }
                }
                
                for (const item of items) {
                    const text = item.textContent.trim();
                    if (text && text.length > 5 && text.length < 300) {
                        const lines = text.split('\\n').map(l => l.trim()).filter(l => l);
                        
                        if (lines.length >= 1 && lines[0] && !lines[0].includes('排名') && !lines[0].includes('应用')) {
                            apps.push({
                                name: lines[0] || '',
                                developer: lines[1] || '',
                                package: lines[2] || '',
                                category: lines[3] || '',
                                date: lines[4] || new Date().toISOString().split('T')[0]
                            });
                        }
                    }
                }
                
                return apps.slice(0, 100);
            }''')
            
            # 转换为数据类
            if app_type == 'new':
                return [
                    NewApp(
                        app_name=app.get('name', ''),
                        package_name=app.get('package', ''),
                        developer=app.get('developer', ''),
                        category=app.get('category', ''),
                        release_date=app.get('date', '')
                    )
                    for app in apps_data if app.get('name') and len(app.get('name', '')) < 100
                ]
            else:
                return [
                    OfflineApp(
                        app_name=app.get('name', ''),
                        package_name=app.get('package', ''),
                        developer=app.get('developer', ''),
                        category=app.get('category', ''),
                        offline_date=app.get('date', '')
                    )
                    for app in apps_data if app.get('name') and len(app.get('name', '')) < 100
                ]
                
        except Exception as e:
            logger.error(f"❌ 提取数据失败：{e}")
            return []
    
    async def fetch_all_channels(self, limit: int = 50) -> Dict[str, Dict]:
        """
        获取所有渠道的数据
        
        Args:
            limit: 每个渠道的数量限制
            
        Returns:
            {渠道名：数据字典}
        """
        result = {}
        
        for channel in self.CHANNELS.keys():
            data = await self.fetch_channel_data(channel, limit)
            result[channel] = data
            logger.info(f"✅ {channel} 完成：新上架 {len(data['new_apps'])} 个，下架 {len(data['offline_apps'])} 个")
            await asyncio.sleep(2)  # 避免请求过快
        
        return result


# 测试函数
async def test_ranker():
    """测试爬虫"""
    ranker = DiandianAndroidWebRanker()
    
    # 测试单个渠道
    print("\n📱 测试华为渠道...")
    data = await ranker.fetch_channel_data('huawei', limit=10)
    
    print(f"\n华为渠道:")
    print(f"  新上架：{len(data['new_apps'])} 个")
    if data['new_apps']:
        print(f"  前 3 个新上架:")
        for i, app in enumerate(data['new_apps'][:3], 1):
            print(f"    {i}. {app.app_name} - {app.developer}")
    
    print(f"\n  下架：{len(data['offline_apps'])} 个")
    if data['offline_apps']:
        print(f"  前 3 个下架:")
        for i, app in enumerate(data['offline_apps'][:3], 1):
            print(f"    {i}. {app.app_name} - {app.developer}")
    
    print(f"\n📸 请查看调试文件:")
    print(f"  - debug_android_page.png")
    print(f"  - debug_android_page.html")


if __name__ == "__main__":
    asyncio.run(test_ranker())
