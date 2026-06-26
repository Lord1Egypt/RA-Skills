---
name: email-reporter
description: Generic email reporting tool for OpenClaw agents. Auto-converts Markdown to PDF and sends as attachments.
version: 2.0.0
author: dirkcaiusa
license: MIT
metadata: {"openclaw":{"requires":{"bins":["python3"],"pip":["markdown","weasyprint"]}}}
---

# Email Reporter Skill

## Overview
A unified email reporting tool for OpenClaw agents. Automatically converts Markdown reports to PDF when images are detected, and sends them as attachments.

## Features

- **Smart Format Detection**: Auto-converts to PDF for reports with images or large files (>500KB)
- **Markdown Support**: Native Markdown rendering with syntax highlighting
- **Flexible Configuration**: Environment variables or config file for email settings
- **Multiple Backends**: Support for msmtp, SMTP, and sendmail

## Installation

```bash
clawhub install email-reporter
```

## Configuration

### Option 1: Environment Variables (Recommended)

```bash
export EMAIL_SENDER="your-email@qq.com"
export EMAIL_RECIPIENT="recipient@example.com"
export EMAIL_SMTP_HOST="smtp.qq.com"
export EMAIL_SMTP_PORT="587"
export EMAIL_SMTP_USER="your-email@qq.com"
export EMAIL_SMTP_PASS="your-auth-code"
```

### Option 2: Config File

Create `~/.email_reporter.conf`:

```json
{
  "sender": "your-email@qq.com",
  "recipient": "recipient@example.com",
  "smtp_host": "smtp.qq.com",
  "smtp_port": 587,
  "smtp_user": "your-email@qq.com",
  "smtp_pass": "your-auth-code",
  "use_msmtp": false
}
```

### Option 3: Command Line

```bash
python3 email_reporter.py report.md --sender me@qq.com --to friend@example.com
```

## Usage

### Basic Usage

```bash
# Send report to default recipient
python3 email_reporter.py report.md

# Specify agent name (used in subject)
python3 email_reporter.py report.md --agent "my-agent"

# Custom recipient
python3 email_reporter.py report.md --to "friend@example.com"

# Custom subject
python3 email_reporter.py report.md --subject "My Analysis Report"
```

### In Your Agent

```python
import subprocess

# Send a report
subprocess.run([
    "python3", "skills/email-reporter/email_reporter.py",
    "reports/analysis.md",
    "--agent", "invest-agent",
    "--to", "recipient@example.com"
])
```

## File Format Selection

| Scenario | Format | Delivery |
|----------|--------|----------|
| Plain text (<100KB) | Markdown | Direct |
| With images or >500KB | PDF | Attachment |
| Data tables | Markdown + CSV | Attachment bundle |

## SMTP Setup Guide

### QQ Mail (腾讯)
1. Enable SMTP: 设置 → 账户 → 开启SMTP服务
2. Generate auth code (not your password!)
3. Use auth code as `EMAIL_SMTP_PASS`

### Gmail
1. Enable 2FA
2. Generate App Password
3. Use app password as `EMAIL_SMTP_PASS`

### Outlook/Office 365
```bash
export EMAIL_SMTP_HOST="smtp.office365.com"
export EMAIL_SMTP_PORT="587"
```

## Troubleshooting

### Email not sending
```bash
# Test SMTP connection
python3 -c "
import smtplib
s = smtplib.SMTP('smtp.qq.com', 587)
s.starttls()
s.login('your-email@qq.com', 'your-auth-code')
print('Login OK')
"
```

### PDF conversion fails
```bash
# Install dependencies
pip install markdown weasyprint

# For Linux (Ubuntu/Debian)
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0
```

## License

MIT
