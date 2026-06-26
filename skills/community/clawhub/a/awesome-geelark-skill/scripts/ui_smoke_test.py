#!/usr/bin/env python3
"""
GeeLark Cloud Phone - uiautomator2 Smoke Test

Tests uiautomator2 connectivity and responsiveness with individual timeouts.
Helps identify if the issue is with connection, agent initialization, or app startup.

Usage:
    python scripts/ui_smoke_test.py <serial>
    python scripts/ui_smoke_test.py 192.168.1.100:5555
"""

import sys
import os
import time
import json
import signal
from typing import Optional

# Add project root to path
_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_script_dir)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)


# ============================================
# Timeout Helper
# ============================================
class TimeoutError(Exception):
    pass


def _timeout_handler(signum, frame):
    raise TimeoutError("Operation timed out")


def run_with_timeout(func, timeout: int, *args, **kwargs):
    """Run function with signal-based timeout (Unix only)"""
    if sys.platform == "win32":
        # Windows doesn't support signal.alarm, run without timeout
        return func(*args, **kwargs)
    
    old_handler = signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(timeout)
    try:
        result = func(*args, **kwargs)
        signal.alarm(0)  # Cancel alarm
        return result
    finally:
        signal.signal(signal.SIGALRM, old_handler)


# ============================================
# Smoke Test Configuration
# ============================================
DEFAULT_TIMEOUT = 30  # seconds per step


# ============================================
# Smoke Test Functions
# ============================================
def step_connect(serial: str, timeout: int = DEFAULT_TIMEOUT) -> dict:
    """Test uiautomator2.connect()"""
    result = {
        "step": "connect",
        "status": "pending",
        "elapsed": 0,
        "error": None
    }

    try:
        import uiautomator2 as u2

        print(f"  ⏳ Connecting to {serial} (timeout={timeout}s)...", flush=True)
        start_time = time.time()

        def _do_connect():
            return u2.connect(serial)

        d = run_with_timeout(_do_connect, timeout)
        
        elapsed = time.time() - start_time
        result["status"] = "ok"
        result["elapsed"] = round(elapsed, 2)
        print(f"  ✅ Connected ({elapsed:.2f}s)", flush=True)
        
        return result, d
    
    except ImportError:
        result["status"] = "failed"
        result["error"] = "uiautomator2 not installed"
        print(f"  ❌ {result['error']}", flush=True)
        return result, None
    
    except Exception as e:
        elapsed = time.time() - start_time
        result["status"] = "failed"
        result["elapsed"] = round(elapsed, 2)
        result["error"] = str(e)
        print(f"  ❌ Connection failed after {elapsed:.2f}s: {e}", flush=True)
        return result, None


def step_get_info(d, timeout: int = DEFAULT_TIMEOUT) -> dict:
    """Test d.info (current activity and device info)"""
    result = {
        "step": "get_info",
        "status": "pending",
        "elapsed": 0,
        "error": None,
        "data": {}
    }
    
    try:
        print(f"  ⏳ Getting device info (timeout={timeout}s)...", flush=True)
        start_time = time.time()

        info = run_with_timeout(lambda: d.info, timeout)
        
        elapsed = time.time() - start_time
        
        if info:
            result["status"] = "ok"
            result["elapsed"] = round(elapsed, 2)
            result["data"] = {
                "current_package": info.get("currentPackageName", "N/A"),
                "display_height": info.get("displayHeight", "N/A"),
                "display_width": info.get("displayWidth", "N/A"),
                "platform": info.get("platform", "N/A")
            }
            print(f"  ✅ Device info retrieved ({elapsed:.2f}s)", flush=True)
            print(f"     Current package: {result['data']['current_package']}", flush=True)
        else:
            result["status"] = "warning"
            result["elapsed"] = round(elapsed, 2)
            result["error"] = "d.info returned empty/None"
            print(f"  ⚠️  d.info returned empty ({elapsed:.2f}s)", flush=True)
        
        return result
    
    except Exception as e:
        elapsed = time.time() - start_time
        result["status"] = "failed"
        result["elapsed"] = round(elapsed, 2)
        result["error"] = str(e)
        print(f"  ❌ Failed to get info after {elapsed:.2f}s: {e}", flush=True)
        return result


def step_dump_hierarchy(d, timeout: int = DEFAULT_TIMEOUT) -> dict:
    """Test d.dump_hierarchy()"""
    result = {
        "step": "dump_hierarchy",
        "status": "pending",
        "elapsed": 0,
        "error": None,
        "data": {}
    }
    
    try:
        print(f"  ⏳ Dumping UI hierarchy (timeout={timeout}s)...", flush=True)
        start_time = time.time()

        hierarchy = run_with_timeout(lambda: d.dump_hierarchy(), timeout)
        
        elapsed = time.time() - start_time
        
        if hierarchy and len(hierarchy) > 100:
            result["status"] = "ok"
            result["elapsed"] = round(elapsed, 2)
            result["data"] = {
                "size_bytes": len(hierarchy),
                "has_root": "<hierarchy" in hierarchy if isinstance(hierarchy, str) else False
            }
            print(f"  ✅ UI hierarchy dumped ({elapsed:.2f}s, {len(hierarchy)} bytes)", flush=True)
        else:
            result["status"] = "warning"
            result["elapsed"] = round(elapsed, 2)
            result["data"] = {
                "size_bytes": len(hierarchy) if hierarchy else 0
            }
            result["error"] = "Hierarchy seems too short or empty"
            print(f"  ⚠️  Hierarchy too short ({elapsed:.2f}s, {len(hierarchy) if hierarchy else 0} bytes)", flush=True)
        
        return result
    
    except Exception as e:
        elapsed = time.time() - start_time
        result["status"] = "failed"
        result["elapsed"] = round(elapsed, 2)
        result["error"] = str(e)
        print(f"  ❌ dump_hierarchy failed after {elapsed:.2f}s: {e}", flush=True)
        return result


