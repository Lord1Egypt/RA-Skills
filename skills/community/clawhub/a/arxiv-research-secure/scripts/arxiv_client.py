#!/usr/bin/env python3
"""
ArXiv Research Assistant Secure
Zero-shell ArXiv paper search with caching and research tracking.
"""

import os
import re
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Optional, Tuple
import xml.etree.ElementTree as ET

# ============== CONFIGURATION ==============

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", Path.home() / ".openclaw" / "workspace"))
CACHE_DIR = WORKSPACE / ".arxiv_cache"
PAPERS_DIR = CACHE_DIR / "papers"
METADATA_DIR = CACHE_DIR / "metadata"
RESEARCH_LOG = WORKSPACE / "memory" / "arxiv_research_log.md"

ARXIV_API_BASE = "https://export.arxiv.org/api/query"
ARXIV_PDF_BASE = "https://arxiv.org/pdf"

ALLOWED_HOSTS = ["export.arxiv.org", "arxiv.org"]
MAX_QUERY_LENGTH = 200
TIMEOUT_SECONDS = 30
MAX_RESULTS_DEFAULT = 10
MAX_RESULTS_LIMIT = 100

# XML Namespaces
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

# ============== DATA CLASSES ==============

@dataclass
class ArxivPaper:
    id: str
    title: str
    authors: List[str]
    summary: str
    published: str
    updated: str
    categories: List[str]
    pdf_url: str
    
    def to_dict(self):
        return asdict(self)
    
    @property
    def paper_id_clean(self) -> str:
        """Extract clean ID from arXiv URL."""
        return self.id.split('/')[-1].replace('abs/', '')

# ============== SECURITY ==============

def validate_query(query: str) -> Tuple[bool, str]:
    """Validate search query for injection attempts."""
    forbidden = [';', '|', '&', '$', '`', '"', "'", '<', '>', '..', '//', '\\', '\n', '\r']
    
    if not query or len(query.strip()) == 0:
        return False, "Query cannot be empty"
    
    if len(query) > MAX_QUERY_LENGTH:
        return False, f"Query too long (max {MAX_QUERY_LENGTH} chars)"
    
    for char in forbidden:
        if char in query:
            return False, f"Invalid character in query: '{char}'"
    
    return True, query.strip()

def safe_urlopen(url: str, timeout: int = TIMEOUT_SECONDS) -> Tuple[bool, bytes, str]:
    """Safely fetch URL with validation."""
    try:
        parsed = urllib.parse.urlparse(url)
        
        if parsed.hostname not in ALLOWED_HOSTS:
            return False, b"", f"FORBIDDEN_HOST: {parsed.hostname} not in allowlist"
        
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "ArXivResearchSecure/1.0 (compatible; research tool)"
            }
        )
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = response.read()
            return True, data, f"OK: {len(data)} bytes"
            
    except urllib.error.HTTPError as e:
        return False, b"", f"HTTP_ERROR: {e.code} {e.reason}"
    except urllib.error.URLError as e:
        return False, b"", f"URL_ERROR: {e.reason}"
    except Exception as e:
        return False, b"", f"ERROR: {e}"

# ============== CACHE MANAGEMENT ==============

