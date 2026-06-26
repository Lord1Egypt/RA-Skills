#!/usr/bin/env python3
"""
Universal Web Crawler - 集成Crawl4AI
支持: crawl4ai (优先) / playwright / requests
"""

import os
import sys
import time
import random
import hashlib
import re
import json
import html
import argparse
import asyncio
import nest_asyncio
from datetime import datetime
from urllib.parse import urlparse, urljoin
from pathlib import Path
from typing import Set, List, Dict, Optional, Callable
from dataclasses import dataclass, field, asdict

# 应用 nest_asyncio 以允许在现有事件循环中运行 async 代码
nest_asyncio.apply()

# ==================== 配置 ====================
DEFAULT_DELAY = 3.0
DEFAULT_MAX_PAGES = 50
DEFAULT_MAX_DEPTH = 5
DEFAULT_TIMEOUT = 30
MAX_WORKERS = 3

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
]

DEFAULT_EXCLUDE = [
    r"/video/", r"/audio/", r"/watch/", r"/live/",
    r"/login", r"/register", r"/account", r"/profile",
    r"\.pdf$", r"\.mp3$", r"\.mp4$", r"\.zip$",
    r"/search", r"/cookies", r"/privacy", r"/terms",
    r"/admin", r"/api", r"/cdn/", r"/static/",
]

# ==================== 数据类 ====================
@dataclass
class CrawlConfig:
    """爬取配置"""
    start_url: str = ""
    output_dir: str = "./output"
    max_pages: int = DEFAULT_MAX_PAGES
    max_depth: int = DEFAULT_MAX_DEPTH
    delay: float = DEFAULT_DELAY
    timeout: int = DEFAULT_TIMEOUT
    
    # 域名控制
    allowed_domains: List[str] = field(default_factory=list)
    exclude_patterns: List[str] = field(default_factory=lambda: DEFAULT_EXCLUDE)
    
    # 爬取方式
    method: str = "auto"  # auto, crawl4ai, playwright, requests
    
    # 内容
    min_content_length: int = 100
    download_images: bool = False
    
    # 输出
    format: str = "markdown"  # markdown, json
    
    # 高级
    respect_robots: bool = True


@dataclass
class PageContent:
    """页面内容"""
    url: str
    title: str = ""
    publish_time: str = ""
    author: str = ""
    body: str = ""
    images: List[str] = field(default_factory=list)
    links: List[str] = field(default_factory=list)
    category: str = ""
    meta: Dict = field(default_factory=dict)
    valid: bool = False
    error: str = ""


@dataclass
class CrawlResult:
    """爬取结果"""
    total: int = 0
    success: int = 0
    failed: int = 0
    skipped: int = 0
    start_time: str = ""
    end_time: str = ""
    output_dir: str = ""
    failed_urls: List[Dict] = field(default_factory=list)


# ==================== 工具函数 ====================
def get_domain(url: str) -> str:
    try: return urlparse(url).netloc.replace("www.", "")
    except: return ""

def is_allowed(url: str, allowed: List[str], excluded: List[str]) -> bool:
    domain = get_domain(url)
    if allowed and not any(d in domain for d in allowed):
        return False
    if any(re.search(p, url, re.I) for p in excluded):
        return False
    return True

def compute_hash(content: str) -> str:
    return hashlib.md5(content.encode("utf-8", errors="ignore")).hexdigest()

def clean_text(text: str) -> str:
    """清理HTML标签和空白字符，保留段落结构"""
    if not text:
        return ""
    
    # 替换换行标签为换行符
    text = re.sub(r'<(br|BR|Br|bR)\s*/?>', '\n', text)
    text = re.sub(r'</(p|div|h\d|li|ul|ol|tr|table|blockquote|section|article|header|footer)>', '\n\n', text, flags=re.I)
    
    # 去除所有其他HTML标签
    text = re.sub(r'<[^>]+>', '', text)
    
    # 解码HTML实体
    text = html.unescape(text)
    
    # 规范化空白字符
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join([line for line in lines if line]) # 去除空行
    
    return text

def extract_category(url: str) -> str:
    try:
        path = urlparse(url).path
        parts = [p for p in path.split("/") if p]
        return parts[0] if parts else "unknown"
    except:
        return "unknown"


