# AI Daily News - Development Guide

## Architecture

```
ai-daily-news/
├── scripts/
│   ├── collect_ai_news.py      # Main orchestrator
│   ├── youtube_collector.py    # YouTube via yt-dlp + RSS
│   ├── rss_collector.py        # RSS feed parser
│   ├── browser_fallback.py     # Playwright fallback
│   ├── push_to_feishu.py       # Report & push
│   ├── daily_scheduler.py      # Task scheduler
│   └── setup_config.py         # Config initialization
└── references/
    ├── config.example.json     # Configuration template
    ├── requirements.txt        # Dependencies
    └── DEVELOPMENT.md          # This file
```

## Adding a New Data Source

### 1. Create Collector Module

Create `scripts/my_source_collector.py`:

```python
def fetch_my_source(config):
    """Fetch data from my source"""
    items = []
    # Implementation
    return items
```

### 2. Add Fallback Method

In `scripts/browser_fallback.py`:

```python
def fallback_my_source(config):
    """Browser-based fallback"""
    items = []
    # Playwright implementation
    return items
```

### 3. Integrate in Main Collector

In `scripts/collect_ai_news.py`:

```python
from my_source_collector import fetch_my_source
from browser_fallback import fallback_my_source

# In main():
if config.get('sources', {}).get('my_source', {}).get('enabled'):
    items = try_with_fallback(
        fetch_my_source,
        fallback_my_source,
        config=config['sources']['my_source']
    )
    all_news.extend(items)
```

### 4. Update Config Schema

Add to `references/config.example.json`:

```json
"my_source": {
  "enabled": true,
  "url": "",
  "max_items": 5
}
```

## Data Format

Each news item should be a dict:

```python
{
    "type": "论文|产品|视频|资讯",
    "tag": "[类型·来源]",
    "title": "Item title",
    "summary": "Brief description (max 200 chars)",
    "url": "https://...",
    "published": "2024-03-15",
    "source": "source_name"
}
```

## Testing

```bash
# Test individual collectors
python scripts/youtube_collector.py
python scripts/rss_collector.py

# Test full pipeline
python scripts/collect_ai_news.py
python scripts/push_to_feishu.py --dry-run
```

## Browser Fallback Testing

```bash
# Install Playwright
pip install playwright
playwright install chromium

# Test fallback
python -c "from browser_fallback import fallback_arxiv_papers; print(fallback_arxiv_papers())"
```

## Troubleshooting

### yt-dlp Issues

```bash
# Update yt-dlp
pip install -U yt-dlp

# Check YouTube access
yt-dlp --list-formats "https://youtube.com/watch?v=..."
```

### Playwright Issues

```bash
# Reinstall browsers
playwright install --force chromium

# Check installation
python -c "from playwright.sync_api import sync_playwright; print('OK')"
```

### RSS Feed Issues

Test RSS URL directly:
```bash
curl -s "https://rsshub.app/zhihu/column/paperweekly" | head -50
```

## Scheduling

### Windows Task Scheduler

```powershell
# Create scheduled task
schtasks /create /tn "AI News Collect" /tr "python scripts/collect_ai_news.py" /sc daily /st 06:00
schtasks /create /tn "AI News Push" /tr "python scripts/push_to_feishu.py" /sc daily /st 08:00
```

### Cron (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add lines:
0 6 * * * cd /path/to/ai-daily-news && python scripts/collect_ai_news.py
0 8 * * * cd /path/to/ai-daily-news && python scripts/push_to_feishu.py
```

## Packaging as Skill

```bash
# Validate skill
python scripts/package_skill.py ai-daily-news --validate

# Package skill
python scripts/package_skill.py ai-daily-news ./dist

# Results in: dist/ai-daily-news.skill
```
