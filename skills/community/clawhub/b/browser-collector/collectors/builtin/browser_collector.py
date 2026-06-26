#!/usr/bin/env python3
"""
collectors/builtin/browser_collector.py - 通用浏览器采集器

整合所有模块的一站式采集器：
- 反检测（stealth.py）
- Cookie持久化（cookie_db.py）
- 验证码识别（captcha_solver.py）
- 代理支持（proxy_pool.py）
- 批量采集（batch_collector.py）

与 base.py 的 StructuredItem 完全兼容

Usage:
    # 基本使用
    collector = BrowserCollector()
    item = collector.collect('https://github.com/microsoft/vscode')
    print(item.title, item.content[:200])

    # 带代理
    collector = BrowserCollector(proxy_pool=ProxyPool())

    # 批量采集
    batch = collector.batch(max_workers=2)
    items = batch.collect_urls(urls)

    # 自定义适配器
    collector = BrowserCollector(adapters={'github': MyGitHubAdapter()})
    item = collector.collect_with_adapter('github', 'https://github.com/microsoft/vscode')
"""

import os
import sys
import time
import random
import hashlib
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any, Callable, Union
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

import sys as _sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from collectors.base import (
    StructuredItem,
    StockQuote,
    Discussion,
    items_to_dict_list,
)

# 导入所有依赖模块
from collectors.stealth import StealthConfig, apply_stealth, stealth_context
from collectors.cookie_db import CookieDatabase, MultiDomainCookieManager
from collectors.captcha_solver import CaptchaSolver, SliderCaptchaSolver
from collectors.proxy_pool import ProxyPool, SyncProxyPool


# ==================== BrowserCollector ====================

