# Telegram File Sender

Send files (zip, pdf, images, video, etc.) to the current Telegram chat via OpenClaw.

The skill automatically routes to whoever is chatting — no hardcoded IDs, no extra config.

## Requirements

- OpenClaw gateway running with a Telegram bot configured
- `openclaw` available in `PATH` (works on Linux/RPi and macOS)

## Trigger phrases

Say any of these to invoke the skill:

- "gửi file cho tao"
- "send this zip to me"
- "attach the pdf"
- "ship file to me"

## How it works

1. Confirms the file exists at the given path
2. Reads `chat_id` from the `Inbound Context` block in the session (injected by OpenClaw — no input needed from the user)
3. Runs `openclaw message send --channel telegram --target <chat_id> --media <file>`

## Usage examples

```
User: gửi file report.pdf cho tao
User: send this zip → /tmp/output.zip
User: attach /home/pi/exports/data.csv
```

Caption is optional — defaults to `File from OpenClaw`.

## Files

```
telegram-file-sender/
├── SKILL.md          # Skill definition
├── scripts/
│   └── send_file.sh  # Shell script (bash, cross-platform)
└── README.md
```

## Compatibility

| Platform | Status |
|----------|--------|
| Raspberry Pi (Linux/bash) | ✅ |
| macOS | ✅ |
| Docker/Linux | ✅ |
