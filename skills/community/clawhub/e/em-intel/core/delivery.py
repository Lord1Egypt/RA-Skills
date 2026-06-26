"""Delivery channel routing: Telegram, Slack, Email, or stdout."""

import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests

logger = logging.getLogger(__name__)


def send(text: str, title: str = "EM Intel Report") -> bool:
    """Route a message to the configured delivery channel.

    Reads EM_DELIVERY env var to determine channel.
    Falls back to print if channel is unset or fails.

    Returns:
        True if delivery succeeded, False otherwise.
    """
    channel = os.getenv("EM_DELIVERY", "print").lower()

    if channel == "telegram":
        return _send_telegram(text, title)
    elif channel == "slack":
        return _send_slack(text, title)
    elif channel == "email":
        return _send_email(text, title)
    else:
        return _send_print(text, title)


def _send_telegram(text: str, title: str) -> bool:
    """Send via Telegram Bot API."""
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        logger.warning("Telegram credentials not configured, falling back to print")
        return _send_print(text, title)

    message = f"*{title}*\n\n{text}"
    # Telegram has a 4096 char limit; truncate if needed
    if len(message) > 4096:
        message = message[:4090] + "\n..."

    try:
        resp = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "Markdown",
            },
            timeout=15,
        )
        resp.raise_for_status()
        logger.info("Sent to Telegram chat %s", chat_id)
        return True
    except requests.RequestException as exc:
        logger.warning("Telegram delivery failed: %s", exc)
        return False


def _send_slack(text: str, title: str) -> bool:
    """Send via Slack incoming webhook."""
    webhook_url = os.getenv("SLACK_WEBHOOK_URL", "")
    if not webhook_url:
        logger.warning("Slack webhook not configured, falling back to print")
        return _send_print(text, title)

    try:
        resp = requests.post(
            webhook_url,
            json={"text": f"*{title}*\n\n{text}"},
            timeout=15,
        )
        resp.raise_for_status()
        logger.info("Sent to Slack webhook")
        return True
    except requests.RequestException as exc:
        logger.warning("Slack delivery failed: %s", exc)
        return False


def _markdown_to_html(text: str, title: str) -> str:
    """Convert Markdown newsletter to a clean HTML email."""
    try:
        import markdown as md
        body_html = md.markdown(text, extensions=["tables", "nl2br"])
    except ImportError:
        # Fallback: wrap plain text in pre tag
        body_html = f"<pre>{text}</pre>"

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
         max-width: 680px; margin: 0 auto; padding: 24px; color: #1a1a1a; }}
  h1 {{ color: #1a1a1a; font-size: 22px; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; }}
  h2 {{ color: #374151; font-size: 16px; margin-top: 24px; }}
  a {{ color: #2563eb; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 14px; }}
  th {{ background: #f3f4f6; text-align: left; padding: 8px 12px; }}
  td {{ padding: 6px 12px; border-bottom: 1px solid #e5e7eb; }}
  ul {{ padding-left: 20px; }}
  li {{ margin: 4px 0; }}
  em {{ color: #6b7280; font-size: 13px; }}
  hr {{ border: none; border-top: 1px solid #e5e7eb; margin: 24px 0; }}
</style>
</head>
<body>
<h1>{title}</h1>
{body_html}
</body>
</html>"""


def _send_email(text: str, title: str) -> bool:
    """Send via SMTP as multipart/alternative (HTML + plain text fallback)."""
    host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER", "")
    password = os.getenv("SMTP_PASSWORD", "")
    to_addr = os.getenv("SMTP_TO", "")

    if not user or not password or not to_addr:
        logger.warning("SMTP not fully configured, falling back to print")
        return _send_print(text, title)

    # Build multipart/alternative: plain text + HTML
    msg = MIMEMultipart("alternative")
    msg["Subject"] = title
    msg["From"] = user
    msg["To"] = to_addr

    # Plain text part (for clients that prefer it)
    msg.attach(MIMEText(text, "plain", "utf-8"))

    # HTML part — Markdown converted to HTML with clickable Jira links
    html = _markdown_to_html(text, title)
    msg.attach(MIMEText(html, "html", "utf-8"))

    try:
        with smtplib.SMTP(host, port, timeout=15) as server:
            server.starttls()
            server.login(user, password)
            server.send_message(msg)
        logger.info("Email sent to %s", to_addr)
        return True
    except Exception as exc:
        logger.warning("Email delivery failed: %s", exc)
        return False


def _send_print(text: str, title: str) -> bool:
    """Fallback: print to stdout."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}\n")
    print(text)
    return True