class BrowserCollector:
    """
    通用浏览器采集器

    功能：
    1. Playwright反检测（可配置级别）
    2. Cookie持久化（自动保存/恢复）
    3. 验证码识别（ddddocr + Tesseract）
    4. 代理支持（从ProxyPool自动选取）
    5. 站点适配器支持
    6. 批量采集（BatchCollector集成）

    与现有采集器的区别：
    - EastMoneyCollector/XueqiuCollector：针对特定站点的API/页面采集
    - BrowserCollector：通用的Playwright控制，适配任意站点

    Usage:
        collector = BrowserCollector()
        item = collector.collect('https://github.com/microsoft/vscode')
        print(item.title, item.content[:100])

        # 指定适配器
        item = collector.collect('https://github.com/microsoft/vscode',
                                adapter='github',
                                wait_selector='article')
    """

    # 内置适配器映射（可扩展）
    DEFAULT_ADAPTERS: Dict[str, str] = {
        'github.com': 'github',
        'zhihu.com': 'zhihu',
        'juejin.cn': 'juejin',
        'csdn.net': 'csdn',
        'aliyun.com': 'aliyun',
        'help.aliyun.com': 'aliyun',
    }

    def __init__(self,
                 cookie_db_path: str = None,
                 proxy_pool: Optional[ProxyPool] = None,
                 stealth_level: str = 'medium',
                 auto_save_cookies: bool = True,
                 auto_save_screenshots: bool = False,
                 screenshot_dir: str = None,
                 max_contexts: int = 5,
                 request_interval: float = 2.0,
                 user_agent: str = None,
                 headless: bool = True):
        """
        Args:
            cookie_db_path: Cookie数据库路径
            proxy_pool: 代理池实例
            stealth_level: 反检测级别 ('basic'/'medium'/'aggressive')
            auto_save_cookies: 是否自动保存Cookie
            auto_save_screenshots: 是否自动保存截图
            screenshot_dir: 截图保存目录
            max_contexts: 最大Context缓存数（超过后LRU淘汰）
            request_interval: 请求间隔（秒）
            user_agent: 固定UA（None则随机）
            headless: 是否无头模式
        """
        base = Path.home() / ".openclaw"
        self.cookie_db_path = cookie_db_path or str(base / "data" / "cookies.db")
        self.screenshot_dir = screenshot_dir or str(base / "screenshots")
        self.stealth_level = stealth_level
        self.auto_save_cookies = auto_save_cookies
        self.auto_save_screenshots = auto_save_screenshots
        self.max_contexts = max_contexts
        self.request_interval = request_interval
        self.headless = headless

        # UA
        if user_agent:
            self.user_agent = user_agent
        else:
            self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'

        # 内部组件
        self._pw = None
        self._browser: Optional[Browser] = None
        self._contexts: Dict[str, BrowserContext] = {}  # domain → Context
        self._lru_order: List[str] = []  # LRU顺序

        # Cookie管理
        self.cookie_db = CookieDatabase(self.cookie_db_path)
        self.cookie_manager = MultiDomainCookieManager(self.cookie_db_path)

        # 代理
        self.proxy_pool = proxy_pool
        self._sync_proxy_pool: Optional[SyncProxyPool] = None
        if proxy_pool:
            self._sync_proxy_pool = SyncProxyPool()

        # 验证码
        self.captcha_solver = CaptchaSolver()
        self.slider_solver = SliderCaptchaSolver()

        # 适配器
        self.adapters: Dict[str, Any] = {}

        # 自动注册内置适配器
        self._register_builtin_adapters()

        # 状态
        self._request_count = 0
        self._last_request_time = time.time()

        Path(self.cookie_db_path).parent.mkdir(parents=True, exist_ok=True)
        Path(self.screenshot_dir).mkdir(parents=True, exist_ok=True)

        self._init_browser()

    def _init_browser(self):
        """初始化Playwright浏览器"""
        self._pw = sync_playwright().start()
        self._browser = self._pw.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu',
                '--disable-setuid-sandbox',
                '--disable-web-security',
                '--allow-running-insecure-content',
                '--no-sandbox',
            ]
        )

    def _get_stealth_script(self) -> str:
        config = StealthConfig(level=self.stealth_level)
        return config.get_combined_script()

    def _get_context(self, domain: str) -> BrowserContext:
        """
        获取/创建指定域名的隔离Context（LRU缓存）
        """
        # 命中
        if domain in self._contexts:
            # 更新LRU
            if domain in self._lru_order:
                self._lru_order.remove(domain)
            self._lru_order.append(domain)
            return self._contexts[domain]

        # LRU淘汰
        if len(self._contexts) >= self.max_contexts:
            oldest = self._lru_order.pop(0)
            self._contexts[oldest].close()
            del self._contexts[oldest]

        # 创建新Context
        context = self._browser.new_context(
            user_agent=self.user_agent,
            viewport={'width': 1920, 'height': 1080},
            locale='zh-CN',
            timezone_id='Asia/Shanghai',
            permissions=['geolocation'],
            ignore_https_errors=True,
        )

        # 反检测（init script在页面JS执行前运行）
        context.add_init_script(self._get_stealth_script())

        # 加载Cookie
        if self.auto_save_cookies:
            cookies = self.cookie_db.get_cookies(domain)
            if cookies:
                try:
                    context.add_cookies(cookies)
                except Exception as e:
                    print(f"[BrowserCollector] Failed to add cookies for {domain}: {e}")

        self._contexts[domain] = context
        self._lru_order.append(domain)
        return context

    def _get_page(self, domain: str) -> Page:
        """获取指定域名的Page（自动创建Context）"""
        context = self._get_context(domain)
        page = context.new_page()

        # 自动保存Cookie on close
        if self.auto_save_cookies:
            def save_on_close():
                try:
                    cookies = context.cookies()
                    self.cookie_db.save_cookies(cookies, domain)
                except Exception as e:
                    print(f"[BrowserCollector] Failed to save cookies: {e}")

            page.on('close', lambda: save_on_close())

        return page

    def _request_throttle(self):
        """请求限速"""
        self._request_count += 1
        now = time.time()
        elapsed = now - self._last_request_time
        if elapsed < self.request_interval:
            time.sleep(self.request_interval - elapsed)
        self._last_request_time = time.time()

    def _get_proxy_for_url(self, url: str) -> Optional[str]:
        """为URL选取代理"""
        if not self._sync_proxy_pool:
            return None
        return self._sync_proxy_pool.get_url()

    def _register_builtin_adapters(self):
        """自动注册内置适配器"""
        try:
            # 新架构适配器（social platforms）
            from collectors.adapters.builtin.social import (
                GitHubAdapter, ZhihuAdapter,
                JuejinAdapter, CsdnAdapter,
            )
            # 新架构云文档适配器
            from collectors.adapters.builtin.cloud_docs.aliyun import AliyunDocAdapter

            self.adapters['github'] = GitHubAdapter()
            self.adapters['zhihu'] = ZhihuAdapter()
            self.adapters['juejin'] = JuejinAdapter()
            self.adapters['csdn'] = CsdnAdapter()
            self.adapters['aliyun'] = AliyunDocAdapter()
        except ImportError as e:
            # 适配器模块不可用，降级到旧架构
            try:
                from collectors.builtin.adapters import (
                    GitHubAdapter, ZhihuAdapter,
                    JuejinAdapter, CsdnAdapter, AliyunAdapter,
                )
                self.adapters['github'] = GitHubAdapter()
                self.adapters['zhihu'] = ZhihuAdapter()
                self.adapters['juejin'] = JuejinAdapter()
                self.adapters['csdn'] = CsdnAdapter()
                self.adapters['aliyun'] = AliyunAdapter()
            except ImportError:
                pass

    def _detect_adapter(self, url: str) -> Optional[str]:
        """根据URL检测适配器（内部）"""
        parsed = urlparse(url)
        domain = parsed.netloc
        return self.DEFAULT_ADAPTERS.get(domain)

    def auto_detect_adapter(self, url: str) -> Optional[str]:
        """
        根据URL自动检测适配器名称

        Args:
            url: 目标URL

        Returns:
            适配器名称（如 'github', 'zhihu'），或 None
        """
        return self._detect_adapter(url)

    # ---- 核心采集API ----

    def collect(self,
                url: str,
                wait_selector: str = None,
                wait_time: float = 2.0,
                retries: int = 2,
                adapter: str = None,
                timeout: float = 30.0) -> StructuredItem:
        """
        通用采集方法

        Args:
            url: 目标URL
            wait_selector: 等待元素加载的选择器
            wait_time: 额外等待时间（秒）
            retries: 重试次数
            adapter: 适配器名称（None则自动检测）
            timeout: 超时时间（秒）

        Returns:
            StructuredItem: 采集结果

        与 base.py 完全兼容
        """
        from urllib.parse import urlparse
        domain = urlparse(url).netloc

        self._request_throttle()

        # 选取代理
        proxy = self._get_proxy_for_url(url)
        context = self._get_context(domain)
        if proxy:
            context.set_proxy(proxy={'server': proxy})

        page = context.new_page()

        try:
            adapter_name = adapter or self._detect_adapter(url)

            for attempt in range(retries + 1):
                try:
                    page.goto(url, wait_until='networkidle', timeout=int(timeout * 1000))

                    if wait_selector:
                        page.wait_for_selector(wait_selector, timeout=int(timeout * 1000))

                    if wait_time > 0:
                        time.sleep(wait_time)

                    # 提取数据
                    if adapter_name and adapter_name in self.adapters:
                        adapter_obj = self.adapters[adapter_name]
                        data = adapter_obj.extract(page, url)
                    else:
                        data = self._default_extract(page, url)

                    # 保存截图
                    if self.auto_save_screenshots:
                        self.save_screenshot(page, domain)

                    return data

                except Exception as e:
                    if attempt < retries:
                        time.sleep(2 ** attempt)
                        continue
                    raise

            return self._default_extract(page, url)

        finally:
            if self.auto_save_cookies:
                try:
                    cookies = context.cookies()
                    self.cookie_db.save_cookies(cookies, domain)
                except:
                    pass

    def _default_extract(self, page: Page, url: str) -> StructuredItem:
        """默认数据提取"""
        return StructuredItem(
            title=page.title(),
            url=page.url,
            platform=urlparse(url).netloc,
            content=page.locator('body').inner_text()[:10000],
            checksum=hashlib.md5(page.content()[:5000].encode()).hexdigest()[:12],
        )

    def collect_as_dict(self, url: str, **kwargs) -> Dict[str, Any]:
        """collect的dict版本"""
        item = self.collect(url, **kwargs)
        return item.to_dict()

    # ---- 验证码处理 ----

    def solve_captcha(self, page: Page, image_bytes: bytes = None) -> Optional[str]:
        """
        处理页面上的图片验证码

        Args:
            page: Playwright Page
            image_bytes: 验证码图片字节（None则自动截取）

        Returns:
            识别出的文字，或None
        """
        if image_bytes is None:
            # 尝试定位验证码图片
            captcha_img = page.locator('img[src*="captcha"], canvas[id*="captcha"]')
            if captcha_img.count() > 0:
                image_bytes = captcha_img.first.screenshot()

        if image_bytes:
            return self.captcha_solver.solve_image(image_bytes)
        return None

    def solve_slider_captcha(self,
                            page: Page,
                            full_image_path: str,
                            slider_selector: str = '[class*="slider"], [class*="drag"]',
                            by: str = 'css') -> bool:
        """
        处理滑块验证码

        Args:
            page: Playwright Page
            full_image_path: 背景图路径（需先截图保存）
            slider_selector: 滑块元素选择器

        Returns:
            是否成功
        """
        from collectors.captcha_solver import solve_slider_with_playwright
        track = self.slider_solver.solve_slider(full_image_path)
        if not track:
            return False

        solve_slider_with_playwright(page, slider_selector, track, by)
        return True

    # ---- 截图 ----

    def save_screenshot(self, page: Page, domain: str = 'unknown') -> str:
        """保存截图"""
        filename = f"{domain}_{int(time.time())}_{random.randint(1000,9999)}.png"
        path = os.path.join(self.screenshot_dir, filename)
        page.screenshot(path=path, full_page=True)
        return path

    # ---- 批量采集 ----

    def batch(self, max_workers: int = 2) -> 'BatchCollectorWrapper':
        """返回批量采集器包装"""
        return BatchCollectorWrapper(self, max_workers=max_workers)

    # ---- 适配器注册 ----

    def register_adapter(self, name: str, adapter: Any):
        """注册站点适配器"""
        self.adapters[name] = adapter

    def collect_with_adapter(self, adapter_name: str, url: str, **kwargs) -> StructuredItem:
        """使用指定适配器采集"""
        return self.collect(url, adapter=adapter_name, **kwargs)

    # ---- 生命周期 ----

    def close(self):
        """关闭所有资源"""
        if self.auto_save_cookies:
            self.save_all_cookies()

        for context in self._contexts.values():
            context.close()

        if self._browser:
            self._browser.close()

        if self._pw:
            self._pw.stop()

    def save_all_cookies(self):
        """保存所有Context的Cookie"""
        for domain, context in self._contexts.items():
            try:
                cookies = context.cookies()
                self.cookie_db.save_cookies(cookies, domain)
            except Exception as e:
                print(f"[BrowserCollector] Failed to save cookies for {domain}: {e}")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'request_count': self._request_count,
            'active_contexts': len(self._contexts),
            'max_contexts': self.max_contexts,
            'cookie_stats': self.cookie_db.get_statistics(),
        }


