#!/usr/bin/env python3
"""Email skill script for SMTP sending and IMAP reading."""

from __future__ import annotations

import argparse
import email
import imaplib
import json
import mimetypes
import os
import smtplib
import ssl
import sys
from dataclasses import dataclass
from email.header import decode_header
from email.message import Message
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, parseaddr
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class EmailConfig:
    smtp_host: str
    imap_host: str
    port: int
    username: str
    password: str
    use_ssl: bool = True
    imap_port: int = 993
    mailbox: str = "INBOX"

    @classmethod
    def from_env(cls) -> "EmailConfig":
        load_nearest_env_file()
        smtp_host = get_env("EMAIL_HOST", "SMTP_HOST")
        imap_host = get_env("IMAP_HOST", "SMTP_IMAP_HOST", "SMTP_HOST")
        port = get_env("EMAIL_PORT", "SMTP_PORT", default="465")
        imap_port = get_env("EMAIL_IMAP_PORT", "IMAP_PORT", default="993")
        mailbox = get_env("EMAIL_MAILBOX", "IMAP_MAILBOX", default="INBOX")
        username = get_env("EMAIL_USER", "SMTP_USER", "SMTP_FROM")
        password = get_env("EMAIL_PASSWORD", "SMTP_PASS")
        use_ssl = get_env("EMAIL_USE_SSL", "SMTP_SECURE", default="true")
        missing = [
            label
            for label, value in (
                ("EMAIL_HOST or SMTP_HOST", smtp_host),
                ("EMAIL_USER or SMTP_USER", username),
                ("EMAIL_PASSWORD or SMTP_PASS", password),
            )
            if not value
        ]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        return cls(
            smtp_host=smtp_host or "",
            imap_host=imap_host or smtp_host or "",
            port=int(port or "465"),
            username=username or "",
            password=password or "",
            use_ssl=(use_ssl or "true").lower() not in {"0", "false", "no"},
            imap_port=int(imap_port or "993"),
            mailbox=mailbox or "INBOX",
        )


class EmailService:
    def __init__(self, config: EmailConfig) -> None:
        self.config = config

    def send_email(
        self,
        to_addresses: list[str],
        subject: str,
        body: str,
        cc_addresses: list[str] | None = None,
        attachments: list[str] | None = None,
        html_body: str | None = None,
    ) -> dict[str, Any]:
        if not to_addresses:
            raise ValueError("At least one recipient is required")

        attachment_paths = self._validate_attachments(attachments or [])
        message = self._build_message(
            to_addresses=to_addresses,
            subject=subject,
            body=body,
            cc_addresses=cc_addresses or [],
            attachments=attachment_paths,
            html_body=html_body,
        )
        recipients = to_addresses + (cc_addresses or [])

        if self.config.use_ssl:
            smtp = smtplib.SMTP_SSL(
                self.config.smtp_host,
                self.config.port,
                context=ssl.create_default_context(),
            )
        else:
            smtp = smtplib.SMTP(self.config.smtp_host, self.config.port)
            smtp.starttls(context=ssl.create_default_context())

        with smtp:
            smtp.login(self.config.username, self.config.password)
            smtp.sendmail(self.config.username, recipients, message.as_string())

        return {
            "success": True,
            "from": self.config.username,
            "to": to_addresses,
            "cc": cc_addresses or [],
            "subject": subject,
            "attachments": [str(path) for path in attachment_paths],
        }

    def read_emails(self, limit: int = 10) -> list[dict[str, Any]]:
        limit = max(1, min(limit, 100))
        with imaplib.IMAP4_SSL(self.config.imap_host, self.config.imap_port) as mailbox:
            mailbox.login(self.config.username, self.config.password)
            mailbox.select(self.config.mailbox)
            _, data = mailbox.search(None, "ALL")
            email_ids = data[0].split()
            latest_ids = email_ids[-limit:]

            messages: list[dict[str, Any]] = []
            for email_id in reversed(latest_ids):
                _, msg_data = mailbox.fetch(email_id, "(RFC822)")
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)
                messages.append(
                    {
                        "id": email_id.decode("utf-8", errors="replace"),
                        "subject": decode_email_header(msg["Subject"] or ""),
                        "from": decode_email_header(msg["From"] or ""),
                        "to": decode_email_header(msg["To"] or ""),
                        "cc": decode_email_header(msg.get("Cc", "")),
                        "date": msg["Date"] or "",
                        "body": get_email_body(msg),
                        "attachments": get_attachments(msg),
                    }
                )
            mailbox.close()
            return messages

    def analyze_emails(self, limit: int = 10) -> dict[str, Any]:
        messages = self.read_emails(limit=limit)
        if not messages:
            return {"total_emails": 0, "with_attachments": 0, "sender_domains": {}}

        sender_domains: dict[str, int] = {}
        parsed_dates = []
        for message in messages:
            _, address = parseaddr(message.get("from", ""))
            if "@" in address:
                domain = address.rsplit("@", 1)[1].lower()
                sender_domains[domain] = sender_domains.get(domain, 0) + 1
            if message.get("date"):
                try:
                    parsed_dates.append(email.utils.parsedate_to_datetime(message["date"]))
                except (TypeError, ValueError):
                    pass

        subjects = [message.get("subject", "") for message in messages]
        date_range = None
        if parsed_dates:
            date_range = {
                "oldest": min(parsed_dates).isoformat(),
                "newest": max(parsed_dates).isoformat(),
            }

        return {
            "total_emails": len(messages),
            "with_attachments": sum(1 for message in messages if message.get("attachments")),
            "sender_domains": sender_domains,
            "date_range": date_range,
            "average_subject_length": sum(len(subject) for subject in subjects) / len(subjects),
        }

    def _build_message(
        self,
        to_addresses: list[str],
        subject: str,
        body: str,
        cc_addresses: list[str],
        attachments: list[Path],
        html_body: str | None,
    ) -> MIMEMultipart:
        message = MIMEMultipart("mixed")
        message["From"] = formataddr((self.config.username, self.config.username))
        message["To"] = ", ".join(to_addresses)
        message["Subject"] = subject
        if cc_addresses:
            message["Cc"] = ", ".join(cc_addresses)

        body_container = MIMEMultipart("alternative") if html_body else None
        if body_container:
            body_container.attach(MIMEText(body, "plain", "utf-8"))
            body_container.attach(MIMEText(html_body, "html", "utf-8"))
            message.attach(body_container)
        else:
            message.attach(MIMEText(body, "plain", "utf-8"))

        for path in attachments:
            mime_type, _ = mimetypes.guess_type(path)
            subtype = (mime_type or "application/octet-stream").split("/", 1)[1]
            with path.open("rb") as file:
                attachment = MIMEApplication(file.read(), _subtype=subtype)
            attachment.add_header("Content-Disposition", "attachment", filename=path.name)
            message.attach(attachment)

        return message

    @staticmethod
    def _validate_attachments(attachments: list[str]) -> list[Path]:
        paths: list[Path] = []
        for attachment in attachments:
            path = Path(attachment).expanduser().resolve()
            if not path.is_file():
                raise ValueError(f"Attachment does not exist: {attachment}")
            paths.append(path)
        return paths


