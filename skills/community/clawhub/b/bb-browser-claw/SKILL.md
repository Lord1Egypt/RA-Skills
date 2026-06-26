# bb-browser Skill

> Chrome CDP automation with 103 commands across 36 platforms. Runs via the bb-browser daemon on the host machine, accessible from inside the Rabbit container.

## How It Works

bb-browser connects to a real Chromium instance on the host via Chrome DevTools Protocol (CDP). The daemon runs at `localhost:19824`. Commands execute within the actual browser — with real cookies and sessions — so you can access logged-in content without any API keys.

The binary is available inside the container at `/usr/local/bin/bb-browser` (bind-mounted from host).

## Basic Syntax

```bash
# Run a site adapter
bb-browser site <adapter>/<command> [args]

# List all available adapters
bb-browser site list

# Get adapter usage details
bb-browser site info boss/search

# Output as JSON
bb-browser site <adapter>/<command> [args] --json
```

## Key Adapters Available

### Job Search (BOSS直聘)
```bash
bb-browser site boss/search '工程师 上海' --json
bb-browser site boss/detail <job_url>
```
> ⚠️ BOSS has anti-bot detection. If you see 您的环境存在异常, the browser session needs a manual BOSS visit to solve captcha first.

### Twitter / X
```bash
bb-browser site twitter/search 'AI agent 2025' --json
bb-browser site twitter/bookmarks --json
bb-browser site twitter/notifications --json
bb-browser site twitter/tweets <username> --json
bb-browser site twitter/user <username> --json
bb-browser site twitter/thread <tweet_url> --json
```

### 小红书 (Xiaohongshu)
```bash
bb-browser site xiaohongshu/search '东京旅游' --json
bb-browser site xiaohongshu/feed --json
bb-browser site xiaohongshu/note <note_url> --json
bb-browser site xiaohongshu/me --json
bb-browser site xiaohongshu/user_posts <user_id> --json
```
> Note: Requires logged-in XHS session in Chromium.

### Bilibili
```bash
bb-browser site bilibili/search 'Claude AI' --json
bb-browser site bilibili/trending --json
bb-browser site bilibili/popular --json
bb-browser site bilibili/feed --json
bb-browser site bilibili/history --json
```

### Weibo
```bash
bb-browser site weibo/hot --json
bb-browser site weibo/feed --json
bb-browser site weibo/search <keyword> --json
bb-browser site weibo/user <uid_or_name> --json
```

### Zhihu
```bash
bb-browser site zhihu/hot --json
bb-browser site zhihu/search <keyword> --json
bb-browser site zhihu/question <question_url> --json
```

### Finance & Markets
```bash
bb-browser site xueqiu/hot-stock 5 --json
bb-browser site xueqiu/stock <code> --json
bb-browser site eastmoney/news --json
bb-browser site yahoo-finance/quote AAPL --json
```

### Research / News
```bash
bb-browser site google/search 'Claude AI 2025' --json
bb-browser site reddit/hot programming --json
bb-browser site hackernews/top --json
bb-browser site arxiv/search 'LLM agents' --json
bb-browser site github/issues owner/repo --json
```

### Translation
```bash
bb-browser site youdao/translate '株式会社' --json
```

## Browser Direct Control

For sites without adapters, use raw CDP commands:
```bash
bb-browser open <url>                  # Open URL in current tab
bb-browser open <url> --tab            # Open in new tab
bb-browser snapshot -i                 # Screenshot + page snapshot
bb-browser tab                         # List open tabs
bb-browser tab <index>                 # Switch to tab
bb-browser eval "document.title"       # Run JS in active tab
bb-browser network requests --json     # Capture network traffic
```

## Calling from OpenClaw Skills

When you want to use bb-browser in a Python subprocess inside the container:

```python
import subprocess, json

result = subprocess.run(
    ['bb-browser', 'site', 'twitter/search', query, '--json'],
    capture_output=True, text=True, timeout=30
)
data = json.loads(result.stdout)
```

Or from a skill shell script:
```bash
bb-browser site zhihu/hot --json | python3 -c "import json,sys; items=json.load(sys.stdin); print('\n'.join(i['title'] for i in items[:5]))"
```

## Requirements

- bb-browser daemon running on host at `localhost:19824`
- Real Chrome/Chromium browser open with bb-browser extension installed
- For site-specific adapters: active logged-in session in that browser
