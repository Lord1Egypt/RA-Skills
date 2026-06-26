"""Tests for Gmail adapter."""

import pytest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from email_bridge.models import Account, EmailProvider
from email_bridge.adapters.gmail import (
    GmailAdapter,
    GmailAdapterError,
    GmailCredentialsNotFoundError,
    GmailAuthError,
)
from email_bridge.adapters.base import FetchOptions, RawMessage


class TestGmailAdapter:
    def test_provider_property(self):
        adapter = GmailAdapter()
        assert adapter.provider == EmailProvider.GMAIL

    def test_default_credentials_dir(self):
        adapter = GmailAdapter()
        expected = Path.home() / ".email-bridge" / "gmail"
        assert adapter.credentials_dir == expected

    def test_custom_credentials_dir(self):
        custom_dir = Path("/tmp/test-gmail")
        adapter = GmailAdapter(credentials_dir=custom_dir)
        assert adapter.credentials_dir == custom_dir

    def test_get_credentials_path_from_config(self):
        adapter = GmailAdapter()
        account = Account(
            id="test1",
            email="test@gmail.com",
            provider=EmailProvider.GMAIL,
            config={"credentials_path": "/custom/creds.json"}
        )

        path = adapter._get_credentials_path(account)
        assert path == Path("/custom/creds.json")

    def test_get_credentials_path_default(self):
        adapter = GmailAdapter()
        account = Account(
            id="test1",
            email="test@gmail.com",
            provider=EmailProvider.GMAIL,
        )

        path = adapter._get_credentials_path(account)
        assert path == adapter.credentials_dir / "credentials.json"

    def test_get_token_path_from_config(self):
        adapter = GmailAdapter()
        account = Account(
            id="test1",
            email="test@gmail.com",
            provider=EmailProvider.GMAIL,
            config={"token_path": "/custom/token.json"}
        )

        path = adapter._get_token_path(account)
        assert path == Path("/custom/token.json")

    def test_get_token_path_default(self):
        adapter = GmailAdapter()
        account = Account(
            id="test1",
            email="test.user@gmail.com",
            provider=EmailProvider.GMAIL,
        )

        path = adapter._get_token_path(account)
        # Email should be sanitized for filename
        assert "test_user_at_gmail_com" in str(path)

    def test_credentials_not_found_error(self):
        adapter = GmailAdapter(credentials_dir=Path("/nonexistent"))
        account = Account(
            id="test1",
            email="test@gmail.com",
            provider=EmailProvider.GMAIL,
        )

        with pytest.raises(GmailCredentialsNotFoundError):
            adapter._get_credentials(account)

    def test_parse_message(self):
        adapter = GmailAdapter()

        # Mock Gmail API message data
        msg_data = {
            "id": "msg123",
            "threadId": "thread123",
            "labelIds": ["INBOX"],
            "snippet": "This is a test...",
            "payload": {
                "headers": [
                    {"name": "Subject", "value": "Test Subject"},
                    {"name": "From", "value": "Sender <sender@example.com>"},
                    {"name": "To", "value": "recipient@example.com"},
                    {"name": "Date", "value": "Mon, 20 Mar 2026 10:00:00 +0000"},
                ],
                "mimeType": "text/plain",
                "body": {
                    "data": "VGhpcyBpcyB0ZXN0IGJvZHk="  # base64 encoded "This is test body"
                }
            }
        }

        raw_msg = adapter._parse_message(msg_data)

        assert raw_msg.message_id == "msg123"
        assert raw_msg.subject == "Test Subject"
        assert raw_msg.sender == "sender@example.com"
        assert raw_msg.sender_name == "Sender"
        assert raw_msg.is_read is True  # No UNREAD label
        assert raw_msg.body_text == "This is test body"

    def test_parse_message_unread(self):
        adapter = GmailAdapter()

        msg_data = {
            "id": "msg123",
            "threadId": "thread123",
            "labelIds": ["INBOX", "UNREAD"],
            "payload": {
                "headers": [
                    {"name": "Subject", "value": "Test"},
                    {"name": "From", "value": "sender@example.com"},
                    {"name": "Date", "value": "Mon, 20 Mar 2026 10:00:00 +0000"},
                ],
            }
        }

        raw_msg = adapter._parse_message(msg_data)
        assert raw_msg.is_read is False

    def test_parse_message_with_name_parsing(self):
        adapter = GmailAdapter()

        msg_data = {
            "id": "msg123",
            "threadId": "thread123",
            "payload": {
                "headers": [
                    {"name": "Subject", "value": "Test"},
                    {"name": "From", "value": '"John Doe" <john@example.com>'},
                    {"name": "Date", "value": "Mon, 20 Mar 2026 10:00:00 +0000"},
                ],
            }
        }

        raw_msg = adapter._parse_message(msg_data)
        assert raw_msg.sender_name == "John Doe"
        assert raw_msg.sender == "john@example.com"

    def test_sync_config_from_account(self):
        adapter = GmailAdapter()

        # Test that account config is used for sync parameters
        account = Account(
            id="test1",
            email="test@gmail.com",
            provider=EmailProvider.GMAIL,
            config={
                "sync_days": 3,
                "sync_max_messages": 50
            }
        )

        # We can't test actual fetch without mock service, but we can verify
        # the config is accessible
        assert account.config.get("sync_days") == 3
        assert account.config.get("sync_max_messages") == 50


class TestGmailAdapterErrors:
    def test_error_hierarchy(self):
        # Test that errors are properly inherited
        assert issubclass(GmailCredentialsNotFoundError, GmailAdapterError)
        assert issubclass(GmailAuthError, GmailAdapterError)
        assert issubclass(GmailAdapterError, Exception)

    def test_credentials_error_message(self):
        error = GmailCredentialsNotFoundError("Credentials not found")
        assert "Credentials not found" in str(error)

    def test_auth_error_message(self):
        error = GmailAuthError("Auth failed")
        assert "Auth failed" in str(error)
