---
name: disposable-email
description: Create disposable Mail.tm inboxes and programmatically read incoming emails/OTP codes. Use when asked to generate a temporary email, poll inbox messages, extract OTPs, or automate email verification testing with Mail.tm.
---

# Disposable Email

Create and read temporary Mail.tm inboxes for testing email flows.

## Use bundled scripts

- Create inbox + token:
  - `python3 scripts/create_inbox.py`
  - Returns JSON with `address`, `password`, `token`, `accountId`, `domain`.

- List messages:
  - `python3 scripts/read_inbox.py --token <TOKEN> --list`

- Read latest message:
  - `python3 scripts/read_inbox.py --token <TOKEN> --latest`

- Wait for OTP from incoming mail:
  - `python3 scripts/read_inbox.py --token <TOKEN> --wait-otp --timeout 120 --interval 3`
  - Default OTP regex: `\\b(\\d{4,8})\\b`
  - Override regex with `--otp-regex`.

- End-to-end (create inbox + wait for first message/OTP):
  - `python3 scripts/e2e_otp.py --timeout 120 --interval 3`
  - First line emits `inbox_created` JSON (address/password/token).
  - Then emits one of: `otp_found`, `message_received_no_otp`, or `timeout`.
  - Add `--save ./otp-result.json` to persist the latest emitted result to disk.

## Workflow

1. Run `create_inbox.py` and share the generated email address.
2. Trigger email delivery to that address.
3. Poll with `read_inbox.py` (`--latest` or `--wait-otp`).
4. Return sender, subject, createdAt, and message text/OTP.

## Notes

- Free temp domains can be blocked by some production services.
- Keep token private; treat it like mailbox access credentials.
- Prefer stable paid inbox providers for CI if reliability is critical.