def test_app_start(d, package: str, timeout: int = DEFAULT_TIMEOUT) -> dict:
    """Test d.app_start()"""
    result = {
        "step": "app_start",
        "status": "pending",
        "elapsed": 0,
        "error": None,
        "data": {"package": package}
    }
    
    try:
        print(f"  ⏳ Starting app {package} (timeout={timeout}s)...", flush=True)
        start_time = time.time()

        run_with_timeout(lambda: d.app_start(package), timeout)

        elapsed = time.time() - start_time
        result["status"] = "ok"
        result["elapsed"] = round(elapsed, 2)
        print(f"  ✅ App started ({elapsed:.2f}s)", flush=True)

        # Verify current package
        time.sleep(2)
        info = run_with_timeout(lambda: d.info, timeout)
        current = info.get("currentPackageName", "unknown") if info else "unknown"
        result["data"]["current_package"] = current
        result["data"]["expected_package"] = package
        result["data"]["match"] = (current == package)
        
        if current != package:
            print(f"  ⚠️  Expected {package}, got {current}", flush=True)
        
        return result
    
    except Exception as e:
        elapsed = time.time() - start_time
        result["status"] = "failed"
        result["elapsed"] = round(elapsed, 2)
        result["error"] = str(e)
        print(f"  ❌ App start failed after {elapsed:.2f}s: {e}", flush=True)
        return result


# ============================================
# Main Smoke Test Runner
# ============================================
def run_smoke_test(serial: str, package: Optional[str] = None, timeout: int = DEFAULT_TIMEOUT) -> dict:
    """
    Run complete uiautomator2 smoke test.
    
    Args:
        serial: ADB serial (e.g., "192.168.1.100:5555")
        package: Optional app package to test starting
        timeout: Timeout in seconds per step
    
    Returns:
        dict with test results
    """
    all_results = []
    
    print("=" * 70)
    print("🤖 GeeLark Cloud Phone - uiautomator2 Smoke Test")
    print("=" * 70)
    print(f"  Serial:  {serial}")
    print(f"  Timeout: {timeout}s per step")
    print(f"  Package: {package or 'N/A (skip app_start test)'}")
    print("=" * 70)
    
    # Step 1: Connect
    print("\n[1/4] Connection Test")
    print("-" * 70)
    conn_result, d = step_connect(serial, timeout)
    all_results.append(conn_result)
    
    if conn_result["status"] != "ok":
        print("\n❌ Connection failed. Cannot continue tests.")
        return {
            "results": all_results,
            "summary": "failed",
            "failed_at": "connect"
        }
    
    # Step 2: Get device info
    print("\n[2/4] Device Info Test")
    print("-" * 70)
    info_result = step_get_info(d, timeout)
    all_results.append(info_result)
    
    # Step 3: Dump hierarchy
    print("\n[3/4] UI Hierarchy Dump Test")
    print("-" * 70)
    dump_result = step_dump_hierarchy(d, timeout)
    all_results.append(dump_result)
    
    # Step 4: App start (optional)
    if package:
        print("\n[4/4] App Start Test")
        print("-" * 70)
        app_result = test_app_start(d, package, timeout)
        all_results.append(app_result)
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Smoke Test Summary")
    print("=" * 70)
    
    ok_count = sum(1 for r in all_results if r["status"] == "ok")
    warn_count = sum(1 for r in all_results if r["status"] == "warning")
    fail_count = sum(1 for r in all_results if r["status"] == "failed")
    total_elapsed = sum(r.get("elapsed", 0) for r in all_results)
    
    print(f"  ✅ OK:        {ok_count}")
    print(f"  ⚠️  WARNING:   {warn_count}")
    print(f"  ❌ FAILED:    {fail_count}")
    print(f"  ⏱️  Total:     {total_elapsed:.2f}s")
    
    # Show elapsed times
    print("\n⏱️  Step Timings:")
    for r in all_results:
        status_icon = {"ok": "✅", "warning": "⚠️", "failed": "❌"}.get(r["status"], "❓")
        print(f"  {status_icon} {r['step']:20s} {r.get('elapsed', 0):6.2f}s")
    
    # Determine overall status
    if fail_count > 0:
        summary = "failed"
    elif warn_count > 0:
        summary = "warning"
    else:
        summary = "passed"
    
    print(f"\n🎯 Overall: {summary.upper()}")
    print("=" * 70)
    
    return {
        "results": all_results,
        "summary": summary,
        "total_elapsed": round(total_elapsed, 2)
    }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="GeeLark uiautomator2 Smoke Test")
    parser.add_argument("serial", help="ADB serial (e.g., 192.168.1.100:5555)")
    parser.add_argument("--package", "-p", help="App package to test (optional)")
    parser.add_argument("--timeout", "-t", type=int, default=DEFAULT_TIMEOUT, help=f"Timeout per step in seconds (default: {DEFAULT_TIMEOUT})")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    
    args = parser.parse_args()
    
    result = run_smoke_test(
        serial=args.serial,
        package=args.package,
        timeout=args.timeout
    )
    
    if args.json:
        print("\n" + json.dumps(result, indent=2))
    
    # Exit with error code if tests failed
    sys.exit(1 if result["summary"] == "failed" else 0)
