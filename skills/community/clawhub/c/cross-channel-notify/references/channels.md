# Channel Configuration

## Email (Himalaya)

Himalaya requires a config file at `~/.config/himalaya/config.toml` with IMAP/SMTP credentials.

Quick setup:
```bash
himalaya account configure
```

Verify:
```bash
himalaya envelope list --page-size 1
```

## iMessage (BlueBubbles)

BlueBubbles requires gateway config `channels.bluebubbles` with:
- `serverUrl`: BlueBubbles server URL
- `password`: API password
- `webhookPath`: webhook endpoint

Verify by sending a test message via the `message` tool with `channel: "bluebubbles"`.

## Target Formats

| Channel | Format | Example |
|---------|--------|---------|
| Email   | RFC 5322 address | `user@example.com` |
| iMessage | E.164 phone or chat_guid | `+15551234567` or `chat_guid:...` |
