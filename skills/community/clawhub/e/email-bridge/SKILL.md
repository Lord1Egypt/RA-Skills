---
name: email-bridge
description: Email management skill for AI assistants with real-time notifications, smart categorization (7 categories), verification code extraction, and HTML content sanitization. Supports Gmail, QQ Mail, and NetEase.
homepage: https://github.com/ryanchan720/email-bridge
source: https://github.com/ryanchan720/email-bridge
version: 0.6.3
---

# Email Bridge Skill

Email management skill for OpenClaw. Provides real-time email monitoring with smart categorization and clean notifications for AI assistants.

## Features

- **Real-time notifications**: IMAP IDLE (QQ/NetEase) + polling (Gmail)
- **Smart categorization**: 7 categories with subject-only classification
- **Verification code extraction**: Context-aware, low false positive rate
- **HTML content sanitization**: Clean text from HTML emails, remove invisible chars
- **Prompt injection protection**: Safe email content for AI processing
- **Multi-provider support**: Gmail (API), QQ Mail (IMAP), NetEase (IMAP)

## Installation

```bash
cd skills/email-bridge
pip install -e .
```

## Setup (Manual CLI Required)

⚠️ **Security Note**: Do NOT share authorization codes in chat. Configure accounts via CLI only.

```bash
# Add account (prompts for authorization code securely)
email-bridge accounts add your@qq.com -p qq

# Sync emails
email-bridge sync

# Start daemon for real-time notifications
email-bridge daemon start -d
```

### Getting Authorization Codes

**QQ Mail:** https://service.mail.qq.com/detail/0/75 (send SMS, get 16-char code)

**NetEase (163/126):** Settings → POP3/SMTP/IMAP → Enable → Get code

**Gmail:** Requires OAuth setup (see README.md)

## Capabilities

- **Receive emails**: Sync and read emails from configured accounts
- **Send emails**: Send emails via SMTP
- **Real-time notifications**: Push to OpenClaw via `openclaw system event`
- **Smart categorization**: 7 categories with keyword-based classification
- **Verification code extraction**: Context-aware extraction with low false positives
- **Link extraction**: Extract action links from emails
- **HTML sanitization**: Clean text extraction with invisible char removal
- **Prompt injection protection**: Sanitize email content for safe AI processing

## Email Categories

Subject-only classification for fast, reliable categorization:

| Category | Icon | Description | Example Keywords |
|----------|------|-------------|------------------|
| verification | 🔐 | Verification codes, activation | 验证码, OTP, activate, 绑定邮箱 |
| security | ⚠️ | Security alerts, login warnings | 安全提醒, security alert, 密码修改 |
| transactional | 📦 | Orders, payments, shipping | 订单确认, receipt, 发货通知 |
| promotion | 🎁 | Marketing, promotions, rewards | 奖励, 优惠, promo, discount |
| subscription | 📰 | Newsletters, digests | newsletter, 订阅, weekly digest |
| spam_like | 🚫 | Suspected spam | 中奖, FREE, click here now |
| normal | — | Regular email | (default) |

## Trigger Keywords

**Chinese:** 邮箱、邮件、发邮件、查看邮件、验证码、QQ邮箱、Gmail

**English:** email, mail, send email, check email, verification code

## Common Commands

```bash
# List recent emails
email-bridge messages list -n 10

# Get verification codes from recent emails
email-bridge codes

# Send email
email-bridge send -a <account_id> -t recipient@example.com -s "Subject" -b "Body"

# Daemon management
email-bridge daemon status
email-bridge daemon stop
```

## Configuration

Configuration file: `~/.email-bridge/config.json`

**Default configuration** (auto-generated, minimal):

```json
{
  "daemon": {
    "poll_interval": 300,
    "notify_openclaw": true
  }
}
```

**Full configuration with all options** (customize as needed):

```json
{
  "daemon": {
    "poll_interval": 300,
    "notify_openclaw": true,
    "notification": {
      "include_body": false,
      "body_max_length": 500,
      "include_verification_codes": true,
      "include_links": false
    }
  }
}
```

