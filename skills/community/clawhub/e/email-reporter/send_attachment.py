#!/usr/bin/env python3
"""
Send email with attachment
Supports SMTP and msmtp backends
"""

import os
import sys
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def get_config():
    """Get configuration from environment"""
    return {
        "sender": os.getenv("EMAIL_SENDER", ""),
        "smtp_host": os.getenv("EMAIL_SMTP_HOST", "smtp.qq.com"),
        "smtp_port": int(os.getenv("EMAIL_SMTP_PORT", "587")),
        "smtp_user": os.getenv("EMAIL_SMTP_USER", ""),
        "smtp_pass": os.getenv("EMAIL_SMTP_PASS", ""),
        "use_msmtp": os.getenv("EMAIL_USE_MSMTP", "false").lower() == "true"
    }

def send_via_smtp(to_addr, subject, body, attachment_path, config):
    """Send email via SMTP"""
    
    sender = config.get("sender") or config.get("smtp_user")
    if not sender:
        raise ValueError("Sender email not configured")
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = to_addr
    msg['Subject'] = subject
    
    # Attach body
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # Attach file
    if attachment_path and os.path.exists(attachment_path):
        filename = os.path.basename(attachment_path)
        
        # Determine MIME type
        mime_type = 'application/octet-stream'
        if filename.endswith('.pdf'):
            mime_type = 'application/pdf'
        elif filename.endswith('.md') or filename.endswith('.txt'):
            mime_type = 'text/plain'
        
        with open(attachment_path, 'rb') as f:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(f.read())
        
        encoders.encode_base64(attachment)
        attachment.add_header(
            'Content-Disposition',
            f'attachment; filename="{filename}"'
        )
        msg.attach(attachment)
        print(f"📎 Attached: {filename}")
    
    # Send via SMTP
    try:
        server = smtplib.SMTP(config["smtp_host"], config["smtp_port"])
        server.starttls()
        server.login(config["smtp_user"], config["smtp_pass"])
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"❌ SMTP error: {e}")
        return False

def send_via_msmtp(to_addr, subject, body, attachment_path):
    """Send email via msmtp"""
    
    # Build MIME message
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    
    config = get_config()
    sender = config.get("sender") or config.get("smtp_user")
    
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = to_addr
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    if attachment_path and os.path.exists(attachment_path):
        filename = os.path.basename(attachment_path)
        
        with open(attachment_path, 'rb') as f:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(f.read())
        
        encoders.encode_base64(attachment)
        attachment.add_header(
            'Content-Disposition',
            f'attachment; filename="{filename}"'
        )
        msg.attach(attachment)
    
    # Write to temp file and send via msmtp
    temp_file = '/tmp/email_reporter_msg.eml'
    with open(temp_file, 'wb') as f:
        f.write(msg.as_bytes())
    
    cmd = f'cat {temp_file} | msmtp -t {to_addr}'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    return result.returncode == 0

def send_email_with_attachment(to_addr, subject, attachment_path, body="Please see attachment."):
    """Main send function - auto-detects backend"""
    
    config = get_config()
    
    if not config.get("smtp_pass"):
        print("❌ SMTP password not configured. Set EMAIL_SMTP_PASS")
        return False
    
    print(f"📧 Sending to: {to_addr}")
    print(f"📋 Subject: {subject}")
    
    if config.get("use_msmtp"):
        print("🔧 Using msmtp backend")
        success = send_via_msmtp(to_addr, subject, body, attachment_path)
    else:
        print(f"🔧 Using SMTP: {config['smtp_host']}:{config['smtp_port']}")
        success = send_via_smtp(to_addr, subject, body, attachment_path, config)
    
    if success:
        print("✅ Email sent successfully")
    else:
        print("❌ Failed to send email")
    
    return success

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 send_attachment.py <to_addr> <subject> <attachment_path> [body_text]")
        print("")
        print("Environment variables:")
        print("  EMAIL_SENDER    - Sender email address")
        print("  EMAIL_SMTP_HOST - SMTP server (default: smtp.qq.com)")
        print("  EMAIL_SMTP_PORT - SMTP port (default: 587)")
        print("  EMAIL_SMTP_USER - SMTP username")
        print("  EMAIL_SMTP_PASS - SMTP password/auth code")
        sys.exit(1)
    
    to_addr = sys.argv[1]
    subject = sys.argv[2]
    attachment_path = sys.argv[3]
    body = sys.argv[4] if len(sys.argv) > 4 else "Please see attachment."
    
    success = send_email_with_attachment(to_addr, subject, attachment_path, body)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
