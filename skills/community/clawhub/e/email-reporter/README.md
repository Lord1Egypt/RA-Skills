# Email Reporter Skill v2.0.0

Generic email reporting tool for OpenClaw agents. Auto-converts Markdown to PDF and sends as attachments.

## Installation

```bash
# Clone or download this skill
cd email-reporter

# Install dependencies
pip install markdown weasyprint

# For Ubuntu/Debian - install system dependencies
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0
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

### Option 2: Interactive Setup Wizard

```bash
python3 email_reporter.py --setup
```

### Option 3: Command Line (Per-use)

```bash
python3 email_reporter.py report.md --sender me@qq.com --to friend@example.com
```

## Usage

```bash
# Basic usage
python3 email_reporter.py report.md

# With agent name
python3 email_reporter.py report.md --agent "my-agent"

# Custom recipient
python3 email_reporter.py report.md --to "friend@example.com"

# Custom subject
python3 email_reporter.py report.md --subject "Weekly Report"
```

## Files

- `email_reporter.py` - Main entry point
- `md2pdf.py` - Markdown to PDF converter
- `send_attachment.py` - Email sender with SMTP/msmtp support

## SMTP Setup

### QQ Mail
1. Enable SMTP: 设置 → 账户 → 开启SMTP服务
2. Generate auth code (NOT your password!)
3. Use auth code as EMAIL_SMTP_PASS

### Gmail
1. Enable 2FA
2. Generate App Password
3. Use app password as EMAIL_SMTP_PASS

### Outlook/Office 365
```bash
export EMAIL_SMTP_HOST="smtp.office365.com"
export EMAIL_SMTP_PORT="587"
```

## License

MIT
