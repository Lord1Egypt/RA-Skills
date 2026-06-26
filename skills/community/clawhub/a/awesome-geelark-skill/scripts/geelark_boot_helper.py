#!/usr/bin/env python3
"""
GeeLark Cloud Phone Boot Helper - Best Practices for Boot and ADB Connection

Improvements:
1. Polling mechanism instead of fixed sleep times
2. Integrated CloudPhoneLog for audit trails
3. Robust error handling for network requests
4. Configurable timeouts and intervals
"""

import requests
import time
import os
import sys
import json
from datetime import datetime

# Add project root to path so absolute imports work when running this script directly
_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_script_dir)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from scripts.utils import generate_traceid, get_base_url, get_token
from scripts.cloudphone_logger import CloudPhoneLog


# ============================================
# Structured Output Helper
# ============================================
def _emit_stage(stage: str, status: str, data: dict = None, flush: bool = True):
    """
    Emit structured JSON stage output for better visibility during long operations.
    
    Args:
        stage: Stage identifier (e.g., "phone_start_poll", "adb_ready")
        status: Status ("ok", "failed", "pending", "info")
        data: Additional data dict
        flush: Force stdout flush
    """
    output = {
        "stage": stage,
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "elapsed": time.time()  # Can be used to calculate duration
    }
    
    if data:
        output.update(data)
    
    # Print as JSON line for easy parsing
    print(json.dumps(output), flush=flush)


# ============================================
# Configuration Constants
# ============================================
PHONE_STARTUP_TIMEOUT = 180  # Max seconds to wait for phone startup
ADB_READY_TIMEOUT = 60       # Max seconds to wait for ADB readiness
POLL_INTERVAL = 10           # Seconds between status checks


