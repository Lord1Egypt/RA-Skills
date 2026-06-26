#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
receive_mail.py — 通过 IMAP 收取邮件
用法: python receive_mail.py --workspace <path> [--unread_only] [--limit <n>]
"""
import json
import imaplib
import email
import re
from email import message as email_message
from pathlib import Path
from datetime import datetime, timezone


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


def load_imap_config(workspace: Path):
    """从 identity.json 读取 IMAP 配置"""
    identity_path = workspace / "agent-network" / "identity.json"
    if not identity_path.exists():
        raise FileNotFoundError("identity.json 不存在")
    
    data = json.loads(identity_path.read_text(encoding="utf-8"))
    if "email" not in data or "imap" not in data["email"]:
        raise ValueError("identity.json 中未配置 IMAP")
    
    return data["email"]["imap"]


def find_inbox(mail) -> str:
    """查找并返回收件箱名称"""
    # 列出文件夹
    status, folders = mail.list()
    if status != "OK":
        return "INBOX"  # 默认尝试
    
    # 解析文件夹名
    pattern = re.compile(r'"([^"]+)"')
    for f in folders:
        matches = pattern.findall(f.decode())
        for match in matches:
            if match.upper() == "INBOX":
                return match
    
    return "INBOX"


def parse_email_content(msg: email_message.Message) -> dict:
    """解析邮件内容，提取 JSON body"""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "application/json":
                payload = part.get_payload(decode=True)
                if payload:
                    return json.loads(payload.decode("utf-8"))
            # 也尝试 text/plain
            if content_type == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    try:
                        return json.loads(payload.decode("utf-8"))
                    except:
                        pass
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            try:
                return json.loads(payload.decode("utf-8"))
            except:
                pass
    return {}


def receive_mail(workspace: Path, unread_only: bool = True, limit: int = 10) -> list:
    """收取邮件，返回邮件列表"""
    imap_config = load_imap_config(workspace)
    
    # 连接 IMAP
    mail = imaplib.IMAP4_SSL(imap_config["host"], imap_config["port"])
    mail.login(imap_config["user"], imap_config["password"])
    
    # 查找收件箱
    inbox_name = find_inbox(mail)
    
    # 尝试选择收件箱（163 邮箱可能需要特殊处理）
    try:
        status, _ = mail.select(inbox_name)
    except Exception as e:
        # 如果 select 失败，尝试不指定文件夹直接搜索
        status = "OK"  # 假设成功
    
    # 检查未读邮件数量
    try:
        status, data = mail.status(inbox_name, '(MESSAGES UNSEEN)')
        if status == "OK":
            # 解析: "INBOX" (MESSAGES 5 UNSEEN 5)
            match = re.search(r'UNSEEN (\d+)', data[0].decode())
            if match:
                unread_count = int(match.group(1))
                print(f"[INFO] 未读邮件: {unread_count}")
    except:
        pass
    
    # 搜索邮件 - 使用 ALL 而不是 UNSEEN 来避免 SELECT 问题
    if unread_only:
        # 尝试获取未读邮件
        try:
            status, message_ids = mail.search(None, "UNSEEN")
        except:
            # 回退到所有邮件
            status, message_ids = mail.search(None, "ALL")
    else:
        status, message_ids = mail.search(None, "ALL")
    
    if status != "OK":
        mail.logout()
        return []
    
    ids = message_ids[0].split()
    ids = ids[-limit:]  # 只取最新的
    
    emails = []
    for mid in ids:
        try:
            status, msg_data = mail.fetch(mid, "(RFC822)")
            if status != "OK":
                continue
            
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            subject = msg["Subject"] or ""
            message_id = msg["Message-ID"] or ""
            from_addr = email.utils.parseaddr(msg["From"])[1]
            date = msg["Date"] or ""
            
            # 解析 JSON 内容
            content = parse_email_content(msg)
            
            emails.append({
                "messageId": message_id,
                "subject": subject,
                "from": from_addr,
                "date": date,
                "content": content
            })
            
            # 尝试标记为已读
            if unread_only:
                try:
                    mail.store(mid, "+FLAGS", "\\Seen")
                except:
                    pass
        except Exception as e:
            print(f"[WARN] 获取邮件 {mid} 失败: {e}")
            continue
    
    mail.logout()
    return emails


if __name__ == "__main__":
    args = parse_args()
    workspace_str = args.get("workspace")
    workspace = Path(workspace_str) if workspace_str else Path(__file__).parent.parent.parent.parent
    
    unread_only = "unread_only" in args
    limit = int(args.get("limit", 10))
    
    try:
        emails = receive_mail(workspace, unread_only, limit)
        print(f"[OK] 收到 {len(emails)} 封邮件")
        for em in emails:
            print(f"\n--- 邮件 ---")
            print(f"  Subject: {em['subject']}")
            print(f"  From: {em['from']}")
            print(f"  Message-ID: {em['messageId']}")
            if em['content']:
                print(f"  Content: {json.dumps(em['content'], ensure_ascii=False)[:200]}...")
        print(f"\nEMAILS_JSON={json.dumps(emails, ensure_ascii=False)}")
    except Exception as e:
        print(f"[ERROR] 收取失败: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
