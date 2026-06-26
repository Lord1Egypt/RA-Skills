# Email Customer Assistant

AI-driven email intelligent classification and customer service assistant. Automatically connects to mailbox via IMAP, classifies emails, generates reply suggestions, and pushes summaries to Feishu.

---

## Features

- 📥 **Email Fetching**: Automatically connects to mailbox via IMAP protocol, retrieves latest emails
- 🏷️ **Smart Classification**: AI-based email classification (inquiry, complaint, order, refund, technical support, etc.)
- 🤖 **Reply Suggestions**: AI generates multi-language reply suggestions (EN/JP/KR), sent after user confirmation
- 🔔 **Feishu Push**: Real-time push for urgent emails, daily digest card pushed to Feishu
- 📊 **Summary Generation**: Auto-extracts key email info and generates structured summary

---

## Installation

```bash
# Navigate to scripts directory
cd scripts/

# Install Python dependencies
pip install -r requirements.txt
```

---

## Configuration

### 1. Copy Config Template

```bash
cp config.yaml.example config.yaml
```

### 2. Configure IMAP

Edit `config.yaml`:

```yaml
imap:
  host: "imap.example.com"        # IMAP server address
  port: 993                       # IMAP port (SSL usually 993)
  username: "your@email.com"      # Email account
  password: "your_app_password"  # App-specific password (NOT login password)
  folders:
    - "INBOX"                    # Folders to check
  check_interval: 300             # Check interval (seconds)
```

### 3. Configure AI API

```yaml
ai:
  provider: "openai"              # or "claude", "deepseek"
  api_key: "sk-xxxx"              # API key
  model: "gpt-4o-mini"             # Model to use
  base_url: "https://api.openai.com/v1"  # API address (for self-hosted)
  max_tokens: 1000
  temperature: 0.7
```

### 4. Configure Feishu Push

**Method 1: Webhook (for group chat)**

```yaml
feishu:
  webhook:
    url: "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx"  # Webhook URL
    secret: ""                       # Signature secret (if any)
```

**Method 2: User ID Push (for DM)**

```yaml
feishu:
  user_push:
    user_id: "ou_xxxxxxxx"          # Feishu user Open ID
    app_token: "your_app_token"     # Feishu app token
```

**Urgent Email Rules**

```yaml
feishu:
  urgent_keywords:
    - "urgent"
    - "critical"
    - "outage"
    - "failure"
  realtime_push: true               # Real-time push for urgent emails
  daily_digest: true                # Daily digest push
  digest_time: "09:00"             # Daily push time
```

---

## Quick Start

### Run Email Check (One-shot)

```bash
cd scripts/
python check_emails.py
```

### Set up Cron Job (Hourly)

```bash
crontab -e
# Add the following line:
# 0 * * * * cd /path/to/scripts && python check_emails.py >> /var/log/email_assistant.log 2>&1
```

### Integrate with OpenClaw

Configure a cron job or workflow in OpenClaw to invoke `check_emails.py` script.

---

## Pricing Tiers

| Tier | Price | Features |
|------|-------|----------|
| FREE | ¥0 | Email classification, Feishu digest push (once daily) |
| STD | ¥9.9/mo | + Reply suggestion generation, real-time urgent email push |
| PRO | ¥29/mo | + Multi-mailbox support, custom classification rules |
| MAX | ¥69/mo | + Full language support, unlimited API, white-label |

---

## Notes

1. **Email Password**: Strongly recommend using "App Password" from your email provider, NOT your login password
2. **IMAP Access**: Ensure IMAP service is enabled on your mailbox; some providers (e.g. QQ mail) require manual enabling in settings
3. **API Quota**: AI reply generation consumes API quota; recommend setting `max_tokens` to limit per-output
4. **Feishu Webhook**: Webhook URL can only push to the corresponding group; add a custom bot to Feishu first
5. **Rate Limits**: Recommend `check_interval` no lower than 60 seconds to avoid triggering mailbox provider rate limits
6. **Data Security**: Config file contains sensitive info — do not commit to public repositories

---

## File Structure

```
email-customer-assistant/
├── SKILL.md              # Skill definition file
├── README.md             # This file
├── CLAWHUB.md            # ClawHub listing info
├── SKILLHUB.md           # Tencent Skillhub listing info
└── scripts/
    ├── requirements.txt     # Python dependencies
    ├── config.yaml.example  # Config template
    ├── imap_client.py       # IMAP connection module
    ├── classifier.py        # AI classification module
    ├── check_emails.py     # Main check script
    ├── feishu_pusher.py    # Feishu push module
    └── reply_generator.py  # Reply generation module
```

---

## Technical Support

For issues, please submit an Issue or contact the developer.

---

> For paid plans, visit [YK-Global.com](https://yk-global.com)
