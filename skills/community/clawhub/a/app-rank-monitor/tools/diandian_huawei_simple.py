#!/usr/bin/env python3
"""
点点数据华为渠道导出 - 简单调试版
一步一步执行，每步都截图确认
"""

import asyncio
import yaml
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

SKILL_DIR = Path(__file__).parent.parent
CONFIG_DIR = SKILL_DIR / "config"
REPORTS_DIR = SKILL_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

def load_credentials():
    config_path = CONFIG_DIR / "credentials.yaml"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            return config.get('diandian', {})
    return {}

async def main():
    print("=" * 60)
    print("📊 点点数据华为渠道导出 - 简单调试版")
    print("=" * 60)
    
    credentials = load_credentials()
    username = credentials.get('username', '')
    password = credentials.get('password', '')
    
    if not username or not password:
        print("❌ 请在 config/credentials.yaml 中配置账号密码")
        return
    
    print(f"📖 账号：{username}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            channel='chrome',
            headless=False,
            args=['--window-size=1920,1080']
        )
        
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        # Step 1: 访问官网
        print("\n1️⃣ 访问官网...")
        try:
            await page.goto('https://app.diandian.com/', wait_until='domcontentloaded', timeout=30000)
            await asyncio.sleep(3)
            print("✅ 页面已加载")
        except Exception as e:
            print(f"⚠️ 加载超时：{e}")
        
        # 截图
        ss1 = REPORTS_DIR / f"step1_home_{datetime.now().strftime('%H%M%S')}.png"
        await page.screenshot(path=ss1, full_page=True)
        print(f"📸 截图：{ss1.name}")
        
        # Step 2: 检查登录状态
        print("\n2️⃣ 检查登录状态...")
        try:
            login_btn = page.locator('.login-title').filter(has_text='登录/注册').first
            if await login_btn.count() > 0:
                print("⚠️ 未登录，开始登录...")
                
                # 点击登录
                await login_btn.click()
                await asyncio.sleep(3)
                print("✅ 已点击登录")
                
                # 截图
                ss2 = REPORTS_DIR / f"step2_login_{datetime.now().strftime('%H%M%S')}.png"
                await page.screenshot(path=ss2, full_page=True)
                print(f"📸 截图：{ss2.name}")
                
                # 点击邮箱
                print("\n3️⃣ 点击邮箱...")
                email_btn = page.locator('text=邮箱').first
                await email_btn.click()
                await asyncio.sleep(2)
                print("✅ 已点击邮箱")
                
                # 输入账号密码
                print("\n4️⃣ 输入账号密码...")
                email_input = page.locator('input[placeholder*="邮箱"]').first
                await email_input.fill(username)
                
                pwd_input = page.locator('input[type="password"]').first
                await pwd_input.fill(password)
                print("✅ 已输入账号密码")
                
                # 点击登录
                print("\n5️⃣ 点击登录按钮...")
                submit_btn = page.locator('button:has-text("登录")').first
                await submit_btn.click()
                await asyncio.sleep(5)
                print("✅ 已点击登录")
                
                # 截图
                ss3 = REPORTS_DIR / f"step3_logged_{datetime.now().strftime('%H%M%S')}.png"
                await page.screenshot(path=ss3, full_page=True)
                print(f"📸 截图：{ss3.name}")
            else:
                print("✅ 已登录")
        except Exception as e:
            print(f"❌ 登录失败：{e}")
        
        # Step 3: 点击上/下架监控
        print("\n6️⃣ 点击'上/下架监控'...")
        try:
            monitor_btn = page.locator('text=上/下架监控').first
            await monitor_btn.click()
            await asyncio.sleep(5)
            print("✅ 已点击上/下架监控")
            
            # 截图
            ss4 = REPORTS_DIR / f"step4_monitor_{datetime.now().strftime('%H%M%S')}.png"
            await page.screenshot(path=ss4, full_page=True)
            print(f"📸 截图：{ss4.name}")
            print(f"📍 当前 URL: {page.url}")
        except Exception as e:
            print(f"❌ 点击失败：{e}")
        
        # Step 4: 选择华为
        print("\n7️⃣ 选择华为渠道...")
        try:
            # 先点击商店选择器
            store_btn = page.locator('text=App Store').first
            await store_btn.click()
            await asyncio.sleep(1)
            
            # 选择华为
            huawei = page.locator('text=华为').first
            await huawei.click()
            await asyncio.sleep(3)
            print("✅ 已选择华为")
            
            # 截图
            ss5 = REPORTS_DIR / f"step5_huawei_{datetime.now().strftime('%H%M%S')}.png"
            await page.screenshot(path=ss5, full_page=True)
            print(f"📸 截图：{ss5.name}")
        except Exception as e:
            print(f"❌ 选择失败：{e}")
        
        # Step 5: 导出
        print("\n8️⃣ 点击'导出数据'...")
        try:
            export_btn = page.locator('text=导出数据').first
            await export_btn.click()
            await asyncio.sleep(3)
            print("✅ 已点击导出")
            
            # 截图
            ss6 = REPORTS_DIR / f"step6_export_{datetime.now().strftime('%H%M%S')}.png"
            await page.screenshot(path=ss6, full_page=True)
            print(f"📸 截图：{ss6.name}")
        except Exception as e:
            print(f"❌ 导出失败：{e}")
        
        print("\n" + "=" * 60)
        print("✅ 执行完成！请查看截图确认流程")
        print("=" * 60)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
