---
name: emailbox
description: 职业邮箱收发与数据处理一体化工具。IMAP/SMTP protocol for 12+ providers (Gmail/Outlook/QQ/163/Yahoo/iCloud etc). Send/receive/search/schedule emails, HTML templates, attachments, forwarding, data integration. 邮件收发、搜索、定时发送、附件、HTML模板、转发、文档数据联动。
version: 1.1.0
license: MIT-0
metadata: {"openclaw": {"emoji": "📬", "requires": {"bins": ["python3"], "env": ["EMAIL_ADDRESS", "EMAIL_AUTH"]}, "primaryEnv": "EMAIL_AUTH"}}
---

# Emailbox - Professional Email Client & Data Integration

IMAP/SMTP-based email toolkit supporting 12+ providers. Send, receive, search, forward, schedule emails with HTML templates, attachments, and document data integration.

## Features

- **Send**: Plain text, HTML, attachments, CC/BCC, reply, forward
- **Receive**: List inbox, read emails, download attachments
- **Search**: By keyword (subject/from/body), date range, sender
- **Forward**: Fetch original email, forward to new recipients
- **Schedule**: Send emails at a future time
- **Templates**: 7 professional HTML email templates
- **Integration**: Excel/OCR/PDF data → format → email
- **Providers**: QQ, 163, 126, Sina, Outlook, Gmail, Yahoo, iCloud, Tencent Exmail, Ali Mail, Huawei, 139

## Trigger

- "Send email to..." / "发邮件给..."
- "Check inbox" / "查看收件箱"
- "Reply to this email" / "回复这封邮件"
- "Forward this email" / "转发这封邮件"
- "Search emails from..." / "搜索...的邮件"
- "Schedule email for..." / "定时发送..."
- "Process data and email..." / "整理数据后发邮件"
- "Attach this file..." / "添加附件..."

---

## Step 0: Setup

### Quick Start (Single Account)

```bash
# Set 2 environment variables and you're ready
export EMAIL_ADDRESS="your@qq.com"
export EMAIL_AUTH="your_authorization_code"
```

### Multi-Account Setup

```bash
# QQ Mail
export EMAIL_QQ="your@qq.com"
export EMAIL_QQ_AUTH="qq_auth_code"

# 163 Mail
export EMAIL_163="your@163.com"
export EMAIL_163_AUTH="163_client_password"

# Gmail
export EMAIL_GMAIL="your@gmail.com"
export EMAIL_GMAIL_AUTH="gmail_app_password"
```

### Provider Auth Guide

How to get authorization codes for each provider → `references/providers.md`

### Persistent Config

**IMPORTANT: Never store email credentials in plaintext files.** Use your system's secure credential manager or session-only environment variables.

```bash
# Option A: Session-only (recommended for security)
# Set environment variables in your current shell session only.
# Credentials will NOT persist after the session ends.
export EMAIL_ADDRESS="your@qq.com"
export EMAIL_AUTH="your_auth_code"

# Option B: Keychain / secret manager
# macOS: Use `security add-internet-password`
# Linux: Use `secret-tool store` (libsecret)
# Windows: Use Windows Credential Manager

# Option C: Restricted file (if persistent config is required)
# Create a file with restricted permissions that only you can read:
mkdir -p ~/.emailbox && touch ~/.emailbox/credentials
chmod 600 ~/.emailbox/credentials
# Then add your credentials:
# EMAIL_ADDRESS=your@qq.com
# EMAIL_AUTH=your_auth_code
# 
# Before running emailbox commands:
# source ~/.emailbox/credentials
```

---

## Step 1: Send Email

### Plain Text

```bash
python3 scripts/send_mail.py \
  --to "recipient@example.com" \
  --subject "Project Update" \
  --body "Hi, here is the project update..." \
  --provider qq
```

### Multiple Recipients + CC/BCC

```bash
python3 scripts/send_mail.py \
  --to "boss@company.com,team@company.com" \
  --cc "hr@company.com" \
  --bcc "archive@company.com" \
  --subject "Weekly Report" \
  --body "Please find the weekly report attached." \
  --provider 163
```

### HTML Email (Use Templates)

Choose a template from `references/templates.md`, fill in variables, save as HTML, then:

```bash
python3 scripts/send_mail.py \
  --to "client@company.com" \
  --subject "Sales Report - 2026W16" \
  --body-file "${OPENCLAW_WORKSPACE:-$PWD}/.emailbox_body.txt" \
  --html-file "${OPENCLAW_WORKSPACE:-$PWD}/.emailbox_body.html" \
  --provider outlook
```

### With Attachments

```bash
python3 scripts/send_mail.py \
  --to "finance@company.com" \
  --subject "Invoice - FP20260418001" \
  --body "Please find the invoice attached." \
  --attach "/path/to/invoice.jpg" "/path/to/detail.xlsx" \
  --provider qq
```

### High Priority + Read Receipt

