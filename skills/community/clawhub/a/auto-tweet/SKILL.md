---
name: auto-tweet
description: Post, search, like, retweet, bookmark, and manage a Twitter/X account via a local twikit-based API server on port 19816. Use when the user asks to tweet, search tweets, check timeline, like/retweet posts, or manage their X account. Replaces openclaw-x with fully auditable open-source Python code.
metadata: {"openclaw": {"emoji": "🐦", "os": ["darwin", "linux"]}}
---

# Auto-Tweet Agent — OpenClaw Skill

> Safe, open-source Twitter/X automation via twikit.
> Replaces openclaw-x with fully auditable Python code.

## Overview

This skill lets you control a Twitter/X account through natural language.
The local API runs on `http://localhost:19816` and wraps the open-source
[twikit](https://github.com/d60/twikit) library (4.1K+ ⭐, MIT license).

**No closed-source binaries. No cookie theft risk. Fully transparent.**

## Prerequisites

The Auto-Tweet server must be running:
```bash
cd ~/.openclaw/skills/auto-tweet
python main.py
```

## Available Actions

### Post a tweet
```bash
curl -X POST http://localhost:19816/tweet \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello from OpenClaw!"}'
```

### Post a tweet with media
```bash
curl -X POST http://localhost:19816/tweet \
  -H "Content-Type: application/json" \
  -d '{"text": "Check this out!", "media_paths": ["/path/to/image.jpg"]}'
```

### Reply to a tweet
```bash
curl -X POST http://localhost:19816/tweet \
  -H "Content-Type: application/json" \
  -d '{"text": "Great point!", "reply_to": "TWEET_ID"}'
```

### Quote tweet
```bash
curl -X POST http://localhost:19816/tweet \
  -H "Content-Type: application/json" \
  -d '{"text": "This is amazing!", "quote_url": "https://x.com/user/status/TWEET_ID"}'
```

### Search tweets
```bash
curl "http://localhost:19816/search?q=AI+Agent&type=Latest&count=10"
```

### Search users
```bash
curl "http://localhost:19816/search/users?q=openai&count=5"
```

### Get timeline (For You)
```bash
curl "http://localhost:19816/timeline?count=20"
```

### Get timeline (Following)
```bash
curl "http://localhost:19816/timeline/following?count=20"
```

### Like a tweet
```bash
curl -X POST http://localhost:19816/like \
  -H "Content-Type: application/json" \
  -d '{"tweet_id": "TWEET_ID"}'
```

### Unlike a tweet
```bash
curl -X POST http://localhost:19816/unlike \
  -H "Content-Type: application/json" \
  -d '{"tweet_id": "TWEET_ID"}'
```

### Retweet
```bash
curl -X POST http://localhost:19816/retweet \
  -H "Content-Type: application/json" \
  -d '{"tweet_id": "TWEET_ID"}'
```

### Undo retweet
```bash
curl -X POST http://localhost:19816/unretweet \
  -H "Content-Type: application/json" \
  -d '{"tweet_id": "TWEET_ID"}'
```

### Bookmark a tweet
```bash
curl -X POST http://localhost:19816/bookmark \
  -H "Content-Type: application/json" \
  -d '{"tweet_id": "TWEET_ID"}'
```

### Get bookmarks
```bash
curl "http://localhost:19816/bookmarks?count=20"
```

### Get user profile
```bash
curl "http://localhost:19816/user/elonmusk"
```

### Get user tweets
```bash
curl "http://localhost:19816/user/elonmusk/tweets?type=Tweets&count=10"
```

### Get a specific tweet
```bash
curl "http://localhost:19816/tweet/TWEET_ID"
```

### Delete a tweet
```bash
curl -X DELETE "http://localhost:19816/tweet/TWEET_ID"
```

### Get trending topics
```bash
curl "http://localhost:19816/trends?category=trending"
```

### Send a DM
```bash
curl -X POST http://localhost:19816/dm \
  -H "Content-Type: application/json" \
  -d '{"user_id": "USER_ID", "text": "Hello!"}'
```

### Follow / Unfollow
```bash
curl -X POST "http://localhost:19816/follow/USER_ID"
curl -X POST "http://localhost:19816/unfollow/USER_ID"
```

### Get notifications
```bash
curl "http://localhost:19816/notifications?type=Mentions&count=20"
```

### Schedule a tweet
```bash
curl -X POST http://localhost:19816/schedule \
  -H "Content-Type: application/json" \
  -d '{"text": "Scheduled tweet!", "scheduled_at": 1735689600}'
```

### Check rate limits
```bash
curl "http://localhost:19816/rate_limits"
```

### Health check
```bash
curl "http://localhost:19816/"
```

## Rate Limits (Built-in Safety)

| Limit | Default | Purpose |
|-------|---------|---------|
| API calls/hour | 30 | Prevent hourly burst |
| API calls/day | 200 | Match normal usage |
| Tweets/day | 20 | Conservative posting |

All limits are configurable in `config.json`.

## Error Handling

All endpoints return standard HTTP status codes:
- `200` — Success
- `400` — Bad request (invalid parameters)
- `401` — Session expired (restart server)
- `403` — Account issue (suspended/locked)
- `409` — Duplicate tweet
- `429` — Rate limit exceeded
- `500` — Twitter API error

## Security Notes

- Server binds to `127.0.0.1` only (localhost) — no external access
- Credentials stay in local `config.json`
- Cookies saved locally in `cookies.json`
- All code is open-source Python — fully auditable
- No telemetry, no external callbacks
- Rate limiter protects against accidental overuse
