"""Email provider adapters."""

from .base import BaseAdapter, FetchOptions, RawMessage
from .mock import MockAdapter
from .gmail import GmailAdapter, GmailAdapterError, GmailCredentialsNotFoundError, GmailAuthError
from .imap import IMAPAdapter, QQMailAdapter, NetEaseMailAdapter, IMAPAdapterError, IMAPAuthError
from .smtp import SMTPAdapter, SMTPAdapterError, SMTPAuthError, SMTPSendError

__all__ = [
    "BaseAdapter",
    "FetchOptions",
    "RawMessage",
    "MockAdapter",
    "GmailAdapter",
    "GmailAdapterError",
    "GmailCredentialsNotFoundError",
    "GmailAuthError",
    "IMAPAdapter",
    "QQMailAdapter",
    "NetEaseMailAdapter",
    "IMAPAdapterError",
    "IMAPAuthError",
    "SMTPAdapter",
    "SMTPAdapterError",
    "SMTPAuthError",
    "SMTPSendError",
]
