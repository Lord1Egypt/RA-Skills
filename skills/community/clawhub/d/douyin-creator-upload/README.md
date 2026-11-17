# byted-sol-douyin-creator-upload

OpenClaw skill for uploading a local video to Douyin Creator Center through an already logged-in Chrome session.

## What It Does

- Connects to Chrome by CDP.
- Reuses the user's logged-in `creator.douyin.com` session.
- Uploads a local video file.
- Fills the work description.
- Sets visibility to public, friends, or private.
- Optionally clicks publish.
- Stops and asks for manual handling if SMS verification appears.

## Requirements

- Node.js 18 or newer.
- Chrome or Chromium started with a remote debugging port.
- `playwright-core` available to Node. In OpenClaw environments this is commonly available through:

```bash
NODE_PATH=/usr/lib/node_modules/openclaw/node_modules
```

## Quick Start

Start Chrome with CDP enabled:

```bash
open -na "Google Chrome" --args --remote-debugging-port=9222
```

Open `creator.douyin.com` in that Chrome instance and log in. Then run:

```bash
NODE_PATH=/usr/lib/node_modules/openclaw/node_modules \
node scripts/upload_to_creator.js \
  --file "/absolute/path/video.mp4" \
  --title "作品描述" \
  --visibility self \
  --publish true
```

## Arguments

| Argument | Required | Default | Description |
| --- | --- | --- | --- |
| `--file` | Yes | None | Absolute path to the local video file. |
| `--visibility` | No | `self` | `public`, `friend`, or `self`. |
| `--title` | No | Empty | Work description text. |
| `--cdp` | No | `http://127.0.0.1:9222` | Chrome DevTools Protocol endpoint. |
| `--publish` | No | `true` | Use `false` to upload and fill fields without publishing. |

## Safety Notes

This skill operates an authenticated browser session. Review the code before publishing or installing from a community registry, and use an account/session with only the access needed for the task.

