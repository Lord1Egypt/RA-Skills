#!/usr/bin/env python3
"""IMAP/SMTP email operations with password and OAuth2 auth modes."""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import mimetypes
import os
import re
import secrets
import smtplib
import ssl
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from email import policy
from email.header import decode_header, make_header
from email.message import EmailMessage, Message
from email.parser import BytesParser
from pathlib import Path

import imaplib


PROVIDER_PRESETS = {
    "qq": {
        "imap_host": "imap.qq.com",
        "imap_port": 993,
        "smtp_host": "smtp.qq.com",
        "smtp_port": 465,
        "smtp_ssl": True,
    },
    "163": {
        "imap_host": "imap.163.com",
        "imap_port": 993,
        "smtp_host": "smtp.163.com",
        "smtp_port": 465,
        "smtp_ssl": True,
    },
    "126": {
        "imap_host": "imap.126.com",
        "imap_port": 993,
        "smtp_host": "smtp.126.com",
        "smtp_port": 465,
        "smtp_ssl": True,
    },
    "gmail": {
        "imap_host": "imap.gmail.com",
        "imap_port": 993,
        "smtp_host": "smtp.gmail.com",
        "smtp_port": 465,
        "smtp_ssl": True,
        "oauth": {
            "auth_endpoint": "https://accounts.google.com/o/oauth2/v2/auth",
            "token_endpoint": "https://oauth2.googleapis.com/token",
            "scope": "https://mail.google.com/",
        },
    },
    "outlook": {
        "imap_host": "outlook.office365.com",
        "imap_port": 993,
        "smtp_host": "smtp.office365.com",
        "smtp_port": 587,
        "smtp_ssl": False,
        "oauth": {
            "auth_endpoint": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
            "token_endpoint": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
            "scope": "offline_access https://outlook.office.com/IMAP.AccessAsUser.All https://outlook.office.com/SMTP.Send",
        },
    },
    "yahoo": {
        "imap_host": "imap.mail.yahoo.com",
        "imap_port": 993,
        "smtp_host": "smtp.mail.yahoo.com",
        "smtp_port": 465,
        "smtp_ssl": True,
        "oauth": {
            "auth_endpoint": "https://api.login.yahoo.com/oauth2/request_auth",
            "token_endpoint": "https://api.login.yahoo.com/oauth2/get_token",
            "scope": "openid mail-r mail-w",
        },
    },
    "aol": {
        "imap_host": "imap.aol.com",
        "imap_port": 993,
        "smtp_host": "smtp.aol.com",
        "smtp_port": 465,
        "smtp_ssl": True,
        "oauth": {
            "auth_endpoint": "https://api.login.yahoo.com/oauth2/request_auth",
            "token_endpoint": "https://api.login.yahoo.com/oauth2/get_token",
            "scope": "openid mail-r mail-w",
        },
    },
    "icloud": {
        "imap_host": "imap.mail.me.com",
        "imap_port": 993,
        "smtp_host": "smtp.mail.me.com",
        "smtp_port": 587,
        "smtp_ssl": False,
    },
    "zoho": {
        "imap_host": "imap.zoho.com",
        "imap_port": 993,
        "smtp_host": "smtp.zoho.com",
        "smtp_port": 465,
        "smtp_ssl": True,
        "oauth": {
            "auth_endpoint": "https://accounts.zoho.com/oauth/v2/auth",
            "token_endpoint": "https://accounts.zoho.com/oauth/v2/token",
        },
    },
}


@dataclass
class MailConfig:
    email: str
    auth_mode: str
    password: str | None
    access_token: str | None
    refresh_token: str | None
    token_endpoint: str | None
    client_id: str | None
    client_secret: str | None
    scope: str | None
    imap_host: str
    imap_port: int
    smtp_host: str
    smtp_port: int
    smtp_ssl: bool
    provider: str | None


def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    raise ValueError(f"Unsupported boolean value: {value}")


def decode_header_value(raw: str | None) -> str:
    if not raw:
        return ""
    try:
        return str(make_header(decode_header(raw)))
    except Exception:
        return raw


