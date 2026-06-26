#!/usr/bin/env python3
"""
GeeLark Cloud Phone Delete Helper - Double Confirmation Mechanism

⚠️ CRITICAL: Deleting cloud phones requires double confirmation:
1. List all phones
2. User manually types phone IDs
3. User types 'YES' (case-sensitive)

Usage:
    from scripts.delete_helper import delete_cloud_phones_with_confirmation

    delete_cloud_phones_with_confirmation(reason="Testing completed")
"""

import sys
import time
import requests
from scripts.geelark_client import GeeLarkClient


def check_interactive_terminal() -> bool:
    """
    Check if running in an interactive terminal.
    
    Returns:
        True if interactive terminal, False otherwise
    """
    if not sys.stdin.isatty():
        print("❌ ERROR: This operation requires an interactive terminal.")
        print("   AI agents cannot perform deletion operations.")
        print("   Please run this script manually in a terminal.")
        return False
    return True


def list_cloud_phones(client: GeeLarkClient) -> list:
    """
    List all available cloud phones.

    Args:
        client: GeeLarkClient instance

    Returns:
        List of cloud phone dictionaries
    """
    try:
        response = client.phone_list()
        if response.get('code') == 0:
            return response.get('data', {}).get('items', [])
        return []
    except requests.RequestException as e:
        print(f"❌ Network error listing phones: {e}")
        return []
    except Exception as e:
        print(f"❌ Unexpected error listing phones: {e}")
        return []


def display_phones(phones: list):
    """
    Display cloud phones for user confirmation.

    Args:
        phones: List of cloud phone dictionaries
    """
    print("=" * 60)
    print("⚠️  WARNING: Delete Operation")
    print("=" * 60)
    print(f"\nFound {len(phones)} cloud phone(s) to delete:\n")

    for i, phone in enumerate(phones, 1):
        status = 'Running' if phone.get('status') == 0 else 'Stopped'
        serial_name = phone.get('serialName', 'N/A')
        os_version = phone.get('equipmentInfo', {}).get('osVersion', 'N/A')
        phone_id = phone.get('id', 'N/A')

        print(f"   {i}. {serial_name} ({phone_id})")
        print(f"      OS: {os_version}, Status: {status}")
    print()


def confirm_phone_ids(phones: list) -> bool:
    """
    First confirmation: User must manually type phone IDs.
    
    Includes timing check to prevent automated rapid input.

    Args:
        phones: List of cloud phone dictionaries

    Returns:
        True if IDs match, False otherwise
    """
    phone_ids = [str(p['id']) for p in phones]

    print("=" * 60)
    print("⚠️  DELETION IS PERMANENT AND CANNOT BE UNDONE!")
    print("=" * 60)
    print()

    print(f"Please type the phone IDs to delete (copy-paste):")
    print(f"   {', '.join(phone_ids)}")
    print()

    # Timing check: prevent automated rapid input
    start_time = time.time()
    
    try:
        user_input = input("Enter phone IDs (comma-separated) to confirm: ").strip()
        elapsed = time.time() - start_time
        
        # If input is too fast (< 0.5 seconds), likely automated
        if elapsed < 0.5:
            print(f"❌ Input too fast ({elapsed:.2f}s). This appears to be automated.")
            print("   Please type the IDs manually.")
            return False
            
    except (EOFError, KeyboardInterrupt):
        print("\n❌ Operation cancelled")
        return False

    input_ids = [id.strip() for id in user_input.split(',')]
    
    # Verify input matches
    if set(input_ids) != set(phone_ids):
        print("❌ Phone IDs do not match. Deletion cancelled.")
        return False

    print()
    return True


def confirm_yes() -> bool:
    """
    Second confirmation: User must type 'YES'.
    
    Includes timing check and mandatory delay to prevent automated input.

    Returns:
        True if user typed 'YES', False otherwise
    """
    # Mandatory 3-second delay before second confirmation
    print("⏳ Waiting 3 seconds before final confirmation...")
    time.sleep(3)
    
    start_time = time.time()
    
    try:
        confirm = input("Type 'YES' (all caps) to confirm deletion: ").strip()
        elapsed = time.time() - start_time
        
        # If input is too fast (< 0.5 seconds), likely automated
        if elapsed < 0.5:
            print(f"❌ Input too fast ({elapsed:.2f}s). This appears to be automated.")
            print("   Please type 'YES' manually.")
            return False
            
    except (EOFError, KeyboardInterrupt):
        print("\n❌ Operation cancelled")
        return False

    if confirm != 'YES':
        print("❌ Confirmation failed. Deletion cancelled.")
        return False

    return True


