---
name: email-automation
description: Automate email processing: smart triage, auto-categorization, draft replies, and inbox zero. Works with Gmail, Outlook, and IMAP.
author: fly3094
version: 1.2.0
tags: [email, automation, gmail, outlook, inbox, productivity, ai, templates, batch, tracking]
support: 
  paypal: 492227637@qq.com
  email: 492227637@qq.com
metadata:
  clawdbot:
    emoji: 📧
    requires:
      bins:
        - python3
        - curl
    config:
      env:
        EMAIL_PROVIDER:
          description: Email provider (gmail|outlook|imap)
          default: "gmail"
          required: false
        EMAIL_ADDRESS:
          description: Your email address
          required: true
        GMAIL_CREDENTIALS_FILE:
          description: Path to Gmail API credentials JSON
          required: false
        OUTLOOK_ACCESS_TOKEN:
          description: Outlook/Microsoft Graph access token
          required: false
        IMAP_SERVER:
          description: IMAP server address
          required: false
        IMAP_USERNAME:
          description: IMAP username
          required: false
        IMAP_PASSWORD:
          description: IMAP password or app password
          required: false
        AUTO_ARCHIVE:
          description: Auto-archive processed emails
          default: "true"
          required: false
        CATEGORIES:
          description: Custom categories (comma-separated)
          default: "urgent,important,newsletters,notifications,receipts"
          required: false
---

# Email Automation 📧

Automate your email inbox with AI-powered triage, categorization, and draft replies. Achieve inbox zero effortlessly.

## What It Does

- 📥 **Smart Triage**: AI analyzes and prioritizes incoming emails
- 🏷️ **Auto-Categorization**: Sort emails into custom categories
- ✍️ **Draft Replies**: AI generates context-aware reply drafts
- 🗑️ **Auto-Archive**: Clean up newsletters, notifications, receipts
- ⚠️ **Urgent Alerts**: Get notified for important emails
- 📊 **Inbox Analytics**: Track email patterns and time saved

## Installation

```bash
clawhub install email-automation
```

## Commands

### Process Inbox
```
Process my inbox and categorize emails
```

### Generate Reply Drafts
```
Draft replies for unread important emails
```

### Clean Inbox
```
Archive newsletters and notifications older than 7 days
```

### Inbox Summary
```
Show me my inbox summary for today
```

### Urgent Emails Only
```
Show only urgent emails from today
```

### Setup Wizard
```
Help me set up email automation
```

## Configuration

### Environment Variables

```bash
# Email provider
export EMAIL_PROVIDER="gmail"  # gmail|outlook|imap

# Your email address
export EMAIL_ADDRESS="your@email.com"

# Gmail API (if using Gmail)
export GMAIL_CREDENTIALS_FILE="/path/to/credentials.json"

# Outlook API (if using Outlook)
export OUTLOOK_ACCESS_TOKEN="your_access_token"

# IMAP (if using other providers)
export IMAP_SERVER="imap.example.com"
export IMAP_USERNAME="your_username"
export IMAP_PASSWORD="your_app_password"

# Automation settings
export AUTO_ARCHIVE="true"
export CATEGORIES="urgent,important,newsletters,notifications,receipts"
```

### Gmail Setup (Recommended)

1. Visit https://console.cloud.google.com
2. Create new project
3. Enable Gmail API
4. Create OAuth credentials
5. Download credentials.json
6. Place in secure location
7. Set `GMAIL_CREDENTIALS_FILE` path

### Outlook Setup

1. Visit https://portal.azure.com
2. Register app in Azure AD
3. Add Microsoft Graph permissions
4. Generate access token
5. Set `OUTLOOK_ACCESS_TOKEN`

## Output Examples

### Inbox Summary
```
📧 Inbox Summary - March 7, 2026

Total emails: 47
• Urgent: 3
• Important: 8
• Newsletters: 15
• Notifications: 12
• Receipts: 5
• Unread: 11

Top senders:
1. Amazon (5 emails)
2. GitHub (4 emails)
3. LinkedIn (3 emails)

Time saved: ~2 hours
```

### Auto-Categorization
```
🏷️ Categorized 47 emails:

[Urgent] (3)
• Boss: "Meeting rescheduled to 3pm"
• Client: "Contract needs review ASAP"
• Bank: "Suspicious activity alert"

[Important] (8)
• Team: "Project update"
• Newsletter: "Industry insights"
...

[Newsletters] (15)
• TechCrunch Daily
• Hacker News Digest
...

[Notifications] (12)
• GitHub notifications
• Slack mentions
...

[Receipts] (5)
• Amazon order confirmation
• Uber receipt
...
```

### Draft Replies
```
✍️ Generated 5 reply drafts:

1. To: Boss
   Subject: Re: Meeting rescheduled
   Draft: "Thanks for the update. I'll be there at 3pm..."
   
2. To: Client
   Subject: Re: Contract review
   Draft: "I've reviewed the contract. Here are my thoughts..."

Drafts saved to drafts folder for your review.
```

## Automation Rules

### Default Rules

| Condition | Action |
|-----------|--------|
| From boss/client | Mark urgent |
| Contains "ASAP", "urgent" | Mark urgent |
| Newsletter sender | Auto-archive after 7 days |
| Receipt/invoice | Label & archive |
| Notification | Auto-archive after 3 days |
| Unsubscribe header | Suggest unsubscribe |

### Custom Rules

Create `rules.yml`:
```yaml
rules:
  - name: VIP senders
    from:
      - boss@company.com
      - important@client.com
    action: mark_urgent
    
  - name: Shopping receipts
    from:
      - amazon.com
      - ebay.com
    action: label_receipts
    
  - name: Social notifications
    subject_contains:
      - "mentioned you"
      - "new follower"
    action: archive
```

## Integration with Other Skills

### rss-to-social
```
Email notifications from rss-to-social
→ Auto-categorize as "Social Media Updates"
→ Archive after reading
```

### social-insights
```
Weekly analytics report
→ Email delivery
→ Auto-generate summary
```

### seo-content-pro
```
Content drafts
→ Send via email for review
→ Track feedback
```

## Use Cases

### Inbox Zero
- Process 100+ emails in minutes
- Auto-archive low-priority
- Focus on what matters

### Business Email
- Prioritize client emails
- Draft professional replies
- Never miss urgent messages

### Personal Email
- Filter newsletters
- Organize receipts
- Clean inbox automatically

## Pricing Integration

This skill powers LobsterLabs email services:
- **Setup & Configuration:** $299 one-time
- **Monthly Management:** $199/month
- **Business Plan:** $499/month (multiple accounts)

Contact: PayPal 492227637@qq.com

## Tips for Best Results

1. **Start with Gmail** - Best API support
2. **Use App Passwords** - More secure than regular passwords
3. **Review First Week** - Train AI on your preferences
4. **Customize Categories** - Match your workflow
5. **Set Up Filters** - Combine with email provider filters

## Troubleshooting

### Authentication Failed
- Verify credentials are correct
- Check API permissions
- Regenerate tokens if expired

### Emails Not Categorizing
- Ensure categories are configured
- Check AI model access
- Review categorization rules

### Drafts Not Generated
- Verify unread emails exist
- Check AI model availability
- Review draft folder permissions

## Changelog

### 1.0.0 (2026-03-07)
- Initial release
- Gmail/Outlook/IMAP support
- AI-powered categorization
- Auto-reply drafts
- Smart archiving
- Inbox analytics

---

## 💖 支持作者

如果你觉得这个技能有用，请考虑打赏支持：

- **PayPal**: 492227637@qq.com
- **邮箱**: 492227637@qq.com

你的支持是我持续改进的动力！

