#!/usr/bin/env python3
"""
ArXiv Watcher - Monitor and track new papers on arXiv.org

Usage:
    python arxiv_watcher.py fetch <category> [--limit N]
    python arxiv_watcher.py star <arxiv_id>
    python arxiv_watcher.py unstar <arxiv_id>
    python arxiv_watcher.py starred
"""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

# ArXiv API endpoints
ARXIV_API_URL = "http://export.arxiv.org/api/query"
ARXIV_NEW_URL = "https://arxiv.org/list/{category}/new"

# Atom namespace
ATOM_NS = "http://www.w3.org/2005/Atom"
ARXIV_NS = "http://arxiv.org/schemas/atom"

# Starred papers storage
STARRED_FILE = Path(__file__).parent.parent / "assets" / "starred.json"


def load_starred() -> dict:
    """Load starred papers from JSON file."""
    if not STARRED_FILE.exists():
        return {}
    try:
        with open(STARRED_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_starred(data: dict) -> None:
    """Save starred papers to JSON file."""
    STARRED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STARRED_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def parse_arxiv_id(url: str) -> str:
    """Extract arxiv_id from URL or return as-is."""
    match = re.search(r"(\d{4}\.\d{4,5}(?:v\d+)?)", url)
    if match:
        return match.group(1)
    return url


def fetch_papers_by_id(arxiv_id: str) -> dict | None:
    """Fetch a single paper by arXiv ID using id_list parameter."""
    # Remove version suffix for API query
    clean_id = re.sub(r'v\d+$', '', arxiv_id)
    
    params = {"id_list": clean_id}
    url = f"{ARXIV_API_URL}?" + "&".join(f"{k}={v}" for k, v in params.items())

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ArXiv-Watcher/1.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            xml_content = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        return None

    root = ET.fromstring(xml_content)
    entry = root.find(f"{{{ATOM_NS}}}entry")
    
    if entry is None:
        return None

    paper = {}
    
    # Extract ID
    id_elem = entry.find(f"{{{ATOM_NS}}}id")
    if id_elem is not None:
        paper["id"] = parse_arxiv_id(id_elem.text)
        paper["url"] = id_elem.text
        paper["pdf_url"] = f"https://arxiv.org/pdf/{paper['id']}.pdf"

    # Extract title
    title_elem = entry.find(f"{{{ATOM_NS}}}title")
    if title_elem is not None:
        paper["title"] = title_elem.text.strip().replace("\n", " ")

    # Extract authors
    authors = []
    for author in entry.findall(f"{{{ATOM_NS}}}author"):
        name_elem = author.find(f"{{{ATOM_NS}}}name")
        if name_elem is not None:
            authors.append(name_elem.text)
    paper["authors"] = authors

    # Extract summary
    summary_elem = entry.find(f"{{{ATOM_NS}}}summary")
    if summary_elem is not None:
        abstract = summary_elem.text.strip().replace("\n", " ")
        paper["abstract"] = abstract
        paper["abstract_preview"] = abstract[:200] + "..." if len(abstract) > 200 else abstract

    # Extract category
    category_elem = entry.find(f"{{{ARXIV_NS}}}primary_category")
    if category_elem is not None:
        paper["category"] = category_elem.get("term")

    # Extract published date
    published_elem = entry.find(f"{{{ATOM_NS}}}published")
    if published_elem is not None:
        paper["published"] = published_elem.text[:10]  # YYYY-MM-DD

    return paper


def fetch_papers_via_api(category: str, limit: int = 10) -> list:
    """Fetch papers using arXiv API."""
    # Build query URL
    query = f"cat:{category}"
    params = {
        "search_query": query,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": str(limit)
    }

    url = f"{ARXIV_API_URL}?" + "&".join(f"{k}={v}" for k, v in params.items())

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ArXiv-Watcher/1.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            xml_content = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        print(f"Error fetching papers: {e}", file=sys.stderr)
        return []

    # Parse Atom feed
    root = ET.fromstring(xml_content)
    papers = []

    for entry in root.findall(f"{{{ATOM_NS}}}entry"):
        paper = {}

        # Extract ID
        id_elem = entry.find(f"{{{ATOM_NS}}}id")
        if id_elem is not None:
            paper["id"] = parse_arxiv_id(id_elem.text)
            paper["url"] = id_elem.text
            paper["pdf_url"] = f"https://arxiv.org/pdf/{paper['id']}.pdf"

        # Extract title
        title_elem = entry.find(f"{{{ATOM_NS}}}title")
        if title_elem is not None:
            paper["title"] = title_elem.text.strip().replace("\n", " ")

        # Extract authors
        authors = []
        for author in entry.findall(f"{{{ATOM_NS}}}author"):
            name_elem = author.find(f"{{{ATOM_NS}}}name")
            if name_elem is not None:
                authors.append(name_elem.text)
        paper["authors"] = authors

        # Extract summary
        summary_elem = entry.find(f"{{{ATOM_NS}}}summary")
        if summary_elem is not None:
            abstract = summary_elem.text.strip().replace("\n", " ")
            paper["abstract"] = abstract
            paper["abstract_preview"] = abstract[:200] + "..." if len(abstract) > 200 else abstract

        # Extract category
        category_elem = entry.find(f"{{{ARXIV_NS}}}primary_category")
        if category_elem is not None:
            paper["category"] = category_elem.get("term")

        # Extract published date
        published_elem = entry.find(f"{{{ATOM_NS}}}published")
        if published_elem is not None:
            paper["published"] = published_elem.text[:10]  # YYYY-MM-DD

        papers.append(paper)

    return papers


def format_paper_markdown(paper: dict, is_starred: bool = False) -> str:
    """Format a paper as Markdown."""
    star = "⭐ " if is_starred else ""
    lines = [
        f"## {star}[{paper.get('id', 'N/A')}] {paper.get('title', 'No title')}",
        "",
        f"**Authors:** {', '.join(paper.get('authors', []))}",
        f"**Category:** {paper.get('category', 'N/A')}",
        f"**Submitted:** {paper.get('published', 'N/A')}",
        "",
        f"**Abstract:**",
        paper.get('abstract_preview', 'No abstract available'),
        "",
        "**Links:**",
        f"- arXiv: {paper.get('url', 'N/A')}",
        f"- PDF: {paper.get('pdf_url', 'N/A')}",
        "",
        "---",
        ""
    ]
    return "\n".join(lines)


def cmd_fetch(args):
    """Fetch papers from arXiv."""
    category = args.category
    limit = args.limit or 10

    print(f"Fetching latest papers from {category}...", file=sys.stderr)

    papers = fetch_papers_via_api(category, limit)

    if not papers:
        print("No papers found or error occurred.", file=sys.stderr)
        return 1

    starred = load_starred()

    for paper in papers:
        is_starred = paper.get("id") in starred
        print(format_paper_markdown(paper, is_starred))

    print(f"\nFound {len(papers)} papers.", file=sys.stderr)
    return 0


def cmd_star(args):
    """Star a paper."""
    arxiv_id = parse_arxiv_id(args.arxiv_id)

    starred = load_starred()

    if arxiv_id in starred:
        print(f"Paper {arxiv_id} is already starred.", file=sys.stderr)
        return 1

    # Fetch paper details by ID
    paper = fetch_papers_by_id(arxiv_id)

    if paper is None:
        # Store minimal info if fetch fails
        starred[arxiv_id] = {
            "id": arxiv_id,
            "url": f"https://arxiv.org/abs/{arxiv_id}",
            "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
            "starred_at": datetime.now().isoformat()
        }
    else:
        paper["starred_at"] = datetime.now().isoformat()
        starred[arxiv_id] = paper

    save_starred(starred)
    print(f"⭐ Starred paper {arxiv_id}")
    return 0


def cmd_unstar(args):
    """Unstar a paper."""
    arxiv_id = parse_arxiv_id(args.arxiv_id)

    starred = load_starred()

    if arxiv_id not in starred:
        print(f"Paper {arxiv_id} is not starred.", file=sys.stderr)
        return 1

    del starred[arxiv_id]
    save_starred(starred)
    print(f"Removed star from paper {arxiv_id}")
    return 0


def cmd_starred(args):
    """List starred papers."""
    starred = load_starred()

    if not starred:
        print("No starred papers yet.", file=sys.stderr)
        return 0

    print(f"You have {len(starred)} starred paper(s):\n")

    # Sort by starred_at descending
    papers = sorted(
        starred.values(),
        key=lambda p: p.get("starred_at", ""),
        reverse=True
    )

    for paper in papers:
        print(format_paper_markdown(paper, is_starred=True))

    return 0


def main():
    parser = argparse.ArgumentParser(description="ArXiv Watcher CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Fetch command
    fetch_parser = subparsers.add_parser("fetch", help="Fetch latest papers from a category")
    fetch_parser.add_argument("category", help="arXiv category (e.g., cs.AI)")
    fetch_parser.add_argument("--limit", "-n", type=int, default=10, help="Number of papers to fetch")

    # Star command
    star_parser = subparsers.add_parser("star", help="Star a paper")
    star_parser.add_argument("arxiv_id", help="arXiv ID (e.g., 2403.12345)")

    # Unstar command
    unstar_parser = subparsers.add_parser("unstar", help="Unstar a paper")
    unstar_parser.add_argument("arxiv_id", help="arXiv ID (e.g., 2403.12345)")

    # Starred command
    subparsers.add_parser("starred", help="List starred papers")

    args = parser.parse_args()

    if args.command == "fetch":
        return cmd_fetch(args)
    elif args.command == "star":
        return cmd_star(args)
    elif args.command == "unstar":
        return cmd_unstar(args)
    elif args.command == "starred":
        return cmd_starred(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
