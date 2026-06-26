# Douyin Scraper

Search Douyin (抖音) videos by natural language — no API key needed.

## Features

- 🔍 **Natural language search**: "搜索一下海鲜视频" just works
- 🔥 **Trending discovery**: Find what's hot on Douyin
- 📋 **Video detail**: Extract metadata from Douyin video URLs

## Install

```bash
clawhub install douyin-scraper
```

## Usage Examples

| You say | What happens |
|---------|-------------|
| 搜索一下海鲜视频 | Searches Douyin for seafood videos |
| 帮我找抖音上做菜的视频 | Searches Douyin for cooking videos |
| 抖音热搜 | Shows today's trending topics |
| 这个抖音视频讲了什么 https://douyin.com/video/xxx | Extracts video details |

## How It Works

Uses web search (Brave) to discover Douyin content, then fetches page metadata where possible. No cookies, API keys, or login required.

## Limitations

- Results depend on search engine coverage (may not be fully real-time)
- Douyin's CAPTCHA may block detailed page fetching in some cases
- Cannot download videos — use a dedicated downloader skill for that