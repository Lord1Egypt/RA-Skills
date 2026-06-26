---
name: feishu-news
description: A skill to fetch and reference news information from Feishu when interacting with users.
---

# Feishu News Skill

This skill enables fetching and referencing news information from Feishu when interacting with users. It provides a way to incorporate current news sources into conversations.

## Usage Examples

- "Fetch latest news from Feishu"
- "Show me recent news articles"
- "Reference news sources in our conversation"
- "Get news updates from Feishu"

## Available Functions

- `fetch_news()`: Retrieves latest news from Feishu
- `reference_source(article_id)`: References a specific news source
- `format_news(news_data)`: Formats news data for user presentation
- `get_news_sources()`: Returns available news sources

## How It Works

This skill integrates with Feishu's news system to provide current information. When users request news or references, the skill:
1. Fetches relevant news articles from Feishu
2. Formats the information with proper source attribution
3. Presents the information to the user with clear references

## Integration Details

The skill uses Feishu's API to access news content and ensures proper attribution of news sources when referenced in conversations.