---
name: content-news-thai
description: Generate news-style social media images (1080x1350) with Thai text overlay and matching captions. Use when asked to create content, make a news post image, generate a headline image with Thai text, or produce a full content set (image + caption) for Facebook/Instagram. Handles Thai fonts (Kanit, Prompt, Sarabun) rendered pixel-perfect via canvas. Triggers on "ทำ content", "ทำรูปข่าว", "สร้างรูปโพส", "make content", "news image", "headline image".
---

# Content News Thai

Generate news-style post images with Thai text overlay + captions for social media.

## Setup (first time only)

Run the setup script to install dependencies (canvas, Thai fonts):

```bash
bash <SKILL_DIR>/scripts/setup.sh
```

On Docker/VPS this installs: libcairo2, libpango, Thai fonts (Kanit, Prompt, Sarabun).
On macOS: uses Homebrew for cairo/pango.

## Generate News Image

```bash
cd <SKILL_DIR>/scripts && node gen-news.mjs '<json>'
```

### Parameters

| Param | Required | Description |
|---|---|---|
| headline | ✅ | Main headline (Thai/English, auto-wraps) |
| sub | | Sub-headline text |
| badge | | Badge label (default: "AI NEWS") |
| badgeColor | | Badge color (default: "#CC0000") |
| bgImage | | Background image path or URL |
| bgColor | | Fallback bg gradient color (default: "#0a0a1a") |
| source | | Source attribution at bottom |
| output | ✅ | Output file path (.jpg) |
| brandName | | Watermark text (bottom-right) |
| accentColor | | Bottom bar color (default: "#CC0000") |

### Example

```bash
cd <SKILL_DIR>/scripts && node gen-news.mjs '{"headline":"AI กำลังเปลี่ยนวงการค้าปลีก","sub":"ยอดขายพุ่ง 40% ใน 6 เดือน","badge":"BREAKING NEWS","source":"Reuters • มี.ค. 2026","brandName":"MY BRAND","output":"/tmp/news_post.jpg"}'
```

Output: JSON `{"status":"done","output":"/tmp/news_post.jpg","size":"1080x1350","type":"image"}`

## Background Image

Two approaches:
1. **With bgImage** — provide a path/URL to a photo. The script covers it with dark gradient for text readability.
2. **Without bgImage** — generates a dark gradient background with subtle grid pattern. Good for text-focused posts.

For best results, generate a background image first (use the AI model's image generation), save it, then pass the path as `bgImage`.

## Workflow: Full Content Set

When asked to create a complete content set:

1. **Write headline + sub** — short, punchy, Thai-friendly
2. **Generate background** — use AI image gen or use bgColor for clean look
3. **Run gen-news.mjs** — creates 1080x1350 image with Thai text overlay
4. **Write caption** — storytelling style, short sentences, end with engaging question
5. **Return** — image path + caption to user

## Caption Style Guide

- Open with a scroll-stopping hook (short, impactful)
- Tell the story with short sentences, reveal layer by layer
- Include the brand's perspective/opinion
- End with: impact summary → specific question → soft share cue (if appropriate)
- Add 3-5 relevant hashtags
- Do NOT end with generic "คิดเห็นยังไงคอมเมนต์มา"

## Troubleshooting

- **"canvas" error** → rerun setup.sh
- **Fonts look wrong** → check assets/fonts/ has .ttf files, rerun setup.sh
- **bgImage not found** → use absolute path or URL
