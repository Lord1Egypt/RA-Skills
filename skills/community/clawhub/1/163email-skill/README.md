# 163email Skill

Email sending skill for ClawHub via 163 SMTP service. Support custom recipient, subject, content.

## Quick Start

```bash
# Set credentials via environment variables
export CLAW_EMAIL="your_163_email@163.com"
export CLAW_EMAIL_AUTH="your_auth_code"

# Send email
python send_email.py "to@example.com" "Subject" "Content"
```

## License

MIT
