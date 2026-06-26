#!/usr/bin/env python3
import argparse
import csv
import html
import json
import os
import re
import socket
import sys
from email import policy
from email.header import decode_header, make_header
from email.parser import BytesParser
from io import StringIO
from pathlib import Path
from typing import Any, Iterable, Optional
from urllib import error, parse, request


DEFAULT_API_URL = "https://mail-api.suilong.online/admin/mails"
ENV_ADMIN_AUTH = "CLOUDFLARE_MAIL_ADMIN_AUTH"
ENV_BEARER_TOKEN = "CLOUDFLARE_MAIL_BEARER_TOKEN"
ENV_CUSTOM_AUTH = "CLOUDFLARE_MAIL_CUSTOM_AUTH"
ENV_FINGERPRINT = "CLOUDFLARE_MAIL_FINGERPRINT"
ENV_LANG = "CLOUDFLARE_MAIL_LANG"
ENV_USER_TOKEN = "CLOUDFLARE_MAIL_USER_TOKEN"
ENV_API_URL = "CLOUDFLARE_MAIL_MAILS_API_URL"

EMAIL_RE = re.compile(
    r"^[A-Za-z0-9](?:[A-Za-z0-9._%+-]{0,62}[A-Za-z0-9])?@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}$"
)
HTML_TAG_RE = re.compile(r"<[^>]+>")
HTML_SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.IGNORECASE | re.DOTALL)
CODE_CONTEXT_PATTERNS = [
    re.compile(
        r"(?:验证码|校验码|验证代码|动态码|动态口令|一次性密码|OTP|one[-\s]?time(?:\s+password)?|verification\s*code|security\s*code|passcode)"
        r"[^A-Za-z0-9]{0,20}([A-Za-z0-9]{4,10})",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b([A-Za-z0-9]{4,10})\b[^A-Za-z0-9]{0,12}(?:为|是|:)?\s*"
        r"(?:验证码|校验码|验证代码|动态码|动态口令|一次性密码|OTP|verification\s*code|security\s*code|passcode)",
        re.IGNORECASE,
    ),
]
CODE_KEYWORD_RE = re.compile(
    r"(?:验证码|校验码|验证代码|动态码|动态口令|一次性密码|OTP|one[-\s]?time|verification\s*code|security\s*code|passcode)",
    re.IGNORECASE,
)
NUMERIC_CODE_RE = re.compile(r"\b(\d{4,8})\b")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read Cloudflare temporary mail messages through the admin API."
    )
    parser.add_argument("--address", help="Mailbox address to filter by.")
    parser.add_argument("--limit", type=int, default=20, help="Number of messages to fetch. Defaults to 20.")
    parser.add_argument("--offset", type=int, default=0, help="Pagination offset. Defaults to 0.")
    parser.add_argument("--admin-auth", help="Value for the x-admin-auth header.")
    parser.add_argument("--bearer-token", help="Bearer token without or with the Bearer prefix.")
    parser.add_argument("--custom-auth", help="Optional x-custom-auth header value.")
    parser.add_argument("--fingerprint", help="Optional x-fingerprint header.")
    parser.add_argument("--lang", help="Optional x-lang header.")
    parser.add_argument("--user-token", help="Optional x-user-token header.")
    parser.add_argument(
        "--api-url",
        default=os.getenv(ENV_API_URL, DEFAULT_API_URL),
        help=f"Admin API URL. Defaults to {DEFAULT_API_URL}.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=15.0,
        help="Request timeout in seconds. Defaults to 15.",
    )
    parser.add_argument(
        "--preview-length",
        type=int,
        default=200,
        help="Maximum characters to keep in the preview field. Defaults to 200.",
    )
    parser.add_argument(
        "--include-raw",
        action="store_true",
        help="Include each original raw item in the normalized JSON output.",
    )
    parser.add_argument(
        "--output-format",
        choices=("json", "csv"),
        default="json",
        help="Output format. Defaults to json.",
    )
    parser.add_argument(
        "--output-file",
        help="Optional path to write the formatted output.",
    )
    return parser


def first_non_empty(*values: Any) -> Optional[Any]:
    for value in values:
        if value is None:
            continue
        if isinstance(value, str) and not value.strip():
            continue
        return value
    return None


