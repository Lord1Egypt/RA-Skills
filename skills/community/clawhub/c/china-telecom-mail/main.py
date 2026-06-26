#!/usr/bin/env python3
"""
China Telecom Mail Skill - Send and receive emails via China Telecom.

Usage:
    # Receive
    python main.py list-today          # List today's emails with summaries
    python main.py read <email_id>     # Read a specific email
    python main.py json-summary        # Output as JSON
    python main.py count               # Count today's emails
    
    # Send
    python main.py send --to <email> --subject <sub> --body <msg>
    python main.py send --to <email> --subject <sub> --body <msg> --attachment <file>
    python main.py forward --email-id <id> --to <email>
    python main.py interactive

Configuration:
    Edit config.toml in the skill directory
"""

import poplib
import smtplib
import email
from email.header import decode_header, Header
from email.utils import parsedate_to_datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import sys
import re
import os
import tomllib
import io

# Fix output encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Default configuration
DEFAULT_CONFIG = {
    'pop_server': 'pop.chinatelecom.cn',
    'pop_port': 995,
    'pop_user': 'zhanggh5@chinatelecom.cn',
    'pop_pass': '填写密码',
    'smtp_server': 'smtp.chinatelecom.cn',
    'smtp_port': 465,
    'smtp_user': 'zhanggh5@chinatelecom.cn',
    'smtp_pass': '填写密码',
}


def load_config():
    """Load configuration from config.toml."""
    config = DEFAULT_CONFIG.copy()
    
    config_path = os.path.join(os.path.dirname(__file__), 'config.toml')
    if os.path.exists(config_path):
        with open(config_path, 'rb') as f:
            toml_config = tomllib.load(f)
            if 'email' in toml_config:
                config['pop_server'] = toml_config['email'].get('server', config['pop_server'])
                config['pop_port'] = toml_config['email'].get('port', config['pop_port'])
                config['pop_user'] = toml_config['email'].get('username', config['pop_user'])
                config['pop_pass'] = toml_config['email'].get('password', config['pop_pass'])
            if 'smtp' in toml_config:
                config['smtp_server'] = toml_config['smtp'].get('server', config['smtp_server'])
                config['smtp_port'] = toml_config['smtp'].get('port', config['smtp_port'])
                config['smtp_user'] = toml_config['smtp'].get('username', config['smtp_user'])
                config['smtp_pass'] = toml_config['smtp'].get('password', config['smtp_pass'])
    
    return config


def decode_mime_header(header_value):
    """Decode MIME-encoded header values."""
    if not header_value:
        return ""
    decoded_parts = []
    for part, encoding in decode_header(header_value):
        if isinstance(part, bytes):
            try:
                decoded_parts.append(part.decode(encoding or 'utf-8'))
            except:
                decoded_parts.append(part.decode('utf-8', errors='ignore'))
        else:
            decoded_parts.append(str(part))
    return ''.join(decoded_parts)


def extract_text_from_html(html_content):
    """Extract plain text from HTML content."""
    if not html_content:
        return ""
    text = re.sub(r'<[^<]+?>', '', html_content)
    text = re.sub(r'\s+', ' ', text)
    entities = {'&nbsp;': ' ', '&lt;': '<', '&gt;': '>', '&amp;': '&', '&quot;': '"', '&#39;': "'"}
    for e, c in entities.items():
        text = text.replace(e, c)
    return text.strip()


def get_email_body(msg):
    """Extract email body text."""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            cd = str(part.get('Content-Disposition'))
            if 'attachment' not in cd:
                if ct == 'text/plain':
                    try:
                        body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='ignore')
                    except:
                        try:
                            body = part.get_payload(decode=True).decode('gbk', errors='ignore')
                        except:
                            pass
                    break
                elif ct == 'text/html' and not body:
                    try:
                        body = extract_text_from_html(part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='ignore'))
                    except:
                        pass
    else:
        ct = msg.get_content_type()
        if ct in ['text/plain', 'text/html']:
            try:
                content = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8', errors='ignore')
                body = extract_text_from_html(content) if ct == 'text/html' else content
            except:
                pass
    return body


def summarize_email(msg, max_length=500):
    """Generate a summary of the email."""
    return {
        'from': decode_mime_header(msg['From']),
        'subject': decode_mime_header(msg['Subject']),
        'date': msg['Date'] or '',
        'body': get_email_body(msg)[:max_length],
        'preview': get_email_body(msg)[:200]
    }


def connect_pop(config):
    """Connect to POP3 server."""
    print('Connecting to POP3 server...', file=sys.stderr)
    mail = poplib.POP3_SSL(config['pop_server'], config['pop_port'])
    mail.user(config['pop_user'])
    mail.pass_(config['pop_pass'])
    num = len(mail.list()[1])
    print(f'Connected! Total messages: {num}', file=sys.stderr)
    
    emails = []
    for i in range(1, num + 1):
        try:
            typ, lines, octets = mail.retr(i)
            msg = email.message_from_string(b'\r\n'.join(lines).decode('utf-8', errors='ignore'))
            emails.append({'id': i, 'msg': msg})
        except Exception as e:
            print(f'Error reading email {i}: {e}', file=sys.stderr)
    mail.quit()
    return emails


def connect_smtp(config):
    """Connect to SMTP server."""
    print('Connecting to SMTP server...', file=sys.stderr)
    server = smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port'], timeout=30)
    print('SMTP connected!', file=sys.stderr)
    server.login(config['smtp_user'], config['smtp_pass'])
    print('Login successful!', file=sys.stderr)
    return server


