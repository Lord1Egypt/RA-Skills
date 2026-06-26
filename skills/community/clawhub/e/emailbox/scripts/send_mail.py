#!/usr/bin/env python3
"""Emailbox - Send email via SMTP with 12+ provider support.

Supports: plain text, HTML, attachments, CC/BCC, reply, forward, read receipts.
Uses only Python standard library (smtplib, email, ssl).

Usage:
  python3 send_mail.py --to user@example.com --subject "Test" --body "Hello"
  python3 send_mail.py --to user@example.com --subject "Report" --html-file report.html
  python3 send_mail.py --to user@example.com --subject "Files" --body "See attached" --attach a.pdf b.xlsx
  python3 send_mail.py --to user@example.com --subject "Re: Hello" --body "Reply" --reply-to "<msgid@example.com>"
  python3 send_mail.py --to user@example.com --subject "Fwd: Hello" --body "See below" --forward-body "Original message..."
"""

import argparse
import mimetypes
import os
import smtplib
import ssl
import sys
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from pathlib import Path

PROVIDERS = {
    "qq.com": {"smtp_server": "smtp.qq.com", "smtp_port": 465, "use_ssl": True, "env_user": "EMAIL_QQ", "env_auth": "EMAIL_QQ_AUTH"},
    "163.com": {"smtp_server": "smtp.163.com", "smtp_port": 465, "use_ssl": True, "env_user": "EMAIL_163", "env_auth": "EMAIL_163_AUTH"},
    "126.com": {"smtp_server": "smtp.126.com", "smtp_port": 465, "use_ssl": True, "env_user": "EMAIL_126", "env_auth": "EMAIL_126_AUTH"},
    "sina.com": {"smtp_server": "smtp.sina.com", "smtp_port": 465, "use_ssl": True, "env_user": "EMAIL_SINA", "env_auth": "EMAIL_SINA_AUTH"},
    "outlook.com": {"smtp_server": "smtp.office365.com", "smtp_port": 587, "use_ssl": False, "env_user": "EMAIL_OUTLOOK", "env_auth": "EMAIL_OUTLOOK_AUTH"},
    "hotmail.com": {"smtp_server": "smtp.office365.com", "smtp_port": 587, "use_ssl": False, "env_user": "EMAIL_OUTLOOK", "env_auth": "EMAIL_OUTLOOK_AUTH"},
    "live.com": {"smtp_server": "smtp.office365.com", "smtp_port": 587, "use_ssl": False, "env_user": "EMAIL_OUTLOOK", "env_auth": "EMAIL_OUTLOOK_AUTH"},
    "gmail.com": {"smtp_server": "smtp.gmail.com", "smtp_port": 587, "use_ssl": False, "env_user": "EMAIL_GMAIL", "env_auth": "EMAIL_GMAIL_AUTH"},
    "yahoo.com": {"smtp_server": "smtp.mail.yahoo.com", "smtp_port": 587, "use_ssl": False, "env_user": "EMAIL_YAHOO", "env_auth": "EMAIL_YAHOO_AUTH"},
    "icloud.com": {"smtp_server": "smtp.mail.me.com", "smtp_port": 587, "use_ssl": False, "env_user": "EMAIL_ICLOUD", "env_auth": "EMAIL_ICLOUD_AUTH"},
    "exmail.qq.com": {"smtp_server": "smtp.exmail.qq.com", "smtp_port": 465, "use_ssl": True, "env_user": "EMAIL_EXMAIL", "env_auth": "EMAIL_EXMAIL_AUTH"},
    "mxhichina.com": {"smtp_server": "smtp.mxhichina.com", "smtp_port": 465, "use_ssl": True, "env_user": "EMAIL_ALIMAIL", "env_auth": "EMAIL_ALIMAIL_AUTH"},
    "hicloud.com": {"smtp_server": "smtp.mail.hicloud.com", "smtp_port": 465, "use_ssl": True, "env_user": "EMAIL_HUAWEI", "env_auth": "EMAIL_HUAWEI_AUTH"},
    "139.com": {"smtp_server": "smtp.mail.139.com", "smtp_port": 465, "use_ssl": True, "env_user": "EMAIL_139", "env_auth": "EMAIL_139_AUTH"},
}

PROVIDER_ALIASES = {
    "hotmail.com": "outlook.com", "live.com": "outlook.com",
    "foxmail.com": "qq.com", "vip.qq.com": "qq.com",
    "vip.163.com": "163.com", "vip.126.com": "126.com", "yeah.net": "163.com",
    "sina.cn": "sina.com", "yahoo.co.jp": "yahoo.com", "yahoo.cn": "yahoo.com",
    "me.com": "icloud.com", "mac.com": "icloud.com",
}


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


