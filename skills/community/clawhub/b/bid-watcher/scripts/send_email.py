#!/usr/bin/env python3
"""
邮件发送脚本
发送周报邮件
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import glob

# 基于脚本自身位置确定 data 目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "data")

# 配置（从环境变量或配置文件读取）
SMTP_HOST = os.environ.get("BID_SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("BID_SMTP_PORT", "587"))
SMTP_USER = os.environ.get("BID_SMTP_USER", "")
SMTP_PASS = os.environ.get("BID_SMTP_PASS", "")
REPORT_TO = os.environ.get("BID_REPORT_TO", "")

def send_report(subject, body, attachments=None):
    """发送周报邮件"""

    if not SMTP_USER or not SMTP_PASS or not REPORT_TO:
        print("[警告] 邮件配置不完整，跳过发送")
        print(f"  SMTP_HOST: {SMTP_HOST}:{SMTP_PORT}")
        print(f"  SMTP_USER: {SMTP_USER}")
        print(f"  REPORT_TO: {REPORT_TO}")
        return False

    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = REPORT_TO
    msg['Subject'] = subject

    # 正文
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    # 附件
    if attachments:
        for filepath in attachments:
            if filepath and os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    filename = os.path.basename(filepath)
                    part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                    msg.attach(part)

    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, REPORT_TO.split(','), msg.as_string())
        server.quit()
        print(f"[✓] 邮件已发送至: {REPORT_TO}")
        return True
    except Exception as e:
        print(f"[✗] 邮件发送失败: {e}")
        return False

def find_latest_report():
    """找最新周报文件"""
    files = glob.glob(os.path.join(DATA_DIR, "bid_report_*.md"))
    if not files:
        return None
    return max(files)

if __name__ == "__main__":
    today = datetime.now()
    year = today.year
    week_num = today.isocalendar()[1]
    subject = f"[投标情报] 第{year}年第{week_num}周周报 - {today.strftime('%m月%d日')}"

    body = f"""您好，

第{year}年第{week_num}周投标情报周报已生成，详见附件。

如需查看完整数据，请访问系统。

---
bid-watcher 自动发送
"""

    report_file = find_latest_report()
    attachments = [report_file] if report_file else []

    if '--dry-run' in sys.argv:
        import sys
        print(f"[模拟] 邮件主题: {subject}")
        print(f"[模拟] 收件人: {REPORT_TO}")
        print(f"[模拟] 附件: {report_file}")
    else:
        send_report(subject, body, attachments)
