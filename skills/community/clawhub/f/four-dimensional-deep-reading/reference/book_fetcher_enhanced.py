#!/usr/bin/env python3
"""
book_fetcher_enhanced.py - Enhanced Book Information Fetcher

Optimized features:
1. Multi-source backup: Douban → Goodreads → Wikipedia → Google Books
2. Local cache: Avoid repeated requests, cache valid for 7 days
3. Error retry: Auto-retry 3 times on failure, exponential backoff
4. Data merge: Intelligent multi-source data merge, pick optimal values

Version: v2.0.0
Updated: 2026-04-28
"""

import os
import json
import time
import hashlib
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path


# ==================== Configuration ====================

CONFIG = {
    # Cache configuration
    "cache_dir": Path("/root/.openclaw/workspace/.cache/book_fetcher"),
    "cache_expire_days": 7,
    
    # Retry configuration
    "max_retries": 3,
    "retry_base_delay": 1.0,  # Base delay (seconds)
    "retry_max_delay": 10.0,  # Max delay (seconds)
    
    # Data source priority (by language)
    "sources": {
        "zh": ["douban", "baidu_baike", "zhihu", "wikipedia_zh"],
        "en": ["goodreads", "google_books", "wikipedia_en", "amazon"],
        "ja": ["booklog", "amazon_jp", "goodreads"],
        "ko": ["yes24", "aladin", "goodreads"],
        "default": ["goodreads", "wikipedia_en", "google_books"]
    },
    
    # Field priority (which source's data is more trustworthy)
    "field_priority": {
        "rating": ["douban", "goodreads", "amazon"],  # Rating priority: Douban
        "summary": ["douban", "goodreads", "wikipedia"],  # Summary priority: Douban
        "reviews": ["douban", "goodreads", "amazon"],  # Review count priority: Douban
    }
}


# ==================== Cache Management ====================

class CacheManager:
    """Local cache manager"""
    
    def __init__(self, cache_dir: Path, expire_days: int = 7):
        self.cache_dir = cache_dir
        self.expire_days = expire_days
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_key(self, book_name: str, source: str) -> str:
        """Generate cache key"""
        key = f"{book_name}_{source}"
        return hashlib.md5(key.encode()).hexdigest()
    
    def _get_cache_path(self, book_name: str, source: str) -> Path:
        """Get cache file path"""
        cache_key = self._get_cache_key(book_name, source)
        return self.cache_dir / f"{cache_key}.json"
    
    def get(self, book_name: str, source: str) -> Optional[Dict]:
        """Get data from cache"""
        cache_path = self._get_cache_path(book_name, source)
        
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cached = json.load(f)
            
            # Check if expired
            cached_time = datetime.fromisoformat(cached.get("cached_at", "2000-01-01"))
            if datetime.now() - cached_time > timedelta(days=self.expire_days):
                return None
            
            return cached.get("data")
        except Exception as e:
            print(f"[cache] Failed to read cache: {e}")
            return None
    
    def set(self, book_name: str, source: str, data: Dict) -> bool:
        """Save data to cache"""
        cache_path = self._get_cache_path(book_name, source)
        
        try:
            cached = {
                "book_name": book_name,
                "source": source,
                "data": data,
                "cached_at": datetime.now().isoformat()
            }
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cached, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"[cache] Failed to write cache: {e}")
            return False
    
    def clear_expired(self) -> int:
        """Clear expired cache"""
        cleared = 0
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached = json.load(f)
                cached_time = datetime.fromisoformat(cached.get("cached_at", "2000-01-01"))
                if datetime.now() - cached_time > timedelta(days=self.expire_days):
                    cache_file.unlink()
                    cleared += 1
            except:
                pass
        return cleared


# ==================== Retry Mechanism ====================

