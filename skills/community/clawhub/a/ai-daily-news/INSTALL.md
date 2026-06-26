# AI Daily News Skill - Installation Guide

## Quick Install

```bash
# 1. Install skill to OpenClaw
clawhub install ai-daily-news.skill

# 2. Or manually extract
cd ~/.openclaw/workspace/skills
unzip ai-daily-news.skill -d ai-daily-news
```

## Setup

```bash
cd ai-daily-news

# Install dependencies
pip install -r references/requirements.txt
playwright install chromium

# Configure
python scripts/setup_config.py

# Or manually copy and edit config
cp references/config.example.json config.json
# Edit config.json with your settings
```

## Usage

### Manual Run

```bash
# Collect news
python scripts/collect_ai_news.py

# Push to Feishu
python scripts/push_to_feishu.py
```

### Scheduled Run

```bash
# Windows
python scripts/daily_scheduler.py

# Or use Task Scheduler
schtasks /create /tn "AI-News-Collect" /tr "python scripts/collect_ai_news.py" /sc daily /st 06:00
schtasks /create /tn "AI-News-Push" /tr "python scripts/push_to_feishu.py" /sc daily /st 08:00
```

## Configuration

Edit `config.json`:

```json
{
  "feishu": {
    "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx",
    "chat_id": "oc_xxx"
  },
  "sources": {
    "arxiv": { "enabled": true },
    "youtube": { "enabled": true },
    "paperweekly": {
      "enabled": true,
      "rss_url": "https://rsshub.app/zhihu/column/paperweekly"
    }
  }
}
```

## Features

- 📚 arXiv papers (cs.CL, cs.LG, cs.AI)
- 📺 YouTube AI creators (Andrew Ng, Matt Wolfe, etc.)
- 🚀 Product Hunt AI products
- 🤗 Hugging Face papers
- 📰 PaperWeekly RSS
- 🌐 Browser fallback when APIs fail

## File Structure

```
ai-daily-news/
├── SKILL.md                    # Skill documentation
├── scripts/                    # Executable scripts
│   ├── collect_ai_news.py      # Main collector
│   ├── youtube_collector.py    # YouTube videos
│   ├── rss_collector.py        # RSS feeds
│   ├── browser_fallback.py     # Browser scraping
│   ├── push_to_feishu.py       # Report & push
│   ├── daily_scheduler.py      # Scheduler
│   ├── setup_config.py         # Config helper
│   └── package_skill.py        # Packaging
└── references/                 # Documentation
    ├── config.example.json     # Config template
    ├── requirements.txt        # Dependencies
    └── DEVELOPMENT.md          # Dev guide
```

## Troubleshooting

**ImportError**: Run `pip install -r references/requirements.txt`

**Playwright errors**: Run `playwright install chromium`

**No data collected**: Check internet connection and config.json settings

**Feishu push fails**: Verify webhook URL and chat_id

## License

MIT
