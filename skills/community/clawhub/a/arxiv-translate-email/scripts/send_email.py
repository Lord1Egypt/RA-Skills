#!/usr/bin/env python3
"""发送邮件，支持 PDF 附件。"""
import sys
import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

SMTP_SERVER = 'smtp.qq.com'
SMTP_PORT = 465
SMTP_USER = '2794002698@qq.com'
SMTP_PASSWORD = 'ydtmhlhcraqudhcc'
FROM_ADDR = '2794002698@qq.com'


def send_email(to_addr: str, subject: str, body: str, pdf_path: str = None, attachment_name: str = None):
    msg = MIMEMultipart()
    msg['From'] = FROM_ADDR
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    # 如果 pdf_path 是 /dev/null 或 None，则不发附件
    if pdf_path and pdf_path != '/dev/null' and Path(pdf_path).exists():
        if attachment_name is None:
            attachment_name = Path(pdf_path).name
        with open(pdf_path, 'rb') as f:
            part = MIMEBase('application', 'pdf')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{attachment_name}"')
            part.add_header('Content-Type', 'application/pdf')
            msg.attach(part)

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(FROM_ADDR, to_addr, msg.as_string())
    print(f'Sent to {to_addr} successfully')


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('Usage: send_email.py <to_email> <subject> <body> <pdf_path> [attachment_name]')
        sys.exit(1)
    to_email = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    pdf_path = sys.argv[4]
    attachment_name = sys.argv[5] if len(sys.argv) > 5 else None
    send_email(to_email, subject, body, pdf_path, attachment_name)
