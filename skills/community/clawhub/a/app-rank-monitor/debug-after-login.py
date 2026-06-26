#!/usr/bin/env python3
"""调试登录后页面"""

import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
import yaml

SKILL_DIR = Path(__file__).parent
CONFIG_DIR = SKILL_DIR / "config"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                '--start-maximized',
                '--disable-extensions',
                '--disable-gpu',
                '--no-first-run',
                '--no-default-browser-check'
            ]
        )
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        
        # 加载 Cookie
        config_path = CONFIG_DIR / "diandian.yaml"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
            cookie_str = config.get('cookie', '')
            if cookie_str:
                print(f"🍪 加载 Cookie: {len(cookie_str)} 字符")
                import re
                cookies = []
                for part in cookie_str.split(';'):
                    part = part.strip()
                    if not part:
                        continue
                    name_value = part.split('=', 1)
                    if len(name_value) == 2:
                        cookies.append({
                            'name': name_value[0].strip(),
                            'value': name_value[1].strip(),
                            'domain': '.diandian.com',
                            'path': '/'
                        })
                if cookies:
                    await context.add_cookies(cookies)
                    print(f"✅ 已加载 {len(cookies)} 个 Cookie")
        
        page = await context.new_page()
        await page.goto('https://app.diandian.com/rank/line-1-0-0-75-0-3-0', wait_until='networkidle', timeout=120000)
        await asyncio.sleep(3)
        
        print(f"\n📍 URL: {page.url}")
        print(f"📄 标题: {await page.title()}")
        
        # 获取页面内容
        body_text = await page.text_content('body')
        print(f"\n📄 页面内容前 500 字符:\n")
        print(body_text[:500])
        
        # 截图
        await page.screenshot(path='debug_page.png', full_page=True)
        print(f"\n📸 截图已保存到 debug_page.png")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
