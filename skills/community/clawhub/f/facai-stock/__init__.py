"""
stock 包公开 API
---
from stock import get_detail, get_detail_by_name, search_by_name, get_all_stocks
"""

from stock.quote import get_detail, get_detail_by_name
from stock.search import get_all_stocks, search_by_name

__all__ = ["get_detail", "get_detail_by_name", "search_by_name", "get_all_stocks"]
