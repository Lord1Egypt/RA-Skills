import smtplib
import ssl
import sys
import json
import html
from email.message import EmailMessage
from email.utils import formataddr, parseaddr
from typing import Any

from .errors import SkillError
from .auth import _detect_auth_type, _get_password_from_env, _get_username_from_env, _get_oauth2_from_env, get_oauth2_token
from .parsers import html_to_text


def text_to_html(value: str) -> str:
    return "<br>".join(html.escape(line) for line in value.splitlines())


def connect_smtp(account_cfg: dict[str, Any]) -> smtplib.SMTP_SSL | smtplib.SMTP:
    smtp_cfg = account_cfg["smtp"]

    host = smtp_cfg.get("host")
    port = smtp_cfg.get("port")
    tls = bool(smtp_cfg.get("tls", True))
    starttls = bool(smtp_cfg.get("starttls", False))
    timeout = smtp_cfg.get("timeout", account_cfg.get("timeout", 30))
    ssl_verify = account_cfg.get("ssl_verify", True)
    ssl_ca_path = account_cfg.get("ssl_ca_path")

    try:
        # Create SSL context
        ssl_context = ssl.create_default_context()
        if not ssl_verify:
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
        if ssl_ca_path:
            ssl_context.load_verify_locations(ssl_ca_path)

        # Connect
        if tls:
            client: smtplib.SMTP_SSL | smtplib.SMTP = smtplib.SMTP_SSL(
                str(host), int(port), timeout=int(timeout), context=ssl_context
            )
        else:
            client = smtplib.SMTP(str(host), int(port), timeout=int(timeout))
            if starttls:
                client.starttls(context=ssl_context)

        # Authenticate
        auth_type = _detect_auth_type()
        if auth_type == "oauth2":
            email = account_cfg.get("email")
            oauth_cfg = _get_oauth2_from_env({})
            access_token = get_oauth2_token(oauth_cfg)
            auth_string = f"user={email}\1auth=Bearer {access_token}\1\1"
            client.auth("XOAUTH2", lambda x=None: auth_string)
        else:
            username = _get_username_from_env()
            password = _get_password_from_env()
            if not username:
                raise SkillError("AUTH_ERROR", "Username not configured. Set EMAIL_USERNAME environment variable.")
            if not password:
                raise SkillError("AUTH_ERROR", "Password not configured. Set EMAIL_PASSWORD environment variable.")
            client.login(str(username), str(password))

        return client
    except smtplib.SMTPAuthenticationError as exc:
        raise SkillError("AUTH_ERROR", "SMTP auth failed", {"message": str(exc)}) from exc
    except smtplib.SMTPException as exc:
        raise SkillError("NETWORK_ERROR", "SMTP protocol error", {"message": str(exc)}) from exc
    except OSError as exc:
        raise SkillError("NETWORK_ERROR", "SMTP connection failed", {"message": str(exc)}) from exc


def close_smtp_safely(client: smtplib.SMTP_SSL | smtplib.SMTP) -> None:
    try:
        client.quit()
    except Exception as exc:
        sys.stderr.write(
            json.dumps(
                {
                    "level": "WARN",
                    "code": "CLEANUP_ERROR",
                    "phase": "smtp.quit",
                    "message": str(exc),
                    "type": type(exc).__name__,
                }
            )
            + "\n"
        )


def get_sender_address(account_cfg: dict[str, Any], custom_from: Any = None) -> tuple[str, str]:
    if custom_from is not None:
        if not isinstance(custom_from, str) or not custom_from.strip():
            raise SkillError("VALIDATION_ERROR", "data.from must be a non-empty string when provided")
        custom_from_str = custom_from.strip()
        parsed_name, parsed_email = parseaddr(custom_from_str)
        if not parsed_email:
            return custom_from_str, custom_from_str
        return parsed_email, custom_from_str

    email_addr = account_cfg.get("email")
    if not isinstance(email_addr, str) or not email_addr.strip():
        raise SkillError("CONFIG_ERROR", "account email is missing")
    email_addr = email_addr.strip()

    display_name = account_cfg.get("display_name")
    if isinstance(display_name, str) and display_name.strip():
        return email_addr, formataddr((display_name.strip(), email_addr))

    return email_addr, email_addr


def get_smtp_signatures(account_cfg: dict[str, Any]) -> tuple[str | None, str | None]:
    smtp_cfg = account_cfg.get("smtp")
    if smtp_cfg is None:
        return None, None
    if not isinstance(smtp_cfg, dict):
        raise SkillError("CONFIG_ERROR", "smtp config must be an object")

    signature_cfg = smtp_cfg.get("signature")
    if signature_cfg is None:
        return None, None
    if not isinstance(signature_cfg, dict):
        raise SkillError("CONFIG_ERROR", "smtp.signature must be an object")

    # Check if signature is explicitly disabled
    if signature_cfg.get("enabled", True) is False:
        return None, None

    signature_html = signature_cfg.get("html")
    signature_text = signature_cfg.get("text")

    if signature_html is not None and not isinstance(signature_html, str):
        raise SkillError("CONFIG_ERROR", "smtp.signature.html must be a string")
    if signature_text is not None and not isinstance(signature_text, str):
        raise SkillError("CONFIG_ERROR", "smtp.signature.text must be a string")

    signature_text = signature_text.rstrip() if isinstance(signature_text, str) else ""
    signature_html = signature_html.rstrip() if isinstance(signature_html, str) else ""

    return (signature_text or None, signature_html or None)


def apply_signatures(
    body_text: str | None,
    body_html: str | None,
    signature_text: str | None,
    signature_html: str | None,
) -> tuple[str | None, str | None]:
    if not signature_text and not signature_html:
        return body_text, body_html

    # Auto-generate text signature from HTML if not provided
    if not signature_text and signature_html:
        signature_text = html_to_text(signature_html)

    # Auto-generate HTML signature from text if not provided
    if not signature_html and signature_text:
        signature_html = text_to_html(signature_text)

    signed_text = body_text
    if signature_text and body_text is not None:
        signed_text = f"{body_text}\n\n{signature_text}" if body_text else signature_text

    signed_html = body_html
    if signature_html and body_html is not None:
        signed_html = f"{body_html}<br><br>{signature_html}"

    return signed_text, signed_html


def build_message(
    sender: str,
    to_list: list[str],
    subject: str,
    body_text: str | None,
    body_html: str | None,
    cc_list: list[str] | None = None,
    bcc_list: list[str] | None = None,
    in_reply_to: str | None = None,
    references: str | None = None,
) -> EmailMessage:
    if not to_list:
        raise SkillError("VALIDATION_ERROR", "to cannot be empty")
    if not subject:
        raise SkillError("VALIDATION_ERROR", "subject cannot be empty")

    message = EmailMessage()
    message["From"] = sender
    message["To"] = ", ".join(to_list)
    message["Subject"] = subject

    if cc_list:
        message["Cc"] = ", ".join(cc_list)

    # Bcc is used for SMTP envelope recipients and should not be exposed in headers.
    _ = bcc_list

    if in_reply_to:
        message["In-Reply-To"] = in_reply_to
    if references:
        message["References"] = references

    if body_text is not None:
        message.set_content(body_text)
    elif body_html:
        message.set_content("This message contains HTML content.")
    else:
        message.set_content("")

    if body_html:
        message.add_alternative(body_html, subtype="html")

    return message
