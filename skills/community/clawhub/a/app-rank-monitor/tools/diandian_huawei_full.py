#!/usr/bin/env python3
"""
点点数据华为渠道导出 - 完整版
登录 → 市场情报 → 上架监控 → 华为 → 导出
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
    print("📊 点点数据华为渠道导出 - 完整版")
    print("=" * 60)
    
    credentials = load_credentials()
    username = credentials.get('username', '')
    password = credentials.get('password', '')
    
    if not username or not password:
        print("❌ 请在 config/credentials.yaml 中配置账号密码")
        return
    
    print(f"📖 账号：{username}")
    
    async with async_playwright() as p:
        # 使用持久化上下文（保持登录状态）
        user_data_dir = SKILL_DIR / ".browser_data" / "diandian"
        user_data_dir.mkdir(parents=True, exist_ok=True)
        
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=False,
            channel='chrome',
            args=['--disable-blink-features=AutomationControlled', '--no-sandbox', '--window-size=1920,1080']
        )
        
        page = browser.pages[0] if browser.pages else await browser.new_page()
        
        # ========== Step 1: 访问并登录 ==========
        print("\n1️⃣ 访问点点数据官网...")
        await page.goto('https://app.diandian.com/', wait_until='domcontentloaded', timeout=60000)
        await asyncio.sleep(3)
        
        # 检查登录状态
        content = await page.content()
        if '退出' not in content and '账号设置' not in content:
            print("⚠️ 未登录，开始登录...")
            try:
                login_btn = page.locator('.login-title').filter(has_text='登录/注册').first
                await login_btn.click()
                await asyncio.sleep(3)
                
                email_btn = page.locator('text=邮箱').first
                await email_btn.click()
                await asyncio.sleep(2)
                
                email_input = page.locator('input[placeholder*="邮箱"]').first
                await email_input.fill(username)
                
                pwd_input = page.locator('input[type="password"]').first
                await pwd_input.fill(password)
                
                submit_btn = page.locator('button:has-text("登录")').first
                await submit_btn.click()
                await asyncio.sleep(5)
                print("✅ 登录成功")
            except Exception as e:
                print(f"❌ 登录失败：{e}")
                await browser.close()
                return
        else:
            print("✅ 已登录")
        
        # 截图
        ss1 = REPORTS_DIR / f"full_step1_{datetime.now().strftime('%H%M%S')}.png"
        await page.screenshot(path=ss1, full_page=True)
        print(f"📸 截图：{ss1.name}")
        
        # ========== Step 2: 点击"市场情报" ==========
        print("\n2️⃣ 点击顶部'市场情报'...")
        try:
            market_btn = page.locator('text=市场情报').first
            await market_btn.click()
            print("✅ 已点击市场情报")
            await asyncio.sleep(3)
            
            # 截图 - 弹窗
            ss2 = REPORTS_DIR / f"full_step2_popup_{datetime.now().strftime('%H%M%S')}.png"
            await page.screenshot(path=ss2, full_page=True)
            print(f"📸 截图：{ss2.name}（市场趋势弹窗）")
        except Exception as e:
            print(f"❌ 点击市场情报失败：{e}")
            await browser.close()
            return
        
        # ========== Step 3: 点击"上架监控" ==========
        print("\n3️⃣ 在弹窗中点击'上架监控'...")
        try:
            await page.wait_for_selector('text=上架监控', timeout=10000)
            await asyncio.sleep(1)
            
            monitor_btn = page.locator('text=上架监控').first
            await monitor_btn.click()
            print("✅ 已点击上架监控")
            await asyncio.sleep(5)
            
            # 截图
            ss3 = REPORTS_DIR / f"full_step3_monitor_{datetime.now().strftime('%H%M%S')}.png"
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
            store_btn = page.locator('text=App Store').first
            await store_btn.click()
            await asyncio.sleep(1)
            
            huawei = page.locator('text=华为').first
            await huawei.click()
            await asyncio.sleep(3)
            print("✅ 已选择华为")
            
            # 截图
            ss4 = REPORTS_DIR / f"full_step4_huawei_{datetime.now().strftime('%H%M%S')}.png"
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
            ss5 = REPORTS_DIR / f"full_step5_export_{datetime.now().strftime('%H%M%S')}.png"
            await page.screenshot(path=ss5, full_page=True)
            print(f"📸 截图：{ss5.name}")
        except Exception as e:
            print(f"❌ 导出失败：{e}")
        
        print("\n" + "=" * 60)
        print("✅ 执行完成！请查看截图")
        print("=" * 60)
        print("\n📂 截图位置:")
        print(f"  {ss1.name}")
        print(f"  {ss2.name}")
        print(f"  {ss3.name}")
        print(f"  {ss4.name}")
        print(f"  {ss5.name}")
        
        # 保持浏览器打开，让用户查看
        print("\n⏸️  浏览器保持打开，按 Ctrl+C 关闭...")
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n✅ 正在关闭浏览器...")
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
