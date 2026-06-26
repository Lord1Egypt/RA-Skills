"""Service layer for email bridge business logic."""

import uuid
from datetime import datetime
from typing import Optional, List

from .adapters.base import FetchOptions
from .adapters.mock import MockAdapter
from .adapters.gmail import GmailAdapter, GmailCredentialsNotFoundError, GmailAuthError
from .adapters.imap import QQMailAdapter, NetEaseMailAdapter, IMAPAdapterError, IMAPAuthError
from .adapters.smtp import SMTPAdapter, SMTPAdapterError, SMTPAuthError, SMTPSendError
from .categories import detect_category
from .db import Database
from .models import Account, AccountStatus, EmailCategory, EmailProvider, Message


class EmailBridgeService:
    """Core service for email management.

    This service provides a clean API layer between the CLI/presentation
    and the data/adapters layer.
    """

    def __init__(self, db: Optional[Database] = None):
        self.db = db or Database()
        self._adapters = {
            EmailProvider.MOCK: MockAdapter(),
            EmailProvider.GMAIL: GmailAdapter(),
            EmailProvider.QQ: QQMailAdapter(),
            EmailProvider.NETEASE: NetEaseMailAdapter(),
        }

    # Account management
    def list_accounts(self, include_disabled: bool = False) -> list[Account]:
        """List all configured accounts."""
        return self.db.list_accounts(include_disabled=include_disabled)

    def get_account(self, account_id: str) -> Optional[Account]:
        """Get account by ID."""
        return self.db.get_account(account_id)

    def add_account(
        self,
        email: str,
        provider: EmailProvider,
        display_name: Optional[str] = None,
        config: Optional[dict] = None
    ) -> Account:
        """Add a new email account."""
        account = Account(
            id=str(uuid.uuid4())[:8],
            email=email,
            provider=provider,
            display_name=display_name,
            config=config or {},
        )
        return self.db.add_account(account)

    def update_account(
        self,
        account_id: str,
        display_name: Optional[str] = None,
        status: Optional[AccountStatus] = None,
        config: Optional[dict] = None
    ) -> Optional[Account]:
        """Update an existing account."""
        account = self.db.get_account(account_id)
        if not account:
            return None

        if display_name is not None:
            account.display_name = display_name
        if status is not None:
            account.status = status
        if config is not None:
            account.config = config

        return self.db.update_account(account)

    def disable_account(self, account_id: str) -> bool:
        """Disable an account (soft delete)."""
        account = self.db.get_account(account_id)
        if not account:
            return False
        account.status = AccountStatus.DISABLED
        self.db.update_account(account)
        return True

    def delete_account(self, account_id: str) -> bool:
        """Permanently delete an account and its messages."""
        return self.db.delete_account(account_id)

    # Message management
    def list_recent_messages(
        self,
        account_id: Optional[str] = None,
        limit: int = 20
    ) -> list[Message]:
        """List recent messages across all or one account."""
        return self.db.list_messages(account_id=account_id, limit=limit)

    def list_unread_messages(
        self,
        account_id: Optional[str] = None,
        limit: int = 20
    ) -> list[Message]:
        """List unread messages."""
        return self.db.list_messages(
            account_id=account_id, unread_only=True, limit=limit
        )

    def search_messages(
        self,
        keyword: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        account_id: Optional[str] = None,
        limit: int = 50
    ) -> list[Message]:
        """Search messages by keyword and/or time range."""
        return self.db.search_messages(
            keyword=keyword,
            start_time=start_time,
            end_time=end_time,
            account_id=account_id,
            limit=limit
        )

    def get_message(self, message_id: str) -> Optional[Message]:
        """Get a single message with full details.

        Supports flexible ID lookup: full ID, message_id only, or partial.
        """
        return self.db.find_message(message_id)

    def mark_read(self, message_id: str, is_read: bool = True) -> bool:
        """Mark a message as read or unread."""
        # First find the message to get its full ID
        msg = self.db.find_message(message_id)
        if msg:
            return self.db.mark_read(msg.id, is_read)
        return False

    # Sync operations
    def sync_account(
        self,
        account_id: str,
        since: Optional[datetime] = None,
        limit: int = 100
    ) -> int:
        """Sync messages from a provider into local storage.

        Returns the number of messages synced.
        """
        account = self.db.get_account(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")

        if account.status != AccountStatus.ACTIVE:
            raise ValueError(f"Account {account_id} is not active")

        adapter = self._adapters.get(account.provider)
        if not adapter:
            raise ValueError(f"No adapter for provider {account.provider}")

        options = FetchOptions(since=since, limit=limit)
        count = 0

        for raw_msg in adapter.fetch_messages(account, options):
            # Detect category
            category = detect_category(
                raw_msg.subject,
                raw_msg.body_text or ""
            )

            # Generate preview
            preview = None
            if raw_msg.body_text:
                preview = raw_msg.body_text[:200].strip()

            # Create message record
            message = Message(
                id=f"{account_id}:{raw_msg.message_id}",
                account_id=account_id,
                message_id=raw_msg.message_id,
                subject=raw_msg.subject,
                sender=raw_msg.sender,
                sender_name=raw_msg.sender_name,
                recipients=raw_msg.recipients,
                received_at=raw_msg.received_at,
                is_read=raw_msg.is_read,
                category=category,
                preview=preview,
                body_text=raw_msg.body_text,
                body_html=raw_msg.body_html,
                provider_data=raw_msg.raw_data,
            )

            self.db.add_message(message)
            count += 1

        return count

    def sync_all_accounts(self, since: Optional[datetime] = None) -> dict[str, int]:
        """Sync all active accounts.

        Returns a dict mapping account_id to sync count.
        """
        results = {}
        for account in self.db.list_accounts(include_disabled=False):
            try:
                count = self.sync_account(account.id, since=since)
                results[account.id] = count
            except Exception as e:
                results[account.id] = f"Error: {e}"
        return results

    # Stats
    def get_stats(self) -> dict:
        """Get overall statistics."""
        accounts = self.db.list_accounts(include_disabled=True)
        active_accounts = [a for a in accounts if a.status == AccountStatus.ACTIVE]
        unread_count = self.db.count_unread()

        return {
            "total_accounts": len(accounts),
            "active_accounts": len(active_accounts),
            "unread_messages": unread_count,
        }

    # Send email
    def send_email(
        self,
        account_id: str,
        to: List[str],
        subject: str,
        body_text: Optional[str] = None,
        body_html: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
    ) -> bool:
        """Send an email from an account.

        Args:
            account_id: Account to send from
            to: List of recipient email addresses
            subject: Email subject
            body_text: Plain text body
            body_html: HTML body
            cc: List of CC recipients
            bcc: List of BCC recipients

        Returns:
            True if sent successfully

        Raises:
            ValueError: Account not found or inactive
            SMTPAuthError: Authentication failed
            SMTPSendError: Sending failed
        """
        account = self.db.get_account(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")

        if account.status != AccountStatus.ACTIVE:
            raise ValueError(f"Account {account_id} is not active")

        # Use SMTP adapter for all providers
        # (Gmail can also use API, but SMTP is simpler for now)
        smtp_adapter = SMTPAdapter()
        from_name = account.display_name

        return smtp_adapter.send_email(
            account=account,
            to=to,
            subject=subject,
            body_text=body_text,
            body_html=body_html,
            cc=cc,
            bcc=bcc,
            from_name=from_name,
        )