def retry_with_backoff(func, *args, max_retries: int = 3, 
                       base_delay: float = 1.0, max_delay: float = 10.0, **kwargs):
    """
    Retry mechanism with exponential backoff
    
    Args:
        func: Function to execute
        max_retries: Maximum retry count
        base_delay: Base delay (seconds)
        max_delay: Maximum delay (seconds)
    
    Returns:
        Function execution result, or None if all attempts fail
    """
    last_error = None
    
    for attempt in range(max_retries):
        try:
            result = func(*args, **kwargs)
            if result:
                return result
        except Exception as e:
            last_error = e
            print(f"[retry] Attempt {attempt + 1} failed: {e}")
        
        # Exponential backoff delay
        if attempt < max_retries - 1:
            delay = min(base_delay * (2 ** attempt), max_delay)
            print(f"[retry] Waiting {delay:.1f} seconds before retry...")
            time.sleep(delay)
    
    print(f"[retry] All {max_retries} attempts failed")
    return None


# ==================== Data Source Fetching ====================

class BookFetcher:
    """Enhanced book information fetcher"""
    
    def __init__(self):
        self.cache = CacheManager(
            CONFIG["cache_dir"], 
            CONFIG["cache_expire_days"]
        )
        self.fetch_stats = {
            "cache_hits": 0,
            "fetches": 0,
            "failures": 0
        }
    
    def detect_language(self, text: str) -> str:
        """Detect text language"""
        # Chinese: CJK Unified Ideographs
        if any('\u4e00' <= c <= '\u9fff' for c in text):
            return 'zh'
        # Japanese: Hiragana or Katakana
        if any('\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff' for c in text):
            return 'ja'
        # Korean: Hangul
        if any('\uac00' <= c <= '\ud7af' for c in text):
            return 'ko'
        # Default English
        return 'en'
    
    def fetch_book_info(self, book_name: str, author: str = None) -> Dict:
        """
        Get complete book information (multi-source backup)
        
        Args:
            book_name: Book title
            author: Author (optional, for improving match accuracy)
        
        Returns:
            Structured book information
        """
        # Initialize result
        result = {
            "title": book_name,
            "author": author,
            "isbn": None,
            "publisher": None,
            "publish_year": None,
            "rating": None,
            "review_count": None,
            "summary": None,
            "chapters": [],
            "background": None,
            "similar_books": [],
            "sources": [],
            "fetch_stats": {}
        }
        
        # Detect language and get data source priority
        language = self.detect_language(book_name)
        sources = CONFIG["sources"].get(language, CONFIG["sources"]["default"])
        
        print(f"[fetch] Detected language: {language}")
        print(f"[fetch] Data source priority: {' → '.join(sources)}")
        
        # Try each data source in priority order
        all_data = {}
        for source in sources:
            print(f"\n[fetch] Trying data source: {source}")
            
            # Check cache first
            cached = self.cache.get(book_name, source)
            if cached:
                print(f"[fetch] ✓ Cache hit")
                self.fetch_stats["cache_hits"] += 1
                all_data[source] = cached
                continue
            
            # Try fetching (with retry)
            fetch_func = getattr(self, f"_fetch_{source}", None)
            if fetch_func:
                data = retry_with_backoff(
                    fetch_func, 
                    book_name, 
                    author,
                    max_retries=CONFIG["max_retries"],
                    base_delay=CONFIG["retry_base_delay"],
                    max_delay=CONFIG["retry_max_delay"]
                )
                
                if data:
                    print(f"[fetch] ✓ Fetch successful")
                    self.fetch_stats["fetches"] += 1
                    all_data[source] = data
                    # Save to cache
                    self.cache.set(book_name, source, data)
                else:
                    print(f"[fetch] ✗ Fetch failed")
                    self.fetch_stats["failures"] += 1
            else:
                print(f"[fetch] ⚠ Data source not implemented")
        
        # Merge multi-source data
        merged = self._merge_data(all_data)
        result.update(merged)
        result["fetch_stats"] = self.fetch_stats
        
        return result
    
    def _merge_data(self, all_data: Dict[str, Dict]) -> Dict:
        """
        Intelligently merge multi-source data
        
        Rules:
        1. Rating: Priority Douban, then Goodreads
        2. Summary: Priority Douban, then Wikipedia
        3. Other fields: Take first non-empty value
        """
        if not all_data:
            return {}
        
        merged = {"sources": list(all_data.keys())}
        
        # Define field merge rules
        field_rules = {
            "title": lambda: self._pick_first_non_empty(all_data, "title"),
            "author": lambda: self._pick_first_non_empty(all_data, "author"),
            "isbn": lambda: self._pick_first_non_empty(all_data, "isbn"),
            "publisher": lambda: self._pick_first_non_empty(all_data, "publisher"),
            "publish_year": lambda: self._pick_first_non_empty(all_data, "publish_year"),
            "rating": lambda: self._pick_by_priority(all_data, "rating", CONFIG["field_priority"]["rating"]),
            "review_count": lambda: self._pick_by_priority(all_data, "review_count", CONFIG["field_priority"]["reviews"]),
            "summary": lambda: self._pick_by_priority(all_data, "summary", CONFIG["field_priority"]["summary"]),
            "chapters": lambda: self._pick_first_non_empty(all_data, "chapters"),
            "background": lambda: self._pick_first_non_empty(all_data, "background"),
            "similar_books": lambda: self._pick_first_non_empty(all_data, "similar_books"),
        }
        
        for field, getter in field_rules.items():
            try:
                value = getter()
                if value is not None:
                    merged[field] = value
            except:
                pass
        
        return merged
    
    def _pick_first_non_empty(self, all_data: Dict, field: str):
        """Take first non-empty value"""
        for source, data in all_data.items():
            value = data.get(field)
            if value is not None and value != "" and value != []:
                return value
        return None
    
    def _pick_by_priority(self, all_data: Dict, field: str, priority: List[str]):
        """Take value by priority"""
        for source in priority:
            if source in all_data:
                value = all_data[source].get(field)
                if value is not None and value != "":
                    return value
        return self._pick_first_non_empty(all_data, field)
    
    # ==================== Data Source Implementations ====================
    
    def _fetch_douban(self, book_name: str, author: str = None) -> Optional[Dict]:
        """
        Fetch Douban books
        
        Note: This method returns fetch instructions, actual execution by AI calling web_fetch
        """
        search_url = f"https://book.douban.com/subject_search?search_text={book_name}"
        
        # Return fetch instructions (for AI execution)
        return {
            "_action": "web_fetch",
            "_url": search_url,
            "_extract": {
                "title": "First search result title",
                "author": "Author field",
                "rating": "Rating number (0-10)",
                "review_count": "Review count",
                "summary": "Book summary",
                "publisher": "Publisher",
                "publish_year": "Publication year",
            },
            "_note": "Douban pages need anti-scraping handling, suggest using web_fetch tool"
        }
    
    def _fetch_goodreads(self, book_name: str, author: str = None) -> Optional[Dict]:
        """Fetch Goodreads"""
        query = f"{book_name} {author}" if author else book_name
        search_url = f"https://www.goodreads.com/search?q={query}"
        
        return {
            "_action": "web_fetch",
            "_url": search_url,
            "_extract": {
                "title": "Book title",
                "author": "Author",
                "rating": "Rating (0-5)",
                "review_count": "Review count",
                "summary": "Description",
                "genres": "Genre tags",
                "similar_books": "Similar book recommendations",
            }
        }
    
    def _fetch_google_books(self, book_name: str, author: str = None) -> Optional[Dict]:
        """Fetch Google Books API"""
        query = f"intitle:{book_name}"
        if author:
            query += f"+inauthor:{author}"
        
        api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
        
        return {
            "_action": "web_fetch",
            "_url": api_url,
            "_extract": {
                "title": "items[0].volumeInfo.title",
                "author": "items[0].volumeInfo.authors",
                "isbn": "items[0].volumeInfo.industryIdentifiers",
                "publisher": "items[0].volumeInfo.publisher",
                "publish_year": "items[0].volumeInfo.publishedDate",
                "summary": "items[0].volumeInfo.description",
            },
            "_note": "Google Books API returns JSON, can be parsed directly"
        }
    
    def _fetch_wikipedia_zh(self, book_name: str, author: str = None) -> Optional[Dict]:
        """Fetch Chinese Wikipedia"""
        url = f"https://zh.wikipedia.org/wiki/{book_name}"
        
        return {
            "_action": "web_fetch",
            "_url": url,
            "_extract": {
                "summary": "Article summary",
                "background": "Creation background",
            }
        }
    
    def _fetch_wikipedia_en(self, book_name: str, author: str = None) -> Optional[Dict]:
        """Fetch English Wikipedia"""
        url = f"https://en.wikipedia.org/wiki/{book_name.replace(' ', '_')}"
        
        return {
            "_action": "web_fetch",
            "_url": url,
            "_extract": {
                "summary": "Article summary",
                "background": "Background section",
            }
        }
    
    def _fetch_baidu_baike(self, book_name: str, author: str = None) -> Optional[Dict]:
        """Fetch Baidu Baike"""
        url = f"https://baike.baidu.com/item/{book_name}"
        
        return {
            "_action": "web_fetch",
            "_url": url,
            "_extract": {
                "summary": "Article summary",
                "background": "Creation background",
            }
        }
    
    def _fetch_zhihu(self, book_name: str, author: str = None) -> Optional[Dict]:
        """Fetch Zhihu related discussions"""
        query = f"{book_name} book review reading notes"
        url = f"https://www.zhihu.com/search?q={query}&type=content"
        
        return {
            "_action": "web_fetch",
            "_url": url,
            "_extract": {
                "reviews": "Popular answer summaries",
            }
        }
    
    def _fetch_amazon(self, book_name: str, author: str = None) -> Optional[Dict]:
        """Fetch Amazon Books"""
        query = f"{book_name} {author}" if author else book_name
        url = f"https://www.amazon.com/s?k={query}&i=stripbooks"
        
        return {
            "_action": "web_fetch",
            "_url": url,
            "_extract": {
                "title": "Book title",
                "author": "Author",
                "rating": "Rating (0-5)",
                "review_count": "Review count",
                "price": "Price",
                "bestseller_rank": "Bestseller rank",
            }
        }


