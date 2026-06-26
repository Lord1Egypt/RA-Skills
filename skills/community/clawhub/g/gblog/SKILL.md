---
name: gblog
description: |
  Blogger API CLI for managing blog posts. Post, edit, delete, list, and monitor Blogger blogs.
  Use when the user wants to: (1) publish blog posts to Blogger, (2) edit existing blog posts,
  (3) list or search blog posts, (4) delete blog posts, (5) schedule posts, (6) monitor blog activity.
  Requires Google OAuth credentials in ~/.config/gblog/credentials.json
---

# gblog - Blogger CLI

Manage Blogger blogs via command line. Supports posting, editing, listing, and monitoring.

## Quick Start

```bash
# Authenticate with Google
gblog auth

# List your blogs
gblog list-blogs

# List posts from a blog
gblog list-posts --blog-id YOUR_BLOG_ID

# Create a new post
gblog post --blog-id YOUR_BLOG_ID --title "My Post" --content ./post.html

# Edit a post
gblog edit --blog-id YOUR_BLOG_ID --post-id POST_ID --content ./updated.html

# Delete a post
gblog delete --blog-id YOUR_BLOG_ID --post-id POST_ID
```

## Setup

### 1. Google Cloud Console Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project or select existing
3. Enable **Blogger API v3**
4. Go to **APIs & Services → Credentials**
5. Create **OAuth 2.0 Client ID** (Desktop application type)
6. Add redirect URIs:
   - `http://localhost:8085/oauth2callback`
   - `http://localhost:8080/oauth2callback`
7. Download credentials JSON

### 2. Local Setup

```bash
# Create config directory
mkdir -p ~/.config/gblog

# Save credentials
cp ~/Downloads/client_secret_*.json ~/.config/gblog/credentials.json

# Run authentication
gblog auth
```

### 3. Authentication

The first time you run `gblog auth`, it will:
1. Open a browser for Google OAuth
2. Request permissions for Blogger
3. Save refresh token to `~/.config/gblog/token.json`

## Commands

### Authentication
```bash
gblog auth                    # Authenticate with Google
gblog auth --status          # Check auth status
gblog auth --logout          # Clear saved tokens
```

### Blog Management
```bash
gblog list-blogs             # List all your blogs
gblog get-blog --id BLOG_ID  # Get blog details
```

### Post Management
```bash
# List posts
gblog list-posts --blog-id BLOG_ID

# Create post
gblog post \
  --blog-id BLOG_ID \
  --title "Post Title" \
  --content ./content.html \
  --labels "AI, Tutorial" \
  --draft

# Edit post
gblog edit \
  --blog-id BLOG_ID \
  --post-id POST_ID \
  --title "Updated Title" \
  --content ./updated.html

# Delete post
gblog delete --blog-id BLOG_ID --post-id POST_ID

# Get post
gblog get-post --blog-id BLOG_ID --post-id POST_ID
```

### Monitoring
```bash
# Monitor new posts (poll every 5 minutes)
gblog monitor --blog-id BLOG_ID --interval 300

# Get post statistics
gblog stats --blog-id BLOG_ID
```

## HTML Content Format

Posts support full HTML. Example structure:

```html
<div style="font-family: Arial, sans-serif; line-height: 1.8;">
  <h1 style="color: #27ae60;">Post Title</h1>
  
  <p>Your content here...</p>
  
  <div style="background: #f5f5f5; padding: 20px; border-radius: 8px;">
    <h3>Call to Action</h3>
    <a href="...">Subscribe</a>
  </div>
</div>
```

## Configuration Files

| File | Purpose |
|------|---------|
| `~/.config/gblog/credentials.json` | OAuth client credentials |
| `~/.config/gblog/token.json` | Saved access/refresh tokens |
| `~/.config/gblog/config.json` | User preferences |

## Environment Variables

```bash
export GBLOG_CREDENTIALS_PATH=/path/to/credentials.json
export GBLOG_TOKEN_PATH=/path/to/token.json
export GBLOG_DEFAULT_BLOG_ID=your-blog-id
```

## Error Handling

Common errors and solutions:

| Error | Solution |
|-------|----------|
| `invalid_grant` | Run `gblog auth` again |
| `insufficient_permissions` | Check Blogger API is enabled |
| `blog not found` | Verify blog ID is correct |
| `rate limit exceeded` | Wait 60 seconds and retry |

## API Reference

Uses Blogger API v3:
- Base URL: `https://www.googleapis.com/blogger/v3`
- Documentation: https://developers.google.com/blogger/docs/3.0/reference

## Scripts

- `scripts/gblog.py` - Main CLI script
- `scripts/auth.py` - OAuth authentication
- `scripts/blogger_api.py` - API wrapper

---
*Powered by Google Blogger API v3*