def list_today_emails():
    """List today's emails."""
    config = load_config()
    emails = connect_pop(config)
    today = datetime.now().date()
    
    today_list = []
    for em in emails:
        try:
            if parsedate_to_datetime(em['msg']['Date']).date() == today:
                s = summarize_email(em['msg'])
                s['id'] = em['id']
                today_list.append(s)
        except:
            pass
    
    print('')
    print('='*60)
    print(f"Today received emails: {len(today_list)}")
    print('='*60)
    
    for i, e in enumerate(today_list, 1):
        print('')
        print(f'Email {i} (ID: {e["id"]}):')
        print(f'  From: {e["from"]}')
        print(f'  Subject: {e["subject"]}')
        print(f'  Date: {e["date"]}')
        print(f'  Preview: {e["preview"]}')
        print('-'*60)
    
    return today_list


def read_email(email_id):
    """Read a specific email."""
    config = load_config()
    emails = connect_pop(config)
    
    if email_id < 1 or email_id > len(emails):
        print(f'Error: Email ID {email_id} not found', file=sys.stderr)
        sys.exit(1)
    
    s = summarize_email(emails[email_id - 1]['msg'], max_length=3000)
    
    print('')
    print('='*60)
    print(f'Email ID: {email_id}')
    print('='*60)
    print('')
    print(f'From: {s["from"]}')
    print(f'Subject: {s["subject"]}')
    print(f'Date: {s["date"]}')
    print('')
    print('Body:')
    print('-'*60)
    print(s['body'])
    print('-'*60)


def send_email(config, to_addr, subject, body, attachment=None):
    """Send an email."""
    try:
        server = connect_smtp(config)
        msg = MIMEMultipart()
        msg['From'] = config['smtp_user']
        msg['To'] = to_addr
        msg['Subject'] = Header(subject, 'utf-8')
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        if attachment and os.path.exists(attachment):
            filename = os.path.basename(attachment)
            with open(attachment, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                msg.attach(part)
            print(f'Attachment: {filename}', file=sys.stderr)
        
        server.send_message(msg)
        print(f'Email sent to {to_addr}!', file=sys.stderr)
        server.quit()
        return True
    except Exception as e:
        print(f'Failed: {e}', file=sys.stderr)
        return False


def forward_email(config, email_id, to_addr):
    """Forward an email."""
    try:
        emails = connect_pop(config)
        if email_id < 1 or email_id > len(emails):
            print(f'Error: Email ID {email_id} not found', file=sys.stderr)
            return False
        
        orig = emails[email_id - 1]['msg']
        orig_from = decode_mime_header(orig['From'])
        orig_subj = decode_mime_header(orig['Subject'])
        orig_date = orig['Date'] or ''
        body = get_email_body(orig)
        
        server = connect_smtp(config)
        msg = MIMEMultipart()
        msg['From'] = config['smtp_user']
        msg['To'] = to_addr
        msg['Subject'] = Header(f'Fwd: {orig_subj}', 'utf-8')
        
        info = f'\n-------- Forwarded Message --------\nFrom: {orig_from}\nDate: {orig_date}\nSubject: {orig_subj}\nTo: {config["smtp_user"]}\n\n'
        msg.attach(MIMEText(info + body, 'plain', 'utf-8'))
        
        server.send_message(msg)
        print(f'Email forwarded to {to_addr}!', file=sys.stderr)
        server.quit()
        return True
    except Exception as e:
        print(f'Failed: {e}', file=sys.stderr)
        return False


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    config = load_config()
    cmd = sys.argv[1]
    
    if cmd == 'list-today':
        list_today_emails()
    elif cmd == 'read' and len(sys.argv) >= 3:
        read_email(int(sys.argv[2]))
    elif cmd == 'json-summary':
        import json
        emails = connect_pop(config)
        today = datetime.now().date()
        today_list = []
        for em in emails:
            try:
                if parsedate_to_datetime(em['msg']['Date']).date() == today:
                    s = summarize_email(em['msg'])
                    s['id'] = em['id']
                    today_list.append(s)
            except:
                pass
        print(json.dumps({'date': str(today), 'count': len(today_list), 'emails': today_list}, ensure_ascii=False, indent=2))
    elif cmd == 'count':
        emails = connect_pop(config)
        today = datetime.now().date()
        count = sum(1 for em in emails if parsedate_to_datetime(em['msg']['Date']).date() == today)
        print(f"Today's emails: {count}")
    elif cmd == 'send':
        args = sys.argv[2:]
        to_addr = subject = body = attachment = None
        i = 0
        while i < len(args):
            if args[i] == '--to' and i + 1 < len(args):
                to_addr = args[i + 1]; i += 2
            elif args[i] == '--subject' and i + 1 < len(args):
                subject = args[i + 1]; i += 2
            elif args[i] == '--body' and i + 1 < len(args):
                body = args[i + 1]; i += 2
            elif args[i] == '--attachment' and i + 1 < len(args):
                attachment = args[i + 1]; i += 2
            else:
                i += 1
        if not to_addr or not subject or not body:
            print('Error: --to, --subject, --body required', file=sys.stderr)
            sys.exit(1)
        send_email(config, to_addr, subject, body, attachment)
    elif cmd == 'forward':
        args = sys.argv[2:]
        email_id = to_addr = None
        i = 0
        while i < len(args):
            if args[i] == '--email-id' and i + 1 < len(args):
                email_id = int(args[i + 1]); i += 2
            elif args[i] == '--to' and i + 1 < len(args):
                to_addr = args[i + 1]; i += 2
            else:
                i += 1
        if not email_id or not to_addr:
            print('Error: --email-id and --to required', file=sys.stderr)
            sys.exit(1)
        forward_email(config, email_id, to_addr)
    else:
        print(f'Unknown command: {cmd}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
