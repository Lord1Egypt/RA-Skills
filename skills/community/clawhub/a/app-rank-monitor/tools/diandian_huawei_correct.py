#!/usr/bin/env python3
"""
点点数据华为渠道导出 - 正确流程版
根据用户提供的截图修正流程
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
    print("📊 点点数据华为渠道导出 - 正确流程版")
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
        
        # ========== Step 1: 访问并登录 ==========
        print("\n1️⃣ 访问点点数据官网...")
        await page.goto('https://app.diandian.com/', wait_until='domcontentloaded', timeout=30000)
        await asyncio.sleep(3)
        print("✅ 页面已加载")
        
        # 检查是否需要登录
        try:
            login_btn = page.locator('.login-title').filter(has_text='登录/注册').first
            if await login_btn.count() > 0:
                print("⚠️ 未登录，开始登录...")
                await login_btn.click()
                await asyncio.sleep(3)
                
                # 点击邮箱
                email_btn = page.locator('text=邮箱').first
                await email_btn.click()
                await asyncio.sleep(2)
                
                # 输入账号密码
                email_input = page.locator('input[placeholder*="邮箱"]').first
                await email_input.fill(username)
                
                pwd_input = page.locator('input[type="password"]').first
                await pwd_input.fill(password)
                
                # 点击登录
                submit_btn = page.locator('button:has-text("登录")').first
                await submit_btn.click()
                await asyncio.sleep(5)
                print("✅ 登录成功")
            else:
                print("✅ 已登录")
        except Exception as e:
            print(f"⚠️ 登录检查失败：{e}")
        
        # 截图
        ss1 = REPORTS_DIR / f"correct_step1_{datetime.now().strftime('%H%M%S')}.png"
        await page.screenshot(path=ss1, full_page=True)
        print(f"📸 截图：{ss1.name}")
        
        # ========== Step 2: 点击"市场情报" ==========
        print("\n2️⃣ 点击顶部'市场情报'...")
        try:
            market_btn = page.locator('text=市场情报').first
            await market_btn.click()
            print("✅ 已点击市场情报")
            await asyncio.sleep(2)
            
            # 截图 - 应该看到"市场趋势"弹窗
            ss2 = REPORTS_DIR / f"correct_step2_popup_{datetime.now().strftime('%H%M%S')}.png"
            await page.screenshot(path=ss2, full_page=True)
            print(f"📸 截图：{ss2.name}（市场趋势弹窗）")
        except Exception as e:
            print(f"❌ 点击市场情报失败：{e}")
            await browser.close()
            return
        
        # ========== Step 3: 点击"上架监控" ==========
        print("\n3️⃣ 在弹窗中点击'上架监控'...")
        try:
            # 等待弹窗出现
            await page.wait_for_selector('text=上架监控', timeout=10000)
            await asyncio.sleep(1)
            
            # 点击上架监控卡片
            monitor_btn = page.locator('text=上架监控').first
            await monitor_btn.click()
            print("✅ 已点击上架监控")
            await asyncio.sleep(5)
            
            # 截图
            ss3 = REPORTS_DIR / f"correct_step3_monitor_{datetime.now().strftime('%H%M%S')}.png"
            await page.screenshot(path=ss3, full_page=True)
            print(f"📸 截图：{ss3.name}")
            print(f"📍 当前 URL: {page.url}")
        except Exception as e:
            print(f"❌ 点击上架监控失败：{e}")
            await browser.close()
            return
        
        # ========== Step 4: 选择华为渠道 ==========
        print("\n4️⃣ 选择华为渠道...")
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
            ss4 = REPORTS_DIR / f"correct_step4_huawei_{datetime.now().strftime('%H%M%S')}.png"
            await page.screenshot(path=ss4, full_page=True)
            print(f"📸 截图：{ss4.name}")
        except Exception as e:
            print(f"❌ 选择华为失败：{e}")
        
        # ========== Step 5: 导出数据 ==========
        print("\n5️⃣ 点击'导出数据'...")
        try:
            export_btn = page.locator('text=导出数据').first
            await export_btn.click()
            print("✅ 已点击导出数据")
            await asyncio.sleep(3)
            
            # 截图
            ss5 = REPORTS_DIR / f"correct_step5_export_{datetime.now().strftime('%H%M%S')}.png"
            await page.screenshot(path=ss5, full_page=True)
            print(f"📸 截图：{ss5.name}")
        except Exception as e:
            print(f"❌ 导出失败：{e}")
        
        print("\n" + "=" * 60)
        print("✅ 执行完成！请查看截图确认")
        print("=" * 60)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
