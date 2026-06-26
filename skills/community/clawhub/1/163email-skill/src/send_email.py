#!/usr/bin/env python3
"""
163email Skill - Send emails via 163 SMTP service
"""
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os

# Credential configuration via environment variables (recommended)
# Set CLAW_EMAIL and CLAW_EMAIL_AUTH before using this skill
SENDER = os.environ.get("CLAW_EMAIL", "")
AUTH_CODE = os.environ.get("CLAW_EMAIL_AUTH", "")

# SMTP configuration (can also be overridden via env vars)
SMTP_SERVER = os.environ.get("CLAW_SMTP_SERVER", "smtp.163.com")
SMTP_PORT = int(os.environ.get("CLAW_SMTP_PORT", "465"))


def send_mail(to, subject, content):
    """
    Send email via 163 SMTP service.

    Args:
        to: Recipient email address (multiple recipients separated by comma)
        subject: Email subject
        content: Email body content

    Returns:
        True if sent successfully, False otherwise
    """
    receivers = [x.strip() for x in to.split(',')]

    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header(f"163email Skill <{SENDER}>", 'utf-8')
    message['To'] = Header(f"Recipient <{to}>", 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtp_obj = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        smtp_obj.login(SENDER, AUTH_CODE)
        smtp_obj.sendmail(SENDER, receivers, message.as_string())
        smtp_obj.quit()
        print("Email sent successfully!")
        return True
    except smtplib.SMTPException as e:
        print(f"Email send failed, error message: {e}")
        return False


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 4:
        print("Usage: python send_email.py <recipient_email> <email_subject> <email_content>")
        print("Example: python send_email.py 'example@example.com' 'Test Email' 'This is test content'")
        sys.exit(1)

    to = sys.argv[1]
    subject = sys.argv[2]
    content = sys.argv[3]

    send_mail(to, subject, content)
