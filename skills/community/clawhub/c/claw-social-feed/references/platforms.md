# Supported Platforms

> Full list: [bb-sites](https://github.com/epiral/bb-sites) — this document covers the most commonly used adapters.

**Note**: bb-browser does not provide a "followees/following" list. Users must manually specify which accounts to track in `config.yaml`.

## Twitter/X

| Command | Description | Key Fields |
|---------|-------------|------------|
| `twitter/tweets <handle>` | User timeline (default 20, max 100) | `text`, `likes`, `retweets`, `created_at`, `type` (tweet/retweet) |
| `twitter/user <handle>` | User profile | `followers`, `following`, `bio` |
| `twitter/thread <url>` | Full thread with replies | |
| `twitter/bookmarks` | Your bookmarks | |
| `twitter/notifications` | Your notifications | |

**Incremental note**: `twitter/tweets` has no time-range parameter — relies on `state.json` timestamp for incremental filtering.

## Reddit

| Command | Description |
|---------|-------------|
| `reddit/posts <user>` | User's posts |
| `reddit/hot` | Hot posts |
| `reddit/thread <url>` | Thread with comments |

## GitHub

| Command | Description |
|---------|-------------|
| `github/repo <owner/repo>` | Repository info |
| `github/issues <owner/repo>` | Issue list |

## HackerNews

| Command | Description |
|---------|-------------|
| `hackernews/top [count]` | Top stories |
| `hackernews/thread <id>` | Story + comments |

## Weibo

| Command | Description |
|---------|-------------|
| `weibo/user_posts <uid>` | User posts |
| `weibo/feed` | Home timeline |

## Bilibili

| Command | Description |
|---------|-------------|
| `bilibili/user_posts <uid>` | User submissions |
| `bilibili/feed` | Following feed |

## Xiaohongshu (小红书)

| Command | Description |
|---------|-------------|
| `xiaohongshu/user_posts <uid>` | User notes |
| `xiaohongshu/note <id>` | Note detail |

## Other Platforms

| Platform | Commands |
|----------|----------|
| V2EX | `v2ex/hot`, `v2ex/latest` |
| 知乎 | `zhihu/hot`, `zhihu/question <id>` |
| 雪球 | `xueqiu/hot`, `xueqiu/stock <code>`, `xueqiu/feed` |
| YouTube | `youtube/video <id>`, `youtube/transcript <id>` (must be on video page) |

## Adapter Status

| Platform | Status | Notes |
|----------|--------|-------|
| Twitter | ✅ Full | tweets/user/thread all work |
| Reddit | ✅ Working | posts/hot/thread |
| GitHub | ✅ Working | repo/issues |
| HackerNews | ✅ Working | top/thread |
| V2EX | ✅ Working | hot/latest |
| Weibo | ✅ Working | user_posts/feed |
| Bilibili | ✅ Working | user_posts/feed |
| 小红书 | ✅ Working | user_posts/note |
| 知乎 | ⚠️ Partial | hot works; search may be unstable |
| 雪球 | ✅ Working | hot/stock/feed |
| YouTube | ⚠️ Limited | needs video id; transcript requires being on video page |

## Adding a New Platform

1. Check supported platforms: `bb-browser site list`
2. Get adapter info: `bb-browser site info <platform>`
3. Update `get_adapter_cmd()` in `fetch_save.py` to add the platform mapping
