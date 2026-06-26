#!/usr/bin/env python
"""钉钉 Talk 测试工具"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server import send_message_to_contact, send_message_to_current, get_dingding_status


def test_status():
    print("\n=== Test: Get DingDing Status ===")
    status = get_dingding_status()
    print(f"Status: {status}")
    return status


def test_send_current(message):
    print(f"\n=== Test: Send Message to Current ===")
    print(f"Message: {message}")
    
    success = send_message_to_current(message)
    
    if success:
        print(f"[OK] Sent: {message}")
    else:
        print(f"[ERROR] Failed to send")
    
    return success


def test_send_contact(contact, message):
    print(f"\n=== Test: Send Message to Contact ===")
    print(f"Contact: {contact}")
    print(f"Message: {message}")
    
    success, err = send_message_to_contact(contact, message)
    
    if success:
        print(f"[OK] Sent to {contact}: {message}")
    else:
        print(f"[ERROR] {err}")
    
    return success, err


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="DingDing Talk Test")
    parser.add_argument("action", choices=["status", "send-current", "send-contact"], help="Action")
    parser.add_argument("--contact", "-c", help="Contact name")
    parser.add_argument("--message", "-m", help="Message")
    
    args = parser.parse_args()
    
    if args.action == "status":
        test_status()
    elif args.action == "send-current":
        if not args.message:
            print("Error: Need --message")
            return
        test_send_current(args.message)
    elif args.action == "send-contact":
        if not args.contact or not args.message:
            print("Error: Need --contact and --message")
            return
        test_send_contact(args.contact, args.message)


if __name__ == "__main__":
    main()
