"""Command-line interface for email bridge."""

import click
from datetime import datetime
from typing import Optional

from .models import EmailProvider, AccountStatus, EmailCategory
from .service import EmailBridgeService
from .extraction import extract_from_email
from .db import Database


def get_service() -> EmailBridgeService:
    """Get service instance."""
    return EmailBridgeService()


@click.group()
@click.version_option()
def main():
    """Email Bridge - Minimal personal email middleware."""
    pass


# Account commands
@main.group()
def accounts():
    """Manage email accounts."""
    pass


@accounts.command("list")
@click.option("--all", "show_all", is_flag=True, help="Include disabled accounts")
def accounts_list(show_all: bool):
    """List all configured accounts."""
    service = get_service()
    accounts = service.list_accounts(include_disabled=show_all)

    if not accounts:
        click.echo("No accounts configured.")
        return

    for acc in accounts:
        status = click.style(acc.status.value, fg="green" if acc.status == AccountStatus.ACTIVE else "red")
        click.echo(f"[{acc.id}] {acc.email} ({acc.provider.value}) - {status}")
        if acc.display_name:
            click.echo(f"    Name: {acc.display_name}")


@accounts.command("add")
@click.argument("email")
@click.option("--provider", "-p", type=click.Choice(["mock", "gmail", "qq", "netease"]), required=True)
@click.option("--name", "-n", help="Display name for the account")
@click.option("--config", "-c", "config_json", help="JSON config (e.g. '{\"password\": \"xxx\"}')")
def accounts_add(email: str, provider: str, name: Optional[str], config_json: Optional[str]):
    """Add a new email account."""
    import json
    service = get_service()

    config = None
    if config_json:
        try:
            config = json.loads(config_json)
        except json.JSONDecodeError as e:
            click.echo(f"Invalid JSON config: {e}", err=True)
            raise click.Abort()

    try:
        account = service.add_account(
            email=email,
            provider=EmailProvider(provider),
            display_name=name,
            config=config
        )
        click.echo(f"Added account: [{account.id}] {account.email}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@accounts.command("update")
@click.argument("account_id")
@click.option("--name", "-n", help="Update display name")
@click.option("--disable", is_flag=True, help="Disable the account")
@click.option("--enable", is_flag=True, help="Enable the account")
def accounts_update(account_id: str, name: Optional[str], disable: bool, enable: bool):
    """Update an account."""
    service = get_service()

    status = None
    if disable:
        status = AccountStatus.DISABLED
    elif enable:
        status = AccountStatus.ACTIVE

    account = service.update_account(account_id, display_name=name, status=status)
    if account:
        click.echo(f"Updated account: [{account.id}] {account.email}")
    else:
        click.echo(f"Account not found: {account_id}", err=True)
        raise click.Abort()


@accounts.command("delete")
@click.argument("account_id")
@click.option("--force", "-f", is_flag=True, help="Skip confirmation")
def accounts_delete(account_id: str, force: bool):
    """Delete an account and all its messages."""
    if not force:
        if not click.confirm(f"Delete account {account_id} and all messages?"):
            click.echo("Aborted.")
            return

    service = get_service()
    if service.delete_account(account_id):
        click.echo(f"Deleted account: {account_id}")
    else:
        click.echo(f"Account not found: {account_id}", err=True)


# Message commands
@main.group()
def messages():
    """View and manage messages."""
    pass


@messages.command("list")
@click.option("--account", "-a", "account_id", help="Filter by account ID")
@click.option("--limit", "-n", default=20, help="Number of messages to show")
def messages_list(account_id: Optional[str], limit: int):
    """List recent messages."""
    service = get_service()
    msgs = service.list_recent_messages(account_id=account_id, limit=limit)

    if not msgs:
        click.echo("No messages found.")
        return

    for msg in msgs:
        read_marker = " " if msg.is_read else click.style("*", fg="yellow", bold=True)
        cat_color = {
            EmailCategory.VERIFICATION: "cyan",
            EmailCategory.SECURITY: "red",
            EmailCategory.SUBSCRIPTION: "blue",
            EmailCategory.SPAM_LIKE: "magenta",
            EmailCategory.NORMAL: "white",
        }.get(msg.category, "white")

        cat = click.style(f"[{msg.category.value:12}]", fg=cat_color)
        click.echo(f"{read_marker} [{msg.id.split(':')[1][:12]}] {cat} {msg.received_at.strftime('%Y-%m-%d %H:%M')}")
        click.echo(f"  From: {msg.sender_name or msg.sender}")
        click.echo(f"  Subj: {msg.subject[:60]}{'...' if len(msg.subject) > 60 else ''}")


@messages.command("unread")
@click.option("--account", "-a", "account_id", help="Filter by account ID")
@click.option("--limit", "-n", default=20, help="Number of messages to show")
def messages_unread(account_id: Optional[str], limit: int):
    """List unread messages."""
    service = get_service()
    msgs = service.list_unread_messages(account_id=account_id, limit=limit)

    if not msgs:
        click.echo("No unread messages.")
        return

    click.echo(f"Unread messages ({len(msgs)}):")
    for msg in msgs:
        click.echo(f"* [{msg.id.split(':')[1][:12]}] {msg.sender_name or msg.sender}")
        click.echo(f"  {msg.subject[:60]}{'...' if len(msg.subject) > 60 else ''}")


@messages.command("search")
@click.option("--keyword", "-k", help="Search keyword")
@click.option("--account", "-a", "account_id", help="Filter by account ID")
@click.option("--from-date", help="Start date (YYYY-MM-DD)")
@click.option("--to-date", help="End date (YYYY-MM-DD)")
@click.option("--limit", "-n", default=50, help="Max results")
def messages_search(
    keyword: Optional[str],
    account_id: Optional[str],
    from_date: Optional[str],
    to_date: Optional[str],
    limit: int
):
    """Search messages by keyword and/or date range."""
    service = get_service()

    start_time = None
    end_time = None
    if from_date:
        start_time = datetime.strptime(from_date, "%Y-%m-%d")
    if to_date:
        end_time = datetime.strptime(to_date, "%Y-%m-%d")

    msgs = service.search_messages(
        keyword=keyword,
        start_time=start_time,
        end_time=end_time,
        account_id=account_id,
        limit=limit
    )

    if not msgs:
        click.echo("No messages found.")
        return

    click.echo(f"Found {len(msgs)} message(s):")
    for msg in msgs:
        click.echo(f"[{msg.id.split(':')[1][:12]}] {msg.received_at.strftime('%Y-%m-%d')} - {msg.subject[:50]}")


@messages.command("get")
@click.argument("message_id")
def messages_get(message_id: str):
    """Get full details of a message."""
    service = get_service()
    msg = service.get_message(message_id)

    if not msg:
        click.echo(f"Message not found: {message_id}", err=True)
        raise click.Abort()

    click.echo(f"Subject: {msg.subject}")
    click.echo(f"From: {msg.sender_name} <{msg.sender}>" if msg.sender_name else f"From: {msg.sender}")
    click.echo(f"To: {', '.join(msg.recipients)}")
    click.echo(f"Date: {msg.received_at.strftime('%Y-%m-%d %H:%M')}")
    click.echo(f"Category: {msg.category.value}")
    click.echo(f"Read: {'Yes' if msg.is_read else 'No'}")
    click.echo()

    if msg.body_text:
        click.echo("--- Body ---")
        click.echo(msg.body_text)
    elif msg.preview:
        click.echo("--- Preview ---")
        click.echo(msg.preview)


@messages.command("read")
@click.argument("message_id")
@click.option("--unread", "-u", is_flag=True, help="Mark as unread instead")
def messages_read(message_id: str, unread: bool):
    """Mark a message as read (or unread with --unread)."""
    service = get_service()
    if service.mark_read(message_id, is_read=not unread):
        status = "unread" if unread else "read"
        click.echo(f"Marked message as {status}: {message_id}")
    else:
        click.echo(f"Message not found: {message_id}", err=True)


# Sync command
@main.command("sync")
@click.option("--account", "-a", "account_id", help="Sync specific account only")
@click.option("--days", "-d", default=None, type=int, help="Sync messages from last N days")
def sync(account_id: Optional[str], days: Optional[int]):
    """Sync messages from providers.

    This fetches messages from configured email providers into local storage.
    Gmail accounts require credentials setup (see README.md).

    Examples:
        email-bridge sync                    # Sync all accounts
        email-bridge sync -a abc123          # Sync specific account
        email-bridge sync --days 3           # Sync last 3 days only
    """
    service = get_service()

    since = None
    if days:
        from datetime import timedelta
        since = datetime.utcnow() - timedelta(days=days)

    if account_id:
        try:
            count = service.sync_account(account_id, since=since)
            click.echo(f"Synced {count} message(s) from account {account_id}")
        except ValueError as e:
            click.echo(f"Sync failed: {e}", err=True)
        except Exception as e:
            # Check for Gmail-specific errors
            error_msg = str(e)
            if "credentials not found" in error_msg.lower():
                click.echo(f"Gmail credentials not found. See README.md for setup instructions.", err=True)
            elif "authentication" in error_msg.lower() or "auth" in error_msg.lower():
                click.echo(f"Authentication failed: {e}", err=True)
            else:
                click.echo(f"Sync failed: {e}", err=True)
    else:
        results = service.sync_all_accounts(since=since)
        for acc_id, result in results.items():
            if isinstance(result, int):
                click.echo(f"Account {acc_id}: {result} message(s)")
            else:
                click.echo(f"Account {acc_id}: {result}")


# Stats command
@main.command("stats")
def stats():
    """Show statistics."""
    service = get_service()
    s = service.get_stats()
    click.echo(f"Accounts: {s['active_accounts']} active / {s['total_accounts']} total")
    click.echo(f"Unread: {s['unread_messages']}")


# Extraction commands
@main.command("extract")
@click.argument("message_id")
@click.option("--codes", "-c", is_flag=True, help="Show verification codes")
@click.option("--links", "-l", is_flag=True, help="Show action links")
@click.option("--all", "show_all", is_flag=True, help="Show all extractions")
def extract(message_id: str, codes: bool, links: bool, show_all: bool):
    """Extract verification codes and action links from a message.

    Examples:
        email-bridge extract mock-001 --codes
        email-bridge extract mock-001 --links
        email-bridge extract mock-001 --all
    """
    service = get_service()
    msg = service.get_message(message_id)

    if not msg:
        click.echo(f"Message not found: {message_id}", err=True)
        raise click.Abort()

    # Default to showing all if no specific flag
    if not codes and not links:
        show_all = True

    # Extract from message
    extracted = extract_from_email(
        subject=msg.subject,
        body_text=msg.body_text,
        body_html=msg.body_html
    )

    if show_all or codes:
        if extracted['codes']:
            click.echo(click.style("Verification Codes:", fg="cyan", bold=True))
            for code in extracted['codes']:
                ctx = f" ({code.context})" if code.context else ""
                click.echo(f"  {click.style(code.code, fg='yellow')}{ctx}")
        else:
            click.echo("No verification codes found.")

    if show_all or links:
        if extracted['links']:
            click.echo(click.style("\nAction Links:", fg="cyan", bold=True))
            for link in extracted['links']:
                link_type = click.style(f"[{link.link_type}]", fg="green")
                domain = f" ({link.domain})" if link.domain else ""
                click.echo(f"  {link_type} {link.url}{domain}")
                if link.text:
                    click.echo(f"    Context: {link.text[:60]}...")
        else:
            click.echo("No action links found.")


@main.command("codes")
@click.option("--account", "-a", "account_id", help="Filter by account ID")
@click.option("--limit", "-n", default=20, help="Number of messages to check")
def codes(account_id: Optional[str], limit: int):
    """Find verification codes in recent messages.

    Scans recent messages and extracts any verification codes found.
    """
    service = get_service()
    msgs = service.list_recent_messages(account_id=account_id, limit=limit)

    found_any = False
    for msg in msgs:
        extracted = extract_from_email(
            subject=msg.subject,
            body_text=msg.body_text,
            body_html=msg.body_html
        )

        if extracted['codes']:
            found_any = True
            click.echo(f"\n[{msg.id.split(':')[1][:12]}] {msg.subject[:50]}")
            click.echo(f"  From: {msg.sender_name or msg.sender}")
            for code in extracted['codes']:
                ctx = f" ({code.context})" if code.context else ""
                click.echo(f"  Code: {click.style(code.code, fg='yellow')}{ctx}")

    if not found_any:
        click.echo("No verification codes found in recent messages.")


# Send command
@main.command("send")
@click.option("--account", "-a", "account_id", required=True, help="Account ID to send from")
@click.option("--to", "-t", "recipients", multiple=True, required=True, help="Recipient email address")
@click.option("--cc", "-c", "cc_list", multiple=True, help="CC email address")
@click.option("--subject", "-s", required=True, help="Email subject")
@click.option("--body", "-b", "body_text", help="Email body (plain text)")
@click.option("--html", "-h", "body_html", help="Email body (HTML)")
def send_email(
    account_id: str,
    recipients: tuple,
    cc_list: tuple,
    subject: str,
    body_text: Optional[str],
    body_html: Optional[str]
):
    """Send an email.

    Examples:
        email-bridge send -a abc123 -t user@example.com -s "Hello" -b "Hi there!"
        email-bridge send -a abc123 -t user1@example.com -t user2@example.com -s "Hello" -b "Hi!"
    """
    service = get_service()

    # Convert tuples to lists
    to_list = list(recipients)
    cc = list(cc_list) if cc_list else None

    # If no body provided, prompt for it
    if not body_text and not body_html:
        click.echo("No body provided. Use --body or --html option.")
        raise click.Abort()

    try:
        result = service.send_email(
            account_id=account_id,
            to=to_list,
            subject=subject,
            body_text=body_text,
            body_html=body_html,
            cc=cc,
        )
        if result:
            click.echo(click.style("✓ Email sent successfully!", fg="green"))
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Failed to send email: {e}", err=True)
        raise click.Abort()


# Daemon commands
@main.group()
def daemon():
    """Manage the background daemon for real-time email monitoring."""
    pass


def _load_daemon_config() -> dict:
    """Load daemon configuration from config file.
    
    Returns:
        Dict with daemon settings or empty dict if no config file
    """
    import json
    from pathlib import Path
    
    config_path = Path.home() / ".email-bridge" / "config.json"
    if not config_path.exists():
        return {}
    
    try:
        with open(config_path) as f:
            config = json.load(f)
            return config.get("daemon", {})
    except Exception:
        return {}


@daemon.command("start")
@click.option("-d", "--detach", is_flag=True, help="Run in background (daemon mode)")
@click.option("-i", "--interval", default=300, type=int, help="Polling interval in seconds (default: 300)")
@click.option("--no-notify", is_flag=True, help="Disable OpenClaw notifications")
def daemon_start(detach: bool, interval: int, no_notify: bool):
    """Start the email monitoring daemon.

    The daemon monitors your email accounts in real-time using IMAP IDLE
    (for QQ/NetEase) or polling (for Gmail).

    When new emails arrive, the daemon will:
    - Sync them to local database
    - Send a notification to OpenClaw main session (unless --no-notify)

    Configuration is read from ~/.email-bridge/config.json:
    {
      "daemon": {
        "poll_interval": 300,
        "notify_openclaw": true,
        "notification": {
          "include_body": false,
          "body_max_length": 500,
          "include_verification_codes": true,
          "include_links": false
        }
      }
    }

    Examples:
        email-bridge daemon start           # Run in foreground
        email-bridge daemon start -d        # Run in background
        email-bridge daemon start -i 60     # Poll every 60 seconds
        email-bridge daemon start -d --no-notify  # No OpenClaw notifications
    """
    from .daemon import EmailDaemon
    
    # Load config from file
    config = _load_daemon_config()
    
    # CLI options override config file
    poll_interval = interval
    notify = not no_notify
    notification_config = config.get("notification", {})
    
    # Use config file values if CLI options are defaults
    if config.get("poll_interval") and interval == 300:  # Default value
        poll_interval = config["poll_interval"]
    if config.get("notify_openclaw") is not None and not no_notify:
        notify = config["notify_openclaw"]

    d = EmailDaemon(
        poll_interval=poll_interval,
        notify_openclaw=notify,
        notification_config=notification_config
    )
    d.start(background=detach)


@daemon.command("stop")
def daemon_stop():
    """Stop the email monitoring daemon."""
    from .daemon import EmailDaemon

    d = EmailDaemon()
    d.stop()


@daemon.command("status")
def daemon_status():
    """Show daemon status."""
    from .daemon import EmailDaemon
    import json

    d = EmailDaemon()
    status = d.status()

    if status["running"]:
        click.echo(click.style("✓ Daemon is running", fg="green"))
        click.echo(f"  PID: {status['pid']}")
        if status["accounts"]:
            click.echo("\n  Monitored accounts:")
            for acc in status["accounts"]:
                click.echo(f"    - {acc['email']} ({acc['provider']})")
    else:
        click.echo(click.style("✗ Daemon is not running", fg="red"))


if __name__ == "__main__":
    main()
