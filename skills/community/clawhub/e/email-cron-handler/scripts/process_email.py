#!/usr/bin/env python3
"""
邮件指令处理器 - Email Cron Handler
用于自动接收邮件指令、执行并回复结果

用法:
    python process_email.py --fetch        # 获取未处理邮件
    python process_email.py --reply <uid> <content>  # 回复邮件

配置文件: config.json (同目录下)
"""

import json
import os
import sys
import argparse
import email
import imaplib
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from pathlib import Path

# 默认配置文件路径
CONFIG_FILE = Path(__file__).parent / "config.json"
PROCESSED_FILE = Path(__file__).parent.parent / "memory" / "processed_emails.json"


def load_config():
    """加载配置文件"""
    if not CONFIG_FILE.exists():
        print(f"错误: 配置文件 {CONFIG_FILE} 不存在", file=sys.stderr)
        print("请创建 config.json 文件，格式如下:", file=sys.stderr)
        print(json.dumps({
            "email": "your_email@qq.com",
            "password": "your_auth_code",
            "imap_host": "imap.qq.com",
            "imap_port": 993,
            "smtp_host": "smtp.qq.com",
            "smtp_port": 465,
            "whitelist_sender": "sender@qq.com"
        }, indent=2, ensure_ascii=False))
        sys.exit(1)
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_processed_uids():
    """加载已处理邮件UID列表"""
    if PROCESSED_FILE.exists():
        with open(PROCESSED_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content:
                return json.loads(content)
    return []


def save_processed_uids(uids):
    """保存已处理邮件UID列表"""
    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PROCESSED_FILE, 'w', encoding='utf-8') as f:
        json.dump(uids, f, ensure_ascii=False)


def connect_imap(config):
    """连接IMAP服务器"""
    mail = imaplib.IMAP4_SSL(config['imap_host'], config['imap_port'])
    mail.login(config['email'], config['password'])
    return mail


def fetch_unprocessed_emails(config):
    """获取未处理的指令邮件"""
    mail = connect_imap(config)
    mail.select('INBOX')
    
    # 获取最近50封邮件
    _, messages = mail.search(None, 'ALL')
    email_ids = messages[0].split()[-50:][::-1]  # 取最后50封，反转顺序（最新在前）
    
    processed_uids = load_processed_uids()
    unprocessed = []
    
    for email_id in email_ids:
        try:
            _, msg_data = mail.fetch(email_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            
            # 获取发件人
            from_header = email.utils.parseaddr(msg.get('From'))
            sender = from_header[1].lower()
            
            # 检查是否在白名单
            whitelist = config.get('whitelist_sender', '').lower()
            if whitelist and sender != whitelist:
                continue
            
            # 获取UID
            uid = email_id.decode() if isinstance(email_id, bytes) else str(email_id)
            
            # 检查是否已处理
            if uid in processed_uids:
                continue
            
            # 获取邮件主题和内容
            subject = msg.get('Subject', '无主题')
            
            # 获取邮件正文
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        try:
                            body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                            break
                        except:
                            pass
            else:
                try:
                    body = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8')
                except:
                    body = msg.get_payload() or ""
            
            # 清理邮件内容
            body = body.strip()
            
            unprocessed.append({
                'uid': uid,
                'subject': subject,
                'from': sender,
                'body': body
            })
            
        except Exception as e:
            print(f"警告: 解析邮件 {email_id} 失败: {e}", file=sys.stderr)
            continue
    
    mail.logout()
    return unprocessed


def reply_email(config, original_subject, reply_content):
    """回复邮件"""
    msg = MIMEText(reply_content, 'plain', 'utf-8')
    msg['Subject'] = f"Re: {original_subject}"
    msg['From'] = config['email']
    msg['To'] = config['whitelist_sender']
    
    smtp = smtplib.SMTP_SSL(config['smtp_host'], config['smtp_port'])
    smtp.login(config['email'], config['password'])
    smtp.sendmail(config['email'], [config['whitelist_sender']], msg.as_string())
    smtp.quit()


def mark_as_processed(uid):
    """标记邮件为已处理"""
    uids = load_processed_uids()
    if uid not in uids:
        uids.append(uid)
        save_processed_uids(uids)


def cmd_fetch(args):
    """获取未处理邮件"""
    config = load_config()
    emails = fetch_unprocessed_emails(config)
    
    if not emails:
        print("没有未处理的指令邮件")
        return
    
    print(f"找到 {len(emails)} 封未处理邮件:")
    for i, email_data in enumerate(emails, 1):
        print(f"\n--- 邮件 {i} ---")
        print(f"UID: {email_data['uid']}")
        print(f"主题: {email_data['subject']}")
        print(f"内容: {email_data['body'][:200]}...")


def cmd_reply(args):
    """回复邮件"""
    config = load_config()
    
    # 读取回复内容
    if args.content_file:
        with open(args.content_file, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = args.content
    
    # 获取原始邮件信息
    mail = connect_imap(config)
    mail.select('INBOX')
    
    # 获取原始邮件主题
    _, messages = mail.search(None, 'ALL')
    email_ids = messages[0].split()
    
    original_subject = "Re: 指令执行结果"
    for email_id in email_ids:
        if email_id.decode() == args.uid or str(email_id) == args.uid:
            _, msg_data = mail.fetch(email_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            original_subject = msg.get('Subject', 'Re: 指令执行结果')
            break
    
    mail.logout()
    
    # 发送回复
    try:
        reply_email(config, original_subject, content)
        mark_as_processed(args.uid)
        print(f"回复成功！已标记 UID {args.uid} 为已处理")
    except Exception as e:
        print(f"回复失败: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_mark(args):
    """标记邮件为已处理"""
    mark_as_processed(args.uid)
    print(f"已标记 UID {args.uid} 为已处理")


def main():
    parser = argparse.ArgumentParser(description='邮件指令处理器')
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # fetch 子命令
    fetch_parser = subparsers.add_parser('fetch', help='获取未处理邮件')
    
    # reply 子命令
    reply_parser = subparsers.add_parser('reply', help='回复邮件')
    reply_parser.add_argument('uid', help='原邮件UID')
    reply_parser.add_argument('content', nargs='?', help='回复内容')
    reply_parser.add_argument('--file', dest='content_file', help='从文件读取回复内容')
    
    # mark 子命令
    mark_parser = subparsers.add_parser('mark', help='标记邮件为已处理')
    mark_parser.add_argument('uid', help='邮件UID')
    
    args = parser.parse_args()
    
    if args.command == 'fetch':
        cmd_fetch(args)
    elif args.command == 'reply':
        cmd_reply(args)
    elif args.command == 'mark':
        cmd_mark(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
