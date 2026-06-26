"""IMAP adapter for QQ Mail, NetEase Mail, and other IMAP providers."""

import email
import imaplib
import re
from datetime import datetime, timedelta
from email.header import decode_header
from email.utils import parsedate_to_datetime
from typing import Iterator, Optional

from ..models import Account, EmailProvider
from .base import BaseAdapter, FetchOptions, RawMessage


class IMAPAdapterError(Exception):
    """Base exception for IMAP adapter errors."""
    pass


class IMAPAuthError(IMAPAdapterError):
    """Raised when authentication fails.
    
    Common causes:
    - Using login password instead of authorization code
    - Authorization code has expired or been reset
    - IMAP service not enabled in email settings
    """
    pass


class IMAPConnectionError(IMAPAdapterError):
    """Raised when connection fails.
    
    Common causes:
    - Network connectivity issues
    - IMAP server is down
    - Firewall blocking the connection
    """
    pass


# Help URLs for common email providers
AUTH_HELP_URLS = {
    EmailProvider.QQ: "https://service.mail.qq.com/detail/0/75",
    EmailProvider.NETEASE: "163/126邮箱: 设置 → POP3/SMTP/IMAP → 开启服务",
}


# IMAP server configurations
IMAP_SERVERS = {
    EmailProvider.QQ: {
        "host": "imap.qq.com",
        "port": 993,
    },
    EmailProvider.NETEASE: {
        # Will be determined by email domain (163.com or 126.com)
        "163.com": {"host": "imap.163.com", "port": 993},
        "126.com": {"host": "imap.126.com", "port": 993},
        "yeah.net": {"host": "imap.yeah.net", "port": 993},
    },
}