def check_running_phones(phones: list, client: GeeLarkClient) -> bool:
    """
    Check if any phones are running and must be stopped first.
    
    Updates phone status in the list after stopping to maintain state consistency.

    Args:
        phones: List of cloud phone dictionaries
        client: GeeLarkClient instance

    Returns:
        True if all phones are stopped, False if any are running
    """
    running_phones = [p for p in phones if p.get('status') == 0]

    if running_phones:
        print("⚠️  The following phones are running and must be stopped first:")
        for phone in running_phones:
            print(f"   - {phone.get('serialName', 'N/A')} ({phone.get('id', 'N/A')})")
        print()
        try:
            response = input("Stop these phones now? (y/n): ").strip().lower()
            if response != 'y':
                print("❌ Operation cancelled")
                return False
        except (EOFError, KeyboardInterrupt):
            print("\n❌ Operation cancelled")
            return False

        # Stop running phones
        phone_ids = [p['id'] for p in running_phones]
        print(f"\nStopping {len(phone_ids)} phone(s)...")
        
        try:
            response = client.phone_stop(phone_ids)
            if response.get('code') == 0:
                print("✅ Phones stopped")
                # Update local status to maintain state consistency
                for phone in phones:
                    if phone['id'] in phone_ids:
                        phone['status'] = 1  # Mark as stopped
            else:
                print(f"❌ Failed to stop phones: {response}")
                return False
        except requests.RequestException as e:
            print(f"❌ Network error stopping phones: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error stopping phones: {e}")
            return False

        print()
    return True


def delete_cloud_phones_with_confirmation(client: GeeLarkClient = None, reason: str = ""):
    """
    Delete cloud phones with mandatory double confirmation.
    
    ⚠️  CRITICAL: This function requires an interactive terminal.
        AI agents cannot execute deletion operations.

    Args:
        client: GeeLarkClient instance (optional, will create if not provided)
        reason: Reason for deletion (optional)
    """
    # Verify interactive terminal before proceeding
    if not check_interactive_terminal():
        return
    
    # Create client if not provided
    if client is None:
        try:
            # Initialize with logging enabled
            client = GeeLarkClient(task_name="phone_deletion", phone_id="batch")
        except Exception as e:
            print(f"❌ Failed to create GeeLarkClient: {e}")
            sys.exit(1)

    # Step 1: List phones
    phones = list_cloud_phones(client)
    if not phones:
        print("❌ No available cloud phones")
        client.save_log()
        return

    # Step 2: Display phones
    display_phones(phones)

    # Step 3: Check and stop running phones
    if not check_running_phones(phones, client):
        client.save_log()
        return

    # Step 4: First confirmation - phone IDs
    if not confirm_phone_ids(phones):
        client.save_log()
        return

    # Step 5: Display reason if provided
    if reason:
        print(f"Reason: {reason}")
        print()

    # Step 6: Second confirmation - YES
    if not confirm_yes():
        client.save_log()
        return

    # Step 7: Execute deletion
    phone_ids = [p['id'] for p in phones]
    print(f"\n🗑️  Deleting {len(phone_ids)} cloud phone(s)...")

    try:
        response = client.execute_phone_deletion(phone_ids, confirmation_code='DELETE_CONFIRMED')

        if response.get('code') == 0:
            print("✅ Deletion successful")
        else:
            print(f"❌ Deletion failed: {response.get('msg', 'Unknown error')}")
    except requests.RequestException as e:
        print(f"❌ Network error during deletion: {e}")
    except Exception as e:
        print(f"❌ Unexpected error during deletion: {e}")
    finally:
        # Always save log
        client.save_log()


if __name__ == "__main__":
    # Test
    delete_cloud_phones_with_confirmation(reason="Test deletion")