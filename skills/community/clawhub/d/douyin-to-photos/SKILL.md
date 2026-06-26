---
name: douyin-to-photos
description: Build and maintain an Apple Shortcuts workflow that takes a Douyin share link, resolves a no-watermark MP4 URL via configurable backend APIs, saves the video into the Photos app, and cleans temporary cache. Use when users ask for one-tap Douyin link-to-Photos automation on iPhone/macOS, Share Sheet/Back Tap integration, publish-ready skill packaging, parameterization, error handling, and privacy-safe behavior.
---

# Douyin-to-Photos

Use this skill to implement a one-tap Apple Shortcuts flow for authorized Douyin video archiving into Photos.

## Hard Rules

- Process only links the user is allowed to download and store.
- Request only required permissions: network + Photos add-only.
- Keep all temporary files in Shortcuts temp folder and delete after import.
- Never persist user links, tokens, or media metadata outside local shortcut runtime.

## Workflow

1. Accept input from Share Sheet (`URL` or text) or clipboard fallback.
2. Normalize and validate Douyin URL (`douyin.com` or `iesdouyin.com`).
3. Resolve playable MP4 via API provider chain:
- Primary: `https://www.tikwm.com/api/`
- Fallback: user-defined gateway API (for example self-hosted parser)
4. Download MP4 to temporary file.
5. Save to Photos (optionally target user-selected album).
6. Delete temporary file and report success/failure.

## Included Resources

- `scripts/fetch_douyin_no_watermark.sh`: provider-chain URL resolver with timeout and structured errors.
- `references/shortcut-build-guide.md`: action-by-action Shortcuts build instructions.
- `assets/skill-manifest.json`: market-ready manifest template with parameterized options.

## Integration Notes

- Share Sheet: enable `URLs` input type.
- Back Tap: configure a tiny launcher shortcut that reads clipboard and calls the main shortcut.
- Keep API base URL and album name configurable via shortcut dictionary values.

## Validation

- Run URL resolver script with a test share link before wiring into Shortcuts.
- Test four scenarios: success, invalid link, API timeout, API quota/blocked.
- Confirm temporary media file is deleted in both success and failure paths.
