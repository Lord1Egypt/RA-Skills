"""Common utilities for email skill scripts."""

from .errors import SkillError, SCHEMA_VERSION, IMAP_SEARCH_COMMANDS
from .validators import validate_imap_query, validate_folder_name
from .config import load_config, resolve_account, validate_account_config, _get_account_names
from .auth import (
    _get_password_from_env,
    _get_username_from_env,
    _detect_auth_type,
    _get_oauth2_from_env,
    get_oauth2_token,
)
from .imap_utils import (
    connect_imap,
    close_imap_safely,
    select_mailbox,
    decode_mime_header,
    extract_fetch_tags,
    get_imap_capabilities,
    expunge_uids_safely,
    fetch_original_message,
)
from .smtp_utils import (
    connect_smtp,
    close_smtp_safely,
    get_sender_address,
    get_smtp_signatures,
    apply_signatures,
    build_message,
    text_to_html,
)
from .parsers import (
    extract_text_body,
    extract_html_body,
    parse_recipients,
    parse_base64_attachments,
    guess_attachment_type,
    ensure_body_alternatives,
    _HTMLToTextParser,
    html_to_text,
    normalize_uids,
)
from .protocol import with_runtime, read_request, write_success, write_error, write_unknown_error

__all__ = [
    "SkillError",
    "SCHEMA_VERSION",
    "IMAP_SEARCH_COMMANDS",
    "validate_imap_query",
    "validate_folder_name",
    "load_config",
    "resolve_account",
    "validate_account_config",
    "_get_account_names",
    "_get_password_from_env",
    "_get_username_from_env",
    "_detect_auth_type",
    "_get_oauth2_from_env",
    "get_oauth2_token",
    "connect_imap",
    "close_imap_safely",
    "select_mailbox",
    "decode_mime_header",
    "extract_fetch_tags",
    "get_imap_capabilities",
    "expunge_uids_safely",
    "connect_smtp",
    "close_smtp_safely",
    "get_sender_address",
    "get_smtp_signatures",
    "apply_signatures",
    "build_message",
    "html_to_text",
    "text_to_html",
    "extract_text_body",
    "extract_html_body",
    "parse_recipients",
    "parse_base64_attachments",
    "guess_attachment_type",
    "ensure_body_alternatives",
    "_HTMLToTextParser",
    "normalize_uids",
    "with_runtime",
    "read_request",
    "write_success",
    "write_error",
    "write_unknown_error",
]
