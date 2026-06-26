#!/usr/bin/env python3
"""
paper-assistant: 从 OpenReview 和 arXiv 获取 Agent 相关论文
输出 JSON 格式的候选论文列表（已排除被拒论文和已推送论文）
"""

import json
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data")
PUSHED_FILE = os.path.join(DATA_DIR, "pushed.json")

# API endpoints
OPENREVIEW_SEARCH = "https://api2.openreview.net/notes/search"
ARXIV_API = "https://export.arxiv.org/api/query"

# Conference configs
CONFERENCES = [
    {"group": "ICLR.cc/2026/Conference", "label": "ICLR 2026"},
    {"group": "NeurIPS.cc/2025/Conference", "label": "NeurIPS 2025"},
]

ARXIV_QUERY = "cat:cs.AI+AND+all:agent+system"


def load_pushed():
    """Load already-pushed paper IDs."""
    if not os.path.exists(PUSHED_FILE):
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(PUSHED_FILE, "w") as f:
            json.dump({"pushed": []}, f)
        return set()
    with open(PUSHED_FILE, "r") as f:
        data = json.load(f)
    return set(data.get("pushed", []))


def fetch_openreview(group, label, limit=200):
    """Fetch accepted papers from OpenReview (all accepted papers, filter later)."""
    # Fetch all accepted papers without keyword filter, LLM will filter later
    url = f"{OPENREVIEW_SEARCH}?group={group}&limit={limit}"
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "paper-assistant/1.0")
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"[WARN] Failed to fetch {label}: {e}", file=sys.stderr)
        return []

    papers = []
    for note in data.get("notes", []):
        fc = note.get("forumContent", {})
        if not fc:
            continue

        # Extract venue info
        venueid = fc.get("venueid", {})
        venueid_val = venueid.get("value", "") if isinstance(venueid, dict) else str(venueid)
        venue = fc.get("venue", {})
        venue_val = venue.get("value", "") if isinstance(venue, dict) else str(venue)

        # Skip rejected papers
        if "Rejected" in venueid_val or "Rejected" in venue_val:
            continue

        # Only keep accepted (Poster/Spotlight/Oral)
        accepted = any(k in venue_val for k in ["Poster", "Spotlight", "Oral"])
        if not accepted:
            continue

        # Extract fields
        title = fc.get("title", {})
        title_val = title.get("value", "") if isinstance(title, dict) else str(title)

        abstract = fc.get("abstract", {})
        abstract_val = abstract.get("value", "") if isinstance(abstract, dict) else str(abstract)

        authors = fc.get("authors", {})
        authors_val = authors.get("value", []) if isinstance(authors, dict) else []

        pdf = fc.get("pdf", {})
        pdf_val = pdf.get("value", "") if isinstance(pdf, dict) else str(pdf)
        pdf_url = f"https://openreview.net{pdf_val}" if pdf_val else ""

        keywords = fc.get("keywords", {})
        keywords_val = keywords.get("value", []) if isinstance(keywords, dict) else []

        forum_id = note.get("forum", note.get("id", ""))

        papers.append({
            "id": f"openreview:{forum_id}",
            "title": title_val,
            "authors": authors_val if isinstance(authors_val, list) else [authors_val],
            "abstract": abstract_val,
            "pdf": pdf_url,
            "venue": venue_val,
            "source": label,
            "keywords": keywords_val if isinstance(keywords_val, list) else [],
        })

    return papers


def fetch_arxiv(max_results=50):
    """Fetch recent agent papers from arXiv (2026+)."""
    url = f"{ARXIV_API}?search_query={ARXIV_QUERY}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "paper-assistant/1.0")
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read().decode()
    except Exception as e:
        print(f"[WARN] Failed to fetch arXiv: {e}", file=sys.stderr)
        return []

    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(data)

    papers = []
    for entry in root.findall("a:entry", ns):
        published = entry.find("a:published", ns).text[:10]
        # Only 2026+ papers
        if published < "2026-01-01":
            continue

        title = entry.find("a:title", ns).text.strip().replace("\n", " ")
        summary = entry.find("a:summary", ns).text.strip().replace("\n", " ")
        arxiv_id = entry.find("a:id", ns).text  # e.g. http://arxiv.org/abs/2603.xxxxx
        arxiv_short = arxiv_id.split("/abs/")[-1] if "/abs/" in arxiv_id else arxiv_id

        authors = []
        for author in entry.findall("a:author", ns):
            name = author.find("a:name", ns)
            if name is not None:
                authors.append(name.text)

        papers.append({
            "id": f"arxiv:{arxiv_short}",
            "title": title,
            "authors": authors,
            "abstract": summary,
            "pdf": f"https://arxiv.org/pdf/{arxiv_short}",
            "venue": "arXiv preprint",
            "source": "arXiv 2026",
            "keywords": [],
        })

    return papers


def main():
    pushed = load_pushed()

    all_papers = []

    # Fetch from OpenReview
    for conf in CONFERENCES:
        papers = fetch_openreview(conf["group"], conf["label"])
        all_papers.extend(papers)
        print(f"[INFO] {conf['label']}: fetched {len(papers)} accepted papers", file=sys.stderr)

    # Fetch from arXiv
    arxiv_papers = fetch_arxiv()
    all_papers.extend(arxiv_papers)
    print(f"[INFO] arXiv: fetched {len(arxiv_papers)} papers (2026+)", file=sys.stderr)

    # Deduplicate by title (case-insensitive)
    seen_titles = set()
    unique_papers = []
    for p in all_papers:
        t = p["title"].lower().strip()
        if t not in seen_titles:
            seen_titles.add(t)
            unique_papers.append(p)

    # Filter out already pushed
    candidates = [p for p in unique_papers if p["id"] not in pushed]

    print(f"[INFO] Total unique: {len(unique_papers)}, already pushed: {len(unique_papers) - len(candidates)}, candidates: {len(candidates)}", file=sys.stderr)

    # Output candidates as JSON to stdout
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
    json.dump(candidates, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()