```bash
python3 scripts/send_mail.py \
  --to "manager@company.com" \
  --subject "URGENT: Contract Review" \
  --body "Please review the attached contract ASAP." \
  --importance high \
  --receipt \
  --provider outlook
```

### Reply to Email

First get the Message-ID from reading an email (Step 3), then:

```bash
python3 scripts/send_mail.py \
  --to "sender@example.com" \
  --subject "Re: Original Subject" \
  --body "Got it, confirmed." \
  --reply-to "<msgid@example.com>" \
  --provider qq
```

### Forward Email

First get the original email metadata (Step 4), then:

```bash
python3 scripts/send_mail.py \
  --to "colleague@company.com" \
  --subject "Fwd: Original Subject" \
  --body "Please see the forwarded message below." \
  --forward-from "Original Sender <sender@example.com>" \
  --forward-date "Mon, 18 Apr 2026 10:30:00 +0800" \
  --forward-subject "Original Subject" \
  --forward-to "me@company.com" \
  --provider qq
```

---

## Step 2: Receive Email

### List Inbox (Recent Emails)

```bash
python3 scripts/receive_mail.py --list
python3 scripts/receive_mail.py --list --count 20
python3 scripts/receive_mail.py --list --provider gmail
python3 scripts/receive_mail.py --list --folder "Sent Items"
```

### Read Email Content

```bash
python3 scripts/receive_mail.py --read 123 --provider qq
```

### Download Attachments

```bash
python3 scripts/receive_mail.py --read 123 --download-attachment 123 \
  --save-dir "${OPENCLAW_WORKSPACE:-$PWD}/downloads"
```

---

## Step 3: Search Email

```bash
# Search by keyword (searches subject, from, AND body)
python3 scripts/receive_mail.py --search "contract" --provider qq

# Search by sender
python3 scripts/receive_mail.py --search "" --from-filter "zhangsan@company.com"

# Search by date range
python3 scripts/receive_mail.py --search "report" --since "2026-04-01"

# Combined search
python3 scripts/receive_mail.py --search "invoice" --from-filter "finance@company.com" --since "2026-04-01" --count 5
```

### IMAP Folders

Access folders beyond INBOX:
```bash
python3 scripts/receive_mail.py --list --folder "Sent Items"
python3 scripts/receive_mail.py --list --folder "Drafts"
python3 scripts/receive_mail.py --list --folder "Trash"
```

Common folder names:
- Gmail: `[Gmail]/Sent Mail`, `[Gmail]/Drafts`, `[Gmail]/Spam`
- QQ Mail: `Sent Messages`, `Drafts`, `Deleted Messages`
- 163 Mail: `Sent`, `Drafts`, `Deleted`
- Outlook: `SentItems`, `Drafts`, `Deleted`

---

## Step 4: Forward Email

```bash
# Step 1: Get original email metadata
python3 scripts/receive_mail.py --forward 123 --provider qq

# Output includes FORWARD_META with From/To/CC/Date/Subject/Message-ID

# Step 2: Forward using the metadata
python3 scripts/send_mail.py \
  --to "colleague@company.com" \
  --subject "Fwd: Original Subject" \
  --body "FYI, please see below." \
  --forward-from "Original Sender <sender@example.com>" \
  --forward-date "Mon, 18 Apr 2026 10:30:00 +0800" \
  --forward-subject "Original Subject" \
  --forward-to "me@company.com" \
  --provider qq
```

---

## Step 5: Document Data Integration

Combine other Skills' output with email sending.

Detailed workflows → `references/integrations.md`

### Common Patterns

```
1. Excel → Email: Read data → HTML table → send
2. OCR → Email: Recognize invoice → extract key info → send
3. PDF → Email: Process PDF → summary + attachment → send
4. Data Analysis → Email: Analyze data → conclusions → send
5. Scheduled Report: Generate content → schedule → send
```

### Excel Data → Email Example

```bash
# Step 1: Read and format data (use excel-studio or python3)
# Step 2: Save HTML content using a template from references/templates.md
# Step 3: Send
python3 scripts/send_mail.py \
  --to "boss@company.com" \
  --subject "Sales Report $(date +%Y%m%d)" \
  --body-file "${OPENCLAW_WORKSPACE:-$PWD}/.emailbox_body.txt" \
  --html-file "${OPENCLAW_WORKSPACE:-$PWD}/.emailbox_body.html" \
  --attach "/path/to/report.xlsx" \
  --provider qq
```

### Related Skills

| Skill | Integration | Scenario |
|-------|------------|----------|
| china-doc-ocr | OCR → email content | Invoice/contract recognition then email |
| excel-studio | Excel → table email | Data reports, financial statements |
| pdf-studio | PDF → email attachment | PDF report sending |
| data-analyzer | Analysis → email conclusions | Data insight notifications |

---

## Step 6: Schedule Email

### Send at Specific Time

