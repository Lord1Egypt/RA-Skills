---
name: file-to-wechat
description: "将任意文件（PDF、Word、Excel、PPT、图片、音频、网页等）转换为 Markdown，再生成为精美的微信公众号文章并发布到草稿箱。组合 markitdown + md_to_wechat_html + publish_to_wechat 三阶段流水线。Use when the user wants to convert any file to a WeChat article."
version: 1.1.0
prerequisites:
  - anything-to-wechat
tags:
  - wechat
  - markdown
  - file-conversion
  - publishing
  - content-creation
  - chinese
triggers:
  - "文件转微信"
  - "文档发公众号"
  - "PDF发微信"
  - "PPT转公众号"
  - "Excel发微信"
  - "convert file to wechat"
  - "file to wechat article"
  - "任意文件转微信公众号"
  - "转成markdown发微信"
  - "文档转公众号文章"
  - "把这个.*发到.*微信公众号"
  - "把.*转成.*公众号文章"
  - "将.*发布到微信"
---

# File to WeChat

将**任意格式的文件**（PDF、Word、Excel、PPT、图片、音频、网页等）一站式转换为精美的微信公众号文章，并发布到草稿箱。

## User-Facing Promise

Accept requests like:

- "把这个 PDF 发到我的微信公众号"
- "帮我把这个 PPT 转成公众号文章"
- "把这个 Excel 报表发布到微信"
- "把这张图片变成微信文章"
- "把这段音频转成公众号文章"
- "把这个网页内容发到我的公众号"

**Return a published draft in the WeChat draft box, not a proposal.**

## How It Differs from anything-to-wechat

| | anything-to-wechat | file-to-wechat |
|---|---|---|
| **Input** | DOCX, PDF, CSV, Markdown, HTML, URL | **25+ formats**: PDF, DOCX, PPTX, XLSX, images, audio, EPUB, HTML, YouTube, ZIP... |
| **Markdown step** | Reads files directly | Converts to Markdown first via MarkItDown (local) or Markdown Anything API (cloud) |
| **Best for** | Documents and data files | **Any file type** including slides, spreadsheets, images, audio |

Use this skill when the user provides a file type that `anything-to-wechat` doesn't handle natively (PPTX, XLSX, images, audio, EPUB, ZIP).

## First-Time Setup

### 1. Install Python Dependencies

```bash
python -m pip install markitdown markdown beautifulsoup4 requests
```

### 2. Install Companion Skill

This skill uses `publish_to_wechat.py` from the **anything-to-wechat** skill. Install it from ClawHub:

```
clawhub install anything-to-wechat
```

### 3. Configure WeChat Credentials

You need a **WeChat Official Account** (服务号 or 订阅号 with API access).

**Get your credentials:**

1. Log in to https://mp.weixin.qq.com/
2. Go to: 设置与开发 → 基本配置
3. Copy your **AppID** and reset/view **AppSecret**
4. Add your server's public IP to the **IP白名单**

**Set environment variables (recommended):**

On **macOS / Linux** — add to `~/.bashrc` or `~/.zshrc`:
```bash
export WECHAT_APP_ID="your_appid_here"
export WECHAT_APP_SECRET="your_appsecret_here"
```

On **Windows** — use PowerShell:
```powershell
[Environment]::SetEnvironmentVariable("WECHAT_APP_ID", "your_appid_here", "User")
[Environment]::SetEnvironmentVariable("WECHAT_APP_SECRET", "your_appsecret_here", "User")
```

**No environment variables?** The publish script will prompt you interactively on first run — just paste your AppID and AppSecret when asked.

### 4. Verify Setup

```bash
python -c "from markitdown import MarkItDown; print('markitdown OK')"
python -c "import markdown; print('markdown OK')"
```

## Prerequisites

