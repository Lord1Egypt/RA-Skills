#!/usr/bin/env python3
"""
arxiv-explorer CLI
Search, download, and summarize arXiv papers
"""

import argparse
import sys
import urllib.request
import urllib.parse
import json
import re
from datetime import datetime

ARXIV_API_URL = "http://export.arxiv.org/api/query"


def search_papers(query, max_results=10, sort_by="relevance"):
    """Search arXiv papers"""
    sort_map = {
        "relevance": "relevance",
        "date": "submittedDate",
        "updated": "lastUpdatedDate"
    }
    
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": sort_map.get(sort_by, "relevance"),
        "sortOrder": "descending"
    }
    
    url = f"{ARXIV_API_URL}?{urllib.parse.urlencode(params)}"
    
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read().decode('utf-8')
            return parse_atom_feed(data)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return []


def parse_atom_feed(xml_data):
    """Parse arXiv Atom feed"""
    papers = []
    
    # Extract entries using regex (lightweight, no external deps)
    entry_pattern = r'<entry>(.*?)</entry>'
    entries = re.findall(entry_pattern, xml_data, re.DOTALL)
    
    for entry in entries:
        paper = {}
        
        # Title
        title_match = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
        paper['title'] = clean_text(title_match.group(1)) if title_match else "N/A"
        
        # Summary
        summary_match = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL)
        paper['summary'] = clean_text(summary_match.group(1)) if summary_match else "N/A"
        
        # Authors
        author_matches = re.findall(r'<name>(.*?)</name>', entry)
        paper['authors'] = author_matches if author_matches else ["N/A"]
        
        # arXiv ID
        id_match = re.search(r'<id>http://arxiv.org/abs/(.*?)</id>', entry)
        paper['id'] = id_match.group(1) if id_match else "N/A"
        
        # Published date
        published_match = re.search(r'<published>(.*?)</published>', entry)
        paper['published'] = published_match.group(1)[:10] if published_match else "N/A"
        
        # PDF link
        if paper['id'] != "N/A":
            paper['pdf_url'] = f"https://arxiv.org/pdf/{paper['id']}.pdf"
        
        papers.append(paper)
    
    return papers


def clean_text(text):
    """Clean up XML text"""
    text = text.replace('\n', ' ').replace('  ', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def format_paper(paper, index=None):
    """Format paper for display"""
    prefix = f"[{index}] " if index else ""
    lines = [
        f"{prefix}{paper['title']}",
        f"    Authors: {', '.join(paper['authors'][:3])}{'...' if len(paper['authors']) > 3 else ''}",
        f"    Date: {paper['published']} | ID: {paper['id']}",
        f"    PDF: {paper.get('pdf_url', 'N/A')}",
        f"    Summary: {paper['summary'][:200]}..." if len(paper['summary']) > 200 else f"    Summary: {paper['summary']}",
        ""
    ]
    return '\n'.join(lines)


def download_pdf(arxiv_id, output_path=None):
    """Download PDF from arXiv"""
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    
    if not output_path:
        output_path = f"{arxiv_id.replace('/', '_')}.pdf"
    
    try:
        print(f"Downloading {arxiv_id}...")
        urllib.request.urlretrieve(pdf_url, output_path)
        print(f"Saved to: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error downloading PDF: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(description='arXiv Paper Explorer')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search papers')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('-n', '--num', type=int, default=10, help='Number of results')
    search_parser.add_argument('-s', '--sort', choices=['relevance', 'date', 'updated'], 
                               default='relevance', help='Sort order')
    search_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Download command
    download_parser = subparsers.add_parser('download', help='Download PDF')
    download_parser.add_argument('arxiv_id', help='arXiv ID (e.g., 2401.12345)')
    download_parser.add_argument('-o', '--output', help='Output filename')
    
    # Recent command
    recent_parser = subparsers.add_parser('recent', help='Get recent papers by category')
    recent_parser.add_argument('category', help='Category (e.g., cs.AI, cs.CL, physics)')
    recent_parser.add_argument('-n', '--num', type=int, default=10, help='Number of results')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'search':
        papers = search_papers(args.query, args.num, args.sort)
        
        if not papers:
            print("No papers found.")
            return
        
        if args.json:
            print(json.dumps(papers, indent=2))
        else:
            print(f"\nFound {len(papers)} papers for '{args.query}':\n")
            for i, paper in enumerate(papers, 1):
                print(format_paper(paper, i))
    
    elif args.command == 'download':
        download_pdf(args.arxiv_id, args.output)
    
    elif args.command == 'recent':
        # Search by category prefix
        query = f"cat:{args.category}*"
        papers = search_papers(query, args.num, 'date')
        
        if not papers:
            print("No papers found.")
            return
        
        print(f"\nRecent {len(papers)} papers in {args.category}:\n")
        for i, paper in enumerate(papers, 1):
            print(format_paper(paper, i))


if __name__ == '__main__':
    main()
