"""Base adapter interface for email providers."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Iterator, Optional

from ..models import Account, EmailProvider


@dataclass
class FetchOptions:
    """Options for fetching messages."""
    since: Optional[datetime] = None
    limit: int = 100
    unread_only: bool = False


@dataclass
class RawMessage:
    """Raw message data from a provider."""
    message_id: str
    subject: str
    sender: str
    sender_name: Optional[str]
    recipients: list[str]
    received_at: datetime
    is_read: bool
    body_text: Optional[str] = None
    body_html: Optional[str] = None
    # Provider-specific raw data
    raw_data: dict = None

    def __post_init__(self):
        if self.raw_data is None:
            self.raw_data = {}


class BaseAdapter(ABC):
    """Abstract base class for email provider adapters.

    Future implementations:
    - GmailAdapter: Uses Gmail API (OAuth2)
    - QQAdapter: Uses IMAP or QQ Mail API
    - NetEaseAdapter: Uses IMAP
    """

    @property
    @abstractmethod
    def provider(self) -> EmailProvider:
        """Return the provider this adapter handles."""
        pass

    @abstractmethod
    def fetch_messages(
        self, account: Account, options: FetchOptions = None
    ) -> Iterator[RawMessage]:
        """Fetch messages from the provider.

        This is a generator to support streaming large result sets.
        """
        pass

    @abstractmethod
    def get_message(self, account: Account, message_id: str) -> Optional[RawMessage]:
        """Fetch a single message by ID."""
        pass

    def authenticate(self, account: Account) -> bool:
        """Authenticate with the provider.

        Override this for providers requiring OAuth2 or other auth flows.
        Returns True if authentication is valid/successful.
        """
        return True

    def test_connection(self, account: Account) -> bool:
        """Test the connection to the provider.

        Override this for health checks.
        """
        return True
