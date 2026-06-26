# Troubleshooting & Error Level Guide

## Error Level Summary

| Level | Type | Behavior |
|-------|------|----------|
| 1 | Transient | Auto-retry silently (max 2, delay 3s/10s) |
| 2 | Auto-repairable | Repair + flag in pre-publish confirmation |
| 3 | Requires user action | Halt + exact setup guide |
| 4 | Unrecoverable | Log + show error + link to mp.weixin.qq.com |

---

## Level 1: Auto-retry (no user action)

| Error | Auto-action |
|-------|-------------|
| Access token expired | Refresh token from AppID/AppSecret, update cache, retry |
| Transient network error (timeout, 5xx) | Wait 3s, retry; wait 10s, retry again |
| WeChat API rate limit (temporary) | Wait 10s, retry once |

If all retries fail → escalate to Level 4.

---

## Level 2: Auto-repair + warn in confirmation

| Issue | Auto-repair |
|-------|-------------|
| Summary missing | Auto-generate from first paragraph |
| Title missing | Auto-generate from H1 / content |
| Cover missing (API, before first inline image) | Use first inline image as cover |
| Article over `default_article_length` | Compress repetition; flag compression in confirmation |
| Long-tail keyword block missing | Generate from article topic |
| Profile block missing | Infer from account config or global defaults |

All Level 2 repairs are shown in the pre-publish confirmation summary with `⚠` markers.

---

## Level 3: Halt + user guidance

### Missing API credentials

```
WeChat API credentials not found.

Steps to obtain:
1. Visit https://mp.weixin.qq.com
2. 开发 → 基本配置
3. Copy AppID and AppSecret

Where to save:
  A) Project-level:  amiao/.env
  B) User-level:     ~/amiao/.env

Format:
  WECHAT_APP_ID=<your_app_id>
  WECHAT_APP_SECRET=<your_app_secret>

For multi-account, use alias-prefixed keys:
  WECHAT_<ALIAS>_APP_ID=<id>
  WECHAT_<ALIAS>_APP_SECRET=<secret>
```

### Cover image missing (after full fallback chain)

```
Cover image required for API publish (article_type=news).

Fallback chain exhausted:
  ✗ --cover flag not provided
  ✗ frontmatter: coverImage / featureImage / cover / image not set
  ✗ imgs/cover.png not found
  ✗ No inline images in article

Options:
  1. Add --cover <path/to/image.png>
  2. Place cover at imgs/cover.png
  3. Add an image to the article body
  4. Switch to browser method: --method browser
```

### Article content empty

```
Article content is empty. Nothing to publish.
Please provide content via:
  - A markdown file path
  - An HTML file path
  - Plain text (will be saved as markdown)
```

### Chrome not found

```
Chrome browser not found.

Options:
  1. Install Google Chrome
  2. Set environment variable:
     WECHAT_BROWSER_CHROME_PATH=/path/to/your/chrome
```

### Accessibility permission denied (macOS)

```
macOS Accessibility permission required for browser automation.

Steps:
  System Settings → Privacy & Security → Accessibility
  → Enable your terminal application (Terminal / iTerm2 / etc.)

After enabling, retry the command.
```

### Paste keystroke unavailable (Linux)

```
Linux paste keystroke tool not found.

Install one of:
  sudo apt install xdotool      # X11
  sudo apt install ydotool      # Wayland
```

---

## Level 4: Log + show error

### WeChat API unrecoverable error

```
WeChat API returned error: [errcode] [errmsg]

Common codes:
  40001  Invalid access_token → check AppID/AppSecret
  40003  Invalid media_id → cover image upload may have failed
  45009  Reach max api daily limit → wait until tomorrow
  48001  API unauthorized → check account permissions at mp.weixin.qq.com

Logged to: amiao/.publish-log.yaml

Fallback option: try browser method
  → re-run with --method browser
```

---

## Quick Reference: Common Issues

| Symptom | Level | Solution |
|---------|-------|----------|
| Output looks too AI | 2 | Increase humanize strength; re-run editorial pass |
| Output messy in WeChat | 2 | Simplify structure; remove fragile layouts |
| Wrong comment defaults | — | Check `need_open_comment` / `only_fans_can_comment` in EXTEND.md |
| Paste fails in browser mode | 3 | Check clipboard + accessibility permissions |
| Access token error | 1→3 | Auto-refresh attempted; if persistent, verify AppID/AppSecret |
| Not logged in (browser) | — | First run opens browser automatically; scan QR code |
| Protected term was altered | — | Add to `protected_terms` in EXTEND.md |
| Score consistently low | — | Check auto-tune suggestions after 10th cycle |