### Notification Options

| Option | Default | Description |
|--------|---------|-------------|
| `include_body` | `false` | Include email body preview in notifications |
| `body_max_length` | `500` | Max characters for body preview |
| `include_verification_codes` | `true` | Auto-extract and show verification codes |
| `include_links` | `false` | Include action links (verify/reset) |

## Notifications

When new emails arrive, the daemon sends formatted notifications:

```
📧 新邮件: account@qq.com

1. 🔐 Google
   您的验证码
   ✨ 验证码: 123456

2. ⚠️ Microsoft
   登录提醒
   📝 We noticed a new sign-in...

3. 🎁 OKX
   150 USDT 奖励等您拿
   📝 亲爱的欧易用户，欧易诚邀您加入邀请好友计划...
```

## HTML Content Processing

HTML-only emails are processed through:

1. **Tag stripping**: Remove `<style>`, `<script>`, and all HTML tags
2. **Entity decoding**: Convert HTML entities to text
3. **Invisible char removal**: Remove zero-width spaces, BOM, etc.
4. **Whitespace normalization**: Clean up spacing
5. **Prompt injection protection**: Remove dangerous patterns

**Example**: HTML with invisible chars → Clean readable text

## Security Features

- **Subject-only classification**: No body scanning for privacy
- **Context-aware code extraction**: Only extract near verification keywords
- **Invisible char sanitization**: Remove U+200B, U+FEFF, U+034F, etc.
- **Prompt injection protection**: Filter dangerous instruction patterns
- **Address pattern exclusion**: Don't extract numbers from addresses

## Data Storage

All data stored locally at `~/.email-bridge/`:

```
~/.email-bridge/
├── email_bridge.db    # SQLite database (accounts, messages)
├── config.json        # Configuration file
├── daemon.pid         # Daemon process ID
├── daemon.log         # Logs
└── gmail/
    ├── credentials.json  # OAuth credentials
    └── token_*.json      # OAuth tokens
```

⚠️ Credentials are stored unencrypted. Protect this directory.

## Revoking Access

```bash
# Stop daemon
email-bridge daemon stop

# Remove all stored data
rm -rf ~/.email-bridge

# For Gmail: revoke at https://myaccount.google.com/permissions
# For QQ/NetEase: regenerate authorization codes in email settings
```

## Dependencies

All from PyPI:
- click >= 8.0
- pydantic >= 2.0
- imaplib2 >= 3.6
- google-api-python-client >= 2.0 (Gmail only)
- google-auth-oauthlib >= 1.0 (Gmail only)

## Security Notes

1. **Never share authorization codes in chat** - use CLI interactively
2. **Credentials stored unencrypted** - protect `~/.email-bridge/` directory
3. **Email content is sanitized** - prompt injection protection enabled
4. **Daemon runs with user privileges** - no elevated access needed
5. **Subject-only classification** - privacy-conscious processing

## Changelog

### v0.6.2

- Add PROMOTION category for marketing emails (🎁 icon)
- Add TRANSACTIONAL category for orders/shipping (📦 icon)
- Expand keyword pools for all categories
- Add invisible character sanitization (U+200B, U+FEFF, U+034F, etc.)
- Improve HTML-to-text extraction
- Update documentation (DESIGN.md, README.md)

### v0.6.1

- Add IDLE keepalive (60s timeout) for connection stability
- Add sync retry mechanism (up to 3 retries)
- Improve daemon reliability for flaky networks

### v0.6.0

- Smart notification format based on email category
- Prompt injection protection with `sanitize_for_notification()`
- HTML-to-text fallback for HTML-only emails
- Subject-only classification for privacy
- Context-aware verification code extraction
- Category icons (🔐 ⚠️ 📦 🎁 📰 🚫)

### v0.5.7

- Initial ClawHub release
- Gmail, QQ Mail, NetEase support
- IMAP IDLE real-time notifications
- Verification code extraction
- Link extraction