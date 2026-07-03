# File to WeChat

将任意格式文件（PDF、Word、Excel、PPT、图片、音频、网页等）一站式转换为精美的微信公众号文章。

## Features

- **25+ input formats** — PDF, DOCX, PPTX, XLSX, images, audio, EPUB, HTML, YouTube, ZIP
- **Local conversion** — MarkItDown (Microsoft), free, no API key needed
- **Smart HTML generation** — Auto-styled with Clockless design tokens for WeChat
- **AI cover image** — Generates topic-relevant cover images
- **One-click publish** — Uploads directly to WeChat draft box

## First-Time Setup

### 1. Install Dependencies

```bash
python -m pip install markitdown markdown beautifulsoup4 requests
```

### 2. Install Companion Skill

```bash
clawhub install anything-to-wechat
```

### 3. Configure WeChat Credentials

1. Log in to https://mp.weixin.qq.com/
2. Go to: 设置与开发 → 基本配置
3. Copy your **AppID** and **AppSecret**
4. Add your server IP to the **IP白名单**

Set environment variables (or the script will prompt you interactively on first run):

**macOS / Linux:**
```bash
export WECHAT_APP_ID="your_appid"
export WECHAT_APP_SECRET="your_appsecret"
```

**Windows (PowerShell):**
```powershell
[Environment]::SetEnvironmentVariable("WECHAT_APP_ID", "your_appid", "User")
[Environment]::SetEnvironmentVariable("WECHAT_APP_SECRET", "your_appsecret", "User")
```

## How It Works

```
File (any format)
    |
    v
markitdown (Python) --> article.md
    |
    v
md_to_wechat_html.py --> wechat_article.html (inline styles, WeChat-safe)
    |
    v
ImageGen --> wechat_cover.png
    |
    v
publish_to_wechat.py --> WeChat Draft Box
    |
    v
Review at mp.weixin.qq.com --> Publish
```

## Quick Start

Simply tell the agent:

```
把这个 PPT 发到我的微信公众号
```

Or provide a file path:

```
C:\path\to\presentation.pptx
```

## Scripts

| Script | Description |
|---|---|
| `scripts/md_to_wechat_html.py` | Converts Markdown to WeChat-compatible inline-style HTML |

Other scripts from companion skill:
- `anything-to-wechat/scripts/publish_to_wechat.py` — WeChat draft publishing

## Supported Formats

| Category | Formats |
|---|---|
| Documents | PDF, DOCX, PPTX, EPUB, MSG |
| Data | XLSX, XLS, CSV, JSON, XML |
| Images | JPG, PNG, GIF, BMP, TIFF |
| Audio | WAV, MP3 (with transcription) |
| Web | HTML, YouTube URLs |
| Archives | ZIP |

## Configuration

| Variable | Required | Description |
|---|---|---|
| `WECHAT_APP_ID` | Yes | WeChat Official Account AppID (or prompted interactively) |
| `WECHAT_APP_SECRET` | Yes | WeChat Official Account AppSecret (or prompted interactively) |
| `MDA_API_TOKEN` | No | Markdown Anything API token (cloud fallback only) |

## License

MIT
