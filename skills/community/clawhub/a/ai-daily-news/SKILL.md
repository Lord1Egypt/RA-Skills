---
name: ai-daily-news
description: |
  Automated AI daily news collection and reporting system. Collects AI papers from arXiv, Hugging Face, AI products from Product Hunt, YouTube videos from AI creators, and RSS feeds like PaperWeekly. Generates structured daily reports and pushes to Feishu.
  
  Use when: (1) Setting up automated AI news collection, (2) Generating daily AI news reports, (3) Fetching latest arXiv papers, Hugging Face papers, Product Hunt AI products, YouTube AI videos, (4) Configuring news sources and scheduling, (5) Troubleshooting news collection issues.
---

# AI Daily News Skill

Automatically collect and report AI news from multiple sources with fallback browser scraping.

## Quick Start

```bash
# Install dependencies
pip install -r references/requirements.txt
playwright install chromium

# Configure
python scripts/setup_config.py

# Run collection
python scripts/collect_ai_news.py

# Generate and push report
python scripts/push_to_feishu.py
```

## Supported Data Sources

| Source | Primary Method | Fallback Method |
|--------|---------------|-----------------|
| arXiv Papers | RSS API | Playwright browser |
| Hugging Face Papers | RSS Feed | Playwright browser |
| Product Hunt | RSS Feed | Playwright browser |
| YouTube AI Creators | yt-dlp | Playwright browser |
| PaperWeekly | RSS | requests |
| Custom RSS | feedparser | requests |

## Configuration

Edit `references/config.example.json` or run `setup_config.py`:

```json
{
  "feishu": {
    "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx",
    "chat_id": "oc_xxx"
  },
  "sources": {
    "arxiv": {"enabled": true, "categories": ["cs.CL", "cs.LG", "cs.AI"]},
    "youtube": {
      "enabled": true,
      "creators": ["andrew_ng", "matt_wolfe", "ai_explained", "greg_isenberg"]
    },
    "paperweekly": {"enabled": true, "rss_url": ""}
  }
}
```

## YouTube Creators

Available creator keys:
- `andrew_ng` - 吴恩达 (DeepLearning.AI)
- `matt_wolfe` - Matt Wolfe
- `ai_explained` - AI Explained
- `ai_with_oliver` - AI with Oliver
- `greg_isenberg` - Greg Isenberg

## Scripts Overview

| Script | Purpose |
|--------|---------|
| `collect_ai_news.py` | Main collector with fallback logic |
| `youtube_collector.py` | YouTube video collection |
| `rss_collector.py` | RSS feed collection |
| `browser_fallback.py` | Browser-based fallback scraping |
| `push_to_feishu.py` | Report generation and Feishu push |
| `daily_scheduler.py` | Scheduled task runner |
| `setup_config.py` | Interactive configuration setup |

## Fallback Mechanism

When primary methods (RSS/API/yt-dlp) fail:
1. Automatically retries with browser-based scraping
2. Uses Playwright for JavaScript-rendered pages
3. Seamless integration - same output format
4. Logs fallback usage for monitoring

## Report Format

Generated reports include:
- 📚 arXiv papers with abstracts
- 🚀 Product Hunt AI products
- 🤗 Hugging Face papers
- 📺 YouTube video summaries
- 📰 PaperWeekly interpretations
- 📊 Source statistics

## Troubleshooting

**arXiv returns 0 papers**: Check `days_back` parameter or network connection
**YouTube fails**: Ensure yt-dlp is installed; fallback to Playwright available
**RSS timeouts**: Browser fallback will attempt direct requests
**Feishu push fails**: Verify webhook URL and chat_id in config

## Advanced: Adding Custom Sources

1. Add RSS feed to `rss` section in config
2. Or implement new collector in `scripts/`
3. Register in `collect_ai_news.py`
4. Add fallback method in `browser_fallback.py`

See `references/DEVELOPMENT.md` for detailed extension guide.
