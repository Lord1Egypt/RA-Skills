#!/usr/bin/env python3
"""
GeeLark Cloud Phone - Doctor Diagnostic Tool

Checks all dependencies and services before running cloud phone operations.
Fast failure detection to avoid long timeouts during boot_and_connect().

Usage:
    python scripts/doctor.py
    python scripts/doctor.py --phone-id <phone_id>  # Include phone-specific checks
"""

import sys
import os
import json
import subprocess
import time
from typing import Dict, List, Tuple, Optional

# Add project root to path
_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_script_dir)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from scripts.utils import get_token, get_base_url, generate_traceid


# ============================================
# Diagnostic Result Types
# ============================================
class DiagStatus:
    OK = "✅ OK"
    WARN = "⚠️  WARNING"
    FAIL = "❌ FAILED"
    SKIP = "⏭️  SKIPPED"


class DiagResult:
    def __init__(self, name: str, status: str, message: str, error_code: str = None):
        self.name = name
        self.status = status
        self.message = message
        self.error_code = error_code

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "status": self.status,
            "message": self.message,
            "error_code": self.error_code
        }


# ============================================
# Diagnostic Checks
# ============================================
def check_python_dependencies() -> List[DiagResult]:
    """Check if required Python packages are installed"""
    results = []
    
    # Check requests
    try:
        import requests
        results.append(DiagResult("requests", DiagStatus.OK, f"requests {requests.__version__} installed"))
    except ImportError:
        results.append(DiagResult(
            "requests",
            DiagStatus.FAIL,
            "requests not installed. Run: pip install requests",
            "ENV_DEPENDENCY_MISSING"
        ))
    
    # Check uiautomator2
    try:
        import uiautomator2
        results.append(DiagResult("uiautomator2", DiagStatus.OK, f"uiautomator2 installed"))
    except ImportError:
        results.append(DiagResult(
            "uiautomator2",
            DiagStatus.FAIL,
            "uiautomator2 not installed. Run: pip install uiautomator2",
            "ENV_DEPENDENCY_MISSING"
        ))
    
    return results


