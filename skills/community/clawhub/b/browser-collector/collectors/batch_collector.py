#!/usr/bin/env python3
"""
collectors/batch_collector.py - 批量采集 + 多进程Session隔离

架构：
- BatchCollector: 批量URL采集器（ThreadPoolExecutor控制并发）
- SessionManager: 多进程Session隔离（每个目标站点独立BrowserContext）
- ProcessWorker: 独立进程 worker（非线程，真正的多进程）

性能考虑：
- 多进程隔离：每个 worker 进程有独立的 Playwright 实例 + 独立内存空间
- 线程池协调：主进程用 ThreadPoolExecutor 分发任务，不直接运行 Playwright
- Cookie 隔离：通过 SQLite 数据库共享（cookie_db.py），各进程独立读写
- 代理隔离：每个 worker 维护自己的代理连接

与 base.py 的 StructuredItem 兼容：
    采集结果 → StructuredItem.from_dict() 转换
"""

import os
import sys
import time
import json
import multiprocessing as mp
from multiprocessing import Process, Queue, Manager, Value
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Callable, Dict, Any, Union
from urllib.parse import urlparse
from pathlib import Path
from queue import Empty
import ctypes

# 路径处理
sys.path.insert(0, str(Path(__file__).parent.parent))

from collectors.base import StructuredItem, items_to_dict_list

# Playwright - 仅在子进程中导入（避免主进程加载开销）
_playwright = None
_BrowserCollector = None


# ==================== SessionManager ====================

class SessionManager:
    """
    Session 隔离管理器

    功能：
    1. 按域名隔离 BrowserContext（防止跨域Cookie污染）
    2. 自动注入反检测脚本
    3. 支持 Cookie 持久化（通过 cookie_db.py）
    4. 自动保存/恢复 Session

    与 browser/playwright.py 的 BrowserPlaywright 配合使用

    Usage:
        sm = SessionManager()
        context = sm.get_session('github.com')  # 获取/创建独立Session
        page = context.new_page()
        # ... 使用 page ...
        sm.save_session('github.com')  # 保存Cookie
        sm.close_all()  # 关闭所有Session
    """

    def __init__(self, cookie_db_path: str = None,
                 screenshot_dir: str = None,
                 stealth: bool = True):
        from pathlib import Path
        base = Path.home() / ".openclaw"

        self.cookie_db_path = cookie_db_path or str(base / "data" / "cookies.db")
        self.screenshot_dir = screenshot_dir or str(base / "screenshots")
        self.stealth = stealth

        self.sessions: Dict[str, Any] = {}  # domain → BrowserContext
        self._pw = None
        self._browser = None

        Path(self.cookie_db_path).parent.mkdir(parents=True, exist_ok=True)
        Path(self.screenshot_dir).mkdir(parents=True, exist_ok=True)

    def _ensure_browser(self):
        """延迟初始化浏览器（仅在第一次需要时）"""
        if self._browser is not None:
            return

        global _playwright
        if _playwright is None:
            from playwright.sync_api import sync_playwright as _playwright

        self._pw = _playwright.start()
        self._browser = self._pw.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-first-run',
                '--disable-gpu',
                '--no-sandbox',
            ]
        )

    def _get_stealth_script(self) -> str:
        """生成反检测JS"""
        return '''
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined, configurable: true});
        Object.defineProperty(navigator, 'plugins', {
            get: () => [{name:'Chrome PDF Plugin'},{name:'Chrome PDF Viewer'},{name:'Native Client'}],
            configurable: true
        });
        Object.defineProperty(navigator, 'languages', {
            get: () => ['zh-CN', 'zh', 'en-US', 'en'],
            configurable: true
        });
        delete window.__webdriver_evaluate;
        delete window.__selenium_evaluate;
        '''

    def get_session(self, domain: str, load_cookies: bool = True):
        """
        获取指定域名的独立Session（BrowserContext）

        如果已存在则复用
        如果不存在则创建新的

        Args:
            domain: 目标域名（如 'github.com'）
            load_cookies: 是否从数据库加载已有Cookie

        Returns:
            BrowserContext
        """
        if domain in self.sessions:
            return self.sessions[domain]

        self._ensure_browser()

        # 尝试加载持久化的Cookie
        context_cookies = []
        if load_cookies:
            try:
                from collectors.cookie_db import CookieDatabase
                db = CookieDatabase(self.cookie_db_path)
                db_cookies = db.get_cookies(domain)
                context_cookies = [
                    {
                        'name': c['name'],
                        'value': c['value'],
                        'domain': c['domain'],
                        'path': c['path'],
                        'expires': c.get('expires', -1),
                        'httpOnly': c.get('httpOnly', False),
                        'secure': c.get('secure', False),
                    }
                    for c in db_cookies
                ]
            except Exception as e:
                print(f"[SessionManager] Failed to load cookies for {domain}: {e}")

        context = self._browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='zh-CN',
            ignore_https_errors=True,
        )

        # 反检测
        if self.stealth:
            context.add_init_script(self._get_stealth_script())

        # 注入Cookie
        if context_cookies:
            try:
                context.add_cookies(context_cookies)
            except Exception as e:
                print(f"[SessionManager] Failed to add cookies: {e}")

        self.sessions[domain] = context
        return context

    def save_session(self, domain: str):
        """将Session的Cookie保存到数据库"""
        if domain not in self.sessions:
            return

        try:
            from collectors.cookie_db import CookieDatabase
            cookies = self.sessions[domain].cookies()
            db = CookieDatabase(self.cookie_db_path)
            db.save_cookies(cookies, domain)
        except Exception as e:
            print(f"[SessionManager] Failed to save cookies for {domain}: {e}")

    def close_session(self, domain: str):
        """关闭并保存单个Session"""
        if domain in self.sessions:
            self.save_session(domain)
            self.sessions[domain].close()
            del self.sessions[domain]

    def close_all(self):
        """关闭所有Session并清理浏览器"""
        for domain in list(self.sessions.keys()):
            self.close_session(domain)

        if self._browser:
            self._browser.close()
            self._browser = None
        if self._pw:
            self._pw.stop()
            self._pw = None