def _format_forward_header(from_addr_hdr, to_hdr, cc_hdr, date_hdr, subject_hdr):
    lines = []
    lines.append("---------- Forwarded message ----------")
    if from_addr_hdr:
        lines.append(f"From: {from_addr_hdr}")
    if date_hdr:
        lines.append(f"Date: {date_hdr}")
    if subject_hdr:
        lines.append(f"Subject: {subject_hdr}")
    if to_hdr:
        lines.append(f"To: {to_hdr}")
    if cc_hdr:
        lines.append(f"Cc: {cc_hdr}")
    lines.append("")
    return "\n".join(lines)


def create_message(from_addr, to_list, cc_list, bcc_list, subject,
                   body_text=None, body_html=None, attachments=None,
                   reply_to=None, forward_header=None, importance=None, request_receipt=False):
    has_html = body_html is not None
    has_attachments = attachments and len(attachments) > 0

    if body_text and forward_header:
        body_text = forward_header + "\n" + body_text

    if has_html or has_attachments:
        if has_attachments:
            msg = MIMEMultipart("mixed")
            if has_html:
                alt = MIMEMultipart("alternative")
                if body_text:
                    alt.attach(MIMEText(body_text, "plain", "utf-8"))
                alt.attach(MIMEText(body_html, "html", "utf-8"))
                msg.attach(alt)
            else:
                if body_text:
                    msg.attach(MIMEText(body_text, "plain", "utf-8"))
            for fpath in attachments:
                part = _create_attachment(fpath)
                if part:
                    msg.attach(part)
        else:
            msg = MIMEMultipart("alternative")
            if body_text:
                msg.attach(MIMEText(body_text, "plain", "utf-8"))
            msg.attach(MIMEText(body_html, "html", "utf-8"))
    else:
        msg = MIMEText(body_text or "", "plain", "utf-8")

    msg["From"] = from_addr
    msg["To"] = ", ".join(to_list)
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain=from_addr.split("@")[1] if "@" in from_addr else "localhost")

    if reply_to:
        msg["In-Reply-To"] = reply_to
        msg["References"] = reply_to

    if importance:
        importance_map = {"high": "1", "normal": "3", "low": "5"}
        msg["X-Priority"] = importance_map.get(importance, "3")
        importance_label = {"high": "high", "normal": "normal", "low": "low"}
        msg["Importance"] = importance_label.get(importance, "normal")

    if request_receipt:
        msg["Disposition-Notification-To"] = from_addr

    return msg


def _create_attachment(filepath):
    fpath = Path(filepath)
    if not fpath.exists():
        print(f"warning: attachment not found: {filepath}", file=sys.stderr)
        return None
    mime_type, _ = mimetypes.guess_type(str(fpath))
    if mime_type is None:
        mime_type = "application/octet-stream"
    main_type, sub_type = mime_type.split("/", 1)
    if main_type == "application":
        with open(fpath, "rb") as f:
            part = MIMEApplication(f.read(), _subtype=sub_type)
    else:
        part = MIMEBase(main_type, sub_type)
        with open(fpath, "rb") as f:
            part.set_payload(f.read())
        encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment", filename=fpath.name)
    return part


def send_email(from_addr, auth_code, provider_config, to_list, cc_list, bcc_list,
               subject, body_text=None, body_html=None, attachments=None,
               reply_to=None, forward_header=None, importance=None, request_receipt=False):
    msg = create_message(
        from_addr, to_list, cc_list, bcc_list, subject,
        body_text, body_html, attachments, reply_to, forward_header, importance, request_receipt
    )

    all_recipients = to_list + (cc_list or []) + (bcc_list or [])

    smtp_server = provider_config["smtp_server"]
    smtp_port = provider_config["smtp_port"]
    use_ssl = provider_config["use_ssl"]

    try:
        if use_ssl:
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL(smtp_server, smtp_port, context=context)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port)
            context = ssl.create_default_context()
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()

        server.login(from_addr, auth_code)
        server.sendmail(from_addr, all_recipients, msg.as_string())
        server.quit()
        return True, None
    except smtplib.SMTPAuthenticationError as e:
        return False, f"SMTP auth failed: {e}. Check your authorization code / app password."
    except smtplib.SMTPRecipientsRefused as e:
        return False, f"Recipient refused: {e}"
    except smtplib.SMTPException as e:
        return False, f"SMTP error: {e}"
    except Exception as e:
        return False, f"Send failed: {e}"