def check_adb() -> List[DiagResult]:
    """Check if ADB is available and working"""
    results = []
    
    # Check adb in PATH
    try:
        result = subprocess.run(
            ["adb", "version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            version_line = result.stdout.strip().split('\n')[0]
            results.append(DiagResult("adb", DiagStatus.OK, version_line))
        else:
            results.append(DiagResult(
                "adb",
                DiagStatus.FAIL,
                f"adb version check failed: {result.stderr.strip()}",
                "ENV_DEPENDENCY_MISSING"
            ))
    except FileNotFoundError:
        results.append(DiagResult(
            "adb",
            DiagStatus.FAIL,
            "adb not found in PATH. Install: brew install android-platform-tools (macOS) or apt install adb (Ubuntu)",
            "ENV_DEPENDENCY_MISSING"
        ))
    except subprocess.TimeoutExpired:
        results.append(DiagResult(
            "adb",
            DiagStatus.FAIL,
            "adb version check timed out",
            "ENV_DEPENDENCY_MISSING"
        ))
    
    return results


def check_network(base_url: str) -> List[DiagResult]:
    """Check network connectivity to GeeLark API"""
    results = []
    
    try:
        import requests
        # Try DNS resolution and connection
        start_time = time.time()
        response = requests.get(base_url, timeout=10)
        elapsed = time.time() - start_time
        
        # Even if it returns 404, DNS and connection worked
        results.append(DiagResult(
            "network_dns",
            DiagStatus.OK,
            f"DNS resolution OK ({base_url}, {elapsed:.2f}s)"
        ))
    except requests.exceptions.Timeout:
        results.append(DiagResult(
            "network_dns",
            DiagStatus.FAIL,
            f"Timeout connecting to {base_url}. Check DNS and firewall.",
            "NETWORK_DNS_FAILED"
        ))
    except requests.exceptions.ConnectionError as e:
        results.append(DiagResult(
            "network_dns",
            DiagStatus.FAIL,
            f"Cannot connect to {base_url}: {e}",
            "NETWORK_DNS_FAILED"
        ))
    except Exception as e:
        results.append(DiagResult(
            "network_dns",
            DiagStatus.FAIL,
            f"Network error: {e}",
            "NETWORK_DNS_FAILED"
        ))
    
    return results


def check_geelark_api(base_url: str, token: str) -> List[DiagResult]:
    """Check GeeLark API authentication and wallet"""
    results = []
    
    try:
        import requests
        
        headers = {
            "Content-Type": "application/json",
            "traceId": generate_traceid(),
            "Authorization": f"Bearer {token}"
        }
        
        # Test wallet endpoint
        start_time = time.time()
        response = requests.post(
            f"{base_url}/open/v1/pay/wallet",
            headers=headers,
            json={},
            timeout=15
        )
        elapsed = time.time() - start_time
        data = response.json()
        
        if data.get('code') == 0:
            balance = data['data']['balance']
            gift_money = data['data'].get('giftMoney', 0)
            results.append(DiagResult(
                "geelark_wallet",
                DiagStatus.OK,
                f"API auth OK. Balance: ${balance:.2f}, Gift: ${gift_money:.2f} ({elapsed:.2f}s)"
            ))
        else:
            results.append(DiagResult(
                "geelark_wallet",
                DiagStatus.FAIL,
                f"API auth failed: {data.get('msg', 'Unknown error')}",
                "GEELARK_API_FAILED"
            ))
    
    except requests.exceptions.Timeout:
        results.append(DiagResult(
            "geelark_wallet",
            DiagStatus.FAIL,
            "API request timed out (15s)",
            "GEELARK_API_FAILED"
        ))
    except Exception as e:
        results.append(DiagResult(
            "geelark_wallet",
            DiagStatus.FAIL,
            f"API error: {e}",
            "GEELARK_API_FAILED"
        ))
    
    return results


def check_adb_connect() -> List[DiagResult]:
    """Check if ADB can connect to devices"""
    results = []
    
    try:
        result = subprocess.run(
            ["adb", "devices"],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            # First line is "List of devices attached"
            device_lines = [l for l in lines[1:] if l.strip() and 'device' in l]
            
            if device_lines:
                devices = [l.split()[0] for l in device_lines]
                results.append(DiagResult(
                    "adb_devices",
                    DiagStatus.OK,
                    f"Found {len(devices)} device(s): {', '.join(devices)}"
                ))
            else:
                results.append(DiagResult(
                    "adb_devices",
                    DiagStatus.WARN,
                    "ADB is working but no devices connected. Connect cloud phone first.",
                    "ADB_CONNECT_FAILED"
                ))
        else:
            results.append(DiagResult(
                "adb_devices",
                DiagStatus.FAIL,
                f"adb devices failed: {result.stderr.strip()}",
                "ADB_CONNECT_FAILED"
            ))
    
    except FileNotFoundError:
        results.append(DiagResult(
            "adb_devices",
            DiagStatus.SKIP,
            "ADB not installed (see previous check)",
            "ENV_DEPENDENCY_MISSING"
        ))
    except subprocess.TimeoutExpired:
        results.append(DiagResult(
            "adb_devices",
            DiagStatus.FAIL,
            "adb devices timed out (15s)",
            "ADB_CONNECT_FAILED"
        ))
    
    return results


def check_phone_status(base_url: str, token: str, phone_id: str) -> List[DiagResult]:
    """Check specific phone status"""
    results = []
    
    try:
        import requests
        
        headers = {
            "Content-Type": "application/json",
            "traceId": generate_traceid(),
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.post(
            f"{base_url}/open/v1/phone/status",
            headers=headers,
            json={"ids": [phone_id]},
            timeout=15
        )
        data = response.json()
        
        if data.get('code') == 0:
            details = data.get('data', {}).get('successDetails', [])
            if details:
                status = details[0]['status']
                status_text = {0: "running", 1: "stopped", 2: "stopped"}.get(status, f"unknown({status})")
                results.append(DiagResult(
                    "phone_status",
                    DiagStatus.OK,
                    f"Phone {phone_id} is {status_text}"
                ))
            else:
                results.append(DiagResult(
                    "phone_status",
                    DiagStatus.FAIL,
                    f"No status details for phone {phone_id}",
                    "GEELARK_API_FAILED"
                ))
        else:
            results.append(DiagResult(
                "phone_status",
                DiagStatus.FAIL,
                f"Status check failed: {data.get('msg', 'Unknown error')}",
                "GEELARK_API_FAILED"
            ))
    
    except Exception as e:
        results.append(DiagResult(
            "phone_status",
            DiagStatus.FAIL,
            f"Phone status error: {e}",
            "GEELARK_API_FAILED"
        ))
    
    return results


def check_uiautomator2(serial: Optional[str] = None) -> List[DiagResult]:
    """Check uiautomator2 connectivity"""
    results = []
    
    try:
        import uiautomator2 as u2
        
        if serial:
            d = u2.connect(serial)
        else:
            # Try to find connected device
            d = u2.connect()
        
        # Test d.info
        start_time = time.time()
        info = d.info
        elapsed = time.time() - start_time
        
        if info:
            results.append(DiagResult(
                "uiautomator2_connect",
                DiagStatus.OK,
                f"Connected to device ({elapsed:.2f}s). Current: {info.get('currentPackageName', 'N/A')}"
            ))
        else:
            results.append(DiagResult(
                "uiautomator2_connect",
                DiagStatus.WARN,
                "Connected but d.info returned empty",
                "UIAUTOMATOR_TIMEOUT"
            ))
        
        # Test dump_hierarchy with timeout
        start_time = time.time()
        try:
            hierarchy = d.dump_hierarchy()
            elapsed = time.time() - start_time
            
            if hierarchy and len(hierarchy) > 100:
                results.append(DiagResult(
                    "uiautomator2_dump",
                    DiagStatus.OK,
                    f"UI hierarchy dumped successfully ({elapsed:.2f}s, {len(hierarchy)} bytes)"
                ))
            else:
                results.append(DiagResult(
                    "uiautomator2_dump",
                    DiagStatus.WARN,
                    f"UI hierarchy seems too short ({elapsed:.2f}s, {len(hierarchy) if hierarchy else 0} bytes)",
                    "UIAUTOMATOR_TIMEOUT"
                ))
        except Exception as e:
            elapsed = time.time() - start_time
            results.append(DiagResult(
                "uiautomator2_dump",
                DiagStatus.FAIL,
                f"dump_hierarchy() failed after {elapsed:.2f}s: {e}",
                "UIAUTOMATOR_TIMEOUT"
            ))
    
    except ImportError:
        results.append(DiagResult(
            "uiautomator2",
            DiagStatus.SKIP,
            "uiautomator2 not installed (see previous check)",
            "ENV_DEPENDENCY_MISSING"
        ))
    except Exception as e:
        results.append(DiagResult(
            "uiautomator2",
            DiagStatus.FAIL,
            f"uiautomator2 connection failed: {e}",
            "UIAUTOMATOR_TIMEOUT"
        ))
    
    return results


# ============================================
# Main Diagnostic Runner
# ============================================
def run_doctor(phone_id: Optional[str] = None, serial: Optional[str] = None, verbose: bool = False) -> Dict:
    """
    Run all diagnostic checks and return results.
    
    Args:
        phone_id: Optional phone ID for phone-specific checks
        serial: Optional ADB serial for uiautomator2 checks
        verbose: Show detailed output
    
    Returns:
        dict with 'results' list and 'summary' dict
    """
    all_results = []
    
    print("=" * 70)
    print("🔍 GeeLark Cloud Phone - Doctor Diagnostic")
    print("=" * 70)
    
    # Phase 1: Environment
    print("\n📦 Phase 1: Environment Dependencies")
    print("-" * 70)
    env_results = check_python_dependencies()
    all_results.extend(env_results)
    for r in env_results:
        print(f"  {r.status} {r.name}: {r.message}")
    
    # Phase 2: ADB
    print("\n📱 Phase 2: ADB (Android Debug Bridge)")
    print("-" * 70)
    adb_results = check_adb()
    all_results.extend(adb_results)
    for r in adb_results:
        print(f"  {r.status} {r.name}: {r.message}")
    
    # Phase 3: Network
    print("\n🌐 Phase 3: Network & GeeLark API")
    print("-" * 70)
    
    try:
        base_url = get_base_url()
        token = get_token()
        
        network_results = check_network(base_url)
        all_results.extend(network_results)
        for r in network_results:
            print(f"  {r.status} {r.name}: {r.message}")
        
        api_results = check_geelark_api(base_url, token)
        all_results.extend(api_results)
        for r in api_results:
            print(f"  {r.status} {r.name}: {r.message}")
    
    except Exception as e:
        fail_result = DiagResult("config", DiagStatus.FAIL, f"Failed to load config: {e}", "ENV_DEPENDENCY_MISSING")
        all_results.append(fail_result)
        print(f"  {fail_result.status} {fail_result.name}: {fail_result.message}")
    
    # Phase 4: ADB Devices
    print("\n🔌 Phase 4: ADB Device Connection")
    print("-" * 70)
    adb_conn_results = check_adb_connect()
    all_results.extend(adb_conn_results)
    for r in adb_conn_results:
        print(f"  {r.status} {r.name}: {r.message}")
    
    # Phase 5: Phone-specific checks (optional)
    if phone_id:
        print(f"\n📞 Phase 5: Phone Status ({phone_id})")
        print("-" * 70)
        try:
            phone_results = check_phone_status(base_url, token, phone_id)
            all_results.extend(phone_results)
            for r in phone_results:
                print(f"  {r.status} {r.name}: {r.message}")
        except:
            fail = DiagResult("phone_status", DiagStatus.SKIP, "Skipping (config not loaded)")
            all_results.append(fail)
            print(f"  {fail.status} {fail.name}: {fail.message}")
    
    # Phase 6: uiautomator2 (optional, requires connected device)
    if serial:
        print(f"\n🤖 Phase 6: uiautomator2 ({serial})")
        print("-" * 70)
        ui_results = check_uiautomator2(serial)
        all_results.extend(ui_results)
        for r in ui_results:
            print(f"  {r.status} {r.name}: {r.message}")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Diagnostic Summary")
    print("=" * 70)
    
    ok_count = sum(1 for r in all_results if r.status == DiagStatus.OK)
    warn_count = sum(1 for r in all_results if r.status == DiagStatus.WARN)
    fail_count = sum(1 for r in all_results if r.status == DiagStatus.FAIL)
    skip_count = sum(1 for r in all_results if r.status == DiagStatus.SKIP)
    
    print(f"  ✅ OK:     {ok_count}")
    print(f"  ⚠️  WARNING: {warn_count}")
    print(f"  ❌ FAILED: {fail_count}")
    print(f"  ⏭️  SKIPPED: {skip_count}")
    
    # Error codes for failed checks
    failed_checks = [r for r in all_results if r.status == DiagStatus.FAIL and r.error_code]
    if failed_checks:
        print("\n🔴 Error Codes:")
        for r in failed_checks:
            print(f"  {r.error_code}: {r.name} - {r.message}")
    
    # Recommendations
    if fail_count > 0:
        print("\n💡 Recommendations:")
        if any(r.error_code == "ENV_DEPENDENCY_MISSING" for r in all_results):
            print("  1. Install missing dependencies:")
            print("     python3 -m venv .venv")
            print("     source .venv/bin/activate")
            print("     pip install requests uiautomator2")
            print("     brew install android-platform-tools  # macOS")
        
        if any(r.error_code == "NETWORK_DNS_FAILED" for r in all_results):
            print("  2. Check network connectivity and DNS settings")
            print("     Verify baseUrl in assets/config.json")
        
        if any(r.error_code == "GEELARK_API_FAILED" for r in all_results):
            print("  3. Verify API token in assets/config.json")
            print("     Run: python scripts/init_config.py")
        
        if any(r.error_code == "ADB_CONNECT_FAILED" for r in all_results):
            print("  4. Ensure cloud phone is started and ADB is enabled")
            print("     Use boot_and_connect() to start phone first")
        
        if any(r.error_code == "UIAUTOMATOR_TIMEOUT" for r in all_results):
            print("  5. uiautomator2 timeout - check device responsiveness")
            print("     Run: python scripts/ui_smoke_test.py <serial>")
    
    print("\n" + "=" * 70)
    
    # Return structured results
    return {
        "results": [r.to_dict() for r in all_results],
        "summary": {
            "ok": ok_count,
            "warning": warn_count,
            "failed": fail_count,
            "skipped": skip_count,
            "total": len(all_results)
        }
    }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="GeeLark Cloud Phone Doctor")
    parser.add_argument("--phone-id", help="Phone ID for phone-specific checks")
    parser.add_argument("--serial", help="ADB serial for uiautomator2 checks")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    
    args = parser.parse_args()
    
    result = run_doctor(
        phone_id=args.phone_id,
        serial=args.serial,
        verbose=args.verbose
    )
    
    if args.json:
        print("\n" + json.dumps(result, indent=2))
    
    # Exit with error code if any checks failed
    sys.exit(1 if result['summary']['failed'] > 0 else 0)
