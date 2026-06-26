# social-search Capability

> 搜索和抓取社交媒体内容（X/Twitter, Reddit 等）

**Provides**: `social-search`  
**Skill**: `claude-code-x-scraper`  
**Version**: 1.0.0

---

## Methods

### getUserTweets

获取指定用户的推文

**Input:**
```json
{
  "username": "sama",
  "count": 5,
  "include_replies": false,
  "since": "2026-03-11"
}
```

**How to fulfill:**
```bash
cd /root/.openclaw/workspace
source /root/.openclaw/venv/bin/activate
python3 skills/claude-code-x-scraper/scripts/fetch_user_tweets.py \
  --username "${username}" \
  --count ${count} \
  --since "${since}"
```

**Output:**
```json
{
  "success": true,
  "user": {
    "username": "sama",
    "name": "Sam Altman",
    "followers": 3500000
  },
  "tweets": [
    {
      "id": "1234567890",
      "text": "Excited about the progress in AI reasoning...",
      "created_at": "2026-03-12T10:30:00Z",
      "likes": 15000,
      "retweets": 3000,
      "replies": 500
    }
  ],
  "total_tweets": 5
}
```

---

### searchTweets

搜索推文

**Input:**
```json
{
  "query": "AI agent framework",
  "count": 10,
  "freshness": "pw",
  "lang": "en"
}
```

**How to fulfill:**
```bash
cd /root/.openclaw/workspace
source /root/.openclaw/venv/bin/activate
python3 skills/claude-code-x-scraper/scripts/search_tweets.py \
  --query "${query}" \
  --count ${count} \
  --freshness "${freshness}"
```

**Output:**
```json
{
  "success": true,
  "tweets": [
    {
      "id": "1234567890",
      "text": "Just released our new AI agent framework...",
      "user": {
        "username": "ai_researcher",
        "name": "AI Researcher"
      },
      "created_at": "2026-03-12T09:00:00Z",
      "likes": 500,
      "url": "https://x.com/ai_researcher/status/1234567890"
    }
  ],
  "total_results": 10
}
```

---

### getTrendingTopics

获取热门话题

**Input:**
```json
{
  "location": "US",
  "count": 10
}
```

**Output:**
```json
{
  "success": true,
  "trending": [
    {
      "name": "#AI",
      "tweet_volume": 500000,
      "rank": 1
    },
    {
      "name": "#QuantumComputing",
      "tweet_volume": 200000,
      "rank": 2
    }
  ]
}
```

---

### getUserTimeline

获取用户完整时间线（带分页）

**Input:**
```json
{
  "username": "elonmusk",
  "max_tweets": 50,
  "cursor": null
}
```

**Output:**
```json
{
  "success": true,
  "tweets": [...],
  "next_cursor": "DAABCgABGNrRwPr__-cKAAIZz9G8hQADCAACAAAAAAgAAwAAAAACAAQAAAAAA",
  "has_more": true
}
```

---

## Error Handling

| Error | Code | Message |
|-------|------|---------|
| User not found | 404 | `User not found: ${username}` |
| Rate limited | 429 | `Rate limited, retry after ${retry_after}s` |
| Auth required | 401 | `Authentication required (cookies expired)` |
| Search failed | 500 | `Search failed: ${error_message}` |

---

## Examples

### Example 1: Get User Tweets
```yaml
- capability: social-search
  method: getUserTweets
  args:
    username: "sama"
    count: 5
  capture: tweets
```

### Example 2: Search Tweets
```yaml
- capability: social-search
  method: searchTweets
  args:
    query: "AI breakthrough"
    count: 10
    freshness: "pd"
  capture: search_results
```

### Example 3: Daily Rotation (8 accounts)
```yaml
- capability: social-search
  method: getUserTweets
  args:
    username: "${rotation(['sama', 'elonmusk', 'karpathy', 'fchollet', 'ylecun', 'DrJimFan', 'EMostaque', 'hardmaru'])}"
    count: 5
  capture: daily_tweets
```

---

## Configuration

**Credentials file**: `/root/.openclaw/credentials/x_login_credentials.env`

**Required environment variables:**
```bash
X_USERNAME=testng233@gmail.com
X_PASSWORD=***
COOKIES_FILE=/root/cookies.json
```

---

*Created: 2026-03-12 14:30 PM*  
*Author: RichTheRaccoon*