# ==================== BatchCollector ====================

ALLOWED_SCHEMES = {'http', 'https'}


def _validate_url(url: str) -> str:
    """验证URL协议和白名单"""
    parsed = urlparse(url)
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}. Only http/https allowed.")
    if not parsed.netloc:
        raise ValueError(f"Invalid URL (no netloc): {url}")
    return url


@dataclass
class CollectTask:
    """采集任务"""
    task_id: str
    url: str
    domain: str
    priority: int = 0

    @classmethod
    def make(cls, url: str, task_id: str = None, priority: int = 0) -> 'CollectTask':
        url = _validate_url(url)
        parsed = urlparse(url)
        return cls(
            task_id=task_id or str(hash(url))[:12],
            url=url,
            domain=parsed.netloc,
            priority=priority,
        )


@dataclass
class CollectResult:
    """采集结果"""
    task_id: str
    url: str
    success: bool
    item: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    elapsed_ms: float = 0.0

    def to_item(self) -> Optional[StructuredItem]:
        if self.item:
            return StructuredItem.from_dict(self.item)
        return None


class BatchCollector:
    """
    批量采集器

    特性：
    1. 多线程并发控制（ThreadPoolExecutor，max_workers控制并发数）
    2. 按域名分组，同一域名单线程访问（避免Session冲突）
    3. 进度回调
    4. 自动去重（已访问URL记录）
    5. 与StructuredItem完全兼容

    Usage:
        collector = BrowserCollector()  # 你的采集器实例
        batch = BatchCollector(collector, max_workers=2)

        def handler(page, url) -> StructuredItem:
            page.goto(url)
            return StructuredItem(title=page.title(), url=url, platform='test')

        def progress(done, total):
            print(f"Progress: {done}/{total}")

        results = batch.collect_urls(urls, handler=handler, progress_callback=progress)
        batch.close()
    """

    def __init__(self,
                 collector=None,
                 max_workers: int = 2,
                 max_per_domain: int = 50,
                 cookie_db_path: str = None):
        """
        Args:
            collector: 可选的采集器实例（如果有的话）
            max_workers: 最大并发数
            max_per_domain: 每个域名的最大URL数
            cookie_db_path: Cookie数据库路径
        """
        self.collector = collector
        self.max_workers = max_workers
        self.max_per_domain = max_per_domain
        self.cookie_db_path = cookie_db_path

        self.visited: set = set()
        self.failed: List[Dict] = []
        self.results: List[Dict] = []
        self.session_manager: Optional[SessionManager] = None

        self._executor: Optional[ThreadPoolExecutor] = None
        self._running = False

    def _get_session_manager(self) -> SessionManager:
        if self.session_manager is None:
            self.session_manager = SessionManager(cookie_db_path=self.cookie_db_path)
        return self.session_manager

    def collect_urls(self,
                     urls: List[str],
                     handler: Callable[[Any, str], Dict[str, Any]] = None,
                     progress_callback: Callable[[int, int], None] = None,
                     timeout_per_url: float = 60.0) -> Dict[str, Any]:
        """
        批量采集URL

        Args:
            urls: URL列表
            handler: 自定义处理函数，签名为 (page, url) → dict
                     如果为None，使用默认采集逻辑
            progress_callback: 进度回调，签名为 (completed, total) → None
            timeout_per_url: 每个URL的超时时间（秒）

        Returns:
            Dict: {
                'results': [CollectResult, ...],
                'failed': [{url, error}, ...],
                'total': int,
                'succeeded': int
            }
        """
        self._running = True

        # 去重 + 按域名分组
        from collections import defaultdict
        by_domain: Dict[str, List[str]] = defaultdict(list)

        for url in urls:
            try:
                url = _validate_url(url)
            except ValueError:
                continue
            if url in self.visited:
                continue
            domain = urlparse(url).netloc
            if len(by_domain[domain]) >= self.max_per_domain:
                continue
            by_domain[domain].append(url)
            self.visited.add(url)

        all_urls = [u for urls in by_domain.values() for u in urls]
        total = len(all_urls)
        completed = 0
        results: List[CollectResult] = []

        # 使用 ThreadPoolExecutor 进行并发控制
        self._executor = ThreadPoolExecutor(max_workers=self.max_workers)

        futures = {}
        for domain, domain_urls in by_domain.items():
            for url in domain_urls:
                future = self._executor.submit(
                    self._collect_one,
                    url,
                    handler,
                    timeout_per_url
                )
                futures[future] = (domain, url)

        for future in as_completed(futures):
            domain, url = futures[future]
            try:
                result = future.result(timeout=timeout_per_url)
            except Exception as e:
                result = CollectResult(
                    task_id=str(hash(url))[:12],
                    url=url,
                    success=False,
                    error=str(e)
                )

            results.append(result)
            if result.success:
                self.results.append(asdict(result))
            else:
                self.failed.append({'url': url, 'error': result.error})

            completed += 1
            if progress_callback:
                try:
                    progress_callback(completed, total)
                except Exception:
                    pass

            if not self._running:
                break

        self._executor.shutdown(wait=False)
        self._executor = None

        return {
            'results': results,
            'failed': self.failed,
            'total': total,
            'succeeded': len([r for r in results if r.success])
        }

    def _collect_one(self,
                     url: str,
                     handler: Callable[[Any, str], Dict[str, Any]],
                     timeout: float) -> CollectResult:
        """在独立线程中采集单个URL"""
        start = time.time()
        task_id = str(hash(url))[:12]
        domain = urlparse(url).netloc

        try:
            sm = self._get_session_manager()
            context = sm.get_session(domain)
            page = context.new_page()

            try:
                if handler:
                    data = handler(page, url)
                else:
                    page.goto(url, wait_until='networkidle', timeout=int(timeout * 1000))
                    data = {
                        'title': page.title(),
                        'url': page.url,
                        'content': page.locator('body').inner_text()[:5000],
                    }

                # 保存Cookie
                sm.save_session(domain)

                return CollectResult(
                    task_id=task_id,
                    url=url,
                    success=True,
                    item=data,
                    elapsed_ms=(time.time() - start) * 1000
                )
            finally:
                page.close()
                context.close()

        except Exception as e:
            return CollectResult(
                task_id=task_id,
                url=url,
                success=False,
                error=str(e),
                elapsed_ms=(time.time() - start) * 1000
            )

    def collect_urls_as_items(self,
                               urls: List[str],
                               handler: Callable[[Any, str], StructuredItem] = None,
                               progress_callback: Callable[[int, int], None] = None) -> List[StructuredItem]:
        """
        collect_urls 的 StructuredItem 版本

        返回 List[StructuredItem]，直接兼容 base.py
        """
        def wrapper(page, url):
            result = handler(page, url) if handler else None
            if result is None:
                page.goto(url, wait_until='networkidle', timeout=30000)
                result = StructuredItem(
                    title=page.title(),
                    url=url,
                    platform='batch',
                )
            if isinstance(result, StructuredItem):
                return result.to_dict()
            return result

        raw_results = self.collect_urls(urls, handler=wrapper, progress_callback=progress_callback)
        return [r.to_item() for r in raw_results['results'] if r.to_item()]

    def stop(self):
        """停止采集"""
        self._running = False

    def close(self):
        """关闭所有资源"""
        self._running = False
        if self._executor:
            self._executor.shutdown(wait=False)
        if self.session_manager:
            self.session_manager.close_all()

    def get_statistics(self) -> Dict[str, Any]:
        """获取采集统计信息"""
        return {
            'total_visited': len(self.visited),
            'total_results': len(self.results),
            'total_failed': len(self.failed),
            'max_workers': self.max_workers,
        }

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


