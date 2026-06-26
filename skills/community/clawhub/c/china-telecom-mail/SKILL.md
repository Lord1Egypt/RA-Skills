---
name: china-telecom-mail
description: "Send and receive emails via China Telecom (POP3:995, SMTP:465). Lists today's emails, reads content, forwards emails, and sends new emails."
metadata:
  {
    "openclaw":
      {
        "emoji": "📧",
        "requires": { "bins": ["uv", "python"] },
        "install": [],
      },
  }
---

# China Telecom Mail Skill

Send and receive emails via China Telecom (pop.chinatelecom.cn:995, smtp.chinatelecom.cn:465).

## Installation

Copy the `china-telecom-mail` folder to your OpenClaw skills directory:

```bash
# On Linux/macOS
cp -r china-telecom-mail ~/.openclaw/skills/

# On Windows
# Copy to C:\Users\<yourusername>\.openclaw\skills\china-telecom-mail
```

## Configuration

Edit `~/.openclaw/skills/china-telecom-mail/config.toml`:

```toml
[email]
# POP3 server (for receiving)
server = "pop.chinatelecom.cn"
port = 995
username = "your_email@chinatelecom.cn"
password = "your_password"

[smtp]
# SMTP server (for sending)
server = "smtp.chinatelecom.cn"
port = 465
```

## Usage

### Receive Emails

**List today's emails:**
```bash
openclaw run --skill china-telecom-mail list-today
```

**Read a specific email:**
```bash
openclaw run --skill china-telecom-mail read 21
```

**JSON output:**
```bash
openclaw run --skill china-telecom-mail json-summary
```

**Count today's emails:**
```bash
openclaw run --skill china-telecom-mail count
```

### Send Emails

**Send a simple email:**
```bash
openclaw run --skill china-telecom-mail send \
  --to "recipient@example.com" \
  --subject "会议通知" \
  --body "请参加明天下午3点的会议。"
```

**Send with attachment:**
```bash
openclaw run --skill china-telecom-mail send \
  --to "recipient@example.com" \
  --subject "报告" \
  --body "请查收附件" \
  --attachment "/path/to/report.pdf"
```

### Forward Emails

**Forward an email:**
```bash
openclaw run --skill china-telecom-mail forward \
  --email-id 21 \
  --to "recipient@example.com"
```

### Interactive Mode

```bash
uv run python ~/.openclaw/skills/china-telecom-mail/main.py interactive
```

## Direct Python Usage

```bash
# List today's emails
uv run python ~/.openclaw/skills/china-telecom-mail/main.py list-today

# Read email
uv run python ~/.openclaw/skills/china-telecom-mail/main.py read 21

# Send email
uv run python ~/.openclaw/skills/china-telecom-mail/main.py send \
  --to "test@example.com" \
  --subject "Test" \
  --body "Hello"

# Forward email
uv run python ~/.openclaw/skills/china-telecom-mail/main.py forward \
  --email-id 21 \
  --to "recipient@example.com"
```

## Directory Structure

```
china-telecom-mail/
├── SKILL.md          # OpenClaw skill metadata
├── main.py           # Main program (receive + send)
├── config.toml       # Configuration file
├── README.md         # This file
└── config.toml.example  # Config template
```

## Features

### Receive
- ✅ List today's emails with previews
- ✅ Read full email content
- ✅ JSON output for automation
- ✅ Automatic Chinese encoding detection

### Send
- ✅ Send plain text emails
- ✅ Send emails with attachments
- ✅ Forward received emails
- ✅ Interactive mode

## Tips

- Use `list-today` to see all today's emails
- Email IDs are 1-based (first email is ID 1)
- Use `forward` to forward received emails
- Use `send` to send new emails
- Supports both text and HTML email bodies
