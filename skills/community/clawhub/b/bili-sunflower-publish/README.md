# bili-sunflower-publish

One-click publishing of HTML or Markdown content to Bilibili, supporting both **Article** (专栏) and **Tribee** (小站) targets.

## Features

- 🔐 Auto-detects login status; prompts manual login when needed
- 📝 Smart title handling: extracts from H1, auto-shortens long titles, generates suggestions for meaningless ones
- 📄 Supports both HTML and Markdown input files
- 🖼️ Local images auto-inlined as base64 data URIs (both HTML and Markdown)
- 🚀 One-click publish with full control over article settings (cover, scheduling, originality declaration, etc.)
- ⚡ Direct editor API injection — no system clipboard dependency

## Supported Targets

| Target | Description |
|--------|-------------|
| **Article (专栏)** | Long-form articles on `member.bilibili.com` |
| **Tribee (小站)** | Community posts on `bilibili.com/bubble` |

## Prerequisites

- **OpenClaw** with the `openclaw` browser profile (Playwright-managed browser)

## Trigger Keywords

This skill activates when the user mentions:

> 发布文章到B站 / 上传专栏 / 发B站文章 / 发小站帖子 / tribee发帖 / publish to Bilibili

## Workflow

1. **Navigate & Login Check** — Opens the target editor page and verifies login status
2. **Preprocess & Title** — Runs preprocess script (H1 extraction, heading promotion, image inlining, HTML cleanup); validates title
3. **Insert Article Body** — HTML via ClipboardEvent dispatch, Markdown via `editor.commands.importMarkdown`
4. **Publish** — Applies user-requested settings and clicks the publish button

## File Structure

```
bili-sunflower-publish/
├── SKILL.md                         # Skill definition & detailed workflow
├── README.md                        # This file (English)
├── README_zh.md                     # 中文说明
└── scripts/
    ├── preprocess_html.py           # HTML preprocessor (H1, images, whitespace)
    └── preprocess_md.py             # Markdown preprocessor (H1, images)
```

## Author

**Vicky**
