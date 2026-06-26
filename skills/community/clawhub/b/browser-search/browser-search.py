#!/usr/bin/env python3
"""
Browser Search 技能 - 安全的浏览器搜索工具
使用本地浏览器进行自动化搜索和内容提取

支持搜索引擎：Bing, Google, Baidu, DuckDuckGo
无需 API 配置，直接使用本地浏览器

【安装要求】
- 需要安装 Playwright: pip install playwright
- 需要安装 Chromium: playwright install chromium

【安全限制】
- 输出路径限制：仅允许保存到用户主目录
- 无危险函数：不使用 eval/exec 等危险函数
- 仅访问公开搜索引擎
- 严格的超时控制
"""

import os
import sys
import json
import time
import urllib.parse
from typing import List, Dict, Optional
from playwright.sync_api import sync_playwright

# 配置
DEFAULT_TIMEOUT = 30000
DEFAULT_MAX_RESULTS = 10
SUPPORTED_ENGINES = ["bing", "google", "baidu", "duckduckgo"]

# 安全配置
ALLOWED_BASE_DIR = os.path.expanduser("~")


class BrowserSearch:
    def __init__(self):
        self.engine = "bing"
        self.search_url = ""
        self.query_selector = "h2"
        self.output_file: Optional[str] = None
        self.results: List[Dict] = []
        
    def set_engine(self, engine: str) -> None:
        """设置搜索引擎"""
        if engine not in SUPPORTED_ENGINES:
            print(f"不支持的搜索引擎：{engine}")
            return
        self.engine = engine
        configs = {
            "bing": "https://www.bing.com/search?q={query}",
            "google": "https://www.google.com/search?q={query}",
            "baidu": "https://www.baidu.com/s?wd={query}",
            "duckduckgo": "https://duckduckgo.com/?q={query}"
        }
        self.search_url = configs.get(engine, configs["bing"])
    
    def validate_output_path(self, path: str) -> bool:
        """验证输出路径是否在允许范围内"""
        if not path:
            return False
        
        try:
            if path.startswith("~/"):
                path = os.path.expanduser(path)
            
            abs_path = os.path.abspath(path)
            real_path = os.path.realpath(abs_path)
            real_base = os.path.realpath(ALLOWED_BASE_DIR)
            
            if real_path.startswith(real_base + os.sep) or real_path == real_base:
                return True
            
            return False
        except Exception:
            return False
    
    def search(self, query: str, max_results: int = DEFAULT_MAX_RESULTS, output_file: Optional[str] = None) -> Dict:
        """执行搜索"""
        clean_query = " ".join(query.split())
        self.results = []
        self.output_file = output_file
        
        if output_file and not self.validate_output_path(output_file):
            return {"error": "invalid_output_path", "message": "路径不合法", "results": []}
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    viewport={"width": 1280, "height": 720},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                )
                page = context.new_page()
                
                encoded_query = urllib.parse.quote(clean_query, safe="+")
                search_url = self.search_url.format(query=encoded_query)
                
                page.goto(search_url, wait_until="domcontentloaded", timeout=DEFAULT_TIMEOUT)
                time.sleep(1)
                
                results = page.query_selector_all(self.query_selector)
                
                count = 0
                for result in results[:max_results]:
                    try:
                        link = result.query_selector("h2 a") or result.query_selector("h3 a") or result.query_selector("a")
                        if link:
                            title = link.text_content().strip()
                            url = link.get_attribute("href")
                            if title and url:
                                self.results.append({"title": title, "url": url, "engine": self.engine})
                                count += 1
                    except Exception:
                        continue
                
                response = {"query": clean_query, "engine": self.engine, "count": len(self.results), "results": self.results}
                
                if self.output_file:
                    with open(self.output_file, 'w', encoding='utf-8') as f:
                        json.dump(response, f, ensure_ascii=False, indent=2)
                
                browser.close()
                
                return response
                
        except Exception as e:
            return {"error": "search_failed", "message": str(e), "results": []}

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        sys.exit(1)
    
    args = sys.argv[1:]
    engine = "bing"
    output_file = None
    max_results = DEFAULT_MAX_RESULTS
    
    i = 0
    while i < len(args):
        if args[i] == "--engine" and i + 1 < len(args):
            engine = args[i + 1]
            i += 2
        elif args[i] == "--output" and i + 1 < len(args):
            output_file = args[i + 1]
            i += 2
        elif args[i] == "--max" and i + 1 < len(args):
            try:
                max_results = int(args[i + 1])
                i += 2
            except Exception:
                sys.exit(1)
        else:
            query_parts = []
            while i < len(args) and not (args[i].startswith("--")):
                query_parts.append(args[i])
                i += 1
            query = " ".join(query_parts)
            break
    
    if not query:
        sys.exit(1)
    
    search = BrowserSearch()
    search.set_engine(engine)
    search.output_file = output_file
    
    response = search.search(query, max_results=max_results)
    sys.exit(0)

if __name__ == "__main__":
    main()