def ensure_cache_dirs():
    """Create cache directories."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    PAPERS_DIR.mkdir(exist_ok=True)
    METADATA_DIR.mkdir(exist_ok=True)

def get_cached_metadata(paper_id: str) -> Optional[dict]:
    """Get cached paper metadata."""
    cache_file = METADATA_DIR / f"{paper_id}.json"
    if cache_file.exists():
        with open(cache_file, 'r') as f:
            return json.load(f)
    return None

def cache_metadata(paper: ArxivPaper):
    """Cache paper metadata."""
    ensure_cache_dirs()
    cache_file = METADATA_DIR / f"{paper.paper_id_clean}.json"
    with open(cache_file, 'w') as f:
        json.dump(paper.to_dict(), f, indent=2)

def is_paper_cached(paper_id: str) -> bool:
    """Check if paper PDF is cached."""
    pdf_file = PAPERS_DIR / f"{paper_id}.pdf"
    return pdf_file.exists()

def cache_stats() -> dict:
    """Get cache statistics."""
    ensure_cache_dirs()
    
    papers_size = sum(f.stat().st_size for f in PAPERS_DIR.glob("*.pdf"))
    meta_count = len(list(METADATA_DIR.glob("*.json")))
    
    return {
        "papers_cached": len(list(PAPERS_DIR.glob("*.pdf"))),
        "metadata_cached": meta_count,
        "total_size_mb": round(papers_size / 1024 / 1024, 2),
        "cache_dir": str(CACHE_DIR)
    }

# ============== API CLIENT ==============

def parse_atom_entry(entry: ET.Element) -> ArxivPaper:
    """Parse Atom XML entry to Paper object."""
    def get_text(tag: str, ns: str = "atom") -> str:
        elem = entry.find(f"{ns}:{tag}", ATOM_NS)
        return elem.text if elem is not None else ""
    
    # Authors
    authors = []
    for author in entry.findall("atom:author", ATOM_NS):
        name = author.find("atom:name", ATOM_NS)
        if name is not None:
            authors.append(name.text)
    
    # Categories
    categories = []
    for cat in entry.findall("atom:category", ATOM_NS):
        term = cat.get("term")
        if term:
            categories.append(term)
    
    # PDF link
    pdf_url = ""
    for link in entry.findall("atom:link", ATOM_NS):
        if link.get("title") == "pdf":
            pdf_url = link.get("href", "")
            break
    
    return ArxivPaper(
        id=get_text("id"),
        title=get_text("title").replace("\n", " "),
        authors=authors,
        summary=get_text("summary").replace("\n", " "),
        published=get_text("published"),
        updated=get_text("updated"),
        categories=categories,
        pdf_url=pdf_url
    )

def search_arxiv(
    query: str,
    max_results: int = 10,
    sort_by: str = "relevance",
    sort_order: str = "descending",
    date_from: Optional[str] = None,
    date_to: Optional[str] = None
) -> Tuple[bool, List[ArxivPaper], str]:
    """Search ArXiv API."""
    
    # Validate query
    valid, msg = validate_query(query)
    if not valid:
        return False, [], msg
    
    # Build query URL
    search_query = msg
    
    # Add date constraints if provided
    if date_from:
        search_query += f"+AND+submittedDate:[{date_from}+TO+"
        if date_to:
            search_query += f"{date_to}]"
        else:
            search_query += "NOW]"
    
    # Sort parameters
    sort_map = {
        "relevance": "relevance",
        "date": "submittedDate",
        "updated": "lastUpdatedDate"
    }
    
    params = urllib.parse.urlencode({
        "search_query": f"all:{search_query}",
        "start": 0,
        "max_results": min(max_results, MAX_RESULTS_LIMIT),
        "sortBy": sort_map.get(sort_by, "relevance"),
        "sortOrder": sort_order
    })
    
    url = f"{ARXIV_API_BASE}?{params}"
    
    # Fetch
    success, data, msg = safe_urlopen(url)
    if not success:
        return False, [], msg
    
    # Parse XML
    try:
        root = ET.fromstring(data)
        entries = root.findall("atom:entry", ATOM_NS)
        
        papers = []
        for entry in entries:
            paper = parse_atom_entry(entry)
            papers.append(paper)
            # Cache metadata
            cache_metadata(paper)
        
        return True, papers, f"Found {len(papers)} papers"
        
    except ET.ParseError as e:
        return False, [], f"XML_PARSE_ERROR: {e}"

def fetch_paper_pdf(paper_id: str) -> Tuple[bool, str]:
    """Download paper PDF."""
    ensure_cache_dirs()
    
    # Clean paper ID
    clean_id = paper_id.replace("arXiv:", "").strip()
    
    # Check cache
    pdf_path = PAPERS_DIR / f"{clean_id}.pdf"
    if pdf_path.exists():
        return True, str(pdf_path)
    
    # Download
    pdf_url = f"{ARXIV_PDF_BASE}/{clean_id}.pdf"
    success, data, msg = safe_urlopen(pdf_url, timeout=60)
    
    if not success:
        return False, msg
    
    # Save
    try:
        with open(pdf_path, 'wb') as f:
            f.write(data)
        return True, str(pdf_path)
    except Exception as e:
        return False, f"SAVE_ERROR: {e}"

# ============== RESEARCH LOGGING ==============

def log_paper(paper: ArxivPaper, notes: str = "") -> Tuple[bool, str]:
    """Log paper to research journal."""
    ensure_cache_dirs()
    
    timestamp = datetime.now().strftime("%Y-%m-%d")
    paper_id = paper.paper_id_clean
    
    entry = f"""
## [{timestamp}] {paper.title}
- **arXiv ID**: `{paper_id}`
- **Authors**: {', '.join(paper.authors[:3])}{' et al.' if len(paper.authors) > 3 else ''}
- **Published**: {paper.published[:10]}
- **Categories**: {', '.join(paper.categories[:3])}
- **Summary**: {paper.summary[:300]}...
- **Notes**: {notes}
- **PDF**: {'✅ Downloaded' if is_paper_cached(paper_id) else '❌ Not downloaded'}