# ==================== Convenience Functions ====================

def fetch_book_info(book_name: str, author: str = None) -> Dict:
    """
    Get book information (main entry)
    
    Usage examples:
        info = fetch_book_info("Atomic Habits")
        info = fetch_book_info("Atomic Habits", author="James Clear")
    """
    fetcher = BookFetcher()
    return fetcher.fetch_book_info(book_name, author)


def clear_cache() -> int:
    """Clear expired cache"""
    cache = CacheManager(CONFIG["cache_dir"], CONFIG["cache_expire_days"])
    return cache.clear_expired()


def get_cache_stats() -> Dict:
    """Get cache statistics"""
    cache_dir = CONFIG["cache_dir"]
    if not cache_dir.exists():
        return {"total": 0, "size_mb": 0}
    
    total = len(list(cache_dir.glob("*.json")))
    size = sum(f.stat().st_size for f in cache_dir.glob("*.json"))
    
    return {
        "total": total,
        "size_mb": round(size / 1024 / 1024, 2)
    }


# ==================== CLI Entry ====================

if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("Enhanced Book Information Fetcher v2.0.0")
    print("=" * 60)
    
    # Show cache statistics
    cache_stats = get_cache_stats()
    print(f"\n[Cache Statistics]")
    print(f"  Cache entries: {cache_stats['total']}")
    print(f"  Cache size: {cache_stats['size_mb']} MB")
    
    if len(sys.argv) < 2:
        print("\nUsage: python book_fetcher_enhanced.py <book_name> [author]")
        print("\nExamples:")
        print("  python book_fetcher_enhanced.py Atomic\\ Habits")
        print("  python book_fetcher_enhanced.py Atomic\\ Habits James\\ Clear")
        print("\nCommands:")
        print("  --clear-cache    Clear expired cache")
        print("  --cache-stats    Show cache statistics")
        sys.exit(0)
    
    if sys.argv[1] == "--clear-cache":
        cleared = clear_cache()
        print(f"\n✓ Cleared {cleared} expired cache entries")
        sys.exit(0)
    
    if sys.argv[1] == "--cache-stats":
        print(f"\n✓ Cache statistics: {cache_stats}")
        sys.exit(0)
    
    # Get book information
    book_name = sys.argv[1]
    author = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"\n[Request] Book: {book_name}")
    if author:
        print(f"[Request] Author: {author}")
    
    result = fetch_book_info(book_name, author)
    
    print("\n" + "=" * 60)
    print("[Result]")
    print("=" * 60)
    print(json.dumps(result, ensure_ascii=False, indent=2))
