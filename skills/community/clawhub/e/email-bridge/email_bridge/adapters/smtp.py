"""SMTP adapter for sending emails via QQ Mail, NetEase Mail, etc."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from typing import Optional

from ..models import Account, EmailProvider
from .base import BaseAdapter


class SMTPAdapterError(Exception):
    """Base exception for SMTP adapter errors."""
    pass


class SMTPAuthError(SMTPAdapterError):
    """Raised when authentication fails."""
    pass


class SMTPSendError(SMTPAdapterError):
    """Raised when sending fails."""
    pass


# SMTP server configurations
SMTP_SERVERS = {
    EmailProvider.QQ: {
        "host": "smtp.qq.com",
        "port": 465,
    },
    EmailProvider.NETEASE: {
        "163.com": {"host": "smtp.163.com", "port": 465},
        "126.com": {"host": "smtp.126.com", "port": 465},
        "yeah.net": {"host": "smtp.yeah.net", "port": 465},
    },
    EmailProvider.GMAIL: {
        "host": "smtp.gmail.com",
        "port": 465,
    },
}


class SMTPAdapter:
    """SMTP adapter for sending emails.

    Configuration (via account.config):
        password: Authorization code (NOT the login password)
            - QQ Mail: Same as IMAP authorization code
            - 163/126: Same as IMAP authorization code
            - Gmail: App password (need to enable 2FA first)
    """

    def _get_smtp_server(self, account: Account) -> tuple[str, int]:
        """Get SMTP server host and port for the account."""
        provider = account.provider
        email_domain = account.email.split("@")[1].lower()

        if provider == EmailProvider.QQ:
            config = SMTP_SERVERS[EmailProvider.QQ]
            return config["host"], config["port"]

        elif provider == EmailProvider.NETEASE:
            netease_config = SMTP_SERVERS[EmailProvider.NETEASE]
            if email_domain in netease_config:
                return netease_config[email_domain]["host"], netease_config[email_domain]["port"]
            return netease_config["163.com"]["host"], netease_config["163.com"]["port"]

        elif provider == EmailProvider.GMAIL:
            config = SMTP_SERVERS[EmailProvider.GMAIL]
            return config["host"], config["port"]

        raise SMTPAdapterError(f"Unknown provider: {provider}")

    def send_email(
        self,
        account: Account,
        to: list[str],
        subject: str,
        body_text: Optional[str] = None,
        body_html: Optional[str] = None,
        cc: Optional[list[str]] = None,
        bcc: Optional[list[str]] = None,
        from_name: Optional[str] = None,
    ) -> bool:
        """Send an email.

        Args:
            account: The account to send from
            to: List of recipient email addresses
            subject: Email subject
            body_text: Plain text body
            body_html: HTML body
            cc: List of CC recipients
            bcc: List of BCC recipients
            from_name: Display name for sender

        Returns:
            True if sent successfully

        Raises:
            SMTPAuthError: Authentication failed
            SMTPSendError: Sending failed
        """
        password = account.config.get("password")
        if not password:
            raise SMTPAuthError(
                f"Password/authorization code not set for {account.email}. "
                "Please set it in account config."
            )

        host, port = self._get_smtp_server(account)

        # Build message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject

        # From
        if from_name:
            msg["From"] = formataddr((from_name, account.email))
        else:
            msg["From"] = account.email

        # To
        msg["To"] = ", ".join(to)

        # CC
        if cc:
            msg["Cc"] = ", ".join(cc)

        # Body
        if body_text:
            msg.attach(MIMEText(body_text, "plain", "utf-8"))
        if body_html:
            msg.attach(MIMEText(body_html, "html", "utf-8"))

        if not body_text and not body_html:
            msg.attach(MIMEText("", "plain", "utf-8"))

        # All recipients
        all_recipients = to + (cc or []) + (bcc or [])

        try:
            # Connect and send
            with smtplib.SMTP_SSL(host, port) as server:
                server.login(account.email, password)
                server.sendmail(account.email, all_recipients, msg.as_string())

            return True

        except smtplib.SMTPAuthenticationError as e:
            raise SMTPAuthError(
                f"Authentication failed for {account.email}. "
                "Make sure you're using the authorization code, not your password."
            ) from e
        except smtplib.SMTPException as e:
            raise SMTPSendError(f"Failed to send email: {e}") from e
        except Exception as e:
            raise SMTPSendError(f"Failed to send email: {e}") from e

    def test_connection(self, account: Account) -> bool:
        """Test SMTP connection and authentication."""
        password = account.config.get("password")
        if not password:
            return False

        host, port = self._get_smtp_server(account)

        try:
            with smtplib.SMTP_SSL(host, port) as server:
                server.login(account.email, password)
            return True
        except Exception:
            return False