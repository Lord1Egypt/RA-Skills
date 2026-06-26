#!/usr/bin/env python3
"""
点点数据安卓渠道网页爬虫 - 调试脚本
用于分析网页结构，找到正确的数据获取方式
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('DiandianDebug')


async def debug_diandian_android():
    """调试点点数据安卓榜单网页结构"""
    logger.info("🔍 开始调试点点数据安卓榜单...")
    
    async with async_playwright() as p:
        # 启动浏览器
        user_data_dir = Path(__file__).parent.parent / ".browser_data" / "diandian"
        
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=False,  # 显示窗口，方便调试
            channel='chrome',
            args=['--disable-blink-features=AutomationControlled']
        )
        
        page = browser.pages[0] if browser.pages else await browser.new_page()
        
        try:
            # Step 1: 访问主页
            logger.info("📖 Step 1: 访问点点数据...")
            await page.goto("https://app.diandian.com/", wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(3)
            
            # Step 2: 检查登录状态
            page_content = await page.content()
            is_logged = '退出' in page_content or '账号设置' in page_content
            logger.info(f"登录状态：{'✅ 已登录' if is_logged else '❌ 未登录'}")
            
            if not is_logged:
                logger.info("⚠️ 请先手动登录，然后按回车继续...")
                input("按回车继续...")
            
            # Step 3: 导航到市场情报
            logger.info("📖 Step 3: 点击'市场情报'...")
            market_intel_btn = await page.query_selector('text=市场情报')
            if market_intel_btn:
                await market_intel_btn.click()
                await asyncio.sleep(3)
                logger.info("✅ 已进入市场情报")
            else:
                logger.warning("⚠️ 未找到'市场情报'按钮")
            
            # Step 4: 导航到国内安卓榜单
            logger.info("📖 Step 4: 点击'国内安卓榜单'...")
            android_btn = await page.query_selector('text=国内安卓榜单')
            if android_btn:
                await android_btn.click()
                await asyncio.sleep(5)
                logger.info("✅ 已进入安卓榜单页面")
            else:
                logger.warning("⚠️ 未找到'国内安卓榜单'按钮")
            
            # Step 5: 截图查看页面
            logger.info("📸 保存页面截图...")
            screenshot_path = Path(__file__).parent.parent / "debug_android_rank.png"
            await page.screenshot(path=str(screenshot_path), full_page=True)
            logger.info(f"✅ 截图已保存：{screenshot_path}")
            
            # Step 6: 获取页面 HTML
            logger.info("📄 获取页面 HTML...")
            html = await page.content()
            html_path = Path(__file__).parent.parent / "debug_android_rank.html"
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html)
            logger.info(f"✅ HTML 已保存：{html_path}")
            
            # Step 7: 分析页面结构
            logger.info("🔍 分析页面结构...")
            
            # 查找渠道选择器
            channel_selectors = await page.query_selector_all('select, [role="listbox"], button')
            logger.info(f"找到 {len(channel_selectors)} 个可能的渠道选择器")
            
            # 查找榜单列表
            list_items = await page.query_selector_all('tr, .app-item, [class*="list"], [class*="rank"]')
            logger.info(f"找到 {len(list_items)} 个列表项")
            
            # 查找新上架/下架标签
            new_apps_text = await page.query_selector('text=新上架')
            offline_apps_text = await page.query_selector('text=下架')
            logger.info(f"新上架标签：{'✅ 找到' if new_apps_text else '❌ 未找到'}")
            logger.info(f"下架标签：{'✅ 找到' if offline_apps_text else '❌ 未找到'}")
            
            # Step 8: 尝试点击不同渠道
            logger.info("\n📊 请手动操作:")
            logger.info("1. 选择'华为'渠道")
            logger.info("2. 点击'新上架'或'下架'标签")
            logger.info("3. 观察页面 URL 和网络请求")
            logger.info("4. 按回车继续分析...")
            input("按回车继续...")
            
            # Step 9: 获取当前 URL
            current_url = page.url
            logger.info(f"当前 URL: {current_url}")
            
            # Step 10: 监听网络请求
            logger.info("\n📡 开始监听网络请求（10 秒）...")
            requests = []
            
            def handle_request(request):
                url = request.url
                if 'api' in url.lower() or 'rank' in url.lower() or 'new' in url.lower():
                    requests.append({
                        'url': url,
                        'method': request.method,
                    })
                    logger.info(f"📡 捕获请求：{request.method} {url}")
            
            page.on('request', handle_request)
            
            # 等待 10 秒
            await asyncio.sleep(10)
            
            logger.info(f"\n✅ 共捕获 {len(requests)} 个相关请求")
            
            # Step 11: 保存请求列表
            if requests:
                import json
                requests_path = Path(__file__).parent.parent / "debug_requests.json"
                with open(requests_path, 'w', encoding='utf-8') as f:
                    json.dump(requests, f, indent=2, ensure_ascii=False)
                logger.info(f"✅ 请求列表已保存：{requests_path}")
            
            logger.info("\n✅ 调试完成！请查看保存的文件:")
            logger.info(f"  - 截图：{screenshot_path}")
            logger.info(f"  - HTML: {html_path}")
            logger.info(f"  - 请求：{requests_path}")
            
        except Exception as e:
            logger.error(f"❌ 调试异常：{e}")
            import traceback
            traceback.print_exc()
        
        finally:
            logger.info("\n📝 请在浏览器中手动操作，观察网络请求，找到正确的 API 端点")
            logger.info("按 Ctrl+C 关闭浏览器...")


if __name__ == "__main__":
    asyncio.run(debug_diandian_android())
