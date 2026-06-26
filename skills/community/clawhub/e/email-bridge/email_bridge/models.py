"""Data models for email bridge."""

from datetime import datetime
from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field


class EmailCategory(str, Enum):
    """Email categories."""
    VERIFICATION = "verification"
    SECURITY = "security"
    SUBSCRIPTION = "subscription"
    SPAM_LIKE = "spam_like"
    NORMAL = "normal"


class AccountStatus(str, Enum):
    """Account status."""
    ACTIVE = "active"
    DISABLED = "disabled"


class EmailProvider(str, Enum):
    """Supported email providers."""
    MOCK = "mock"
    GMAIL = "gmail"
    QQ = "qq"
    NETEASE = "netease"


class Account(BaseModel):
    """Email account configuration."""
    id: str
    email: str
    provider: EmailProvider
    status: AccountStatus = AccountStatus.ACTIVE
    display_name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    # Provider-specific config (e.g., tokens, credentials) stored encrypted later
    config: dict = Field(default_factory=dict)


class Message(BaseModel):
    """Email message metadata."""
    id: str
    account_id: str
    message_id: str  # Original message ID from provider
    subject: str
    sender: str
    sender_name: Optional[str] = None
    recipients: list[str] = Field(default_factory=list)
    received_at: datetime
    is_read: bool = False
    is_starred: bool = False
    category: EmailCategory = EmailCategory.NORMAL
    # Optional cached content
    preview: Optional[str] = None  # First ~200 chars
    body_text: Optional[str] = None
    body_html: Optional[str] = None
    # Metadata
    synced_at: datetime = Field(default_factory=datetime.utcnow)
    provider_data: dict = Field(default_factory=dict)  # Provider-specific raw data