# ==================== ProcessWorker（独立进程模式） ====================

def _process_worker_fn(worker_id: int,
                       task_queue: Queue,
                       result_queue: Queue,
                       cookie_db_path: str,
                       stealth: bool):
    """
    独立进程 worker 函数

    每个进程有独立的 Playwright 实例，完全隔离
    通过 Queue 与主进程通信

    Args:
        worker_id: Worker编号
        task_queue: 任务队列（输入）
        result_queue: 结果队列（输出）
        cookie_db_path: Cookie数据库路径
        stealth: 是否启用反检测
    """
    from playwright.sync_api import sync_playwright
    from collectors.cookie_db import CookieDatabase

    browser = None
    pw = None

    try:
        pw = sync_playwright().start()
        browser = pw.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-first-run',
                '--disable-gpu',
                '--no-sandbox',
            ]
        )

        stealth_script = '''
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'plugins', {
            get: () => [{name:'Chrome PDF Plugin'},{name:'Chrome PDF Viewer'}],
            configurable: true
        });
        Object.defineProperty(navigator, 'languages', {
            get: () => ['zh-CN', 'zh', 'en-US', 'en'],
            configurable: true
        });
        '''

        db = CookieDatabase(cookie_db_path)

        while True:
            try:
                task = task_queue.get(timeout=5)
            except Empty:
                continue

            if task is None:  # 终止信号
                break

            task_id = task.get('task_id', '')
            url = task.get('url', '')
            domain = urlparse(url).netloc if url else ''
            start = time.time()

            try:
                # 获取/创建该域名的独立Context
                context = browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36',
                    viewport={'width': 1920, 'height': 1080},
                    ignore_https_errors=True,
                )
                if stealth:
                    context.add_init_script(stealth_script)

                # 加载Cookie
                cookies = db.get_cookies(domain)
                if cookies:
                    context.add_cookies([
                        {'name': c['name'], 'value': c['value'],
                         'domain': c['domain'], 'path': c['path']}
                        for c in cookies
                    ])

                page = context.new_page()
                page.goto(url, wait_until='networkidle', timeout=30000)

                result = {
                    'task_id': task_id,
                    'url': url,
                    'success': True,
                    'title': page.title(),
                    'content_length': len(page.content()),
                    'elapsed_ms': (time.time() - start) * 1000,
                }

                # 保存Cookie
                new_cookies = context.cookies()
                db.save_cookies(new_cookies, domain)

                page.close()
                context.close()

            except Exception as e:
                result = {
                    'task_id': task_id,
                    'url': url,
                    'success': False,
                    'error': str(e),
                    'elapsed_ms': (time.time() - start) * 1000,
                }

            result_queue.put(result)

    except Exception as e:
        result_queue.put({'worker_error': str(e)})

    finally:
        if browser:
            browser.close()
        if pw:
            pw.stop()


