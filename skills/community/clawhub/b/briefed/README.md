# briefed

An AI newsletter intelligence skill for [OpenClaw](https://openclaw.ai).

Fetches your Gmail newsletters daily, uses Claude Haiku to summarise them, and serves a polished local web reader with voting, notes, and interest tracking.

![Briefed reader app](assets/reader/public/icon.svg)

## What it does

- Pulls newsletters from Gmail (filters out transactional email automatically)
- Summarises each one with Claude Haiku — real headlines and bullets, not just subject lines
- Serves a local web app at `127.0.0.1:3001` to read, vote, save, and annotate stories
- Sends a daily notification ping when your digest is ready
- Learns your interests over time from what you open and upvote

## Installation

```bash
openclaw skills install @jamesnation/briefed
```

Or download the `.skill` file from [Releases](../../releases) and install it in OpenClaw. Then ask your agent to set up Briefed — it follows `SKILL.md`.

## Requirements

- [OpenClaw](https://openclaw.ai)
- Python 3.10+ and Node.js ≥ 18
- A Google Cloud OAuth Desktop client (for read-only Gmail access)
- `claude-haiku-4-5` on your OpenClaw models allowlist
- A notification channel (Telegram, Discord, etc.)

## Privacy & data

Briefed handles your email, so here is exactly what it does with it:

- **Gmail access is read-only** (`gmail.readonly`). It can't send, delete, or change mail. The OAuth token is stored at `~/.openclaw/workspace/briefed-gmail-token.json` with owner-only permissions.
- **Sent to your model provider:** subjects, sender names and short snippets of the last day's newsletters, so Haiku can summarise them. Nothing else leaves your machine, apart from the notification you configure.
- **Stored locally, unencrypted:** email metadata, full newsletter HTML, your notes, votes, and reading list, all in `~/.openclaw/workspace/` with owner-only (`0600`) permissions.
- **Interest signals:** opening a story records a local "open" signal, and votes and saves are recorded too. They are used only to rank future digests and stay in `newsletter-interests.json`.
- **Reader exposure:** the reader listens on `127.0.0.1` only. Remote access is opt-in and requires a token. The recommended setup is HTTPS via Tailscale Serve; plain-HTTP LAN access needs an explicit opt-in because the token would travel unencrypted (see `SKILL.md` → *Reading on another device*).
- **Tracking pixels:** remote images in emails are blocked by default, so senders can't see when you read. Use **Load images** per email, or **Always** to opt out.

## Setup overview

1. Deploy the reader app and install dependencies
2. Authorise Gmail (read-only) via a one-time browser OAuth flow
3. Configure your interest topics
4. Start the reader
5. Create a daily 7am cron job in OpenClaw

Full instructions in `SKILL.md`.

## Auto-start on macOS (optional)

Only needed if you want the reader running permanently. Otherwise run `node ~/.openclaw/workspace/briefed/server.js` when you want it.

Create `~/Library/LaunchAgents/ai.openclaw.briefed.plist`, replacing `YOUR_USER` and the node path (`which node`):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>ai.openclaw.briefed</string>
  <key>ProgramArguments</key><array>
    <string>/usr/local/bin/node</string>
    <string>/Users/YOUR_USER/.openclaw/workspace/briefed/server.js</string>
  </array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><dict><key>SuccessfulExit</key><false/></dict>
  <key>WorkingDirectory</key><string>/Users/YOUR_USER/.openclaw/workspace/briefed</string>
  <key>StandardOutPath</key><string>/Users/YOUR_USER/Library/Logs/briefed.log</string>
  <key>StandardErrorPath</key><string>/Users/YOUR_USER/Library/Logs/briefed.log</string>
</dict></plist>
```

The reader doesn't need Gmail credentials, so none are passed to it. For remote access, add `BRIEFED_TOKEN` and `BRIEFED_ALLOWED_HOSTS` (see `SKILL.md` → *Reading on another device*) under an `EnvironmentVariables` dict.

```bash
launchctl load ~/Library/LaunchAgents/ai.openclaw.briefed.plist
```

## Uninstall

1. **Remove the daily job:** delete the Briefed cron job with the OpenClaw cron tool (or ask your agent to).
2. **Stop auto-start** (if you set it up):
   ```bash
   launchctl unload ~/Library/LaunchAgents/ai.openclaw.briefed.plist
   rm ~/Library/LaunchAgents/ai.openclaw.briefed.plist
   ```
3. **Delete local data:**
   ```bash
   rm -rf ~/.openclaw/workspace/briefed
   rm -f ~/.openclaw/workspace/{briefed-gmail-token.json,newsletter-inbox.json,newsletter-today.json,newsletter-interests.json,newsletter-notes.json,newsletter-filter-rules.json,newsletter-filter-skips.jsonl,reading-list.md}
   ```
4. **Revoke Google access:** remove your Briefed OAuth app at <https://myaccount.google.com/permissions>.

## License

MIT
