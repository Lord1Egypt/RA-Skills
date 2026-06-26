# Facebook Graph API Skill (Advanced)

## Purpose
Production-oriented guide for building Facebook Graph API workflows for Pages:
publishing posts (text + image), managing tokens, and operating Page content
safely using direct HTTPS calls.

## Best fit
- Page posting automation with images (DALL-E generated or external URL)
- Token management (short-lived → long-lived → page token)
- Retry-safe, rate-limit-aware production pipelines

## Not a fit
- Personal profile posting (not supported by Graph API for third-party apps)
- Ads / Marketing API workflows
- Browser-based OAuth flows

## Quick orientation
```
agents/fb_token_helper.py     ← Get & exchange tokens (run this first!)
agents/fb_publisher_agent.py  ← Post text / images to Page
config.py                     ← All env vars
test_fb_connection.py         ← Verify token is working
```

## Token Flow
```
Short-lived User Token (1-2h)
        ↓  GET /oauth/access_token?grant_type=fb_exchange_token
Long-lived User Token (60 days)
        ↓  GET /me/accounts
Page Access Token (never expires*)
```
*Until user changes password or revokes app.

## Required Environment Variables
```env
FB_APP_ID=...           # From Meta for Developers
FB_APP_SECRET=...       # App secret
FB_PAGE_ID=...          # Target Fanpage ID
FB_PAGE_ACCESS_TOKEN=... # From fb_token_helper.py
```

## Key API Endpoints

### Post text
```
POST /v21.0/{page_id}/feed
  message=...
  access_token={page_token}
```

### Upload photo (unpublished)
```
POST /v21.0/{page_id}/photos
  url={image_url}
  published=false
  access_token={page_token}
→ Returns: { "id": "PHOTO_ID" }
```

### Post with photo
```
POST /v21.0/{page_id}/feed
  message=...
  attached_media[0]={"media_fbid":"PHOTO_ID"}
  access_token={page_token}
```

### Scheduled post
```
POST /v21.0/{page_id}/feed
  message=...
  scheduled_publish_time={unix_timestamp}
  published=false
  access_token={page_token}
```

## Required Permissions
| Permission | Purpose |
|-----------|---------|
| `pages_manage_posts` | Create/edit posts |
| `pages_read_engagement` | Read reactions, comments |
| `pages_show_list` | List managed pages |
| `public_profile` | Basic user identity |

## Rate Limits
- 200 calls/hour/user token
- Implement retry with exponential backoff (see fb_publisher_agent.py)
- POST 4-5 times/day max per Page for safety

## Security
- Never log tokens or app secrets
- Store all secrets in .env (ignored by git)
- Validate webhook signatures if using webhooks
- Monitor token validity daily with a cron job
