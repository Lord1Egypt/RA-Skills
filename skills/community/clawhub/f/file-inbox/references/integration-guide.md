# Channel Integration Guide

## How Files Arrive

OpenClaw receives files from messaging channels as attachments. The agent can access them as local file paths during the session.

### Telegram
- Documents: delivered as file path, original filename preserved
- Photos: delivered as image path, may have generic name (photo.jpg)
- Voice/video: delivered as media path

### Discord
- Attachments: delivered as file path with original filename
- Embeds: not file-deliverable — ignore

### Slack
- Files: delivered as file path with original filename

## Registration Flow

When a file arrives on any channel:

1. The file is available at a temporary or workspace path
2. Run `register_file.py --path <path> --direction in --sender "<user>" --tags "<tags>" --notes "<context>"`
3. The script moves it into `inbox/inbound/YYYY-MM/` with an ID prefix
4. Confirm to user: "Saved as F-NNN"

When the agent creates a file to send:

1. Generate the file (save to workspace or temp)
2. Run `register_file.py --path <path> --direction out --dest "<user>" --copy --tags "<tags>" --notes "<context>"`
3. Use `--copy` so the original stays available for sending
4. Send the file to the user via the channel
5. Confirm: "Sent and archived as F-NNN"

## AGENTS.md Addition (optional)

Add to your workspace AGENTS.md to remind the agent:

```markdown
## File Management
- When receiving files: register with `file-inbox` skill before processing
- When sending files: register with `file-inbox` skill after creating
- Use `inbox/INDEX.md` for file lookups before filesystem scans
```

## Sender Name Resolution

Extract sender from channel metadata:
- Telegram: `sender` field in conversation info
- Discord: `author` field
- Slack: `user` field

Use the display name (not ID) for readability in INDEX.md.
