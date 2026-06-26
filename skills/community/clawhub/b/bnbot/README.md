---
name: bnbot
description: The safest and most efficient way to automate Twitter/X — BNBot operates through a real browser session with 40+ AI-powered CLI tools. Grow your Twitter without API bans.
version: 1.5.0
homepage: https://github.com/bnbot-ai/bnbot-cli
metadata:
  openclaw:
    emoji: "\U0001F916"
    os: [darwin, linux, windows]
    requires:
      bins: [bnbot-cli]
    install:
      - id: node
        kind: node
        package: bnbot-cli
        bins: [bnbot-cli]
        label: Install bnbot-cli (npm)
---

# BNBot - Control Twitter/X via AI

BNBot operates through a real browser session via Chrome Extension. 40+ CLI tools for posting, engagement, scraping, user profiles, content fetching, articles, and job searching.

- **Chrome Extension**: [Install](https://chromewebstore.google.com/detail/bnbot-your-ai-growth-agen/haammgigdkckogcgnbkigfleejpaiiln)
- **npm**: [bnbot-cli](https://www.npmjs.com/package/bnbot-cli)

## First-time setup (run once after install)

After `bnbot-cli` is installed, start the WebSocket daemon:

```bash
nohup bnbot serve > /tmp/bnbot.log 2>&1 &
sleep 1
lsof -i :18900 -P 2>/dev/null | grep LISTEN
```

Confirm port 18900 is LISTEN before proceeding.

## Before using any bnbot tool

Check if the daemon is still running:

```bash
lsof -i :18900 -P 2>/dev/null | grep LISTEN
```

If empty, restart it:

```bash
nohup bnbot serve > /tmp/bnbot.log 2>&1 &
```

## How to use tools

All tools are executed via the `bnbot` CLI:

```bash
bnbot get-extension-status
bnbot post-tweet --text "Hello world!"
bnbot scrape-timeline --limit 10
```

Output is JSON.

**Auto-thread for multiple images**: When `post-tweet` receives more than 4 images (Twitter's limit), it automatically splits into a thread — first tweet gets the text + first 4 images, subsequent tweets get remaining images in batches of 4. You don't need to manually use `post-thread` for this.

**Media support**: Parameters like `--media`, `--image`, `--headerImage`, `--bodyImages` accept both local file paths (`~/Downloads/image.png`) and URLs (`https://example.com/image.jpg`). Files are auto-converted to base64 before sending.

## If extension is not connected

If `bnbot get-extension-status` shows `connected: false`, tell the user:

> Chrome Extension is not connected. Please:
> 1. Install extension: https://chromewebstore.google.com/detail/bnbot-your-ai-growth-agen/haammgigdkckogcgnbkigfleejpaiiln
> 2. Open https://x.com in Chrome
> 3. Open BNBot sidebar → Settings → turn on **OpenClaw**

## Available CLI commands

### Status
- `bnbot get-extension-status` — Check if extension is connected
- `bnbot get-current-page-info` — Get current Twitter/X page info

### Navigation
- `bnbot navigate-to-tweet --tweetUrl <url>`
- `bnbot navigate-to-search [--query "..."] [--sort top|latest|people|media]`
- `bnbot navigate-to-bookmarks`
- `bnbot navigate-to-notifications`
- `bnbot navigate-to-following`
- `bnbot return-to-timeline`

### Posting
- `bnbot post-tweet --text "..." [--media file1.png file2.jpg] [--draftOnly]`
- `bnbot post-thread --tweets '[{"text":"..."},{"text":"..."}]'`
- `bnbot submit-reply --text "..." [--tweetUrl <url>] [--image <path>]`
- `bnbot quote-tweet --tweetUrl <url> --text "..." [--media ...] [--draftOnly]`

### Engagement
- `bnbot like-tweet [--tweetUrl <url>]`
- `bnbot unlike-tweet [--tweetUrl <url>]`
- `bnbot retweet [--tweetUrl <url>]`
- `bnbot unretweet [--tweetUrl <url>]`
- `bnbot follow-user [--username <handle>]`
- `bnbot unfollow-user [--username <handle>]`
- `bnbot bookmark-tweet [--tweetUrl <url>]`
- `bnbot unbookmark-tweet [--tweetUrl <url>]`
- `bnbot delete-tweet [--tweetUrl <url>]`

### Scraping
- `bnbot scrape-timeline [--limit <n>] [--scrollAttempts <n>]`
- `bnbot scrape-bookmarks [--limit <n>]`
- `bnbot scrape-search-results --query "..." [--tab top|latest|people|media|lists] [--limit <n>] [--from <username>] [--since YYYY-MM-DD] [--until YYYY-MM-DD] [--lang en] [--has images|videos|links|media] [--minLikes <n>] [--minRetweets <n>] [--minReplies <n>] [--excludeReplies] [--excludeRetweets]`
- `bnbot scrape-current-view`
- `bnbot scrape-thread [--tweetUrl <url>] [--maxScrolls <n>]`
- `bnbot account-analytics [--startDate YYYY-MM-DD] [--endDate YYYY-MM-DD] [--granularity Daily|Weekly|Monthly]`

### User Profiles
- `bnbot scrape-user-profile --username <handle>`
- `bnbot scrape-user-tweets --username <handle> [--limit <n>] [--scrollAttempts <n>]`

### Content Fetching
- `bnbot fetch-wechat-article --url <url>`
- `bnbot fetch-tiktok-video --url <url> [--savePath <path>]`
- `bnbot fetch-xiaohongshu-note --url <url>`

### Articles
- `bnbot open-article-editor`
- `bnbot fill-article-title --title "..."`
- `bnbot fill-article-body --content "..." [--format plain|markdown|html] [--bodyImages img1 img2]`
- `bnbot upload-article-header-image --headerImage <path>`
- `bnbot publish-article [--publish] [--asDraft]`
- `bnbot create-article --title "..." --content "..." [--format plain|markdown|html] [--headerImage <path>] [--bodyImages img1 img2] [--publish]`

### Authentication
- `bnbot login [--email <email>]` — Login to BNBot via email verification

### Jobs
- `bnbot search-jobs [--type boost|hire|all] [--status active|completed|expired] [--sort created_at|reward|deadline] [--limit <n>] [--keyword "..."] [--endingSoon] [--token ETH|USDC|USDT]`
