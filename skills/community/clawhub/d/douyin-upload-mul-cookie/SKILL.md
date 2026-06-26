---
name: 抖音自动发布
description: |
  自动化发布抖音视频。上传到抖音平台。全自动操作。
---
# auto-douyin skill

This skill publishes videos to Douyin on the user's machine with Playwright.

## Default workflow

Use this order:

1. Make sure the target Douyin cookie profile exists and is valid.
2. Use the guarded publish entry so the platform can deduct points first.
3. Let the local script finish on the user's machine.

## Commands

Capture the default cookie:

```bash
python skills/auto-douyin/scripts/get_cookie.py
```

Capture a named cookie profile:

```bash
python skills/auto-douyin/scripts/get_cookie.py --cookie-name account_a
```

Validate a cookie profile:

```bash
python skills/auto-douyin/scripts/check_cookie.py --cookie-name account_a
```

Publish through the controlled path with a specific cookie profile:

```bash
python skills/auto-douyin/scripts/publish_guarded.py \
  --video "D:\\videos\\demo.mp4" \
  --title "Douyin title" \
  --tags "tag1,tag2" \
  --cover "D:\\videos\\cover.png" \
  --cookie-name account_a
```

Optional scheduled publish:

```bash
python skills/auto-douyin/scripts/publish_guarded.py \
  --video "D:\\videos\\demo.mp4" \
  --title "Douyin title" \
  --schedule "2026-03-20 18:30" \
  --cookie-name account_a
```

## Cookie storage

- Default cookie file: `cookies/douyin.json`
- Named cookie file: `cookies/douyin-<cookie-name>.json`
- `--cookie-name` is optional. If omitted, the scripts stay backward compatible and use the default file.

## Required environment variables

- `CHANJING_PLATFORM_BASE_URL` (optional, defaults to `http://easyclaw.bar/shuzirenapi`)
- `CHANJING_PLATFORM_API_TOKEN`

or:

- `CHANJING_PLATFORM_API_KEY`
- `CHANJING_PLATFORM_API_SECRET`

If the key is missing or invalid, direct the user to `http://easyclaw.bar/shuziren/user` to generate a valid platform key.

## Notes

- `publish_guarded.py` is the normal entry point.
- `publish.py` also performs platform authorization when called directly, so points are still deducted.
- The guarded path controls normal usage and deducts points before publish starts.
