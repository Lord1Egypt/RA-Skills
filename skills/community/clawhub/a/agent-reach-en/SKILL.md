---
name: agent-reach
description: >
  Give your AI agent eyes to see the entire internet. Install and configure
  upstream tools for Twitter/X, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu,
  Douyin, LinkedIn, Boss Zhipin, WeChat Official Accounts, RSS, and any web page — then call them directly.
  Use when: (1) setting up platform access tools for the first time,
  (2) checking which platforms are available,
  (3) user asks to configure/enable a platform channel.
  Triggers: "configure", "add channel", "install", "agent reach", "install channels",
  "configure twitter", "enable reddit".
version: 1.1.0
---

# Agent Reach

Install and configure upstream tools for 13+ platforms. After setup, call them directly — no wrapper layer.

## Workspace Rules

**Never create files, clone repos, or write output in the agent workspace.** Use these directories instead:

| Purpose | Directory |
|---------|-----------|
| Temporary output (subtitles, downloads) | `/tmp/` |
| Upstream tool repos | `~/.agent-reach/tools/` |
| Config & tokens | `~/.agent-reach/` |

Violating this will pollute the user's workspace and degrade their agent experience over time.

## Setup

```bash
pip install https://github.com/Panniantong/agent-reach/archive/main.zip
agent-reach install --env=auto
agent-reach doctor
```

`install` auto-detects your environment and installs core dependencies (Node.js, mcporter, xreach CLI, gh CLI, yt-dlp, feedparser). Run `doctor` to see what's active.

## Management

```bash
agent-reach doctor        # channel status overview
agent-reach watch         # quick health + update check
agent-reach check-update  # check for new versions
```

## Configure channels

```bash
agent-reach configure twitter-cookies "auth_token=xxx; ct0=yyy"
agent-reach configure proxy http://user:pass@ip:port
agent-reach configure --from-browser chrome    # auto-extract cookies from local browser
```

## Configuring a channel

When a user asks to configure/enable any channel:

1. Run `agent-reach doctor`
2. Find the channel — it shows status (✅/⚠️/⬜) and **what to do next**
3. Execute what you can automatically (install packages, start services)
4. For human-required steps (paste cookies), tell the user what to do
5. Run `agent-reach doctor` again to verify

**Do NOT memorize per-channel steps.** Always rely on `doctor` output.

### Cookie Import (Universal for all login-required platforms)

> **Important:** Platforms using cookie login have account ban risks. Remind users to use a **dedicated secondary account**.

For all platforms requiring cookies (Twitter, XiaoHongShu, etc.), **prefer Cookie-Editor import**:

1. User logs into the platform in their browser
2. Install [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) Chrome extension
3. Click extension → Export → Header String
4. Send the exported string to the Agent

Local computer users can also use `agent-reach configure --from-browser chrome` for automatic extraction.

QR code login is a backup option (only for local environments with browser), Cookie-Editor is simpler and more reliable.

### Other human actions

- **Proxy:** Reddit/Bilibili/XiaoHongShu may block server IPs — suggest a residential proxy if on a server

---

## Using Upstream Tools Directly

After `agent-reach install`, call the upstream tools directly.

> **Note:** `agent-reach` is an installer and config tool — it does NOT have `read`, `search`, or content-fetching commands. Use the upstream tools below instead.

### Twitter/X (xreach CLI)

```bash
# Search tweets
xreach search "query" --json -n 10

# Read a specific tweet
xreach tweet https://x.com/user/status/123 --json

# Read a user's timeline
xreach tweets @username --json -n 20
```

### YouTube (yt-dlp)

> yt-dlp requires JS runtime for YouTube downloads. `agent-reach install` auto-configures Node.js as runtime.
> If you see "Sign in to confirm you're not a bot", the IP is blocked by YouTube anti-crawler. Switch proxy or add cookies.

```bash
# Get video metadata
yt-dlp --dump-json "https://www.youtube.com/watch?v=xxx"

# Download subtitles only
yt-dlp --write-sub --write-auto-sub --sub-lang "zh-Hans,zh,en" --skip-download -o "/tmp/%(id)s" "URL"
# Then read the .vtt file

# Search (yt-dlp ytsearch)
yt-dlp --dump-json "ytsearch5:query"

# If "no JS runtime" warning: ensure Node.js is installed, then run:
#   mkdir -p ~/.config/yt-dlp && echo "--js-runtimes node" >> ~/.config/yt-dlp/config
```

### Bilibili (yt-dlp)

> Server IPs may be blocked by Bilibili (412 error). Recommend using proxy or add `--cookies-from-browser chrome`.

```bash
# Get video metadata
yt-dlp --dump-json "https://www.bilibili.com/video/BVxxx"

# Download subtitles
yt-dlp --write-sub --write-auto-sub --sub-lang "zh-Hans,zh,en" --convert-subs vtt --skip-download -o "/tmp/%(id)s" "URL"

# If blocked (412 / login required):
yt-dlp --cookies-from-browser chrome --dump-json "URL"
```

### Reddit (JSON API)

```bash
# Read a subreddit
curl -s "https://www.reddit.com/r/python/hot.json?limit=10" -H "User-Agent: agent-reach/1.0"

# Read a post with comments
curl -s "https://www.reddit.com/r/python/comments/POST_ID.json" -H "User-Agent: agent-reach/1.0"

# Search
curl -s "https://www.reddit.com/search.json?q=query&limit=10" -H "User-Agent: agent-reach/1.0"
```

Note: On servers, Reddit may block your IP. Use proxy or search via Exa instead.