def decode_mime_header(value: Any) -> Optional[str]:
    text = ensure_text(value)
    if not text:
        return None
    try:
        return str(make_header(decode_header(text))).strip() or None
    except Exception:
        return text


def ensure_text(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        text = value.strip()
        return text or None
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, list):
        parts = [ensure_text(item) for item in value]
        cleaned = [part for part in parts if part]
        return ", ".join(cleaned) if cleaned else None
    if isinstance(value, dict):
        for key in ("address", "email", "name", "text", "value"):
            candidate = ensure_text(value.get(key))
            if candidate:
                return candidate
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def csv_cell(value: Any) -> Any:
    return "" if value is None else value


def html_to_text(html_body: Optional[str]) -> Optional[str]:
    if not html_body:
        return None
    cleaned = HTML_SCRIPT_STYLE_RE.sub(" ", html_body)
    cleaned = HTML_TAG_RE.sub(" ", cleaned)
    cleaned = html.unescape(cleaned)
    normalized = " ".join(cleaned.split())
    return normalized or None


def is_plausible_code(candidate: str) -> bool:
    if not (4 <= len(candidate) <= 10):
        return False
    if not re.fullmatch(r"[A-Za-z0-9]+", candidate):
        return False
    # Most verification codes include at least one digit; this filters random words.
    if not any(ch.isdigit() for ch in candidate):
        return False
    return True


def extract_verification_code(subject: Optional[str], text_body: Optional[str], html_body: Optional[str]) -> Optional[str]:
    sources = [subject, text_body, html_to_text(html_body)]
    for source in sources:
        if not source:
            continue
        for pattern in CODE_CONTEXT_PATTERNS:
            match = pattern.search(source)
            if not match:
                continue
            candidate = match.group(1).strip()
            if is_plausible_code(candidate):
                return candidate

    merged = " ".join([segment for segment in sources if segment])
    if not merged or not CODE_KEYWORD_RE.search(merged):
        return None

    seen = []
    for candidate in NUMERIC_CODE_RE.findall(merged):
        if candidate not in seen:
            seen.append(candidate)
    return seen[0] if seen else None


def decode_payload_bytes(payload_bytes: Optional[bytes], charset: Optional[str]) -> Optional[str]:
    if payload_bytes is None:
        return None
    encodings = []
    if charset:
        encodings.append(charset)
    encodings.extend(["utf-8", "gb18030", "gbk", "latin-1"])
    for encoding in encodings:
        try:
            text = payload_bytes.decode(encoding)
            return text.strip() or None
        except (LookupError, UnicodeDecodeError):
            continue
    return payload_bytes.decode("utf-8", errors="replace").strip() or None


def parse_raw_email(raw_email: Optional[str]) -> dict[str, Optional[str]]:
    if not raw_email:
        return {
            "message_id": None,
            "from": None,
            "to": None,
            "subject": None,
            "date": None,
            "text": None,
            "html": None,
        }

    try:
        message = BytesParser(policy=policy.default).parsebytes(raw_email.encode("utf-8", errors="replace"))
    except Exception:
        return {
            "message_id": None,
            "from": None,
            "to": None,
            "subject": None,
            "date": None,
            "text": None,
            "html": None,
        }

    text_body = None
    html_body = None
    if message.is_multipart():
        for part in message.walk():
            if part.get_content_maintype() == "multipart":
                continue
            content_type = part.get_content_type()
            payload_bytes = part.get_payload(decode=True)
            decoded = decode_payload_bytes(payload_bytes, part.get_content_charset())
            if not decoded:
                continue
            if content_type == "text/plain" and text_body is None:
                text_body = decoded
            elif content_type == "text/html" and html_body is None:
                html_body = decoded
    else:
        decoded = decode_payload_bytes(message.get_payload(decode=True), message.get_content_charset())
        if message.get_content_type() == "text/html":
            html_body = decoded
        else:
            text_body = decoded

    return {
        "message_id": decode_mime_header(message.get("Message-ID")),
        "from": decode_mime_header(message.get("From")),
        "to": decode_mime_header(message.get("To")),
        "subject": decode_mime_header(message.get("Subject")),
        "date": decode_mime_header(message.get("Date")),
        "text": text_body,
        "html": html_body,
    }