# ==================== BatchCollectorWrapper ====================

class BatchCollectorWrapper:
    """
    BatchCollector的便捷包装

    将 BrowserCollector 的方法适配为 BatchCollector 的回调
    """

    def __init__(self, collector: BrowserCollector, max_workers: int = 2):
        from collectors.batch_collector import BatchCollector as _BC
        self._collector = collector
        self._batch = _BC(
            collector=None,  # 不使用默认collector，用自定义handler
            max_workers=max_workers,
            cookie_db_path=collector.cookie_db_path,
        )

    def collect_urls(self,
                     urls: List[str],
                     handler: Callable[[Page, str], StructuredItem] = None,
                     progress_callback: Callable[[int, int], None] = None) -> List[StructuredItem]:
        """批量采集URL"""

        def wrapper(page, url):
            if handler:
                result = handler(page, url)
            else:
                result = self._collector.collect(url)
            if isinstance(result, StructuredItem):
                return result.to_dict()
            return result

        return self._batch.collect_urls_as_items(urls, handler=wrapper,
                                                 progress_callback=progress_callback)

    def close(self):
        self._batch.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


# ==================== auto_fetch ====================

import json
import re
import urllib.request
from typing import Tuple, Optional

# SPA站点列表路径
_SPA_SITES_PATH = Path(__file__).parent.parent.parent / "spa_sites.json"


