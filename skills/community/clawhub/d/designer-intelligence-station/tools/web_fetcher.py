#!/usr/bin/env python3
"""
设计师情报站 - 网页抓取器

功能：
- 批量抓取网页内容（通过 web_fetch 工具）
- 智能解析 HTML 提取标题、链接、摘要
- 支持多个媒体网站结构
- 结果缓存

使用方式:
    python web_fetcher.py fetch <source_id>      # 抓取单个源
    python web_fetcher.py fetch-all              # 抓取所有网页源
    python web_fetcher.py parse <html_file>      # 解析 HTML 文件
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict

# 添加父目录到路径，导入 sources_manager
sys.path.insert(0, str(Path(__file__).parent))
from sources_manager import get_enabled_sources, get_source

# 缓存目录
CACHE_DIR = Path(__file__).parent.parent / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


class WebItem:
    """网页抓取条目数据结构"""
    
    def __init__(self, title: str, link: str, source: str, source_id: str,
                 summary: Optional[str] = None, published: Optional[datetime] = None,
                 author: Optional[str] = None, tags: Optional[list[str]] = None):
        self.title = title
        self.link = link
        self.source = source
        self.source_id = source_id
        self.summary = summary
        self.published = published or datetime.now(timezone.utc)
        self.author = author
        self.tags = tags or []
    
    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "link": self.link,
            "source": self.source,
            "source_id": self.source_id,
            "published": self.published.isoformat(),
            "summary": self.summary,
            "author": self.author,
            "tags": self.tags,
            "type": "web",
        }


# 媒体网站解析配置
# 定义常见媒体的 CSS 选择器
MEDIA_SELECTORS = {
    "36kr.com": {
        "article": "a[class*='post-item']",
        "title": "h2, h3, div[class*='title']",
        "link": "href",
        "summary": "p[class*='summary'], div[class*='desc']",
    },
    "jiqizhixin.com": {
        "article": "article, div[class*='article']",
        "title": "h2, h3, a[class*='title']",
        "link": "href",
        "summary": "p[class*='summary'], div[class*='abstract']",
    },
    "qbitai.com": {
        "article": "div[class*='post']",
        "title": "h2, h3, a[class*='title']",
        "link": "href",
        "summary": "p[class*='summary'], div[class*='excerpt']",
    },
    "ifanr.com": {
        "article": "article, div[class*='post']",
        "title": "h2, h3, a[class*='title']",
        "link": "href",
        "summary": "p[class*='summary'], div[class*='excerpt']",
    },
    "sspai.com": {
        "article": "article, div[class*='post']",
        "title": "h2, h3, a[class*='title']",
        "link": "href",
        "summary": "p[class*='summary'], div[class*='excerpt']",
    },
    "theverge.com": {
        "article": "article, div[class*='entry']",
        "title": "h2, h3, a[class*='title']",
        "link": "href",
        "summary": "p[class*='summary'], div[class*='excerpt']",
    },
    "techcrunch.com": {
        "article": "article, div[class*='post']",
        "title": "h2, h3, a[class*='title']",
        "link": "href",
        "summary": "p[class*='summary'], div[class*='excerpt']",
    },
    "default": {
        "article": "article, div[class*='post'], div[class*='item'], li[class*='item']",
        "title": "h2, h3, h4, a[class*='title'], a[class*='headline']",
        "link": "href",
        "summary": "p[class*='summary'], p[class*='desc'], div[class*='excerpt']",
    },
}


def get_selector(url: str) -> dict:
    """根据 URL 获取对应的解析选择器"""
    for domain, selector in MEDIA_SELECTORS.items():
        if domain in url:
            return selector
    return MEDIA_SELECTORS["default"]


def call_web_fetch(url: str) -> str:
    """
    调用 OpenClaw web_fetch 工具抓取网页
    
    注意：这个函数需要 Agent 在实际执行时替换为真实的 web_fetch 调用
    这里提供一个模拟接口用于测试
    """
    # 实际使用时，Agent 应该这样调用：
    # result = web_fetch(url=url, extractMode="markdown")
    # return result.content
    
    # 测试模式：返回提示
    return f"[web_fetch] 抓取：{url}\n请使用 OpenClaw web_fetch 工具获取实际内容"


def parse_web_content(url: str, content: str, source_name: str, source_id: str) -> List[WebItem]:
    """
    解析网页内容，提取文章列表
    
    Args:
        url: 原始 URL
        content: 网页内容（Markdown 或 HTML）
        source_name: 信息源名称
        source_id: 信息源 ID
    
    Returns:
        WebItem 列表
    """
    items = []
    selector = get_selector(url)
    
    # 简单解析：按行分割，查找可能的文章标题
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # 跳过空行和无关内容
        if not line or len(line) < 10:
            continue
        
        # 查找可能的标题（包含链接的 Markdown 格式）
        if '](' in line and line.startswith('['):
            try:
                # 解析 Markdown 链接：[标题](链接)
                title_end = line.index('](')
                title = line[1:title_end]
                link_start = title_end + 2
                link_end = line.index(')', link_start)
                link = line[link_start:link_end]
                
                # 清理标题
                title = title.strip()[:200]
                
                # 跳过太短的标题
                if len(title) < 5:
                    continue
                
                items.append(WebItem(
                    title=title,
                    link=link if link.startswith('http') else url,
                    source=source_name,
                    source_id=source_id,
                ))
            except (ValueError, IndexError):
                continue
        
        # 查找纯文本标题（可能是 H2/H3）
        elif line.startswith('## ') or line.startswith('### '):
            title = line.lstrip('#').strip()[:200]
            if len(title) >= 5:
                items.append(WebItem(
                    title=title,
                    link=url,
                    source=source_name,
                    source_id=source_id,
                ))
    
    # 限制每个源最多 20 条
    return items[:20]


def fetch_web_source(source: dict) -> List[WebItem]:
    """
    抓取单个网页源
    
    Args:
        source: 信息源字典
    
    Returns:
        WebItem 列表
    """
    url = source["url"]
    source_name = source["name"]
    source_id = source["id"]
    
    print(f"抓取：{source_name} ({url})")
    
    try:
        # 实际使用时由 Agent 调用 web_fetch 工具
        # 这里输出指令供 Agent 执行
        print(f"  → [AGENT] 请调用：web_fetch(url='{url}', extractMode='markdown')")
        
        # 测试模式：返回模拟数据（实际使用时删除）
        items = [
            WebItem(
                title=f"[测试] {source_name} - 示例文章标题",
                link=url,
                source=source_name,
                source_id=source_id,
                summary="这是测试数据，实际使用时 Agent 会调用 web_fetch 工具获取真实内容",
            )
        ]
        print(f"  → 提取 {len(items)} 条（测试模式）")
        return items
    
    except Exception as e:
        print(f"  ✗ 抓取失败：{e}")
        return []


def fetch_all_web(limit_per_source: int = 15) -> List[WebItem]:
    """
    抓取所有网页源（排除已覆盖的 RSS 源）
    
    Returns:
        WebItem 列表
    """
    # 获取所有启用的源
    sources = get_enabled_sources()
    
    # 排除 RSS 源（已有 rss_fetcher 处理）
    web_sources = [s for s in sources if s["type"] in ["中文媒体", "英文媒体", "设计媒体"]]
    
    if not web_sources:
        print("未找到需要网页抓取的源")
        return []
    
    print(f"开始抓取 {len(web_sources)} 个网页源...")
    
    all_items = []
    
    for source in web_sources:
        items = fetch_web_source(source, use_real_fetch=False)
        items = items[:limit_per_source]
        all_items.extend(items)
    
    print(f"\n共抓取 {len(all_items)} 条网页内容")
    return all_items


def save_to_cache(items: List[WebItem], prefix: str = "web"):
    """缓存抓取结果"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{prefix}_cache_{timestamp}.json"
    cache_file = CACHE_DIR / filename
    
    data = [item.to_dict() for item in items]
    
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"缓存已保存：{cache_file}")
    return cache_file