# ==================== 爬虫类 ====================
class UniversalCrawler:
    """通用爬虫"""
    
    def __init__(self, config: CrawlConfig):
        self.config = config
        self.output_dir = Path(config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 状态
        self.visited: Set[str] = set()
        self.content_hashes: Set[str] = set()
        self.queue: List[tuple] = []
        self.failed: List[Dict] = []
        self.result = CrawlResult(
            start_time=datetime.now().isoformat(),
            output_dir=str(self.output_dir)
        )
        
        # requests可用
        self.requests_available = self._check_requests()
        
        # 检测方法
        self.method = self._detect_method()
        
    def _detect_method(self) -> str:
        """检测可用方法"""
        if self.config.method != "auto":
            return self.config.method
            
        # 1. Crawl4AI (优先)
        try:
            import crawl4ai
            return "crawl4ai"
        except:
            pass

        # 2. Playwright
        try:
            from playwright.sync_api import sync_playwright
            return "playwright"
        except:
            pass
            
        if self.requests_available:
            return "requests"
            
        return "requests" # 默认回退到 requests
    
    def _check_requests(self) -> bool:
        try:
            import requests
            return True
        except:
            return False
    
    # ------ 提取器 ------
    def extract_by_crawl4ai(self, url: str) -> Optional[PageContent]:
        """使用Crawl4AI提取"""
        try:
            from crawl4ai import AsyncWebCrawler
            
            async def _crawl():
                async with AsyncWebCrawler(verbose=False) as crawler:
                    result = await crawler.arun(url=url)
                    return result

            # 在当前事件循环或新循环中运行
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                     # 如果已有循环运行（例如在 Jupyter 或其他 async 环境），使用 nest_asyncio 允许嵌套
                     future = asyncio.ensure_future(_crawl())
                     result = loop.run_until_complete(future)
                else:
                     result = loop.run_until_complete(_crawl())
            except RuntimeError:
                # 如果没有循环，创建一个新的
                result = asyncio.run(_crawl())

            if not result or not result.success:
                error_msg = result.error_message if result else 'No result'
                self.failed.append({"url": url, "error": f"crawl4ai failed: {error_msg}"})
                return None
            
            # 优先使用HTML解析以保持一致性
            html_content = result.html
            
            if not html_content and result.markdown:
                 # 如果只有 Markdown，尝试转换或直接使用（这里简化处理，如果没有HTML则视为失败，保持逻辑一致）
                 pass
                
            if html_content:
                return self._parse_html(html_content, url)
            
            return None
            
        except Exception as e:
            self.failed.append({
                "url": url, 
                "error": f"crawl4ai exception: {str(e)}",
                "time": datetime.now().isoformat()
            })
            return None

    def extract_by_playwright(self, url: str) -> Optional[PageContent]:
        """使用playwright提取"""
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    user_agent=random.choice(USER_AGENTS),
                    viewport={'width': 1920, 'height': 1080}
                )
                page = context.new_page()
                
                try:
                    page.goto(url, timeout=self.config.timeout * 1000, wait_until="domcontentloaded")
                    # 简单等待内容
                    page.wait_for_timeout(3000)
                except:
                    pass
                    
                content = page.content()
                browser.close()
                return self._parse_html(content, url)
                
        except Exception as e:
            self.failed.append({
                "url": url, 
                "error": f"playwright: {str(e)}",
                "time": datetime.now().isoformat()
            })
            return None

    def extract_by_requests(self, url: str) -> Optional[PageContent]:
        """使用requests提取"""
        import requests
        
        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept": "text/html,application/xhtml+xml",
            }
            response = requests.get(url, headers=headers, timeout=self.config.timeout)
            response.raise_for_status()
            response.encoding = response.apparent_encoding or "utf-8"
            
            return self._parse_html(response.text, url)
        except Exception as e:
            self.failed.append({"url": url, "error": str(e)})
            return None
    
    def _parse_html(self, html_str: str, url: str) -> PageContent:
        """解析HTML"""
        content = PageContent(url=url)
        
        if not html_str:
            content.error = "HTML为空"
            return content
            
        if len(html_str) < 500:
            content.error = f"内容过短 ({len(html_str)} chars)"
            return content
        
        # 标题
        for p in [r'<h1[^>]*>([^<]+)</h1>', r'<title>([^<]+)</title>',
                   r'<meta[^>]*property="og:title"[^>]*content="([^"]+)"',
                   r'<meta[^>]*name="twitter:title"[^>]*content="([^"]+)"']:
            m = re.search(p, html_str, re.I)
            if m:
                content.title = m.group(1).strip()
                break
        
        # JSON-LD Title Fallback
        if not content.title:
             m = re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>', html_str)
             if m:
                 try:
                     data = json.loads(m.group(1))
                     if isinstance(data, list): data = data[0]
                     if 'headline' in data: content.title = data['headline']
                     elif 'name' in data: content.title = data['name']
                 except: pass

        # 时间
        m = re.search(r'<time[^>]*datetime="([^"]+)"', html_str, re.I)
        if m: content.publish_time = m.group(1)
        
        # 正文提取
        body_html = self._extract_body_html(html_str)
        content.body = clean_text(body_html)
        
        # 图片 (仅从正文提取)
        if body_html:
            content.images = re.findall(r'<img[^>]+src="(https?://[^"]+)"', body_html)
        else:
            # 降级: 尝试从 main 提取
            m = re.search(r'<main[^>]*>([\s\S]*?)</main>', html_str, re.I)
            if m:
                content.images = re.findall(r'<img[^>]+src="(https?://[^"]+)"', m.group(1))
            else:
                content.images = []
        
        content.images = [i for i in content.images if i.startswith("http")]
        
        # 链接
        raw_links = re.findall(r'<a\s+(?:[^>]*?\s+)?href=["\']([^"\']+)["\']', html_str, re.I)
        links = []
        for link in raw_links:
            if link.startswith(('javascript:', 'mailto:', 'tel:', '#')):
                continue 
            full_link = urljoin(url, link)
            if full_link.startswith("http"):
                links.append(full_link)
        
        content.links = list(set(links))[:50]
        content.category = extract_category(url)
        
        if not content.title:
            content.error = "未找到标题"
        elif len(content.body) <= self.config.min_content_length:
            content.error = f"正文过短 ({len(content.body)} chars)"
        else:
            content.valid = True
            
        return content
    
    def _extract_body_html(self, html_str: str) -> str:
        """提取正文HTML"""
        # 尝试 article
        m = re.search(r'<article[^>]*>([\s\S]*?)</article>', html_str, re.I)
        if m: return m.group(1)
        
        # 尝试 main
        m = re.search(r'<main[^>]*>([\s\S]*?)</main>', html_str, re.I)
        if m: return m.group(1)

        # 尝试常见类名
        for cls in ['content', 'article-body', 'post-content', 'entry-content', 'story-body__inner', 'ssrcss-1r7b75b-MainColumn']:
            m = re.search(rf'<div[^>]*class="[^"]*{cls}[^"]*"[^>]*>([\s\S]*?)</div>', html_str, re.I)
            if m: return m.group(1)
        
        return ""
    
    def _download_image(self, img_url: str, save_dir: Path) -> Optional[str]:
        """下载图片并返回文件名"""
        try:
            import requests
            import mimetypes
            
            img_hash = hashlib.md5(img_url.encode('utf-8')).hexdigest()
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Referer": self.config.start_url
            }
            response = requests.get(img_url, headers=headers, timeout=10)
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '').split(';')[0].strip()
                ext = mimetypes.guess_extension(content_type)
                if not ext:
                    path = urlparse(img_url).path
                    ext = os.path.splitext(path)[1]
                if not ext or len(ext) > 5:
                    ext = ".jpg"
                if ext in ['.jpe', '.jpeg']: ext = '.jpg'
                
                filename = f"{img_hash}{ext}"
                filepath = save_dir / filename
                filepath.write_bytes(response.content)
                return filename
        except:
            pass
        return None
    
    # ------ 保存 ------
    def to_markdown(self, content: PageContent) -> str:
        lines = [
            "---",
            f"title: \"{content.title}\"",
            f"publish_time: {content.publish_time}",
            f"author: {content.author}",
            f"category: {content.category}",
            f"url: {content.url}",
            f"crawl_time: {datetime.now().isoformat()}",
            "---",
            "",
            f"# {content.title}",
            "",
            content.body,
            ""
        ]
        
        if content.images:
            lines.extend(["", "## 图片", ""])
            for i, img in enumerate(content.images, 1):
                lines.append(f"![图片{i}]({img})")
        
        return "\n".join(lines)
    
    def save(self, content: PageContent) -> Optional[Path]:
        if not content.valid:
            return None
        
        h = compute_hash(content.body)
        if h in self.content_hashes:
            self.result.skipped += 1
            return None
        self.content_hashes.add(h)
        
        crawl_date = datetime.now().strftime('%Y-%m-%d')
        category = content.category if content.category and content.category != "unknown" else "uncategorized"
        safe_category = re.sub(r'[^\w\s-]', '', category).strip().replace(" ", "-")
        if not safe_category: safe_category = "uncategorized"
        
        save_dir = self.output_dir / crawl_date / safe_category
        save_dir.mkdir(parents=True, exist_ok=True)

        images_dir = save_dir / "images"
        images_dir.mkdir(exist_ok=True)

        original_images = content.images
        local_images = []
        for img_url in content.images:
            local_name = self._download_image(img_url, images_dir)
            if local_name:
                local_images.append(f"./images/{local_name}")
            else:
                local_images.append(img_url)
        content.images = local_images

        domain = get_domain(content.url)
        safe_title = re.sub(r'[^\w\s-]', '', content.title)[:50].replace(" ", "-")
        timestamp = datetime.now().strftime('%H%M%S')
        filename = f"{domain}_{timestamp}_{safe_title}.md"
        
        filepath = save_dir / filename
        filepath.write_text(self.to_markdown(content), encoding="utf-8")
        
        content.images = original_images
        return filepath
    
    # ------ 爬取 ------
    def should_crawl(self, url: str, depth: int) -> bool:
        url = url.split("#")[0]
        if url in self.visited: return False
        if depth > self.config.max_depth: return False
        if len(self.visited) >= self.config.max_pages: return False
        if not url.startswith("http"): return False
        if not is_allowed(url, self.config.allowed_domains, self.config.exclude_patterns):
            return False
        return True
    
    def crawl_page(self, url: str) -> PageContent:
        """爬取单个页面"""
        if self.method == "crawl4ai":
            content = self.extract_by_crawl4ai(url)
        elif self.method == "playwright":
            content = self.extract_by_playwright(url)
        elif self.method == "requests":
            content = self.extract_by_requests(url)
        else:
            # Auto
            content = self.extract_by_crawl4ai(url)
            if not content or not content.valid:
                content = self.extract_by_playwright(url)
            if not content or not content.valid:
                content = self.extract_by_requests(url)
        
        return content or PageContent(url=url, valid=False, error=f"方法 {self.method} 失败")
    
    def run(self) -> CrawlResult:
        print("=" * 60)
        print("Universal Web Crawler (Crawl4AI Edition)")
        print("=" * 60)
        print(f"起始: {self.config.start_url}")
        print(f"方法: {self.method}")
        print(f"最大: {self.config.max_pages}页, 深度{self.config.max_depth}")
        print(f"输出: {self.output_dir}")
        print("")
        
        self.queue.append((self.config.start_url, 0))
        
        while self.queue and self.result.total < self.config.max_pages:
            self.queue.sort(key=lambda x: x[1])
            url, depth = self.queue.pop(0)
            
            if not self.should_crawl(url, depth):
                continue
            
            url = url.split("#")[0]
            self.visited.add(url)
            
            print(f"[{self.result.total + 1}/{self.config.max_pages}] ", end="")
            print(f"D{depth}: {url[:45]}...", end=" ")
            
            content = self.crawl_page(url)
            
            if content.valid:
                filepath = self.save(content)
                if filepath:
                    self.result.success += 1
                    try:
                        rel_path = filepath.relative_to(self.output_dir)
                        print(f"✓ {rel_path}")
                    except:
                        print(f"✓ {filepath.name}")
                    
                    if depth < self.config.max_depth:
                        for link in content.links:
                            if self.should_crawl(link, depth + 1):
                                self.queue.append((link, depth + 1))
                else:
                    self.result.skipped += 1
                    print("⊘ 跳过")
            else:
                self.result.failed += 1
                print(f"✗ {content.error or '失败'}")
                self.failed.append({
                    "url": url, 
                    "error": content.error or "失败",
                    "time": datetime.now().isoformat()
                })
            
            self.result.total += 1
            time.sleep(random.uniform(self.config.delay * 0.8, self.config.delay * 1.2))
        
        if self.failed:
            (self.output_dir / "failed_urls.txt").write_text(
                "\n".join(f"{f.get('time', '')}\t{f['url']}\t{f.get('error', '')}" for f in self.failed),
                encoding="utf-8"
            )
        
        self.result.end_time = datetime.now().isoformat()
        
        print("")
        print("=" * 60)
        print("完成!")
        print(f"成功: {self.result.success}, 失败: {self.result.failed}, 跳过: {self.result.skipped}")
        
        return self.result


def main():
    parser = argparse.ArgumentParser(description="Universal Web Crawler")
    parser.add_argument("--url", "-u", required=True)
    parser.add_argument("--output", "-o", default="./output")
    parser.add_argument("--max-pages", "-m", type=int, default=DEFAULT_MAX_PAGES)
    parser.add_argument("--depth", "-d", type=int, default=DEFAULT_MAX_DEPTH)
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY)
    parser.add_argument("--method", choices=["auto", "requests", "crawl4ai", "playwright"], default="auto")
    parser.add_argument("--domains", help="允许域名,逗号分隔")
    
    args = parser.parse_args()
    
    config = CrawlConfig(
        start_url=args.url,
        output_dir=args.output,
        max_pages=args.max_pages,
        max_depth=args.depth,
        delay=args.delay,
        method=args.method
    )
    
    if args.domains:
        config.allowed_domains = [d.strip() for d in args.domains.split(",")]
    else:
        config.allowed_domains = [get_domain(args.url)]
    
    crawler = UniversalCrawler(config)
    result = crawler.run()
    
    print(f"\n结果: {result.output_dir}")
    return result


if __name__ == "__main__":
    main()