def decode_email_header(header: str) -> str:
    decoded_parts: list[str] = []
    for part, encoding in decode_header(header):
        if isinstance(part, bytes):
            decoded_parts.append(part.decode(encoding or "utf-8", errors="replace"))
        else:
            decoded_parts.append(part)
    return " ".join(decoded_parts)


def get_email_body(message: Message) -> str:
    if not message.is_multipart():
        payload = message.get_payload(decode=True)
        return payload.decode("utf-8", errors="replace") if isinstance(payload, bytes) else ""

    html_fallback = ""
    for part in message.walk():
        content_disposition = str(part.get("Content-Disposition"))
        if "attachment" in content_disposition:
            continue
        payload = part.get_payload(decode=True)
        if not isinstance(payload, bytes):
            continue
        content = payload.decode("utf-8", errors="replace")
        if part.get_content_type() == "text/plain":
            return content
        if part.get_content_type() == "text/html" and not html_fallback:
            html_fallback = content
    return html_fallback


def get_attachments(message: Message) -> list[dict[str, Any]]:
    attachments: list[dict[str, Any]] = []
    if not message.is_multipart():
        return attachments

    for part in message.walk():
        content_disposition = str(part.get("Content-Disposition"))
        if "attachment" not in content_disposition:
            continue
        filename = part.get_filename()
        payload = part.get_payload(decode=True) or b""
        if filename:
            attachments.append(
                {
                    "filename": decode_email_header(filename),
                    "content_type": part.get_content_type() or "application/octet-stream",
                    "size": len(payload),
                }
            )
    return attachments


def split_values(values: list[str] | None) -> list[str]:
    if not values:
        return []
    result: list[str] = []
    for value in values:
        result.extend(item.strip() for item in value.split(",") if item.strip())
    return result


def read_text_arg(value: str | None) -> str:
    if value == "-":
        return sys.stdin.read()
    return value or ""


def load_nearest_env_file() -> None:
    seen: set[Path] = set()
    starts = [Path.cwd(), Path(__file__).resolve().parent]
    for start in starts:
        for directory in (start, *start.parents):
            env_file = directory / ".env"
            if env_file in seen:
                continue
            seen.add(env_file)
            if env_file.is_file():
                load_env_file(env_file)
                return


def load_env_file(path: Path) -> None:
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key:
            continue
        os.environ.setdefault(key, value.strip().strip("\"'"))


def get_env(*names: str, default: str | None = None) -> str | None:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return default


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SMTP/IMAP email skill script.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    send_parser = subparsers.add_parser("send", help="Send an email.")
    send_parser.add_argument("--to", action="append", required=True, help="Recipient email. May repeat or comma-separate.")
    send_parser.add_argument("--subject", required=True)
    send_parser.add_argument("--body", required=True, help="Plain text body. Use '-' to read stdin.")
    send_parser.add_argument("--cc", action="append", help="CC email. May repeat or comma-separate.")
    send_parser.add_argument("--attachment", action="append", help="Attachment path. May repeat.")
    send_parser.add_argument("--html-body", help="HTML body. Use '-' to read stdin.")

    read_parser = subparsers.add_parser("read", help="Read recent inbox emails.")
    read_parser.add_argument("--limit", type=int, default=10)

    analyze_parser = subparsers.add_parser("analyze", help="Analyze recent inbox emails.")
    analyze_parser.add_argument("--limit", type=int, default=10)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        service = EmailService(EmailConfig.from_env())
        if args.command == "send":
            result = service.send_email(
                to_addresses=split_values(args.to),
                subject=args.subject,
                body=read_text_arg(args.body),
                cc_addresses=split_values(args.cc),
                attachments=args.attachment or [],
                html_body=read_text_arg(args.html_body) if args.html_body else None,
            )
        elif args.command == "read":
            result = service.read_emails(limit=args.limit)
        elif args.command == "analyze":
            result = service.analyze_emails(limit=args.limit)
        else:
            parser.error(f"Unknown command: {args.command}")
    except Exception as exc:
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=True), file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
