#!/usr/bin/env python3
"""
设计师情报站 - 独立网页抓取器（不依赖 OpenClaw）

功能：
- 使用 requests + BeautifulSoup 直接抓取网页
- 支持多种网站结构解析
- 结果缓存
- 可在 qclaw/任何 Python 环境运行

使用方式:
    python web_fetcher_standalone.py fetch-all    # 抓取所有网页源
    python web_fetcher_standalone.py fetch CN001  # 抓取单个源
"""

import json
import sys
import time
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict
from urllib.parse import urljoin

# 依赖检查
try:
    import requests
    from bs4 import BeautifulSoup
    from dateutil import parser as date_parser
except ImportError as e:
    print(f"❌ 缺少依赖：{e}")
    print("请安装：pip install requests beautifulsoup4 python-dateutil")
    sys.exit(1)

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))
from sources_manager import get_enabled_sources, get_source

# 缓存目录
CACHE_DIR = Path(__file__).parent.parent / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# User-Agent 轮换
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
]


class StandaloneWebFetcher:
    """独立网页抓取器（不依赖 OpenClaw）"""
    
    def __init__(self, delay: float = 1.0, timeout: int = 10):
        self.delay = delay  # 请求间隔（秒）
        self.timeout = timeout  # 超时时间（秒）
        self.session = requests.Session()
        
    def fetch(self, url: str, source_id: str = None) -> Optional[Dict]:
        """抓取单个网页"""
        
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        
        try:
            print(f"  🕷️  抓取：{url}")
            print(f"  Headers: {headers['User-Agent'][:50]}...")
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            print(f"  状态码：{response.status_code}")
            print(f"  内容长度：{len(response.text)}")
            response.raise_for_status()
            
            # 解析 HTML
            items = self.parse_html(response.text, url, source_id)
            
            # 缓存
            if items:
                self.save_cache(source_id, items)
            
            # 随机延迟
            time.sleep(self.delay + random.uniform(0, 0.5))
            
            return items
            
        except requests.exceptions.RequestException as e:
            print(f"  ❌ 抓取失败：{type(e).__name__}: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"     状态码：{e.response.status_code}")
                print(f"     响应：{e.response.text[:200]}")
            return None
        except Exception as e:
            print(f"  ❌ 解析失败：{type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def parse_html(self, html: str, base_url: str, source_id: str) -> List[Dict]:
        """解析 HTML 提取文章列表"""
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # 根据源 ID 选择解析策略
        if source_id:
            parser = getattr(self, f'parse_{source_id.lower()}', self.parse_generic)
            items = parser(soup, base_url)
        else:
            items = self.parse_generic(soup, base_url)
        
        return items
    
    def parse_generic(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """通用解析策略"""
        
        items = []
        
        # 查找文章链接（常见模式）
        selectors = [
            'article a[href]',
            '.post-title a[href]',
            '.entry-title a[href]',
            'h2 a[href]',
            'h3 a[href]',
        ]
        
        for selector in selectors:
            links = soup.select(selector)
            for link in links[:10]:  # 最多 10 条
                title = link.get_text(strip=True)
                href = link.get('href')
                
                if title and len(title) > 5 and len(title) < 200 and href:
                    full_url = urljoin(base_url, href)
                    
                    # 避免重复
                    if not any(item['link'] == full_url for item in items):
                        items.append({
                            'title': title,
                            'link': full_url,
                            'source': base_url,
                            'source_id': 'WEB',
                            'summary': '',
                            'published': datetime.now(timezone.utc).isoformat(),
                            'type': 'web'
                        })
        
        return items
    
    def parse_cn001(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """36 氪解析策略"""
        # 可以添加特定网站的解析逻辑
        return self.parse_generic(soup, base_url)
    
    def parse_cn004(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """爱范儿解析策略"""
        return self.parse_generic(soup, base_url)
    
    def save_cache(self, source_id: str, items: List[Dict]):
        """保存缓存"""
        cache_file = CACHE_DIR / f"web_cache_{source_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
    
    def fetch_all(self, sources: List[Dict]) -> Dict[str, List[Dict]]:
        """批量抓取所有网页源"""
        
        results = {}
        
        for source in sources:
            if source.get('fetch_method') != 'web':
                continue
            
            source_id = source['id']
            url = source['url']
            
            print(f"\n📰 [{source_id}] {source['name']}")
            items = self.fetch(url, source_id)
            
            if items:
                results[source_id] = items
                print(f"   ✅ 抓取到 {len(items)} 条")
            else:
                print(f"   ❌ 抓取失败")
        
        return results


def main():
    """CLI 入口"""
    
    if len(sys.argv) < 2:
        print("用法：python web_fetcher_standalone.py <command> [args]")
        print("命令:")
        print("  fetch-all         抓取所有网页源")
        print("  fetch <source_id> 抓取单个源")
        sys.exit(1)
    
    command = sys.argv[1]
    
    fetcher = StandaloneWebFetcher(delay=2.0, timeout=15)
    
    if command == 'fetch-all':
        print("=" * 60)
        print("🕷️  独立网页抓取器（不依赖 OpenClaw）")
        print("=" * 60)
        
        sources = get_enabled_sources()
        web_sources = [s for s in sources if s.get('fetch_method') == 'web']
        
        print(f"\n📊 待抓取：{len(web_sources)} 个网页源")
        
        results = fetcher.fetch_all(web_sources)
        
        # 合并结果
        all_items = []
        for source_id, items in results.items():
            all_items.extend(items)
        
        # 保存总结果
        output_file = CACHE_DIR / f"web_items_standalone_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_items, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 抓取完成：共 {len(all_items)} 条")
        print(f"📁 保存到：{output_file}")
        
    elif command == 'fetch':
        if len(sys.argv) < 3:
            print("用法：python web_fetcher_standalone.py fetch <source_id>")
            sys.exit(1)
        
        source_id = sys.argv[2]
        source = get_source(source_id)
        
        if not source:
            print(f"❌ 未找到信息源：{source_id}")
            sys.exit(1)
        
        print(f"\n📰 [{source_id}] {source['name']}")
        items = fetcher.fetch(source['url'], source_id)
        
        if items:
            print(f"✅ 抓取到 {len(items)} 条")
        else:
            print("❌ 抓取失败")
    
    else:
        print(f"❌ 未知命令：{command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
