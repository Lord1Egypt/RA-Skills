# ClawHub Listing · Email Customer Assistant

## Basic Info

- **Slug**: `email-customer-assistant`
- **Name**: Email Customer Assistant
- **Subtitle**: AI-powered email intelligent classification & customer service assistant
- **Category**: Productivity / Customer Service
- **Tags**: `email`, `IMAP`, `customer service`, `AI`, `classification`, `feishu`, `lark`
- **Pricing Tiers**:

| Tier | Price | Token Prefix |
|------|-------|--------------|
| FREE | ¥0 | `EMAIL-FREE` |
| STD | ¥9.9/mo | `EMAIL-STD` |
| PRO | ¥29/mo | `EMAIL-PRO` |
| MAX | ¥69/mo | `EMAIL-MAX` |

---

## Features (English)

### Core Features

- **📥 Email Fetching** — Connect to any IMAP-compatible mailbox and fetch new emails automatically
- **🏷️ AI Classification** — Classify emails into categories: Inquiry, Complaint, Order, Refund, Technical Support, etc.
- **🤖 Reply Suggestions** — Generate multilingual reply suggestions (Chinese/English/Japanese/Korean) via AI
- **🔔 Feishu Push** — Push real-time urgent email alerts and daily digest summaries to Feishu
- **📊 Summary Generation** — Automatically extract key email info and generate structured summaries

### Tier Feature Matrix

| Feature | FREE | STD | PRO | MAX |
|---------|:----:|:---:|:---:|:---:|
| Email Classification | ✅ | ✅ | ✅ | ✅ |
| Feishu Daily Digest | ✅ (1/day) | ✅ | ✅ | ✅ |
| Reply Suggestions | ❌ | ✅ | ✅ | ✅ |
| Urgent Email Realtime Push | ❌ | ✅ | ✅ | ✅ |
| Multi-email Support | ❌ | ❌ | ✅ | ✅ |
| Custom Classification Rules | ❌ | ❌ | ✅ | ✅ |
| All Language Support | ❌ | ❌ | ❌ | ✅ |
| API Unlimited | ❌ | ❌ | ❌ | ✅ |
| White Label | ❌ | ❌ | ❌ | ✅ |

---

## Requirements

### System Requirements
- Python 3.8+
- Internet access (for IMAP & AI API)
- IMAP-enabled email account

### Python Dependencies
```
imapclient>=2.3.0
email>=4.0.0
openai>=1.0.0
pyyaml>=6.0
requests>=2.28.0
```

### Configuration Required
- IMAP server host/port/credentials
- AI API key (OpenAI / Claude / DeepSeek compatible)
- Feishu webhook URL or user_id for push notifications

---

## Quick Start

```bash
# 1. Navigate to scripts directory
cd /home/gem/workspace/agent/skills/email-customer-assistant/scripts

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy and edit config
cp config.yaml.example config.yaml
# Edit config.yaml with your IMAP, AI API, and Feishu settings

# 4. Run email check (single execution)
python check_emails.py

# 5. Set up cron job for periodic checks (hourly)
# 0 * * * * cd /home/gem/workspace/agent/skills/email-customer-assistant/scripts && python check_emails.py
```

---

## File Structure

```
email-customer-assistant/
├── SKILL.md
├── README.md
├── CLAWHUB.md
├── SKILLHUB.md
└── scripts/
    ├── requirements.txt
    ├── config.yaml.example
    ├── imap_client.py
    ├── classifier.py
    ├── check_emails.py
    ├── feishu_pusher.py
    └── reply_generator.py
```

---

## Support

For issues or feature requests, please contact the developer.
