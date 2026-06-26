#!/usr/bin/env python3
"""Emailbox - Receive/search/forward emails via IMAP with 12+ provider support.

Supports: list inbox, read email, search emails, download attachments, forward.
Uses only Python standard library (imaplib, email).

Usage:
  python3 receive_mail.py --list [--count 10]
  python3 receive_mail.py --read UID
  python3 receive_mail.py --forward UID [--save-dir DIR]
  python3 receive_mail.py --search "keyword" [--from-filter ...] [--since ...]
  python3 receive_mail.py --download-attachment UID [--save-dir DIR]
"""

import argparse
import email
import imaplib
import os
import re
import sys
from email.header import decode_header
from pathlib import Path

PROVIDERS = {
    "qq.com": {"imap_server": "imap.qq.com", "imap_port": 993, "smtp_server": "smtp.qq.com", "smtp_port": 465, "use_ssl": True, "env_user": "EMAIL_QQ", "env_auth": "EMAIL_QQ_AUTH"},
    "163.com": {"imap_server": "imap.163.com", "imap_port": 993, "smtp_server": "smtp.163.com", "smtp_port": 465, "use_ssl": True, "env_user": "EMAIL_163", "env_auth": "EMAIL_163_AUTH"},
    "126.com": {"imap_server": "imap.126.com", "imap_port": 993, "smtp_server": "smtp.126.com", "smtp_port": 465, "use_ssl": True, "env_user": "EMAIL_126", "env_auth": "EMAIL_126_AUTH"},
    "sina.com": {"imap_server": "imap.sina.com", "imap_port": 993, "smtp_server": "smtp.sina.com", "smtp_port": 465, "use_ssl": True, "env_user": "EMAIL_SINA", "env_auth": "EMAIL_SINA_AUTH"},
    "outlook.com": {"imap_server": "outlook.office365.com", "imap_port": 993, "smtp_server": "smtp.office365.com", "smtp_port": 587, "use_ssl": False, "env_user": "EMAIL_OUTLOOK", "env_auth": "EMAIL_OUTLOOK_AUTH"},
    "hotmail.com": {"imap_server": "outlook.office365.com", "imap_port": 993, "smtp_server": "smtp.office365.com", "smtp_port": 587, "use_ssl": False, "env_user": "EMAIL_OUTLOOK", "env_auth": "EMAIL_OUTLOOK_AUTH"},
    "gmail.com": {"imap_server": "imap.gmail.com", "imap_port": 993, "smtp_server": "smtp.gmail.com", "smtp_port": 587, "use_ssl": False, "env_user": "EMAIL_GMAIL", "env_auth": "EMAIL_GMAIL_AUTH"},
    "yahoo.com": {"imap_server": "imap.mail.yahoo.com", "imap_port": 993, "smtp_server": "smtp.mail.yahoo.com", "smtp_port": 587, "use_ssl": False, "env_user": "EMAIL_YAHOO", "env_auth": "EMAIL_YAHOO_AUTH"},
    "icloud.com": {"imap_server": "imap.mail.me.com", "imap_port": 993, "smtp_server": "smtp.mail.me.com", "smtp_port": 587, "use_ssl": False, "env_user": "EMAIL_ICLOUD", "env_auth": "EMAIL_ICLOUD_AUTH"},
    "exmail.qq.com": {"imap_server": "imap.exmail.qq.com", "imap_port": 993, "smtp_server": "smtp.exmail.qq.com", "smtp_port": 465, "use_ssl": True, "env_user": "EMAIL_EXMAIL", "env_auth": "EMAIL_EXMAIL_AUTH"},
    "mxhichina.com": {"imap_server": "imap.mxhichina.com", "imap_port": 993, "smtp_server": "smtp.mxhichina.com", "smtp_port": 465, "use_ssl": True, "env_user": "EMAIL_ALIMAIL", "env_auth": "EMAIL_ALIMAIL_AUTH"},
    "hicloud.com": {"imap_server": "imap.mail.hicloud.com", "imap_port": 993, "smtp_server": "smtp.mail.hicloud.com", "smtp_port": 465, "use_ssl": True, "env_user": "EMAIL_HUAWEI", "env_auth": "EMAIL_HUAWEI_AUTH"},
    "139.com": {"imap_server": "imap.mail.139.com", "imap_port": 993, "smtp_server": "smtp.mail.139.com", "smtp_port": 465, "use_ssl": True, "env_user": "EMAIL_139", "env_auth": "EMAIL_139_AUTH"},
}