class ProcessBatchCollector:
    """
    多进程批量采集器

    与 BatchCollector 的区别：
    - BatchCollector: 多线程（共享同一进程内存）
    - ProcessBatchCollector: 多进程（真正的进程隔离，适合大规模采集）

    使用场景：
    - 大规模数据采集（>100 URLs）
    - 目标站点有强反爬（进程隔离防关联）
    - 需要长时间运行（进程隔离，防内存泄漏）

    Usage:
        collector = ProcessBatchCollector(max_workers=2)
        for url in urls:
            collector.submit_task(url)
        collector.start()  # 启动worker进程
        # ...
        for result in collector.iter_results():
            print(result)
        collector.stop()
    """

    def __init__(self,
                 max_workers: int = 2,
                 cookie_db_path: str = None,
                 stealth: bool = True):
        self.max_workers = max_workers
        self.cookie_db_path = cookie_db_path or str(Path.home() / ".openclaw" / "data" / "cookies.db")
        self.stealth = stealth

        self._task_queue: Optional[Queue] = None
        self._result_queue: Optional[Queue] = None
        self._processes: List[Process] = []
        self._running = False

    def start(self):
        """启动所有worker进程"""
        if self._running:
            return

        self._task_queue = Queue()
        self._result_queue = Queue()
        self._running = True

        for i in range(self.max_workers):
            p = Process(
                target=_process_worker_fn,
                args=(i, self._task_queue, self._result_queue,
                      self.cookie_db_path, self.stealth)
            )
            p.start()
            self._processes.append(p)

    def submit_task(self, url: str, task_id: str = None):
        """提交采集任务"""
        if not self._running:
            self.start()
        self._task_queue.put({
            'task_id': task_id or str(hash(url))[:12],
            'url': url,
        })

    def submit_tasks(self, tasks: List[Dict]):
        """批量提交任务"""
        for t in tasks:
            self._task_queue.put(t)

    def iter_results(self, timeout: float = 5.0):
        """迭代获取结果（非阻塞）"""
        while self._running:
            try:
                result = self._result_queue.get(timeout=timeout)
                yield result
            except Empty:
                continue

    def get_result(self, timeout: float = None) -> Optional[Dict]:
        """获取单个结果（阻塞）"""
        try:
            return self._result_queue.get(timeout=timeout)
        except Empty:
            return None

    def stop(self):
        """停止所有worker"""
        self._running = False

        # 发送终止信号
        for _ in range(self.max_workers):
            self._task_queue.put(None)

        # 等待进程结束
        for p in self._processes:
            p.join(timeout=10)
            if p.is_alive():
                p.terminate()

        self._processes.clear()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()


