#!/usr/bin/env python3
"""
点点数据华为渠道上架监控导出工具
正确流程：登录 → 上/下架监控 → 选择华为 → 导出数据 → 下载文件
"""

import asyncio
import yaml
import time
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

# 配置路径
SKILL_DIR = Path(__file__).parent.parent
CONFIG_DIR = SKILL_DIR / "config"
REPORTS_DIR = SKILL_DIR / "reports"

# 确保目录存在
REPORTS_DIR.mkdir(exist_ok=True)


def load_credentials():
    """加载账号密码配置"""
    config_path = CONFIG_DIR / "credentials.yaml"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            return config.get('diandian', {})
    return {}


def save_cookie(token: str):
    """保存 Cookie 到配置文件"""
    config_path = CONFIG_DIR / "diandian.yaml"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}
    else:
        config = {}
    
    config['token'] = token
    config['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M PST')
    config['auto_updated'] = True
    
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
    
    print(f"✅ Cookie 已保存到 {config_path}")


async def main():
    """主流程"""
    print("=" * 60)
    print("📊 点点数据华为渠道上架监控导出工具")
    print("=" * 60)
    
    # 加载配置
    credentials = load_credentials()
    username = credentials.get('username', '')
    password = credentials.get('password', '')
    
    if not username or not password:
        print("❌ 错误：请在 config/credentials.yaml 中配置点点数据的账号和密码")
        return
    
    print(f"📖 使用账号：{username}")
    
    async with async_playwright() as p:
        # 启动浏览器（使用正式版 Chrome）
        browser = await p.chromium.launch(
            channel='chrome',
            headless=False,  # 显示浏览器窗口，方便调试
            args=['--window-size=1920,1080']
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        page = await context.new_page()
        
        # ========== Step 1: 访问官网并登录 ==========
        print("\n📖 Step 1: 访问点点数据官网...")
        try:
            await page.goto('https://app.diandian.com/', wait_until='domcontentloaded', timeout=30000)
        except:
            # 如果超时，可能是已登录在重定向，继续执行
            print("⚠️ 页面加载超时，可能是已登录状态，继续执行...")
        await asyncio.sleep(3)
        
        # 检查是否需要登录
        need_login = False
        login_btn = None
        try:
            # 优先查找右上角的登录按钮（更精确的选择器）
            login_btn = page.locator('.login-title').filter(has_text='登录/注册').first
            if await login_btn.count() > 0:
                need_login = True
                print("⚠️ 检测到未登录，开始登录流程...")
        except:
            pass
        
        if need_login and login_btn:
            # 点击登录/注册按钮
            print("📖 Step 2: 点击右上角'登录/注册'按钮...")
            await login_btn.click()
            await asyncio.sleep(3)
            
            # 截图查看当前状态
            debug_login = REPORTS_DIR / "debug_login_dialog.png"
            await page.screenshot(path=debug_login, full_page=True)
            print(f"📸 已保存登录弹窗截图：{debug_login}")
            
            # 点击邮箱按钮
            print("📖 Step 3: 点击'邮箱'按钮...")
            try:
                # 等待邮箱按钮出现
                await page.wait_for_selector('text=邮箱', timeout=5000)
                email_btn = page.locator('text=邮箱').first
                await email_btn.click()
                print("✅ 已点击邮箱按钮")
                await asyncio.sleep(2)
            except Exception as e:
                print(f"⚠️ 点击邮箱按钮失败：{e}")
                await browser.close()
                return
            
            # 输入账号密码
            print("📖 Step 4: 输入账号和密码...")
            try:
                # 等待输入框出现
                await page.wait_for_selector('input[placeholder*="邮箱"], input[type="text"]', timeout=5000)
                await asyncio.sleep(1)
                
                # 查找邮箱输入框
                email_input = page.locator('input[placeholder*="邮箱"]').first
                await email_input.fill(username)
                await asyncio.sleep(0.5)
                
                # 查找密码框
                password_input = page.locator('input[type="password"]').first
                await password_input.fill(password)
                await asyncio.sleep(0.5)
                
                print("✅ 账号密码已填入")
            except Exception as e:
                print(f"❌ 填入账号密码失败：{e}")
                await browser.close()
                return
            
            # 点击登录按钮
            print("📖 Step 5: 点击'登录'按钮...")
            try:
                submit_btn = page.locator('button:has-text("登录")').first
                await submit_btn.click()
                print("✅ 已点击登录按钮")
                await asyncio.sleep(5)
                
                # 等待页面加载（可能跳转回主页）
                await page.wait_for_load_state('networkidle')
                print("✅ 登录完成，页面已加载")
            except Exception as e:
                print(f"⚠️ 登录按钮点击失败：{e}")
        
        # 获取并保存 Cookie
        print("📖 Step 7: 获取 Cookie...")
        cookies = await context.cookies()
        cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
        save_cookie(cookie_str)
        print(f"✅ Cookie 长度：{len(cookie_str)}")
        
        # ========== Step 2: 点击上/下架监控 ==========
        print("\n📖 Step 2: 点击顶部'上/下架监控'按钮...")
        await asyncio.sleep(2)
        
        try:
            # 查找上/下架监控按钮
            monitor_btn = page.locator('text=上/下架监控').first
            await monitor_btn.click()
            print("✅ 已点击上/下架监控")
            
            # 等待页面加载（不等待特定 URL）
            await page.wait_for_load_state('networkidle', timeout=15000)
            print(f"✅ 页面已加载：{page.url}")
            
            # 截图确认
            debug_monitor = REPORTS_DIR / "debug_monitor_page.png"
            await page.screenshot(path=debug_monitor, full_page=True)
            print(f"📸 已保存监控页面截图：{debug_monitor}")
        except Exception as e:
            print(f"⚠️ 等待页面加载超时，但继续执行：{e}")
        
        await asyncio.sleep(2)
        
        # ========== Step 3: 选择华为渠道 ==========
        print("\n📖 Step 3: 选择华为渠道...")
        
        try:
            # 点击商店选择框
            store_selector = page.locator('text=App Store').first
            await store_selector.click()
            await asyncio.sleep(1)
            
            # 选择华为
            huawei_option = page.locator('text=华为').first
            await huawei_option.click()
            print("✅ 已选择华为渠道")
        except Exception as e:
            print(f"⚠️ 选择华为渠道失败：{e}")
        
        await asyncio.sleep(2)
        
        # ========== Step 4: 导出数据 ==========
        print("\n📖 Step 4: 点击'导出数据'按钮...")
        
        try:
            # 配置下载路径
            download_path = REPORTS_DIR / "diandian_exports"
            download_path.mkdir(exist_ok=True)
            
            # 设置下载行为
            async with page.expect_download(timeout=30000) as download_info:
                # 点击导出按钮
                export_btn = page.locator('text=导出数据').first
                await export_btn.click()
                print("✅ 已点击导出数据")
                
                # 等待文件列表弹窗
                await asyncio.sleep(2)
                
                # 在弹窗中点击下载
                try:
                    download_link = page.locator('text=下载').first
                    await download_link.click()
                    print("✅ 已点击下载按钮")
                except Exception as e:
                    print(f"⚠️ 点击下载按钮失败：{e}")
                
                # 等待下载完成
                download = await download_info.value
                file_path = download_path / download.suggested_filename
                await download.save_as(file_path)
                print(f"✅ 文件已下载：{file_path}")
                print(f"📄 文件大小：{file_path.stat().st_size / 1024:.1f} KB")
                
        except Exception as e:
            print(f"❌ 导出或下载失败：{e}")
            # 截图保存当前状态
            screenshot_path = REPORTS_DIR / f"debug_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 已保存截图：{screenshot_path}")
        
        await asyncio.sleep(2)
        
        # ========== 完成 ==========
        print("\n" + "=" * 60)
        print("✅ 华为渠道上架监控数据导出完成！")
        print("=" * 60)
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
