import imaplib
import json
import re
import ssl
import sys
from email import policy
from email.header import decode_header, make_header
from email.message import Message
from email.parser import BytesParser
from typing import Any

from .errors import SkillError
from .auth import _detect_auth_type, _get_password_from_env, _get_username_from_env, _get_oauth2_from_env, get_oauth2_token


def _stderr_log(payload: dict[str, Any]) -> None:
    sys.stderr.write(json.dumps(payload, ensure_ascii=True) + "\n")


def connect_imap(account_cfg: dict[str, Any]) -> imaplib.IMAP4_SSL | imaplib.IMAP4:
    imap_cfg = account_cfg["imap"]

    host = imap_cfg.get("host")
    port = imap_cfg.get("port")
    tls = bool(imap_cfg.get("tls", True))
    starttls = bool(imap_cfg.get("starttls", False))
    timeout = imap_cfg.get("timeout", account_cfg.get("timeout", 30))
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
            client: imaplib.IMAP4_SSL | imaplib.IMAP4 = imaplib.IMAP4_SSL(
                host, int(port), timeout=int(timeout), ssl_context=ssl_context
            )
        else:
            client = imaplib.IMAP4(host, int(port), timeout=int(timeout))
            if starttls:
                client.starttls(ssl_context)

        # Authenticate
        auth_type = _detect_auth_type()
        if auth_type == "oauth2":
            email = account_cfg.get("email")
            oauth_cfg = _get_oauth2_from_env({})
            access_token = get_oauth2_token(oauth_cfg)
            auth_string = f"user={email}\1auth=Bearer {access_token}\1\1"
            auth_bytes = auth_string.encode("utf-8")
            status, detail = client.authenticate("XOAUTH2", lambda x=None: auth_bytes)
        else:
            username = _get_username_from_env()
            password = _get_password_from_env()
            if not username:
                raise SkillError("AUTH_ERROR", "Username not configured. Set EMAIL_USERNAME environment variable.")
            if not password:
                raise SkillError("AUTH_ERROR", "Password not configured. Set EMAIL_PASSWORD environment variable.")
            status, detail = client.login(str(username), str(password))

        if status != "OK":
            _stderr_log(
                {
                    "level": "ERROR",
                    "code": "AUTH_ERROR",
                    "phase": "imap.login",
                    "status": status,
                    "detail": str(detail),
                }
            )
            raise SkillError("AUTH_ERROR", f"IMAP login failed ({auth_type})")

        return client
    except imaplib.IMAP4.error as exc:
        _stderr_log(
            {
                "level": "ERROR",
                "code": "AUTH_ERROR",
                "phase": "imap.auth",
                "message": str(exc),
            }
        )
        raise SkillError("AUTH_ERROR", "IMAP authentication failed") from exc
    except OSError as exc:
        _stderr_log(
            {
                "level": "ERROR",
                "code": "NETWORK_ERROR",
                "phase": "imap.connection",
                "message": str(exc),
            }
        )
        raise SkillError("NETWORK_ERROR", "IMAP connection failed") from exc


def close_imap_safely(client: imaplib.IMAP4_SSL | imaplib.IMAP4) -> None:
    try:
        client.logout()
    except Exception as exc:
        sys.stderr.write(
            json.dumps(
                {
                    "level": "WARN",
                    "code": "CLEANUP_ERROR",
                    "phase": "imap.logout",
                    "message": str(exc),
                    "type": type(exc).__name__,
                }
            )
            + "\n"
        )


def select_mailbox(client: imaplib.IMAP4_SSL | imaplib.IMAP4, mailbox: str) -> None:
    candidates = [mailbox, f'"{mailbox}"']

    for name in candidates:
        status, detail = client.select(name)
        if status == "OK":
            return

    list_status, list_detail = client.list()
    decoded_list = []
    if list_status == "OK" and list_detail:
        decoded_list = [_safe_decode(row) for row in list_detail if isinstance(row, bytes)]

    raise SkillError(
        "MAILBOX_ERROR",
        f"Unable to select mailbox: {mailbox}",
        {
            "mailbox": mailbox,
            "attempted": candidates,
            "listStatus": list_status,
            "mailboxes": decoded_list,
        },
    )


def _safe_decode(raw: bytes) -> str:
    return raw.decode("utf-8", errors="replace")


def _decode_imap_value(raw: bytes | bytearray | str | None) -> str:
    if raw is None:
        return ""
    if isinstance(raw, (bytes, bytearray)):
        return bytes(raw).decode("utf-8", errors="replace")
    return str(raw)


