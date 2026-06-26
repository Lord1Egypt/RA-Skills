#!/usr/bin/env python3
"""Email Bridge Daemon - Background service for real-time email monitoring.

This daemon runs in the background and monitors email accounts using IMAP IDLE
for real-time new message notifications.

Usage:
    email-bridge daemon start
    email-bridge daemon stop
    email-bridge daemon status
"""

import json
import os
import signal
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable, Dict, Any

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from email_bridge.models import EmailProvider
from email_bridge.service import EmailBridgeService
from email_bridge.adapters.imap import IMAPAdapter
from email_bridge.sanitize import sanitize_for_notification, sanitize_sender, sanitize_subject
from email_bridge.extraction import extract_verification_codes


class EmailDaemon:
    """Background daemon for monitoring emails."""

    def __init__(
        self,
        poll_interval: int = 300,  # Fallback polling interval (seconds)
        on_new_email: Optional[Callable[[Dict[str, Any]], None]] = None,
        notify_openclaw: bool = True,  # Send notifications to OpenClaw
        notification_time_limit: int = 3600,  # Only notify for emails received within this many seconds
        notification_config: Optional[Dict[str, Any]] = None,  # Notification settings
        idle_timeout: int = 60,  # IDLE timeout in seconds (keepalive interval)
        sync_max_retries: int = 3,  # Max retries when sync fails
        sync_retry_delay: float = 2.0,  # Delay between sync retries (seconds)
    ):
        """Initialize the daemon.

        Args:
            poll_interval: Fallback polling interval in seconds (default 5 min)
            on_new_email: Callback function when new email arrives
            notify_openclaw: Send new email notifications to OpenClaw main session
            notification_time_limit: Only notify for emails received within this time (seconds)
            notification_config: Dict with notification settings:
                - include_body: bool (default False)
                - body_max_length: int (default 500)
                - include_verification_codes: bool (default True)
                - include_links: bool (default False)
            idle_timeout: IDLE timeout in seconds, acts as keepalive interval (default 60)
            sync_max_retries: Max retries when sync fails after detecting new mail (default 3)
            sync_retry_delay: Delay between sync retries in seconds (default 2.0)
        """
        self.poll_interval = poll_interval
        self.on_new_email = on_new_email
        self.notify_openclaw = notify_openclaw
        self.notification_time_limit = notification_time_limit
        self.idle_timeout = idle_timeout
        self.sync_max_retries = sync_max_retries
        self.sync_retry_delay = sync_retry_delay
        
        # Default notification config
        self.notification_config = notification_config or {}
        self.notification_config.setdefault('include_body', False)
        self.notification_config.setdefault('body_max_length', 500)
        self.notification_config.setdefault('include_verification_codes', True)
        self.notification_config.setdefault('include_links', False)
        
        self.service = EmailBridgeService()
        self._running = False
        self._threads: Dict[str, threading.Thread] = {}
        self._stop_events: Dict[str, threading.Event] = {}
        self._last_seen: Dict[str, set] = {}  # account_id -> set of message_ids
        self._notified_messages: Dict[str, set] = {}  # account_id -> set of notified message_ids

        # PID file for daemon management
        self.pid_file = Path.home() / ".email-bridge" / "daemon.pid"
        self.log_file = Path.home() / ".email-bridge" / "daemon.log"

    def start(self, background: bool = False):
        """Start the daemon.

        Args:
            background: If True, fork to background (daemon mode)
        """
        if self.is_running():
            print("Daemon is already running")
            return

        if background:
            self._fork_to_background()
        else:
            self._run_foreground()

    def stop(self):
        """Stop the daemon."""
        if not self.is_running():
            print("Daemon is not running")
            return

        pid = self._read_pid()
        if pid:
            try:
                os.kill(pid, signal.SIGTERM)
                print(f"Sent SIGTERM to daemon (PID {pid})")
                # Wait for daemon to stop
                for _ in range(10):
                    time.sleep(0.5)
                    if not self.is_running():
                        break
                if self.is_running():
                    os.kill(pid, signal.SIGKILL)
                    print(f"Sent SIGKILL to daemon (PID {pid})")
            except ProcessLookupError:
                pass

        # Clean up PID file
        if self.pid_file.exists():
            self.pid_file.unlink()

    def status(self) -> dict:
        """Get daemon status."""
        result = {
            "running": self.is_running(),
            "pid": self._read_pid(),
            "accounts": [],
        }

        if self.is_running():
            accounts = self.service.list_accounts()
            for acc in accounts:
                if acc.status.value == "active":
                    result["accounts"].append({
                        "id": acc.id,
                        "email": acc.email,
                        "provider": acc.provider.value,
                    })

        return result

    def is_running(self) -> bool:
        """Check if daemon is running."""
        pid = self._read_pid()
        if not pid:
            return False

        try:
            os.kill(pid, 0)  # Check if process exists
            return True
        except ProcessLookupError:
            # PID file exists but process is dead
            if self.pid_file.exists():
                self.pid_file.unlink()
            return False

    def _read_pid(self) -> Optional[int]:
        """Read PID from file."""
        if not self.pid_file.exists():
            return None
        try:
            return int(self.pid_file.read_text().strip())
        except (ValueError, IOError):
            return None

    def _write_pid(self):
        """Write current PID to file."""
        self.pid_file.parent.mkdir(parents=True, exist_ok=True)
        self.pid_file.write_text(str(os.getpid()))

    def _fork_to_background(self):
        """Fork to background (Unix daemon)."""
        # First fork
        pid = os.fork()
        if pid > 0:
            # Parent exits
            print(f"Daemon started in background (PID {pid})")
            sys.exit(0)

        # Decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # Second fork
        pid = os.fork()
        if pid > 0:
            sys.exit(0)

        # Redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()

        # Redirect to log file
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.log_file, "a") as log:
            os.dup2(log.fileno(), sys.stdout.fileno())
            os.dup2(log.fileno(), sys.stderr.fileno())

        # Write PID
        self._write_pid()

        # Run daemon
        self._run()

    def _run_foreground(self):
        """Run in foreground (for debugging)."""
        self._write_pid()
        print(f"Daemon started (PID {os.getpid()})")
        try:
            self._run()
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            if self.pid_file.exists():
                self.pid_file.unlink()

    def _run(self):
        """Main daemon loop."""
        self._running = True

        # Set up signal handlers
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)

        self._log("Daemon started")

        # Get active accounts
        accounts = self.service.list_accounts()
        active_accounts = [a for a in accounts if a.status.value == "active"]

        if not active_accounts:
            self._log("No active accounts to monitor")
            return

        # Start a monitor thread for each account
        for account in active_accounts:
            if account.provider in [EmailProvider.QQ, EmailProvider.NETEASE]:
                self._start_account_monitor(account)
            elif account.provider == EmailProvider.GMAIL:
                # Gmail doesn't support IMAP IDLE, use polling
                self._start_account_poller(account)

        # Wait for stop signal
        while self._running:
            time.sleep(1)

        # Stop all threads
        for account_id in list(self._stop_events.keys()):
            self._stop_events[account_id].set()

        # Wait for threads to finish
        for thread in self._threads.values():
            thread.join(timeout=5)

        self._log("Daemon stopped")

    def _handle_signal(self, signum, frame):
        """Handle shutdown signals."""
        self._log(f"Received signal {signum}")
        self._running = False

    def _log(self, message: str):
        """Log a message."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] {message}"
        print(log_line, flush=True)

    def _start_account_monitor(self, account):
        """Start IMAP IDLE monitor for an account."""
        stop_event = threading.Event()
        self._stop_events[account.id] = stop_event

        thread = threading.Thread(
            target=self._monitor_account,
            args=(account, stop_event),
            daemon=True,
        )
        thread.start()
        self._threads[account.id] = thread
        self._log(f"Started monitor for {account.email}")

    def _start_account_poller(self, account):
        """Start polling for Gmail (no IDLE support)."""
        stop_event = threading.Event()
        self._stop_events[account.id] = stop_event

        thread = threading.Thread(
            target=self._poll_account,
            args=(account, stop_event),
            daemon=True,
        )
        thread.start()
        self._threads[account.id] = thread
        self._log(f"Started poller for {account.email} (interval: {self.poll_interval}s)")

    def _monitor_account(self, account, stop_event: threading.Event):
        """Monitor an account using IMAP IDLE with keepalive and sync retry.
        
        Features:
        - IDLE with configurable timeout (acts as keepalive)
        - Sync retry on failure (up to sync_max_retries times)
        - Automatic reconnection on connection errors
        """
        import imaplib2

        # Get IMAP server config
        host, port = self._get_imap_server(account)
        password = account.config.get("password")

        if not password:
            self._log(f"{account.email}: No password configured")
            return

        while not stop_event.is_set():
            try:
                # Connect
                conn = imaplib2.IMAP4_SSL(host, port)
                conn.login(account.email, password)
                conn.select("INBOX")

                # Get initial message count
                status, data = conn.search(None, "ALL")
                last_count = len(data[0].split()) if data[0] else 0
                self._log(f"{account.email}: Connected, {last_count} messages in inbox")

                # Clear any pending responses
                list(conn.pop_untagged_responses())

                # IDLE loop with keepalive
                last_keepalive = time.time()
                
                while not stop_event.is_set():
                    try:
                        # Use configured idle_timeout for keepalive
                        self._log(f"{account.email}: Entering IDLE mode (timeout={self.idle_timeout}s)...")

                        # Start IDLE - timeout acts as keepalive
                        result = conn.idle(timeout=self.idle_timeout)
                        last_keepalive = time.time()

                        # Check untagged responses for new mail notifications
                        untagged = list(conn.pop_untagged_responses())
                        
                        # Check for EXISTS response (new message)
                        for resp in untagged:
                            if len(resp) >= 2 and resp[0] == 'EXISTS':
                                new_count = int(resp[1][0]) if resp[1] else 0
                                self._log(f"{account.email}: EXISTS response, count={new_count}")
                                break

                        # Also check if message count changed
                        status, data = conn.search(None, "ALL")
                        current_count = len(data[0].split()) if data[0] else 0

                        if current_count > last_count:
                            new_msg_count = current_count - last_count
                            self._log(f"{account.email}: {new_msg_count} new message(s) detected!")
                            
                            # Sync with retry logic
                            sync_success = self._sync_with_retry(
                                account, new_msg_count, conn, stop_event
                            )
                            
                            if sync_success:
                                last_count = current_count
                                # Notify OpenClaw
                                self._notify_openclaw(account.email, new_msg_count, account.id)

                                # Trigger callback
                                if self.on_new_email:
                                    self.on_new_email({
                                        "account_id": account.id,
                                        "email": account.email,
                                        "new_count": new_msg_count,
                                    })
                            else:
                                # Sync failed after all retries, but still update count
                                # to avoid re-detecting same messages
                                last_count = current_count
                                self._log(f"{account.email}: Sync failed after {self.sync_max_retries} retries, will retry notification on next sync")
                        else:
                            self._log(f"{account.email}: No new messages (count: {current_count})")

                    except Exception as e:
                        self._log(f"{account.email}: IDLE error: {e}")
                        break

                try:
                    conn.logout()
                except:
                    pass
                self._log(f"{account.email}: Disconnected")

            except Exception as e:
                self._log(f"{account.email}: Connection error: {e}")

            # Wait before reconnecting
            if not stop_event.is_set():
                stop_event.wait(timeout=60)
    
    def _sync_with_retry(self, account, new_msg_count: int, conn, stop_event: threading.Event) -> bool:
        """Sync new messages with retry logic.
        
        Args:
            account: Email account to sync
            new_msg_count: Number of new messages detected
            conn: Current IMAP connection (may be used for direct fetch)
            stop_event: Stop event to check for shutdown
        
        Returns:
            True if sync succeeded, False otherwise
        """
        for attempt in range(1, self.sync_max_retries + 1):
            if stop_event.is_set():
                return False
                
            try:
                self._log(f"{account.email}: Syncing {new_msg_count} message(s) (attempt {attempt}/{self.sync_max_retries})")
                sync_count = self.service.sync_account(account.id, limit=new_msg_count)
                self._log(f"{account.email}: Synced {sync_count} message(s)")
                return True
                
            except Exception as e:
                self._log(f"{account.email}: Sync error (attempt {attempt}): {e}")
                
                if attempt < self.sync_max_retries:
                    # Wait before retry
                    if stop_event.wait(timeout=self.sync_retry_delay):
                        return False  # Stop requested
                    
                    # Try to reconnect IMAP if connection is broken
                    try:
                        # Test if connection is still alive
                        conn.noop()
                    except:
                        self._log(f"{account.email}: Connection lost, will reconnect")
                        return False  # Let outer loop handle reconnection
        
        return False  # All retries failed

    def _get_imap_server(self, account) -> tuple:
        """Get IMAP server host and port for an account."""
        from .adapters.imap import IMAP_SERVERS

        email_domain = account.email.split("@")[1].lower()

        if account.provider == EmailProvider.QQ:
            config = IMAP_SERVERS[EmailProvider.QQ]
            return config["host"], config["port"]
        elif account.provider == EmailProvider.NETEASE:
            netease_config = IMAP_SERVERS[EmailProvider.NETEASE]
            if email_domain in netease_config:
                return netease_config[email_domain]["host"], netease_config[email_domain]["port"]
            return netease_config["163.com"]["host"], netease_config["163.com"]["port"]

        raise ValueError(f"Unknown provider: {account.provider}")

    def _get_latest_message_info(self, account_id: str, count: int, time_limit: int = None) -> list:
        """Get details of the latest messages from an account.
        
        Args:
            account_id: Account ID
            count: Max number of messages to return
            time_limit: Only include messages received within this many seconds (default: self.notification_time_limit)
        
        Returns:
            List of message info dicts with sender, subject, message_id, received_at,
            and optionally body_preview, codes, links based on notification_config
        """
        from datetime import datetime, timedelta, timezone
        
        if time_limit is None:
            time_limit = self.notification_time_limit
            
        try:
            messages = self.service.list_recent_messages(account_id=account_id, limit=count * 2)
            
            # Get already notified messages
            notified = self._notified_messages.get(account_id, set())
            
            # Use timezone-aware now for comparison
            now = datetime.now(timezone.utc)
            time_cutoff = now - timedelta(seconds=time_limit)
            
            result = []
            for msg in messages:
                # Skip already notified messages
                if msg.id in notified:
                    continue
                    
                # Check time limit - handle both naive and aware datetimes
                if hasattr(msg, 'received_at') and msg.received_at:
                    msg_time = msg.received_at
                    # If message time is naive, assume UTC
                    if msg_time.tzinfo is None:
                        msg_time = msg_time.replace(tzinfo=timezone.utc)
                    if msg_time < time_cutoff:
                        continue
                
                # Build message info
                info = {
                    "message_id": msg.id,
                    "sender": sanitize_sender(msg.sender_name or msg.sender),
                    "subject": sanitize_subject(msg.subject),
                    "category": msg.category.value if hasattr(msg, 'category') and msg.category else "normal",
                }
                
                # Get body text (fallback to HTML if no plain text)
                import re
                body_text = msg.body_text
                if not body_text and msg.body_html:
                    # Strip HTML tags and CSS for basic text extraction
                    html = msg.body_html
                    # Remove style blocks
                    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
                    # Remove script blocks
                    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
                    # Remove HTML tags
                    html = re.sub(r'<[^>]+>', ' ', html)
                    # Decode HTML entities
                    import html as html_module
                    html = html_module.unescape(html)
                    # Normalize whitespace
                    body_text = re.sub(r'\s+', ' ', html).strip()
                
                # Optionally include body preview
                if self.notification_config.get('include_body') and body_text:
                    max_len = self.notification_config.get('body_max_length', 500)
                    info['body_preview'] = sanitize_for_notification(body_text, max_length=max_len)
                
                # Extract verification codes for all emails (not just verification category)
                if self.notification_config.get('include_verification_codes'):
                    codes = extract_verification_codes(f"{msg.subject}\n\n{body_text or ''}")
                    if codes:
                        info['codes'] = [c.code for c in codes[:3]]  # Max 3 codes
                
                # Optionally extract links (disabled by default for security)
                if self.notification_config.get('include_links') and body_text:
                    from email_bridge.extraction import extract_action_links
                    links = extract_action_links(body_text, msg.body_html)
                    # Only include verify/reset links, not unsubscribe
                    filtered_links = [l for l in links if l.link_type in ('verify', 'reset')][:2]
                    if filtered_links:
                        info['links'] = [{'type': l.link_type, 'domain': l.domain} for l in filtered_links]
                
                result.append(info)
                
                if len(result) >= count:
                    break
                    
            return result
        except Exception as e:
            self._log(f"Error getting message info: {e}")
            return []

    def _notify_openclaw(self, account_email: str, new_count: int, account_id: str = None):
        """Send notification to OpenClaw main session via system event.
        
        Uses structured JSON format internally for safety, then formats
        as human-readable text for display.
        """
        if not self.notify_openclaw:
            return

        try:
            import subprocess
            
            # Get message details if available
            details = []
            if account_id:
                details = self._get_latest_message_info(account_id, min(new_count, 3))
            
            # Skip notification if no new messages to report
            if not details:
                self._log(f"{account_email}: No new messages to notify (already notified or outside time limit)")
                return
            
            # Mark messages as notified
            if account_id not in self._notified_messages:
                self._notified_messages[account_id] = set()
            for info in details:
                self._notified_messages[account_id].add(info["message_id"])
            
            # Build structured data (for internal processing)
            notification = {
                "type": "email_notification",
                "account": account_email,
                "count": new_count,
                "messages": details
            }
            
            # Format as human-readable text
            message = self._format_notification(notification)
            
            self._log(f"Sending notification to OpenClaw: {len(details)} messages")
            result = subprocess.run(
                ["openclaw", "system", "event", "--text", message, "--mode", "now"],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                self._log(f"OpenClaw notification sent successfully")
            else:
                self._log(f"OpenClaw notification failed (code {result.returncode}): {result.stderr.strip() or 'No error'}")
        except subprocess.TimeoutExpired:
            self._log("OpenClaw notification timed out")
        except FileNotFoundError:
            self._log("OpenClaw CLI not found at PATH")
        except Exception as e:
            self._log(f"Error sending notification: {e}")

    def _format_notification(self, notification: dict) -> str:
        """Format notification data as human-readable text.
        
        Adapts format based on email category for better UX.
        
        Args:
            notification: Structured notification dict
        
        Returns:
            Human-readable text message
        """
        lines = [f"📧 新邮件: {notification['account']}"]
        
        for i, msg in enumerate(notification['messages'], 1):
            category = msg.get('category', 'normal')
            sender = msg['sender']
            subject = msg['subject']
            
            # Category emoji and format
            if category == 'verification':
                # 验证码邮件：重点显示验证码
                lines.append(f"\n{i}. 🔐 {sender}")
                lines.append(f"   {subject}")
                if msg.get('codes'):
                    codes_str = ', '.join(msg['codes'])
                    lines.append(f"   ✨ 验证码: {codes_str}")
                elif msg.get('body_preview'):
                    # 没提取到验证码但显示正文
                    lines.append(f"   📝 {msg['body_preview'][:80]}...")
                    
            elif category == 'security':
                # 安全邮件：突出警示
                lines.append(f"\n{i}. ⚠️ {sender}")
                lines.append(f"   {subject}")
                if msg.get('body_preview'):
                    lines.append(f"   📝 {msg['body_preview'][:100]}...")
                    
            elif category == 'transactional':
                # 交易邮件：订单/支付/发货
                lines.append(f"\n{i}. 📦 {sender}")
                lines.append(f"   {subject}")
                if msg.get('body_preview'):
                    lines.append(f"   📝 {msg['body_preview'][:100]}...")
                    
            elif category == 'promotion':
                # 推广邮件：营销/优惠/奖励
                lines.append(f"\n{i}. 🎁 {sender}")
                lines.append(f"   {subject}")
                if msg.get('body_preview'):
                    lines.append(f"   📝 {msg['body_preview'][:80]}...")
                    
            elif category == 'subscription':
                # 订阅邮件：简化显示
                lines.append(f"\n{i}. 📰 {sender}")
                lines.append(f"   {subject}")
                # 订阅邮件不显示正文，避免噪音
                
            elif category == 'spam_like':
                # 垃圾邮件：标记但不展开
                lines.append(f"\n{i}. 🚫 {sender}")
                lines.append(f"   {subject} (疑似垃圾)")
                
            else:
                # 普通邮件：标准格式
                lines.append(f"\n{i}. {sender}")
                lines.append(f"   {subject}")
                if msg.get('body_preview'):
                    lines.append(f"   📝 {msg['body_preview'][:100]}...")
                if msg.get('codes'):
                    codes_str = ', '.join(msg['codes'])
                    lines.append(f"   🔐 验证码: {codes_str}")
            
            # Links for any category
            if msg.get('links'):
                for link in msg['links'][:2]:
                    lines.append(f"   🔗 {link['type']}: {link['domain']}")
        
        if notification['count'] > len(notification['messages']):
            lines.append(f"\n... 还有 {notification['count'] - len(notification['messages'])} 封")
        
        return '\n'.join(lines)

    def _poll_account(self, account, stop_event: threading.Event):
        """Poll an account for new messages (for Gmail)."""
        # Track message count to detect new messages
        last_count = None
        
        while not stop_event.is_set():
            try:
                # Get current message count from database
                messages = self.service.list_recent_messages(account_id=account.id, limit=1000)
                current_count = len(messages)
                
                # First poll: just record the count, don't notify
                if last_count is None:
                    last_count = current_count
                    self._log(f"{account.email}: Initial count = {current_count}")
                elif current_count > last_count:
                    # New messages detected
                    new_count = current_count - last_count
                    self._log(f"{account.email}: {new_count} new message(s) detected (was {last_count}, now {current_count})")
                    last_count = current_count
                    
                    # Sync to get message details
                    self.service.sync_account(account.id, limit=new_count)
                    
                    # Notify OpenClaw
                    self._notify_openclaw(account.email, new_count, account.id)
                    
                    # Trigger callback
                    if self.on_new_email:
                        self.on_new_email({
                            "account_id": account.id,
                            "email": account.email,
                            "new_count": new_count,
                        })
                else:
                    # No new messages, just sync to keep database updated
                    self._log(f"{account.email}: No new messages (count: {current_count})")
                    self.service.sync_account(account.id, limit=10)
                    last_count = current_count

            except Exception as e:
                self._log(f"{account.email}: Poll error: {e}")

            # Wait for next poll
            stop_event.wait(timeout=self.poll_interval)


def main():
    """CLI entry point for daemon management."""
    import argparse

    parser = argparse.ArgumentParser(description="Email Bridge Daemon")
    parser.add_argument(
        "action",
        choices=["start", "stop", "status"],
        help="Action to perform",
    )
    parser.add_argument(
        "-d", "--daemon",
        action="store_true",
        help="Run in background (daemon mode)",
    )
    parser.add_argument(
        "-i", "--interval",
        type=int,
        default=300,
        help="Polling interval in seconds (default: 300)",
    )

    args = parser.parse_args()

    daemon = EmailDaemon(poll_interval=args.interval)

    if args.action == "start":
        daemon.start(background=args.daemon)
    elif args.action == "stop":
        daemon.stop()
    elif args.action == "status":
        status = daemon.status()
        print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()