| Dependency | Required | Purpose |
|---|---|---|
| `markitdown` (pip) | Yes | File → Markdown conversion (local, free) |
| `markdown` (pip) | Yes | Markdown → HTML (used by md_to_wechat_html.py) |
| `beautifulsoup4` (pip) | Yes | HTML processing |
| `requests` (pip) | Yes | WeChat API calls |
| **anything-to-wechat** skill | Yes | Provides `publish_to_wechat.py` |
| `all-to-markdown` skill | Optional | Alternative file → Markdown wrapper |
| `html-anything` skill | Optional | Richer HTML design (Approach B only) |
| `markdown-anything` skill | Optional | Cloud Markdown API fallback |

## Workflow

### Phase 1: Collect Input

If the user has NOT provided a source file, ask using AskUserQuestion:

```
Question: "请提供你想发布到微信公众号的文件"
Options:
  - "提供文件路径" (PDF, DOCX, PPTX, XLSX, images, audio, etc.)
  - "粘贴 URL" (web page or YouTube video)
  - "选择文件夹" (batch convert)
```

If the user already provided a file path or URL, **skip and proceed**.

### Phase 2: Convert File to Markdown

**IMPORTANT: Always use UTF-8 encoding.** On Windows, the console defaults to GBK which will garble Chinese text. Use Python with explicit `encoding='utf-8'` for all file I/O and `sys.stdout.reconfigure(encoding='utf-8')` for console output.

**Primary: markitdown pip package (free, no API key, always available)**

```python
python -c "
import sys; sys.stdout.reconfigure(encoding='utf-8')
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert(r'<file_path>')
with open(r'<workspace>/article.md', 'w', encoding='utf-8') as f:
    f.write(result.text_content)
print('Done, length:', len(result.text_content))
"
```

**Alternative: all-to-markdown skill (if installed)**

```bash
bash "<all-to-markdown_skill_dir>/scripts/run.sh" "<file_path>" -o "<workspace>/article.md"
```

**Fallback: markdown-anything (cloud API, requires MDA_API_TOKEN)**

```bash
MDA_API_TOKEN="<token>" bash "<markdown-anything_skill_dir>/scripts/convert.sh" "<file_path>" > "<workspace>/article.md"
```

**After conversion:** Read the Markdown output with `encoding='utf-8'`. Inspect the structure (headings, tables, images, code blocks). Use this to inform the HTML generation style.

### Phase 3: Generate WeChat-Compatible HTML

Two approaches, pick based on content:

**Approach A: Use md_to_wechat_html.py (quick, for structured documents) — PREFERRED**

```bash
python "<skill_dir>/scripts/md_to_wechat_html.py" \
  --input "<workspace>/article.md" \
  --output "<workspace>/wechat_article.html" \
  --title "<article_title>"
```

This script converts Markdown directly to WeChat-ready inline-style HTML with Clockless design tokens. No additional CSS inlining step needed.

**Approach B: Use html-anything (richer design, for complex content)**

1. Load the `html-anything` skill.
2. Feed it the Markdown content as the source.
3. Follow html-anything workflow with WeChat compatibility rules (inline styles, light background, no CSS vars, max-width 680px, system fonts).
4. Then run `anything-to-wechat`'s convert script:

```bash
python "<anything-to-wechat_skill_dir>/scripts/convert_for_wechat.py" \
  --input "<workspace>/wechat_article.html" \
  --output "<workspace>/wechat_article_final.html"
```

**Decision guide:**
- PPTX, XLSX, data-heavy → Approach A (structured, table-friendly)
- Long essays, research papers, narrative → Approach B (richer design)
- Images, audio transcripts → Approach A (simpler layout)

### Phase 4: Generate Cover Image

Use the `ImageGen` tool with a prompt derived from the article's topic and content.

- Save as `wechat_cover.png` in the workspace.
- **Size: `1024x768`** (WeChat cover ratio 4:3).
- Make it visually compelling.

### Phase 5: Publish to WeChat Draft Box

**IMPORTANT: On Windows, use Python subprocess to pass environment variables.**
The `set VAR=val && python ...` pattern does NOT work reliably on Windows CMD.

**Cross-platform approach (recommended):**

