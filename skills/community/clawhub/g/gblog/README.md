# gblog — Blogger CLI Skill for OpenClaw

Manage your Google Blogger blogs directly from your AI assistant. Publish, edit, delete, list, and monitor blog posts — all through natural language or command line.

---

## Features

- **Publish posts** — Create new blog posts with HTML content
- **Edit posts** — Update title or content of existing posts
- **Delete posts** — Remove posts with confirmation prompt
- **List posts** — Browse all posts across your blogs
- **Bulk publish** — Publish multiple posts at once from HTML files
- **Monitor** — Watch for new or updated posts in real time
- **OAuth flow** — Secure Google authentication via browser

---

## Setup

### 1. Enable Blogger API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (e.g., `my-blogger`)
3. Navigate to **APIs & Services → Library**
4. Search for **Blogger API v3** and enable it
5. Go to **APIs & Services → Credentials**
6. Click **Create Credentials → OAuth 2.0 Client ID**
7. Application type: **Web application**
8. Add redirect URIs:
   ```
   http://localhost:8085/oauth2callback
   http://localhost:8080/oauth2callback
   ```
9. Download the credentials JSON file

### 2. Save Credentials

```bash
mkdir -p ~/.config/gblog
cp ~/Downloads/client_secret_*.json ~/.config/gblog/credentials.json
chmod 600 ~/.config/gblog/credentials.json
```

### 3. Install Dependencies

```bash
pip install youtube-transcript-api  # optional, for transcript-based blog generation
```

### 4. Authenticate

```bash
python3 scripts/gblog.py auth
```

This opens your browser for Google OAuth. After approving, your token is saved to `~/.config/gblog/token.json`.

---

## Usage

### Authentication

```bash
python3 scripts/gblog.py auth           # Authenticate
python3 scripts/gblog.py auth --status  # Check auth status
python3 scripts/gblog.py auth --logout  # Clear saved tokens
```

### Blog Management

```bash
python3 scripts/gblog.py list-blogs     # List all your blogs
```

### Post Management

```bash
# List posts
python3 scripts/gblog.py list-posts --blog-id YOUR_BLOG_ID

# Create a post
python3 scripts/gblog.py post \
  --blog-id YOUR_BLOG_ID \
  --title "My Post Title" \
  --content ./post.html \
  --labels "AI, Tutorial"

# Create as draft
python3 scripts/gblog.py post \
  --blog-id YOUR_BLOG_ID \
  --title "Draft Post" \
  --content ./post.html \
  --draft

# Edit a post
python3 scripts/gblog.py edit \
  --blog-id YOUR_BLOG_ID \
  --post-id POST_ID \
  --content ./updated.html

# Delete a post
python3 scripts/gblog.py delete --blog-id YOUR_BLOG_ID --post-id POST_ID

# Get post details
python3 scripts/gblog.py get-post --blog-id YOUR_BLOG_ID --post-id POST_ID
```

### Bulk Publish

```bash
# Publish multiple posts from a folder of HTML files
python3 scripts/gblog-bulk-post.py \
  --blog-id YOUR_BLOG_ID \
  --posts-dir ./html-posts/ \
  --update-json posts.json
```

### Monitor

```bash
# Watch for new/updated posts (checks every 5 minutes)
python3 scripts/gblog-monitor.py --blog-id YOUR_BLOG_ID --interval 300

# One-time check
python3 scripts/gblog-monitor.py --blog-id YOUR_BLOG_ID --once
```

---

## HTML Content Format

Posts accept standard HTML. Inline styles work best on Blogger:

```html
<div style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.8; max-width: 800px; margin: 0 auto;">

  <h2 style="color: #27ae60;">Section Title</h2>

  <p>Your paragraph content here...</p>

  <ul>
    <li><strong>Point one</strong> — explanation</li>
    <li><strong>Point two</strong> — explanation</li>
  </ul>

  <pre style="background: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 8px;">
    code example here
  </pre>

</div>
```

---

## Configuration

| File | Purpose |
|------|---------|
| `~/.config/gblog/credentials.json` | Google OAuth client credentials |
| `~/.config/gblog/token.json` | Saved access + refresh tokens (auto-generated) |

### Environment Variables

```bash
export GBLOG_DEFAULT_BLOG_ID=your-blog-id   # Skip --blog-id on every command
```

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `gblog.py` | Main CLI — auth, post, edit, delete, list |
| `gblog-bulk-post.py` | Bulk publish from folder of HTML files |
| `gblog-monitor.py` | Monitor blog for new/updated posts |
| `update-blogger-full.py` | Batch update existing posts with new content |

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `invalid_grant` | Token expired — run `gblog.py auth` again |
| `insufficient_permissions` | Ensure Blogger API v3 is enabled in Cloud Console |
| `blog not found` | Double-check your `--blog-id` value |
| `rate limit exceeded` | Wait 60 seconds and retry |
| `Expecting value` on DELETE | Token may need refresh — re-authenticate |

---

## OpenClaw Integration

Once installed as an OpenClaw skill, your assistant can manage your Blogger blog via natural language:

> "Post a new blog about LLMfit with the content from post.html"

> "List all my blog posts and delete any drafts"

> "Monitor my blog and notify me of new posts"

---

## License

MIT — free to use, modify, and distribute.

---

*Built for [OpenClaw](https://openclaw.ai) — The AI that actually does things.*