def _load_spa_sites() -> dict:
    """加载SPA站点列表"""
    try:
        with open(_SPA_SITES_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
        return {"sites": [], "detection_rules": {}}
    except Exception:
        return {"sites": [], "detection_rules": {}}


def _is_known_spa(url: str, spa_sites: dict) -> bool:
    """检查URL是否属于已知SPA站点"""
    parsed = urlparse(url)
    hostname = parsed.netloc.lower()
    for site in spa_sites.get("sites", []):
        if site["domain"].lower() in hostname:
            return True
    return False


def _detect_spa_from_html(html: str, spa_sites: dict) -> bool:
    """
    从HTML内容检测是否为JS渲染页面
    
    Returns:
        True if page appears to be JS-rendered (no real content)
    """
    if not html or len(html) < 200:
        return True
    
    rules = spa_sites.get("detection_rules", {})
    
    # 检查SPA特征
    for indicator in rules.get("spa_indicators", []):
        if indicator in html:
            # 有SPA特征但内容可能还没渲染
            pass
    
    # 检查空内容指示器
    for indicator in rules.get("empty_content_indicators", []):
        if indicator in html:
            return True
    
    # 检查是否只有导航/页脚（正文太少）
    # 移除script/style标签后看实际文本量
    text_only = re.sub(r'<script[^>]*>[\s\S]*?</script>', '', html, flags=re.I)
    text_only = re.sub(r'<style[^>]*>[\s\S]*?</style>', '', text_only, flags=re.I)
    text_only = re.sub(r'<[^>]+>', '', text_only)
    text_only = text_only.strip()
    
    min_len = rules.get("min_content_length", 500)
    if len(text_only) < min_len:
        return True
    
    return False


def _quick_fetch(url: str, timeout: int = 10) -> Tuple[str, int]:
    """
    快速获取页面前20KB用于检测
    
    Returns:
        (html_content, status_code)
    """
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            }
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.status
            # 只读前20KB
            html = resp.read(20 * 1024).decode('utf-8', errors='ignore')
            return html, status
    except Exception as e:
        return f"ERROR: {e}", 0


