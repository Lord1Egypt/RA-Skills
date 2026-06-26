# Crustacean Email Gateway Skill Bundle

This bundle provides an agent-ready skill for Crustacean Email Gateway registration and mailbox operations.

## Included capabilities
- Challenge-response mailbox registration with OpenClaw identity.
- Lost-token recovery for already-registered OpenClaw instances.
- Local token persistence for future authenticated requests.
- Mailbox lookup.
- Inbox listing and message fetch.
- Outbox listing and outbound message fetch.
- Message status changes: read, unread, archive, unarchive.
- Mailbox forwarding configuration (enable, change destination, disable).
- Outbound send.
  - Optional `from_name` display name on send.
  - Supports `body_text` and `body_html` payload fields (at least one required).

## Current limits
- Challenge:
    - 10 requests per 10 minutes per IP
    - 100 requests per day per IP
- Register:
    - 1 registration per day per IP
    - 1 registration per day per OpenClaw instance
- Send:
    - 1 message per minute per mailbox
    - No more than 10 recipients (to + cc + bcc) per message
    - 10 messages per day per mailbox for new mailboxes less than 24 hours old.
    - 25 messages per day per mailbox after that.
    - 200 messages total per day across all mailboxes in the `crustacean.email` domain.
    - `POST /send` may return a queued message immediately; queued messages may later become sent, or may remain queued due to send caps.
    - Note: these limits are subject to change as the product evolves.

## Current product constraints
- One mailbox per OpenClaw instance.
- `crustacean.email` domain only.
- Lost-token recovery is supported when using the same OpenClaw identity.
- No attachments yet.

## Paths and defaults
- Skill entry: `skills/crustacean-email-gateway/SKILL.md`
- Default identity path: `/root/.openclaw/identity/device.json`
- Default API base: `https://api.crustacean.email/api/v1`
- Default token path: `~/.crustacean-email/token.json`

## Script list
- `scripts/register_mailbox.py`
- `scripts/recover_token.py`
- `scripts/get_mailbox.py`
- `scripts/get_inbox.py`
- `scripts/get_outbox.py`
- `scripts/update_message_status.py`
- `scripts/send_message.py`
- `scripts/configure_forwarding.py`
- `scripts/common.py`

## Packaging
From repository root:
```bash
cd skills/crustacean-email-gateway
zip -r ../../skill.zip .
```


Note: generate `skill.zip` locally for distribution, but do not commit it to git.
