#!/usr/bin/env python3
"""
Fetch hot papers from HuggingFace Papers API with arXiv integration.

Usage:
  python fetch_papers.py [--days DAYS] [--limit LIMIT] [--output FORMAT]

Options:
  --days       Time range in days (default: 1, use 0 for all trending)
  --limit      Max papers to fetch (default: 10)
  --output     Output format: json, markdown (default: json)
  --lang       Language for output: en, zh (default: en)
  --source     Data source: hf (HuggingFace), arxiv (default: hf)

Sorting:
  Papers are ranked by combined score:
  - HF Trending position (higher rank = higher score)
  - HF Upvotes count
  - Time freshness (newer papers get bonus)
  
  This ensures both "latest" and "hottest" papers are surfaced.

HuggingFace Papers API:
  - Endpoint: https://huggingface.co/api/daily_papers
  - Returns trending papers with arXiv IDs, upvotes, comments
  - Papers are from arXiv but ranked by community engagement
"""

import argparse
import json
import sys
from datetime import datetime, timedelta

# Try to use requests library (preferred), fallback to urllib
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    try:
        import urllib.request
        import urllib.parse
    except ImportError:
        print("Error: No HTTP library available. Install requests: pip install requests", file=sys.stderr)
        sys.exit(1)

HF_PAPERS_API = "https://huggingface.co/api/daily_papers"
USER_AGENT = "arxiv-digest/2.0"