---
"""
    
    try:
        RESEARCH_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(RESEARCH_LOG, 'a', encoding='utf-8') as f:
            f.write(entry)
        return True, f"Logged to {RESEARCH_LOG}"
    except Exception as e:
        return False, f"LOG_ERROR: {e}"

def list_log() -> Tuple[bool, List[dict], str]:
    """Parse research log entries."""
    if not RESEARCH_LOG.exists():
        return True, [], "No research log found"
    
    try:
        with open(RESEARCH_LOG, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple parsing - extract entries
        entries = []
        for block in content.split("---"):
            if "## [" in block:
                lines = block.strip().split("\n")
                title = ""
                paper_id = ""
                for line in lines:
                    if line.startswith("## ["):
                        title = line.split("]", 1)[1].strip() if "]" in line else line
                    if "arXiv ID" in line:
                        paper_id = line.split("`")[1] if "`" in line else ""
                
                if title:
                    entries.append({
                        "title": title,
                        "paper_id": paper_id,
                        "preview": block[:200] + "..."
                    })
        
        return True, entries, f"Found {len(entries)} logged papers"
        
    except Exception as e:
        return False, [], f"PARSE_ERROR: {e}"

# ============== OUTPUT FORMATTERS ==============

def format_papers_table(papers: List[ArxivPaper]) -> str:
    """Format papers as markdown table."""
    lines = ["| ID | Title | Authors | Date | Category |", "|---|---|---|---|---|"]
    
    for p in papers:
        authors = ', '.join(p.authors[:2]) + (' et al.' if len(p.authors) > 2 else '')
        date = p.published[:10]
        cat = p.categories[0] if p.categories else "N/A"
        lines.append(f"| {p.paper_id_clean} | {p.title[:50]}... | {authors[:30]} | {date} | {cat} |")
    
    return '\n'.join(lines)

def export_log_json() -> Tuple[bool, str]:
    """Export research log as JSON."""
    success, entries, msg = list_log()
    if not success:
        return False, msg
    
    export_data = {
        "exported_at": datetime.now().isoformat(),
        "total_papers": len(entries),
        "papers": entries
    }
    
    export_path = WORKSPACE / "arxiv_research_export.json"
    with open(export_path, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    return True, str(export_path)

# ============== MAIN ==============

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No command provided"}, indent=2))
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    # SEARCH
    if cmd == "search":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Query required"}, indent=2))
            sys.exit(1)
        
        query = sys.argv[2]
        max_results = 10
        sort_by = "relevance"
        
        # Parse optional args
        for arg in sys.argv[3:]:
            if arg.startswith("--max="):
                max_results = int(arg.split("=")[1])
            elif arg.startswith("--sort="):
                sort_by = arg.split("=")[1]
        
        success, papers, msg = search_arxiv(query, max_results=max_results, sort_by=sort_by)
        
        result = {
            "success": success,
            "message": msg,
            "count": len(papers),
            "papers": [p.to_dict() for p in papers]
        }
        
        if success and papers:
            result["table"] = format_papers_table(papers)
        
        print(json.dumps(result, indent=2))
    
    # FETCH
    elif cmd == "fetch":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Paper ID required"}, indent=2))
            sys.exit(1)
        
        paper_id = sys.argv[2]
        success, msg = fetch_paper_pdf(paper_id)
        print(json.dumps({"success": success, "pdf_path": msg if success else None, "message": msg}, indent=2))
    
    # LOG
    elif cmd == "log":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Paper ID required"}, indent=2))
            sys.exit(1)
        
        paper_id = sys.argv[2]
        notes = sys.argv[3] if len(sys.argv) > 3 else ""
        
        # First get paper metadata from cache or API
        cached = get_cached_metadata(paper_id)
        if cached:
            paper = ArxivPaper(**cached)
        else:
            # Search for this specific paper
            success, papers, _ = search_arxiv(f"id:{paper_id}", max_results=1)
            if success and papers:
                paper = papers[0]
            else:
                print(json.dumps({"error": f"Paper {paper_id} not found"}, indent=2))
                sys.exit(1)
        
        success, msg = log_paper(paper, notes)
        print(json.dumps({"success": success, "message": msg}, indent=2))
    
    # LIST-LOG
    elif cmd == "list-log":
        success, entries, msg = list_log()
        print(json.dumps({"success": success, "entries": entries, "message": msg}, indent=2))
    
    # CACHE-STATS
    elif cmd == "cache-stats":
        stats = cache_stats()
        print(json.dumps({"success": True, "stats": stats}, indent=2))
    
    # EXPORT-LOG
    elif cmd == "export-log":
        success, msg = export_log_json()
        print(json.dumps({"success": success, "export_path": msg if success else None, "message": msg}, indent=2))
    
    else:
        print(json.dumps({"error": f"Unknown command: {cmd}"}, indent=2))

if __name__ == "__main__":
    main()
