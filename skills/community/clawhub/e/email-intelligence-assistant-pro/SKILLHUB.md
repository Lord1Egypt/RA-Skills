# Tencent Skillhub Listing Info · Email Customer Assistant

---

## Basic Info

- **Skill Name**: Email Customer Assistant
- **Subtitle**: AI-driven Email Intelligent Classification & Customer Service Assistant
- **Category**: Office Efficiency > Customer Service > Email Assistant
- **Slug**: `email-customer-assistant`
- **Token Prefixes**: `EMAIL-FREE` / `EMAIL-STD` / `EMAIL-PRO` / `EMAIL-MAX`

---

## Detailed Feature Description

### Core Features

**📥 Automatic Email Fetching**
- Connect to any mailbox via IMAP protocol (QQ Mail, 163, Enterprise Mail, Gmail, etc.)
- Automatically retrieve new emails from specified folder (INBOX by default)
- Customizable check interval for flexible frequency control

**🏷️ AI Smart Classification**
- Semantic analysis of email content via LLM
- Auto-classification: inquiry, complaint, order, refund, technical support, quote, partnership, other
- Custom classification rules supported (PRO and above)

**🤖 Reply Suggestion Generation**
- AI analyzes email content and generates professional reply suggestions
- Multi-language support: EN/JP/KR (full language support in MAX tier)
- User confirmation required before sending — safe and controllable

**🔔 Feishu Push**
- Real-time push for urgent emails (STD and above)
- Daily scheduled digest card pushed to Feishu group or DM
- Keyword-triggered urgent detection (urgent, critical, outage, failure, etc.)

**📊 Email Summary**
- Auto-extracts key email info: sender, subject, summary, urgency level, suggested category
- Structured output for quick browsing

---

## Pricing Tiers

| Tier | Price | Features |
|------|-------|----------|
| **FREE** | ¥0/mo | Email classification, Feishu digest push (once daily) |
| **STD** | ¥9.9/mo | + Reply suggestion generation, real-time urgent email push |
| **PRO** | ¥29/mo | + Multi-mailbox support, custom classification rules |
| **MAX** | ¥69/mo | + Full language support, unlimited API, white-label |

### Feature Comparison

| Feature | FREE | STD | PRO | MAX |
|---------|:----:|:---:|:---:|:---:|
| AI Email Classification | ✅ | ✅ | ✅ | ✅ |
| Feishu Daily Digest | ✅ (once/day) | ✅ | ✅ | ✅ |
| Reply Suggestion Generation | ❌ | ✅ | ✅ | ✅ |
| Real-time Urgent Email Push | ❌ | ✅ | ✅ | ✅ |
| Multi-mailbox Support | ❌ | ❌ | ✅ | ✅ |
| Custom Classification Rules | ❌ | ❌ | ✅ | ✅ |
| Full Language Support | ❌ | ❌ | ❌ | ✅ |
| Unlimited API | ❌ | ❌ | ❌ | ✅ |
| White-label | ❌ | ❌ | ❌ | ✅ |

---

## Technical Requirements

### System Requirements
- Python 3.8+
- Network access (IMAP + AI API)
- Mailbox with IMAP enabled

### Python Dependencies
```
imapclient>=2.3.0
email>=4.0.0
openai>=1.0.0
pyyaml>=6.0
requests>=2.28.0
```

### Configuration Items
- IMAP server address/port/auth info
- AI API key (supports OpenAI/Claude/DeepSeek compatible endpoints)
- Feishu Webhook URL or user ID (for push notifications)

---

## Pre-upload Cleanup

Run the following commands before uploading:

```bash
# Delete test config files (keep .example template)
cd scripts/
rm -f config.yaml test_emails.json debug.log

# Delete __pycache__ and cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true

# Check for sensitive info
grep -r "password\|api_key\|token\|secret" --include="*.yaml" --include="*.py" --include="*.md" . || echo "No secrets found - OK"
```

---

## Quick Start

```bash
# 1. Navigate to scripts directory
cd scripts/

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy config template
cp config.yaml.example config.yaml
# Edit config.yaml, fill in IMAP, AI API, Feishu push config

# 4. Run once
python check_emails.py

# 5. Set up cron job (hourly)
crontab -e
# Add: 0 * * * * cd /path/to/scripts && python check_emails.py
```

---

## File Structure

```
email-customer-assistant/
├── SKILL.md              # Skill definition
├── README.md             # Usage guide
├── CLAWHUB.md            # ClawHub listing info (English)
├── SKILLHUB.md           # Tencent Skillhub listing info (this file)
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

## Notes

1. **Email Password**: Use "App Password" from your email provider, NOT your login password
2. **IMAP Access**: Some mailbox providers require manual IMAP enabling in settings (e.g. QQ Mail, 163)
3. **API Quota**: Recommend setting `max_tokens` to limit per-output and avoid excessive consumption
4. **Feishu Webhook**: Webhook URL can only push to the corresponding group; add a custom bot to Feishu first
5. **Check Frequency**: `check_interval` recommended no lower than 60 seconds to avoid rate limits
6. **Data Security**: Config file contains sensitive info — do not commit to public repositories