def list_cloud_phones(token: str = None, base_url: str = None):
    """
    List all available cloud phones.

    Args:
        token: GeeLark API Token (optional, loads from config if not provided)
        base_url: API base URL (optional, loads from config if not provided)

    Returns:
        List of cloud phone dictionaries or None
    """
    if token is None:
        token = get_token()
    if base_url is None:
        base_url = get_base_url()

    headers = {
        "Content-Type": "application/json",
        "traceId": generate_traceid(),
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(
            f"{base_url}/open/v1/phone/list",
            headers=headers,
            json={"page": 1, "pageSize": 100},
            timeout=20
        )
        response.raise_for_status()
        data = response.json()
        
        if data.get('code') == 0:
            return data.get('data', {}).get('items', [])
        
        print(f"❌ Failed to list cloud phones: {data.get('msg')}")
        return None
    except requests.RequestException as e:
        print(f"❌ Network error listing phones: {e}")
        return None


def _wait_for_phone_running(client_log: CloudPhoneLog, phone_id: str, token: str, base_url: str, timeout: int = PHONE_STARTUP_TIMEOUT):
    """
    Poll phone status until it is running.
    """
    headers = {
        "Content-Type": "application/json",
        "traceId": generate_traceid(),
        "Authorization": f"Bearer {token}"
    }

    _emit_stage("phone_start_poll", "pending", {"phone_id": phone_id, "timeout": timeout})
    print(f"  ⏳ Waiting for phone to be ready (max {timeout}s)...", flush=True)
    client_log.info(f"Polling phone status (timeout={timeout}s)")

    elapsed = 0
    while elapsed < timeout:
        try:
            status_response = requests.post(
                f"{base_url}/open/v1/phone/status",
                headers=headers,
                json={"ids": [phone_id]},
                timeout=10
            )
            status_data = status_response.json()

            if status_data.get('code') == 0:
                details = status_data.get('data', {}).get('successDetails', [])
                if not details:
                    fail_details = status_data.get('data', {}).get('failDetails', [])
                    if fail_details:
                        for fd in fail_details:
                            code = fd.get('code', 'unknown')
                            msg = fd.get('msg', '')
                            print(f"  ❌ Status check failed: {code} - {msg}", flush=True)
                            client_log.error(f"POLL_STATUS_{code}", msg)
                    else:
                        print(f"  ⚠️ Status check returned no details, retrying...", flush=True)
                    time.sleep(POLL_INTERVAL)
                    elapsed += POLL_INTERVAL
                    continue

                phone_status = details[0]['status']
                if phone_status == 0:  # Running
                    _emit_stage("phone_start_poll", "ok", {"phone_id": phone_id, "elapsed": elapsed, "status": "running"})
                    print(f"  ✅ Phone is running (took {elapsed}s)", flush=True)
                    client_log.info(f"Phone running after {elapsed}s")
                    return True
                else:
                    status_text = {1: "stopped", 2: "stopped"}.get(phone_status, "unknown")
                    _emit_stage("phone_start_poll", "pending", {"phone_id": phone_id, "elapsed": elapsed, "status": status_text})
                    print(f"  🔄 Status: {status_text} ({elapsed}s)", flush=True)
            else:
                print(f"  ⚠️ Status check failed: {status_data.get('msg')}", flush=True)

        except requests.RequestException as e:
            print(f"  ⚠️ Network error during polling: {e}", flush=True)

        time.sleep(POLL_INTERVAL)
        elapsed += POLL_INTERVAL

    _emit_stage("phone_start_poll", "failed", {"phone_id": phone_id, "elapsed": timeout, "status": "timeout"})
    print(f"  ❌ Timeout waiting for phone to start ({timeout}s)", flush=True)
    client_log.error("TIMEOUT", f"Phone did not start within {timeout}s")
    return False


def _get_adb_info(phone_id: str, token: str, base_url: str):
    """
    Helper to get ADB info safely.
    """
    headers = {
        "Content-Type": "application/json",
        "traceId": generate_traceid(),
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.post(
            f"{base_url}/open/v1/adb/getData",
            headers=headers,
            json={"ids": [phone_id]},
            timeout=10
        )
        data = response.json()
        if data.get('code') == 0:
            items = data.get('data', {}).get('items', [])
            if items:
                return items[0]
        return None
    except requests.RequestException:
        return None


def boot_and_connect(phone_id: str, token: str = None, base_url: str = None, task_name: str = "boot_helper"):
    """
    GeeLark Cloud Phone Boot and ADB Connection - Best Practices Flow

    Args:
        phone_id: Cloud phone ID
        token: GeeLark API Token (optional)
        base_url: API base URL (optional)
        task_name: Name for logging context

    Returns:
        dict: {'ip': str, 'port': str, 'pwd': str} or None
    """
    if token is None:
        token = get_token()
    if base_url is None:
        base_url = get_base_url()

    # Initialize Logger
    client_log = CloudPhoneLog(task_name, phone_id)

    headers = {
        "Content-Type": "application/json",
        "traceId": generate_traceid(),
        "Authorization": f"Bearer {token}"
    }

    try:
        # Step 0: Check balance
        _emit_stage("balance_check", "pending")
        client_log.info("Checking balance")
        balance_response = requests.post(f"{base_url}/open/v1/pay/wallet", headers=headers, timeout=10)
        balance_data = balance_response.json()

        if balance_data.get('code') == 0:
            balance = balance_data['data']['balance']
            gift_money = balance_data['data'].get('giftMoney', 0)
            available_time = balance_data['data'].get('availableTimeAddOn') or 0

            _emit_stage("balance_check", "ok", {"balance": balance, "gift_money": gift_money, "available_time": available_time})
            print(f"  💰 Balance: ${balance:.2f}, Gift: ${gift_money:.2f}, Time: {available_time}h", flush=True)

            if balance <= 0 and gift_money <= 0 and available_time <= 0:
                _emit_stage("balance_check", "failed", {"reason": "insufficient_balance"})
                print(f"  ❌ Insufficient balance", flush=True)
                client_log.error("INSUFFICIENT_BALANCE", "Cannot start phone")
                client_log.save()
                return None
        else:
            _emit_stage("balance_check", "failed", {"error": balance_data.get('msg')})
            print(f"  ❌ Balance check failed: {balance_data.get('msg')}", flush=True)
            client_log.save()
            return None

        # Step 1: Check status
        _emit_stage("phone_status_check", "pending", {"phone_id": phone_id})
        client_log.info("Checking phone status")
        status_response = requests.post(
            f"{base_url}/open/v1/phone/status",
            headers=headers,
            json={"ids": [phone_id]},
            timeout=10
        )
        status_data = status_response.json()

        if status_data.get('code') != 0:
            _emit_stage("phone_status_check", "failed", {"error": status_data.get('msg')})
            print(f"  ❌ Status check failed: {status_data.get('msg')}", flush=True)
            client_log.save()
            return None

        details = status_data.get('data', {}).get('successDetails', [])
        fail_details = status_data.get('data', {}).get('failDetails', [])

        if not details:
            _emit_stage("phone_status_check", "failed", {"reason": "no_details"})
            if fail_details:
                for fd in fail_details:
                    code = fd.get('code', 'unknown')
                    msg = fd.get('msg', '')
                    print(f"  ❌ Status check failed: {code} - {msg}", flush=True)
                    client_log.error(f"STATUS_{code}", msg)
            else:
                print(f"  ❌ Status check returned no details", flush=True)
                client_log.error("EMPTY_STATUS", "No successDetails or failDetails")
            client_log.save()
            return None

        phone_status = details[0]['status']
        status_text = {0: "running", 1: "stopped", 2: "stopped"}.get(phone_status, f"unknown({phone_status})")
        _emit_stage("phone_status_check", "ok", {"phone_id": phone_id, "status": status_text})
        print(f"  📱 Status: {status_text}", flush=True)

        # Step 2: Start if stopped
        if phone_status != 0:
            _emit_stage("phone_start", "pending", {"phone_id": phone_id})
            client_log.info("Starting phone")
            print(f"\n  🚀 Starting cloud phone...", flush=True)
            
            start_response = requests.post(
                f"{base_url}/open/v1/phone/start",
                headers=headers,
                json={"ids": [phone_id], "energySavingMode": 1},
                timeout=10
            )
            start_data = start_response.json()

            fail_amount = start_data.get('data', {}).get('failAmount', 0)
            if fail_amount > 0:
                print(f"  ❌ Start failed:")
                for fail in start_data['data']['failDetails']:
                    print(f"     {fail.get('code')}: {fail.get('msg', '')}")
                client_log.error("START_FAILED", str(start_data['data']['failDetails']))
                client_log.save()
                return None

            # Poll for status instead of fixed sleep
            if not _wait_for_phone_running(client_log, phone_id, token, base_url):
                client_log.save()
                return None
        else:
            print(f"  ℹ️ Phone already running")

        # Step 3: Check & Enable ADB
        _emit_stage("adb_check", "pending", {"phone_id": phone_id})
        client_log.info("Checking ADB status")
        print(f"\n  🔌 Checking ADB status...", flush=True)

        adb_item = _get_adb_info(phone_id, token, base_url)

        if not adb_item:
            _emit_stage("adb_check", "failed", {"reason": "no_adb_info"})
            print(f"  ❌ Failed to get ADB info", flush=True)
            client_log.save()
            return None

        if adb_item.get('code') != 0:
            _emit_stage("adb_enable", "pending", {"phone_id": phone_id})
            print(f"  ⚠️ ADB not enabled (code={adb_item.get('code')}), enabling...", flush=True)
            client_log.info("Enabling ADB")
            
            enable_response = requests.post(
                f"{base_url}/open/v1/adb/setStatus",
                headers=headers,
                json={"ids": [phone_id], "open": True},
                timeout=10
            )
            enable_data = enable_response.json()
            
            if enable_data.get('code') != 0:
                print(f"  ❌ ADB enable failed: {enable_data.get('msg')}")
                client_log.save()
                return None

            # Poll for ADB readiness
            print(f"  ⏳ Waiting for ADB to be ready...")
            adb_ready = False
            elapsed = 0
            while elapsed < ADB_READY_TIMEOUT:
                time.sleep(POLL_INTERVAL)
                elapsed += POLL_INTERVAL
                adb_item = _get_adb_info(phone_id, token, base_url)
                if adb_item and adb_item.get('code') == 0:
                    adb_ready = True
                    print(f"  ✅ ADB ready (took {elapsed}s)")
                    break
            
            if not adb_ready:
                _emit_stage("adb_ready", "failed", {"reason": "timeout"})
                print(f"  ❌ Timeout waiting for ADB", flush=True)
                client_log.error("TIMEOUT", "ADB did not become ready")
                client_log.save()
                return None
        else:
            _emit_stage("adb_check", "ok", {"phone_id": phone_id, "adb_status": "already_enabled"})
            print(f"  ✅ ADB already enabled", flush=True)

        # Step 4: Return info
        if adb_item.get('code') == 0:
            result = {
                'ip': adb_item.get('ip'),
                'port': adb_item.get('port'),
                'pwd': adb_item.get('pwd')
            }
            _emit_stage("boot_complete", "ok", {"phone_id": phone_id, "adb": f"{result['ip']}:{result['port']}"})
            print(f"\n✅ Cloud phone is ready", flush=True)
            print(f"  ADB: {result['ip']}:{result['port']}", flush=True)

            client_log.info("Boot completed successfully")
            client_log.save()
            return result
        else:
            _emit_stage("adb_ready", "failed", {"reason": adb_item.get('msg')})
            print(f"  ❌ ADB not ready: {adb_item.get('msg')}", flush=True)
            client_log.save()
            return None

    except requests.RequestException as e:
        print(f"❌ Network error: {e}")
        client_log.error("NETWORK_ERROR", str(e))
        client_log.save()
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        client_log.error("UNEXPECTED_ERROR", str(e))
        client_log.save()
        return None


if __name__ == "__main__":
    import sys

    # Load config
    try:
        from scripts.utils import load_config
        config = load_config()
        token = config['auth']['token']
    except Exception as e:
        print(f"❌ Failed to load config: {e}")
        sys.exit(1)

    # If no phone_id provided, list available phones
    if len(sys.argv) < 2:
        print("ℹ️  No phone ID provided. Listing available cloud phones...\n")
        phones = list_cloud_phones(token)
        if phones:
            print(f"Found {len(phones)} phone(s):\n")
            for i, phone in enumerate(phones, 1):
                name = phone.get('serialName', 'N/A')
                pid = phone.get('id', 'N/A')
                status = 'Running' if phone.get('status') == 0 else 'Stopped'
                print(f"   {i}. {name} ({pid}) - Status: {status}")
            print(f"\n💡 Usage: python -m scripts.geelark_boot_helper <phone_id>")
        else:
            print("❌ No cloud phones found.")
        sys.exit(0)

    phone_id = sys.argv[1]
    print(f"🚀 Booting cloud phone: {phone_id}\n")

    result = boot_and_connect(phone_id, token)

    if result:
        print(f"\n✅ Boot successful")
    else:
        print(f"\n❌ Boot failed")
        sys.exit(1)
