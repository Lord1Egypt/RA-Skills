from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime
import hashlib
import feedparser
import httpx
from pydantic import BaseModel
from dateutil import parser
from apscheduler.schedulers.asyncio import AsyncIOScheduler

app = FastAPI(title="AI News API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RSS_FEEDS = [
    {"name": "OpenAI Blog", "url": "https://openai.com/blog/rss.xml", "category": "AI"},
    {"name": "Google AI Blog", "url": "https://ai.googleblog.com/feeds/posts/default", "category": "AI"},
    {"name": "MIT AI News", "url": "https://news.mit.edu/topic/artificial-intelligence2/feed", "category": "AI"},
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/", "category": "Technology"},
    {"name": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/feed/", "category": "Technology"},
    {"name": "Wired AI", "url": "https://www.wired.com/feed/tag/ai/latest/rss", "category": "Technology"},
]


class Article(BaseModel):
    id: str
    title: str
    source: str
    category: str
    link: str
    published_at: str
    summary: str
    content: Optional[str] = None


articles_db: List[Article] = []


def get_content_hash(title: str, link: str) -> str:
    return hashlib.md5(f"{title}:{link}".encode()).hexdigest()[:12]


async def fetch_feed(feed_config: dict) -> List[Article]:
    try:
        feed = feedparser.parse(feed_config["url"])
        results = []
        for entry in feed.entries[:20]:
            try:
                article_id = get_content_hash(entry.title, entry.link)
                published_date = parser.parse(entry.published) if hasattr(entry, "published") else datetime.now()
                summary = entry.summary if hasattr(entry, "summary") else ""
                results.append(Article(
                    id=article_id,
                    title=entry.title,
                    source=feed_config["name"],
                    category=feed_config["category"],
                    link=entry.link,
                    published_at=published_date.isoformat(),
                    summary=summary[:500]
                ))
            except Exception:
                continue
        return results
    except Exception:
        return []


async def refresh_articles():
    global articles_db
    new_articles = []
    seen_ids = set()
    for feed in RSS_FEEDS:
        feed_articles = await fetch_feed(feed)
        for article in feed_articles:
            if article.id not in seen_ids:
                seen_ids.add(article.id)
                new_articles.append(article)
    new_articles.sort(key=lambda x: x.published_at, reverse=True)
    articles_db = new_articles
    return new_articles


scheduler = AsyncIOScheduler()


@app.on_event("startup")
async def startup_event():
    await refresh_articles()
    scheduler.add_job(refresh_articles, 'interval', hours=6, id='refresh_rss')
    scheduler.start()


@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "articles": len(articles_db)}


@app.get("/api/articles", response_model=List[Article])
async def get_articles(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    source: Optional[str] = None,
    category: Optional[str] = None
):
    filtered = articles_db
    if source:
        filtered = [a for a in filtered if a.source == source]
    if category:
        filtered = [a for a in filtered if a.category == category]
    start = (page - 1) * limit
    end = start + limit
    return filtered[start:end]


@app.get("/api/articles/{article_id}", response_model=Optional[Article])
async def get_article(article_id: str):
    for article in articles_db:
        if article.id == article_id:
            return article
    return None


@app.get("/api/sources")
async def get_sources():
    return list(set(a.source for a in articles_db))


@app.get("/api/categories")
async def get_categories():
    return list(set(a.category for a in articles_db))


@app.post("/api/refresh")
async def trigger_refresh():
    refreshed = await refresh_articles()
    return {"count": len(refreshed), "status": "success"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