class IMAPAdapter(BaseAdapter):
    """IMAP adapter for QQ Mail and NetEase Mail.

    Configuration (via account.config):
        password: Authorization code (NOT the login password)
            - QQ Mail: Generate at https://service.mail.qq.com/detail/0/75
            - 163 Mail: Generate at Settings > POP3/SMTP/IMAP
            - 126 Mail: Same as 163

    Setup:
        1. Enable IMAP in your email settings
        2. Generate an authorization code (授权码)
        3. Add account with the authorization code as password
    """

    def __init__(self):
        self._connections = {}  # Cache connections by account ID

    @property
    def provider(self) -> EmailProvider:
        # This is a base class, subclasses will override
        raise NotImplementedError

    def _get_imap_server(self, account: Account) -> tuple[str, int]:
        """Get IMAP server host and port for the account."""
        provider = account.provider
        email_domain = account.email.split("@")[1].lower()

        if provider == EmailProvider.QQ:
            config = IMAP_SERVERS[EmailProvider.QQ]
            return config["host"], config["port"]

        elif provider == EmailProvider.NETEASE:
            netease_config = IMAP_SERVERS[EmailProvider.NETEASE]
            # Determine by email domain
            if email_domain in netease_config:
                return netease_config[email_domain]["host"], netease_config[email_domain]["port"]
            # Default to 163
            return netease_config["163.com"]["host"], netease_config["163.com"]["port"]

        raise IMAPAdapterError(f"Unknown provider: {provider}")

    def _connect(self, account: Account) -> imaplib.IMAP4_SSL:
        """Connect to IMAP server and authenticate."""
        host, port = self._get_imap_server(account)
        password = account.config.get("password")

        if not password:
            help_url = AUTH_HELP_URLS.get(account.provider, "")
            raise IMAPAuthError(
                f"❌ 未设置授权码: {account.email}\n\n"
                f"请使用授权码（不是登录密码）配置账户：\n"
                f"  email-bridge accounts add {account.email} -p {account.provider.value} \\\n"
                f"    --config '{{\"password\": \"YOUR_AUTH_CODE\"}}'\n\n"
                f"📚 获取授权码: {help_url}"
            )

        try:
            conn = imaplib.IMAP4_SSL(host, port)
            conn.login(account.email, password)
            return conn
        except imaplib.IMAP4.error as e:
            error_msg = str(e)
            if "authentication failed" in error_msg.lower() or "login" in error_msg.lower():
                help_url = AUTH_HELP_URLS.get(account.provider, "")
                raise IMAPAuthError(
                    f"❌ 认证失败: {account.email}\n\n"
                    f"可能原因：\n"
                    f"  1. 使用了登录密码而非授权码\n"
                    f"  2. 授权码已过期或被重置\n"
                    f"  3. 未开启 IMAP 服务\n\n"
                    f"📚 获取授权码: {help_url}"
                ) from e
            raise IMAPConnectionError(
                f"❌ 连接失败: {host}:{port}\n\n"
                f"可能原因：\n"
                f"  1. 网络连接问题\n"
                f"  2. 防火墙阻止了连接\n"
                f"  3. IMAP 服务暂时不可用\n\n"
                f"错误详情: {e}"
            ) from e

    def _get_connection(self, account: Account) -> imaplib.IMAP4_SSL:
        """Get or create a connection for the account."""
        if account.id not in self._connections:
            self._connections[account.id] = self._connect(account)
        return self._connections[account.id]

    def _decode_header_value(self, value: str) -> str:
        """Decode email header value."""
        if not value:
            return ""

        decoded_parts = []
        for part, charset in decode_header(value):
            if isinstance(part, bytes):
                try:
                    decoded_parts.append(part.decode(charset or "utf-8", errors="replace"))
                except (LookupError, UnicodeDecodeError):
                    decoded_parts.append(part.decode("utf-8", errors="replace"))
            else:
                decoded_parts.append(part)

        return "".join(decoded_parts)

    def _parse_sender(self, sender: str) -> tuple[str, Optional[str]]:
        """Parse sender into email and name.

        Returns: (email, name or None)
        """
        if not sender:
            return "", None

        sender = self._decode_header_value(sender)

        # Try "Name <email@domain.com>" format
        match = re.match(r"(.+?)\s*<(.+?)>", sender)
        if match:
            name = match.group(1).strip().strip('"')
            email_addr = match.group(2).strip()
            return email_addr, name

        # Plain email
        return sender.strip(), None

    def _parse_message(self, msg: email.message.Message, message_id: str) -> RawMessage:
        """Parse email.message.Message into RawMessage."""
        # Headers
        subject = self._decode_header_value(msg.get("Subject", "(no subject)"))
        sender_raw = msg.get("From", "")
        sender, sender_name = self._parse_sender(sender_raw)

        # Recipients
        recipients = []
        for field in ["To", "Cc"]:
            value = msg.get(field)
            if value:
                # Simple extraction
                for addr in value.split(","):
                    addr = addr.strip()
                    if "<" in addr and ">" in addr:
                        match = re.search(r"<(.+?)>", addr)
                        if match:
                            recipients.append(match.group(1))
                    else:
                        recipients.append(addr)

        # Date
        date_str = msg.get("Date", "")
        try:
            received_at = parsedate_to_datetime(date_str)
        except Exception:
            received_at = datetime.utcnow()

        # Flags for read status
        is_read = True  # IMAP doesn't always give us flags easily

        # Body extraction
        body_text = None
        body_html = None

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))

                # Skip attachments
                if "attachment" in content_disposition:
                    continue

                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or "utf-8"
                        text = payload.decode(charset, errors="replace")

                        if content_type == "text/plain" and not body_text:
                            body_text = text
                        elif content_type == "text/html" and not body_html:
                            body_html = text
                except Exception:
                    pass
        else:
            try:
                payload = msg.get_payload(decode=True)
                if payload:
                    charset = msg.get_content_charset() or "utf-8"
                    text = payload.decode(charset, errors="replace")
                    content_type = msg.get_content_type()
                    if content_type == "text/html":
                        body_html = text
                    else:
                        body_text = text
            except Exception:
                pass

        return RawMessage(
            message_id=message_id,
            subject=subject,
            sender=sender,
            sender_name=sender_name,
            recipients=recipients,
            received_at=received_at,
            is_read=is_read,
            body_text=body_text,
            body_html=body_html,
            raw_data={},
        )

    def fetch_messages(
        self, account: Account, options: FetchOptions = None
    ) -> Iterator[RawMessage]:
        """Fetch messages from IMAP server."""
        options = options or FetchOptions()

        conn = self._get_connection(account)

        try:
            # Select INBOX
            conn.select("INBOX")

            # Build search criteria
            search_criteria = "ALL"

            # Date filter
            if options.since:
                date_str = options.since.strftime("%d-%b-%Y")
                search_criteria = f'(SINCE "{date_str}")'

            # Search for messages
            status, message_ids = conn.search(None, search_criteria)

            if status != "OK":
                raise IMAPAdapterError(f"Failed to search messages: {status}")

            message_id_list = message_ids[0].split()

            # Apply limit (from newest to oldest)
            if options.limit and len(message_id_list) > options.limit:
                message_id_list = message_id_list[-options.limit:]

            # Fetch messages
            for msg_id in message_id_list:
                status, msg_data = conn.fetch(msg_id, "(RFC822)")

                if status != "OK":
                    continue

                # Parse the message
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                # Use IMAP message ID as unique ID
                imap_id = msg_id.decode()

                raw_msg = self._parse_message(msg, f"imap-{imap_id}")
                yield raw_msg

        except IMAPAdapterError:
            raise
        except Exception as e:
            raise IMAPAdapterError(f"Failed to fetch messages: {e}") from e

    def get_message(self, account: Account, message_id: str) -> Optional[RawMessage]:
        """Get a specific message by ID."""
        if not message_id.startswith("imap-"):
            return None

        imap_id = message_id[5:]  # Remove "imap-" prefix

        conn = self._get_connection(account)

        try:
            conn.select("INBOX")
            status, msg_data = conn.fetch(imap_id.encode(), "(RFC822)")

            if status != "OK":
                return None

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            return self._parse_message(msg, message_id)

        except Exception:
            return None

    def authenticate(self, account: Account) -> bool:
        """Test authentication with IMAP server."""
        try:
            conn = self._connect(account)
            conn.logout()
            return True
        except (IMAPAuthError, IMAPConnectionError):
            return False

    def test_connection(self, account: Account) -> bool:
        """Test connection to IMAP server."""
        return self.authenticate(account)


class QQMailAdapter(IMAPAdapter):
    """QQ Mail IMAP adapter."""

    @property
    def provider(self) -> EmailProvider:
        return EmailProvider.QQ


class NetEaseMailAdapter(IMAPAdapter):
    """NetEase Mail (163/126) IMAP adapter."""

    @property
    def provider(self) -> EmailProvider:
        return EmailProvider.NETEASE