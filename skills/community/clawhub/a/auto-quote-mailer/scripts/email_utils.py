"""
Email utility functions
Handle email connection, fetching, content extraction
邮件工具函数
处理邮件连接、收取、内容提取
"""

import imaplib
import email
from email.header import decode_header
import os
import re
import datetime
import sys

# Add config directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config'))
import config

def connect_to_imap():
    """Connect to IMAP server"""
    conf = config.IMAP_CONFIG
    if conf['use_ssl']:
        conn = imaplib.IMAP4_SSL(conf['server'], conf['port'])
    else:
        conn = imaplib.IMAP4(conf['server'], conf['port'])
    
    # Send IMAP ID information (fixes NetEase 163 "Unsafe Login" issue)
    # 需要标识客户端信息才能通过网易安全检查
    try:
        conn._command('ID', '("name" "email-quote-automation" "version" "1.0.0" "vendor" "github" "support-email" "admin@example.com")')
        conn.readline()  # consume response
    except Exception:
        # some servers don't support ID, ignore
        pass
    
    conn.login(conf['username'], conf['password'])
    return conn

def extract_text_from_email(msg):
    """Extract plain text content from email object"""
    text_content = ""
    html_content = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            # Skip attachments / 跳过附件
            if "attachment" in content_disposition:
                continue

            if content_type == "text/plain":
                charset = part.get_content_charset()
                if charset:
                    try:
                        text_content += part.get_payload(decode=True).decode(charset)
                    except:
                        text_content += part.get_payload(decode=True).decode('utf-8', errors='replace')
                else:
                    text_content += part.get_payload()
            elif content_type == "text/html":
                charset = part.get_content_charset()
                if charset:
                    try:
                        html_content += part.get_payload(decode=True).decode(charset)
                    except:
                        html_content += part.get_payload(decode=True).decode('utf-8', errors='replace')
                else:
                    html_content += part.get_payload()
    else:
        content_type = msg.get_content_type()
        charset = msg.get_content_charset()
        if content_type == "text/plain":
            if charset:
                text_content = msg.get_payload(decode=True).decode(charset)
            else:
                text_content = msg.get_payload()

    # If no plain text but has HTML, simple extract text
    # 如果没有纯文本但有HTML，简单提取文本
    if not text_content and html_content:
        text_content = re.sub(r'<[^>]+>', '', html_content)
        text_content = re.sub(r'\s+', ' ', text_content).strip()

    return text_content

def decode_header_value(header):
    """Decode email header"""
    if header is None:
        return ""
    decoded, charset = decode_header(header)[0]
    if charset:
        try:
            return decoded.decode(charset)
        except:
            return str(decoded)
    else:
        if isinstance(decoded, bytes):
            return decoded.decode('utf-8', errors='replace')
        return decoded

def get_new_unread_messages(conn):
    """Get all unread messages"""
    status, _ = conn.select('INBOX')
    if status != 'OK':
        return []

    status, messages = conn.search(None, 'UNSEEN')
    if status != 'OK':
        return []

    msg_nums = messages[0].split()
    messages_list = []

    for num in msg_nums:
        status, msg_data = conn.fetch(num, '(RFC822)')
        if status != 'OK':
            continue
        msg = email.message_from_bytes(msg_data[0][1])

        # Parse headers
        subject = decode_header_value(msg['Subject'])
        from_ = decode_header_value(msg['From'])
        date_ = decode_header_value(msg['Date'])

        # Extract text content
        body = extract_text_from_email(msg)

        messages_list.append({
            'uid': num.decode(),
            'subject': subject,
            'from': from_,
            'date': date_,
            'body': body,
            'raw_msg': msg,
            'raw_bytes': msg_data[0][1],
        })

    return messages_list

def mark_as_read(conn, msg_uid):
    """Mark email as read"""
    conn.select('INBOX')
    conn.store(msg_uid.encode(), '+FLAGS', '\\Seen')

def ensure_storage_directories():
    """Ensure storage directories exist"""
    conf = config.STORAGE_CONFIG
    base = conf['base_path']
    for folder in [conf['raw_folder'], conf['text_folder'], conf['translated_folder'], conf['quotes_folder']]:
        path = os.path.join(base, folder)
        os.makedirs(path, exist_ok=True)

def generate_filename(prefix=""):
    """Generate filename with timestamp"""
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y%m%d_%H%M%S')
    if prefix:
        return f"{prefix}_{timestamp}"
    return timestamp

def save_raw_email(filename, raw_bytes):
    """Save raw email"""
    path = os.path.join(config.STORAGE_CONFIG['base_path'], config.STORAGE_CONFIG['raw_folder'], filename + '.eml')
    with open(path, 'wb') as f:
        f.write(raw_bytes)
    return path

def save_text_content(filename, text, is_translated=False):
    """Save text content"""
    if is_translated:
        folder = config.STORAGE_CONFIG['translated_folder']
    else:
        folder = config.STORAGE_CONFIG['text_folder']
    path = os.path.join(config.STORAGE_CONFIG['base_path'], folder, filename + '.txt')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    return path

def save_quote(filename, quote_text):
    """Save generated quotation"""
    path = os.path.join(config.STORAGE_CONFIG['base_path'], config.STORAGE_CONFIG['quotes_folder'], filename + '.txt')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(quote_text)
    return path
