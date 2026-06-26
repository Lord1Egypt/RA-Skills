#!/usr/bin/env python3
"""
点点数据自动登录
- 检查 Cookie 是否有效
- 无效则自动登录并保存 Cookie
- 有效则直接使用
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
USER_DATA_DIR = SKILL_DIR / ".browser_data" / "diandian"
USER_DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_credentials():
    """加载账号密码"""
    config_path = CONFIG_DIR / "credentials.yaml"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            return config.get('diandian', {})
    return {}


def save_credentials(username, password):
    """保存账号密码"""
    config_path = CONFIG_DIR / "credentials.yaml"
    config = {}
    
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}
    
    if 'diandian' not in config:
        config['diandian'] = {}
    
    config['diandian']['username'] = username
    config['diandian']['password'] = password
    
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
    
    print(f"✅ 账号已保存到 {config_path}")


def load_cookie():
    """加载保存的 Cookie"""
    config_path = CONFIG_DIR / "diandian.yaml"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            return config.get('cookie', '')
    return ''


def save_cookie(cookie_string):
    """保存 Cookie"""
    config_path = CONFIG_DIR / "diandian.yaml"
    config = {}
    
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}
    
    # 提取 token
    token = ''
    for cookie in cookie_string.split('; '):
        if cookie.startswith('token='):
            token = cookie.split('=')[1]
            break
    
    config['cookie'] = cookie_string
    config['token'] = token
    config['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M PST')
    
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
    
    print(f"✅ Cookie 已保存到 {config_path}")
    if token:
        print(f"   Token: {token[:30]}...")


async def check_login_status(page):
    """检查登录状态"""
    content = await page.content()
    # 已登录的特征
    is_logged = (
        '退出' in content or 
        '账号设置' in content or 
        '市场情报' in content
    )
    # 未登录的特征
    has_login_btn = '登录/注册' in content
    
    return is_logged and not has_login_btn


async def auto_login(page, username, password):
    """自动登录"""
    print("\n📖 Step 1: 访问登录页...")
    # 已经连接了浏览器，当前页面可能已经打开
    current_url = page.url
    if '/login' not in current_url:
        await page.goto('https://app.diandian.com/login', wait_until='domcontentloaded', timeout=60000)
        await asyncio.sleep(3)
        try:
            await page.wait_for_load_state('networkidle', timeout=10000)
        except Exception:
            # 超时没关系，页面可能已经加载好了
            pass
    print("   ✅ 登录页已加载")
    
    print("\n📖 Step 2: 确认邮箱登录...")
    # 检查是否已经在邮箱登录 tab
    email_tab = page.locator('text=邮箱').first
    if await email_tab.count() > 0:
        # 如果已经有邮箱 tab，点击激活
        await email_tab.click()
        await asyncio.sleep(2)
        print("   ✅ 已切换到邮箱登录")
    else:
        print("   ⚠️ 未找到邮箱 tab，可能已经在邮箱登录模式")
    
    print("\n📖 Step 3: 输入账号密码...")
    # 等待输入框出现
    await asyncio.sleep(3)
    
    # 尝试多种选择器组合
    email_input = page.locator('input[placeholder="请输入邮箱"], input[placeholder*="邮箱"], input[type="email"]').first
    password_input = page.locator('input[placeholder="请输入密码"], input[placeholder*="密码"], input[type="password"]').first
    
    found = False
    if await email_input.count() > 0 and await password_input.count() > 0:
        await email_input.fill(username)
        print(f"   ✅ 账号已输入")
        await asyncio.sleep(0.5)
        await password_input.fill(password)
        print(f"   ✅ 密码已输入")
        await asyncio.sleep(0.5)
        found = True
    else:
        # 尝试按位置选择
        email_input = page.locator('input').nth(0)
        password_input = page.locator('input').nth(1)
        if await email_input.count() > 0 and await password_input.count() > 0:
            print(f"   💡 使用通用选择器找到输入框")
            await email_input.fill(username)
            print(f"   ✅ 账号已输入")
            await asyncio.sleep(0.5)
            await password_input.fill(password)
            print(f"   ✅ 密码已输入")
            await asyncio.sleep(0.5)
            found = True
        else:
            # 尝试在整个页面查找所有 input
            count = await page.locator('input').count()
            print(f"   🔍 页面找到 {count} 个 input 元素")
            if count >= 2:
                email_input = page.locator('input').nth(0)
                password_input = page.locator('input').nth(1)
                await email_input.fill(username)
                print(f"   ✅ 账号已输入（第 0 个 input）")
                await asyncio.sleep(0.5)
                await password_input.fill(password)
                print(f"   ✅ 密码已输入（第 1 个 input）")
                await asyncio.sleep(0.5)
                found = True
    
    if not found:
        print("   ❌ 未找到输入框")
        return False
    
    print("\n📖 Step 5: 点击'登录'...")
    submit_btn = page.locator('button:has-text("登录"), input[type="submit"]').first
    if await submit_btn.count() > 0:
        await submit_btn.click()
        print("   ✅ 已点击")
        await asyncio.sleep(5)
    else:
        print("   ⚠️ 未找到登录按钮，尝试按 Enter")
        await password_input.press('Enter')
        await asyncio.sleep(5)
    
    # 验证登录成功
    is_logged = await check_login_status(page)
    if is_logged:
        print("   ✅ 登录成功")
        
        # 保存 Cookie
        cookies = await page.context.cookies()
        cookie_string = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
        save_cookie(cookie_string)
        
        return True
    else:
        print("   ❌ 登录失败")
        return False


async def main():
    """主函数"""
    print("=" * 60)
    print("📊 点点数据 - 自动登录")
    print("=" * 60)
    
    # 加载账号
    credentials = load_credentials()
    username = credentials.get('username', '')
    password = credentials.get('password', '')
    
    if not username or not password:
        print("❌ 账号密码未配置")
        print("💡 请在 config/credentials.yaml 中配置")
        return False
    
    print(f"📖 账号：{username}")
    
    async with async_playwright() as p:
        # 连接已运行的浏览器
        print("\n🔌 连接浏览器...")
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        
        # 获取或创建页面
        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = context.pages[0] if context.pages else await context.new_page()
        
        print("   ✅ 已连接")
        
        try:
            # 检查登录状态
            print("\n📖 检查登录状态...")
            await page.goto('https://app.diandian.com/', wait_until='domcontentloaded', timeout=60000)
            await asyncio.sleep(3)
            
            is_logged = await check_login_status(page)
            
            if is_logged:
                print("   ✅ 已登录，无需重复登录")
                
                # 检查 Cookie 是否已保存
                saved_cookie = load_cookie()
                if not saved_cookie:
                    print("   💡 保存当前 Cookie...")
                    cookies = await page.context.cookies()
                    cookie_string = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
                    save_cookie(cookie_string)
                
                return True
            else:
                print("   ⚠️ 未登录或 Cookie 过期")
                
                # 尝试加载保存的 Cookie
                saved_cookie = load_cookie()
                if saved_cookie:
                    print("   💡 尝试使用保存的 Cookie...")
                    # 解析 Cookie
                    cookies = []
                    for cookie_str in saved_cookie.split('; '):
                        if '=' in cookie_str:
                            name, value = cookie_str.split('=', 1)
                            cookies.append({
                                'name': name,
                                'value': value,
                                'domain': '.diandian.com',
                                'path': '/'
                            })
                    
                    if cookies:
                        await page.context.add_cookies(cookies)
                        await page.reload(wait_until='domcontentloaded')
                        await asyncio.sleep(3)
                        
                        is_logged = await check_login_status(page)
                        if is_logged:
                            print("   ✅ Cookie 有效，登录成功")
                            return True
                        else:
                            print("   ❌ Cookie 已过期，需要重新登录")
                
                # 自动登录
                print("\n📖 开始自动登录...")
                success = await auto_login(page, username, password)
                
                if success:
                    print("\n" + "=" * 60)
                    print("✅ 登录完成！")
                    print("=" * 60)
                    return True
                else:
                    print("\n" + "=" * 60)
                    print("❌ 登录失败")
                    print("=" * 60)
                    return False
        
        finally:
            await browser.close()
            print("\n💡 浏览器保持运行")


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
