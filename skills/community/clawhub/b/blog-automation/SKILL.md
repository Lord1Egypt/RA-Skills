---
name: blog-automation
description: Automated WordPress blog publishing with scheduling
version: 1.0.0
author: Migration from Agent Zero
---

# Blog Automation Skill

## Overview
Scheduled blog publishing system that publishes generated articles to WordPress.

## Purpose
- Convert articles to WordPress HTML format
- Schedule posts for optimal timing
- Handle image embeds and SEO tags
- Publish via WordPress REST API

## Input Variables
| Variable | Description | Example |
|----------|-------------|---------|
| WP_URL | WordPress site URL | https://paylesstax.co.za |
| WP_USERNAME | WordPress API username | blog_manager |
| WP_APP_TOKEN | Application password | (configured in OpenClaw) |
| ARTICLE_JSON | Path to generated article | ./article.json |
| SCHEDULE_TIME | Optional publish time | 2025-03-15T09:00:00 |
| CATEGORIES | Post categories | [Tax, Compliance] |
| TAGS | Post tags | [SARS, 2026] |

## Workflow
1. Load article JSON from generator
2. Convert markdown to HTML
3. Upload images (if any) to WordPress media
4. Create WordPress post via REST API
5. Log result to memory file

## Triggers
- Cron schedule (e.g., daily at 8am)
- Manual CLI execution
- Post-generation webhook from article generator

## APIs & Dependencies
- WordPress REST API v2
- requests library for HTTP
- markdown2 or mistletoe for MD->HTML

## Output
```
{
  "status": "published|scheduled|failed",
  "wordpress_id": 12345,
  "url": "https://site.com/blog/post",
  "timestamp": "2025-03-02T05:03:19"
}
```

## Files
- index.py - Publishing logic
- formatter.py - MD to HTML conversion
- scheduler.py - Cron/schedule management
