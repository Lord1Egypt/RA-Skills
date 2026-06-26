#!/usr/bin/env python3
"""
arXiv Research Assistant (Local File System Version)
"""

import arxiv
import argparse
import json
import os
import csv
import re
import requests
import time
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', 'paper_list'))
CSV_PATH = os.path.join(WORKSPACE_DIR, 'paper_list.csv')

class LocalArxivManager:
    def __init__(self):
        self.client = arxiv.Client()
        self._init_workspace()

    def _init_workspace(self):
        Path(WORKSPACE_DIR).mkdir(parents=True, exist_ok=True)
        if not os.path.exists(CSV_PATH):
            with open(CSV_PATH, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['arxiv ID', 'title', 'abstract'])

    def _get_downloaded_ids(self) -> set:
        downloaded = set()
        if os.path.exists(CSV_PATH):
            with open(CSV_PATH, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    downloaded.add(row['arxiv ID'])
        return downloaded

    def _sanitize_filename(self, text: str) -> str:
        text = re.sub(r'[\\/*?:"<>|]', "", text)
        text = text.replace('\n', ' ').strip()
        return text

    def search(self, query: str, max_results: int = 15, sort_by: str = "relevance") -> list:
        
        sort_criterion = arxiv.SortCriterion.Relevance
        if sort_by == "date":
            sort_criterion = arxiv.SortCriterion.SubmittedDate

        ai_categories = "(cat:cs.AI OR cat:cs.CV OR cat:cs.LG OR cat:cs.CL OR cat:cs.NE OR cat:cs.RO OR cat:stat.ML)"
        
        if "cat:" not in query:
            full_query = f"({query}) AND {ai_categories}"
        else:
            full_query = query

        search = arxiv.Search(
            query=full_query,
            max_results=max_results,
            sort_by=sort_criterion
        )
        
        downloaded_ids = self._get_downloaded_ids()
        results = []
        
        for paper in self.client.results(search):
            paper_id = paper.entry_id.split("/")[-1].split("v")[0] 
            results.append({
                "arxiv_id": paper_id,
                "title": paper.title,
                "abstract": paper.summary.replace('\n', ' '),
                "comment": paper.comment if paper.comment else "",
                "published": paper.published.strftime('%Y-%m-%d') if paper.published else "",
                "is_downloaded": paper_id in downloaded_ids
            })
            
        return results

    def download(self, arxiv_id: str) -> dict:
        downloaded_ids = self._get_downloaded_ids()
        
        clean_id = arxiv_id.replace("arXiv:", "").replace("arxiv:", "").split("v")[0]
        
        if clean_id in downloaded_ids:
            return {"status": "skipped", "message": f"Paper {clean_id} is already in paper_list.csv, skip download."}

        search = arxiv.Search(id_list=[clean_id])
        papers = list(self.client.results(search))
        
        if not papers:
            return {"status": "error", "message": f"No papers were found with the ID {clean_id}."}
            
        paper = papers[0]
        sanitized_title = self._sanitize_filename(paper.title)
        filename = f"{clean_id}_{sanitized_title}.pdf"
        
        try:
            pdf_url = paper.pdf_url
            if not pdf_url.endswith('.pdf'):
                pdf_url += '.pdf'
                
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            max_retries = 3
            for attempt in range(max_retries):
                time.sleep(3)
                
                response = requests.get(pdf_url, stream=True, timeout=60, headers=headers)
                
                if response.status_code == 429:
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 10
                        print(f"A 429 rate limit has been triggered. We will wait {wait_time} seconds before attempting the {attempt + 2}th retry...")
                        time.sleep(wait_time)
                        continue
                    else:
                        response.raise_for_status()
                else:
                    response.raise_for_status()
                    break
            
            filepath = os.path.join(WORKSPACE_DIR, filename)
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            with open(CSV_PATH, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([clean_id, paper.title, paper.summary.replace('\n', ' ')])
                
            return {
                "status": "success", 
                "message": f"Successful streaming download and recording: {filename}",
                "path": filepath
            }
        except Exception as e:
            filepath = os.path.join(WORKSPACE_DIR, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
            return {"status": "error", "message": f"Streaming download failed: {str(e)}"}

def main():
    parser = argparse.ArgumentParser(description="ArXiv CLI for OpenClaw")
    subparsers = parser.add_subparsers(dest="command")
    
    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("query", help="Search keywords")
    search_parser.add_argument("--max", type=int, default=15, help="Maximum number of results")
    search_parser.add_argument("--sort", choices=["relevance", "date"], default="relevance", help="Sorting method")
    
    dl_parser = subparsers.add_parser("download")
    dl_parser.add_argument("arxiv_id", help="ArXiv ID")
    
    args = parser.parse_args()
    manager = LocalArxivManager()
    
    if args.command == "search":
        results = manager.search(args.query, args.max, args.sort)
        print(json.dumps(results, indent=2, ensure_ascii=False))
        
    elif args.command == "download":
        result = manager.download(args.arxiv_id)
        print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()