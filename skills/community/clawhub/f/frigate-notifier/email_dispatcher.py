import smtplib
import json
import argparse
import sys
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)

def send_email(to, subject, body, attachment_path=None):
    config = load_config()
    
    msg = MIMEMultipart()
    msg['From'] = config['smtp_user']
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    if attachment_path:
        try:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part['Content-Disposition'] = f"attachment; filename={os.path.basename(attachment_path)}"
            msg.attach(part)
        except Exception as e:
            print(f"Could not attach file {attachment_path}: {e}")

    try:
        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        if config.get('smtp_security') == 'tls':
            server.starttls()
        server.login(config['smtp_user'], config['smtp_pass'])
        server.send_message(msg)
        server.quit()
        print(f"Successfully sent email to {to}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="General Email Dispatcher")
    parser.add_argument("--to", required=True, help="Recipient email address")
    parser.add_argument("--subject", required=True, help="Email subject")
    parser.add_argument("--body", required=True, help="Email body text")
    parser.add_argument("--attachment", help="Path to file attachment")
    
    args = parser.parse_args()
    
    if send_email(args.to, args.subject, args.body, args.attachment):
        sys.exit(0)
    else:
        sys.exit(1)
