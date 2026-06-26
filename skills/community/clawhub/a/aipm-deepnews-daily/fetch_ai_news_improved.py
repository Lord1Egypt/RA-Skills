#!/usr/bin/env python3
"""
AI News Digest - 自动抓取 AI 领域资讯并翻译成中文
改进版：过滤未来日期和过旧文章
"""

import asyncio
import feedparser
import json
import os
import re
import sys
import hashlib
from datetime import datetime, timedelta, timezone
from pathlib import Path
from googletrans import Translator

# RSS 源列表 - AI 领域优质来源
RSS_FEEDS = {
    # 科技新闻
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "The Verge AI": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "Ars Technica AI": "https://feeds.arstechnica.com/arstechnica/technology-lab",
    "MIT Technology Review AI": "https://www.technologyreview.com/topic/artificial-intelligence/feed",

    # AI 专业博客
    "OpenAI Blog": "https://openai.com/blog/rss.xml",
    "Google AI Blog": "https://blog.google/technology/ai/rss/",
    "DeepMind Blog": "https://deepmind.google/blog/rss.xml",
    "Anthropic Blog": "https://www.anthropic.com/rss.xml",
    "Hugging Face Blog": "https://huggingface.co/blog/feed.xml",

    # 社区与播客
    "Latent Space": "https://www.latent.space/feed",
    "The Cognitive Revolution": "https://feeds.buzzsprout.com/2139927.rss",

    # 论文 (arXiv AI)
    "arXiv cs.AI": "https://rss.arxiv.org/rss/cs.AI",
    "arXiv cs.CL": "https://rss.arxiv.org/rss/cs.CL",

    # Reddit
    "r/MachineLearning": "https://www.reddit.com/r/MachineLearning/top/.rss?t=day",
    "r/LocalLLaMA": "https://www.reddit.com/r/LocalLLaMA/top/.rss?t=day",

    # Hacker News AI
    "Hacker News": "https://hnrss.org/newest?q=AI+OR+LLM+OR+GPT+OR+Claude+OR+machine+learning&points=50",
}

# 已处理文章的缓存文件
CACHE_FILE = Path(__file__).parent / "seen_articles.json"
OUTPUT_FILE = Path(__file__).parent / "latest_digest.md"
MAX_ARTICLES_PER_FEED = 5
MAX_TOTAL_ARTICLES = 30
MAX_DAYS_OLD = 3  # 最多显示3天内的文章


def load_cache():
    """加载已处理文章缓存"""
    if CACHE_FILE.exists():
        try:
            data = json.loads(CACHE_FILE.read_text())
            # 清理超过7天的缓存
            cutoff = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
            return {k: v for k, v in data.items() if v.get("ts", "") > cutoff}
        except (json.JSONDecodeError, KeyError):
            return {}
    return {}


def save_cache(cache):
    """保存缓存"""
    CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=2))


def article_id(entry):
    """生成文章唯一ID"""
    key = entry.get("link", "") or entry.get("title", "")
    return hashlib.md5(key.encode()).hexdigest()


def parse_feed_date(date_str):
    """解析 RSS 日期字符串"""
    if not date_str:
        return None
    
    # 尝试多种日期格式
    formats = [
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%d %H:%M:%S%z",
        "%Y-%m-%d",
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except (ValueError, TypeError):
            continue
    
    # 如果无法解析，返回 None
    return None


def is_recent_article(entry):
    """检查文章是否在最近 MAX_DAYS_OLD 天内"""
    now = datetime.now(timezone.utc)
    
    # 获取发布日期
    published_str = entry.get("published", entry.get("updated", ""))
    published_date = parse_feed_date(published_str)
    
    if not published_date:
        # 如果没有发布日期，默认接受
        return True
    
    # 确保日期有时区信息
    if published_date.tzinfo is None:
        published_date = published_date.replace(tzinfo=timezone.utc)
    
    # 检查是否在未来（超过1天）
    if published_date > now + timedelta(days=1):
        return False
    
    # 检查是否太旧
    if published_date < now - timedelta(days=MAX_DAYS_OLD):
        return False
    
    return True


def fetch_feeds():
    """从所有 RSS 源抓取文章"""
    cache = load_cache()
    articles = []

    for source_name, feed_url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(feed_url)
            count = 0
            for entry in feed.entries:
                if count >= MAX_ARTICLES_PER_FEED:
                    break
                
                # 检查文章日期
                if not is_recent_article(entry):
                    continue
                
                aid = article_id(entry)
                if aid in cache:
                    continue

                title = entry.get("title", "无标题")
                link = entry.get("link", "")
                summary = entry.get("summary", entry.get("description", ""))
                # 清理 HTML 标签
                summary = re.sub(r"<[^>]+>", "", summary).strip()

                # 限制摘要长度
                if len(summary) > 500:
                    summary = summary[:500] + "..."

                published = entry.get("published", entry.get("updated", ""))

                articles.append({
                    "id": aid,
                    "source": source_name,
                    "title": title,
                    "link": link,
                    "summary": summary,
                    "published": published,
                })
                cache[aid] = {"ts": datetime.now(timezone.utc).isoformat()}
                count += 1
        except Exception as e:
            print(f"[WARN] 获取 {source_name} 失败: {e}", file=sys.stderr)
            continue

    save_cache(cache)

    # 限制总数
    return articles[:MAX_TOTAL_ARTICLES]


async def translate_text(text, translator):
    """翻译英文到中文"""
    if not text or not text.strip():
        return text
    try:
        result = await translator.translate(text, src="en", dest="zh-cn")
        return result.text
    except Exception as e:
        print(f"[WARN] 翻译失败: {e}", file=sys.stderr)
        return text  # 翻译失败返回原文


def format_digest(articles, translated_articles):
    """格式化为 Markdown 摘要"""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"🤖 **AI 资讯日报** - {now}",
        f"📰 共 {len(articles)} 条新资讯\n",
        "---\n",
    ]

    # 按来源分组
    grouped = {}
    for orig, trans in zip(articles, translated_articles):
        source = orig["source"]
        if source not in grouped:
            grouped[source] = []
        grouped[source].append((orig, trans))

    for source, items in grouped.items():
        lines.append(f"### 📌 {source}\n")
        for orig, trans in items:
            lines.append(f"**{trans['title']}**")
            if trans["summary"]:
                lines.append(f"> {trans['summary'][:200]}")
            if orig["link"]:
                lines.append(f"🔗 [原文链接]({orig['link']})")
            lines.append("")

    lines.append("---")
    lines.append("_由 OpenClaw AI News Digest 自动生成_")

    return "\n".join(lines)


async def main():
    print("📡 正在抓取 AI 资讯...", file=sys.stderr)
    articles = fetch_feeds()

    if not articles:
        print("今天没有新的 AI 资讯。")
        return

    print(f"📝 获取到 {len(articles)} 条新文章，正在翻译...", file=sys.stderr)

    translator = Translator()
    translated = []
    for art in articles:
        title = await translate_text(art["title"], translator)
        summary = await translate_text(art["summary"], translator)
        translated.append({
            "title": title,
            "summary": summary,
        })

    digest = format_digest(articles, translated)

    # 保存到文件
    OUTPUT_FILE.write_text(digest, encoding="utf-8")

    # 输出到 stdout（供 OpenClaw 读取）
    print(digest)


if __name__ == "__main__":
    asyncio.run(main())