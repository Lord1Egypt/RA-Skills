"""Basic tests for email bridge."""

import tempfile
from pathlib import Path
import pytest

from email_bridge.models import Account, EmailProvider, AccountStatus, Message, EmailCategory
from email_bridge.db import Database
from email_bridge.service import EmailBridgeService
from email_bridge.categories import detect_category, EmailCategory as Cat


class TestModels:
    def test_account_creation(self):
        account = Account(
            id="test1",
            email="test@example.com",
            provider=EmailProvider.MOCK,
        )
        assert account.id == "test1"
        assert account.email == "test@example.com"
        assert account.status == AccountStatus.ACTIVE

    def test_message_creation(self):
        from datetime import datetime
        msg = Message(
            id="acc:msg1",
            account_id="acc",
            message_id="msg1",
            subject="Test Subject",
            sender="sender@example.com",
            recipients=["recv@example.com"],
            received_at=datetime.utcnow(),
        )
        assert msg.subject == "Test Subject"
        assert msg.is_read is False


class TestDatabase:
    def test_database_operations(self, tmp_path):
        db = Database(db_path=tmp_path / "test.db")

        # Add account
        account = Account(
            id="test1",
            email="test@example.com",
            provider=EmailProvider.MOCK,
        )
        db.add_account(account)

        # List accounts
        accounts = db.list_accounts()
        assert len(accounts) == 1
        assert accounts[0].email == "test@example.com"

        # Get account
        acc = db.get_account("test1")
        assert acc is not None
        assert acc.email == "test@example.com"

        db.close()

    def test_message_operations(self, tmp_path):
        from datetime import datetime

        db = Database(db_path=tmp_path / "test.db")

        # Add account first
        account = Account(id="acc1", email="test@example.com", provider=EmailProvider.MOCK)
        db.add_account(account)

        # Add message
        msg = Message(
            id="acc1:msg1",
            account_id="acc1",
            message_id="msg1",
            subject="Test Subject",
            sender="sender@example.com",
            recipients=["test@example.com"],
            received_at=datetime.utcnow(),
            category=EmailCategory.NORMAL,
        )
        db.add_message(msg)

        # List messages
        msgs = db.list_messages()
        assert len(msgs) == 1
        assert msgs[0].subject == "Test Subject"

        # Find message
        found = db.find_message("msg1")
        assert found is not None
        assert found.subject == "Test Subject"

        db.close()


class TestCategoryDetection:
    def test_verification_category(self):
        cat = detect_category("Your verification code is 123456", "")
        assert cat == Cat.VERIFICATION

    def test_security_category(self):
        cat = detect_category("Security Alert: New login", "")
        assert cat == Cat.SECURITY

    def test_subscription_category(self):
        cat = detect_category("Weekly Newsletter", "Click to unsubscribe")
        assert cat == Cat.SUBSCRIPTION

    def test_spam_category(self):
        cat = detect_category("CONGRATULATIONS! You've WON!!!", "")
        assert cat == Cat.SPAM_LIKE

    def test_normal_category(self):
        cat = detect_category("Re: Project Update Meeting", "Hi, thanks for the update")
        assert cat == Cat.NORMAL


class TestService:
    def test_add_account(self, tmp_path):
        from email_bridge.db import Database
        db = Database(db_path=tmp_path / "test.db")
        service = EmailBridgeService(db=db)

        account = service.add_account(
            email="test@example.com",
            provider=EmailProvider.MOCK,
            display_name="Test Account"
        )

        assert account.email == "test@example.com"
        assert account.provider == EmailProvider.MOCK

        db.close()

    def test_stats(self, tmp_path):
        from email_bridge.db import Database
        db = Database(db_path=tmp_path / "test.db")
        service = EmailBridgeService(db=db)

        stats = service.get_stats()
        assert stats["total_accounts"] == 0
        assert stats["unread_messages"] == 0

        db.close()
