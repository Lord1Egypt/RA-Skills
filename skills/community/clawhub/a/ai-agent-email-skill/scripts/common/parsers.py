import base64
import binascii
import html
import mimetypes
import re
from email.message import EmailMessage
from html.parser import HTMLParser
from typing import Any

from .errors import SkillError


def normalize_uids(value: Any) -> str:
    uids = _normalize_str_list(value, "uids")
    if not uids:
        raise SkillError("VALIDATION_ERROR", "uids cannot be empty")
    
    # Validate UID format: IMAP UIDs should be digits, '*', or ranges separated by ':'
    # Each UID element can be a single UID or a range (e.g., "123", "*", "1:10")
    uid_pattern = re.compile(r'^(\d+|\*)(:\d+)?$')
    
    normalized_uids = []
    for uid_entry in uids:
        # Split by comma in case a single entry contains multiple UIDs
        for uid in uid_entry.split(','):
            uid = uid.strip()
            if not uid:
                continue
            
            # Validate format
            if not uid_pattern.match(uid):
                raise SkillError(
                    "VALIDATION_ERROR",
                    f"Invalid UID format: {uid}. UIDs must be numeric, '*', or ranges (e.g., '123', '*', '1:10')"
                )
            
            # Additional validation for ranges
            if ':' in uid:
                parts = uid.split(':')
                if len(parts) != 2:
                    raise SkillError(
                        "VALIDATION_ERROR",
                        f"Invalid UID range: {uid}. Ranges must be in format 'start:end'"
                    )
                start, end = parts[0], parts[1]
                # '*' cannot be used in ranges
                if start == '*' or not end:
                    raise SkillError(
                        "VALIDATION_ERROR",
                        f"Invalid UID range: {uid}. '*' cannot be used in ranges and both ends must be numeric"
                    )
                # Validate range values
                start_num = int(start)
                end_num = int(end)
                if start_num < 1 or end_num < 1:
                    raise SkillError(
                        "VALIDATION_ERROR",
                        f"Invalid UID range: {uid}. UID values must be positive integers"
                    )
                if start_num > end_num:
                    raise SkillError(
                        "VALIDATION_ERROR",
                        f"Invalid UID range: {uid}. Start UID must be <= end UID"
                    )
            
            normalized_uids.append(uid)
    
    return ",".join(normalized_uids)


class _HTMLToTextParser(HTMLParser):
    _BLOCK_TAGS = {"p", "div", "br", "li", "tr", "table", "section", "article"}

    def __init__(self) -> None:
        super().__init__()
        self._parts: list[str] = []
        self._ignore_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del attrs
        normalized = tag.lower()
        if normalized in {"script", "style"}:
            self._ignore_depth += 1
            return
        if normalized in self._BLOCK_TAGS:
            self._parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        normalized = tag.lower()
        if normalized in {"script", "style"} and self._ignore_depth:
            self._ignore_depth -= 1
            return
        if normalized in self._BLOCK_TAGS:
            self._parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._ignore_depth or not data:
            return
        self._parts.append(data)

    def get_text(self) -> str:
        combined = "".join(self._parts)
        combined = combined.replace("\r\n", "\n").replace("\r", "\n")
        combined = re.sub(r"\n{3,}", "\n\n", combined)
        return "\n".join(line.rstrip() for line in combined.splitlines()).strip()


def _clean_surrogate_chars(text: str) -> str:
    """Remove or replace Unicode surrogate characters that cannot be encoded in UTF-8."""
    if not text:
        return text
    return text.encode("utf-8", errors="surrogatepass").decode("utf-8", errors="replace")


def extract_text_body(message) -> str:
    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain" and part.get_content_disposition() in (None, "inline"):
                return _clean_surrogate_chars(part.get_content()).strip()
        return ""
    if message.get_content_type() == "text/plain":
        return _clean_surrogate_chars(message.get_content()).strip()
    return ""


def extract_html_body(message) -> str | None:
    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            if content_type == "text/html" and part.get_content_disposition() in (None, "inline"):
                return _clean_surrogate_chars(part.get_content()).strip()
        return None
    if message.get_content_type() == "text/html":
        return _clean_surrogate_chars(message.get_content()).strip()
    return None


def html_to_text(value: str) -> str:
    parser = _HTMLToTextParser()
    parser.feed(value)
    parser.close()
    text = html.unescape(parser.get_text())
    return re.sub(r"[ \t]+", " ", text).strip()


def ensure_body_alternatives(
    body_text: str | None,
    body_html: str | None,
) -> tuple[str | None, str | None]:
    normalized_text = body_text.strip() if isinstance(body_text, str) and body_text.strip() else None
    normalized_html = body_html.strip() if isinstance(body_html, str) and body_html.strip() else None

    if normalized_html and not normalized_text:
        normalized_text = html_to_text(normalized_html)
    if normalized_text and not normalized_html:
        return normalized_text, None
    return normalized_text, normalized_html


def _normalize_str_list(value: Any, field_name: str) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return [item.strip() for item in value if item.strip()]
    raise SkillError(
        "VALIDATION_ERROR",
        f"{field_name} must be a string or list of strings",
    )


def parse_recipients(data: dict[str, Any]) -> tuple[list[str], list[str], list[str]]:
    to_list = _normalize_str_list(data.get("to"), "to")
    cc_list = _normalize_str_list(data.get("cc"), "cc")
    bcc_list = _normalize_str_list(data.get("bcc"), "bcc")
    return to_list, cc_list, bcc_list


def parse_base64_attachments(raw_attachments: Any) -> list[dict[str, Any]]:
    if raw_attachments is None:
        return []
    if not isinstance(raw_attachments, list):
        raise SkillError("VALIDATION_ERROR", "data.attachments must be an array when provided")

    attachments: list[dict[str, Any]] = []
    for idx, item in enumerate(raw_attachments):
        if not isinstance(item, dict):
            raise SkillError("VALIDATION_ERROR", f"data.attachments[{idx}] must be an object")

        filename = item.get("filename")
        content_base64 = item.get("contentBase64")
        if not isinstance(filename, str) or not filename.strip():
            raise SkillError("VALIDATION_ERROR", f"data.attachments[{idx}].filename is required")
        if not isinstance(content_base64, str) or not content_base64.strip():
            raise SkillError("VALIDATION_ERROR", f"data.attachments[{idx}].contentBase64 is required")

        try:
            content_bytes = base64.b64decode(content_base64, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise SkillError(
                "VALIDATION_ERROR",
                f"data.attachments[{idx}].contentBase64 is not valid base64",
            ) from exc

        attachments.append({"filename": filename.strip(), "content": content_bytes})

    return attachments


def guess_attachment_type(filename: str) -> tuple[str, str]:
    guessed_type, _ = mimetypes.guess_type(filename)
    if not guessed_type:
        return "application", "octet-stream"
    maintype, subtype = guessed_type.split("/", 1)
    return maintype, subtype
