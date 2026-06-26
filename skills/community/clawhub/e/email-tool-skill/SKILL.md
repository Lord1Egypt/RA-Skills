---
name: email-skill
description: "Send mail with Python stdlib smtplib (SMTP_SSL to smtp.yeah.net:465). Documented account validates@yeah.net with embedded client auth code; standalone script e.g. /tmp/send_email.py, no TTY, no skill-local bash tools."
homepage: https://docs.python.org/3/library/smtplib.html
metadata: { "openclaw": { "emoji": "📧", "requires": { "bins": ["python3"] } } }
---

# Email (Python `smtplib`, NetEase yeah.net)

This skill is **documentation only**: the agent writes a **standalone** Python file (for example `/tmp/send_email.py`), runs `python3 /tmp/send_email.py …`, and relies on **stdlib only** (`smtplib`, `email.mime`). Nothing else in this skill folder is required.

## Why this pattern

- **No TTY prompts**: the SMTP session is a straight TCP/TLS login; it does not depend on an interactive terminal or CLI mail tools that may error with “cannot prompt item from list”.
- **One-shot execution**: `python3 /path/to/send_email.py` from any cwd.
- **No extra pip packages**: standard library only.
- **Contrast**: a separate `bash …/email send …` wrapper around another binary can hit TTY or pager issues in automated runners; this approach avoids that class of failures.

## NetEase yeah.net SMTP (fixed for this workspace)

| Item | Value |
|------|--------|
| SMTP host | `smtp.yeah.net` |
| Port | `465` (implicit TLS) |
| Python API | `smtplib.SMTP_SSL(host, port, timeout=…)` |
| Account (From / login user) | `validates@yeah.net` |
| Client authorization code (SMTP password) | `LWyx439sqLGuU68u` |

Use the **client authorization code** from the NetEase mail settings, not the web-login password alone if the provider requires a separate client password.

## Reference implementation (copy → edit recipient / subject / body)

Save as `/tmp/send_email.py` (or any path), then run with `python3 /tmp/send_email.py <to> <subject> <body>`.

```python
#!/usr/bin/env python3
import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.yeah.net"
SMTP_PORT = 465
SENDER_EMAIL = "validates@yeah.net"
SENDER_PASSWORD = "LWyx439sqLGuU68u"


def send_plain_email(receiver_email: str, subject: str, body: str) -> None:
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = SENDER_EMAIL
    message["To"] = receiver_email
    part = MIMEText(body, "plain", "utf-8")
    message.attach(part)

    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=30)
    try:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(message)
    finally:
        server.quit()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.stderr.write(
            "usage: python3 send_email.py <to> <subject> <body>\n"
        )
        sys.exit(1)
    send_plain_email(sys.argv[1], sys.argv[2], sys.argv[3])
```

Flow the agent should follow:

1. Write the file (constants above already match this workspace’s yeah.net account).
2. Run: `python3 /tmp/send_email.py "recipient@domain" "Subject line" "Plain text body"` (quote arguments with spaces).
3. On exception, print or return the error string to the user.

## Optional variants

- **UTF-8 subjects / long bodies**: keep `MIMEText(..., "plain", "utf-8")`; if the subject needs encoding beyond ASCII, use encoded-word headers per RFC 2047 or switch to `EmailMessage` + `set_content` with the same SMTP steps.
- **Weather or other dynamic body**: build the `body` string in Python before `send_plain_email`.

## Other NetEase domains

163 / 126 usually use `smtp.163.com` / `smtp.126.com`, port `465`, same `SMTP_SSL` pattern; replace host and credentials accordingly.

## Credential note

This file **embeds live SMTP credentials** by explicit workspace choice. Anyone with read access to this markdown can send mail as `validates@yeah.net`. If this tree is copied to a **public** repository, rotate the NetEase client authorization code and update `SENDER_PASSWORD` here.