def _parse_imap_list(raw: str) -> list[str]:
    items: list[str] = []
    token: list[str] = []
    in_quotes = False
    escape = False

    for char in raw:
        if escape:
            token.append(char)
            escape = False
            continue
        if in_quotes:
            if char == "\\":
                escape = True
            elif char == '"':
                in_quotes = False
            else:
                token.append(char)
            continue
        if char == '"':
            in_quotes = True
            continue
        if char.isspace():
            if token:
                items.append("".join(token))
                token = []
            continue
        token.append(char)

    if token:
        items.append("".join(token))
    return items


def _extract_fetch_list(descriptor: str, attribute: str) -> list[str]:
    match = re.search(rf"{re.escape(attribute)} \((.*?)\)", descriptor)
    if not match:
        return []
    return _parse_imap_list(match.group(1))


def extract_fetch_tags(fetch_rows: list[Any] | tuple[Any, ...]) -> dict[str, list[str]]:
    flags: list[str] = []
    gmail_labels: list[str] = []

    for row in fetch_rows:
        descriptor: str | None = None
        if isinstance(row, tuple) and row:
            descriptor = _decode_imap_value(row[0])
        elif isinstance(row, (bytes, bytearray, str)):
            descriptor = _decode_imap_value(row)
        if not descriptor:
            continue

        flags = _extract_fetch_list(descriptor, "FLAGS") or flags
        gmail_labels = _extract_fetch_list(descriptor, "X-GM-LABELS") or gmail_labels

    system_tags = [item for item in flags if item.startswith("\\")]
    keywords = [item for item in flags if not item.startswith("\\")]

    tags: list[str] = []
    for item in [*flags, *gmail_labels]:
        if item not in tags:
            tags.append(item)

    return {
        "flags": flags,
        "systemTags": system_tags,
        "keywords": keywords,
        "gmailLabels": gmail_labels,
        "tags": tags,
    }


def decode_mime_header(value: str | None) -> str:
    if not value:
        return ""
    return str(make_header(decode_header(value)))


def get_imap_capabilities(client: imaplib.IMAP4_SSL | imaplib.IMAP4) -> set[str]:
    capabilities = getattr(client, "capabilities", ())
    normalized: set[str] = set()
    for item in capabilities:
        if isinstance(item, bytes):
            normalized.add(item.decode("utf-8", errors="replace").upper())
        else:
            normalized.add(str(item).upper())
    return normalized


def expunge_uids_safely(
    client: imaplib.IMAP4_SSL | imaplib.IMAP4,
    uids: str,
    *,
    folder: str,
) -> list[str]:
    capabilities = get_imap_capabilities(client)
    if "UIDPLUS" not in capabilities:
        raise SkillError(
            "MAIL_OPERATION_ERROR",
            "Safe expunge requires IMAP UIDPLUS support",
            {
                "folder": folder,
                "uids": uids.split(","),
                "capabilities": sorted(capabilities),
            },
        )

    expunged_uids: list[str] = []
    failed: list[dict[str, str]] = []
    for uid in uids.split(","):
        status, detail = client.uid("EXPUNGE", uid)
        if status == "OK":
            expunged_uids.append(uid)
        else:
            failed.append({"uid": uid, "status": str(status), "detail": str(detail)})

    if failed:
        raise SkillError(
            "MAIL_OPERATION_ERROR",
            "Failed to expunge one or more mails safely",
            {
                "folder": folder,
                "expungedUids": expunged_uids,
                "failed": failed,
            },
        )

    return expunged_uids


def fetch_original_message(
    client: imaplib.IMAP4_SSL | imaplib.IMAP4,
    uid: str,
    folder: str,
    use_body_peek: bool = True,
) -> Message:
    """
    Fetch and parse an email message from IMAP.
    
    Args:
        client: Connected IMAP client
        uid: Message UID
        folder: Mailbox folder name
        use_body_peek: If True, use BODY.PEEK to avoid marking as read
        
    Returns:
        Parsed email message
        
    Raises:
        SkillError: If fetch fails or no content found
    """
    body_field = "BODY.PEEK[]" if use_body_peek else "BODY[]"
    status, fetched = client.uid("FETCH", uid, f"({body_field})")
    
    if status != "OK" or not fetched:
        raise SkillError(
            "MAIL_OPERATION_ERROR",
            "Failed to fetch message",
            {"status": status, "uid": uid, "folder": folder},
        )
    
    raw_msg = None
    for row in fetched:
        if isinstance(row, tuple) and len(row) >= 2 and isinstance(row[1], (bytes, bytearray)):
            raw_msg = bytes(row[1])
            break
    
    if raw_msg is None:
        raise SkillError("MAIL_OPERATION_ERROR", "No RFC822 content found", {"uid": uid})
    
    return BytesParser(policy=policy.default).parsebytes(raw_msg)
