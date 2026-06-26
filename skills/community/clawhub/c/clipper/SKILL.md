---
name: clipper
version: 1.0.0
description: Save web content to Obsidian vault. Supports Twitter/X, WeChat MP, Xiaohongshu, YouTube, Bilibili, and any web page. Automatically routes to the best fetch method per platform.
---

# Clipper

Unified web content clipper for Obsidian. One entry point, auto-detects platform, uses optimal method.

## Usage

When user provides a URL and wants to save it:

```bash
python3 {{SKILL_DIR}}/scripts/clip.py "<url>"
```

**Output:**
- Twitter: `<vault>/clippings/tweet/YYYY-MM-DD-<handle>-<id>.md`
- Other: `<vault>/clippings/web/<domain>/YYYY-MM-DD-<slug>.md`

## Platform Routing

| Platform | Method | Why |
|----------|--------|-----|
| Twitter/X | Jina Reader | Fast, reliable, no auth needed |
| WeChat MP | Browser snapshot | Handles JS rendering |
| Xiaohongshu | x-reader | Works well |
| YouTube | x-reader | Gets description/metadata |
| Bilibili | x-reader | Works well |
| Other | x-reader | General purpose |

## Workflows

### Twitter / General Web (Auto)

```bash
python3 {{SKILL_DIR}}/scripts/clip.py "https://x.com/user/status/123"
```

One command, done.

### WeChat MP (Two-step)

WeChat articles need browser rendering. The script will return `needs_browser: true`.

**Step 1:** Open in browser
```
browser action=open profile=openclaw targetUrl=<url>
```

**Step 2:** Get snapshot
```
browser action=snapshot profile=openclaw targetId=<targetId>
```

**Step 3:** Extract content and save
```bash
python3 {{SKILL_DIR}}/scripts/wechat.py \
  --url "<url>" \
  --title "<title>" \
  --author "<author>" \
  --date "<date>" \
  --content "<markdown>"
```

Or pipe content via stdin:
```bash
echo "<markdown>" | python3 {{SKILL_DIR}}/scripts/wechat.py \
  --url "<url>" \
  --title "<title>"
```

## Supported URL Formats

**Twitter:**
- `https://twitter.com/<handle>/status/<id>`
- `https://x.com/<handle>/status/<id>`

**WeChat:**
- `https://mp.weixin.qq.com/s/<id>`

**Others:**
- Any valid HTTP/HTTPS URL

## Requirements

- `obsidian-cli` (for vault detection) OR manually configured vault path
- `x-reader` for general web: `pipx install 'git+https://github.com/runesleo/x-reader.git'`

## Example

```
User: https://x.com/naval/status/1234567890 save this
You: [runs clip.py] → Saved to clippings/tweet/2026-03-18-naval-1234567890.md

User: https://mp.weixin.qq.com/s/abc123 保存这个
You: [runs clip.py] → needs_browser: true
    [opens browser, gets snapshot]
    [extracts content, runs wechat.py]
    → Saved to clippings/web/mp_weixin_qq_com/2026-03-18-article-title.md
```

## Git Sync

All saves trigger automatic git sync: `pull --rebase → add → commit → push`

Git warnings (non-fatal) are returned in `git_warnings` array.