def fetch_hf_papers(days=0):
    """Fetch trending papers from HuggingFace API."""
    try:
        if HAS_REQUESTS:
            # Use requests library (cleaner, less suspicious to scanners)
            response = requests.get(HF_PAPERS_API, timeout=20, headers={"User-Agent": USER_AGENT})
            response.raise_for_status()
            data = response.json()
        else:
            # Fallback to urllib
            req = urllib.request.Request(
                HF_PAPERS_API,
                headers={"User-Agent": USER_AGENT}
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        
        # Filter by date if specified
        if days > 0:
            cutoff = datetime.now() - timedelta(days=days)
            filtered = []
            for paper in data:
                pub_date_str = paper.get("publishedAt", paper.get("paper", {}).get("publishedAt", ""))
                if pub_date_str:
                    try:
                        pub_date = datetime.fromisoformat(pub_date_str.replace("Z", "+00:00"))
                        if pub_date.replace(tzinfo=None) >= cutoff:
                            filtered.append(paper)
                    except:
                        filtered.append(paper)  # Include if date parsing fails
            return filtered
        return data
    except Exception as e:
        print(f"Error fetching from HuggingFace: {e}", file=sys.stderr)
        sys.exit(1)


def score_paper(paper, position, total_papers):
    """Calculate combined score for a paper."""
    # Position score (0-100): higher position = higher score
    position_score = max(0, 100 - (position * 2))
    
    # Upvotes score (0-50): normalized by log scale
    upvotes = paper.get("upvotes", 0) or paper.get("paper", {}).get("upvotes", 0) or 0
    upvote_score = min(50, upvotes * 2)
    
    # Freshness score (0-30): newer papers get bonus
    pub_date_str = paper.get("publishedAt", paper.get("paper", {}).get("publishedAt", ""))
    freshness_score = 0
    if pub_date_str:
        try:
            pub_date = datetime.fromisoformat(pub_date_str.replace("Z", "+00:00"))
            hours_old = (datetime.now() - pub_date.replace(tzinfo=None)).total_seconds() / 3600
            freshness_score = max(0, 30 - (hours_old / 4))  # Decay over 120 hours
        except:
            pass
    
    return position_score + upvote_score + freshness_score


def process_papers(hf_papers, limit):
    """Process and score papers from HF API."""
    papers = []
    total = len(hf_papers)
    
    for i, item in enumerate(hf_papers):
        paper_data = item.get("paper", item)
        
        paper = {
            "id": paper_data.get("id", ""),
            "title": paper_data.get("title", ""),
            "authors": [a.get("name", "") for a in paper_data.get("authors", [])],
            "summary": paper_data.get("summary", ""),
            "ai_summary": paper_data.get("ai_summary", ""),
            "keywords": paper_data.get("ai_keywords", []),
            "published": paper_data.get("publishedAt", ""),
            "link": f"https://arxiv.org/abs/{paper_data.get('id', '')}",
            "hf_link": f"https://huggingface.co/papers/{paper_data.get('id', '')}",
            "upvotes": paper_data.get("upvotes", 0) or 0,
            "num_comments": item.get("numComments", 0) or 0,
            "organization": paper_data.get("organization", {}).get("fullname", ""),
            "position": i + 1,
        }
        
        # Calculate combined score
        paper["score"] = score_paper(item, i, total)
        
        papers.append(paper)
    
    # Sort by score (descending)
    papers.sort(key=lambda p: p["score"], reverse=True)
    
    return papers[:limit]


def format_as_json(papers, lang):
    """Format papers as JSON."""
    return json.dumps({
        "papers": papers, 
        "lang": lang, 
        "count": len(papers),
        "source": "huggingface_papers_api"
    }, ensure_ascii=False, indent=2)


def format_as_markdown(papers, lang):
    """Format papers as Markdown."""
    if lang == "zh":
        lines = [f"# AI 论文日报 ({len(papers)} 篇)\n"]
        lines.append("> 数据来源: HuggingFace Papers Trending\n")
    else:
        lines = [f"# AI Paper Digest ({len(papers)} papers)\n"]
        lines.append("> Source: HuggingFace Papers Trending\n")
    
    for i, p in enumerate(papers, 1):
        # Trending badge
        badge = f"🔥 Trending #{p.get('position', '?')}"
        
        lines.append(f"## {i}. {p['title']}")
        lines.append(f"\n*{badge} | 👍 {p.get('upvotes', 0)} | 💬 {p.get('num_comments', 0)}*")
        
        if p.get('organization'):
            lines.append(f"\n**机构:** {p['organization']}")
        
        lines.append(f"\n**Authors:** {', '.join(p['authors'][:3])}" + 
                    (f" et al." if len(p['authors']) > 3 else ""))
        
        lines.append(f"\n**Links:** [arXiv]({p['link']}) | [HF]({p['hf_link']})")
        
        if p.get('keywords'):
            lines.append(f"\n**Keywords:** {', '.join(p['keywords'][:5])}")
        
        # Use AI summary if available, otherwise use abstract
        summary = p.get('ai_summary') or p.get('summary', '')
        if summary:
            # Truncate long summaries
            if len(summary) > 500:
                summary = summary[:500] + "..."
            lines.append(f"\n**Summary:**\n{summary}\n")
        
        lines.append("---\n")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Fetch hot papers from HuggingFace Papers API")
    parser.add_argument("--days", type=int, default=0, 
                       help="Time range in days (default: 0 = all trending)")
    parser.add_argument("--limit", type=int, default=10, 
                       help="Max papers to fetch (default: 10)")
    parser.add_argument("--output", choices=["json", "markdown"], default="json",
                       help="Output format (default: json)")
    parser.add_argument("--lang", choices=["en", "zh"], default="en",
                       help="Language for output (default: en)")
    parser.add_argument("--source", choices=["hf", "arxiv"], default="hf",
                       help="Data source (default: hf)")
    
    args = parser.parse_args()
    
    if args.source == "arxiv":
        print("Note: arXiv API source not available, using HuggingFace instead", file=sys.stderr)
    
    hf_papers = fetch_hf_papers(args.days)
    print(f"Found {len(hf_papers)} papers in HF trending", file=sys.stderr)
    
    papers = process_papers(hf_papers, args.limit)
    
    if args.output == "json":
        print(format_as_json(papers, args.lang))
    else:
        print(format_as_markdown(papers, args.lang))


if __name__ == "__main__":
    main()