def truncate_preview(text: Optional[str], preview_length: int) -> Optional[str]:
    if not text:
        return None
    normalized = " ".join(text.split())
    if len(normalized) <= preview_length:
        return normalized
    return normalized[: max(0, preview_length - 3)].rstrip() + "..."


def normalize_address(value: Optional[str]) -> tuple[Optional[str], Optional[str]]:
    if value is None:
        return None, None
    address = value.strip().lower()
    if not address:
        return None, None
    if not EMAIL_RE.match(address):
        return None, "address is invalid"
    return address, None


def validate_pagination(limit: int, offset: int) -> Optional[str]:
    if limit <= 0:
        return "limit must be greater than 0"
    if offset < 0:
        return "offset must be 0 or greater"
    return None


def load_json_bytes(raw_bytes: bytes) -> Optional[Any]:
    if not raw_bytes:
        return None
    try:
        return json.loads(raw_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None


def extract_error_message(status_code: Optional[int], raw_bytes: bytes, fallback: str) -> str:
    payload = load_json_bytes(raw_bytes)
    if isinstance(payload, dict):
        for key in ("error", "message", "detail"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    body_text = raw_bytes.decode("utf-8", errors="replace").strip()
    if body_text:
        return body_text
    if status_code is not None:
        return f"http {status_code}: {fallback}"
    return fallback


def classify_error(status_code: Optional[int], message: str) -> str:
    normalized = message.lower()
    if status_code in {401, 403}:
        return "auth_error"
    if any(token in normalized for token in ("unauthorized", "forbidden", "auth", "token", "credential")):
        return "auth_error"
    return "error"


def build_headers(args: argparse.Namespace) -> tuple[Optional[dict[str, str]], Optional[str]]:
    admin_auth = args.admin_auth or os.getenv(ENV_ADMIN_AUTH)
    if not admin_auth:
        return None, f"missing admin credential: provide --admin-auth or {ENV_ADMIN_AUTH}"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "x-admin-auth": admin_auth,
    }

    bearer_token = args.bearer_token or os.getenv(ENV_BEARER_TOKEN)
    if bearer_token:
        token = bearer_token.strip()
        if token:
            headers["Authorization"] = token if token.lower().startswith("bearer ") else f"Bearer {token}"

    custom_auth = args.custom_auth or os.getenv(ENV_CUSTOM_AUTH)
    if custom_auth:
        headers["x-custom-auth"] = custom_auth

    fingerprint = args.fingerprint or os.getenv(ENV_FINGERPRINT)
    if fingerprint:
        headers["x-fingerprint"] = fingerprint

    lang = args.lang or os.getenv(ENV_LANG)
    if lang:
        headers["x-lang"] = lang

    user_token = args.user_token or os.getenv(ENV_USER_TOKEN)
    if user_token:
        headers["x-user-token"] = user_token

    return headers, None


def query_payload(address: Optional[str], limit: int, offset: int) -> dict[str, Any]:
    return {
        "address": address,
        "limit": limit,
        "offset": offset,
    }


def error_payload(status: str, message: str, address: Optional[str], limit: int, offset: int) -> dict[str, Any]:
    return {
        "status": status,
        "query": query_payload(address, limit, offset),
        "summary": {
            "count": 0,
            "limit": limit,
            "offset": offset,
        },
        "results": [],
        "error": message,
    }


def coerce_items(payload: Any) -> list[Any]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("mails", "messages", "items", "results", "data", "list"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
            if isinstance(value, dict):
                nested = coerce_items(value)
                if nested:
                    return nested
    return []


def maybe_total(payload: Any, fallback_count: int) -> int:
    if isinstance(payload, dict):
        for key in ("total", "count", "totalCount"):
            value = payload.get(key)
            if isinstance(value, int):
                return value
            if isinstance(value, dict):
                nested = value.get("total")
                if isinstance(nested, int):
                    return nested
    return fallback_count


def normalize_mail_item(item: Any, requested_address: Optional[str], preview_length: int, include_raw: bool) -> dict[str, Any]:
    if not isinstance(item, dict):
        text_value = ensure_text(item)
        normalized = {
            "id": None,
            "address": requested_address,
            "from": None,
            "to": None,
            "subject": None,
            "date": None,
            "preview": truncate_preview(text_value, preview_length),
            "text": text_value,
            "html": None,
            "verification_code": extract_verification_code(None, text_value, None),
        }
        if include_raw:
            normalized["raw"] = item
        return normalized

    headers = item.get("headers") if isinstance(item.get("headers"), dict) else {}
    envelope = item.get("envelope") if isinstance(item.get("envelope"), dict) else {}
    parsed_raw = parse_raw_email(ensure_text(item.get("raw")))

    text_body = ensure_text(
        first_non_empty(
            item.get("text"),
            item.get("textBody"),
            item.get("plain"),
            item.get("body"),
            item.get("bodyText"),
            item.get("content"),
            parsed_raw.get("text"),
        )
    )
    html_body = ensure_text(
        first_non_empty(item.get("html"), item.get("htmlBody"), item.get("bodyHtml"), parsed_raw.get("html"))
    )
    preview = ensure_text(
        first_non_empty(
            item.get("preview"),
            item.get("intro"),
            item.get("snippet"),
            item.get("excerpt"),
            text_body,
            html_body,
            parsed_raw.get("subject"),
        )
    )
    normalized = {
        "id": ensure_text(
            first_non_empty(
                item.get("id"),
                item.get("_id"),
                item.get("messageId"),
                item.get("message_id"),
                parsed_raw.get("message_id"),
            )
        ),
        "message_id": ensure_text(
            first_non_empty(
                item.get("message_id"),
                headers.get("message-id"),
                headers.get("Message-Id"),
                parsed_raw.get("message_id"),
            )
        ),
        "address": ensure_text(
            first_non_empty(
                requested_address,
                item.get("address"),
                item.get("mailAddress"),
                item.get("mailbox"),
            )
        ),
        "from": ensure_text(
            first_non_empty(
                item.get("from"),
                item.get("source"),
                item.get("sender"),
                item.get("fromAddress"),
                envelope.get("from"),
                headers.get("from"),
                headers.get("From"),
                parsed_raw.get("from"),
            )
        ),
        "to": ensure_text(
            first_non_empty(
                item.get("to"),
                item.get("recipient"),
                item.get("toAddress"),
                envelope.get("to"),
                headers.get("to"),
                headers.get("To"),
                parsed_raw.get("to"),
            )
        ),
        "subject": ensure_text(
            first_non_empty(
                item.get("subject"),
                item.get("title"),
                headers.get("subject"),
                headers.get("Subject"),
                parsed_raw.get("subject"),
            )
        ),
        "date": ensure_text(
            first_non_empty(
                item.get("createdAt"),
                item.get("created_at"),
                item.get("date"),
                item.get("receivedAt"),
                item.get("timestamp"),
                headers.get("date"),
                headers.get("Date"),
                parsed_raw.get("date"),
            )
        ),
        "source": ensure_text(first_non_empty(item.get("source"), parsed_raw.get("from"))),
        "metadata": item.get("metadata"),
        "preview": truncate_preview(preview, preview_length),
        "text": text_body,
        "html": html_body,
        "verification_code": extract_verification_code(
            subject=ensure_text(
                first_non_empty(
                    item.get("subject"),
                    item.get("title"),
                    headers.get("subject"),
                    headers.get("Subject"),
                    parsed_raw.get("subject"),
                )
            ),
            text_body=text_body,
            html_body=html_body,
        ),
    }
    if include_raw:
        normalized["raw"] = item
    return normalized


def normalize_response(
    payload: Any,
    address: Optional[str],
    limit: int,
    offset: int,
    preview_length: int,
    include_raw: bool,
) -> dict[str, Any]:
    items = coerce_items(payload)
    if not items and isinstance(payload, list):
        items = payload

    results = [
        normalize_mail_item(item, requested_address=address, preview_length=preview_length, include_raw=include_raw)
        for item in items
    ]
    return {
        "status": "ok",
        "query": query_payload(address, limit, offset),
        "summary": {
            "count": len(results),
            "total": maybe_total(payload, len(results)),
            "limit": limit,
            "offset": offset,
        },
        "results": results,
    }


def fetch_mails(
    api_url: str,
    headers: dict[str, str],
    timeout: float,
    address: Optional[str],
    limit: int,
    offset: int,
    preview_length: int,
    include_raw: bool,
) -> dict[str, Any]:
    params = {
        "limit": str(limit),
        "offset": str(offset),
    }
    if address:
        params["address"] = address
    url = f"{api_url}?{parse.urlencode(params)}"
    req = request.Request(url, headers=headers, method="GET")

    try:
        with request.urlopen(req, timeout=timeout) as response:
            raw_bytes = response.read()
            payload = load_json_bytes(raw_bytes)
            if payload is None:
                return error_payload("error", "server returned a non-JSON response", address, limit, offset)
            return normalize_response(payload, address, limit, offset, preview_length, include_raw)
    except error.HTTPError as exc:
        raw_bytes = exc.read()
        message = extract_error_message(exc.code, raw_bytes, exc.reason or "request failed")
        status = classify_error(exc.code, message)
        return error_payload(status, message, address, limit, offset)
    except error.URLError as exc:
        reason = exc.reason
        if isinstance(reason, socket.timeout):
            message = "network error: request timed out"
        else:
            message = f"network error: {reason}"
        return error_payload("error", message, address, limit, offset)
    except TimeoutError:
        return error_payload("error", "network error: request timed out", address, limit, offset)
    except Exception as exc:  # pragma: no cover
        return error_payload("error", f"unexpected error: {exc}", address, limit, offset)


def json_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)


def csv_text(payload: dict[str, Any]) -> str:
    buffer = StringIO()
    fieldnames = [
        "row_type",
        "address",
        "limit",
        "offset",
        "count",
        "total",
        "id",
        "message_id",
        "source",
        "from",
        "to",
        "subject",
        "date",
        "preview",
        "text",
        "html",
        "verification_code",
        "status",
        "error",
    ]
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()

    query = payload.get("query", {})
    summary = payload.get("summary", {})
    writer.writerow(
        {
            "row_type": "query",
            "address": csv_cell(query.get("address")),
            "limit": csv_cell(query.get("limit")),
            "offset": csv_cell(query.get("offset")),
            "count": csv_cell(summary.get("count")),
            "total": csv_cell(summary.get("total")),
            "status": csv_cell(payload.get("status")),
            "error": csv_cell(payload.get("error")),
        }
    )

    for item in payload.get("results", []):
        writer.writerow(
            {
                "row_type": "result",
                "address": csv_cell(item.get("address")),
                "id": csv_cell(item.get("id")),
                "message_id": csv_cell(item.get("message_id")),
                "source": csv_cell(item.get("source")),
                "from": csv_cell(item.get("from")),
                "to": csv_cell(item.get("to")),
                "subject": csv_cell(item.get("subject")),
                "date": csv_cell(item.get("date")),
                "preview": csv_cell(item.get("preview")),
                "text": csv_cell(item.get("text")),
                "html": csv_cell(item.get("html")),
                "verification_code": csv_cell(item.get("verification_code")),
                "status": csv_cell(payload.get("status")),
            }
        )

    return buffer.getvalue()


def emit_output(payload: dict[str, Any], output_format: str, output_file: Optional[str]) -> None:
    rendered = json_text(payload) if output_format == "json" else csv_text(payload)
    if output_file:
        path = Path(output_file)
        if path.parent and not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8", newline="")
    print(rendered, end="" if rendered.endswith("\n") else "\n")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    address, address_error = normalize_address(args.address)
    if address_error:
        payload = error_payload("error", address_error, args.address, args.limit, args.offset)
        emit_output(payload, args.output_format, args.output_file)
        return 1

    pagination_error = validate_pagination(args.limit, args.offset)
    if pagination_error:
        payload = error_payload("error", pagination_error, address, args.limit, args.offset)
        emit_output(payload, args.output_format, args.output_file)
        return 1

    if args.preview_length <= 0:
        payload = error_payload("error", "preview-length must be greater than 0", address, args.limit, args.offset)
        emit_output(payload, args.output_format, args.output_file)
        return 1

    headers, header_error = build_headers(args)
    if header_error:
        payload = error_payload("auth_error", header_error, address, args.limit, args.offset)
        emit_output(payload, args.output_format, args.output_file)
        return 1

    payload = fetch_mails(
        api_url=args.api_url,
        headers=headers,
        timeout=args.timeout,
        address=address,
        limit=args.limit,
        offset=args.offset,
        preview_length=args.preview_length,
        include_raw=args.include_raw and args.output_format == "json",
    )
    emit_output(payload, args.output_format, args.output_file)
    return 0 if payload.get("status") == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