```bash
python3 scripts/schedule_mail.py \
  --schedule --at "2026-04-19 09:00" \
  --to "boss@company.com" \
  --subject "Daily Report - 2026-04-19" \
  --body "Today's work summary..." \
  --provider qq
```

### Send in N Minutes

```bash
python3 scripts/schedule_mail.py \
  --schedule --in 30 \
  --to "client@example.com" \
  --subject "Follow up" \
  --body "Following up on our meeting..." \
  --provider 163
```

### Manage Scheduled Emails

```bash
# View scheduled emails
python3 scripts/schedule_mail.py --list-scheduled

# Cancel a scheduled email
python3 scripts/schedule_mail.py --cancel SCHEDULE_ID

# Manually process due emails
python3 scripts/schedule_mail.py --process-queue
```

### Auto-Processing (Manual Setup Only)

**⚠️ The schedule script will NEVER modify your crontab automatically.** You must manually confirm any crontab changes.

```bash
# Step 1: Check your current crontab first
crontab -l > ~/crontab_backup.txt

# Step 2: Add the emailbox processor manually (review before adding!)
# Add this line to your crontab ONLY if you want auto-processing:
# * * * * * python3 /path/to/emailbox/scripts/schedule_mail.py --process-queue

# Step 3: To remove later, edit your crontab and remove the line
```

---

## Step 7: HTML Email Templates

7 professional templates available → `references/templates.md`

| Template | Use Case |
|----------|----------|
| Business Report | Data reports, financial summaries |
| Meeting Invitation | Meetings, events, interviews |
| Notification / Announcement | Company announcements, system alerts |
| Thank You Letter | Appreciation, follow-ups |
| Weekly/Daily Report | Work progress updates |
| Invoice Notification | Invoice/receipt processing |
| Formal Letter | Official correspondence |

---

## Provider Configuration

12+ providers with IMAP/SMTP config and auth code guides → `references/providers.md`

| Provider | IMAP | SMTP | Port | Auth | China |
|----------|------|------|------|------|-------|
| QQ Mail | imap.qq.com | smtp.qq.com | 465 | Authorization code | Yes |
| 163 Mail | imap.163.com | smtp.163.com | 465 | Client password | Yes |
| 126 Mail | imap.126.com | smtp.126.com | 465 | Client password | Yes |
| Sina | imap.sina.com | smtp.sina.com | 465 | Enable IMAP | Yes |
| Outlook | outlook.office365.com | smtp.office365.com | 587 | App password | Yes |
| Gmail | imap.gmail.com | smtp.gmail.com | 587 | App password | VPN |
| Yahoo | imap.mail.yahoo.com | smtp.mail.yahoo.com | 587 | App password | VPN |
| iCloud | imap.mail.me.com | smtp.mail.me.com | 587 | App password | VPN |
| Tencent Exmail | imap.exmail.qq.com | smtp.exmail.qq.com | 465 | Enable IMAP | Yes |
| Ali Mail | imap.mxhichina.com | smtp.mxhichina.com | 465 | Enable IMAP | Yes |
| Huawei | imap.mail.hicloud.com | smtp.mail.hicloud.com | 465 | App password | Yes |
| 139 Mail | imap.mail.139.com | smtp.mail.139.com | 465 | Enable IMAP | Yes |

---

## Error Handling

```
Error                              → Solution
──────────────────────────────────────────────────────────
SMTP auth failed                   → Check authorization code, see providers.md
IMAP connection failed             → Verify IMAP enabled, check network
Connection timeout                 → Gmail/Yahoo/iCloud need VPN in China
SMTP auth code error (QQ/163)     → Use authorization code, NOT login password
Sending rate limit                 → QQ: 1/min, 500/day; 163: 200/day; Gmail: 500/day
Attachment too large               → QQ: 50MB; Gmail: 25MB; Outlook: 20MB
IMAP not enabled                   → Enable in email settings, see providers.md
163 requires phone verification    → Verify via SMS, wait 5-10 minutes
```

---

## Privacy & Security

- Direct IMAP/SMTP connection to email servers, no third-party data transfer
- **Credentials should be stored in environment variables only, NOT in plaintext files**
- Use provider-specific app passwords/authorization codes (NOT your login password)
- Authorization codes are email-specific, cannot be used to log into webmail
- Schedule queue stored in `~/.emailbox/queue/` — review and clean up regularly
- **This skill will NEVER modify your crontab or system scheduler without your explicit manual action**
- For maximum security, use a dedicated email account for automated sending

## Notes

- Requires IMAP/SMTP service enabled and authorization code configured
- Gmail/Yahoo/iCloud require VPN in mainland China
- QQ Mail limits: 500 emails/day, 1 email/minute
- 163/126 Mail limits: 200 emails/day
- Attachment size limits vary by provider (QQ: 50MB, Gmail: 25MB, Outlook: 20MB)
- Scheduled sending uses a local queue in `~/.emailbox/queue/`; processing requires manual crontab setup
- **Always use app passwords/authorization codes, never your real email login password**