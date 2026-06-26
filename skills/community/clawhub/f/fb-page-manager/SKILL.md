---
name: fb-page-poster
description: Publish posts to a Facebook Page via the Meta Graph API. Use when the user says "post to Facebook", "FB post", "粉專發文", "社群貼文", "幫我發文", "schedule post", "排程發文", or provides content and says "post this" or "publish this". Supports text-only, image, link-in-comment, scheduled posts, and multilingual translation (ZH↔EN) with a review step before publishing.
version: 1.0.0
metadata: {"openclaw": {"emoji": "📘", "requires": {"env": ["LONG_META_page_TOKEN", "META_PAGE_ID", "META_APP_SECRET"], "bins": ["node"]}, "primaryEnv": "LONG_META_page_TOKEN"}}
---

# Facebook Page Poster

Publish content to a Facebook Page through the Meta Graph API.

## Environment Variables

| Variable | Purpose |
|---|---|
| `LONG_META_page_TOKEN` | Long-lived Page Access Token with `pages_manage_posts` and `pages_read_engagement` permissions |
| `META_PAGE_ID` | Numeric Page ID |
| `META_APP_SECRET` | Meta App Secret for appsecret_proof |

If any are missing, walk the user through `{baseDir}/references/token-setup-guide.md`.

## Workflow

### 1. Parse the request

Extract from the user message:
- **Content**: the text to post
- **Language direction**: ZH→EN, EN→ZH, ZH→ZH, or EN→EN
- **Post type**: text | image | link-in-comment | scheduled (combinable)
- **Tone**: infer automatically — marketing/social (upbeat, CTA) for promotions and events; formal/professional for announcements and corporate. Ask if ambiguous.
- **Image**: local file path or URL (if applicable)
- **Schedule**: ISO 8601 timestamp (if applicable)
- **Link**: URL for the first comment (if applicable)

### 2. Draft and translate — always preview first

**Never publish without user confirmation.**

If source language differs from target, translate with these rules:
- Preserve meaning, intent, hashtags
- Adapt idioms naturally, do not translate literally
- Keep brand names and proper nouns in original form
- Maintain emoji usage unless unnatural in target language

Present preview:

```
📋 Post Preview
─────────────────
[Post text here]

🔗 First comment: [URL or N/A]
🖼️ Image: [filename/URL or N/A]
⏰ Schedule: [time or "Publish immediately"]
─────────────────
Confirm? (yes / edit / cancel)
```

### 3. Publish

Run the script at `{baseDir}/scripts/fb-post.js`:

```bash
# Text-only
node {baseDir}/scripts/fb-post.js --type text --message "content"

# Image (file)
node {baseDir}/scripts/fb-post.js --type image --message "content" --image-file /path/to/img.jpg

# Image (URL)
node {baseDir}/scripts/fb-post.js --type image --message "content" --image-url "https://..."

# Link in first comment
node {baseDir}/scripts/fb-post.js --type text --message "content" --comment-link "https://..."

# Scheduled (append to any above)
node {baseDir}/scripts/fb-post.js --type text --message "content" --schedule "2025-12-25T10:00:00+0800"
```

Flags are combinable. Example — image + comment link + scheduled:

```bash
node {baseDir}/scripts/fb-post.js --type image --message "content" --image-url "https://..." --comment-link "https://..." --schedule "2025-12-25T10:00:00+0800"
```

### 4. Report result

- Show the post ID
- Confirm comment was posted (if link-in-comment)
- Confirm scheduled time (if scheduled)
- On error, show the message and suggest a fix

## Error reference

| Error | Likely cause | Fix |
|---|---|---|
| OAuthException / Invalid token | Token expired | Refresh via `{baseDir}/references/token-setup-guide.md` |
| Permission denied | Missing `pages_manage_posts` | Re-authorize token with correct scopes |
| Scheduled time in past | Must be ≥10 min in the future | Adjust the timestamp |
| Image too large | >10 MB | Compress or resize |
| Rate limit | Too many requests | Wait a few minutes, retry |
