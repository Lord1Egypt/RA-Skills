---
name: capture-windows-screen
description: Capture the current Windows desktop from this WSL/OpenClaw environment and return the PNG path for inspection or delivery. Use when the user asks to screenshot the current screen, show what is on the Windows desktop, inspect a visible app/window, or send the latest screen image back to them.
---

# Capture Windows Screen

Use the bundled script for screenshot requests in this environment. It calls the Windows PowerShell helper, copies the PNG into a chosen staging folder, and prints the staged path.

Use two staging modes:

- **Analysis / inspection**: keep the default workspace `tmp-media/` staging.
- **Messaging-surface delivery**: prefer `~/.openclaw/media/outbound/` so the file is already in OpenClaw's managed outbound media store.

## Quick workflow

1. For analysis or inspection, run `bash scripts/capture-windows-screen.sh` from this skill directory.
2. For delivery back to a chat app, run `STAGE_DIR=/home/lhs/.openclaw/media/outbound bash scripts/capture-windows-screen.sh`.
3. Treat the printed path as the staged screenshot to use next.
4. If the user wants the image in chat, prefer the managed outbound path from step 2 and send it with a bare `MEDIA:` line when possible.
5. If the user wants analysis, inspect the staged image after capture.

## Commands

Analysis / inspection path:

```bash
bash scripts/capture-windows-screen.sh
```

Delivery-safe path for chat apps:

```bash
STAGE_DIR=/home/lhs/.openclaw/media/outbound bash scripts/capture-windows-screen.sh
```

Expected output:

```text
/home/lhs/.openclaw/workspace/tmp-media/latest-screen-YYYYMMDD-HHMMSS.png
```

or, for delivery-safe staging:

```text
/home/lhs/.openclaw/media/outbound/latest-screen-YYYYMMDD-HHMMSS.png
```

## Environment assumptions

This skill assumes these host-side paths exist:

- PowerShell: `/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe`
- Capture helper: `C:\OpenClaw\capture-screen.ps1`
- Screenshot output: `C:\OpenClaw\latest-screen.png`
- WSL mirror path: `/mnt/c/OpenClaw/latest-screen.png`
- Workspace staging directory for inspection copies: `/home/lhs/.openclaw/workspace/tmp-media`
- Managed outbound media store for delivery retries / chat attachments: `/home/lhs/.openclaw/media/outbound`

## Failure handling

- If PowerShell or the helper script is missing, check local machine-specific notes before changing paths.
- If the command succeeds but the PNG is missing, rerun once, then verify the helper still writes to `C:\OpenClaw\latest-screen.png`.
- If the browser shows the image but Telegram or another chat app does not receive it, assume the file stayed at local-preview level. Restage it into `/home/lhs/.openclaw/media/outbound` and retry using only the managed outbound path.
- Do not assume a workspace `tmp-media/` path is delivery-safe just because the web UI can preview it.
- Do not invent alternate screenshot commands unless the configured path is clearly broken.
