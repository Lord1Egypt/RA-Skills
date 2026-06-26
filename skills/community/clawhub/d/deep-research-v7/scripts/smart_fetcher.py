#!/usr/bin/env python3
"""
smart_fetcher.py - 智能获取器（简化版v1.0）
多策略冗余获取，自动选择最优策略
"""

import requests
import re
import json
from urllib.parse import urlparse
from typing import Dict, Any, Optional


class SmartFetcher:
    """智能获取器"""
    
    def __init__(self, url: str, domain: str = "general"):
        self.url = url
        self.domain = domain
        self.result = {
            "url": url,
            "success": False,
            "strategy_used": None,
            "error": None,
            "content": None
        }
    
    def fetch(self) -> Dict[str, Any]:
        """执行智能获取"""
        # 识别来源类型
        if "arxiv.org" in self.url.lower():
            return self._fetch_arxiv()
        elif "pubmed" in self.url.lower():
            return self._fetch_pubmed()
        else:
            return self._fetch_generic()
    
    def _fetch_arxiv(self) -> Dict[str, Any]:
        """arXiv获取策略：PDF优先，API备用"""
        # 策略1: PDF直链
        try:
            pdf_url = self.url.replace("/abs/", "/pdf/").replace(".abs", "")
            if not pdf_url.endswith(".pdf"):
                pdf_url += ".pdf"
            
            resp = requests.get(pdf_url, timeout=30)
            if resp.status_code == 200 and len(resp.content) > 1000:
                self.result["success"] = True
                self.result["strategy_used"] = "arxiv_pdf"
                self.result["content_type"] = "pdf"
                self.result["pdf_bytes"] = resp.content
                return self.result
        except Exception as e:
            self.result["pdf_error"] = str(e)
        
        # 策略2: arXiv API获取元数据
        try:
            arxiv_id = self._extract_arxiv_id(self.url)
            if arxiv_id:
                import feedparser
                feed = feedparser.parse(f"http://export.arxiv.org/api/query?id_list={arxiv_id}")
                if feed.entries:
                    entry = feed.entries[0]
                    self.result["success"] = True
                    self.result["strategy_used"] = "arxiv_api"
                    self.result["content_type"] = "api_metadata"
                    self.result["metadata"] = {
                        "title": entry.title,
                        "authors": [a.name for a in entry.authors] if hasattr(entry, 'authors') else [],
                        "published": entry.published[:10] if hasattr(entry, 'published') else None,
                        "summary": entry.summary if hasattr(entry, 'summary') else "",
                        "arxiv_id": arxiv_id
                    }
                    return self.result
        except Exception as e:
            self.result["api_error"] = str(e)
        
        self.result["error"] = "All arXiv strategies failed"
        return self.result
    
    def _fetch_pubmed(self) -> Dict[str, Any]:
        """PubMed获取策略"""
        try:
            # 提取PMID
            pmid_match = re.search(r'/(\d+)', urlparse(self.url).path)
            if pmid_match:
                pmid = pmid_match.group(1)
                # 使用E-utilities API
                summary_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid}&retmode=json"
                resp = requests.get(summary_url, timeout=15)
                data = resp.json()
                
                if "result" in data and pmid in data["result"]:
                    article = data["result"][pmid]
                    self.result["success"] = True
                    self.result["strategy_used"] = "pubmed_api"
                    self.result["content_type"] = "pubmed_metadata"
                    self.result["metadata"] = {
                        "title": article.get("title"),
                        "authors": [a.get("name") for a in article.get("authors", [])],
                        "published": article.get("pubdate"),
                        "pmid": pmid
                    }
                    return self.result
        except Exception as e:
            self.result["error"] = f"PubMed fetch failed: {str(e)}"
        
        return self.result
    
    def _fetch_generic(self) -> Dict[str, Any]:
        """通用网页获取"""
        try:
            resp = requests.get(self.url, timeout=30, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            if resp.status_code == 200:
                self.result["success"] = True
                self.result["strategy_used"] = "generic_web"
                self.result["content_type"] = "html"
                self.result["html"] = resp.text
                return self.result
        except Exception as e:
            self.result["error"] = f"Generic fetch failed: {str(e)}"
        
        return self.result
    
    def _extract_arxiv_id(self, url: str) -> Optional[str]:
        """从URL提取arXiv ID"""
        match = re.search(r'arXiv[/:](\d+\.\d+)', url, re.IGNORECASE)
        if match:
            return match.group(1)
        # 尝试从路径提取
        path = urlparse(url).path
        match = re.search(r'/(\d+\.\d+)', path)
        if match:
            return match.group(1)
        return None


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="智能获取器（简化版v1.0）")
    parser.add_argument("url", help="目标URL")
    parser.add_argument("--domain", "-d", default="general", help="研究领域")
    parser.add_argument("--output", "-o", help="输出JSON文件路径")
    
    args = parser.parse_args()
    
    fetcher = SmartFetcher(args.url, args.domain)
    result = fetcher.fetch()
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"✅ 结果已保存: {args.output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    return 0 if result["success"] else 1


if __name__ == "__main__":
    exit(main())
