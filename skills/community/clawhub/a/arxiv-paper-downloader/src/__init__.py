"""
arXiv Paper Downloader Skill

Download AI/ML papers from arXiv with pre-curated collections.
"""

from .skill import (
    ArxivDownloader,
    download_papers,
    download_by_arxiv_ids,
    list_categories,
    get_category_info
)

__all__ = [
    "ArxivDownloader",
    "download_papers",
    "download_by_arxiv_ids",
    "list_categories",
    "get_category_info",
]

__version__ = "1.0.0"
