"""Gmail adapter using Gmail API with OAuth2."""

import base64
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterator, Optional

from ..models import Account, EmailProvider
from .base import BaseAdapter, FetchOptions, RawMessage

# Gmail API scopes - read-only access
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Default paths for credentials
DEFAULT_CREDENTIALS_DIR = Path.home() / ".email-bridge" / "gmail"


class GmailAdapterError(Exception):
    """Base exception for Gmail adapter errors."""
    pass


class GmailCredentialsNotFoundError(GmailAdapterError):
    """Raised when credentials file is not found."""
    pass


class GmailAuthError(GmailAdapterError):
    """Raised when authentication fails."""
    pass


class GmailAdapter(BaseAdapter):
    """Gmail adapter using Gmail API.

    Configuration (via account.config):
        credentials_path: Path to credentials.json from Google Cloud Console
        token_path: Path to store/load OAuth token (default: ~/.email-bridge/gmail/token.json)
        sync_days: Number of days back to sync (default: 7)
        sync_max_messages: Maximum messages per sync (default: 100)

    Setup:
        1. Create a Google Cloud project
        2. Enable Gmail API
        3. Create OAuth 2.0 Desktop credentials
        4. Download credentials.json to ~/.email-bridge/gmail/credentials.json
        5. Run first sync - browser will open for OAuth consent
        6. Token is cached for subsequent runs
    """

    @property
    def provider(self) -> EmailProvider:
        return EmailProvider.GMAIL

    def __init__(
        self,
        credentials_dir: Optional[Path] = None,
    ):
        """Initialize Gmail adapter.

        Args:
            credentials_dir: Directory to store credentials and tokens
        """
        self.credentials_dir = credentials_dir or DEFAULT_CREDENTIALS_DIR
        self._service = None

    def _get_credentials_path(self, account: Account) -> Path:
        """Get credentials path from account config or default."""
        if "credentials_path" in account.config:
            return Path(account.config["credentials_path"])
        return self.credentials_dir / "credentials.json"

    def _get_token_path(self, account: Account) -> Path:
        """Get token path from account config or default."""
        if "token_path" in account.config:
            return Path(account.config["token_path"])
        # Use account-specific token file
        safe_email = account.email.replace("@", "_at_").replace(".", "_")
        return self.credentials_dir / f"token_{safe_email}.json"

    def _get_credentials(self, account: Account):
        """Load or create OAuth2 credentials.

        Returns credentials object for Gmail API.
        Raises GmailCredentialsNotFoundError if credentials.json not found.
        Raises GmailAuthError if authentication fails.
        """
        try:
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
        except ImportError as e:
            raise GmailAdapterError(
                "Gmail dependencies not installed. Run: pip install google-api-python-client google-auth google-auth-oauthlib"
            ) from e

        credentials_path = self._get_credentials_path(account)
        token_path = self._get_token_path(account)

        creds = None

        # Load existing token if available
        if token_path.exists():
            try:
                creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
            except Exception:
                creds = None

        # Refresh if expired
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                # Save refreshed token
                token_path.parent.mkdir(parents=True, exist_ok=True)
                token_path.write_text(creds.to_json())
            except Exception as e:
                creds = None

        # If no valid credentials, need to authenticate
        if not creds or not creds.valid:
            if not credentials_path.exists():
                raise GmailCredentialsNotFoundError(
                    f"Gmail credentials not found at {credentials_path}. "
                    "Download credentials.json from Google Cloud Console. "
                    "See README.md for setup instructions."
                )

            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(credentials_path), SCOPES
                )
                creds = flow.run_local_server(port=0)

                # Save token for future use
                token_path.parent.mkdir(parents=True, exist_ok=True)
                token_path.write_text(creds.to_json())
            except Exception as e:
                raise GmailAuthError(f"Failed to authenticate with Gmail: {e}") from e

        return creds

    def _get_service(self, account: Account):
        """Get or create Gmail API service."""
        if self._service is None:
            try:
                from googleapiclient.discovery import build
            except ImportError as e:
                raise GmailAdapterError(
                    "Gmail dependencies not installed. Run: pip install google-api-python-client"
                ) from e

            creds = self._get_credentials(account)
            self._service = build("gmail", "v1", credentials=creds)

        return self._service

    def _parse_message(self, msg_data: dict) -> RawMessage:
        """Parse Gmail API message data into RawMessage."""
        headers = {h["name"]: h["value"] for h in msg_data.get("payload", {}).get("headers", [])}

        # Extract sender info
        sender = headers.get("From", "")
        sender_name = None
        if "<" in sender and ">" in sender:
            # Parse "Name <email@domain.com>" format
            import re
            match = re.match(r"(.+?)\s*<(.+?)>", sender)
            if match:
                sender_name = match.group(1).strip().strip('"')
                sender = match.group(2)

        # Extract recipients
        recipients = []
        for field in ["To", "Cc"]:
            if field in headers:
                # Simple extraction - could be improved for complex formats
                recipients.extend([r.strip() for r in headers[field].split(",")])

        # Extract body
        body_text = None
        body_html = None
        payload = msg_data.get("payload", {})

        def extract_body(part: dict) -> tuple[Optional[str], Optional[str]]:
            """Recursively extract body from message parts."""
            text = None
            html = None

            if part.get("mimeType") == "text/plain" and "data" in part.get("body", {}):
                data = part["body"]["data"]
                text = base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
            elif part.get("mimeType") == "text/html" and "data" in part.get("body", {}):
                data = part["body"]["data"]
                html = base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

            for subpart in part.get("parts", []):
                sub_text, sub_html = extract_body(subpart)
                if sub_text and not text:
                    text = sub_text
                if sub_html and not html:
                    html = sub_html

            return text, html

        body_text, body_html = extract_body(payload)

        # Parse date
        date_str = headers.get("Date", "")
        try:
            # Gmail provides RFC 2822 format
            from email.utils import parsedate_to_datetime
            received_at = parsedate_to_datetime(date_str)
        except Exception:
            received_at = datetime.utcnow()

        # Get labels for read status
        labels = msg_data.get("labelIds", [])
        is_read = "UNREAD" not in labels

        return RawMessage(
            message_id=msg_data["id"],
            subject=headers.get("Subject", "(no subject)"),
            sender=sender,
            sender_name=sender_name,
            recipients=recipients,
            received_at=received_at,
            is_read=is_read,
            body_text=body_text,
            body_html=body_html,
            raw_data={
                "threadId": msg_data.get("threadId"),
                "labelIds": labels,
                "snippet": msg_data.get("snippet"),
            },
        )

    def fetch_messages(
        self, account: Account, options: FetchOptions = None
    ) -> Iterator[RawMessage]:
        """Fetch messages from Gmail.

        Supports recent-window sync via account.config:
            - sync_days: Only fetch messages from last N days (default: 7)
            - sync_max_messages: Maximum messages to fetch (default: 100)
        """
        options = options or FetchOptions()

        # Get sync configuration
        sync_days = account.config.get("sync_days", 7)
        sync_max = account.config.get("sync_max_messages", 100)

        # Calculate effective limit
        limit = min(options.limit, sync_max) if options.limit else sync_max

        # Build query
        query_parts = []

        # Add date filter for recent window
        if not options.since:
            since_date = datetime.utcnow() - timedelta(days=sync_days)
            query_parts.append(f"after:{since_date.strftime('%Y/%m/%d')}")
        else:
            query_parts.append(f"after:{options.since.strftime('%Y/%m/%d')}")

        # Add unread filter if requested
        if options.unread_only:
            query_parts.append("is:unread")

        query = " ".join(query_parts)

        try:
            service = self._get_service(account)
        except (GmailCredentialsNotFoundError, GmailAuthError) as e:
            # Re-raise to let caller handle
            raise

        try:
            # List messages matching query
            results = service.users().messages().list(
                userId="me",
                q=query,
                maxResults=limit
            ).execute()

            messages = results.get("messages", [])

            for msg_ref in messages:
                # Fetch full message details
                msg_data = service.users().messages().get(
                    userId="me",
                    id=msg_ref["id"],
                    format="full"
                ).execute()

                raw_msg = self._parse_message(msg_data)
                yield raw_msg

        except Exception as e:
            if isinstance(e, (GmailCredentialsNotFoundError, GmailAuthError)):
                raise
            raise GmailAdapterError(f"Failed to fetch messages: {e}") from e

    def get_message(self, account: Account, message_id: str) -> Optional[RawMessage]:
        """Get a specific message by Gmail message ID."""
        try:
            service = self._get_service(account)
        except (GmailCredentialsNotFoundError, GmailAuthError):
            return None

        try:
            msg_data = service.users().messages().get(
                userId="me",
                id=message_id,
                format="full"
            ).execute()

            return self._parse_message(msg_data)

        except Exception:
            return None

    def authenticate(self, account: Account) -> bool:
        """Test authentication with Gmail.

        Returns True if credentials are valid.
        """
        try:
            self._get_credentials(account)
            return True
        except (GmailCredentialsNotFoundError, GmailAuthError):
            return False

    def test_connection(self, account: Account) -> bool:
        """Test connection to Gmail API.

        Returns True if we can connect and fetch profile.
        """
        try:
            service = self._get_service(account)
            service.users().getProfile(userId="me").execute()
            return True
        except Exception:
            return False
