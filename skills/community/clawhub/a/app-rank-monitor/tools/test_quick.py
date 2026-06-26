#!/usr/bin/env python3
"""
点点数据导出 - 快速测试版本
用于诊断问题出在哪一步
"""

import asyncio
import yaml
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('DiandianTest')


async def test_step_by_step():
    """逐步测试每个步骤"""
    
    logger.info("="*60)
    logger.info("开始测试点点数据导出流程")
    logger.info("="*60)
    
    async with async_playwright() as p:
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
        
        try:
            # Step 1: 访问主页
            logger.info("\n[Step 1/6] 访问点点数据主页...")
            start = datetime.now()
            await page.goto("https://app.diandian.com/", wait_until="domcontentloaded", timeout=60000)
            logger.info(f"✅ 主页加载成功 (耗时：{(datetime.now()-start).total_seconds():.1f}秒)")
            await asyncio.sleep(2)
            
            # Step 2: 检查登录状态
            logger.info("\n[Step 2/6] 检查登录状态...")
            start = datetime.now()
            page_content = await page.content()
            is_logged = '退出' in page_content or '账号设置' in page_content
            logger.info(f"✅ 登录状态：{'已登录' if is_logged else '未登录'} (耗时：{(datetime.now()-start).total_seconds():.1f}秒)")
            await asyncio.sleep(2)
            
            # Step 3: 点击市场情报
            logger.info("\n[Step 3/6] 点击'市场情报'...")
            start = datetime.now()
            market_btn = await page.wait_for_selector('text="市场情报"', timeout=10000)
            await market_btn.click()
            await asyncio.sleep(3)
            logger.info(f"✅ 已点击市场情报 (耗时：{(datetime.now()-start).total_seconds():.1f}秒)")
            
            # Step 4: 点击上架监控
            logger.info("\n[Step 4/6] 点击'上架监控'...")
            start = datetime.now()
            monitor_btn = await page.wait_for_selector('text="上架监控"', timeout=10000)
            await monitor_btn.click()
            await asyncio.sleep(5)
            logger.info(f"✅ 已进入上架监控页面 (耗时：{(datetime.now()-start).total_seconds():.1f}秒)")
            
            # Step 5: 选择华为渠道
            logger.info("\n[Step 5/6] 选择'华为'渠道...")
            start = datetime.now()
            result = await page.evaluate('''() => {
                const allDivs = document.querySelectorAll('div');
                for (const div of allDivs) {
                    if (div.textContent.includes('华为') && div.className.includes('app-name')) {
                        div.click();
                        return true;
                    }
                }
                return false;
            }''')
            await asyncio.sleep(3)
            logger.info(f"✅ 已选择华为渠道 (耗时：{(datetime.now()-start).total_seconds():.1f}秒)")
            
            # Step 6: 点击导出按钮
            logger.info("\n[Step 6/6] 点击'导出数据'按钮...")
            start = datetime.now()
            result = await page.evaluate('''() => {
                const allButtons = document.querySelectorAll('button, [role="button"]');
                for (const btn of allButtons) {
                    const text = btn.textContent.trim();
                    if (text.includes('导出') || text.includes('下载')) {
                        btn.click();
                        return true;
                    }
                }
                return false;
            }''')
            await asyncio.sleep(3)
            logger.info(f"✅ 已点击导出按钮 (耗时：{(datetime.now()-start).total_seconds():.1f}秒)")
            
            logger.info("\n" + "="*60)
            logger.info("🎉 所有步骤测试完成！")
            logger.info("="*60)
            
            # 等待用户观察
            logger.info("\n请在浏览器中查看弹窗是否出现...")
            await asyncio.sleep(10)
            
            await context.close()
            return True
            
        except Exception as e:
            logger.error(f"\n❌ 测试失败：{e}")
            import traceback
            traceback.print_exc()
            
            # 保存错误截图
            screenshot_path = Path(__file__).parent.parent / "debug_test_error.png"
            await page.screenshot(path=str(screenshot_path))
            logger.info(f"📸 错误截图已保存：{screenshot_path}")
            
            await context.close()
            return False


if __name__ == "__main__":
    success = asyncio.run(test_step_by_step())
    
    if success:
        print("\n✅ 测试成功！脚本可以正常运行。")
        print("\n如果下载弹窗出现了但文件没有下载，可能是:")
        print("1. 浏览器下载设置问题")
        print("2. 弹窗中的按钮没有找到")
        print("3. 需要手动点击一次下载按钮")
    else:
        print("\n❌ 测试失败！请查看错误日志和截图。")
