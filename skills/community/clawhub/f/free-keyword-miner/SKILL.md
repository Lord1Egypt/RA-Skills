---
name: Free Keyword Miner
slug: free-keyword-miner
version: 1.0.0
description: Free keyword research using Google PAA, Autocomplete, Reddit discussions, and Bing. No paid API needed.
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---

## When to Use

需要免费获取关键词数据，替代Ahrefs/SEMrush等付费工具：
- Google "People Also Ask" 问题抓取
- Google Autocomplete 下拉框关键词
- Reddit用户讨论/痛点提取
- Bing搜索相关关键词
- 自动生成话题标题

适用于SEO关键词研究、内容策略规划、竞品分析。

## Quick Reference

```bash
python3 {baseDir}/keyword_miner.py --seed "your keyword" --sources all --output results.json
```

## Parameters

- `--seed`: 种子关键词（必填）
- `--sources`: 数据源（all/google-paa/autocomplete/reddit/bing）
- `--output`: 输出文件路径
- `--max-results`: 每个源最大结果数（默认20）
- `--language`: 语言代码（默认en）

## Output Format

```json
{
  "seed_keyword": "adult products for couples",
  "google_paa": ["question1", "question2"],
  "autocomplete": ["suggestion1", "suggestion2"],
  "reddit_topics": [{"title": "...", "score": 100, "pain_points": "..."}],
  "bing_related": ["related1", "related2"],
  "clusters": [{"name": "cluster1", "keywords": [...]}],
  "topic_ideas": ["How to...", "Best ..."]
}
```

## Installation

```bash
pip install people-also-ask beautifulsoup4 requests
```

## Data Sources Explained

### Google PAA (People Also Ask)
Uses `people-also-ask` Python library to scrape "People also ask" questions from Google. Works without API key. May need proxy rotation for heavy use.

### Google Autocomplete
Queries Google's suggestion API endpoint. Returns related searches. Free but rate-limited.

### Reddit
Uses Reddit's public JSON API. Searches relevant subreddits for user discussions, pain points, and questions. Great for understanding real user needs.

### Bing Search
Bing has less aggressive bot detection than Google. Good for related searches and content ideas.

## Tips for Better Results

1. Use multiple seed keywords for broader coverage
2. Combine sources for comprehensive data
3. Filter results by relevance to your niche
4. Use clusters to identify content gaps
5. Reddit data is gold for understanding pain points

## Known Limitations

- Google may block requests from data center IPs
- Reddit API may require authentication for heavy use
- Results quality depends on seed keyword specificity
- Rate limiting may slow down large research jobs
