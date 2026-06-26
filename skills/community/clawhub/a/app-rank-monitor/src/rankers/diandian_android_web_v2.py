#!/usr/bin/env python3
"""
点点数据安卓渠道榜单爬虫 - 优化版 v2
改进数据提取逻辑，使用更精确的选择器
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


class DiandianAndroidWebRankerV2:
    """点点数据安卓渠道网页爬虫（优化版 v2）"""
    
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
        """获取指定渠道的数据"""
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
                    return {"channel": channel, "channel_name": self.CHANNELS.get(channel, {}).get('name', channel), "new_apps": [], "offline_apps": [], "fetch_time": datetime.now().isoformat(), "error": "未登录"}
                
                logger.info("✅ 已登录状态")
                
                # Step 3: 导航到安卓榜单
                logger.info("📖 导航到安卓榜单...")
                
                # 尝试访问已知的安卓榜单 URL
                android_url = "https://app.diandian.com/rank/android"
                await page.goto(android_url, wait_until="domcontentloaded", timeout=30000)
                await asyncio.sleep(3)
                
                # Step 4: 截图调试
                screenshot_path = Path(__file__).parent.parent.parent / f"debug_{channel}.png"
                await page.screenshot(path=str(screenshot_path))
                logger.info(f"📸 截图已保存：{screenshot_path}")
                
                # Step 5: 获取新上架数据
                logger.info("📊 获取新上架应用...")
                new_apps = await self._extract_apps_v2(page, 'new', limit)
                logger.info(f"✅ 获取到 {len(new_apps)} 个新上架应用")
                
                # Step 6: 获取下架数据
                logger.info("📊 获取下架应用...")
                offline_apps = await self._extract_apps_v2(page, 'offline', limit)
                logger.info(f"✅ 获取到 {len(offline_apps)} 个下架应用")
                
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
    
    async def _extract_apps_v2(self, page, app_type: str, limit: int = 100) -> List:
        """
        优化版数据提取逻辑
        """
        try:
            # Step 1: 点击对应的标签
            tab_text = "新上架" if app_type == "new" else "下架"
            try:
                # 等待标签出现
                tab = await page.wait_for_selector(f'text="{tab_text}"', timeout=5000)
                if tab:
                    await tab.click()
                    await asyncio.sleep(2)
                    logger.info(f"✅ 已点击 {tab_text} 标签")
            except Exception as e:
                logger.warning(f"⚠️ 未找到 {tab_text} 标签：{e}")
            
            # Step 2: 等待榜单加载
            await asyncio.sleep(2)
            
            # Step 3: 使用 JavaScript 提取数据
            apps_data = await page.evaluate('''() => {
                const apps = [];
                
                // 尝试多种选择器策略
                const strategies = [
                    // 策略 1: 表格行
                    'table tr',
                    // 策略 2: 列表项
                    '[class*="list"] [class*="item"]',
                    // 策略 3: 应用行
                    '.app-row, [class*="app-row"]',
                    // 策略 4: 排名项
                    '[class*="rank"] tr, [data-rank]',
                    // 策略 5: Flex 布局
                    '.row, .item',
                ];
                
                let items = [];
                for (const selector of strategies) {
                    items = document.querySelectorAll(selector);
                    if (items.length >= 5) {
                        console.log(`使用选择器：${selector}, 找到 ${items.length} 项`);
                        break;
                    }
                }
                
                if (items.length === 0) {
                    // 如果还没找到，尝试获取所有可见的文本块
                    items = document.querySelectorAll('body *');
                }
                
                for (const item of items) {
                    const text = item.textContent.trim();
                    const rect = item.getBoundingClientRect();
                    
                    // 过滤条件
                    if (!text || text.length < 5 || text.length > 300) continue;
                    if (rect.width < 100 || rect.height < 20) continue; // 太小的元素
                    if (text.includes('排名') || text.includes('应用名称') || text.includes('开发者')) continue; // 表头
                    
                    const lines = text.split('\\n').map(l => l.trim()).filter(l => l);
                    
                    // 尝试解析应用信息
                    let app = { name: '', developer: '', package: '', category: '', date: '' };
                    
                    if (lines.length >= 1) {
                        // 策略：第一行可能是应用名
                        const firstLine = lines[0];
                        
                        // 跳过纯数字（排名）
                        if (/^\\d+$/.test(firstLine)) {
                            // 这是排名，尝试下一行
                            if (lines.length >= 2) {
                                app.name = lines[1];
                                app.developer = lines[2] || '';
                            }
                        } else {
                            // 第一行就是应用名
                            app.name = firstLine;
                            app.developer = lines[1] || '';
                        }
                        
                        // 提取包名（如果有）
                        const packageMatch = app.developer.match(/\\(([a-zA-Z0-9._-]+)\\)/);
                        if (packageMatch) {
                            app.package = packageMatch[1];
                            app.developer = app.developer.replace(packageMatch[0], '').trim();
                        }
                        
                        // 提取日期（如果有）
                        const dateMatch = app.developer.match(/(\\d{4}-\\d{2}-\\d{2})/);
                        if (dateMatch) {
                            app.date = dateMatch[1];
                            app.developer = app.developer.replace(dateMatch[1], '').trim();
                        }
                        
                        // 验证应用名是否合理
                        if (app.name && app.name.length > 1 && app.name.length < 100 && !/^[\\d\\s]+$/.test(app.name)) {
                            apps.push(app);
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
                        release_date=app.get('date', '') or datetime.now().strftime('%Y-%m-%d')
                    )
                    for app in apps_data if app.get('name') and len(app.get('name', '')) > 1 and len(app.get('name', '')) < 100
                ]
            else:
                return [
                    OfflineApp(
                        app_name=app.get('name', ''),
                        package_name=app.get('package', ''),
                        developer=app.get('developer', ''),
                        category=app.get('category', ''),
                        offline_date=app.get('date', '') or datetime.now().strftime('%Y-%m-%d')
                    )
                    for app in apps_data if app.get('name') and len(app.get('name', '')) > 1 and len(app.get('name', '')) < 100
                ]
                
        except Exception as e:
            logger.error(f"❌ 提取数据失败：{e}")
            import traceback
            traceback.print_exc()
            return []
    
    async def fetch_all_channels(self, limit: int = 50) -> Dict[str, Dict]:
        """获取所有渠道的数据"""
        result = {}
        
        for channel in self.CHANNELS.keys():
            data = await self.fetch_channel_data(channel, limit)
            result[channel] = data
            logger.info(f"✅ {channel} 完成：新上架 {len(data['new_apps'])} 个，下架 {len(data['offline_apps'])} 个")
            await asyncio.sleep(2)
        
        return result


# 测试函数
async def test_ranker_v2():
    """测试优化版爬虫"""
    ranker = DiandianAndroidWebRankerV2()
    
    # 测试单个渠道
    print("\n📱 测试华为渠道（优化版 v2）...")
    data = await ranker.fetch_channel_data('huawei', limit=20)
    
    print(f"\n华为渠道:")
    print(f"  新上架：{len(data['new_apps'])} 个")
    if data['new_apps']:
        print(f"\n  前 5 个新上架:")
        for i, app in enumerate(data['new_apps'][:5], 1):
            print(f"    {i}. {app.app_name} - {app.developer} ({app.package_name})")
    
    print(f"\n  下架：{len(data['offline_apps'])} 个")
    if data['offline_apps']:
        print(f"\n  前 5 个下架:")
        for i, app in enumerate(data['offline_apps'][:5], 1):
            print(f"    {i}. {app.app_name} - {app.developer} ({app.package_name})")
    
    print(f"\n📸 请查看调试文件:")
    print(f"  - debug_huawei.png")


if __name__ == "__main__":
    asyncio.run(test_ranker_v2())
