#!/usr/bin/env python3
"""
send_email.py — 发送抖音日报邮件（使用 EmailMessage 正确处理中文文件名）
"""
import argparse
import json
import os
import smtplib
from email.message import EmailMessage
from pathlib import Path


DEFAULT_RECIPIENTS = ['3249331357@qq.com']
DEFAULT_SMTP_HOST = 'smtp.qq.com'
DEFAULT_SMTP_PORT = 587


def build_recipients() -> list[str]:
    env_val = os.environ.get('DOUYIN_EMAIL_RECIPIENTS', '')
    if env_val.strip():
        return [r.strip() for r in env_val.split(',') if r.strip()]
    return DEFAULT_RECIPIENTS


def send(note_path: str, topic: str, docx_path: str = None) -> dict:
    smtp_host = os.environ.get('SMTP_HOST', DEFAULT_SMTP_HOST)
    smtp_port = int(os.environ.get('SMTP_PORT', DEFAULT_SMTP_PORT))
    sender = os.environ.get('SMTP_USER', '')
    password = os.environ.get('SMTP_PASS', '')

    if not sender or not password:
        raise EnvironmentError('SMTP_USER and SMTP_PASS environment variables must be set.')

    recipients = build_recipients()
    path = Path(note_path)
    subject = f'【抖音视频分析】{topic}'

    msg = EmailMessage()
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject
    msg.set_content(path.read_text(encoding='utf-8'), charset='utf-8')

    # 只发 DOCX 附件（不发 MD）
    if docx_path and Path(docx_path).exists():
        docx_bytes = Path(docx_path).read_bytes()
        docx_name = Path(docx_path).name
        msg.add_attachment(
            docx_bytes,
            maintype='application',
            subtype='vnd.openxmlformats-officedocument.wordprocessingml.document',
            filename=docx_name,
        )

    with smtplib.SMTP(smtp_host, smtp_port) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(sender, password)
        smtp.sendmail(sender, recipients, msg.as_bytes())

    return {
        'status': 'sent',
        'recipients': recipients,
        'subject': subject,
        'attachments': [path.name] + ([Path(docx_path).name] if docx_path else []),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--note-path', required=True)
    ap.add_argument('--docx-path', default='')
    ap.add_argument('--topic', default='抖音视频')
    args = ap.parse_args()
    result = send(args.note_path, args.topic, args.docx_path if args.docx_path else None)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