### XiaoHongShu (mcporter + xiaohongshu-mcp)

> Requires login. Import cookies via Cookie-Editor or QR code login.

```bash
# Search posts
mcporter call 'xiaohongshu.search_feeds(keyword: "query")'

# Get post details (with comments)
mcporter call 'xiaohongshu.get_feed_detail(feed_id: "xxx", xsec_token: "yyy")'

# Get all comments
mcporter call 'xiaohongshu.get_feed_detail(feed_id: "xxx", xsec_token: "yyy", load_all_comments: true)'

# Publish image post
mcporter call 'xiaohongshu.publish_content(title: "Title", content: "Content", images: ["/path/to/img.jpg"], tags: ["food"])'

# Publish video post
mcporter call 'xiaohongshu.publish_with_video(title: "Title", content: "Content", video: "/path/to/video.mp4", tags: ["vlog"])'
```

Other features (like, collect, comment, user profile, etc.): `npx mcporter list xiaohongshu`

### Douyin (mcporter + douyin-mcp-server)

```bash
# Parse Douyin video info (share link -> title, author, watermark-free video URL, etc.)
mcporter call 'douyin.parse_douyin_video_info(share_link: "https://v.douyin.com/xxx/")'

# Get watermark-free video download link
mcporter call 'douyin.get_douyin_download_link(share_link: "https://v.douyin.com/xxx/")'

# AI extract video voice transcript (requires SiliconFlow API Key)
mcporter call 'douyin.extract_douyin_text(share_link: "https://v.douyin.com/xxx/")'
```

> No login required to parse videos. Supports both Douyin share links and direct links.

### GitHub (gh CLI)

```bash
# Search repos
gh search repos "query" --sort stars --limit 10

# View a repo
gh repo view owner/repo

# Search code
gh search code "query" --language python

# List issues
gh issue list -R owner/repo --state open

# View a specific issue/PR
gh issue view 123 -R owner/repo
```

### Web — Any URL (Jina Reader)

```bash
# Read any webpage as markdown
curl -s "https://r.jina.ai/URL" -H "Accept: text/markdown"

# Search the web
curl -s "https://s.jina.ai/query" -H "Accept: text/markdown"
```

### Exa Search (mcporter + exa MCP)

```bash
# Web search
mcporter call 'exa.web_search_exa(query: "query", numResults: 5)'

# Code search (GitHub, StackOverflow, docs)
mcporter call 'exa.get_code_context_exa(query: "how to parse JSON in Python", tokensNum: 3000)'

# Company research
mcporter call 'exa.company_research_exa(companyName: "OpenAI")'
```

### LinkedIn (mcporter + linkedin-scraper-mcp)

```bash
# View a profile
mcporter call 'linkedin.get_person_profile(linkedin_url: "https://linkedin.com/in/username")'

# Search people
mcporter call 'linkedin.search_people(keyword: "AI engineer", limit: 10)'

# View company
mcporter call 'linkedin.get_company_profile(linkedin_url: "https://linkedin.com/company/xxx")'
```

Fallback: `curl -s "https://r.jina.ai/https://linkedin.com/in/username"`

### Boss Zhipin (mcporter + mcp-bosszp)

```bash
# Browse recommended jobs
mcporter call 'bosszhipin.get_recommend_jobs_tool(page: 1)'

# Search jobs
mcporter call 'bosszhipin.search_jobs_tool(keyword: "Python", city: "Beijing", page: 1)'

# View job details
mcporter call 'bosszhipin.get_job_detail_tool(job_url: "https://www.zhipin.com/job_detail/xxx")'
```

Fallback: `curl -s "https://r.jina.ai/https://www.zhipin.com/job_detail/xxx"`

### WeChat Official Accounts (wechat-article-for-ai + miku_ai)

**Search** (miku_ai — Sogou WeChat search):

```python
# Search WeChat articles by keyword
python3 -c "
import asyncio
from miku_ai import get_wexin_article

async def search():
    articles = await get_wexin_article('AI Agent', 5)
    for a in articles:
        print(f'{a[\"title\"]} | {a[\"source\"]} | {a[\"date\"]}')
        print(f'  {a[\"url\"]}')

asyncio.run(search())
"
```

**Read** (Camoufox — stealth Firefox, bypasses WeChat anti-bot):

```bash
# Read a WeChat article (returns Markdown with images)
cd ~/.agent-reach/tools/wechat-article-for-ai && python3 main.py "https://mp.weixin.qq.com/s/ARTICLE_ID"

# Run as MCP server (for AI agent integration)
python3 mcp_server.py
```

Typical agent workflow: search → get URLs → immediately read full content.

Note: WeChat articles require a real browser to render. Jina Reader and curl cannot read them.

### RSS (feedparser)

```python
python3 -c "
import feedparser
d = feedparser.parse('https://example.com/feed')
for e in d.entries[:5]:
    print(f'{e.title} — {e.link}')
"
```

## Troubleshooting

### Twitter "fetch failed"

xreach CLI uses Node.js `undici`, which doesn't respect `HTTP_PROXY`. Solutions:
1. Ensure `undici` is installed: `npm install -g undici`
2. Configure proxy: `agent-reach configure proxy http://user:pass@ip:port`
3. If still failing, use transparent proxy (Clash TUN, Proxifier)

### Channel broken?

Run `agent-reach doctor` — it shows what's wrong and how to fix it.

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v1.1.0 | 2025-03-15 | Translated to English |
| v1.0.0 | 2025-03-05 | Initial release |
