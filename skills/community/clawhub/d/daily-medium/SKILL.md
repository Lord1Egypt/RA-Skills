---
name: daily-medium
description: Fetch and summarize Medium Daily Digest emails from Gmail. Extracts article URLs, generates Freedium links to bypass paywalls, and provides article summaries. Use when the user wants to check their Medium Daily Digest, read Medium articles without paywall, or get summaries of Medium content from their email.
---

# Daily Medium Skill

Fetch Medium Daily Digest emails from Gmail and extract article information with paywall-free links.

## Overview

This skill connects to Gmail via IMAP, retrieves the latest Medium Daily Digest email, extracts article URLs, and provides Freedium mirror links to bypass Medium's paywall.

## Prerequisites

**Environment Variables Required:**
- `EMAIL_ADDRESS` - Gmail address (e.g., user@gmail.com)
- `EMAIL_PASSWORD` - Gmail App Password (not regular password)

**How to get Gmail App Password:**
1. Go to Google Account → Security → 2-Step Verification
2. At the bottom, click "App passwords"
3. Select "Mail" and your device
4. Copy the 16-character password

## Usage

### Basic Usage

```python
from scripts.fetch_medium import fetch_medium_digest

# Fetch today's Medium digest
result = fetch_medium_digest()

if result:
    print(f"Digest: {result['digest_title']}")
    for article in result['articles']:
        print(f"- {article['title']}")
        print(f"  Freedium: {article['freedium_url']}")
```

### With Custom Credentials

```python
result = fetch_medium_digest(
    email_address="user@gmail.com",
    password="xxxx xxxx xxxx xxxx"
)
```

## Output Format

The `fetch_medium_digest()` function returns:

```python
{
    'digest_date': 'Mon, 16 Feb 2026 12:30:00 +0000',
    'digest_title': '10 OpenClaw Use Cases for a Personal AI Assistant | Balazs Kocsis',
    'articles': [
        {
            'title': 'Article Title Here',
            'author': 'username',
            'url': 'https://medium.com/@username/article-slug',
            'freedium_url': 'https://freedium-mirror.cfd/https://medium.com/@username/article-slug'
        },
        # ... more articles
    ]
}
```

## Article Summaries

To generate article summaries, fetch the content via Freedium and summarize:

```python
import requests
from bs4 import BeautifulSoup

def summarize_article(freedium_url):
    response = requests.get(freedium_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    # Return first 300 chars as summary
    return text[:300] + "..."
```

## Notes

- Maximum 15 articles returned by default (configurable via `max_articles` parameter)
- Requires IMAP access enabled in Gmail settings
- Uses Freedium (freedium-mirror.cfd) to bypass Medium's paywall
- Only fetches the most recent Medium Daily Digest email