def auto_fetch(url: str,
               wait_time: float = 3.0,
               force_browser: bool = False,
               timeout: int = 30) -> Tuple[str, str, str]:
    """
    智能内容获取 - 自动选择最佳抓取方式

    策略:
    1. 已知SPA站点 → 直接Playwright渲染
    2. 未知站点 → 先web_fetch快速试探
    3. 内容检测为SPA → 切换Playwright渲染
    4. 普通页面 → web_fetch结果

    Args:
        url: 目标URL
        wait_time: Playwright等待JS渲染时间（秒）
        force_browser: True则跳过检测，直接用Playwright
        timeout: 请求超时（秒）

    Returns:
        Tuple[content, title, source]
        - content: 页面文本内容
        - title: 页面标题
        - source: 'playwright' | 'webfetch' | 'error'

    Usage:
        content, title, source = auto_fetch("https://help.aliyun.com/doc/123")
        print(f"从 {source} 获取，标题: {title}")
    """
    spa_sites = _load_spa_sites()

    # 策略1: 已知SPA站点，直接用Playwright
    if _is_known_spa(url, spa_sites):
        content, title = _fetch_with_playwright(url, wait_time, timeout)
        return content, title, 'playwright'

    # 策略2: 强制浏览器模式
    if force_browser:
        content, title = _fetch_with_playwright(url, wait_time, timeout)
        return content, title, 'playwright'

    # 策略3: 先用web_fetch快速检测
    html, status_code = _quick_fetch(url)

    if status_code != 200:
        # HTTP错误，回退到Playwright
        content, title = _fetch_with_playwright(url, wait_time, timeout)
        return content, title, 'playwright'

    # 检测是否为JS渲染页
    if _detect_spa_from_html(html, spa_sites):
        # 切换Playwright渲染
        content, title = _fetch_with_playwright(url, wait_time, timeout)
        return content, title, 'playwright'

    # 普通页面，用web_fetch完整获取
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            }
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            full_html = resp.read(1024 * 1024).decode('utf-8', errors='ignore')

        # 提纯文本
        text = _extract_text_from_html(full_html)

        # 提标题
        title_match = re.search(r'<title>([^<]+)</title>', full_html, re.I)
        title = title_match.group(1).strip() if title_match else ''

        return text, title, 'webfetch'
    except Exception as e:
        # web_fetch失败，fallback到Playwright
        content, title = _fetch_with_playwright(url, wait_time, timeout)
        return content, title, 'playwright'


