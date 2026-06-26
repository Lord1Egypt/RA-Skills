---
name: content-repurposer
description: Repurpose a single piece of content (tweet, article, description) into 10+ formats: Twitter thread, LinkedIn post, blog intro, email newsletter, Discord announcement, Reddit post, Quora answer, Instagram caption, email subject lines, and meta descriptions.
tools:
  - repurpose_content
---

# Content Repurposer

Repurpose any content into 10+ marketing formats instantly.

## Usage

```bash
uv run python scripts/repurpose.py "Your content here" [--type auto] [--tone professional|casual|humorous] [--output ./output]
```

## Arguments

- `content` (required): The source content — a tweet, article text, product description, or any string.
- `--type` (optional): Override auto-detection. Values: `tweet`, `article`, `description`, `speech`, `email`.
- `--tone` (optional): Writing tone. Values: `professional` (default), `casual`, `humorous`, `inspirational`, `technical`.
- `--output` (optional): Output directory for individual files. Defaults to `./output`.

## Output Formats

| Format | Description |
|--------|-------------|
| **Twitter Thread** | 5-7 tweet thread with hook, points, CTA |
| **LinkedIn Post** | Professional post with 3-5 key insights |
| **Blog Intro** | 200-word engaging blog introduction |
| **Email Newsletter** | Full newsletter paragraph with subject line |
| **Discord Announcement** | Server-friendly announcement with emoji formatting |
| **Reddit Post** | Title + body for relevant subreddit |
| **Quora Answer** | Informative answer to a related question |
| **Instagram Caption** | Engaging caption with hashtags |
| **Email Subject Lines** | 5 compelling subject line variants |
| **Meta Descriptions** | 3 SEO-optimized meta descriptions |

## Workflow

1. **Input**: Content is analyzed and classified
2. **Generation**: Each format is generated with platform-specific optimization
3. **Output**: All formats returned as structured JSON

## Error Handling

All outputs return JSON with `success` field:
- `success: true` — Operation completed, check `results` dict
- `success: false` — Check `error_code` and `error_message`

## Notes

- Uses MiniMax API via OpenClaw for generation
- Rate limiting handled with exponential backoff
- Empty content returns an error with code `EMPTY_CONTENT`