PROVIDER_ALIASES = {
    "hotmail.com": "outlook.com", "live.com": "outlook.com",
    "foxmail.com": "qq.com", "vip.qq.com": "qq.com",
    "vip.163.com": "163.com", "vip.126.com": "126.com", "yeah.net": "163.com",
    "sina.cn": "sina.com", "yahoo.co.jp": "yahoo.com", "yahoo.cn": "yahoo.com",
    "me.com": "icloud.com", "mac.com": "icloud.com",
}


def decode_mime_header(value):
    if not value:
        return ""
    decoded_parts = decode_header(value)
    result = []
    for part, charset in decoded_parts:
        if isinstance(part, bytes):
            try:
                result.append(part.decode(charset or "utf-8", errors="replace"))
            except (LookupError, UnicodeDecodeError):
                result.append(part.decode("utf-8", errors="replace"))
        else:
            result.append(part)
    return "".join(result)


def strip_html(html_content):
    text = re.sub(r"<style[^>]*>.*?</style>", "", html_content, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</p>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</div>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</tr>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</li>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"&quot;", '"', text)
    text = re.sub(r"&#\d+;", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def get_text_from_message(msg):
    body_text = None
    body_html = None
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition", ""))
            if "attachment" in content_disposition:
                continue
            if content_type == "text/plain" and body_text is None:
                charset = part.get_content_charset() or "utf-8"
                try:
                    payload = part.get_payload(decode=True)
                    body_text = payload.decode(charset, errors="replace")
                except Exception:
                    body_text = payload.decode("utf-8", errors="replace") if payload else ""
            elif content_type == "text/html" and body_html is None:
                charset = part.get_content_charset() or "utf-8"
                try:
                    payload = part.get_payload(decode=True)
                    body_html = payload.decode(charset, errors="replace")
                except Exception:
                    body_html = payload.decode("utf-8", errors="replace") if payload else ""
    else:
        content_type = msg.get_content_type()
        charset = msg.get_content_charset() or "utf-8"
        payload = msg.get_payload(decode=True)
        if payload:
            decoded = payload.decode(charset, errors="replace")
            if content_type == "text/html":
                body_html = decoded
            else:
                body_text = decoded
    if body_text:
        return body_text
    if body_html:
        return strip_html(body_html)
    return "(empty email)"


def get_attachments_info(msg):
    attachments = []
    if msg.is_multipart():
        for part in msg.walk():
            content_disposition = str(part.get("Content-Disposition", ""))
            if "attachment" in content_disposition:
                filename = decode_mime_header(part.get_filename() or "unknown")
                size = len(part.get_payload(decode=True) or b"")
                attachments.append({"filename": filename, "size": size})
    return attachments


def download_attachments(msg, save_dir):
    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)
    saved = []
    if msg.is_multipart():
        for part in msg.walk():
            content_disposition = str(part.get("Content-Disposition", ""))
            if "attachment" in content_disposition:
                filename = decode_mime_header(part.get_filename() or "unknown")
                payload = part.get_payload(decode=True)
                if payload:
                    fpath = save_path / filename
                    with open(fpath, "wb") as f:
                        f.write(payload)
                    saved.append(str(fpath))
    return saved


def detect_provider(email_addr):
    if not email_addr or "@" not in email_addr:
        return None, None
    domain = email_addr.split("@")[1].lower()
    domain = PROVIDER_ALIASES.get(domain, domain)
    if domain in PROVIDERS:
        return domain, PROVIDERS[domain]
    return None, None


def get_credentials(provider_config, from_addr_override=None):
    from_addr = from_addr_override or ""
    if not from_addr and provider_config:
        env_user = provider_config.get("env_user", "")
        from_addr = os.environ.get(env_user, "") or os.environ.get("EMAIL_ADDRESS", "")
    if not from_addr:
        from_addr = os.environ.get("EMAIL_ADDRESS", "")
    if not from_addr:
        return None, None
    auth_code = ""
    if provider_config:
        env_auth = provider_config.get("env_auth", "")
        auth_code = os.environ.get(env_auth, "") or os.environ.get("EMAIL_AUTH", "")
    else:
        auth_code = os.environ.get("EMAIL_AUTH", "")
    return from_addr, auth_code


def connect_imap(provider_config, email_addr, auth_code):
    imap_server = provider_config["imap_server"]
    imap_port = provider_config.get("imap_port", 993)
    try:
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)
        mail.login(email_addr, auth_code)
        return mail, None
    except imaplib.IMAP4.error as e:
        return None, f"IMAP auth failed: {e}"
    except Exception as e:
        return None, f"IMAP connection failed: {e}"


def format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f}KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f}MB"


