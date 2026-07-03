---
name: anything-to-wechat
description: "One-step workflow: accept any file (PDF, DOCX, CSV, Markdown), folder, URL, or idea → generate polished HTML via html-anything → auto-convert for WeChat compatibility → publish to WeChat Official Account draft box. Use when the user wants to publish content to WeChat, send articles to WeChat, turn anything into a WeChat post, or convert documents for WeChat publishing."
version: 2.0.0
prerequisites:
  - html-anything
tags:
  - wechat
  - publishing
  - content-creation
  - document-conversion
  - chinese
triggers:
  - "发布到微信"
  - "发到公众号"
  - "微信文章"
  - "publish to wechat"
  - "send to wechat"
  - "turn into wechat post"
  - "convert for wechat"
  - "发到我的微信"
  - "微信公众号"
  - "一键发布"
  - "草稿箱"
---

# Anything to WeChat

Turn **any file, folder, URL, or idea** into a **published WeChat Official Account draft** in one seamless workflow.

## User-Facing Promise

Accept requests like:

- "把这篇论文发到我的微信公众号草稿箱"
- "用这个 CSV 做个报告发到微信"
- "把这个 URL 的内容变成微信文章"
- "帮我把桌面上的 PDF 发布到公众号"
- "Publish this research paper to my WeChat account"
- "把这个文件夹做成微信文章"

**Return a published draft in the WeChat draft box, not a proposal.**

## Prerequisites

This skill depends on:

1. **`html-anything`** — generates the polished HTML page from any input. **Must be installed.**

The publishing and conversion scripts are self-contained in this skill's `scripts/` directory. No additional skills are required for publishing.

## First-Time Setup (Required)

Before using this skill, every user **must** configure their own WeChat Official Account credentials. These credentials are unique to each account — never share them.

### Step 1: Get Your AppID and AppSecret

