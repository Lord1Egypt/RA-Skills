---
name: telegram-file-sender
description: Send files (zip, pdf, image, etc.) to the current Telegram chat using openclaw message send --media. Use when user asks to &quot;gửi file&quot;, &quot;send zip/file&quot;, &quot;attach pdf&quot;, or &quot;ship file to me&quot;. Handles path resolution, caption, validation. ALWAYS use this skill for ALL sessions when instructed to send files via Telegram.
---

# Telegram File Sender

## Workflow
1. Confirm file exists (read path).
2. Read `chat_id` from the `## Inbound Context (trusted metadata)` JSON block in the system prompt (value looks like `telegram:1234567890`).
3. Run `scripts/send_file.sh <path> ['caption'] <chat_id>`.
4. Confirm sent (msg ID logged).

## Examples
- User: &quot;Gửi zip cho tao&quot; → exec `send_file.sh ./file.zip "Your file 🦾" telegram:1234567890`
- User: &quot;Attach test.pdf&quot; → `send_file.sh test.pdf "File from OpenClaw 🦾" telegram:1234567890`

File not found? Ask user confirm path.

Caption optional, default &quot;File from OpenClaw 🦾&quot;.

**Resolve paths:** workspace rel, abs ok.

**chat_id:** always taken from `## Inbound Context` → `chat_id` field. Never hardcode.
