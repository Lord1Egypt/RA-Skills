#!/usr/bin/env python3
"""
AI联网搜索技能 v1.0
安全的网络搜索工具，支持多个搜索引擎API
"""

import json
import requests
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urlparse
import re


class AISecurityError(Exception):
    """安全相关异常"""
    pass


class SearchSecurityValidator:
    """搜索安全验证器"""

    # 允许的搜索引擎域名
    ALLOWED_DOMAINS = [
        'api.duckduckgo.com',
        'serpapi.com',
        'google.serper.dev',
        'api.search.brave.com'
    ]

    # 敏感关键词黑名单
    SENSITIVE_KEYWORDS = [
        'hack', 'exploit', 'dark web', 'darknet',
        'illegal', 'porn', 'piracy'
    ]

    @classmethod
    def validate_query(cls, query: str) -> bool:
        """验证搜索查询"""
        query_lower = query.lower()

        # 检查敏感关键词
        for keyword in cls.SENSITIVE_KEYWORDS:
            if keyword in query_lower:
                raise AISecurityError(f"查询包含敏感关键词: {keyword}")

        return True

    @classmethod
    def validate_url(cls, url: str) -> bool:
        """验证URL安全性"""
        try:
            parsed = urlparse(url)
            return parsed.scheme in ['http', 'https']
        except Exception:
            return False


class CachedSearch:
    """带缓存的搜索引擎"""

    def __init__(self, cache_path: str = None, cache_hours: int = 24):
        """
        初始化搜索引擎

        Args:
            cache_path: 缓存数据库路径
            cache_hours: 缓存有效期（小时）
        """
        if cache_path is None:
            cache_path = Path.home() / ".ai_search_cache.db"

        self.db_path = Path(cache_path)
        self.cache_hours = cache_hours
        self.validator = SearchSecurityValidator()

        self._init_db()

    def _init_db(self):
        """初始化缓存数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                engine TEXT,
                results TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('CREATE INDEX IF NOT EXISTS idx_query ON search_cache(query)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON search_cache(created_at)')

        conn.commit()
        conn.close()

    def _get_cached(self, query: str, engine: str = None) -> Optional[List[Dict]]:
        """从缓存获取结果"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cutoff_time = datetime.now() - timedelta(hours=self.cache_hours)

        if engine:
            cursor.execute('''
                SELECT results FROM search_cache
                WHERE query = ? AND engine = ? AND created_at > ?
                ORDER BY created_at DESC LIMIT 1
            ''', (query, engine, cutoff_time))
        else:
            cursor.execute('''
                SELECT results FROM search_cache
                WHERE query = ? AND created_at > ?
                ORDER BY created_at DESC LIMIT 1
            ''', (query, cutoff_time))

        row = cursor.fetchone()
        conn.close()

        if row:
            return json.loads(row[0])
        return None

    def _save_cache(self, query: str, results: List[Dict], engine: str = None):
        """保存到缓存"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO search_cache (query, engine, results)
            VALUES (?, ?, ?)
        ''', (query, engine, json.dumps(results)))

        conn.commit()
        conn.close()

    def clean_cache(self):
        """清理过期缓存"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cutoff_time = datetime.now() - timedelta(hours=self.cache_hours)
        cursor.execute('DELETE FROM search_cache WHERE created_at < ?', (cutoff_time,))

        deleted = cursor.rowcount
        conn.commit()
        conn.close()

        return deleted


