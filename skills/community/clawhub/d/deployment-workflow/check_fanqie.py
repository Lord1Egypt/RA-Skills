from playwright.sync_api import sync_playwright
import time

def main():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:18800")
        context = browser.contexts[0]
        
        # 找到红番茄后台页面
        target_page = None
        for page in context.pages:
            if "fanqieadmin" in page.url:
                target_page = page
                break
        
        if target_page:
            print(f"找到页面: {target_page.title()}")
            print(f"URL: {target_page.url}")
            
            if "login" in target_page.url.lower():
                print("\n需要登录! 请在VNC中登录...")
            else:
                print("\n页面已登录，可以操作")
                # 获取页面内容
                print("\n页面快照:")
                print(target_page.content()[:2000])
        else:
            print("未找到红番茄后台页面")
            print("\n当前页面:")
            for page in context.pages:
                print(f"  - {page.title()}: {page.url}")
        
        input("\n按回车退出...")

if __name__ == "__main__":
    main()