```python
python -c "
import os, subprocess, sys
os.environ['WECHAT_APP_ID'] = '<app_id>'
os.environ['WECHAT_APP_SECRET'] = '<app_secret>'
result = subprocess.run([
    sys.executable,
    r'<anything-to-wechat_skill_dir>/scripts/publish_to_wechat.py',
    '--file', r'<workspace>/wechat_article.html',
    '--title', '<article_title>',
    '--cover', r'<workspace>/wechat_cover.png',
    '--digest', '<article_summary_under_120_chars>'
], capture_output=True, text=True, encoding='utf-8')
print(result.stdout)
print(result.stderr)
"
```

**Or with environment variables already set:**

```bash
python "<anything-to-wechat_skill_dir>/scripts/publish_to_wechat.py" \
  --file "<workspace>/wechat_article.html" \
  --title "<article_title>" \
  --cover "<workspace>/wechat_cover.png" \
  --digest "<article_summary_under_120_chars>"
```

**Credentials:** The `publish_to_wechat.py` script reads from `WECHAT_APP_ID` / `WECHAT_APP_SECRET` env vars. If not set, it will **prompt interactively** — the user just needs to paste their AppID and AppSecret.

### Phase 6: Confirm & Handoff

Report success with Media ID and link to `https://mp.weixin.qq.com/`.

Tell the user: "文章已发送到你的微信公众号草稿箱，请登录微信公众平台审核后一键发布。"

## WeChat HTML Compatibility

Same rules as `anything-to-wechat`:

- Inline styles only (no `<style>` tags)
- Light background (#ffffff)
- No CSS variables
- No `position: fixed/sticky`
- System fonts
- `max-width: 680px`
- Under 2MB total

## Error Handling

| Error | Action |
|---|---|
| `markitdown` not installed | Run `python -m pip install markitdown` |
| `all-to-markdown` not installed | Use `markitdown` pip package directly (primary method) |
| `markdown-anything` token missing | Use `markitdown` (free) or ask user for `MDA_API_TOKEN` |
| MarkItDown fails on format | Try `markdown-anything` cloud API |
| Scanned PDF (no text) | Use `markdown-anything` with `MDA_ENHANCED_AI=true` |
| Markdown too large for WeChat | Summarize, keep under 5000 words |
| Chinese characters garbled (GBK) | Add `sys.stdout.reconfigure(encoding='utf-8')` and use `encoding='utf-8'` for all file I/O |
| Windows `set VAR=val` fails | Use Python subprocess with `os.environ` to pass env vars |
| WeChat credentials missing | `publish_to_wechat.py` prompts interactively — paste AppID/AppSecret |
| IP not in whitelist | Show IP from error, guide user to add at mp.weixin.qq.com, retry |
| `anything-to-wechat` skill missing | Install: `clawhub install anything-to-wechat` |

## Supported Input Formats

| Category | Formats |
|---|---|
| Documents | PDF, DOCX, PPTX, EPUB, MSG |
| Data | XLSX, XLS, CSV, JSON, XML |
| Images | JPG, PNG, GIF, BMP, TIFF (with EXIF metadata, optional OCR) |
| Audio | WAV, MP3 (with speech transcription) |
| Web | HTML pages, YouTube URLs (subtitle extraction) |
| Archives | ZIP (converts each file inside) |

## Script Reference

| Script | Source | Purpose |
|---|---|---|
| `markitdown` (pip) | Microsoft MarkItDown | File/URL → Markdown (local, free) |
| `scripts/md_to_wechat_html.py` | **this skill** | Markdown → WeChat inline HTML |
| `anything-to-wechat/scripts/convert_for_wechat.py` | anything-to-wechat skill | CSS inlining & WeChat cleanup |
| `anything-to-wechat/scripts/publish_to_wechat.py` | anything-to-wechat skill | Upload to WeChat draft box |

## Configuration

| Variable | Required | Description |
|---|---|---|
| `WECHAT_APP_ID` | Yes | WeChat Official Account AppID (or prompted interactively) |
| `WECHAT_APP_SECRET` | Yes | WeChat Official Account AppSecret (or prompted interactively) |
| `MDA_API_TOKEN` | No | Markdown Anything API token (only if using cloud API fallback) |
