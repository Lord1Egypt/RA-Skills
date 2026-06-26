#!/usr/bin/env python3
"""
book_fetcher.py - Deep Reader Book Information Fetcher

Function: Automatically fetch book metadata and content summary from multiple sources
Data sources: Douban, Wikipedia, Google Books, Zhihu reviews, etc.

Usage (in OpenClaw):
    from book_fetcher import fetch_book_info
    info = fetch_book_info("Atomic Habits")
    
Return structure:
    {
        "title": str,           # Book title
        "author": str,          # Author
        "isbn": str,            # ISBN
        "publisher": str,       # Publisher
        "publish_year": int,    # Publication year
        "rating": float,        # Douban rating
        "review_count": int,    # Review count
        "summary": str,         # Book summary
        "chapters": list,       # Table of contents / chapter list
        "background": str,      # Creation background (for vertical analysis)
        "similar_books": [...], # Similar books (for horizontal analysis)
        "sources": [...]        # Data source URL list
    }
"""

import re
from typing import Dict, List, Optional
import json


def fetch_book_info(book_name: str) -> Dict:
    """
    Get complete book information by book name
    
    Args:
        book_name: Book name (supports Chinese/English)
        
    Returns:
        Structured book information dictionary
    """
    result = {
        "title": book_name,
        "author": None,
        "isbn": None,
        "publisher": None,
        "publish_year": None,
        "rating": None,
        "review_count": None,
        "summary": None,
        "chapters": [],
        "background": None,
        "similar_books": [],
        "sources": []
    }
    
    # Step 1: Search Douban page
    douban_data = _fetch_douban(book_name)
    if douban_data:
        result.update(douban_data)
        result["sources"].append(f"Douban: https://book.douban.com/subject_search?search_text={book_name}")
    
    # Step 2: If detailed info not found, try Wikipedia
    if not result.get("summary"):
        wiki_data = _fetch_wikipedia(book_name)
        if wiki_data:
            result.update(wiki_data)
            result["sources"].append("Wikipedia")
    
    # Step 3: Search creation background
    if not result.get("background"):
        background = _search_background(book_name)
        result["background"] = background
    
    # Step 4: Search similar book recommendations
    if not result.get("similar_books"):
        similar = _find_similar_books(book_name, result.get("category", "books"))
        result["similar_books"] = similar
    
    return result


def _fetch_douban(book_name: str) -> Optional[Dict]:
    """
    Fetch Douban book information
    
    Note: Due to Douban anti-scraping, this provides the logical framework.
    In actual OpenClaw environment, use web_fetch tool instead of direct HTTP requests.
    """
    # This is pseudo-code framework, actual execution should be defined in SKILL.md
    
    search_url = f"https://book.douban.com/subject_search?search_text={book_name}"
    
    # Expected parsing logic (implemented by AI during execution)
    expected_structure = {
        "title": "Extract first matching book title from search results",
        "author": "Extract from author field",
        "rating": "Extract rating number (0-10)",
        "review_count": "Extract from 'X people rated'",
        "summary": "Extract from 'Summary' paragraph",
        "publisher": "Extract from publication info",
        "publish_year": "Extract publication year (4 digits)",
        "chapters": "Extract from 'Table of Contents' or 'Excerpt'"
    }
    
    print(f"[info] Please use web_fetch on the following URL to get Douban info:")
    print(f"[info] {search_url}")
    print(f"[info] Expected fields to extract: {list(expected_structure.keys())}")
    
    return None  # Actual execution filled by AI calling web_fetch


def _fetch_wikipedia(book_name: str) -> Optional[Dict]:
    """
    Fetch book information from Wikipedia (if exists)
    """
    # Same framework requiring AI to call web_fetch
    
    zh_url = f"https://zh.wikipedia.org/wiki/{book_name}"
    en_url = f"https://en.wikipedia.org/wiki/{book_name.replace(' ', '_')}"
    
    print(f"[info] Try accessing Wikipedia:")
    print(f"[info] Chinese: {zh_url}")
    print(f"[info] English: {en_url}")
    
    return None


