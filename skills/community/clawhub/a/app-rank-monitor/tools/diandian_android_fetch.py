#!/usr/bin/env python3
"""
点点数据安卓渠道榜单爬虫
基于 diandian_auto_login_v2.py 修改
支持渠道：华为、小米、应用宝、OPPO、vivo、百度、360、豌豆荚
"""

import asyncio
import sys
import yaml
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from playwright.async_api import async_playwright
from rankers.base import NewApp, OfflineApp

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('DiandianAndroidFetch')


def load_credentials() -> dict:
    """加载账号凭证"""
    cred_path = Path(__file__).parent.parent / "config" / "credentials.yaml"
    if not cred_path.exists():
        raise FileNotFoundError(f"凭证文件不存在：{cred_path}")
    
    with open(cred_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


async def navigate_to_market_intel(page):
    """导航到市场情报页面并获取应用列表"""
    try:
        # Step 1: 点击"市场情报"
        logger.info("📖 点击'市场情报'...")
        market_intel_btn = await page.query_selector('text=市场情报')
        if market_intel_btn:
            await market_intel_btn.click()
            await asyncio.sleep(3)
            logger.info("✅ 已点击'市场情报'")
        else:
            logger.error("❌ 未找到'市场情报'按钮")
            return
        
        # Step 2: 点击"上架监控"
        logger.info("📖 点击'上架监控'...")
        new_apps_btn = await page.query_selector('text=上架监控')
        if new_apps_btn:
            await new_apps_btn.click()
            await asyncio.sleep(5)
            logger.info("✅ 已点击'上架监控'")
            
            # 截图并获取上架应用列表
            try:
                screenshot_path = Path(__file__).parent.parent / "debug_step_new_apps.png"
                await page.screenshot(path=str(screenshot_path), timeout=10000)
                logger.info(f"📸 已保存截图：{screenshot_path}")
            except Exception as e:
                logger.warning(f"⚠️ 截图失败：{e}")
            
            # 获取上架应用数据
            new_apps_list = await extract_app_list(page)
            logger.info(f"📊 获取到 {len(new_apps_list)} 个上架应用")
            
            # 保存上架应用列表
            if new_apps_list:
                save_app_list(new_apps_list, "diandian_new_apps")
        else:
            logger.warning("⚠️ 未找到'上架监控'按钮")
        
        # Step 3: 点击"下架监控"
        logger.info("📖 点击'下架监控'...")
        offline_apps_btn = await page.query_selector('text=下架监控')
        if offline_apps_btn:
            await offline_apps_btn.click()
            await asyncio.sleep(5)
            logger.info("✅ 已点击'下架监控'")
            
            # 截图并获取下架应用列表
            try:
                screenshot_path = Path(__file__).parent.parent / "debug_step_offline_apps.png"
                await page.screenshot(path=str(screenshot_path), timeout=10000)
                logger.info(f"📸 已保存截图：{screenshot_path}")
            except Exception as e:
                logger.warning(f"⚠️ 截图失败：{e}")
            
            # 获取下架应用数据
            offline_apps_list = await extract_app_list(page)
            logger.info(f"📊 获取到 {len(offline_apps_list)} 个下架应用")
            
            # 保存下架应用列表
            if offline_apps_list:
                save_app_list(offline_apps_list, "diandian_offline_apps")
        else:
            logger.warning("⚠️ 未找到'下架监控'按钮")
            
    except Exception as e:
        logger.error(f"❌ 市场情报导航失败：{e}")


def save_diandian_token(cookie_string: str):
    """保存点点 Cookie 字符串到配置文件"""
    config_path = Path(__file__).parent.parent / "config" / "diandian.yaml"
    config = {}
    
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}
    
    config['token'] = cookie_string
    config['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M PST')
    config['auto_updated'] = True
    
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False, width=1000)
    
    logger.info("✅ 点点 Cookie 已保存")