class DuckDuckGoSearch(CachedSearch):
    """DuckDuckGo搜索引擎（免费，无需API密钥）"""

    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        执行搜索

        Args:
            query: 搜索关键词
            max_results: 最大结果数

        Returns:
            搜索结果列表
        """
        # 安全验证
        self.validator.validate_query(query)

        # 检查缓存
        cached = self._get_cached(query, "duckduckgo")
        if cached:
            print(f"[缓存] 使用缓存结果")
            return cached[:max_results]

        # 执行搜索
        try:
            from duckduckgo_search import DDGS
            ddgs = DDGS()

            results = []
            search_results = ddgs.text(query, max_results=max_results)

            for r in search_results:
                if self.validator.validate_url(r.get('link', '')):
                    results.append({
                        'title': r.get('title', ''),
                        'url': r.get('link', ''),
                        'snippet': r.get('body', ''),
                        'source': 'DuckDuckGo'
                    })

            # 保存缓存
            self._save_cache(query, results, "duckduckgo")

            return results

        except ImportError:
            print("提示: 安装 duckduckgo-search 以获得更好的搜索体验")
            print("命令: pip install duckduckgo-search")
            return []
        except Exception as e:
            print(f"搜索错误: {e}")
            return []


class WikipediaSearch(CachedSearch):
    """维基百科搜索（免费，无需API密钥）"""

    def search(self, query: str, max_results: int = 3) -> List[Dict]:
        """
        搜索维基百科

        Args:
            query: 搜索关键词
            max_results: 最大结果数

        Returns:
            搜索结果列表
        """
        self.validator.validate_query(query)

        # 检查缓存
        cached = self._get_cached(query, "wikipedia")
        if cached:
            return cached[:max_results]

        try:
            import wikipedia

            # 设置中文
            wikipedia.set_lang("zh")

            results = []
            search_results = wikipedia.search(query, results=max_results)

            for title in search_results:
                try:
                    page = wikipedia.page(title, auto_suggest=False)
                    results.append({
                        'title': page.title,
                        'url': page.url,
                        'snippet': page.summary[:200] + "...",
                        'source': 'Wikipedia'
                    })
                except Exception:
                    continue

            self._save_cache(query, results, "wikipedia")
            return results

        except ImportError:
            print("提示: 安装 wikipedia 以获得维基百科搜索")
            print("命令: pip install wikipedia")
            return []
        except Exception as e:
            print(f"维基百科搜索错误: {e}")
            return []


class WebSearchTool:
    """综合网络搜索工具"""

    def __init__(self):
        self.ddg = DuckDuckGoSearch()
        self.wikipedia = WikipediaSearch()

    def search(self, query: str, engines: List[str] = None, max_results: int = 5) -> Dict[str, List[Dict]]:
        """
        综合搜索

        Args:
            query: 搜索关键词
            engines: 使用的搜索引擎列表 ['duckduckgo', 'wikipedia']
            max_results: 每个引擎的最大结果数

        Returns:
            各引擎的搜索结果
        """
        if engines is None:
            engines = ['duckduckgo']

        results = {}

        if 'duckduckgo' in engines:
            results['duckduckgo'] = self.ddg.search(query, max_results)

        if 'wikipedia' in engines:
            results['wikipedia'] = self.wikipedia.search(query, max_results)

        return results

    def quick_search(self, query: str) -> str:
        """快速搜索，返回格式化的摘要"""
        results = self.search(query, ['duckduckgo', 'wikipedia'], max_results=3)

        output = f"\n搜索结果: {query}\n"
        output += "=" * 50 + "\n"

        for engine, items in results.items():
            if items:
                output += f"\n【{engine}】\n"
                for i, item in enumerate(items, 1):
                    output += f"\n{i}. {item['title']}\n"
                    output += f"   {item['snippet'][:100]}...\n"
                    output += f"   🔗 {item['url']}\n"

        return output

    def clean_cache(self):
        """清理所有缓存"""
        total = 0
        total += self.ddg.clean_cache()
        total += self.wikipedia.clean_cache()
        return total


def main():
    """命令行界面"""
    print("=" * 50)
    print("AI联网搜索工具 v1.0")
    print("=" * 50)

    search_tool = WebSearchTool()

    while True:
        print("\n请选择操作:")
        print("1. 搜索")
        print("2. 快速搜索")
        print("3. 清理缓存")
        print("0. 退出")

        choice = input("\n请输入选项: ").strip()

        if choice == "0":
            print("再见！")
            break

        elif choice in ["1", "2"]:
            query = input("请输入搜索关键词: ").strip()

            if not query:
                print("搜索关键词不能为空")
                continue

            if choice == "1":
                engines = input("选择搜索引擎 (duckduckgo/wikipedia/both, 默认duckduckgo): ").strip().lower()

                if engines == "wikipedia":
                    selected_engines = ['wikipedia']
                elif engines == "both":
                    selected_engines = ['duckduckgo', 'wikipedia']
                else:
                    selected_engines = ['duckduckgo']

                results = search_tool.search(query, selected_engines)

                for engine, items in results.items():
                    print(f"\n【{engine}】找到 {len(items)} 条结果:")
                    for i, item in enumerate(items, 1):
                        print(f"\n{i}. {item['title']}")
                        print(f"   {item['snippet'][:100]}...")
                        print(f"   🔗 {item['url']}")

            else:  # choice == "2"
                print(search_tool.quick_search(query))

        elif choice == "3":
            deleted = search_tool.clean_cache()
            print(f"✓ 已清理 {deleted} 条过期缓存")


if __name__ == "__main__":
    main()
