"""
babata_browser.py — 巴巴塔浏览器控制工具
基于 Playwright/CloakBrowser 的轻量浏览器自动化，用自然语言控制浏览器操作
零额外AI依赖，比 browser-use 轻 50+ 个包

Backend: CloakBrowser (default) → Playwright (fallback)
  CloakBrowser: C++ 级 Chromium 反检测，30/30 bot 测试通过，reCAPTCHA v3 0.9
  迁移自 Playwright 仅需一行改动
"""
import sys, os, json, re
from datetime import datetime

# ── Backend Detection ───────────────────────────────────
_CLOAKBROWSER_AVAILABLE = False
_cloak_launch = None
_get_stealth_args = None
try:
    from cloakbrowser import launch as _cloak_launch
    from cloakbrowser import get_default_stealth_args as _get_stealth_args
    _CLOAKBROWSER_AVAILABLE = True
except ImportError:
    pass

# Always import Playwright as fallback
from playwright.sync_api import sync_playwright


class BabataBrowser:
    def __init__(self, headless=True, backend='auto'):
        """
        backend: 'auto' (优先CloakBrowser) | 'cloakbrowser' | 'playwright'
        """
        self.headless = headless
        self.backend = backend
        self.playwright = None
        self.browser = None
        self._using_cloak = False
    
    def start(self):
        use_cloak = (
            (self.backend == 'auto' and _CLOAKBROWSER_AVAILABLE) or
            self.backend == 'cloakbrowser'
        )
        
        if use_cloak and _CLOAKBROWSER_AVAILABLE:
            self._using_cloak = True
            # CloakBrowser: C++ 级反检测 Chromium，30/30 测试通过
            # 对政府网站(中纪委/卫健委)CloudFlare/爬虫检测有显著提升
            self.browser = _cloak_launch(headless=self.headless)
        else:
            self._using_cloak = False
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(
                headless=self.headless,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
        return self
    
    def new_page(self):
        return self.browser.new_page()
    
    def stop(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        # CloakBrowser manages its own lifecycle, no explicit stop needed
    
    # ── Actions ──────────────────────────────────────────
    def goto(self, page, url, timeout=30000):
        """Navigate to URL"""
        page.goto(url, timeout=timeout)
        return f"OK: {page.title()[:80]}"
    
    def get_text(self, page, selector=None):
        """Get page text content"""
        if selector:
            el = page.query_selector(selector)
            return el.inner_text()[:5000] if el else 'Element not found'
        return page.inner_text('body')[:5000]
    
    def get_html(self, page, selector='body'):
        """Get HTML content"""
        el = page.query_selector(selector)
        return el.inner_html()[:10000] if el else ''
    
    def click(self, page, text=None, selector=None):
        """Click element by text match or CSS selector"""
        if text:
            el = page.get_by_text(text, exact=False).first
        elif selector:
            el = page.locator(selector).first
        else:
            return 'Need text or selector'
        if el: el.click(timeout=5000)
        return f"Clicked: {text or selector}"
    
    def fill(self, page, selector, value):
        """Fill input field"""
        el = page.locator(selector).first
        el.fill(value)
        return f"Filled {selector} with: {value[:50]}"
    
    def get_links(self, page, limit=20):
        """Get all links on page"""
        links = []
        for a in page.locator('a').all()[:limit]:
            try:
                href = a.get_attribute('href')
                text = a.inner_text().strip()[:80]
                if href and text:
                    links.append({'text': text, 'href': href})
            except: pass
        return links
    
    def screenshot(self, page, path=None):
        """Take screenshot"""
        if not path:
            path = f'babata_screenshot_{datetime.now().strftime("%H%M%S")}.png'
        page.screenshot(path=path, full_page=True)
        return f'Screenshot saved: {path}'
    
    def scroll(self, page, times=3):
        """Scroll down the page"""
        for _ in range(times):
            page.evaluate('window.scrollBy(0, window.innerHeight)')
            page.wait_for_timeout(500)
        return f'Scrolled {times} times'
    
    def wait(self, page, ms=2000):
        page.wait_for_timeout(ms)
        return f'Waited {ms}ms'
    
    def execute_js(self, page, code):
        """Execute JavaScript"""
        result = page.evaluate(code)
        return str(result)[:5000]
    
    # ── Compound Actions ─────────────────────────────────
    def extract_table(self, page, selector='table'):
        """Extract table data as list of dicts"""
        tables = page.locator(selector).all()
        if not tables:
            return []
        results = []
        for table in tables[:3]:
            rows = table.locator('tr').all()
            if not rows: continue
            headers = [h.inner_text().strip() for h in rows[0].locator('th,td').all()]
            for row in rows[1:]:
                cells = [c.inner_text().strip() for c in row.locator('td').all()]
                if cells and headers:
                    results.append(dict(zip(headers[:len(cells)], cells)))
        return results
    
    def search_and_extract(self, page, query, input_selector='input[type="text"], input[type="search"], input[name="q"], textarea[name="q"]'):
        """Type a query and submit the search form"""
        el = page.locator(input_selector).first
        if el:
            el.fill(query)
            el.press('Enter')
            page.wait_for_timeout(3000)
            return self.get_text(page)[:3000]
        return 'No search input found'
    
    def login_if_needed(self, page, username, password, user_sel='input[type="email"], input[name="username"]', pass_sel='input[type="password"]', submit_sel='button[type="submit"]'):
        """Attempt login"""
        u = page.locator(user_sel).first
        p = page.locator(pass_sel).first
        s = page.locator(submit_sel).first
        if u and p:
            u.fill(username)
            p.fill(password)
            s.click()
            page.wait_for_timeout(3000)
            return 'Login attempted'
        return 'No login form detected'


# ── Natural Language Interface ──────────────────────────
def execute_task(task_desc, headless=True):
    """
    用自然语言描述浏览器任务。
    
    Usage:
        result = execute_task("打开卫健委官网，找到最新政策标题，提取前5条")
        result = execute_task("打开 https://example.com，搜索 医疗AI，返回搜索结果")
    """
    browser = BabataBrowser(headless=headless)
    browser.start()
    page = browser.new_page()
    
    result = {
        'task': task_desc,
        'steps': [],
        'data': None,
        'error': None
    }
    
    try:
        # Parse URL from task
        urls = re.findall(r'https?://[^\s，,]+', task_desc)
        if urls:
            step = browser.goto(page, urls[0])
            result['steps'].append(step)
        
        # Detect search intent
        if '搜索' in task_desc or 'search' in task_desc.lower():
            query = re.search(r'搜索[：:]\s*(.+?)(?:[,，\s]|$)', task_desc)
            if query:
                q = query.group(1)
                result['data'] = browser.search_and_extract(page, q)
                result['steps'].append(f'Searched: {q}')
        
        # Extract text
        if '提取' in task_desc or '获取' in task_desc or '抓取' in task_desc:
            if '链接' in task_desc:
                result['data'] = browser.get_links(page)
                result['steps'].append(f'Got {len(result["data"])} links')
            elif '表格' in task_desc:
                result['data'] = browser.extract_table(page)
                result['steps'].append(f'Got {len(result["data"])} table rows')
            else:
                result['data'] = browser.get_text(page)
                result['steps'].append(f'Got text ({len(result["data"])} chars)')
        
        # Screenshot
        if '截图' in task_desc or 'screenshot' in task_desc.lower():
            result['data'] = browser.screenshot(page)
            result['steps'].append('Screenshot taken')
        
        # Scroll
        if '滚动' in task_desc or '翻页' in task_desc:
            browser.scroll(page, 3)
            result['steps'].append('Scrolled')
            result['data'] = browser.get_text(page)
        
    except Exception as e:
        result['error'] = str(e)
    finally:
        browser.stop()
    
    return result


# ── CLI ──────────────────────────────────────────────────
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Babata Browser - Natural language browser control')
    parser.add_argument('task', nargs='?', help='Task description in Chinese')
    parser.add_argument('--headless', type=bool, default=True)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    
    if not args.task:
        print("Usage: python babata_browser.py '打开卫健委官网，提取最新政策标题'")
        print("")
        print("Quick test:")
        result = execute_task('打开 https://example.com，提取页面文字')
        print(f'  Test result: {result["steps"]}')
    else:
        result = execute_task(args.task, headless=args.headless)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f'Task: {result["task"]}')
            print(f'Steps: {result["steps"]}')
            if result['data']:
                data_str = str(result['data'])
                print(f'Data: {data_str[:500]}')
            if result['error']:
                print(f'Error: {result["error"]}')