def cmd_list(mail, count=10, folder="INBOX"):
    mail.select(folder, readonly=True)
    status, data = mail.search(None, "ALL")
    if status != "OK":
        print("Search failed / search failed")
        return
    msg_ids = data[0].split()
    total = len(msg_ids)
    recent_ids = msg_ids[-count:] if total > count else msg_ids

    print(f"Inbox / 收件箱 ({total} emails, showing latest {len(recent_ids)})")
    print("=" * 70)

    for mid in reversed(recent_ids):
        status, msg_data = mail.fetch(mid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
        if status != "OK":
            continue
        raw = msg_data[0][1]
        msg = email.message_from_bytes(raw)
        sender = decode_mime_header(msg.get("From", ""))
        subject = decode_mime_header(msg.get("Subject", ""))
        date = msg.get("Date", "")
        print(f"  #{mid.decode() if isinstance(mid, bytes) else mid}")
        print(f"  From: {sender}")
        print(f"  Subject: {subject}")
        print(f"  Date: {date}")
        print("-" * 70)


def cmd_read(mail, uid, folder="INBOX", save_dir=None, forward=False):
    mail.select(folder, readonly=True)
    status, msg_data = mail.fetch(uid, "(RFC822)")
    if status != "OK":
        print(f"Failed to read email #{uid} / 读取邮件 #{uid} 失败")
        return

    raw = msg_data[0][1]
    msg = email.message_from_bytes(raw)

    if forward:
        from_hdr = decode_mime_header(msg.get("From", ""))
        to_hdr = decode_mime_header(msg.get("To", ""))
        cc_hdr = decode_mime_header(msg.get("Cc", ""))
        date_hdr = msg.get("Date", "")
        subject_hdr = decode_mime_header(msg.get("Subject", ""))
        msg_id = msg.get("Message-ID", "")

        print("FORWARD_META_START")
        print(f"FORWARD_FROM={from_hdr}")
        print(f"FORWARD_TO={to_hdr}")
        print(f"FORWARD_CC={cc_hdr}")
        print(f"FORWARD_DATE={date_hdr}")
        print(f"FORWARD_SUBJECT={subject_hdr}")
        print(f"FORWARD_MSGID={msg_id}")
        print("FORWARD_META_END")
        print()

    print(f"Email Detail / 邮件详情 (#{uid})")
    print("=" * 70)
    print(f"From:    {decode_mime_header(msg.get('From', ''))}")
    print(f"To:      {decode_mime_header(msg.get('To', ''))}")
    cc = msg.get("Cc")
    if cc:
        print(f"Cc:      {decode_mime_header(cc)}")
    print(f"Subject: {decode_mime_header(msg.get('Subject', ''))}")
    print(f"Date:    {msg.get('Date', '')}")
    reply_to = msg.get("In-Reply-To")
    if reply_to:
        print(f"In-Reply-To: {reply_to}")
    msg_id = msg.get("Message-ID")
    if msg_id:
        print(f"Message-ID: {msg_id}")
    print("=" * 70)

    body = get_text_from_message(msg)
    print(body)
    print("=" * 70)

    attachments = get_attachments_info(msg)
    if attachments:
        print(f"\nAttachments ({len(attachments)}):")
        for att in attachments:
            print(f"  - {att['filename']} ({format_size(att['size'])})")

        if save_dir:
            saved = download_attachments(msg, save_dir)
            if saved:
                print(f"\nAttachments saved to: {save_dir}")
                for s in saved:
                    print(f"  {s}")

    if msg_id and not forward:
        print(f'\nTo reply, use: --reply-to "{msg_id}"')
        print(f"To forward, use: --forward {uid}")


def cmd_search(mail, keyword=None, from_filter=None, subject_filter=None,
               since_date=None, before_date=None, folder="INBOX", count=10):
    mail.select(folder, readonly=True)

    criteria_parts = []
    if from_filter:
        criteria_parts.append(f'(FROM "{from_filter}")')
    if subject_filter:
        criteria_parts.append(f'(SUBJECT "{subject_filter}")')
    if since_date:
        criteria_parts.append(f'(SINCE "{since_date}")')
    if before_date:
        criteria_parts.append(f'(BEFORE "{before_date}")')
    if keyword:
        keyword_criteria = f'(OR OR SUBJECT "{keyword}" FROM "{keyword}" BODY "{keyword}")'
        criteria_parts.append(keyword_criteria)

    if not criteria_parts:
        criteria_parts.append("ALL")

    criteria = " ".join(criteria_parts)
    status, data = mail.search(None, criteria)
    if status != "OK":
        print("Search failed / 搜索失败")
        return

    msg_ids = data[0].split()
    total = len(msg_ids)

    if total == 0:
        print("No matching emails found / 没有找到匹配的邮件")
        return

    recent_ids = msg_ids[-count:] if total > count else msg_ids

    print(f"Search Results / 搜索结果 ({total} found, showing {len(recent_ids)})")
    print(f"  Criteria: {criteria}")
    print("=" * 70)

    for mid in reversed(recent_ids):
        status, msg_data = mail.fetch(mid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
        if status != "OK":
            continue
        raw = msg_data[0][1]
        msg = email.message_from_bytes(raw)
        sender = decode_mime_header(msg.get("From", ""))
        subject = decode_mime_header(msg.get("Subject", ""))
        date = msg.get("Date", "")
        print(f"  #{mid.decode() if isinstance(mid, bytes) else mid}")
        print(f"  From: {sender}")
        print(f"  Subject: {subject}")
        print(f"  Date: {date}")
        print("-" * 70)


def main():
    parser = argparse.ArgumentParser(description="Emailbox - Receive/search/forward emails")
    parser.add_argument("--list", action="store_true", help="List recent emails")
    parser.add_argument("--read", help="Read email by UID")
    parser.add_argument("--forward", help="Read email in forward format (outputs metadata for forwarding)")
    parser.add_argument("--search", help="Search keyword (searches subject, from, and body)")
    parser.add_argument("--count", type=int, default=10, help="Number of emails (default 10)")
    parser.add_argument("--from-addr", help="Email address (overrides env)")
    parser.add_argument("--provider", help="Force provider (qq/163/gmail/outlook/126/sina/yahoo/icloud/exmail/mxhichina/hicloud/139)")
    parser.add_argument("--from-filter", help="Filter by sender")
    parser.add_argument("--subject-filter", help="Filter by subject")
    parser.add_argument("--since", help="Since date (YYYY-MM-DD)")
    parser.add_argument("--before", help="Before date (YYYY-MM-DD)")
    parser.add_argument("--folder", default="INBOX", help="IMAP folder (default INBOX, e.g. Sent, Drafts, Trash)")
    parser.add_argument("--download-attachment", help="UID to download attachments from")
    parser.add_argument("--save-dir", help="Directory to save attachments")
    args = parser.parse_args()

    if not (args.list or args.read or args.search or args.download_attachment or args.forward):
        parser.print_help()
        sys.exit(1)

    from_addr = args.from_addr or os.environ.get("EMAIL_ADDRESS", "")
    if not from_addr:
        print("error: no email address. Set EMAIL_ADDRESS env or use --from-addr")
        sys.exit(1)

    if args.provider:
        prov_name = args.provider.lower()
        provider_config = PROVIDERS.get(prov_name)
        if not provider_config:
            print(f"error: unknown provider '{prov_name}'")
            sys.exit(1)
    else:
        prov_name, provider_config = detect_provider(from_addr)
        if not provider_config:
            print(f"error: unsupported email domain for '{from_addr}'")
            sys.exit(1)

    email_addr, auth_code = get_credentials(provider_config, args.from_addr)
    if not email_addr:
        email_addr = from_addr
    if not auth_code:
        auth_code = os.environ.get("EMAIL_AUTH", "")
    if not auth_code:
        print(f"error: no auth code. Set EMAIL_AUTH or {provider_config.get('env_auth', 'EMAIL_*_AUTH')} env")
        sys.exit(1)

    mail, err = connect_imap(provider_config, email_addr, auth_code)
    if err:
        print(f"Connection failed: {err}")
        sys.exit(1)

    try:
        if args.list:
            cmd_list(mail, args.count, args.folder)
        elif args.forward:
            save_dir = args.save_dir or os.path.join(os.path.expanduser("~"), ".emailbox", "downloads")
            cmd_read(mail, args.forward, args.folder, save_dir, forward=True)
        elif args.read or args.download_attachment:
            uid = args.read or args.download_attachment
            save_dir = args.save_dir or os.path.join(os.path.expanduser("~"), ".emailbox", "downloads")
            cmd_read(mail, uid, args.folder, save_dir if args.download_attachment else None)
        elif args.search:
            since_str = args.since
            if since_str and re.match(r"^\d{4}-\d{2}-\d{2}$", since_str):
                from datetime import datetime
                dt = datetime.strptime(since_str, "%Y-%m-%d")
                since_str = dt.strftime("%d-%b-%Y")
            cmd_search(mail, args.search, args.from_filter, args.subject_filter,
                       since_str, args.before, args.folder, args.count)
    finally:
        mail.logout()


if __name__ == "__main__":
    main()