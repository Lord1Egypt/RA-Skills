---
name: chatgpt-image-gen
description: Generate images using ChatGPT/DALL-E through OpenClaw browser automation. Use when the user wants to create images via ChatGPT's web interface with their logged-in session. Requires Chrome extension setup for first use. Use for image generation tasks where ChatGPT's native DALL-E image creation is preferred.
---

# ChatGPT Image Generation

Generate images using ChatGPT's DALL-E integration through OpenClaw browser automation.

## Prerequisites

1. **Chrome Extension Installation:**
   - Install OpenClaw Browser Relay from Chrome Web Store
   - Or use the extension that comes with OpenClaw

2. **Initial Setup (one-time):**
   - Open ChatGPT (chatgpt.com) in Chrome/Brave
   - Login to your ChatGPT account (Pro subscription recommended for best quality)
   - Click the OpenClaw extension icon on the ChatGPT tab to attach it
   - The badge should show "ON" when attached

## How It Works

This skill uses OpenClaw's built-in `browser` tool with Chrome extension relay (`profile="chrome"`) to control an already-logged-in ChatGPT tab. This bypasses ChatGPT's bot detection because it uses your real browser session.

## CLI Command Reference

**IMPORTANT:** There is NO `browser act` subcommand. Each action is a direct subcommand.

| Action | CLI Syntax |
|--------|-----------|
| List tabs | `openclaw browser tabs` |
| Snapshot | `openclaw browser snapshot --target-id <ID>` |
| Click | `openclaw browser click <ref> --target-id <ID>` |
| Type | `openclaw browser type <ref> "<text>" --target-id <ID>` |
| Press key | `openclaw browser press <key> --target-id <ID>` |
| Navigate | `openclaw browser navigate <url> --target-id <ID>` |
| Screenshot | `openclaw browser screenshot --target-id <ID>` |

- `<ref>` and `<text>` are **positional arguments** (no `--ref` flag)
- `--target-id` accepts a full ID or unique prefix (e.g. `77CB` instead of `77CB8A574E8A44861C5FE49388EF6ABC`)
- `--profile` is a parent option on `openclaw browser`, not on subcommands

## Workflow

### 1. List Attached Tabs

```bash
openclaw browser tabs
```

Look for a tab with URL containing `chatgpt.com`. Note the `targetId`.

### 2. Get Snapshot (find element refs)

```bash
openclaw browser snapshot --target-id <ID> --format ai --efficient
```

This outputs a tree with refs like `e23`, `e589`, etc. Always run snapshot before interacting.

### 3. Click an Element

```bash
openclaw browser click e23 --target-id <ID>
```

### 4. Type Text

```bash
openclaw browser type e589 "Generate an image: a futuristic city at sunset" --target-id <ID>
```

Add `--submit` to press Enter after typing:
```bash
openclaw browser type e589 "Generate an image: a cat riding a skateboard" --target-id <ID> --submit
```

### 5. Press a Key

```bash
openclaw browser press Enter --target-id <ID>
```

### 6. Wait for Generation

Use `sleep` to wait for DALL-E to generate (30-60 seconds):
```bash
sleep 45
```

Then take a new snapshot to check the result:
```bash
openclaw browser snapshot --target-id <ID> --format ai --efficient
```

## Complete Example Session

```bash
# 1. List tabs, find the ChatGPT tab targetId
openclaw browser tabs

# 2. Take snapshot to find element refs
openclaw browser snapshot --target-id 4535E --format ai --efficient

# 3. Click input field (check ref from snapshot, usually labeled "Ask anything")
openclaw browser click e589 --target-id 4535E

# 4. Type prompt and submit
openclaw browser type e589 "Generate an image: a futuristic city at sunset" --target-id 4535E --submit

# 5. Wait for DALL-E generation
sleep 45

# 6. Take new snapshot to see result and find download button
openclaw browser snapshot --target-id 4535E --format ai --efficient

# 7. Click download button (ref from new snapshot)
openclaw browser click e745 --target-id 4535E
```

## Troubleshooting

**"Can't reach the OpenClaw browser control service":**
- Gateway restart needed: `openclaw gateway restart`
- Or restart via OpenClaw menu bar app

**"Chrome extension relay is running, but no tab is connected":**
- ChatGPT tab is not attached
- Go to the ChatGPT tab and click the OpenClaw extension icon

**"ref is required" error:**
- You need to specify which element to interact with
- Run `snapshot` first to get the refs

**Command not found / Unknown command:**
- Do NOT use `browser act` — use direct subcommands: `browser click`, `browser type`, `browser press`
- ref is a positional argument: `browser click e23`, NOT `browser click --ref e23`

**Image generation timeout:**
- DALL-E generation takes 30-60 seconds
- Use `sleep 45` then re-snapshot to check

**Bot detection / Login issues:**
- The tab must be already logged in via your real browser
- Use the Chrome extension relay (attached tab), not the isolated browser

## Tips

1. **Keep ChatGPT tab open:** Once attached, keep the tab open for future use
2. **Check targetId:** The targetId changes if you close/reopen the tab — always run `tabs` first
3. **Use `--submit`:** The `type` command supports `--submit` to press Enter automatically
4. **Unique prefix:** `--target-id` accepts a unique prefix, no need for the full 32-char ID
5. **Pro subscription:** ChatGPT Pro gives better image quality and faster generation

## Security Note

This approach uses your actual Chrome browser session, so it inherits all your ChatGPT permissions and settings. No credentials are stored or transmitted - everything happens in your existing browser session.
