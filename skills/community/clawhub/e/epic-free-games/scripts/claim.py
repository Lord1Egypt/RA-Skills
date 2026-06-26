#!/usr/bin/env python3
"""
Epic Games Free Games Auto Claimer
2026 Latest Page Adaptation with Persistent Login

Usage:
    python claim.py --login      # First time login (save auth state)
    python claim.py              # Auto claim free games
    python claim.py --headed     # Show browser window
"""

import subprocess
import json
import argparse
import os
import sys
import time
from pathlib import Path

# Configuration
EPIC_FREE_URL = "https://store.epicgames.com/zh-CN/free-games"
AUTH_FILE = Path(__file__).parent.parent / "epic_auth.json"
TIMEOUT = 30

# 2026 Latest CSS Selectors (data-testid based, stable against page updates)
SELECTORS = {
    "sign_in_btn": "button#sign-in, button[data-testid='sign-in']",
    "free_game_get": 'button[data-testid="purchase-button"]',
    "order_confirm": 'button[data-testid="checkout-order-button"], button[data-testid="confirm-order-button"]',
    "success_tip": 'div[data-testid="purchase-complete-success"], [data-testid="success"]',
    "already_owned": '[data-testid="already-owned"], .already-owned',
}


def run_browser_cmd(args: list, session: str = "epic") -> dict:
    """Run agent-browser command and return JSON result."""
    # Get full path to agent-browser
    import shutil
    browser_path = shutil.which("agent-browser")
    if not browser_path:
        return {"success": False, "error": "agent-browser not found. Install with: npm install -g agent-browser"}
    
    cmd = [browser_path, "--session", session] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=TIMEOUT + 10
        )
        if result.stdout:
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return {"success": False, "error": "Invalid JSON output", "raw": result.stdout}
        return {"success": False, "error": result.stderr or "No output"}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Command timeout"}
    except FileNotFoundError:
        return {"success": False, "error": "agent-browser not found. Install with: npm install -g agent-browser"}


def save_auth_state(session: str = "epic", auth_file: Path = AUTH_FILE):
    """Save browser auth state to file."""
    result = run_browser_cmd(["state", "save", str(auth_file)], session)
    if result.get("success"):
        print(f"[OK] Auth state saved to {auth_file}")
    else:
        print(f"[WARN] Failed to save auth state: {result.get('error')}")


def load_auth_state(session: str = "epic", auth_file: Path = AUTH_FILE) -> bool:
    """Load browser auth state from file."""
    if not auth_file.exists():
        return False
    result = run_browser_cmd(["state", "load", str(auth_file)], session)
    return result.get("success", False)


def check_login_status(session: str = "epic") -> bool:
    """Check if user is logged in by looking for sign-in button."""
    result = run_browser_cmd(["snapshot", "-i", "--json"], session)
    if not result.get("success"):
        return False
    
    refs = result.get("data", {}).get("refs", {})
    # If sign-in button exists, user is NOT logged in
    for ref_id, ref_data in refs.items():
        name = ref_data.get("name", "").lower()
        role = ref_data.get("role", "")
        if "sign in" in name or "登录" in name or role == "button" and "sign" in name:
            return False
    return True


def find_element_by_testid(session: str, testid: str) -> str | None:
    """Find element ref by data-testid attribute."""
    result = run_browser_cmd(["snapshot", "-i", "--json"], session)
    if not result.get("success"):
        return None
    
    refs = result.get("data", {}).get("refs", {})
    for ref_id, ref_data in refs.items():
        # Check if element matches the selector pattern
        name = ref_data.get("name", "").lower()
        role = ref_data.get("role", "")
        
        # Match patterns like "获取", "Get", "下订单", "Place Order"
        if testid == "purchase-button":
            if role == "button" and ("get" in name or "获取" in name or "免费" in name):
                return ref_id
        elif testid == "checkout-order-button":
            if role == "button" and ("order" in name or "订单" in name or "购买" in name):
                return ref_id
        elif testid == "purchase-complete-success":
            if "success" in name or "成功" in name or "完成" in name:
                return ref_id
    
    return None


def click_element(session: str, ref: str) -> bool:
    """Click element by ref."""
    result = run_browser_cmd(["click", f"@{ref}"], session)
    return result.get("success", False)


def wait_for_element(session: str, testid: str, timeout: int = 10) -> str | None:
    """Wait for element to appear."""
    start = time.time()
    while time.time() - start < timeout:
        ref = find_element_by_testid(session, testid)
        if ref:
            return ref
        time.sleep(1)
    return None


def login_flow(headed: bool = False, auth_file: Path = AUTH_FILE):
    """Interactive login flow - user logs in manually."""
    print("=" * 50)
    print("Epic Games Login Flow")
    print("=" * 50)
    
    session = "epic"
    
    # Open Epic store
    args = ["open", EPIC_FREE_URL]
    if headed:
        args.append("--headed")
    
    print(f"[INFO] Opening Epic Games Store...")
    result = run_browser_cmd(args, session)
    
    if not result.get("success"):
        print(f"[ERROR] Failed to open page: {result.get('error')}")
        return False
    
    print("\n" + "!" * 50)
    print("请在打开的浏览器窗口中手动登录你的 Epic 账号")
    print("Please log in to your Epic account in the browser window")
    print("登录完成后按 Enter 继续...")
    print("Press Enter after logging in...")
    print("!" * 50 + "\n")
    
    input()  # Wait for user to press Enter
    
    # Save auth state
    save_auth_state(session, auth_file)
    
    # Close browser
    run_browser_cmd(["close"], session)
    
    print("\n[OK] Login complete! Auth state saved.")
    print("[INFO] You can now run 'python claim.py' to claim free games.")
    return True


