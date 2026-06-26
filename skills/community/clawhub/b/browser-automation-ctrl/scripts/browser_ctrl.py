#!/usr/bin/env python3
"""
Browser Control Tool
浏览器控制工具 - 通过 Selenium 实现浏览器自动化
"""
import os
import sys
import json
import base64
import re
import io
import time

# 输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SCREENSHOT_DIR = os.path.expanduser("~/Pictures/OpenClaw")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


class BrowserController:
    """浏览器控制"""
    
    def __init__(self, browser="chrome", proxy=None, user_agent=None):
        self.driver = None
        self.browser = browser
        self.proxy = proxy
        self.user_agent = user_agent
    
    def _init_driver(self):
        """初始化浏览器驱动"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            
            # 代理
            if self.proxy:
                options.add_argument(f"--proxy-server={self.proxy}")
            
            # 用户代理
            if self.user_agent:
                options.add_argument(f"--user-agent={self.user_agent}")
            
            self.driver = webdriver.Chrome(options=options)
            
            # 反检测
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined})
                """
            })
            return True
        except Exception as e:
            return str(e)
    
    def open_url(self, url):
        """打开网址"""
        try:
            if not self.driver:
                init_result = self._init_driver()
                if init_result is not True:
                    return {"success": False, "error": f"浏览器初始化失败: {init_result}"}
            
            # 验证 URL
            if not re.match(r'^https?://', url):
                url = 'http://' + url
            
            self.driver.get(url)
            return {
                "success": True,
                "url": self.driver.current_url,
                "title": self.driver.title
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def screenshot(self, filename=None, base64_encode=False):
        """网页截图"""
        try:
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            
            if not filename:
                import datetime
                ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"browser_{ts}.png"
            
            filepath = os.path.join(SCREENSHOT_DIR, filename)
            self.driver.save_screenshot(filepath)
            
            if base64_encode:
                with open(filepath, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                return {"success": True, "path": filepath, "base64": b64[:100] + "..."}
            
            return {"success": True, "path": filepath}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def execute_script(self, script):
        """执行 JavaScript"""
        try:
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            
            result = self.driver.execute_script(script)
            return {"success": True, "result": str(result)[:1000]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def close(self):
        """关闭浏览器"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_cookies(self):
        """获取 Cookies"""
        try:
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            
            cookies = self.driver.get_cookies()
            return {"success": True, "cookies": cookies}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_cookies(self, cookies):
        """设置 Cookies"""
        try:
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_page_source(self):
        """获取页面源码"""
        try:
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            
            source = self.driver.page_source
            return {"success": True, "source": source[:2000] + "..."}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_element(self, selector):
        """查找元素 (支持 CSS 和 XPath)"""
        try:
            from selenium.webdriver.common.by import By
            
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            
            # 自动判断选择器类型
            if selector.startswith("//"):
                by = By.XPATH
            else:
                by = By.CSS_SELECTOR
            
            element = self.driver.find_element(by, selector)
            return {
                "success": True,
                "tag": element.tag_name,
                "text": element.text[:200],
                "href": element.get_attribute("href"),
                "id": element.get_attribute("id"),
                "class": element.get_attribute("class")
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def click(self, selector):
        """点击元素"""
        try:
            from selenium.webdriver.common.by import By
            
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            
            if selector.startswith("//"):
                by = By.XPATH
            else:
                by = By.CSS_SELECTOR
            
            element = self.driver.find_element(by, selector)
            element.click()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def fill(self, selector, text):
        """填写输入框"""
        try:
            from selenium.webdriver.common.by import By
            
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            
            if selector.startswith("//"):
                by = By.XPATH
            else:
                by = By.CSS_SELECTOR
            
            element = self.driver.find_element(by, selector)
            element.clear()
            element.send_keys(text)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def back(self):
        """后退"""
        try:
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            self.driver.back()
            return {"success": True, "url": self.driver.current_url}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def forward(self):
        """前进"""
        try:
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            self.driver.forward()
            return {"success": True, "url": self.driver.current_url}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def refresh(self):
        """刷新"""
        try:
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            self.driver.refresh()
            return {"success": True, "url": self.driver.current_url}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def wait(self, seconds):
        """等待"""
        try:
            time.sleep(float(seconds))
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def scroll(self, x=0, y=0):
        """滚动页面"""
        try:
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            self.driver.execute_script(f"window.scrollTo({x}, {y})")
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def scroll_to_element(self, selector):
        """滚动到元素"""
        try:
            from selenium.webdriver.common.by import By
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            
            if selector.startswith("//"):
                by = By.XPATH
            else:
                by = By.CSS_SELECTOR
            
            element = self.driver.find_element(by, selector)
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def new_tab(self, url=""):
        """新建标签页"""
        try:
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            self.driver.execute_script(f"window.open('{url}')")
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def switch_tab(self, index=0):
        """切换标签页"""
        try:
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            
            windows = self.driver.window_handles
            if index < len(windows):
                self.driver.switch_to.window(windows[index])
                return {"success": True, "url": self.driver.current_url}
            return {"success": False, "error": f"标签页 {index} 不存在"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def close_tab(self):
        """关闭当前标签页"""
        try:
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            self.driver.close()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_tabs(self):
        """获取所有标签页"""
        try:
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            
            tabs = []
            for i, handle in enumerate(self.driver.window_handles):
                self.driver.switch_to.window(handle)
                tabs.append({"index": i, "url": self.driver.current_url, "title": self.driver.title})
            return {"success": True, "tabs": tabs}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def screenshot_element(self, selector, filename=None):
        """元素截图"""
        try:
            from selenium.webdriver.common.by import By
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            
            if selector.startswith("//"):
                by = By.XPATH
            else:
                by = By.CSS_SELECTOR
            
            element = self.driver.find_element(by, selector)
            
            if not filename:
                import datetime
                ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"element_{ts}.png"
            
            filepath = os.path.join(SCREENSHOT_DIR, filename)
            element.screenshot(filepath)
            return {"success": True, "path": filepath}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def submit(self, selector):
        """提交表单"""
        try:
            from selenium.webdriver.common.by import By
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            
            if selector.startswith("//"):
                by = By.XPATH
            else:
                by = By.CSS_SELECTOR
            
            element = self.driver.find_element(by, selector)
            element.submit()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def hover(self, selector):
        """悬停"""
        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.common.action_chains import ActionChains
            
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            
            if selector.startswith("//"):
                by = By.XPATH
            else:
                by = By.CSS_SELECTOR
            
            element = self.driver.find_element(by, selector)
            ActionChains(self.driver).move_to_element(element).perform()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_attributes(self, selector, attr):
        """获取元素属性"""
        try:
            from selenium.webdriver.common.by import By
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            
            if selector.startswith("//"):
                by = By.XPATH
            else:
                by = By.CSS_SELECTOR
            
            element = self.driver.find_element(by, selector)
            value = element.get_attribute(attr)
            return {"success": True, "value": value}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ========== 高级功能 ==========
    
    def set_user_agent(self, ua):
        """设置 User-Agent (需要在打开网页前设置)"""
        try:
            # 重新初始化浏览器
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument(f"--user-agent={ua}")
            
            if self.driver:
                self.driver.quit()
            self.driver = webdriver.Chrome(options=options)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_proxy(self, proxy):
        """设置代理"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument(f"--proxy-server={proxy}")
            
            if self.driver:
                self.driver.quit()
            self.driver = webdriver.Chrome(options=options)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def save_pdf(self, filepath=None):
        """导出 PDF"""
        try:
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            
            if not filepath:
                import datetime
                ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filepath = os.path.join(SCREENSHOT_DIR, f"page_{ts}.pdf")
            
            # 使用打印到 PDF
            self.driver.execute_script("window.print()")
            return {"success": True, "path": filepath}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_screensize(self):
        """获取页面尺寸"""
        try:
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            
            width = self.driver.execute_script("return document.documentElement.scrollWidth")
            height = self.driver.execute_script("return document.documentElement.scrollHeight")
            return {"success": True, "width": width, "height": height}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def full_screenshot(self, filename=None):
        """全页面截图"""
        try:
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            
            # 获取完整页面尺寸
            width = self.driver.execute_script("return document.documentElement.scrollWidth")
            height = self.driver.execute_script("return document.documentElement.scrollHeight")
            
            # 设置窗口大小
            self.driver.set_window_size(width, height)
            
            if not filename:
                import datetime
                ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"full_{ts}.png"
            
            filepath = os.path.join(SCREENSHOT_DIR, filename)
            self.driver.save_screenshot(filepath)
            
            # 恢复窗口大小
            self.driver.set_window_size(1920, 1080)
            
            return {"success": True, "path": filepath}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def wait_element(self, selector, timeout=10):
        """等待元素出现"""
        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            
            if selector.startswith("//"):
                by = By.XPATH
            else:
                by = By.CSS_SELECTOR
            
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, selector))
            )
            return {"success": True, "tag": element.tag_name}
        except Exception as e:
            return {"success": False, "error": f"等待超时: {str(e)}"}
    
    def click_until_success(self, selector, max_attempts=3):
        """重试点击直到成功"""
        try:
            from selenium.webdriver.common.by import By
            
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            
            if selector.startswith("//"):
                by = By.XPATH
            else:
                by = By.CSS_SELECTOR
            
            for i in range(max_attempts):
                try:
                    element = self.driver.find_element(by, selector)
                    element.click()
                    return {"success": True, "attempts": i + 1}
                except:
                    time.sleep(0.5)
            
            return {"success": False, "error": f"点击失败，已重试 {max_attempts} 次"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_all_links(self):
        """获取所有链接"""
        try:
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            
            links = []
            elements = self.driver.find_elements("tag name", "a")
            for elem in elements:
                href = elem.get_attribute("href")
                text = elem.text[:50]
                if href:
                    links.append({"text": text, "href": href})
            
            return {"success": True, "links": links[:50]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_all_images(self):
        """获取所有图片"""
        try:
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            
            images = []
            elements = self.driver.find_elements("tag name", "img")
            for elem in elements:
                src = elem.get_attribute("src")
                alt = elem.get_attribute("alt")
                if src:
                    images.append({"src": src, "alt": alt})
            
            return {"success": True, "images": images[:30]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def clear_cookies(self):
        """清除所有 Cookies"""
        try:
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            self.driver.delete_all_cookies()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_cookie(self, name, value, **kwargs):
        """设置单个 Cookie"""
        try:
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            
            cookie = {"name": name, "value": value}
            cookie.update(kwargs)
            self.driver.add_cookie(cookie)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_title(self):
        """获取标题"""
        try:
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            return {"success": True, "title": self.driver.title}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_url(self):
        """获取当前 URL"""
        try:
            if not self.driver:
                return {"success": False, "error": "浏览器未启动"}
            return {"success": True, "url": self.driver.current_url}
        except Exception as e:
            return {"success": False, "error": str(e)}


def main():
    if len(sys.argv) < 2:
        print("Usage: python browser_ctrl.py <command> [args...]")
        print("")
        print("Commands:")
        print("  open <url>                - 打开网页")
        print("  screenshot                - 网页截图")
        print("  screenshotb64            - 网页截图(base64)")
        print("  js <script>              - 执行 JavaScript")
        print("  cookies                  - 获取 Cookies")
        print("  source                   - 获取页面源码")
        print("  find <selector>          - 查找元素")
        print("  click <selector>         - 点击元素")
        print("  fill <selector> <text>  - 填写输入框")
        print("  submit <selector>         - 提交表单")
        print("  hover <selector>         - 悬停")
        print("  attr <selector> <name>   - 获取元素属性")
        print("  back                     - 后退")
        print("  forward                  - 前进")
        print("  refresh                  - 刷新")
        print("  wait <seconds>            - 等待")
        print("  scroll [x] [y]          - 滚动页面")
        print("  scrollto <selector>      - 滚动到元素")
        print("  newtab <url>             - 新建标签页")
        print("  switchtab <index>        - 切换标签页")
        print("  closetab                 - 关闭标签页")
        print("  tabs                     - 获取所有标签页")
        print("  title                    - 获取标题")
        print("  url                      - 获取当前 URL")
        print("  close                    - 关闭浏览器")
        sys.exit(1)
    
    browser = BrowserController()
    cmd = sys.argv[1]
    
    if cmd == "open":
        url = sys.argv[2] if len(sys.argv) > 2 else ""
        result = browser.open_url(url)
    elif cmd == "screenshot":
        filename = sys.argv[2] if len(sys.argv) > 2 else None
        result = browser.screenshot(filename)
    elif cmd == "screenshotb64":
        result = browser.screenshot(base64_encode=True)
    elif cmd == "js":
        script = sys.argv[2] if len(sys.argv) > 2 else ""
        result = browser.execute_script(script)
    elif cmd == "cookies":
        result = browser.get_cookies()
    elif cmd == "source":
        result = browser.get_page_source()
    elif cmd == "find":
        selector = sys.argv[2] if len(sys.argv) > 2 else ""
        result = browser.find_element(selector)
    elif cmd == "click":
        selector = sys.argv[2] if len(sys.argv) > 2 else ""
        result = browser.click(selector)
    elif cmd == "fill":
        selector = sys.argv[2] if len(sys.argv) > 2 else ""
        text = sys.argv[3] if len(sys.argv) > 3 else ""
        result = browser.fill(selector, text)
    elif cmd == "submit":
        selector = sys.argv[2] if len(sys.argv) > 2 else ""
        result = browser.submit(selector)
    elif cmd == "hover":
        selector = sys.argv[2] if len(sys.argv) > 2 else ""
        result = browser.hover(selector)
    elif cmd == "attr":
        selector = sys.argv[2] if len(sys.argv) > 2 else ""
        attr = sys.argv[3] if len(sys.argv) > 3 else ""
        result = browser.get_attributes(selector, attr)
    elif cmd == "back":
        result = browser.back()
    elif cmd == "forward":
        result = browser.forward()
    elif cmd == "refresh":
        result = browser.refresh()
    elif cmd == "wait":
        seconds = sys.argv[2] if len(sys.argv) > 2 else "1"
        result = browser.wait(seconds)
    elif cmd == "scroll":
        x = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        y = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        result = browser.scroll(x, y)
    elif cmd == "scrollto":
        selector = sys.argv[2] if len(sys.argv) > 2 else ""
        result = browser.scroll_to_element(selector)
    elif cmd == "newtab":
        url = sys.argv[2] if len(sys.argv) > 2 else ""
        result = browser.new_tab(url)
    elif cmd == "switchtab":
        index = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        result = browser.switch_tab(index)
    elif cmd == "closetab":
        result = browser.close_tab()
    elif cmd == "tabs":
        result = browser.get_tabs()
    elif cmd == "title":
        result = browser.get_title()
    elif cmd == "url":
        result = browser.get_url()
    elif cmd == "fullscreen":
        result = browser.full_screenshot()
    elif cmd == "waitelem":
        selector = sys.argv[2] if len(sys.argv) > 2 else ""
        timeout = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        result = browser.wait_element(selector, timeout)
    elif cmd == "links":
        result = browser.get_all_links()
    elif cmd == "images":
        result = browser.get_all_images()
    elif cmd == "size":
        result = browser.get_screensize()
    elif cmd == "clearcookies":
        result = browser.clear_cookies()
    elif cmd == "setcookie":
        name = sys.argv[2] if len(sys.argv) > 2 else ""
        value = sys.argv[3] if len(sys.argv) > 3 else ""
        result = browser.set_cookie(name, value)
    elif cmd == "ua":
        ua = sys.argv[2] if len(sys.argv) > 2 else ""
        result = browser.set_user_agent(ua)
    elif cmd == "proxy":
        proxy = sys.argv[2] if len(sys.argv) > 2 else ""
        result = browser.set_proxy(proxy)
    elif cmd == "close":
        result = browser.close()
    else:
        result = {"success": False, "error": f"Unknown command: {cmd}"}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
