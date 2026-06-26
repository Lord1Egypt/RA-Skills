---
name: diffbot-fetch
description: Fetch and extract clean article content from any URL using the Diffbot Article API. Returns clean Markdown.
requires:
  - ENV: DIFFBOT_API_KEY
---

# Diffbot Fetch

Use this skill to fetch and extract clean article content from any URL using the Diffbot Article API. Use this when you need to read the main text of an article, blog post, or news story without the clutter of ads, navigation, or sidebars.

## Setup

You need a Diffbot API token to use this skill. Set it as an environment variable:

```bash
export DIFFBOT_API_KEY="your_token_here"
```

## Usage

```bash
uv run fetch.py "https://example.com/article"
```