async def login_and_get_token(username: str, password: str, headless: bool = True) -> bool:
    """使用 Playwright 自动登录点点数据并获取 Token"""
    logger.info(f"🚀 开始自动登录点点数据：{username}")
    
    async with async_playwright() as p:
        # 启动浏览器（使用正式版 Chrome）
        user_data_dir = Path(__file__).parent.parent / ".browser_data" / "diandian"
        user_data_dir.mkdir(parents=True, exist_ok=True)
        
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=headless,
            channel='chrome',  # 使用正式版 Chrome，避免测试版
            args=['--disable-blink-features=AutomationControlled', '--no-sandbox']
        )
        
        page = browser.pages[0] if browser.pages else await browser.new_page()
        
        # 防检测
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        try:
            # Step 1: 访问主页并点击右上角"登录/注册"
            logger.info("📖 Step 1: 访问点点数据主页...")
            await page.goto("https://app.diandian.com/", wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(3)
            
            # 检查是否已登录
            page_content = await page.content()
            is_logged = '退出' in page_content or '账号设置' in page_content
            
            if is_logged:
                logger.info("✅ 已登录，继续执行市场情报...")
                # 直接跳到市场情报步骤
                await navigate_to_market_intel(page)
                # 获取 Cookie
                return await get_token(page)
            else:
                logger.info("⚠️ 未登录，开始登录流程...")
                # 继续执行登录步骤
                pass
            
            # Step 2: 点击右上角的"登录/注册"按钮（仅未登录时执行）
            logger.info("📖 Step 2: 点击右上角的'登录/注册'...")
            
            # 截图
            screenshot_path = Path(__file__).parent.parent / "debug_step1_homepage.png"
            await page.screenshot(path=str(screenshot_path))
            logger.info(f"📸 已保存截图：{screenshot_path}")
            
            # 查找右上角的登录/注册按钮
            login_btn = await page.query_selector('text=登录/注册')
            if login_btn:
                await login_btn.click()
                await asyncio.sleep(3)
                logger.info("✅ 已点击登录/注册按钮")
            else:
                logger.error("❌ 未找到登录/注册按钮")
                return False
            
            # Step 3: 跳转到登录页后，点击右下角的"邮箱"
            logger.info("📖 Step 3: 点击右下角的'邮箱'选项...")
            
            # 截图查看登录弹窗
            screenshot_path = Path(__file__).parent.parent / "debug_step2_modal.png"
            await page.screenshot(path=str(screenshot_path))
            logger.info(f"📸 已保存截图：{screenshot_path}")
            
            # 等待页面跳转（可能会跳转到 /login 页面）
            try:
                await page.wait_for_url("https://app.diandian.com/login", timeout=5000)
                logger.info("✅ 已跳转到登录页面")
            except:
                logger.info("⏳ 未跳转，可能在弹窗中")
            
            # 点击"邮箱"选项（在"其他登录/注册方式"下方）
            email_selectors = [
                'text=邮箱',
                'div:has-text("邮箱")',
                'span:has-text("邮箱")',
                '[class*="email"]',
            ]
            
            clicked = False
            for selector in email_selectors:
                try:
                    email_els = await page.query_selector_all(selector)
                    for el in email_els:
                        el_text = await el.inner_text()
                        # 排除"Google 邮箱"
                        if '邮箱' in el_text and 'Google' not in el_text:
                            logger.info(f"✅ 点击邮箱选项：{el_text}")
                            await el.click()
                            clicked = True
                            break
                    if clicked:
                        break
                except Exception as e:
                    logger.debug(f"选择器 {selector} 失败：{e}")
            
            if not clicked:
                logger.warning("⚠️ 未找到邮箱选项，尝试使用 JavaScript 点击...")
                await page.evaluate("""
                    () => {
                        const elements = document.querySelectorAll('*');
                        for (const el of elements) {
                            const text = el.textContent;
                            if (text && text.includes('邮箱') && !text.includes('Google') && !text.includes('短信')) {
                                el.click();
                                return true;
                            }
                        }
                        return false;
                    }
                """)
            
            await asyncio.sleep(3)
            
            # 截图查看邮箱登录表单
            screenshot_path = Path(__file__).parent.parent / "debug_step3_email_form.png"
            await page.screenshot(path=str(screenshot_path))
            logger.info(f"📸 已保存截图：{screenshot_path}")
            
            # Step 4: 输入账号密码
            logger.info("📖 Step 4: 输入账号密码...")
            
            # 根据截图，输入框的 placeholder 是"请输入邮箱"和"请输入密码"
            username_input = await page.query_selector('input[placeholder="请输入邮箱"]')
            password_input = await page.query_selector('input[placeholder="请输入密码"]')
            
            # 降级方案：查找所有 input
            if not username_input or not password_input:
                all_inputs = await page.query_selector_all('input')
                for input_el in all_inputs:
                    input_type = await input_el.get_attribute('type')
                    if input_type == 'text' and not username_input:
                        username_input = input_el
                    elif input_type == 'password':
                        password_input = input_el
            
            if not username_input or not password_input:
                logger.error("❌ 未找到输入框")
                # 截图调试
                screenshot_path = Path(__file__).parent.parent / "debug_step4_no_inputs.png"
                await page.screenshot(path=str(screenshot_path))
                logger.info(f"📸 已保存截图：{screenshot_path}")
                return False
            
            logger.info(f"✅ 找到输入框，准备输入账号密码...")
            await username_input.fill(username)
            await asyncio.sleep(0.5)
            await password_input.fill(password)
            await asyncio.sleep(0.5)
            
            # Step 5: 点击登录按钮
            logger.info("📖 Step 5: 点击登录按钮...")
            
            # 根据截图，登录按钮是蓝色的，文本是"登录"
            submit_btn = await page.query_selector('button:has-text("登录")')
            
            if submit_btn:
                logger.info("✅ 找到登录按钮，点击登录...")
                await submit_btn.click()
            else:
                logger.warning("⚠️ 未找到登录按钮，尝试按回车...")
                await password_input.press('Enter')
            
            await asyncio.sleep(5)
            
            # 截图查看登录结果（带超时保护）
            try:
                screenshot_path = Path(__file__).parent.parent / "debug_step5_after_login.png"
                await page.screenshot(path=str(screenshot_path), timeout=10000)
                logger.info(f"📸 已保存截图：{screenshot_path}")
            except Exception as e:
                logger.warning(f"⚠️ 截图失败：{e}")
            
            # Step 6: 点击"市场情报"
            logger.info("📖 Step 6: 点击'市场情报'...")
            
            market_intel_btn = await page.query_selector('text=市场情报')
            if market_intel_btn:
                await market_intel_btn.click()
                await asyncio.sleep(3)
                logger.info("✅ 已点击'市场情报'")
            else:
                logger.error("❌ 未找到'市场情报'按钮")
                return await get_token(page)  # 至少获取 Token
            
            # Step 7: 点击"上架监控"
            logger.info("📖 Step 7: 点击'上架监控'...")
            
            new_apps_btn = await page.query_selector('text=上架监控')
            if new_apps_btn:
                await new_apps_btn.click()
                await asyncio.sleep(5)
                logger.info("✅ 已点击'上架监控'")
                
                # 截图并获取上架应用列表（带超时保护）
                try:
                    screenshot_path = Path(__file__).parent.parent / "debug_step7_new_apps.png"
                    await page.screenshot(path=str(screenshot_path), timeout=10000)
                    logger.info(f"📸 已保存截图：{screenshot_path}")
                except Exception as e:
                    logger.warning(f"⚠️ 截图失败：{e}")
                
                # 获取上架应用数据
                new_apps_list = await extract_app_list(page)
                logger.info(f"📊 获取到 {len(new_apps_list)} 个上架应用")
                
                # 保存上架应用列表
                if new_apps_list:
                    save_app_list(new_apps_list, "diandian_new_apps")
            else:
                logger.warning("⚠️ 未找到'上架监控'按钮")
            
            # Step 8: 点击"下架监控"
            logger.info("📖 Step 8: 点击'下架监控'...")
            
            offline_apps_btn = await page.query_selector('text=下架监控')
            if offline_apps_btn:
                await offline_apps_btn.click()
                await asyncio.sleep(5)
                logger.info("✅ 已点击'下架监控'")
                
                # 截图并获取下架应用列表（带超时保护）
                try:
                    screenshot_path = Path(__file__).parent.parent / "debug_step8_offline_apps.png"
                    await page.screenshot(path=str(screenshot_path), timeout=10000)
                    logger.info(f"📸 已保存截图：{screenshot_path}")
                except Exception as e:
                    logger.warning(f"⚠️ 截图失败：{e}")
                
                # 获取下架应用数据
                offline_apps_list = await extract_app_list(page)
                logger.info(f"📊 获取到 {len(offline_apps_list)} 个下架应用")
                
                # 保存下架应用列表
                if offline_apps_list:
                    save_app_list(offline_apps_list, "diandian_offline_apps")
            else:
                logger.warning("⚠️ 未找到'下架监控'按钮")
            
            # Step 9: 获取 Token
            return await get_token(page)
            
        except Exception as e:
            logger.error(f"❌ 登录异常：{e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            await browser.close()


async def extract_app_list(page) -> list:
    """从页面提取应用列表"""
    try:
        # 尝试从页面元素中提取应用信息
        apps = await page.evaluate("""
            () => {
                const apps = [];
                // 查找应用列表项（根据实际页面结构调整选择器）
                const items = document.querySelectorAll('[class*="app"], [class*="list"], tr, .rank-item');
                
                for (const item of items) {
                    const text = item.textContent.trim();
                    if (text && text.length > 5 && text.length < 200) {
                        // 尝试提取应用名和开发者
                        const lines = text.split('\\n').map(l => l.trim()).filter(l => l);
                        if (lines.length >= 1) {
                            apps.push({
                                name: lines[0],
                                developer: lines[1] || '',
                                date: lines[2] || ''
                            });
                        }
                    }
                }
                
                return apps.slice(0, 100);
            }
        """)
        
        return apps
    except Exception as e:
        logger.debug(f"提取应用列表失败：{e}")
        return []


def save_app_list(apps: list, prefix: str = "diandian"):
    """保存应用列表到文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(__file__).parent.parent / "reports" / f"{prefix}_{timestamp}.txt"
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# 点点数据 - {prefix} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for i, app in enumerate(apps, 1):
            name = app.get('name', 'Unknown')
            developer = app.get('developer', '')
            date = app.get('date', '')
            f.write(f"{i}. {name}")
            if developer:
                f.write(f" ({developer})")
            if date:
                f.write(f" [{date}]")
            f.write("\n")
    
    logger.info(f"📄 应用列表已保存：{output_path}")


async def get_token(page) -> bool:
    """从页面获取 Token 并保存"""
    logger.info("📖 获取 Token...")
    await asyncio.sleep(2)
    
    # 获取完整 Cookie 字符串
    cookie_string = await page.evaluate("() => document.cookie")
    logger.info(f"完整 Cookie 字符串长度：{len(cookie_string)}")
    
    # 检查是否包含 token
    has_token = 'token=' in cookie_string.lower()
    logger.info(f"Cookie 包含 'token=': {has_token}")
    
    if has_token:
        logger.info(f"✅ 获取到完整 Cookie 字符串")
        save_diandian_token(cookie_string)
        return True
    
    logger.error("❌ 未找到 token")
    return False


async def main():
    """主函数"""
    try:
        creds = load_credentials()
        diandian = creds.get('diandian', {})
        username = diandian.get('username', '')
        password = diandian.get('password', '')
        
        if not username or not password:
            logger.error("❌ 点点账号密码未配置")
            return 1
        
        # 无头模式设为 True，不显示浏览器窗口
        success = await login_and_get_token(username, password, headless=True)
        
        if success:
            logger.info("✅ 点点数据登录成功")
            return 0
        else:
            logger.error("❌ 点点数据登录失败")
            return 1
    
    except Exception as e:
        logger.error(f"❌ 异常：{e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(asyncio.run(main()))
