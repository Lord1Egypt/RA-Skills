#!/usr/bin/env python3
"""
Android Permission Dialog Handler

Reusable module for handling common Android permission/system dialogs
that appear during app installation and first launch.

Handles both English and Chinese UI text, including curly quotes
(DON'T ALLOW / ALLOW vs DON'T ALLOW / ALLOW).

Usage:
    # As a module (recommended)
    from scripts.handle_android_permissions import handle_permission_dialogs
    handle_permission_dialogs(d, max_retries=5)

    # As a standalone script
    python scripts/handle_android_permissions.py <adb_serial>
    python scripts/handle_android_permissions.py 192.168.1.100:5555 --action deny
"""

import sys
import os
import time
import argparse
from typing import Optional

# Add project root to path
_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_script_dir)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)


# ============================================
# Permission Button Definitions
# ============================================

# Allow buttons: English (straight + curly quotes), Chinese
ALLOW_BUTTONS = [
    "Allow",
    "ALLOW",
    "allow",
    "ALLOW",        # curly left single quote
    "Allow",        # curly quotes
    "ALLOW",        # curly quotes
    "允许",
    "同意",
    "确定",
    "OK",
    "ok",
]

# Deny buttons: English (straight + curly quotes), Chinese
DENY_BUTTONS = [
    "Don't Allow",
    "DON'T ALLOW",
    "don't allow",
    "Don't Allow",    # curly left single quote
    "DON'T ALLOW",    # curly quotes
    "Don't Allow",    # curly quotes
    "拒绝",
    "不允许",
    "取消",
    "Cancel",
    "CANCEL",
]

# Close/Dismiss buttons (for non-permission system dialogs)
CLOSE_BUTTONS = [
    "Close",
    "CLOSE",
    "close",
    "关闭",
    "结束",
    "Done",
    "DONE",
    "完成",
]


def _try_click(d, texts: list, timeout: float = 2.0) -> bool:
    """
    Try to find and click any button matching the given text list.

    Args:
        d: uiautomator2 device instance
        texts: List of button text patterns to try
        timeout: Max seconds to wait for each element

    Returns:
        True if a button was found and clicked, False otherwise
    """
    for text in texts:
        try:
            btn = d(text=text)
            if btn.exists and btn.visible:
                btn.click()
                return True
        except Exception:
            continue
    return False


def handle_permission_dialog(d, action: str = "allow", timeout: float = 3.0) -> bool:
    """
    Handle a single Android permission dialog.

    Args:
        d: uiautomator2 device instance
        action: "allow" or "deny" - what to do with the permission
        timeout: Seconds to wait for dialog to appear

    Returns:
        True if a dialog was handled, False if no dialog found
    """
    buttons = ALLOW_BUTTONS if action == "allow" else DENY_BUTTONS

    # Wait briefly for dialog to appear
    start = time.time()
    while time.time() - start < timeout:
        if _try_click(d, buttons):
            return True
        time.sleep(0.3)

    return False


def handle_permission_dialogs(d, max_retries: int = 5, action: str = "allow", interval: float = 1.0) -> int:
    """
    Repeatedly handle permission dialogs until none appear.

    Useful after app installation or first launch when multiple
    permission requests appear sequentially.

    Args:
        d: uiautomator2 device instance
        max_retries: Maximum number of dialogs to handle
        action: "allow" or "deny" - what to do with each permission
        interval: Seconds between checks

    Returns:
        Number of dialogs handled
    """
    handled = 0
    consecutive_empty = 0
    max_empty = 3  # Stop after 3 consecutive checks with no dialog

    for i in range(max_retries):
        if handle_permission_dialog(d, action=action, timeout=2.0):
            handled += 1
            consecutive_empty = 0
            print(f"  ✅ Handled permission dialog #{handled} (action: {action})", flush=True)
        else:
            consecutive_empty += 1
            if consecutive_empty >= max_empty:
                break
        time.sleep(interval)

    if handled > 0:
        print(f"  📊 Total dialogs handled: {handled}", flush=True)
    return handled