def merge_all_sources(rss_file: Optional[str] = None, 
                      api_file: Optional[str] = None,
                      web_file: Optional[str] = None) -> List[dict]:
    """
    合并所有抓取源的结果
    
    Args:
        rss_file: RSS 缓存文件路径
        api_file: API 缓存文件路径
        web_file: 网页缓存文件路径
    
    Returns:
        合并后的条目列表
    """
    all_items = []
    
    for file_path, source_type in [(rss_file, "rss"), (api_file, "api"), (web_file, "web")]:
        if file_path:
            path = Path(file_path)
            if not path.is_absolute():
                path = CACHE_DIR / file_path
            
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    items = json.load(f)
                print(f"加载 {source_type}: {len(items)} 条")
                all_items.extend(items)
    
    # 去重（按链接）
    seen_links = set()
    unique_items = []
    for item in all_items:
        link = item.get("link", "")
        if link and link not in seen_links:
            seen_links.add(link)
            unique_items.append(item)
    
    print(f"合并后：{len(unique_items)} 条（去重 {len(all_items) - len(unique_items)} 条重复）")
    return unique_items


# CLI 入口
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "fetch":
        if len(sys.argv) < 3:
            print("用法：python web_fetcher.py fetch <source_id>")
            sys.exit(1)
        
        source = get_source(sys.argv[2])
        if not source:
            print(f"未找到信息源：{sys.argv[2]}")
            sys.exit(1)
        
        items = fetch_web_source(source, use_real_fetch=False)
        print(f"\n抓取到 {len(items)} 条:")
        for item in items[:10]:
            print(f"  - {item.title[:50]}...")
    
    elif command == "fetch-all":
        items = fetch_all_web()
        save_to_cache(items)
        
        # 输出 JSON
        if len(sys.argv) > 2 and sys.argv[2] == "--json":
            print(json.dumps([item.to_dict() for item in items], ensure_ascii=False, indent=2))
    
    elif command == "merge":
        rss = sys.argv[2] if len(sys.argv) > 2 else None
        api = sys.argv[3] if len(sys.argv) > 3 else None
        web = sys.argv[4] if len(sys.argv) > 4 else None
        
        merged = merge_all_sources(rss_file=rss, api_file=api, web_file=web)
        
        # 输出合并结果
        if len(sys.argv) > 5 and sys.argv[5] == "--json":
            print(json.dumps(merged, ensure_ascii=False, indent=2))
    
    elif command == "list-cache":
        cache_files = list(CACHE_DIR.glob("*_cache_*.json"))
        if cache_files:
            print("缓存文件:")
            for f in cache_files[-10:]:
                print(f"  {f.name}")
        else:
            print("无缓存文件")
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