def _fetch_with_playwright(url: str, wait_time: float = 3.0, timeout: int = 30) -> Tuple[str, str]:
    """
    使用Playwright获取页面内容

    Returns:
        Tuple[content, title]
    """
    from playwright.sync_api import sync_playwright

    try:
        pw = sync_playwright().start()
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        )
        page = context.new_page()

        page.goto(url, wait_until='networkidle', timeout=timeout * 1000)

        # 等待JS渲染
        import time
        time.sleep(wait_time)

        title = page.title()
        content = page.locator('body').inner_text()

        browser.close()
        pw.stop()

        return content, title
    except Exception as e:
        return f"Playwright Error: {e}", ""


def _extract_text_from_html(html: str) -> str:
    """从HTML中提取纯文本"""
    # 移除script和style
    text = re.sub(r'<script[^>]*>[\s\S]*?</script>', '', html, flags=re.I)
    text = re.sub(r'<style[^>]*>[\s\S]*?</style>', '', text, flags=re.I)
    # 移除注释
    text = re.sub(r'<!--[\s\S]*?-->', '', text)
    # 移除标签
    text = re.sub(r'<[^>]+>', ' ', text)
    # 合并空白
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def auto_fetch_as_item(url: str, **kwargs) -> StructuredItem:
    """
    auto_fetch的StructuredItem版本

    Returns:
        StructuredItem with:
        - url: 原始URL
        - title: 页面标题
        - content: 页面文本
        - platform: 'auto_detected'
        - metadata.source: 'playwright' | 'webfetch'
    """
    content, title, source = auto_fetch(url, **kwargs)

    return StructuredItem(
        platform='auto_detected',
        title=title or url,
        url=url,
        content=content,
        metadata={
            'source': source,
            'collected_at': time.time(),
        }
    )


# ---- CLI ----

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Browser Collector CLI')
    parser.add_argument('command', choices=['collect', 'batch', 'test'])
    parser.add_argument('--url', help='目标URL')
    parser.add_argument('--file', help='URL文件路径')
    parser.add_argument('--adapter', help='适配器名称')
    parser.add_argument('--workers', type=int, default=2, help='并发数')
    parser.add_argument('--wait-selector', help='等待选择器')
    args = parser.parse_args()

    if args.command == 'test':
        print("BrowserCollector initialized successfully")
        return 0

    collector = BrowserCollector()

    if args.command == 'collect':
        if not args.url:
            print("Error: --url required")
            return 1
        item = collector.collect(args.url, adapter=args.adapter,
                               wait_selector=args.wait_selector)
        print(f"Title: {item.title}")
        print(f"URL: {item.url}")
        print(f"Content (first 500 chars):")
        print(item.content[:500] if item.content else "(empty)")
        collector.close()
        return 0

    if args.command == 'batch':
        if not args.file:
            print("Error: --file required")
            return 1

        urls = []
        with open(args.file, 'r') as f:
            urls = [line.strip() for line in f
                    if line.strip() and not line.startswith('#')]

        print(f"Loaded {len(urls)} URLs")

        with collector.batch(max_workers=args.workers) as batch:
            def progress(done, total):
                print(f"Progress: {done}/{total}")

            items = batch.collect_urls(urls, progress_callback=progress)
            print(f"\nDone! Collected {len(items)} items")

        collector.close()
        return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
