# Anything to WeChat

One-step workflow: turn any file, folder, URL, or idea into a polished WeChat Official Account article.

## Features

- **Universal input** — PDF, DOCX, CSV, Markdown, HTML, URLs, folders, or plain text ideas
- **Smart HTML generation** — Uses `html-anything` skill with 17+ design systems for professional output
- **Auto WeChat conversion** — Inlines CSS, resolves variables, converts dark themes to light
- **AI cover image** — Generates topic-relevant cover images automatically
- **One-click publish** — Uploads directly to your WeChat draft box for review and publishing

## Quick Start

### Prerequisites

1. Install the `html-anything` skill from ClawHub

### First-Time Setup

You'll need your own WeChat Official Account credentials. Each user must configure their own — never share credentials.

1. **Get AppID & AppSecret**: Log in to [mp.weixin.qq.com](https://mp.weixin.qq.com/) → Settings → Basic Config → copy AppID, reset/view AppSecret.
2. **Add IP to Whitelist**: In Basic Config → IP Whitelist → add your server's public IP.
3. **Set environment variables**:
   ```bash
   export WECHAT_APP_ID="your_appid_here"
   export WECHAT_APP_SECRET="your_appsecret_here"
   ```
   If not set, the skill will prompt you interactively on first use.

### Usage

Simply tell the agent:

```
把这篇论文发到我的微信公众号草稿箱
```

Or provide a file directly:

```
C:\path\to\your\document.pdf
```

The skill handles everything: reading the source, generating beautiful HTML, converting for WeChat compatibility, generating a cover image, and publishing to your draft box.

## How It Works

```
Input (any format)
    ↓
html-anything (generate polished HTML)
    ↓
convert_for_wechat.py (inline CSS, dark→light, remove incompatible)
    ↓
ImageGen (generate cover image)
    ↓
publish_to_wechat.py (upload to WeChat draft box)
    ↓
WeChat Draft Box (review & publish)
```

## Scripts

| Script | Description |
|---|---|
| `scripts/convert_for_wechat.py` | Converts HTML with `<style>` tags to WeChat-compatible inline styles |
| `scripts/publish_to_wechat.py` | Publishes HTML articles to WeChat Official Account draft box |

Both scripts auto-install missing Python dependencies.

### convert_for_wechat.py

```bash
python scripts/convert_for_wechat.py \
    --input article.html \
    --output wechat_article.html
```

### publish_to_wechat.py

```bash
WECHAT_APP_ID=wxXXX WECHAT_APP_SECRET=xxx \
python scripts/publish_to_wechat.py \
    --file wechat_article.html \
    --title "Article Title" \
    --cover cover.png \
    --digest "Article summary" \
    --author "Author Name"
```

## WeChat Compatibility

WeChat strips many standard HTML/CSS features. This skill handles:

| Stripped by WeChat | Our Solution |
|---|---|
| `<style>` tags | Inline `style=""` attributes |
| CSS variables | Resolved to literal values |
| `position: fixed/sticky` | Removed |
| Dark themes | Converted to light |
| External fonts | System font fallback |
| `<script>` tags | Removed |
| Complex layouts | Simple block/table layouts |

## Configuration

| Variable | Required | Description |
|---|---|---|
| `WECHAT_APP_ID` | Yes | WeChat Official Account AppID |
| `WECHAT_APP_SECRET` | Yes | WeChat Official Account AppSecret |

## Troubleshooting

| Issue | Solution |
|---|---|
| IP not in whitelist | Add your server IP in WeChat backend: Settings → Basic Config → IP Whitelist |
| Invalid AppSecret | Reset your AppSecret in WeChat backend: Settings → Basic Config |
| HTML too large | Keep articles under 2MB; simplify content or reduce images |
| Images not showing | Ensure images use `<img>` tags with explicit styles |

## Dependencies

- **Skills**: `html-anything` (required)
- **Python packages**: `requests`, `beautifulsoup4`, `cssutils` (auto-installed)

## License

MIT
