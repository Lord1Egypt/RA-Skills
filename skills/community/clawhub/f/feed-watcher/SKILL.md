---
name: feed-watcher
description: |
  Monitor RSS/Atom feeds and send notifications when new content appears.
  Track YouTube channels, Reddit subreddits, GitHub releases, blogs, and any RSS/Atom feed.
  Supports webhook notifications for Discord, Telegram, Slack, etc.
compatibility: Node.js 14+
metadata:
  author: Seth
  version: "0.0.1"
---

# Feed Watcher

Monitor RSS/Atom feeds and send notifications when new content appears.

## Description

This skill monitors RSS and Atom feeds for new content and sends notifications via webhook or cron job. It's designed to track YouTube channels, Reddit subreddits, GitHub repos, blogs, and any other RSS/Atom feed.

## Features

- Add multiple feeds to monitor
- Track new articles/posts since last check
- Configurable notification via webhook
- Persistent state (remembers last checked item)
- Supports any RSS/Atom feed

## Installation

```bash
# Install required dependencies
npm install

# Or use globally
npm install -g rss-parser dotenv
```

## Configuration

Create a `.env` file with:

```env
# Webhook URL for notifications (Discord, Telegram, Slack, etc.)
WEBHOOK_URL=https://your-webhook-url.com/hook

# Optional: Custom user agent
USER_AGENT=feed-watcher/1.0
```

## Commands

### Add a feed

```bash
node index.js add "feed_name" "https://example.com/feed.xml"
```

Example - YouTube channel:
```bash
node index.js add "Psychopoly" "https://www.youtube.com/feeds/videos.xml?channel_id=UCXXXX"
```

Example - Reddit subreddit:
```bash
node index.js add "programming" "https://www.reddit.com/r/programming/.rss"
```

Example - GitHub releases:
```bash
node index.js add "openclaw" "https://github.com/openclaw/openclaw/releases.atom"
```

### List feeds

```bash
node index.js list
```

### Scan for updates

```bash
node index.js scan
```

### Check specific feed

```bash
node index.js check "feed_name"
```

### Remove feed

```bash
node index.js remove "feed_name"
```

## Usage as a Cron Job

Add to crontab for automatic monitoring:

```bash
# Run every 30 minutes
*/30 * * * * cd /path/to/feed-watcher && node index.js scan >> /var/log/feed-watcher.log 2>&1
```

## Supported Feed Types

- RSS 2.0
- Atom 1.0
- YouTube channel feeds
- Reddit subreddit feeds (.rss)
- GitHub release/issue feeds
- Any standard RSS/Atom feed

## Examples

### YouTube Channel

Find channel ID, then use:
```
https://www.youtube.com/feeds/videos.xml?channel_id=UCxxxxx
```

### Reddit

For r/programming:
```
https://www.reddit.com/r/programming/.rss
```

### GitHub Releases

For a repo:
```
https://github.com/owner/repo/releases.atom
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| WEBHOOK_URL | No | URL to send notifications |
| DATA_DIR | No | Directory for state files (default: ~/.feed-watcher) |

## Notification Format

When new content is found, the webhook receives:

```json
{
  "feed": "Feed Name",
  "count": 3,
  "items": [
    {
      "title": "Article Title",
      "link": "https://example.com/article",
      "pubDate": "2024-01-15T10:30:00Z"
    }
  ]
}
```

## Notes

- State is stored in `~/.feed-watcher/feeds.json`
- Each feed tracks its own last-seen item
- Run `scan` before setting up cron to test feeds
- You can use with any notification service (Discord webhook, Telegram bot, Slack, etc.)