def main():
    parser = argparse.ArgumentParser(description="Emailbox - Send email")
    parser.add_argument("--to", required=True, help="Recipients (comma-separated)")
    parser.add_argument("--subject", required=True, help="Email subject")
    parser.add_argument("--body", help="Plain text body")
    parser.add_argument("--body-file", help="File path for plain text body")
    parser.add_argument("--html-body", help="HTML body (inline)")
    parser.add_argument("--html-file", help="File path for HTML body")
    parser.add_argument("--cc", help="CC recipients (comma-separated)")
    parser.add_argument("--bcc", help="BCC recipients (comma-separated)")
    parser.add_argument("--attach", nargs="*", help="Files to attach")
    parser.add_argument("--from-addr", help="Sender email (overrides env)")
    parser.add_argument("--provider", help="Force provider (qq/163/gmail/outlook/126/sina/yahoo/icloud/exmail/mxhichina/hicloud/139)")
    parser.add_argument("--reply-to", help="Original Message-ID for reply")
    parser.add_argument("--forward-from", help="Original sender for forward header")
    parser.add_argument("--forward-date", help="Original date for forward header")
    parser.add_argument("--forward-to", help="Original recipients for forward header")
    parser.add_argument("--forward-cc", help="Original CC for forward header")
    parser.add_argument("--forward-subject", help="Original subject for forward header")
    parser.add_argument("--importance", choices=["high", "normal", "low"], help="Email priority (high/normal/low)")
    parser.add_argument("--receipt", action="store_true", help="Request read receipt")
    args = parser.parse_args()

    body_text = args.body
    if args.body_file:
        with open(args.body_file, "r", encoding="utf-8") as f:
            body_text = f.read()

    body_html = args.html_body
    if args.html_file:
        with open(args.html_file, "r", encoding="utf-8") as f:
            body_html = f.read()

    if not body_text and not body_html:
        print("error: --body, --body-file, --html-body, or --html-file is required")
        sys.exit(1)

    to_list = [e.strip() for e in args.to.split(",") if e.strip()]
    cc_list = [e.strip() for e in args.cc.split(",") if e.strip()] if args.cc else []
    bcc_list = [e.strip() for e in args.bcc.split(",") if e.strip()] if args.bcc else []
    attachments = args.attach or []

    from_addr = args.from_addr or os.environ.get("EMAIL_ADDRESS", "")

    if args.provider:
        prov_name = args.provider.lower()
        provider_config = PROVIDERS.get(prov_name)
        if not provider_config:
            print(f"error: unknown provider '{prov_name}'")
            print(f"supported: {', '.join(sorted(set(PROVIDERS.keys())))}")
            sys.exit(1)
    elif from_addr:
        prov_name, provider_config = detect_provider(from_addr)
        if not provider_config:
            print(f"error: unsupported email domain for '{from_addr}'")
            print(f"supported: {', '.join(sorted(set(PROVIDERS.keys()) | set(PROVIDER_ALIASES.keys())))}")
            sys.exit(1)
    else:
        from_addr = os.environ.get("EMAIL_ADDRESS", "")
        if not from_addr:
            print("error: no sender email. Set EMAIL_ADDRESS env or use --from-addr")
            sys.exit(1)
        prov_name, provider_config = detect_provider(from_addr)
        if not provider_config:
            print(f"error: unsupported email domain for '{from_addr}'")
            sys.exit(1)

    if not from_addr:
        from_addr = os.environ.get("EMAIL_ADDRESS", "")
    if not from_addr:
        print("error: no sender email. Set EMAIL_ADDRESS env or use --from-addr")
        sys.exit(1)

    email_addr, auth_code = get_credentials(provider_config, args.from_addr)
    if not email_addr:
        email_addr = from_addr
    if not auth_code:
        auth_code = os.environ.get("EMAIL_AUTH", "")
    if not auth_code:
        env_auth_key = provider_config.get("env_auth", "EMAIL_AUTH")
        print(f"error: no auth code. Set EMAIL_AUTH or {env_auth_key} env")
        print(f"hint: see references/providers.md for {prov_name} auth code setup")
        sys.exit(1)

    forward_header = None
    if args.forward_from or args.forward_date or args.forward_subject:
        forward_header = _format_forward_header(
            args.forward_from, args.forward_to, args.forward_cc,
            args.forward_date, args.forward_subject
        )

    subject = args.subject
    if forward_header and not subject.lower().startswith("fwd:") and not subject.lower().startswith("转发:"):
        subject = f"Fwd: {args.subject}"

    ok, err = send_email(
        email_addr, auth_code, provider_config,
        to_list, cc_list, bcc_list,
        subject, body_text, body_html, attachments,
        args.reply_to, forward_header, args.importance, args.receipt
    )

    if ok:
        print("Email sent successfully / 邮件发送成功")
        print(f"  From: {email_addr}")
        print(f"  To: {', '.join(to_list)}")
        if cc_list:
            print(f"  CC: {', '.join(cc_list)}")
        print(f"  Subject: {subject}")
        if attachments:
            print(f"  Attachments: {', '.join(str(a) for a in attachments)}")
    else:
        print(f"Email send failed / 邮件发送失败")
        print(f"  Error: {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()