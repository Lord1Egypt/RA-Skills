---
name: record
description: Record a browser session as a video/animation for demos, tutorials, or documentation. 录制操作、录屏、制作演示视频、录制教程、操作录像、浏览器录制。
disable-model-invocation: true
allowed-tools: Bash, Read, Write
argument-hint: <url> <action-description>
---

# Record

Record browser interactions as video for demos, tutorials, or documentation.

## Usage

```
/record https://example.com Navigate the site and click the About link
```

## Instructions

1. **Parse arguments**: first arg = URL, remaining = action description
2. **Navigate** to the URL
3. **Execute the actions** described, at a steady pace for clarity
4. **Capture screenshots** at key moments as static fallbacks
5. **Report** the recording/screenshot paths

## Tips

- Pace actions with pauses between steps for clear recordings
- Resize the browser before recording for optimal framing
- Capture a screenshot at each key state as a fallback

## Platform Notes

- **Antigravity**: `browser_subagent` auto-records all interactions as WebP video via `RecordingName`
- **Playwright CLI**: Use `browser.py screenshot` at each step to create a screenshot sequence

Refer to [browser-context](../browser-context/SKILL.md) for available tools per backend.
