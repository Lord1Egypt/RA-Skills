---
name: boring-social-analytics
description: "Track social media performance and analytics across platforms using Boring. Use when the user says 'show my analytics', 'check social media performance', 'how are my posts doing', 'engagement report', 'post metrics', 'view stats', or wants to see performance data for Facebook, Instagram, Threads, YouTube, or TikTok accounts."
version: 1.0.0
metadata:
  openclaw:
    emoji: "📊"
    homepage: https://boring-doc.aiagent-me.com/getting-started/mcp.html
    requires:
      config:
        - MCP Connector link from boring.aiagent-me.com (contains embedded auth token)
---

# Boring Social Analytics

Track performance and engagement across all your social media platforms. Powered by [Boring](https://boring-doc.aiagent-me.com).

## Security & Data Handling

- **MCP link is a credential**: Your MCP Server URL contains an embedded authentication token. Treat it like a password — do not share it publicly. Regenerate anytime in Settings.
- **Data flow**: Analytics queries are sent from Boring's server to social media platform APIs (Facebook, Instagram, Threads, YouTube, TikTok) on your behalf. Only performance metrics are retrieved — no content is uploaded.
- **No local credentials**: No local API keys or environment variables needed. All auth is embedded in the MCP link.

## Prerequisites

1. **Sign up** at [boring.aiagent-me.com](https://boring.aiagent-me.com) with Google
2. **Connect accounts** — supports Facebook, Instagram, Threads, YouTube, TikTok
3. **Get your MCP link**: Go to **Settings** → copy your MCP Server URL (contains your auth token — treat it like a password)
4. **Add to Claude**: Paste the MCP link as a Connector — no install, no API key needed

## Available Analytics Tools

| Tool | Data Source | Best For |
|------|-----------|----------|
| `boring_get_performance` | Real-time platform API | Account-level overview (reach, engagement, followers) |
| `boring_get_video_analytics` | Real-time platform API | Per-post/video metrics (views, likes, comments, shares) |
| `boring_get_posts_performance` | Daily snapshots (collected at 2 AM) | Historical post performance over date ranges |
| `boring_get_publish_history` | Boring database | Publishing history and status tracking |

## Workflow

### Step 1: List Accounts

Call `boring_list_accounts` to see all connected platforms. Show a summary to the user.

### Step 2: Determine What the User Wants

| User Request | Tool to Use |
|-------------|------------|
| "How is my account doing?" | `boring_get_performance` |
| "Show my best posts" | `boring_get_video_analytics` |
| "Performance over the last month" | `boring_get_posts_performance` |
| "What did I post recently?" | `boring_get_publish_history` |
| "Compare platforms" | `boring_get_performance` for each platform |

### Step 3: Fetch Data

#### Account-Level Performance
```
boring_get_performance(
  account_id="<account_id>",
  platform="instagram",
  period="week"       // "day", "week", or "month"
)
```

Returns metrics like reach, follower count, engagement rate, profile views.

#### Per-Post Analytics (Real-Time)
```
boring_get_video_analytics(
  account_id="<account_id>",
  platform="instagram",
  limit=20             // max 100
)
```

Returns per-post data: views, likes, comments, shares for up to 100 recent posts.

#### Historical Post Performance (Snapshots)
```
boring_get_posts_performance(
  account_id="<account_id>",
  since="2025-12-01",  // YYYY-MM-DD (default: 30 days ago)
  until="2025-12-31",  // YYYY-MM-DD (default: today)
  limit=20             // max 100
)
```

Returns post-level engagement, metrics, and content from daily collected snapshots.

#### Publishing History
```
boring_get_publish_history(
  limit=20,
  platform="facebook"  // optional filter
)
```

Returns recent publishing activity with status and post IDs.

### Step 4: Present Results

Format the data clearly for the user:

**For account overview**: Show key metrics in a summary table
**For post analytics**: Rank posts by engagement, highlight top performers
**For cross-platform comparison**: Side-by-side metrics across platforms
**For historical data**: Show trends over time

## Metrics by Platform

### Facebook
- `page_media_view`: Total video views
- `page_post_engagements`: Likes, comments, shares
- `page_total_actions`: Total page actions

### Instagram
- `reach`: Accounts reached
- `follower_count`: Total followers
- `profile_views`: Profile visits
- `total_interactions`: Likes + comments + saves + shares
- Reels: `ig_reels_avg_watch_time`, `ig_reels_video_view_total_time`

### Threads
- `views`: Post views
- `likes`, `replies`, `reposts`, `quotes`
- `followers_count`: Account followers

### YouTube
- `views`, `likes`, `comments`, `shares`
- `estimatedMinutesWatched`: Total watch time
- `averageViewDuration`: Average view duration
- `subscribersGained` / `subscribersLost`

### TikTok
- Video views, likes, comments, shares
- Account-level performance metrics

## Cross-Platform Comparison

When the user asks to compare platforms, fetch `boring_get_performance` for each connected account and present a unified table:

```
| Platform   | Reach   | Engagement | Followers |
|-----------|---------|------------|-----------|
| Facebook  | 12,500  | 1,200      | 5,000     |
| Instagram | 8,300   | 2,100      | 3,200     |
| Threads   | 3,100   | 450        | 1,800     |
| YouTube   | 15,000  | 3,500      | 2,100     |
```

## Error Handling

| Error | Solution |
|-------|----------|
| `InvalidApiKey` | MCP link may be invalid — regenerate it at boring.aiagent-me.com Settings |
| `InvalidAccountId` | Run `boring_list_accounts` to get valid IDs |
| `TokenExpired` | Reconnect account at boring.aiagent-me.com |
| No data returned | Account may be newly connected — data collection runs daily at 2 AM |

## Documentation

Full API docs: [boring-doc.aiagent-me.com](https://boring-doc.aiagent-me.com)
