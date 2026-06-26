---
name: 163email-skill
description: "163email skill - Send emails via 163 SMTP service with custom recipient, subject, content. Support CLI and Python import"
version: 1.2.0
author: geekbin
license: MIT
tags:
  - 163email
  - email
  - smtp
  - notification
  - utility
  - latest
metadata:
  openclaw:
    requires:
      env:
        - CLAW_EMAIL
        - CLAW_EMAIL_AUTH
      bins:
        - python
    install: []
---

# 163email Skill - Email Sender

Send emails via 163 SMTP service. Support custom recipient, subject, content. Both CLI and Python module import calling methods are supported.

## Features

- Send plain text emails via 163 SMTP
- One-click command line invocation
- Python module import support
- SSL encrypted transmission
- Multiple recipients support

## Usage

### Method 1: Command Line

```bash
python send_email.py "recipient@example.com" "Test Subject" "Email content here"
```

### Method 2: Python Import

```python
from src.send_email import send_mail

send_mail(
    to="recipient@example.com",
    subject="Test Email",
    content="This is the email content"
)
```

## Configuration

Set environment variables before use:

```bash
export CLAW_EMAIL="your_163_email@163.com"
export CLAW_EMAIL_AUTH="your_smtp_authorization_code"
export CLAW_SMTP_SERVER="smtp.163.com"  # optional
export CLAW_SMTP_PORT="465"  # optional
```

Or use in Python:
```python
import os
os.environ["CLAW_EMAIL"] = "your_email@163.com"
os.environ["CLAW_EMAIL_AUTH"] = "your_auth_code"
```

## Requirements

- Python 3.6+
- No third-party dependencies (uses smtplib, email standard library)

## License

MIT
