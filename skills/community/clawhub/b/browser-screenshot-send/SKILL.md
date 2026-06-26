---
name: browser-screenshot-send
description: Automatically send browser screenshots to users via message tool. Solves the common issue where browser screenshots are generated but not delivered to the conversation channel. Essential for web automation workflows requiring visual feedback.
---

# Browser Screenshot Send

Automatically deliver browser screenshots to users through messaging channels. This skill bridges the gap between browser automation and user communication.

## Problem It Solves

When using `browser action=screenshot`, the screenshot is saved to disk but **not automatically sent** to the user. Many agents mistakenly use `read` to display screenshots, which doesn't reliably transmit images through chat channels.

This skill ensures screenshots actually reach the user.

## When to Use

- After any `browser screenshot` operation where the user needs to see the result
- Web scraping results visualization
- UI automation progress reporting
- Page verification and debugging
- Visual testing workflows

## Quick Start

```
# 1. Take screenshot
browser action=screenshot targetId=<page>
# Returns: MEDIA:/root/.openclaw/media/browser/<uuid>.png

# 2. Send to user
message action=send media=/root/.openclaw/media/browser/<uuid>.png
```

## Why Not `read`?

❌ **Don't**: `read file_path=/path/to/screenshot.png`
- Displays in agent context only
- Not transmitted to chat channels
- User sees nothing

✅ **Do**: `message action=send media=/path/to/screenshot.png`
- Actively pushes to conversation
- Works across all channels (Slack, Discord, Telegram, etc.)
- User receives the image

## Handling Long Screenshots

For full-page screenshots that may be too long:

**Option 1**: Send as-is with warning
```
message action=send media=<path>
Note: This is a full-page screenshot and may be quite long.
```

**Option 2**: Split into sections
Use `canvas` tool to crop sections when user requests "send in parts".

**Option 3**: Partial screenshots
```
browser action=screenshot fullPage=false
# Scroll and repeat for different sections
```

## File Organization

Screenshots are auto-saved to:
- Source: `/root/.openclaw/media/browser/<uuid>.png`
- Recommended: Copy to workspace for persistence:
  ```
  cp <source> /workspace/media/screenshots/<descriptive_name>.png
  ```

## Example Workflow

```
# Navigate and screenshot
browser action=navigate targetUrl=https://example.com
browser action=screenshot fullPage=true

# Returns path in MEDIA: line
MEDIA:/root/.openclaw/media/browser/abc123.png

# Send to user
message action=send media=/root/.openclaw/media/browser/abc123.png
```

## Best Practices

1. **Always use `message` tool** - Never rely on `read` for user-facing images
2. **Copy to workspace** - Browser media is temporary; save important screenshots
3. **Name descriptively** - When copying, use meaningful filenames
4. **Warn for long screenshots** - Full-page captures can be very tall

## Requirements

- OpenClaw with `browser` and `message` tools enabled
- Compatible with all OpenClaw-supported channels
