#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
send_mail.py — 通过 SMTP 发送邮件
用法: python send_mail.py --workspace <path> --to <email> --subject <subject> --body <json>
"""
import json
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path


def parse_args():
    args = {}
    i = 1
    while i < len(sys.argv):
        key = sys.argv[i].lstrip("-").replace("-", "_")
        if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith("--"):
            args[key] = sys.argv[i + 1]
            i += 2
        else:
            args[key] = True
            i += 1
    return args


def load_smtp_config(workspace: Path):
    """从 identity.json 读取 SMTP 配置"""
    identity_path = workspace / "agent-network" / "identity.json"
    if not identity_path.exists():
        raise FileNotFoundError("identity.json 不存在，请先运行 init.py")
    
    data = json.loads(identity_path.read_text(encoding="utf-8"))
    if "email" not in data or "smtp" not in data["email"]:
        raise ValueError("identity.json 中未配置 SMTP，请先配置邮箱")
    
    return data["email"]["smtp"]


def send_mail(workspace: Path, to_email: str, subject: str, body_json: dict) -> str:
    """发送邮件，返回邮件 Message-ID"""
    smtp_config = load_smtp_config(workspace)
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = smtp_config["user"]
    msg["To"] = to_email
    
    # 添加纯文本和 JSON 两种格式
    text_body = json.dumps(body_json, ensure_ascii=False, indent=2)
    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(text_body, "json", "utf-8"))
    
    context = ssl.create_default_context()
    
    # 优先使用 SSL 端口 465
    try:
        with smtplib.SMTP_SSL(smtp_config["host"], 465, context=context) as server:
            server.login(smtp_config["user"], smtp_config["password"])
            server.sendmail(smtp_config["user"], [to_email], msg.as_string())
    except Exception as e:
        # 回退到 STARTTLS
        print(f"[WARN] SSL 失败，尝试 STARTTLS: {e}")
        with smtplib.SMTP(smtp_config["host"], 587) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(smtp_config["user"], smtp_config["password"])
            server.sendmail(smtp_config["user"], [to_email], msg.as_string())
    
    # 提取 Message-ID
    message_id = msg["Message-ID"]
    return message_id


if __name__ == "__main__":
    args = parse_args()
    workspace_str = args.get("workspace")
    workspace = Path(workspace_str) if workspace_str else Path(__file__).parent.parent.parent.parent
    
    to_email = args.get("to")
    subject = args.get("subject")
    body_str = args.get("body")
    
    if not to_email or not subject or not body_str:
        print("[ERROR] 需要 --to, --subject, --body", file=sys.stderr)
        sys.exit(1)
    
    try:
        body_json = json.loads(body_str)
        message_id = send_mail(workspace, to_email, subject, body_json)
        print(f"[OK] 邮件已发送")
        print(f"  收件人: {to_email}")
        print(f"  主题: {subject}")
        print(f"  Message-ID: {message_id}")
        print(f"\nMESSAGE_ID={message_id}")
    except Exception as e:
        print(f"[ERROR] 发送失败: {e}", file=sys.stderr)
        sys.exit(1)