def imap_date(date_text: str) -> str:
    date_value = dt.datetime.strptime(date_text, "%Y-%m-%d").date()
    return date_value.strftime("%d-%b-%Y")


def extract_uid(fetch_response: list[object]) -> str:
    for item in fetch_response:
        if isinstance(item, tuple) and item and isinstance(item[0], bytes):
            match = re.search(rb"UID\s+(\d+)", item[0])
            if match:
                return match.group(1).decode("ascii")
    raise RuntimeError("Unable to parse UID from IMAP response")


def collect_text_body(msg: Message, max_chars: int) -> str:
    if msg.is_multipart():
        plain_chunks: list[str] = []
        html_chunks: list[str] = []
        for part in msg.walk():
            disposition = (part.get_content_disposition() or "").lower()
            if disposition == "attachment":
                continue
            payload = part.get_payload(decode=True)
            if payload is None:
                continue
            charset = part.get_content_charset() or "utf-8"
            text = payload.decode(charset, errors="replace")
            content_type = part.get_content_type()
            if content_type == "text/plain":
                plain_chunks.append(text)
            elif content_type == "text/html":
                html_chunks.append(text)
        body = "\n".join(plain_chunks).strip() or "\n".join(html_chunks).strip()
    else:
        payload = msg.get_payload(decode=True)
        if payload is None:
            body = ""
        else:
            charset = msg.get_content_charset() or "utf-8"
            body = payload.decode(charset, errors="replace")
    return body[:max_chars]


def collect_attachments(msg: Message) -> list[str]:
    files: list[str] = []
    for part in msg.walk():
        disposition = (part.get_content_disposition() or "").lower()
        if disposition != "attachment":
            continue
        filename = part.get_filename()
        if filename:
            files.append(decode_header_value(filename))
    return files


def get_provider_defaults(provider_key: str | None) -> dict:
    return PROVIDER_PRESETS.get(provider_key or "", {})


def resolve_auth_mode(args: argparse.Namespace, has_oauth_data: bool) -> str:
    mode = (args.auth_mode or os.getenv("EMAIL_AUTH_MODE", "auto")).strip().lower()
    if mode not in {"auto", "password", "oauth2"}:
        raise ValueError("EMAIL_AUTH_MODE must be one of auto/password/oauth2.")
    if mode == "auto":
        return "oauth2" if has_oauth_data else "password"
    return mode


def resolve_config(args: argparse.Namespace) -> MailConfig:
    provider_key = (args.provider or os.getenv("EMAIL_PROVIDER", "")).strip().lower() or None
    provider = get_provider_defaults(provider_key)
    oauth_defaults = provider.get("oauth", {})

    email = args.email or os.getenv("EMAIL_ADDRESS")
    if not email:
        raise ValueError("Missing email. Pass --email or set EMAIL_ADDRESS.")

    password = args.password or os.getenv("EMAIL_APP_PASSWORD") or os.getenv("EMAIL_PASSWORD")
    access_token = args.access_token or os.getenv("EMAIL_ACCESS_TOKEN")
    refresh_token = args.refresh_token or os.getenv("EMAIL_REFRESH_TOKEN")
    token_endpoint = args.token_endpoint or os.getenv("EMAIL_TOKEN_ENDPOINT") or oauth_defaults.get("token_endpoint")
    client_id = args.client_id or os.getenv("EMAIL_CLIENT_ID")
    client_secret = args.client_secret or os.getenv("EMAIL_CLIENT_SECRET")
    scope = args.scope or os.getenv("EMAIL_SCOPE") or oauth_defaults.get("scope")
    auth_mode = resolve_auth_mode(args, bool(access_token or refresh_token))

    smtp_ssl_env = os.getenv("EMAIL_SMTP_SSL")
    if args.smtp_ssl and args.smtp_starttls:
        raise ValueError("Use only one of --smtp-ssl and --smtp-starttls.")
    if args.smtp_ssl:
        smtp_ssl = True
    elif args.smtp_starttls:
        smtp_ssl = False
    elif smtp_ssl_env:
        smtp_ssl = parse_bool(smtp_ssl_env)
    elif "smtp_ssl" in provider:
        smtp_ssl = bool(provider["smtp_ssl"])
    else:
        smtp_ssl = False

    if auth_mode == "password" and not password:
        raise ValueError("Missing password for password mode. Set --password or EMAIL_APP_PASSWORD.")
    if auth_mode == "oauth2" and not (access_token or refresh_token):
        raise ValueError("OAuth2 mode requires --access-token or --refresh-token.")

    return MailConfig(
        email=email,
        auth_mode=auth_mode,
        password=password,
        access_token=access_token,
        refresh_token=refresh_token,
        token_endpoint=token_endpoint,
        client_id=client_id,
        client_secret=client_secret,
        scope=scope,
        imap_host=args.imap_host or os.getenv("EMAIL_IMAP_HOST") or provider.get("imap_host", ""),
        imap_port=int(args.imap_port or os.getenv("EMAIL_IMAP_PORT") or provider.get("imap_port", 993)),
        smtp_host=args.smtp_host or os.getenv("EMAIL_SMTP_HOST") or provider.get("smtp_host", ""),
        smtp_port=int(args.smtp_port or os.getenv("EMAIL_SMTP_PORT") or provider.get("smtp_port", 465 if smtp_ssl else 587)),
        smtp_ssl=smtp_ssl,
        provider=provider_key,
    )