def handle_system_dialogs(d, max_retries: int = 3, interval: float = 1.0) -> int:
    """
    Handle common system dialogs (Not Now, Close, Done, etc.).

    These are non-permission dialogs that appear during app setup.

    Args:
        d: uiautomator2 device instance
        max_retries: Maximum number of dialogs to handle
        interval: Seconds between checks

    Returns:
        Number of dialogs handled
    """
    handled = 0
    consecutive_empty = 0
    max_empty = 3

    all_buttons = CLOSE_BUTTONS + ["Not Now", "NOT NOW", "稍后", "以后再说"]

    for i in range(max_retries):
        if _try_click(d, all_buttons):
            handled += 1
            consecutive_empty = 0
            print(f"  ✅ Handled system dialog #{handled}", flush=True)
        else:
            consecutive_empty += 1
            if consecutive_empty >= max_empty:
                break
        time.sleep(interval)

    return handled


def handle_all_dialogs(d, permission_action: str = "allow", max_permission_retries: int = 5,
                       max_system_retries: int = 3, interval: float = 1.0) -> dict:
    """
    Handle all types of dialogs: permissions first, then system dialogs.

    Args:
        d: uiautomator2 device instance
        permission_action: "allow" or "deny" for permission dialogs
        max_permission_retries: Max permission dialogs to handle
        max_system_retries: Max system dialogs to handle
        interval: Seconds between checks

    Returns:
        dict with 'permissions_handled' and 'system_handled' counts
    """
    print(f"\n🔧 Handling dialogs (permissions: {permission_action})...", flush=True)

    # Handle permission dialogs first
    perm_count = handle_permission_dialogs(d, max_retries=max_permission_retries,
                                           action=permission_action, interval=interval)

    # Then handle system dialogs
    sys_count = handle_system_dialogs(d, max_retries=max_system_retries, interval=interval)

    result = {
        "permissions_handled": perm_count,
        "system_handled": sys_count,
        "total": perm_count + sys_count
    }

    print(f"  📊 Summary: {perm_count} permissions + {sys_count} system = {result['total']} total dialogs", flush=True)
    return result


# ============================================
# Standalone CLI
# ============================================
def main():
    parser = argparse.ArgumentParser(
        description="Android Permission Dialog Handler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Handle all dialogs on a device (allow permissions)
  python scripts/handle_android_permissions.py 192.168.1.100:5555

  # Deny all permissions
  python scripts/handle_android_permissions.py 192.168.1.100:5555 --action deny

  # Handle up to 10 dialogs
  python scripts/handle_android_permissions.py 192.168.1.100:5555 --max-retries 10
        """
    )

    parser.add_argument("serial", help="ADB serial (e.g., 192.168.1.100:5555)")
    parser.add_argument("--action", choices=["allow", "deny"], default="allow",
                        help="Action for permission dialogs (default: allow)")
    parser.add_argument("--max-retries", type=int, default=5,
                        help="Max permission dialogs to handle (default: 5)")
    parser.add_argument("--max-system", type=int, default=3,
                        help="Max system dialogs to handle (default: 3)")
    parser.add_argument("--interval", type=float, default=1.0,
                        help="Seconds between checks (default: 1.0)")

    args = parser.parse_args()

    print("=" * 70)
    print("🔧 Android Permission Dialog Handler")
    print("=" * 70)
    print(f"  Serial:    {args.serial}")
    print(f"  Action:    {args.action}")
    print(f"  Max perms: {args.max_retries}")
    print(f"  Max sys:   {args.max_system}")
    print("=" * 70)

    try:
        import uiautomator2 as u2
        d = u2.connect(args.serial)
        print(f"  ✅ Connected to {args.serial}", flush=True)
    except ImportError:
        print("  ❌ uiautomator2 not installed", flush=True)
        sys.exit(1)
    except Exception as e:
        print(f"  ❌ Connection failed: {e}", flush=True)
        sys.exit(1)

    # Handle all dialogs
    result = handle_all_dialogs(
        d,
        permission_action=args.action,
        max_permission_retries=args.max_retries,
        max_system_retries=args.max_system,
        interval=args.interval
    )

    print("\n" + "=" * 70)
    print(f"✅ Done: {result['total']} dialogs handled")
    print("=" * 70)


if __name__ == "__main__":
    main()
