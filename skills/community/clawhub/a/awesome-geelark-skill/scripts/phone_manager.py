#!/usr/bin/env python3
"""
GeeLark Cloud Phone Manager - Auto-Close Idle Devices

Automatically close cloud phones that have been idle for a specified timeout.

Usage:
    from scripts.phone_manager import PhoneManager

    # Method 1: Context manager (recommended)
    with PhoneManager(timeout_minutes=5) as manager:
        d = manager.connect_device(phone_id, ip, port, pwd, name="Android15")
        d(text="Dark theme").click()
        manager.record_activity(phone_id)

    # Method 2: Manual control
    manager = PhoneManager(timeout_minutes=5)
    manager.start_monitor()
    # ... operations ...
    manager.stop_all()
"""

import time
import threading
import subprocess
from datetime import datetime, timedelta
from typing import Dict, Optional

import uiautomator2 as u2

from scripts.geelark_client import GeeLarkClient
from scripts.cloudphone_logger import CloudPhoneLog


class PhoneManager:
    """
    Manages cloud phone connections and auto-closes idle devices.
    All operations use phone_id for precise matching.
    """

    def __init__(self, timeout_minutes: int = 5, token: str = None, base_url: str = None, task_name: str = "phone_manager"):
        """
        Initialize PhoneManager.

        Args:
            timeout_minutes: Timeout in minutes before auto-closing
            token: GeeLark API token (optional, reads from config if not provided)
            base_url: API base URL (optional)
            task_name: Name for logging context
        """
        self.timeout = timedelta(minutes=timeout_minutes)
        self.last_activity: Dict[str, datetime] = {}  # key: phone_id
        self.phone_status: Dict[str, str] = {}        # key: phone_id
        self.devices: Dict[str, u2.Device] = {}       # key: phone_id
        self._display_names: Dict[str, str] = {}      # key: phone_id, value: display name
        self.client = GeeLarkClient(token=token, base_url=base_url, task_name=task_name, phone_id="batch")
        self.monitor_thread: Optional[threading.Thread] = None
        self.whitelist: list = []
        self._monitoring = False
        self.task_name = task_name

    def connect_device(self, phone_id: str, ip: str, port: str, pwd: str, name: str = None) -> u2.Device:
        """
        Connect to cloud phone and record activity.

        Args:
            phone_id: Cloud phone ID (required, used for all operations)
            ip: ADB IP address
            port: ADB port
            pwd: ADB password
            name: Display name (optional, for logging only)

        Returns:
            uiautomator2.Device instance
        """
        display_name = name or phone_id
        
        # Connect to device
        d = u2.connect(f"{ip}:{port}")

        # glogin authentication
        try:
            r = subprocess.run(
                ['adb', '-s', f"{ip}:{port}", 'shell', 'glogin', pwd],
                capture_output=True,
                text=True,
                timeout=30
            )
            if r.returncode != 0:
                print(f"❌ glogin failed: {r.stderr}")
                self.client._log.error("GLLOGIN_FAILED", r.stderr) if self.client._log else None
        except subprocess.TimeoutExpired:
            print(f"❌ glogin timeout for {ip}:{port}")
        except Exception as e:
            print(f"❌ glogin error: {e}")

        self.devices[phone_id] = d
        self._display_names[phone_id] = display_name
        self.record_activity(phone_id)

        print(f"✅ Connected to {display_name} ({ip}:{port})")
        return d

    def record_activity(self, phone_id: str):
        """
        Record cloud phone activity time.

        Args:
            phone_id: Cloud phone ID
        """
        self.last_activity[phone_id] = datetime.now()
        self.phone_status[phone_id] = "active"

    def stop_phone(self, phone_id: str) -> bool:
        """
        Stop cloud phone.

        Args:
            phone_id: Cloud phone ID

        Returns:
            True if stopped successfully, False otherwise
        """
        display_name = self._display_names.get(phone_id, phone_id)

        # Call GeeLark API to stop
        try:
            response = self.client.phone_stop([phone_id])
            if response.get('code') == 0:
                print(f"🛑 Stopped {display_name} ({phone_id})")
                self.client._log.info(f"Stopped {display_name}") if self.client._log else None
            else:
                print(f"⚠️  Failed to stop {display_name}: {response.get('msg', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"❌ Error stopping {display_name}: {e}")
            return False

        self.phone_status[phone_id] = "stopped"
        if phone_id in self.devices:
            del self.devices[phone_id]
        if phone_id in self.last_activity:
            del self.last_activity[phone_id]
        if phone_id in self._display_names:
            del self._display_names[phone_id]
        return True

    def check_idle_phones(self):
        """
        Check and close idle cloud phones.
        """
        now = datetime.now()

        for phone_id, last_time in list(self.last_activity.items()):
            # Skip whitelisted devices
            if phone_id in self.whitelist:
                continue

            idle_time = now - last_time
            if idle_time > self.timeout:
                idle_minutes = int(idle_time.total_seconds() / 60)
                display_name = self._display_names.get(phone_id, phone_id)
                print(f"⚠️  {display_name}: Idle for {idle_minutes} minutes, stopping...")
                self.stop_phone(phone_id)

    def start_monitor(self, check_interval: int = 60):
        """
        Start background monitoring thread.

        Args:
            check_interval: Check interval in seconds (default: 60)
        """
        if self._monitoring:
            print("⚠️  Monitor already running")
            return

        self._monitoring = True

        def monitor_loop():
            while self._monitoring:
                try:
                    self.check_idle_phones()
                except Exception as e:
                    print(f"❌ Monitor error: {e}")
                time.sleep(check_interval)

        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
        print(f"🔍 Background monitoring started (timeout: {self.timeout.seconds // 60} minutes, check every {check_interval}s)")

    def stop_monitor(self):
        """Stop background monitoring."""
        self._monitoring = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)
        print("🔍 Background monitoring stopped")

    def add_to_whitelist(self, phone_id: str):
        """
        Add device to whitelist (not auto-closed).

        Args:
            phone_id: Cloud phone ID
        """
        if phone_id not in self.whitelist:
            self.whitelist.append(phone_id)
            display_name = self._display_names.get(phone_id, phone_id)
            print(f"📋 {display_name} ({phone_id}): Added to whitelist")

    def remove_from_whitelist(self, phone_id: str):
        """
        Remove device from whitelist.

        Args:
            phone_id: Cloud phone ID
        """
        if phone_id in self.whitelist:
            self.whitelist.remove(phone_id)
            display_name = self._display_names.get(phone_id, phone_id)
            print(f"📋 {display_name} ({phone_id}): Removed from whitelist")

    def stop_all(self):
        """
        Stop all active cloud phones.
        """
        if not self.devices:
            return

        print(f"\n🛑 Stopping all active cloud phones ({len(self.devices)} devices)...")
        for phone_id in list(self.devices.keys()):
            self.stop_phone(phone_id)

        # Save logs
        self.client.save_log()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - stop all phones."""
        self.stop_monitor()
        self.stop_all()
        return False


# Example usage
if __name__ == "__main__":
    print("PhoneManager Example Usage\n")

    # Create manager with 5-minute timeout
    manager = PhoneManager(timeout_minutes=5)

    # Start background monitoring
    manager.start_monitor()

    # Connect to device (this is just example, you'd use real IP/port/pwd)
    # d = manager.connect_device("phone_id_123", "1.2.3.4", "5555", "password", name="Android15")

    # Record activity periodically to prevent auto-close
    def long_running_task():
        for i in range(10):
            print(f"Task step {i+1}/10")
            manager.record_activity("phone_id_123")
            time.sleep(30)  # Record activity every 30 seconds

    # Run long task
    # long_running_task()

    # Phone will auto-close after 5 minutes of no activity

    print("✅ Example completed")
