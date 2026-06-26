#!/usr/bin/env python3
import os, csv, smtplib, time, random, argparse
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ACCOUNT = os.environ.get('MAIL_ACCOUNT') or os.environ.get('GMAIL_EMAIL')
MAIL_CREDENTIAL = os.environ.get('MAIL_CREDENTIAL')
FROM_NAME = os.environ.get('FROM_NAME', 'Business Team')

if not EMAIL_ACCOUNT or not MAIL_CREDENTIAL:
    raise SystemExit('Missing MAIL_ACCOUNT / MAIL_CREDENTIAL')


def pick_email(row):
    for key in ['email', '邮箱', '真实邮箱']:
        val = (row.get(key) or '').strip()
        if '@' in val:
            return val
    return ''


def send_email(to_email, subject, body, attachments=None):
    msg = MIMEMultipart('mixed')
    msg['From'] = Header(f"{FROM_NAME} <{EMAIL_ACCOUNT}>")
    msg['To'] = to_email
    msg['Subject'] = Header(subject, 'utf-8')
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    for filepath in attachments or []:
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(filepath)}"')
                msg.attach(part)
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30)
    server.ehlo(); server.starttls(); server.login(EMAIL_ACCOUNT, MAIL_CREDENTIAL)
    server.sendmail(EMAIL_ACCOUNT, [to_email], msg.as_string())
    server.quit()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('csv_file')
    ap.add_argument('--subject', required=True)
    ap.add_argument('--body-file', required=True)
    ap.add_argument('--log-file', default='send_log.csv')
    ap.add_argument('--attachments', nargs='*', default=[])
    args = ap.parse_args()

    body = open(args.body_file, 'r', encoding='utf-8').read()
    with open(args.csv_file, 'r', encoding='utf-8') as f:
        clients = list(csv.DictReader(f))

    log_exists = os.path.exists(args.log_file)
    with open(args.log_file, 'a', encoding='utf-8', newline='') as log:
        writer = csv.writer(log)
        if not log_exists:
            writer.writerow(['time', 'email', 'status', 'note'])
        for row in clients:
            email = pick_email(row)
            if not email:
                continue
            try:
                send_email(email, args.subject, body, args.attachments)
                writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), email, 'success', ''])
                print(f'✓ {email}')
            except Exception as e:
                writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), email, 'fail', str(e)])
                print(f'✗ {email} {e}')
            log.flush()
            time.sleep(random.uniform(3, 8))

if __name__ == '__main__':
    main()
