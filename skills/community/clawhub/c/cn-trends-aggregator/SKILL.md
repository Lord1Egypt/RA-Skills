---
name: cn-hot-trends
description: "中文+全球热榜聚合器。一键获取百度热榜、今日头条、V2EX、Hacker News、GitHub 热门新项目。Use when: user asks about trending topics, hot searches, what's popular, today's hot news, tech trends, or wants a daily briefing. Triggers on: 热榜、热搜、趋势、trending、hot、what's popular、daily briefing."
---

# CN Hot Trends — 中文+全球热榜聚合

## Quick Start

```bash
python3 scripts/fetch_trends.py --proxy http://127.0.0.1:7897 --format markdown
```

## Data Sources

| Source | ID | Content | Auth |
|--------|----|---------|------|
| 百度热榜 | `baidu` | 实时热搜，7M+ 热度值 | No |
| 今日头条 | `toutiao` | 头条热榜 | No |
| V2EX | `v2ex` | 技术社区热帖 + 回复数 | No |
| Hacker News | `hn` | 全球科技热帖 + 分数 | No |
| GitHub | `github` | 近 7 天热门新项目 | No |

## Usage

```bash
# All sources, markdown output
python3 scripts/fetch_trends.py --format markdown

# Specific sources, JSON output
python3 scripts/fetch_trends.py --sources baidu,v2ex --format json --limit 5

# With proxy (needed for V2EX, HN, GitHub)
python3 scripts/fetch_trends.py --proxy http://127.0.0.1:7897

# Plain text
python3 scripts/fetch_trends.py --format text --limit 10
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--sources` | `baidu,toutiao,v2ex,hn,github` | Comma-separated source IDs |
| `--limit` | `10` | Items per source |
| `--format` | `json` | Output: `json`, `text`, `markdown` |
| `--proxy` | none | HTTP proxy URL |

## Output Formats

- **json**: Structured data, good for further processing
- **text**: Human-readable plain text
- **markdown**: Formatted tables, good for chat/email output

## Tips

- Baidu and Toutiao work without proxy; V2EX/HN/GitHub need proxy in some regions
- Combine with AI analysis: fetch trends → summarize → identify patterns
- Use `--sources github` to discover trending open-source projects
- Pair with cron for daily automated briefings
