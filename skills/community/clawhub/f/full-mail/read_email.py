#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
接收邮件 - IMAP 协议
用法：
  python3 read_email.py list [数量]     - 查看收件箱邮件列表
  python3 read_email.py read [序号]     - 查看指定邮件内容
  python3 read_email.py search [关键词]  - 搜索邮件
  python3 read_email.py attachments [序号] - 下载附件
  python3 read_email.py markread [序号]  - 标记已读
  python3 read_email.py delete [序号]    - 删除邮件
"""

import sys
import os
import imaplib
import email
from email.header import decode_header
from datetime import datetime

def get_env():
    """从环境变量获取配置"""
    return {
        'imap_server': os.environ.get('EMAIL_IMAP_SERVER', ''),
        'imap_port': int(os.environ.get('EMAIL_IMAP_PORT', '993')),
        'email_user': os.environ.get('EMAIL_USER', ''),
        'email_password': os.environ.get('EMAIL_PASSWORD', '')
    }

def decode_mime_words(s):
    """解码 MIME 编码的字符串"""
    if not s:
        return ''
    decoded = []
    for word, encoding in decode_header(s):
        if isinstance(word, bytes):
            try:
                decoded.append(word.decode(encoding or 'utf-8', errors='ignore'))
            except:
                decoded.append(word.decode('utf-8', errors='ignore'))
        else:
            decoded.append(word)
    return ''.join(decoded)

def get_email_body(msg):
    """获取邮件正文"""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    charset = part.get_content_charset() or 'utf-8'
                    body = part.get_payload(decode=True).decode(charset, errors='ignore')
                    break
                except:
                    pass
            elif content_type == "text/html" and not body:
                try:
                    charset = part.get_content_charset() or 'utf-8'
                    body = part.get_payload(decode=True).decode(charset, errors='ignore')
                except:
                    pass
    else:
        try:
            charset = msg.get_content_charset() or 'utf-8'
            body = msg.get_payload(decode=True).decode(charset, errors='ignore')
        except:
            body = msg.get_payload()
    return body

def list_emails(imap, num=10):
    """列出收件箱邮件"""
    try:
        imap.select('INBOX')
        status, messages = imap.search(None, 'ALL')
        if status != 'OK':
            print("❌ 获取邮件列表失败")
            return
        
        email_ids = messages[0].split()
        if not email_ids:
            print("📭 收件箱为空")
            return
        
        # 获取最新的 num 封邮件
        latest_ids = email_ids[-num:]
        print(f"📬 收件箱最新 {len(latest_ids)} 封邮件：\n")
        print(f"{'序号':<6} {'发件人':<30} {'主题':<40} {'日期':<20}")
        print("-" * 100)
        
        for i, eid in enumerate(reversed(latest_ids)):
            status, msg_data = imap.fetch(eid, '(RFC822.HEADER)')
            if status == 'OK':
                msg = email.message_from_bytes(msg_data[0][1])
                subject = decode_mime_words(msg.get('Subject', '无主题'))
                from_addr = decode_mime_words(msg.get('From', '未知'))
                date_str = msg.get('Date', '')
                try:
                    parsed_date = email.utils.parsedate_to_datetime(date_str)
                    date_display = parsed_date.strftime('%Y-%m-%d %H:%M')
                except:
                    date_display = date_str[:20] if date_str else '未知'
                
                # 截断过长的主题和发件人
                subject = subject[:38] + '...' if len(subject) > 40 else subject
                from_addr = from_addr[:28] + '...' if len(from_addr) > 30 else from_addr
                
                print(f"{len(latest_ids)-i:<6} {from_addr:<30} {subject:<40} {date_display:<20}")
        
        print("\n💡 提示：使用 'read [序号]' 查看邮件详情")
        
    except Exception as e:
        print(f"❌ 错误：{e}")

def read_email(imap, seq_num):
    """读取指定邮件"""
    try:
        imap.select('INBOX')
        status, messages = imap.search(None, 'ALL')
        if status != 'OK':
            print("❌ 获取邮件失败")
            return
        
        email_ids = messages[0].split()
        if not email_ids:
            print("📭 收件箱为空")
            return
        
        if seq_num < 1 or seq_num > len(email_ids):
            print(f"❌ 序号超出范围 (1-{len(email_ids)})")
            return
        
        eid = email_ids[-seq_num]
        status, msg_data = imap.fetch(eid, '(RFC822)')
        if status != 'OK':
            print("❌ 获取邮件内容失败")
            return
        
        msg = email.message_from_bytes(msg_data[0][1])
        
        subject = decode_mime_words(msg.get('Subject', '无主题'))
        from_addr = decode_mime_words(msg.get('From', '未知'))
        to_addr = decode_mime_words(msg.get('To', '未知'))
        date_str = msg.get('Date', '')
        
        print("=" * 80)
        print(f"📧 邮件详情")
        print("=" * 80)
        print(f"发件人：{from_addr}")
        print(f"收件人：{to_addr}")
        print(f"主  题：{subject}")
        print(f"日  期：{date_str}")
        print("-" * 80)
        print("📄 正文：")
        print(get_email_body(msg))
        print("=" * 80)
        
        # 检查附件
        attachments = []
        if msg.is_multipart():
            for part in msg.walk():
                content_disposition = str(part.get("Content-Disposition"))
                if "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        attachments.append(decode_mime_words(filename))
        
        if attachments:
            print(f"\n📎 附件：{', '.join(attachments)}")
            print("💡 提示：使用 'attachments [序号]' 下载附件")
        
    except Exception as e:
        print(f"❌ 错误：{e}")

def search_emails(imap, keyword):
    """搜索邮件"""
    try:
        imap.select('INBOX')
        # 搜索主题或正文中包含关键词的邮件
        search_criteria = f'(BODY "{keyword}")'
        status, messages = imap.search(None, search_criteria)
        if status != 'OK':
            print("❌ 搜索失败")
            return
        
        email_ids = messages[0].split()
        if not email_ids:
            print(f"📭 未找到包含 \"{keyword}\" 的邮件")
            return
        
        print(f"✅ 找到 {len(email_ids)} 封包含 \"{keyword}\" 的邮件：\n")
        
        for i, eid in enumerate(reversed(email_ids[-10:])):
            status, msg_data = imap.fetch(eid, '(RFC822.HEADER)')
            if status == 'OK':
                msg = email.message_from_bytes(msg_data[0][1])
                subject = decode_mime_words(msg.get('Subject', '无主题'))
                from_addr = decode_mime_words(msg.get('From', '未知'))
                print(f"{i+1}. [{from_addr}] {subject}")
        
    except Exception as e:
        print(f"❌ 错误：{e}")

def download_attachments(imap, seq_num):
    """下载附件"""
    try:
        imap.select('INBOX')
        status, messages = imap.search(None, 'ALL')
        email_ids = messages[0].split()
        
        if seq_num < 1 or seq_num > len(email_ids):
            print(f"❌ 序号超出范围")
            return
        
        eid = email_ids[-seq_num]
        status, msg_data = imap.fetch(eid, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        
        save_dir = os.path.expanduser('~/Downloads/email_attachments')
        os.makedirs(save_dir, exist_ok=True)
        
        downloaded = 0
        if msg.is_multipart():
            for part in msg.walk():
                content_disposition = str(part.get("Content-Disposition"))
                if "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        filename = decode_mime_words(filename)
                        filepath = os.path.join(save_dir, filename)
                        with open(filepath, 'wb') as f:
                            f.write(part.get_payload(decode=True))
                        print(f"✅ 已下载：{filepath}")
                        downloaded += 1
        
        if downloaded == 0:
            print("📭 该邮件没有附件")
        else:
            print(f"\n📂 附件保存位置：{save_dir}")
        
    except Exception as e:
        print(f"❌ 错误：{e}")

def mark_as_read(imap, seq_num):
    """标记为已读"""
    try:
        imap.select('INBOX')
        status, messages = imap.search(None, 'ALL')
        email_ids = messages[0].split()
        
        if seq_num < 1 or seq_num > len(email_ids):
            print(f"❌ 序号超出范围")
            return
        
        eid = email_ids[-seq_num]
        imap.store(eid, '+FLAGS', '\\Seen')
        print("✅ 已标记为已读")
        
    except Exception as e:
        print(f"❌ 错误：{e}")

def delete_email(imap, seq_num):
    """删除邮件"""
    try:
        imap.select('INBOX')
        status, messages = imap.search(None, 'ALL')
        email_ids = messages[0].split()
        
        if seq_num < 1 or seq_num > len(email_ids):
            print(f"❌ 序号超出范围")
            return
        
        eid = email_ids[-seq_num]
        imap.store(eid, '+FLAGS', '\\Deleted')
        imap.expunge()
        print("✅ 已删除")
        
    except Exception as e:
        print(f"❌ 错误：{e}")

if __name__ == '__main__':
    config = get_env()
    
    if not config['imap_server']:
        print("❌ 错误：EMAIL_IMAP_SERVER 未配置")
        sys.exit(1)
    if not config['email_user']:
        print("❌ 错误：EMAIL_USER 未配置")
        sys.exit(1)
    if not config['email_password']:
        print("❌ 错误：EMAIL_PASSWORD 未配置")
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 read_email.py list [数量]     - 查看收件箱邮件列表")
        print("  python3 read_email.py read [序号]     - 查看指定邮件内容")
        print("  python3 read_email.py search [关键词]  - 搜索邮件")
        print("  python3 read_email.py attachments [序号] - 下载附件")
        print("  python3 read_email.py markread [序号]  - 标记已读")
        print("  python3 read_email.py delete [序号]    - 删除邮件")
        sys.exit(1)
    
    command = sys.argv[1]
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        imap = imaplib.IMAP4_SSL(config['imap_server'], config['imap_port'])
        imap.login(config['email_user'], config['email_password'])
        print(f"✅ 已连接到邮箱：{config['email_user']}")
        print()
        
        if command == 'list':
            num = int(arg) if arg else 10
            list_emails(imap, num)
        elif command == 'read':
            if not arg:
                print("❌ 请提供邮件序号")
                sys.exit(1)
            read_email(imap, int(arg))
        elif command == 'search':
            if not arg:
                print("❌ 请提供搜索关键词")
                sys.exit(1)
            search_emails(imap, arg)
        elif command == 'attachments':
            if not arg:
                print("❌ 请提供邮件序号")
                sys.exit(1)
            download_attachments(imap, int(arg))
        elif command == 'markread':
            if not arg:
                print("❌ 请提供邮件序号")
                sys.exit(1)
            mark_as_read(imap, int(arg))
        elif command == 'delete':
            if not arg:
                print("❌ 请提供邮件序号")
                sys.exit(1)
            delete_email(imap, int(arg))
        else:
            print(f"❌ 未知命令：{command}")
        
        imap.close()
        imap.logout()
        
    except imaplib.IMAP4.error as e:
        print(f"❌ IMAP 错误：{e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误：{e}")
        sys.exit(1)
