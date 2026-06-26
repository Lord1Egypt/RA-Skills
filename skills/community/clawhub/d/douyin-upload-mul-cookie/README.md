# auto-douyin

Local Playwright automation for publishing videos to Douyin Creator Center.

## What changed

Normal publishing should now go through `scripts/publish_guarded.py`.

That script will:

1. Call the platform API to authorize the publish request.
2. Deduct the configured points from the current user.
3. Run the local browser automation on the user's machine.
4. Report success or failure back to the platform.

This is the preferred publish path.

## Requirements

- Python 3.10+
- Playwright and browser dependencies installed locally
- Valid Douyin login cookies
- Platform environment variables configured:
- `CHANJING_PLATFORM_BASE_URL` (optional, defaults to `http://easyclaw.bar/shuzirenapi`)
- `CHANJING_PLATFORM_API_TOKEN`
- or both `CHANJING_PLATFORM_API_KEY` and `CHANJING_PLATFORM_API_SECRET`

If the key is missing or invalid, the skill will prompt the user to visit `http://easyclaw.bar/shuziren/user` to obtain a valid platform key.

## Cookie flow

Get cookies:

```bash
python scripts/get_cookie.py
```

Check whether cookies are still valid:

```bash
python scripts/check_cookie.py
```

## Publish video

Recommended entry:

```bash
python scripts/publish_guarded.py \
  --video "D:\\videos\\demo.mp4" \
  --title "Product launch" \
  --tags "brand,new" \
  --cover "D:\\videos\\cover.png"
```

Optional scheduled publish:

```bash
python scripts/publish_guarded.py \
  --video "D:\\videos\\demo.mp4" \
  --title "Scheduled post" \
  --schedule "2026-03-20 18:30"
```

## Raw script behavior

`scripts/publish.py` now also performs platform authorization and result reporting itself.

That means direct execution still goes through the points flow. `scripts/publish_guarded.py` remains the preferred compatibility entry.
