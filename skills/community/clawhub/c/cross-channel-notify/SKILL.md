---
name: cross-channel-notify
description: Send the same notification across email (Himalaya) and iMessage (BlueBubbles) in one shot. Use when the user wants to broadcast or notify someone through multiple channels simultaneously, or asks for cross-channel / multi-channel notifications. Handles content formatting via a shared markdown template so both channels receive consistent, well-structured messages.
---

# Cross-Channel Notify

Send a single notification through both email and iMessage with unified markdown formatting.

## Prerequisites

- **Email**: Himalaya CLI configured (`himalaya --version`). See [references/channels.md](references/channels.md) for setup.
- **iMessage**: BlueBubbles channel enabled in gateway config (`channels.bluebubbles`).

## Workflow

1. **Collect inputs**: `to_email`, `to_imessage` (E.164 or chat_guid), `subject` (email), `body` (markdown).
2. **Format content**: Run `scripts/format_message.sh` to apply the shared markdown template. This produces two outputs:
   - `email_body`: full markdown (headers, bullet lists, signature block)
   - `imessage_body`: compact plain-text (stripped markdown syntax, ≤2000 chars)
3. **Send email**:
   ```bash
   cat << 'EOF' | himalaya template send
   From: <sender>
   To: <to_email>
   Subject: <subject>

   <email_body>
   EOF
   ```
4. **Send iMessage**: Use the `message` tool with `channel: "bluebubbles"`, `target: <to_imessage>`, `message: <imessage_body>`.
5. **Report**: Confirm both sends or surface any failures.

## Format Template

`scripts/format_message.sh` reads the body and applies:

- Title line (`## Notification`) prepended
- Timestamp line appended
- For email: keeps full markdown
- For iMessage: strips `#`, `**`, bullet markers, and truncates to 2000 chars

Usage:
```bash
scripts/format_message.sh "Your message body here"
# Outputs two lines: EMAIL_BODY <tab> IMESSAGE_BODY
```

## Channel Selection

Both channels are sent by default. To skip a channel:
- **Email only**: set `SKIP_IMESSAGE=1`
- **iMessage only**: set `SKIP_EMAIL=1`

```bash
SKIP_EMAIL=1 scripts/format_message.sh "Urgent: server down"
```

## Error Handling

- If Himalaya send fails, log the error and continue to iMessage.
- If iMessage send fails, log the error and report partial failure.
- Always report which channels succeeded/failed.
