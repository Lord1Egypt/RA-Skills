#!/usr/bin/env python3
"""读取邮件脚本。直接执行即可，无需修改。"""
import imaplib, email, email.header, sys

def read_inbox(user: str = 'xxx@example.com', password: str = 'yourpassword', limit: int = 5):
    m = imaplib.IMAP4('localhost', 1143)
    m.login(user, password)
    m.select('INBOX')
    _, msgs = m.search(None, 'ALL')
    for num in msgs[0].split()[-limit:]:
        _, data = m.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
        # 解码 subject
        subject = email.header.make_header(email.header.decode_header(msg['Subject'] or ''))
        sender = email.header.make_header(email.header.decode_header(msg['From'] or ''))
        print(f"From: {sender} | Subject: {subject}")
    m.logout()

if __name__ == '__main__':
    user = sys.argv[1] if len(sys.argv) > 1 else 'xxx@example.com'
    password = sys.argv[2] if len(sys.argv) > 2 else 'yourpassword'
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    read_inbox(user, password, limit)