def require_hosts(config: MailConfig) -> None:
    if not config.imap_host:
        raise ValueError("Missing IMAP host. Pass --imap-host, --provider, or EMAIL_IMAP_HOST.")
    if not config.smtp_host:
        raise ValueError("Missing SMTP host. Pass --smtp-host, --provider, or EMAIL_SMTP_HOST.")


def refresh_access_token(config: MailConfig) -> dict:
    if not config.refresh_token:
        raise ValueError("Missing refresh token.")
    if not config.token_endpoint:
        raise ValueError("Missing token endpoint. Set --token-endpoint or EMAIL_TOKEN_ENDPOINT.")
    if not config.client_id:
        raise ValueError("Missing client id. Set --client-id or EMAIL_CLIENT_ID.")

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": config.refresh_token,
        "client_id": config.client_id,
    }
    if config.client_secret:
        payload["client_secret"] = config.client_secret
    if config.scope:
        payload["scope"] = config.scope

    data = urllib.parse.urlencode(payload).encode("utf-8")
    request = urllib.request.Request(
        config.token_endpoint,
        data=data,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Token refresh failed: HTTP {exc.code} {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Token refresh failed: {exc.reason}") from exc

    parsed = json.loads(body)
    token = parsed.get("access_token")
    if not token:
        raise RuntimeError(f"Token response missing access_token: {body}")

    config.access_token = token
    new_refresh_token = parsed.get("refresh_token")
    if new_refresh_token:
        config.refresh_token = new_refresh_token
    return {
        "access_token": token,
        "expires_in": parsed.get("expires_in"),
        "refresh_token_rotated": bool(new_refresh_token),
    }


def resolve_access_token(config: MailConfig) -> tuple[str, str]:
    if config.access_token:
        return config.access_token, "provided"
    refreshed = refresh_access_token(config)
    return refreshed["access_token"], "refreshed"


def build_xoauth2_blob(email: str, access_token: str) -> bytes:
    return f"user={email}\x01auth=Bearer {access_token}\x01\x01".encode("utf-8")


def imap_authenticate(client: imaplib.IMAP4_SSL, config: MailConfig) -> str:
    if config.auth_mode == "password":
        client.login(config.email, config.password or "")
        return "password"

    access_token, token_source = resolve_access_token(config)
    xoauth2 = build_xoauth2_blob(config.email, access_token)
    status, _ = client.authenticate("XOAUTH2", lambda _: xoauth2)
    if status != "OK":
        raise RuntimeError("IMAP XOAUTH2 authentication failed.")
    return f"oauth2:{token_source}"


def smtp_authenticate(smtp: smtplib.SMTP, config: MailConfig) -> str:
    if config.auth_mode == "password":
        smtp.login(config.email, config.password or "")
        return "password"

    access_token, token_source = resolve_access_token(config)
    xoauth2 = build_xoauth2_blob(config.email, access_token)
    encoded = base64.b64encode(xoauth2).decode("ascii")
    code, message = smtp.docmd("AUTH", f"XOAUTH2 {encoded}")
    if code != 235:
        text = message.decode("utf-8", errors="replace") if isinstance(message, bytes) else str(message)
        raise RuntimeError(f"SMTP XOAUTH2 authentication failed: {code} {text}")
    return f"oauth2:{token_source}"


def run_check(config: MailConfig, mailbox: str) -> dict:
    require_hosts(config)
    result = {"imap": "unknown", "smtp": "unknown", "auth_mode": config.auth_mode}

    with imaplib.IMAP4_SSL(config.imap_host, config.imap_port) as client:
        result["imap_auth"] = imap_authenticate(client, config)
        status, _ = client.select(mailbox, readonly=True)
        if status != "OK":
            raise RuntimeError(f"IMAP select failed for mailbox {mailbox}")
        result["imap"] = "ok"

    context = ssl.create_default_context()
    if config.smtp_ssl:
        with smtplib.SMTP_SSL(config.smtp_host, config.smtp_port, timeout=30, context=context) as smtp:
            result["smtp_auth"] = smtp_authenticate(smtp, config)
            smtp.noop()
    else:
        with smtplib.SMTP(config.smtp_host, config.smtp_port, timeout=30) as smtp:
            smtp.ehlo()
            smtp.starttls(context=context)
            smtp.ehlo()
            result["smtp_auth"] = smtp_authenticate(smtp, config)
            smtp.noop()
    result["smtp"] = "ok"
    return result


def build_search_criteria(args: argparse.Namespace) -> list[str]:
    criteria: list[str] = []
    if args.unseen:
        criteria.append("UNSEEN")
    if args.since:
        criteria.extend(["SINCE", imap_date(args.since)])
    if args.sender:
        criteria.extend(["FROM", f'"{args.sender}"'])
    if args.subject:
        criteria.extend(["SUBJECT", f'"{args.subject}"'])
    if not criteria:
        criteria.append("ALL")
    return criteria


def run_list(config: MailConfig, args: argparse.Namespace) -> dict:
    require_hosts(config)
    with imaplib.IMAP4_SSL(config.imap_host, config.imap_port) as client:
        imap_authenticate(client, config)
        status, _ = client.select(args.mailbox, readonly=True)
        if status != "OK":
            raise RuntimeError(f"Cannot open mailbox {args.mailbox}")

        criteria = build_search_criteria(args)
        status, data = client.search(None, *criteria)
        if status != "OK":
            raise RuntimeError("IMAP search failed")
        ids = data[0].split() if data and data[0] else []
        ids = ids[-args.limit :]
        items = []
        for msg_id in ids:
            header_status, header_data = client.fetch(msg_id, "(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE)])")
            uid_status, uid_data = client.fetch(msg_id, "(UID)")
            if header_status != "OK" or uid_status != "OK" or not header_data:
                continue
            payload = None
            for block in header_data:
                if isinstance(block, tuple) and isinstance(block[1], bytes):
                    payload = block[1]
                    break
            if payload is None:
                continue
            msg = BytesParser(policy=policy.default).parsebytes(payload)
            uid = extract_uid(uid_data)
            items.append(
                {
                    "uid": uid,
                    "from": decode_header_value(msg.get("From")),
                    "subject": decode_header_value(msg.get("Subject")),
                    "date": decode_header_value(msg.get("Date")),
                }
            )
        return {"count": len(items), "mailbox": args.mailbox, "messages": items}


def run_read(config: MailConfig, args: argparse.Namespace) -> dict:
    require_hosts(config)
    with imaplib.IMAP4_SSL(config.imap_host, config.imap_port) as client:
        imap_authenticate(client, config)
        status, _ = client.select(args.mailbox, readonly=not args.mark_read)
        if status != "OK":
            raise RuntimeError(f"Cannot open mailbox {args.mailbox}")

        fetch_selector = "(RFC822)" if args.mark_read else "(BODY.PEEK[])"
        status, data = client.uid("fetch", args.uid, fetch_selector)
        if status != "OK" or not data:
            raise RuntimeError(f"Cannot read UID {args.uid}")

        payload = None
        for block in data:
            if isinstance(block, tuple) and isinstance(block[1], bytes):
                payload = block[1]
                break
        if payload is None:
            raise RuntimeError(f"Message payload missing for UID {args.uid}")

        msg = BytesParser(policy=policy.default).parsebytes(payload)
        body = collect_text_body(msg, args.max_chars)
        attachments = collect_attachments(msg)

        if args.mark_read:
            client.uid("store", args.uid, "+FLAGS", "(\\Seen)")

        return {
            "uid": args.uid,
            "from": decode_header_value(msg.get("From")),
            "to": decode_header_value(msg.get("To")),
            "subject": decode_header_value(msg.get("Subject")),
            "date": decode_header_value(msg.get("Date")),
            "body": body,
            "attachments": attachments,
            "marked_read": bool(args.mark_read),
        }


def run_send(config: MailConfig, args: argparse.Namespace) -> dict:
    require_hosts(config)
    msg = EmailMessage()
    msg["From"] = config.email
    msg["To"] = ", ".join(args.to)
    if args.cc:
        msg["Cc"] = ", ".join(args.cc)
    msg["Subject"] = args.subject

    plain_body = args.body or ""
    msg.set_content(plain_body)
    if args.html_file:
        html_content = Path(args.html_file).read_text(encoding="utf-8")
        msg.add_alternative(html_content, subtype="html")

    for file_path in args.attach or []:
        path = Path(file_path)
        content = path.read_bytes()
        mime_type, _ = mimetypes.guess_type(path.name)
        if mime_type:
            maintype, subtype = mime_type.split("/", 1)
        else:
            maintype, subtype = "application", "octet-stream"
        msg.add_attachment(content, maintype=maintype, subtype=subtype, filename=path.name)

    recipients = list(args.to) + list(args.cc or []) + list(args.bcc or [])
    context = ssl.create_default_context()
    if config.smtp_ssl:
        with smtplib.SMTP_SSL(config.smtp_host, config.smtp_port, timeout=30, context=context) as smtp:
            smtp_authenticate(smtp, config)
            smtp.send_message(msg, to_addrs=recipients)
    else:
        with smtplib.SMTP(config.smtp_host, config.smtp_port, timeout=30) as smtp:
            smtp.ehlo()
            smtp.starttls(context=context)
            smtp.ehlo()
            smtp_authenticate(smtp, config)
            smtp.send_message(msg, to_addrs=recipients)

    return {
        "status": "sent",
        "auth_mode": config.auth_mode,
        "subject": args.subject,
        "to": args.to,
        "cc": args.cc or [],
        "bcc_count": len(args.bcc or []),
        "attachments": [Path(p).name for p in (args.attach or [])],
    }


def run_token(config: MailConfig, show_token: bool) -> dict:
    if config.auth_mode != "oauth2":
        raise ValueError("token command requires oauth2 auth mode.")
    access_token, token_source = resolve_access_token(config)
    if not show_token:
        if len(access_token) > 18:
            masked = f"{access_token[:8]}...{access_token[-6:]}"
        else:
            masked = "***"
    else:
        masked = access_token
    return {
        "provider": config.provider,
        "auth_mode": config.auth_mode,
        "token_source": token_source,
        "access_token": masked,
        "refresh_token_present": bool(config.refresh_token),
    }


def parse_extra_oauth_params(raw_params: list[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for item in raw_params:
        if "=" not in item:
            raise ValueError(f"Invalid --param value {item!r}. Expected key=value.")
        key, value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError("OAuth parameter key cannot be empty.")
        parsed[key] = value
    return parsed


def run_auth_url(args: argparse.Namespace) -> dict:
    provider_key = (args.provider or os.getenv("EMAIL_PROVIDER", "")).strip().lower() or None
    provider = get_provider_defaults(provider_key)
    oauth_defaults = provider.get("oauth", {})

    client_id = args.client_id or os.getenv("EMAIL_CLIENT_ID")
    if not client_id:
        raise ValueError("Missing client id. Set --client-id or EMAIL_CLIENT_ID.")

    redirect_uri = args.redirect_uri or os.getenv("EMAIL_REDIRECT_URI")
    if not redirect_uri:
        raise ValueError("Missing redirect URI. Set --redirect-uri or EMAIL_REDIRECT_URI.")

    auth_endpoint = args.auth_endpoint or os.getenv("EMAIL_AUTH_ENDPOINT") or oauth_defaults.get("auth_endpoint")
    if not auth_endpoint:
        raise ValueError("Missing auth endpoint. Set --auth-endpoint, EMAIL_AUTH_ENDPOINT, or choose a provider with OAuth preset.")

    scope = args.scope or os.getenv("EMAIL_SCOPE") or oauth_defaults.get("scope")
    if not scope:
        raise ValueError("Missing scope. Set --scope, EMAIL_SCOPE, or choose a provider with OAuth scope preset.")

    state = args.state or os.getenv("EMAIL_OAUTH_STATE") or secrets.token_urlsafe(24)
    response_type = args.response_type or "code"

    query_params: dict[str, str] = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": response_type,
        "scope": scope,
        "state": state,
    }

    login_hint = args.login_hint or args.email or os.getenv("EMAIL_ADDRESS")
    if login_hint:
        query_params["login_hint"] = login_hint
    if args.prompt:
        query_params["prompt"] = args.prompt

    access_type = args.access_type or os.getenv("EMAIL_ACCESS_TYPE")
    if access_type:
        query_params["access_type"] = access_type

    include_granted_scopes = args.include_granted_scopes
    if not include_granted_scopes:
        env_value = os.getenv("EMAIL_INCLUDE_GRANTED_SCOPES")
        if env_value:
            include_granted_scopes = parse_bool(env_value)
    if include_granted_scopes:
        query_params["include_granted_scopes"] = "true"

    nonce: str | None = None
    if provider_key in {"yahoo", "aol"}:
        nonce = args.nonce or os.getenv("EMAIL_NONCE") or secrets.token_urlsafe(24)
        query_params["nonce"] = nonce

    extras = parse_extra_oauth_params(args.param or [])
    for key, value in extras.items():
        if key in query_params:
            raise ValueError(f"OAuth parameter {key!r} is already set by built-in options.")
        query_params[key] = value

    authorization_url = f"{auth_endpoint}?{urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)}"
    result = {
        "provider": provider_key or "",
        "auth_endpoint": auth_endpoint,
        "scope": scope,
        "state": state,
        "authorization_url": authorization_url,
    }
    if nonce:
        result["nonce"] = nonce
    return result


def print_result(result: dict, output_format: str) -> None:
    if output_format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if "messages" in result:
        print(f"Mailbox: {result['mailbox']}")
        print(f"Messages: {result['count']}")
        for item in result["messages"]:
            print(f"- UID {item['uid']} | {item['date']} | {item['from']} | {item['subject']}")
        return

    for key, value in result.items():
        if isinstance(value, (list, dict)):
            rendered = json.dumps(value, ensure_ascii=False)
        else:
            rendered = str(value)
        print(f"{key}: {rendered}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="IMAP/SMTP mailbox operations")
    parser.add_argument("--provider", choices=sorted(PROVIDER_PRESETS.keys()), help="Provider preset name")
    parser.add_argument("--email", help="Mailbox login email")
    parser.add_argument("--auth-mode", choices=["auto", "password", "oauth2"], default="auto", help="Authentication mode")
    parser.add_argument("--password", help="Mailbox password or app password")
    parser.add_argument("--access-token", help="OAuth2 access token")
    parser.add_argument("--refresh-token", help="OAuth2 refresh token")
    parser.add_argument("--token-endpoint", help="OAuth2 token endpoint for refresh")
    parser.add_argument("--client-id", help="OAuth2 client id")
    parser.add_argument("--client-secret", help="OAuth2 client secret")
    parser.add_argument("--scope", help="OAuth2 scope for token refresh")
    parser.add_argument("--redirect-uri", help="OAuth2 redirect URI")
    parser.add_argument("--auth-endpoint", help="OAuth2 authorization endpoint")
    parser.add_argument("--imap-host", help="IMAP host override")
    parser.add_argument("--imap-port", type=int, help="IMAP port override")
    parser.add_argument("--smtp-host", help="SMTP host override")
    parser.add_argument("--smtp-port", type=int, help="SMTP port override")
    parser.add_argument("--smtp-ssl", action="store_true", help="Use SSL for SMTP")
    parser.add_argument("--smtp-starttls", action="store_true", help="Use STARTTLS for SMTP")
    parser.add_argument("--output", choices=["text", "json"], default="text")

    subparsers = parser.add_subparsers(dest="command", required=True)

    p_check = subparsers.add_parser("check", help="Check IMAP/SMTP login connectivity")
    p_check.add_argument("--mailbox", default="INBOX", help="Mailbox to select for check")

    p_list = subparsers.add_parser("list", help="List email summaries")
    p_list.add_argument("--mailbox", default="INBOX", help="Mailbox folder")
    p_list.add_argument("--limit", type=int, default=20, help="Max messages to return")
    p_list.add_argument("--unseen", action="store_true", help="Only unread messages")
    p_list.add_argument("--since", help="Filter since date (YYYY-MM-DD)")
    p_list.add_argument("--sender", help="Filter by sender")
    p_list.add_argument("--subject", help="Filter by subject keyword")

    p_read = subparsers.add_parser("read", help="Read an email by UID")
    p_read.add_argument("--mailbox", default="INBOX", help="Mailbox folder")
    p_read.add_argument("--uid", required=True, help="IMAP UID")
    p_read.add_argument("--mark-read", action="store_true", help="Mark as read after fetching")
    p_read.add_argument("--max-chars", type=int, default=4000, help="Max body length")

    p_send = subparsers.add_parser("send", help="Send an email")
    p_send.add_argument("--to", nargs="+", required=True, help="Recipient emails")
    p_send.add_argument("--cc", nargs="*", default=[], help="CC recipient emails")
    p_send.add_argument("--bcc", nargs="*", default=[], help="BCC recipient emails")
    p_send.add_argument("--subject", required=True, help="Subject line")
    p_send.add_argument("--body", default="", help="Plain text body")
    p_send.add_argument("--html-file", help="Path to HTML body file")
    p_send.add_argument("--attach", action="append", help="Attachment path (repeatable)")

    p_token = subparsers.add_parser("token", help="Resolve OAuth2 access token")
    p_token.add_argument("--show-token", action="store_true", help="Print full token instead of masked output")

    p_auth = subparsers.add_parser("auth-url", help="Build OAuth2 authorization URL")
    p_auth.add_argument("--response-type", default="code", help="OAuth2 response_type")
    p_auth.add_argument("--state", help="OAuth2 state (auto-generated if omitted)")
    p_auth.add_argument("--nonce", help="OAuth2 nonce (auto-generated for yahoo/aol)")
    p_auth.add_argument("--login-hint", help="OAuth2 login hint, usually an email")
    p_auth.add_argument("--prompt", help="OAuth2 prompt parameter")
    p_auth.add_argument("--access-type", help="OAuth2 access_type parameter")
    p_auth.add_argument("--include-granted-scopes", action="store_true", help="Set include_granted_scopes=true")
    p_auth.add_argument("--param", action="append", default=[], help="Extra OAuth2 query parameter as key=value (repeatable)")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "auth-url":
            result = run_auth_url(args)
        else:
            config = resolve_config(args)
            if args.command == "check":
                result = run_check(config, args.mailbox)
            elif args.command == "list":
                result = run_list(config, args)
            elif args.command == "read":
                result = run_read(config, args)
            elif args.command == "send":
                result = run_send(config, args)
            elif args.command == "token":
                result = run_token(config, args.show_token)
            else:
                raise RuntimeError(f"Unsupported command: {args.command}")

        print_result(result, args.output)
        return 0
    except Exception as exc:  # noqa: BLE001
        if args.output == "json":
            print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        else:
            print(f"error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
