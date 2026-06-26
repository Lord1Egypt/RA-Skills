#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time

def check_poolx():
    with sync_playwright() as p:
        # 尝试不同设置
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu',
            ]
        )
        
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        page = context.new_page()
        
        # 注入stealth脚本
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        try:
            page.goto("https://www.bitget.com/events/poolx", timeout=45000)
            time.sleep(10)  # 等待更长时间
            
            # 检查是否有人登录状态（可能有不同的内容）
            content = page.content()
            
            if "Just a moment" in content or "security verification" in content or "challenge" in content.lower():
                print("❌ 被 Cloudflare 拦截")
            else:
                text = page.inner_text("body")
                print(f"✅ 成功! 文本长度: {len(text)}")
                if "Stake" in text:
                    print("  - 包含 Stake")
                if "Pool" in text:
                    print("  - 包含 Pool")
                if "No projects" in text:
                    print("  - 显示无项目")
                    
        except Exception as e:
            print(f"❌ 错误: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    check_poolx()
