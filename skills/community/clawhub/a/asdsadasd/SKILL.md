---
name: ai-content-pipeline
description: An end-to-end AI Content Pipeline that crawls articles, rewrites them using Google Gemini, and automatically publishes to Facebook Fanpage.
version: 2.0.0
env:
  - GEMINI_API_KEY
  - APIFY_API_TOKEN
  - FB_APP_ID
  - FB_APP_SECRET
  - FB_PAGE_ID
  - FB_PAGE_ACCESS_TOKEN
---

# 🤖 OpenClaw AI Content Pipeline (Analyze + Publish)

## Purpose
This is a production-ready OpenClaw Skill that merges a Web Crawler, an AI Rewriter (Google Gemini), and a Facebook Auto-Publisher into one seamless pipeline. It reads URLs (news articles or Facebook posts), rewrites them into engaging social media captions, and posts them directly to your Fanpage.

## Core Capabilities
- **Analyze Mode**: Extracts data from URLs via Python `requests`/`BeautifulSoup` (for static news) or `Apify` (for JS-heavy content like Facebook). Generates localized rewritten text via Gemini 2.5 Flash.
- **Publish Mode**: Pushes the generated content directly to a Facebook Page via Graph API v21.0.
- **Batch Processing**: Can ingest URLs line-by-line from a text file, process them in bulk, and save JSON reports.

## Architecture Map
- `run.bat` / `main.py`  ← Central Orchestrators (CLI Entry points)
- `agents/crawler_agent.py` ← Hybrid Crawler (Native + Apify API)
- `agents/writer_agent.py` ← AI Content Generator (Gemini Integration)
- `agents/fb_publisher_agent.py` ← Graph API Poster (Messages & Images)
- `config.py` ← Environment Loader & System Validation

## Setup & Environment
Ensure you create a `.env` file at the root with the following variables:
```env
# AI Models
GEMINI_API_KEY=...
OPENAI_API_KEY=...    # Optional: For DALL-E 3 image generation

# Scraping
APIFY_API_TOKEN=...

# Facebook Graph API
FB_APP_ID=...
FB_APP_SECRET=...
FB_PAGE_ID=...
FB_PAGE_ACCESS_TOKEN=...
```

## Usage commands
From your terminal, run the following commands (Windows `run.bat` wrappers):

### 1. Analyze (Test scrape and text rewrite)
```cmd
# Analyze a single URL
run.bat analyze "https://vnexpress.net/..."

# Analyze and save as JSON
run.bat analyze "https://dantri.com.vn/..." --save

# Batch analyze from a text file
run.bat analyze-file urls.txt
```

### 2. Publish (Post directly to Facebook)
```cmd
# Test Graph API Token connection
run.bat test
run.bat test-post

# Full pipeline (Crawl -> Rewrite -> Post to Fanpage)
run.bat run "https://dantri.com.vn/..."

# Pipeline dry-run (No actual post)
run.bat dry "https://dantri.com.vn/..."
```
