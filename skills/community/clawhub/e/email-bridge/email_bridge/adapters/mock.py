"""Mock adapter for demo and testing with local JSON fixtures."""

import json
from datetime import datetime
from pathlib import Path
from typing import Iterator, Optional

from ..models import Account, EmailProvider
from .base import BaseAdapter, FetchOptions, RawMessage


# Default fixture path
DEFAULT_FIXTURES_PATH = Path(__file__).parent.parent.parent / "fixtures" / "sample_emails.json"


class MockAdapter(BaseAdapter):
    """Mock adapter that loads emails from local JSON fixtures.

    This allows full demo/testing without real email connections.
    """

    @property
    def provider(self) -> EmailProvider:
        return EmailProvider.MOCK

    def __init__(self, fixtures_path: Optional[Path] = None):
        self.fixtures_path = fixtures_path or DEFAULT_FIXTURES_PATH
        self._messages: Optional[list[dict]] = None

    def _load_fixtures(self) -> list[dict]:
        """Load messages from JSON fixtures file."""
        if self._messages is not None:
            return self._messages

        if not self.fixtures_path.exists():
            return []

        with open(self.fixtures_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self._messages = data.get("messages", [])
            return self._messages

    def fetch_messages(
        self, account: Account, options: FetchOptions = None
    ) -> Iterator[RawMessage]:
        """Yield messages from fixtures for the given account."""
        options = options or FetchOptions()
        messages = self._load_fixtures()

        count = 0
        for msg_data in messages:
            # Filter by account email if specified in fixture
            if msg_data.get("account_email") and msg_data["account_email"] != account.email:
                continue

            received_at = datetime.fromisoformat(msg_data["received_at"])

            # Apply filters
            if options.since and received_at < options.since:
                continue
            if options.unread_only and msg_data.get("is_read", False):
                continue

            yield RawMessage(
                message_id=msg_data["message_id"],
                subject=msg_data["subject"],
                sender=msg_data["sender"],
                sender_name=msg_data.get("sender_name"),
                recipients=msg_data.get("recipients", []),
                received_at=received_at,
                is_read=msg_data.get("is_read", False),
                body_text=msg_data.get("body_text"),
                body_html=msg_data.get("body_html"),
                raw_data=msg_data.get("raw_data", {}),
            )

            count += 1
            if count >= options.limit:
                break

    def get_message(self, account: Account, message_id: str) -> Optional[RawMessage]:
        """Get a specific message by ID."""
        messages = self._load_fixtures()

        for msg_data in messages:
            if msg_data["message_id"] == message_id:
                return RawMessage(
                    message_id=msg_data["message_id"],
                    subject=msg_data["subject"],
                    sender=msg_data["sender"],
                    sender_name=msg_data.get("sender_name"),
                    recipients=msg_data.get("recipients", []),
                    received_at=datetime.fromisoformat(msg_data["received_at"]),
                    is_read=msg_data.get("is_read", False),
                    body_text=msg_data.get("body_text"),
                    body_html=msg_data.get("body_html"),
                    raw_data=msg_data.get("raw_data", {}),
                )
        return None
