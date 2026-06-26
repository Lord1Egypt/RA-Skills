#!/usr/bin/env python3
"""
Everything Search - Core Module

Provides Python interface to Everything HTTP Server API.
"""

import urllib.request
import urllib.parse
import json
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SearchItem:
    """Represents a single search result item."""

    name: str
    path: str
    full_path: str
    item_type: str  # "file" or "folder"
    size: int = 0
    date_modified: Optional[str] = None

    def format_size(self) -> str:
        """Format file size in human-readable format."""
        if self.size == 0:
            return "0 B"
        elif self.size < 1024:
            return f"{self.size} B"
        elif self.size < 1024 * 1024:
            return f"{self.size / 1024:.1f} KB"
        else:
            return f"{self.size / (1024 * 1024):.1f} MB"


@dataclass
class SearchResult:
    """Represents complete search results."""

    keyword: str
    total: int
    items: List[SearchItem]
    query_time: float = 0.0


class EverythingSearch:
    """
    Python client for Everything HTTP Server API.

    Usage:
        search = EverythingSearch(port=2853)
        results = search.search("数据资产")
        print(f"Found {results.total} results")
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 2853, timeout: int = 10):
        """
        Initialize Everything Search client.

        Args:
            host: Everything HTTP Server host (default: 127.0.0.1)
            port: Everything HTTP Server port (default: 2853)
            timeout: Request timeout in seconds (default: 10)
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.base_url = f"http://{host}:{port}/"

    def _build_url(self, keyword: str, **params) -> str:
        """Build search URL with encoded keyword and parameters."""
        encoded = urllib.parse.quote(keyword)
        url = f"{self.base_url}?search={encoded}&json=1"

        for key, value in params.items():
            url += f"&{key}={value}"

        return url

    def search(
        self,
        keyword: str,
        file_type: Optional[str] = None,
        min_size: Optional[str] = None,
        max_size: Optional[str] = None,
        path: Optional[str] = None,
        exclude_path: Optional[str] = None,
        modified_after: Optional[str] = None,
        max_results: int = 100,
        include_size: bool = True,
    ) -> SearchResult:
        """
        Search for files/folders.

        Args:
            keyword: Search keyword (supports Chinese)
            file_type: Filter by file extension (e.g., "jpg", "pdf")
            min_size: Minimum file size (e.g., "1mb", "100kb")
            max_size: Maximum file size
            path: Search only in this path
            exclude_path: Exclude this path from search
            modified_after: Only files modified after date (YYYY-MM-DD)
            max_results: Maximum number of results to return
            include_size: Include file size in results

        Returns:
            SearchResult object with total count and list of SearchItem
        """
        import time

        start_time = time.time()

        # Build search query
        query = keyword

        # Add filters
        if file_type:
            query += f" ext:{file_type}"
        if min_size:
            query += f" size:>{min_size}"
        if max_size:
            query += f" size:<{max_size}"
        if path:
            query += f' path:"{path}"'
        if exclude_path:
            query += f' !path:"{exclude_path}"'
        if modified_after:
            query += f" dm:>{modified_after}"

        # Build URL
        params = {
            "maxresults": max_results,
        }
        if include_size:
            params["size"] = 1

        url = self._build_url(query, **params)

        # Execute search
        try:
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "Mozilla/5.0 (Everything Search Client)")

            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))

                total = data.get("totalResults", 0)
                results = data.get("results", [])

                items = []
                for item in results:
                    name = item.get("name", "")
                    path = item.get("path", "")
                    item_type = item.get("type", "file")
                    size = item.get("size", 0)

                    full_path = f"{path}\\{name}" if path else name

                    items.append(
                        SearchItem(
                            name=name,
                            path=path,
                            full_path=full_path,
                            item_type=item_type,
                            size=size,
                        )
                    )

                query_time = time.time() - start_time

                return SearchResult(
                    keyword=keyword, total=total, items=items, query_time=query_time
                )

        except urllib.error.URLError as e:
            raise ConnectionError(f"Failed to connect to Everything HTTP Server: {e}")
        except Exception as e:
            raise RuntimeError(f"Search failed: {e}")

    def search_photos(
        self, person_name: str, formats: List[str] = None
    ) -> SearchResult:
        """
        Search for photos of a specific person.

        Args:
            person_name: Person's name (e.g., "张三")
            formats: List of image formats to search (default: ["jpg", "png"])

        Returns:
            SearchResult with photo files
        """
        if formats is None:
            formats = ["jpg", "png"]

        # Search for each format
        all_items = []
        total = 0

        for fmt in formats:
            try:
                results = self.search(f"{person_name} {fmt}", max_results=50)
                total += results.total
                all_items.extend(results.items)
            except Exception:
                continue

        # Sort by name
        all_items.sort(key=lambda x: x.name)

        return SearchResult(
            keyword=f"{person_name} photos",
            total=total,
            items=all_items[:100],  # Limit to 100 results
        )

    def search_documents(
        self, keyword: str, doc_types: List[str] = None
    ) -> SearchResult:
        """
        Search for document files.

        Args:
            keyword: Search keyword
            doc_types: List of document types (default: ["pdf", "docx", "xlsx", "pptx"])

        Returns:
            SearchResult with document files
        """
        if doc_types is None:
            doc_types = ["pdf", "docx", "xlsx", "pptx", "md", "txt"]

        all_items = []
        total = 0

        for doc_type in doc_types:
            try:
                results = self.search(f"{keyword} {doc_type}", max_results=50)
                total += results.total
                all_items.extend(results.items)
            except Exception:
                continue

        all_items.sort(key=lambda x: x.name)

        return SearchResult(
            keyword=f"{keyword} documents", total=total, items=all_items[:100]
        )

    def check_connection(self) -> bool:
        """
        Check if Everything HTTP Server is accessible.

        Returns:
            True if connection successful, False otherwise
        """
        import socket

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((self.host, self.port))
            sock.close()

            if result == 0:
                # Try HTTP request
                req = urllib.request.Request(self.base_url)
                with urllib.request.urlopen(req, timeout=5) as response:
                    return response.status == 200
            return False

        except Exception:
            return False


# Convenience function for quick searches
def quick_search(keyword: str, port: int = 2853, max_results: int = 20) -> List[str]:
    """
    Quick search function - returns list of full paths.

    Args:
        keyword: Search keyword
        port: Everything HTTP Server port
        max_results: Maximum results to return

    Returns:
        List of full file paths
    """
    search = EverythingSearch(port=port)
    results = search.search(keyword, max_results=max_results)
    return [item.full_path for item in results.items]
