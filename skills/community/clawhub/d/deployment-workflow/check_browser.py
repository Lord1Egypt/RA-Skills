from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        # 连接已经运行的Chrome
        browser = p.chromium.connect_over_cdp("http://localhost:18800")
        
        # 获取所有页面
        contexts = browser.contexts
        if contexts:
            context = contexts[0]
            pages = context.pages
            print(f"找到 {len(pages)} 个页面:")
            for i, page in enumerate(pages):
                print(f"  {i+1}. {page.title()} - {page.url}")
            
            # 切换到第一个页面
            if pages:
                page = pages[0]
                print(f"\n当前页面: {page.title()}")
                print(f"URL: {page.url}")
                
                # 如果是登录页面，提示需要登录
                if "login" in page.url.lower():
                    print("\n需要登录! 请在VNC中登录...")
                else:
                    print("\n页面已加载，可以开始操作")
        else:
            print("没有找到浏览器上下文")
        
        input("按回车退出...")

if __name__ == "__main__":
    main()
