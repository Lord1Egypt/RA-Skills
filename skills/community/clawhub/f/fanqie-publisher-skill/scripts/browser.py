# -*- coding: utf-8 -*-
"""
番茄小说自动发布 - 浏览器自动化核心
"""

import json
import os
import time
import random
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from config import BROWSER_CONFIG, COOKIE_FILE, TIMEOUT, SELECTORS, BASE_URL

# 全局变量 - 保持浏览器实例
_playwright_instance = None
_browser_instance = None
_context_instance = None
_page_instance = None


class FanqieBrowser:
    """番茄小说浏览器自动化类"""
    
    def __init__(self):
        self.cookie_path = Path(__file__).parent / COOKIE_FILE
    
    @property
    def playwright(self):
        """获取playwright实例（单例）"""
        global _playwright_instance
        if _playwright_instance is None:
            _playwright_instance = sync_playwright().start()
        return _playwright_instance
    
    @property
    def browser(self) -> Browser:
        """获取浏览器实例（单例）"""
        global _browser_instance
        if _browser_instance is None:
            print("[浏览器] 正在启动...")
            _browser_instance = self.playwright.chromium.launch(
                headless=BROWSER_CONFIG["headless"],
                slow_mo=BROWSER_CONFIG["slow_mo"],
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-infobars',
                    '--no-sandbox',
                ]
            )
            print("[浏览器] 启动成功")
        return _browser_instance
    
    @property
    def context(self) -> BrowserContext:
        """获取浏览器上下文（单例）"""
        global _context_instance
        if _context_instance is None:
            _context_instance = self.browser.new_context(
                viewport=BROWSER_CONFIG["viewport"],
                user_agent=BROWSER_CONFIG["user_agent"]
            )
            # 注入反检测脚本
            _context_instance.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)
        return _context_instance
    
    @property
    def page(self) -> Page:
        """获取页面实例（单例）"""
        global _page_instance
        if _page_instance is None:
            _page_instance = self.context.new_page()
        return _page_instance
    
    def stop(self):
        """关闭浏览器"""
        global _playwright_instance, _browser_instance, _context_instance, _page_instance
        
        if _browser_instance:
            _browser_instance.close()
            _browser_instance = None
        if _playwright_instance:
            _playwright_instance.stop()
            _playwright_instance = None
        _context_instance = None
        _page_instance = None
        print("[浏览器] 已关闭")
    
    def save_cookies(self):
        """保存Cookie到文件"""
        cookies = self.context.cookies()
        with open(self.cookie_path, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        print(f"[Cookie] 已保存到 {self.cookie_path}")
    
    def load_cookies(self) -> bool:
        """从文件加载Cookie"""
        if not self.cookie_path.exists():
            print("[Cookie] Cookie文件不存在")
            return False
        
        try:
            with open(self.cookie_path, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            self.context.add_cookies(cookies)
            print("[Cookie] Cookie加载成功")
            return True
        except Exception as e:
            print(f"[Cookie] 加载失败: {e}")
            return False
    
    def clear_cookies(self):
        """清除保存的Cookie"""
        if self.cookie_path.exists():
            os.remove(self.cookie_path)
            print("[Cookie] Cookie文件已删除")
    
    def goto(self, url: str):
        """导航到指定URL"""
        print(f"[导航] 正在访问: {url}")
        self.page.goto(url, timeout=TIMEOUT["page_load"])
        self._random_delay()
    
    def wait_for_selector(self, selector: str, timeout: int = None):
        """等待元素出现"""
        timeout = timeout or TIMEOUT["page_load"]
        return self.page.wait_for_selector(selector, timeout=timeout)
    
    def click(self, selector: str):
        """点击元素"""
        self._random_delay()
        self.page.click(selector)
        self._random_delay()
    
    def fill(self, selector: str, text: str):
        """填充输入框"""
        self._random_delay()
        self.page.fill(selector, text)
        self._random_delay()
    
    def type_text(self, selector: str, text: str, delay: int = 50):
        """模拟打字"""
        self.page.click(selector)
        for char in text:
            self.page.keyboard.type(char, delay=random.randint(delay - 20, delay + 20))
    
    def get_text(self, selector: str) -> str:
        """获取元素文本"""
        element = self.page.query_selector(selector)
        return element.text_content() if element else ""
    
    def screenshot(self, path: str):
        """截图"""
        self.page.screenshot(path=path)
        print(f"[截图] 已保存到 {path}")
    
    def _random_delay(self, min_ms: int = 500, max_ms: int = 1500):
        """随机延迟"""
        delay = random.randint(min_ms, max_ms) / 1000
        time.sleep(delay)
    
    def is_logged_in(self) -> bool:
        """检查是否已登录"""
        try:
            self.goto(BASE_URL)
            # 检查是否有"作家专区"或用户信息
            writer_zone = self.page.query_selector(SELECTORS["login_success"])
            return writer_zone is not None
        except:
            return False


def get_browser() -> FanqieBrowser:
    """获取浏览器实例（单例）"""
    return FanqieBrowser()


if __name__ == "__main__":
    # 测试代码
    browser = get_browser()
    
    try:
        browser.goto(BASE_URL)
        print("页面标题:", browser.page.title())
        
        if browser.is_logged_in():
            print("已登录")
        else:
            print("未登录，请先执行登录操作")
    finally:
        browser.stop()