def _search_background(book_name: str) -> str:
    """
    Search creation background and writing motivation
    
    Returns: Background summary synthesized from multiple search results
    """
    query = f"{book_name} creation background writing motivation author interview"
    
    print(f"[info] Please use duckduckgo-search on the following query:")
    print(f"[info] Query: {query}")
    print(f"[info] Suggest getting top 3-5 results and summarize")
    
    return None


def _find_similar_books(book_name: str, category: str = "books") -> List[Dict]:
    """
    Find similar book recommendations
    """
    query = f"{category} classic books ranking TOP10"
    
    print(f"[info] Please use duckduckgo-search on the following query:")
    print(f"[info] Query: {query}")
    print(f"[info] Suggest taking top 5 results as competitive comparison reference")
    
    return []


# ====== Sample data below (for testing) ======

SAMPLE_BOOK_DATA = {
    "Atomic Habits": {
        "title": "Atomic Habits: Tiny Changes, Remarkable Results",
        "author": "James Clear",
        "isbn": "9780735211292",
        "publisher": "Avery",
        "publish_year": 2018,
        "rating": 9.1,
        "review_count": 180000,
        "summary": "Every action you take is a vote for the type of person you wish to become. This book provides a systematic method to build good habits and break bad ones.",
        "chapters": [
            "Part 1: The Fundamentals",
            "Chapter 1: Why Habits Matter - Small habits lead to big results",
            "Chapter 2: How Your Identity Affects Habits",
            "...",
            "Part 2: The Four Laws of Behavior Change",
            "...",
            "Part 3: Advanced Tactics",
            "...",
            "Conclusion"
        ],
        "background": "James Clear suffered a severe accident in a baseball game during high school and spent three years recovering. This experience led him to research habits and human behavior, with his blog articles accumulating over 10 million readers.",
        "similar_books": [
            {"title": "The Power of Habit", "author": "Charles Duhigg", "rating": 8.2},
            {"title": "Deep Work", "author": "Cal Newport", "rating": 8.4},
            {"title": "Essentialism", "author": "Greg McKeown", "rating": 8.0}
        ]
    },
    "The Black Swan": {
        "title": "The Black Swan: The Impact of the Highly Improbable",
        "author": "Nassim Nicholas Taleb",
        "isbn": "9780812973815",
        "publisher": "Random House",
        "publish_year": 2010,
        "rating": 8.4,
        "review_count": 65000,
        "summary": "A few extreme events have far more impact than most ordinary events. Taleb proposes a philosophy and methodology for dealing with uncertainty.",
        "chapters": [
            "Part 1: The Black Swan's Genesis",
            "Chapter 1: A Report on the Giants",
            "...",
            "Part 2: Blind Observation",
            "...",
            "Part 3: The Black Swan's Protection Mechanism",
            "...",
            "Part 4: The Ethics of the Black Swan",
            "Epilogue: Don't Be a Turkey"
        ],
        "background": "Taleb worked as a trader on Wall Street for many years, experiencing multiple financial market crises. He crystallized his thoughts on uncertainty into this book, which became Financial Times' Best Book of the Year.",
        "similar_books": [
            {"title": "Antifragile", "author": "Nassim Taleb", "rating": 8.3},
            {"title": "Fooled by Randomness", "author": "Nassim Taleb", "rating": 8.1},
            {"title": "Thinking, Fast and Slow", "author": "Daniel Kahneman", "rating": 8.5}
        ]
    }
}


# CLI test entry
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python book_fetcher.py <book_name>")
        print("\nSample book data:")
        for name in SAMPLE_BOOK_DATA:
            print(f"  - {name}")
        sys.exit(1)
    
    book_name = sys.argv[1]
    
    if book_name in SAMPLE_BOOK_DATA:
        print(json.dumps(SAMPLE_BOOK_DATA[book_name], ensure_ascii=False, indent=2))
    else:
        print(f"\n[Note] '{book_name}' has no sample data")
        print("[Note] This script needs to work with OpenClaw's web_fetch/duckduckgo-search tools")
        print("\nFetch workflow to implement:")
        print("1. Call web_fetch to get Douban page")
        print("2. Call duckduckgo-search to search creation background")
        print("3. Call web_fetch to get related reviews")
        print("4. Synthesize all sources into structured output")