# ---- CLI Entrance ----

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Batch Collector CLI')
    parser.add_argument('command', choices=['collect', 'batch', 'test'])
    parser.add_argument('--url', help='单个URL（collect命令）')
    parser.add_argument('--file', help='URL文件路径（batch命令）')
    parser.add_argument('--adapter', default='browser', help='适配器名称')
    parser.add_argument('--workers', type=int, default=2, help='并发数')
    parser.add_argument('--limit', type=int, default=50, help='每个域名最大URL数')
    args = parser.parse_args()

    if args.command == 'test':
        print(f"max_workers: {args.workers}")
        print(f"cookie_db: {Path.home() / '.openclaw' / 'data' / 'cookies.db'}")
        return 0

    if args.command == 'collect':
        if not args.url:
            print("Error: --url required for collect command")
            return 1
        batch = BatchCollector(max_workers=args.workers)
        results = batch.collect_urls([args.url])
        print(json.dumps(results, indent=2, ensure_ascii=False))
        batch.close()
        return 0

    if args.command == 'batch':
        if not args.file:
            print("Error: --file required for batch command")
            return 1

        urls = []
        with open(args.file, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        print(f"Loaded {len(urls)} URLs, starting batch collect...")
        batch = BatchCollector(max_workers=args.workers, max_per_domain=args.limit)

        def progress(done, total):
            print(f"Progress: {done}/{total} ({done*100//total}%)")

        results = batch.collect_urls(urls, progress_callback=progress)
        print(f"\nDone! Succeeded: {results['succeeded']}/{results['total']}")
        batch.close()
        return 0


if __name__ == '__main__':
    sys.exit(main())
