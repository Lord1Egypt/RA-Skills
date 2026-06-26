# claw-boston-email

Give your OpenClaw agent a real email address at @claw.boston. Send and receive emails with one command.

## Install

```bash
openclaw skill install claw-boston-email
```

## Quick Start

1. **Set up your email:**
   Say "Set up my email" or "I need an email address"

2. **Send an email:**
   "Send an email to alice@example.com about tomorrow's meeting"

3. **Check your inbox:**
   "Do I have new emails?"

4. **Read an email:**
   "Read the latest email"

5. **Reply:**
   "Reply to that email saying I agree"

## Configuration

After setup, your credentials are stored at:
```
~/.openclaw/skills/claw-boston-email/config.json
```

Format:
```json
{
  "api_key": "ck_...",
  "address": "yourname@claw.boston",
  "webhook_configured": true
}
```

> **Security:** Never share your api_key. It grants full access to your mailbox.

## Free Plan Limits

- 1 mailbox
- 30 emails/day
- 7-day history

Paid plans coming soon at [claw.boston/pricing](https://claw.boston/pricing).

## FAQ

**Registration failed — name taken?**
Choose a different name. Names must be 8-32 characters, lowercase letters, numbers, dots, and hyphens only.

**Can't send emails?**
Check your daily quota. Free plan allows 30 emails/day. New accounts have lower limits in the first week.

**Not receiving emails?**
Make sure your webhook is configured. Say "Check my webhook config" to verify.

## Links

- Website: [claw.boston](https://claw.boston)
- Discord: [discord.gg/WuPp45xumx](https://discord.gg/WuPp45xumx)
- Twitter: [@clawboston](https://x.com/clawboston)