1. Log in to [微信公众平台](https://mp.weixin.qq.com/) with your WeChat Official Account.
2. Navigate to: **设置与开发** → **基本配置**
3. Copy your **AppID** (开发者ID).
4. Click **重置** to generate a new **AppSecret** (开发者密码), then copy it immediately (it will not be shown again).

### Step 2: Add IP to Whitelist

1. In the same **基本配置** page, find **IP白名单**.
2. Click **查看** or **修改**.
3. Add the public IP address of the server running this skill. The skill will display the required IP if it's missing (from the API error message).
4. Save the whitelist.

### Step 3: Set Environment Variables

Set the credentials as environment variables so the skill can read them automatically:

**macOS / Linux:**
```bash
export WECHAT_APP_ID="your_appid_here"
export WECHAT_APP_SECRET="your_appsecret_here"
```

**Windows (Command Prompt):**
```cmd
set WECHAT_APP_ID=your_appid_here
set WECHAT_APP_SECRET=your_appsecret_here
```

**Windows (PowerShell):**
```powershell
$env:WECHAT_APP_ID="your_appid_here"
$env:WECHAT_APP_SECRET="your_appsecret_here"
```

If environment variables are not set, the skill will prompt you interactively to provide them on first use.

### Step 4: Test Your Setup

Try publishing a simple article. If you see `[SUCCESS] Draft published successfully!`, your setup is complete. If you get an IP whitelist error, go back to Step 2 and add the IP shown in the error message.

## Workflow

### Phase 1: Collect Input

If the user has NOT provided a source, ask using the AskUserQuestion tool:

```
Question: "请提供你想发布到微信公众号的内容来源"
Options:
  - "上传文件" (PDF, DOCX, CSV, Markdown, HTML, etc.)
  - "选择文件夹" (turn a folder into a browsable page)
  - "粘贴 URL" (fetch and transform a web page)
  - "描述一个想法" (generate from a text brief)
```

If the user has already provided a file path, URL, or brief in their message, **skip the question and proceed directly**.

### Phase 2: Generate HTML via html-anything

1. **Load the `html-anything` skill** by calling the Skill tool with `skill: "html-anything"`.
2. **Follow the html-anything workflow** exactly:
   - Inspect the source or brief.
   - Choose auto style based on use-case taxonomy.
   - Build the page following all html-anything guidelines.
3. **Save the HTML** to the workspace as `wechat_article.html`.

**Critical WeChat compatibility rules** (apply during HTML generation):

| Rule | Why |
|---|---|
| Use **inline styles only** | WeChat strips all `<style>` tags and `<link>` stylesheet tags |
| Use **light background** (`#ffffff` / `#fafafa`) | WeChat renders on white; dark themes are invisible |
| **Avoid CSS variables** | `var(--xxx)` is stripped by WeChat |
| **Avoid `position: fixed/sticky`** | WeChat strips these properties |
| **Avoid complex flex/grid** | Use simple block layouts or `<table>` elements |
| **`max-width: 680px`** | WeChat article reading width |
| **System fonts only** | `-apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif` |
| **Total HTML under 2MB** | WeChat API hard limit |
| All images as `<img>` with explicit `style` | WeChat only accepts standard img tags |
| Use `<section>` instead of `<div>` for wrappers | Better WeChat compatibility |

### Phase 3: Convert to WeChat-Compatible HTML

Run the conversion script to ensure full WeChat compatibility:

```bash
python "<skill_dir>/scripts/convert_for_wechat.py" \
  --input "<path_to_generated_html>" \
  --output "<path_to_wechat_ready_html>"
```

The script performs:

1. Extracts CSS from `<style>` tags and converts to inline `style` attributes
2. Recursively resolves all CSS variables (`var(--xxx)`) to literal values
3. Converts dark theme backgrounds to light equivalents
4. Removes WeChat-incompatible CSS properties (position, z-index, backdrop-filter, etc.)
5. Removes `<script>` tags (not supported by WeChat)
6. Wraps content in a `<section>` element with WeChat-friendly base styles

### Phase 4: Generate Cover Image

If the html-anything step did not generate a suitable hero image, generate one:

- Use the `ImageGen` tool with a prompt derived from the article's topic and content.
- Save as `wechat_cover.png` in the workspace.
- **Preferred size: `1024x768`** (WeChat cover ratio 4:3).
- Make it visually compelling — the cover image directly affects click-through rate.

If the article already contains a prominent hero image, extract and reuse it.

### Phase 5: Publish to WeChat Draft Box

#### 5a. Get Credentials

Read credentials from environment variables:

- `WECHAT_APP_ID` — WeChat Official Account AppID
- `WECHAT_APP_SECRET` — WeChat Official Account AppSecret

If not available, ask the user using AskUserQuestion:

```
Question: "请提供你的微信公众号 API 凭证"
Options:
  - "提供 AppID 和 AppSecret"
  - "我需要帮助找到这些信息"
```

Guide the user if they need help:
- Log in to [微信公众平台](https://mp.weixin.qq.com/)
- Go to: 设置与开发 → 基本配置
- Find AppID and reset/view AppSecret
- Add the server's public IP to the IP whitelist (IP白名单)

#### 5b. Publish

Run the publishing script:

```bash
WECHAT_APP_ID=<app_id> WECHAT_APP_SECRET=<app_secret> \
python "<skill_dir>/scripts/publish_to_wechat.py" \
  --file "<path_to_wechat_ready_html>" \
  --title "<article_title>" \
  --cover "<path_to_cover_image>" \
  --digest "<article_summary_under_120_chars>"
```

**Important:** Always generate a meaningful `--digest` (article summary, under 120 Chinese characters) for the WeChat article preview.

#### 5c. Handle IP Whitelist Errors

If the API returns `ip not in whitelist`:

1. Extract the server's public IP from the error message.
2. Tell the user: "请将 IP `<ip>` 添加到微信公众号后台的 IP 白名单中（设置与开发 → 基本配置 → IP白名单）。"
3. Wait for user confirmation, then retry the publish command.

### Phase 6: Confirm & Handoff

After successful publishing:

1. Report success with the **Media ID**.
2. Provide the link to WeChat backend: `https://mp.weixin.qq.com/`
3. Tell the user: "文章已发送到你的微信公众号草稿箱，请登录微信公众平台审核后一键发布。"

## WeChat HTML Compatibility Reference

### Stripped by WeChat (do NOT use)

| Category | Properties / Elements |
|---|---|
| CSS Elements | `<style>`, `<link rel="stylesheet">`, `<script>` |
| CSS Features | `var(--xxx)`, `@media (prefers-color-scheme: dark)`, `@import` |
| Position | `position: fixed`, `position: sticky` |
| Stacking | `z-index` |
| Visual Effects | `backdrop-filter`, `filter`, `mix-blend-mode`, `clip-path`, `mask` |
| Layout | Complex `display: flex`, `display: grid`, `overflow: hidden/scroll` |
| Fonts | External web fonts (`@font-face`, Google Fonts `<link>`) |
| Colors | CSS variables, `color-scheme: dark` |

### Safe for WeChat (always use)

| Category | Values |
|---|---|
| Styling | Inline `style="..."` attributes on every element |
| Layout | Block flow, `<table>` for tabular data, simple `text-align` |
| Fonts | `-apple-system, 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', sans-serif` |
| Colors | Literal hex/rgb values: `#ffffff`, `rgb(30, 27, 25)` |
| Images | `<img src="..." style="max-width:100%;height:auto;">` |
| Containers | `<section>` wrappers with inline styles |
| Width | `max-width: 680px` on outer container |

## Error Handling

| Error | Action |
|---|---|
| `html-anything` skill missing | Stop and tell user: "请先安装 html-anything 技能" |
| No AppID / AppSecret | Ask user for credentials via AskUserQuestion |
| IP not in whitelist | Show IP from error, guide user to add it in WeChat backend, then retry |
| Cover image upload fails | Retry once; if still fails, try with a smaller image or different format |
| HTML too large (>2MB) | Simplify content, reduce image sizes, remove non-essential sections |
| `invalid content` from WeChat | Re-run convert_for_wechat.py, check for remaining `<style>` tags |
| Access token expired | Re-fetch token automatically and retry |
| Network timeout | Retry once after 5 seconds |
| Image in article fails to upload | Skip that image, log warning, continue publishing |

## Supported Input Types

| Format | Extension | Notes |
|---|---|---|
| PDF | `.pdf` | Read and extract text/structure, generate HTML |
| Word | `.docx` | Read paragraphs/tables/headings, generate HTML |
| Markdown | `.md` | Convert to structured HTML with inline styles |
| CSV / Excel | `.csv`, `.xlsx` | Generate data-driven HTML with tables |
| HTML | `.html` | Re-style for WeChat compatibility |
| Plain Text | `.txt` | Structure and format, then generate HTML |
| URL | Any URL | Fetch content, generate HTML |
| Folder | Directory | Browse files, generate overview/atlas HTML |
| Idea / Brief | Text input | Expand into full article, generate HTML |

## Optimization Tips

- **Article length**: Keep under 5000 words for best WeChat reading experience.
- **Long sources**: For 30+ page PDFs, summarize and extract key findings rather than reproducing the full text.
- **Images**: WeChat auto-compresses uploaded images. Use PNG for diagrams, JPEG for photos.
- **Mobile-first**: Most WeChat users read on phones. Test readability at 375px width.
- **Cover image**: Critical for click-through rate. Make it visually compelling and relevant.

## Script Reference

| Script | Purpose | Usage |
|---|---|---|
| `scripts/convert_for_wechat.py` | Convert CSS to inline styles, dark→light, remove incompatible props | `python convert_for_wechat.py --input in.html --output out.html` |
| `scripts/publish_to_wechat.py` | Upload cover + article to WeChat draft box via API | `python publish_to_wechat.py --file out.html --title "..." --cover img.png` |

Both scripts auto-install missing Python dependencies (`beautifulsoup4`, `cssutils`, `requests`).

## Configuration

| Environment Variable | Required | Description |
|---|---|---|
| `WECHAT_APP_ID` | Yes | WeChat Official Account AppID |
| `WECHAT_APP_SECRET` | Yes | WeChat Official Account AppSecret |

Both can be set as environment variables or provided interactively when prompted.
