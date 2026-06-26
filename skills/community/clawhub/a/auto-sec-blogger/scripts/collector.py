"""
News Collector - RSS/News 수집 모듈

RSS feeds (Google News, arXiv, HackerNews, Hada.io, Geeknews)에서 보안 관련 뉴스를 수집합니다.
SQLite를 사용하여 수집 이력을 영구 저장하고 중복을 방지합니다.
"""

import feedparser
import arxiv
import sqlite3
from typing import List, Dict, Optional
from datetime import datetime
import re
from urllib.parse import quote
from modules.intelligence.config import DB_PATH
from modules.intelligence.utils import setup_logger

logger = setup_logger(__name__, "collector.log")

class NewsCollector:
    """뉴스 수집기"""

    def __init__(self, keywords: List[str] = None):
        """
        초기화

        Args:
            keywords: 필터링할 키워드 리스트 (기본값: 보안 관련 키워드)
        """
        if keywords is None:
            keywords = [
                # Security
                "Vulnerability", "Security", "Cybersecurity", "CVE", "Exploit",
                "Zero-day", "Penetration Testing", "Web Security", "Network Security",
                "Malware", "Ransomware", "Phishing", "Threat", "Attack",
                "Injection", "XSS", "CSRF", "RCE", "Authentication", "Authorization",

                # AI
                "Artificial Intelligence", "Machine Learning", "Deep Learning",
                "Neural Network", "Transformer", "GPT", "LLM", "Diffusion",
                "Computer Vision", "NLP", "MLOps", "Model", "Training", "Inference",

                # LLM
                "Large Language Model", "ChatGPT", "Claude", "GPT-4", "Llama",
                "Prompt Engineering", "RAG", "Fine-tuning", "RLHF", "Token",
                "Context Window", "AI Agent", "Hallucination", "Alignment",

                # Agent
                "Agent", "AI Agent", "Autonomous Agent", "Multi-agent", "Swarm",
                "Workflow", "Automation", "Tool Use", "Function Calling",
                "Agent Framework", "LangChain", "AutoGPT", "BabyAGI",

                # Research/Tech
                "Research", "Paper", "arXiv", "Open Source", "Framework",
                "Library", "API", "GitHub", "Release", "Update", "Patch"
            ]
        self.keywords = keywords
        self._init_db()

    def _init_db(self):
        """SQLite DB 초기화"""
        try:
            self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS seen_articles (
                    url TEXT PRIMARY KEY,
                    collected_at TIMESTAMP
                )
            """)
            self.conn.commit()
        except Exception as e:
            logger.error(f"DB Initialization failed: {e}")
            raise

    def is_seen(self, url: str) -> bool:
        """URL 중복 확인"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT 1 FROM seen_articles WHERE url = ?", (url,))
            return cursor.fetchone() is not None
        except Exception as e:
            logger.error(f"DB Check failed for {url}: {e}")
            return False

    def add_seen(self, url: str):
        """URL 수집 이력 저장"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO seen_articles (url, collected_at) VALUES (?, ?)",
                (url, datetime.now())
            )
            self.conn.commit()
        except Exception as e:
            logger.error(f"DB Insert failed for {url}: {e}")

    def __del__(self):
        """소멸자: DB 연결 종료"""
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

    def fetch_google_news(self, keyword: str = "Cybersecurity", max_results: int = 10) -> List[Dict]:
        """Google News 수집"""
        logger.info(f"Fetching Google News for '{keyword}'...")
        encoded_keyword = quote(keyword)
        url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=en-US&gl=US&ceid=US:en"
        
        try:
            feed = feedparser.parse(url)
            articles = []

            for entry in feed.entries[:max_results]:
                if self.is_seen(entry.link):
                    continue

                article = {
                    "source": "Google News",
                    "title": entry.title,
                    "url": entry.link,
                    "published": entry.get("published", ""),
                    "summary": entry.get("summary", ""),
                    "keyword": keyword
                }
                articles.append(article)
                self.add_seen(entry.link)

            logger.info(f"  → Found {len(articles)} new articles")
            return articles
        except Exception as e:
            logger.error(f"Failed to fetch Google News: {e}")
            return []

    def fetch_arxiv(self, categories: List[str] = None, max_results: int = 10) -> List[Dict]:
        """arXiv 논문 수집"""
        logger.info("Fetching arXiv papers...")
        if categories is None:
            categories = ["cs.CR", "cs.LG", "cs.SE"]

        try:
            articles = []
            search = arxiv.Search(
                query="cat:cs.CR OR cat:cs.LG OR cat:cs.SE",
                max_results=max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate
            )

            for result in search.results():
                if self.is_seen(result.entry_id):
                    continue

                # 키워드 필터링
                title_lower = result.title.lower()
                summary_lower = result.summary.lower()
                if not any(keyword.lower() in title_lower or keyword.lower() in summary_lower
                        for keyword in self.keywords):
                    continue

                article = {
                    "source": "arXiv",
                    "title": result.title,
                    "url": result.entry_id,
                    "published": result.published.strftime("%Y-%m-%d %H:%M:%S"),
                    "summary": result.summary,
                    "authors": [author.name for author in result.authors],
                    "categories": result.categories
                }
                articles.append(article)
                self.add_seen(result.entry_id)

            logger.info(f"  → Found {len(articles)} new papers")
            return articles
        except Exception as e:
            logger.error(f"Failed to fetch arXiv: {e}")
            return []

    def fetch_hackernews(self, max_results: int = 10) -> List[Dict]:
        """HackerNews 수집"""
        logger.info("Fetching HackerNews...")
        url = "https://hnrss.org/frontpage"
        
        try:
            feed = feedparser.parse(url)
            articles = []

            for entry in feed.entries[:max_results]:
                if self.is_seen(entry.link):
                    continue

                title_lower = entry.title.lower()
                summary_lower = entry.get("summary", "").lower()
                if not any(keyword.lower() in title_lower or keyword.lower() in summary_lower
                        for keyword in self.keywords):
                    continue

                article = {
                    "source": "HackerNews",
                    "title": entry.title,
                    "url": entry.link,
                    "published": entry.get("published", ""),
                    "summary": entry.get("summary", ""),
                    "comments_url": entry.get("comments", "")
                }
                articles.append(article)
                self.add_seen(entry.link)

            logger.info(f"  → Found {len(articles)} new articles")
            return articles
        except Exception as e:
            logger.error(f"Failed to fetch HackerNews: {e}")
            return []

    def fetch_hadaio(self, max_results: int = 10) -> List[Dict]:
        """Hada.io 수집"""
        logger.info("Fetching Hada.io...")
        url = "https://news.hada.io/rss/news"
        
        try:
            feed = feedparser.parse(url)
            articles = []

            for entry in feed.entries[:max_results]:
                link = entry.get("link", entry.get("id", ""))
                if self.is_seen(link):
                    continue

                content = entry.get("content", [{}])[0].get("value", "") if entry.get("content") else ""
                summary_lower = entry.get("summary", content).lower()
                
                # Hada.io는 모두 수집 (필터링 최소화)
                article = {
                    "source": "Hada.io",
                    "title": entry.title,
                    "url": link,
                    "published": entry.get("published", ""),
                    "summary": summary_lower[:200] if summary_lower else "",
                    "comments_url": link
                }
                articles.append(article)
                self.add_seen(link)

            logger.info(f"  → Found {len(articles)} new articles")
            return articles
        except Exception as e:
            logger.error(f"Failed to fetch Hada.io: {e}")
            return []

    def fetch_geeknews(self, max_results: int = 10) -> List[Dict]:
        """Geeknews 수집"""
        return self.fetch_hadaio(max_results)

    def fetch_all(self, max_results_per_source: int = 10) -> List[Dict]:
        """모든 소스 수집"""
        all_articles = []

        for keyword in self.keywords[:3]:
            all_articles.extend(self.fetch_google_news(keyword, max_results_per_source))

        all_articles.extend(self.fetch_arxiv(max_results=max_results_per_source))
        all_articles.extend(self.fetch_hackernews(max_results=max_results_per_source))
        all_articles.extend(self.fetch_hadaio(max_results=max_results_per_source))
        all_articles.extend(self.fetch_geeknews(max_results=max_results_per_source))

        all_articles.sort(key=lambda x: x["published"], reverse=True)
        return all_articles

if __name__ == "__main__":
    collector = NewsCollector()
    articles = collector.fetch_all(max_results_per_source=2)
    print(f"Collected {len(articles)} new articles.")