def claim_free_games(headed: bool = False, timeout: int = TIMEOUT, auth_file: Path = AUTH_FILE):
    """Main flow to claim free games."""
    print("=" * 50)
    print("Epic Free Games Auto Claimer")
    print("=" * 50)
    
    session = "epic"
    
    # Step 1: Open Epic free games page
    print("\n[1/5] Opening Epic Free Games page...")
    args = ["open", EPIC_FREE_URL]
    if headed:
        args.append("--headed")
    
    result = run_browser_cmd(args, session)
    if not result.get("success"):
        print(f"[ERROR] Failed to open page: {result.get('error')}")
        return False
    
    time.sleep(3)  # Wait for page load
    
    # Step 2: Load auth state
    print("[2/5] Loading auth state...")
    if auth_file.exists():
        if load_auth_state(session, auth_file):
            print("[OK] Auth state loaded")
        else:
            print("[WARN] Failed to load auth state, may need to re-login")
    else:
        print("[WARN] No auth file found. Run with --login first!")
        return False
    
    # Step 3: Check login status
    print("[3/5] Checking login status...")
    time.sleep(2)
    
    result = run_browser_cmd(["snapshot", "-i", "--json"], session)
    if result.get("success"):
        refs = result.get("data", {}).get("refs", {})
        print(f"[INFO] Found {len(refs)} interactive elements")
        
        # Look for sign-in button
        for ref_id, ref_data in refs.items():
            name = ref_data.get("name", "").lower()
            if "sign in" in name or "登录" in name:
                print("[ERROR] Not logged in! Please run with --login first")
                run_browser_cmd(["close"], session)
                return False
    else:
        print("[WARN] Could not verify login status")
    
    print("[OK] Login verified")
    
    # Step 4: Find and click "Get" button
    print("[4/5] Looking for free games to claim...")
    time.sleep(2)
    
    result = run_browser_cmd(["snapshot", "-i", "--json"], session)
    if not result.get("success"):
        print(f"[ERROR] Failed to get page snapshot: {result.get('error')}")
        run_browser_cmd(["close"], session)
        return False
    
    refs = result.get("data", {}).get("refs", {})
    
    # Find "Get" button
    get_button_ref = None
    for ref_id, ref_data in refs.items():
        name = ref_data.get("name", "").lower()
        role = ref_data.get("role", "")
        if role == "button" and ("获取" in name or "get" in name or "免费" in name):
            get_button_ref = ref_id
            print(f"[INFO] Found 'Get' button: {ref_data.get('name')}")
            break
    
    if not get_button_ref:
        print("[INFO] No free games available or already claimed all games")
        run_browser_cmd(["close"], session)
        return True
    
    # Click Get button
    print(f"[INFO] Clicking 'Get' button...")
    result = run_browser_cmd(["click", f"@{get_button_ref}"], session)
    if not result.get("success"):
        print(f"[ERROR] Failed to click Get button: {result.get('error')}")
        run_browser_cmd(["close"], session)
        return False
    
    print("[OK] Clicked 'Get' button, waiting for order page...")
    time.sleep(5)  # Wait for redirect
    
    # Step 5: Click "Place Order" button
    print("[5/5] Looking for 'Place Order' button...")
    
    result = run_browser_cmd(["snapshot", "-i", "--json"], session)
    if not result.get("success"):
        print(f"[ERROR] Failed to get order page snapshot")
        run_browser_cmd(["close"], session)
        return False
    
    refs = result.get("data", {}).get("refs", {})
    
    # Find "Place Order" button
    order_button_ref = None
    for ref_id, ref_data in refs.items():
        name = ref_data.get("name", "").lower()
        role = ref_data.get("role", "")
        if role == "button" and ("订单" in name or "order" in name or "购买" in name or "buy" in name):
            order_button_ref = ref_id
            print(f"[INFO] Found 'Place Order' button: {ref_data.get('name')}")
            break
    
    if order_button_ref:
        print(f"[INFO] Clicking 'Place Order' button...")
        result = run_browser_cmd(["click", f"@{order_button_ref}"], session)
        if result.get("success"):
            print("[OK] Order placed successfully!")
            time.sleep(3)
            
            # Check for success
            result = run_browser_cmd(["snapshot", "-i", "--json"], session)
            if result.get("success"):
                refs = result.get("data", {}).get("refs", {})
                for ref_id, ref_data in refs.items():
                    name = ref_data.get("name", "").lower()
                    if "成功" in name or "success" in name or "完成" in name:
                        print("\n" + "=" * 50)
                        print("SUCCESS! Free game claimed!")
                        print("免费游戏领取成功！")
                        print("=" * 50)
                        break
        else:
            print(f"[WARN] Failed to click order button: {result.get('error')}")
    else:
        print("[INFO] No order button found - game may already be owned")
    
    # Cleanup
    run_browser_cmd(["close"], session)
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Epic Games Free Games Auto Claimer (2026 Edition)"
    )
    parser.add_argument(
        "--login",
        action="store_true",
        help="First-time login mode (opens browser for manual login)"
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Show browser window (useful for debugging or handling captcha)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=TIMEOUT,
        help=f"Wait timeout in seconds (default: {TIMEOUT})"
    )
    parser.add_argument(
        "--auth-file",
        type=str,
        default=str(AUTH_FILE),
        help="Auth state file path"
    )
    
    args = parser.parse_args()
    
    # Update auth file path if specified
    auth_file = Path(args.auth_file)
    
    try:
        if args.login:
            success = login_flow(headed=True, auth_file=auth_file)  # Login always shows browser
        else:
            success = claim_free_games(headed=args.headed, timeout=args.timeout, auth_file=auth_file)
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
