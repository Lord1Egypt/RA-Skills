---
name: fb-personal-poster
description: >
  Post text and photos to personal Facebook timeline using browser automation (Patchright/Playwright).
  Use when: user asks to post to personal Facebook, publish to FB personal profile, upload photos
  to FB timeline, or share content on their personal Facebook wall. NOT for Facebook Pages (use
  fb-page-poster or Graph API instead). CREDENTIALS REQUIRED: FB_COOKIE_FILE (Facebook session
  cookies JSON — treat as password), FB_STATE_FILE (Playwright state path, writable).
---

# FB Personal Poster

Post text + photos to personal Facebook timeline via Patchright stealth browser automation.

## Why Not Graph API?

Facebook removed `publish_actions` permission in 2018. API cannot post to personal timelines.
Only browser automation works — this skill uses Patchright (stealth Chromium) to mimic human behavior.

## Requirements

```bash
cd scripts/ && pip install -r requirements.txt
python -m patchright install chromium
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `FB_COOKIE_FILE` | ✅ | Path to Facebook cookies JSON (Selenium format). Full account access. |
| `FB_STATE_FILE` | ✅ | Writable path for Playwright state (default: `/tmp/fb_state.json`) |
| `FB_DRY_RUN` | — | `true` (default) = preview only. `false` = actually post. |
| `FB_USER_AGENT` | — | Override browser user agent |

## How to Get Cookies

1. Log in to Facebook in Chrome (manually, once)
2. Export all `facebook.com` cookies as JSON via EditThisCookie extension
3. Save to path in `FB_COOKIE_FILE` with `chmod 600`

Cookies last ~30–90 days. Re-export when expired.

## Usage

### Text-only post
```bash
FB_COOKIE_FILE=~/.fb_cookies.json FB_DRY_RUN=false \
  python3 scripts/fb_post.py -m "Hello from automation!"
```

### Post with photos
```bash
FB_COOKIE_FILE=~/.fb_cookies.json FB_DRY_RUN=false \
  python3 scripts/fb_post.py -m "Beautiful day!" -p photo1.jpg photo2.jpg
```

### Dry run (default)
```bash
python3 scripts/fb_post.py -m "Test post" -p photo.jpg
# No actual posting — previews the flow
```

## OpenClaw Integration (Recommended)

Use the built-in `browser` tool — already proven working for personal timeline posting:

```python
# Step 1: Navigate to Facebook
browser(action="navigate", url="https://www.facebook.com/")

# Step 2: Confirm on personal profile (url should be facebook.com/me)
# Step 3: Click "What's on your mind"
browser(action="act", kind="click", ref="[post input box]")

# Step 4: Type message
browser(action="act", kind="type", text="Your message here")

# Step 5: Upload photo (if needed)
browser(action="upload", paths=["/path/to/photo.jpg"])

# Step 6: Set sharing to Public
# Step 7: Click Post button
browser(action="act", kind="click", ref="[post button]")
```

### Tips
- Facebook 頁面結構複雜，selector 會變，用 `snapshot` 找當前可用的 ref
- 上傳圖片用 `browser(action="upload")` 功能
- 如果 timeout，重試一次通常就好
- 個人動態和粉絲專頁的操作流程不同，注意確認在正確頁面

## Safety

- Dry-run is ON by default — must explicitly set `FB_DRY_RUN=false` for live posting
- Cookies stored locally with `chmod 600` — never committed to git
- Human-like delays and typing speed to avoid detection
