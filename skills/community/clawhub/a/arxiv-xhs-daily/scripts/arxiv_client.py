from __future__ import annotations

import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Any

ARXIV_API = "http://export.arxiv.org/api/query"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}


def fetch_category_for_date(category: str, target_date: str | None = None, page_size: int = 200, max_scan_results: int = 800) -> list[dict[str, Any]]:
    papers: list[dict[str, Any]] = []
    start = 0
    resolved_target_date = target_date
    while start < max_scan_results:
        batch = _fetch_batch(category, start=start, max_results=min(page_size, max_scan_results - start))
        if not batch:
            break
        if resolved_target_date is None:
            resolved_target_date = (batch[0].get("published") or "")[:10]
        saw_older = False
        for paper in batch:
            published_date = (paper.get("published") or "")[:10]
            if published_date == resolved_target_date:
                papers.append(paper)
            elif published_date < resolved_target_date:
                saw_older = True
                break
        if saw_older:
            break
        start += len(batch)
        if len(batch) < page_size:
            break
    return papers


def _fetch_batch(category: str, start: int = 0, max_results: int = 100) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode(
        {
            "search_query": f"cat:{category}",
            "start": start,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
    )
    url = f"{ARXIV_API}?{params}"
    with urllib.request.urlopen(url, timeout=60) as response:
        payload = response.read()
    root = ET.fromstring(payload)
    papers: list[dict[str, Any]] = []
    for entry in root.findall("atom:entry", ATOM_NS):
        title = _node_text(entry, "atom:title")
        summary = _node_text(entry, "atom:summary")
        paper_id = _node_text(entry, "atom:id")
        published = _node_text(entry, "atom:published")
        updated = _node_text(entry, "atom:updated")
        authors = [node.text.strip() for node in entry.findall("atom:author/atom:name", ATOM_NS) if node.text]
        categories = [node.attrib.get("term", "") for node in entry.findall("atom:category", ATOM_NS)]
        papers.append(
            {
                "id": paper_id,
                "title": " ".join(title.split()),
                "summary": " ".join(summary.split()),
                "published": published,
                "updated": updated,
                "authors": authors,
                "categories": categories,
                "primary_category": category,
            }
        )
    return papers


def today_date_string() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def _node_text(entry: ET.Element, xpath: str) -> str:
    node = entry.find(xpath, ATOM_NS)
    return node.text.strip() if node is not None and node.text else ""
