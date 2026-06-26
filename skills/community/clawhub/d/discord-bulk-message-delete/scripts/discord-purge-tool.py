#!/usr/bin/env python3
"""
Discord Bulk Message Purge Tool (With --delete Flag)
========================================

A simple, reusable Python script for deleting messages from Discord channels.
Uses only Python standard library + requests.

USAGE:
  python discord-purge-tool.py <count> [OPTIONS] --channel-id <channel_id>
  
  Without --delete flag (DRY-RUN mode):
    python discord-purge-tool.py 25 --channel-id 1499147924926627992
    
  With --delete flag (actual deletion):
    python discord-purge-tool.py 25 --delete --channel-id 1499147924926627992

EXAMPLES:
  # Delete last 5 messages
  python discord-purge-tool.py 5 --channel-id 1499147924926627992
  
  # Delete last 20 messages  
  python discord-purge-tool.py purge 20 --channel-id 1499147924926627992
  
  # Dry-run mode (no deletion)
  python discord-purge-tool.py purge 50 --channel-id 1499147924926627992
  
  # Actual deletion
  python discord-purge-tool.py purge 50 --delete --channel-id 1499147924926627992

CONFIGURATION:
  - Create token.json with your bot token OR set DISCORD_TOKEN environment variable
  - Example token.json: {"token": "token.token2.token3-token4"}

RATE LIMITING:
  - Handles Discord's 100 messages per batch limit automatically
  - Waits between batches if needed

PERMISSIONS REQUIRED:
  - Bot must have MANAGE_MESSAGES permission in target channel
"""

import sys
import json
import urllib.request
from pathlib import Path


def get_token():
    """Load Discord bot token from file or environment variable."""
    import os
    token_file = Path(__file__).parent / "token.json"
    
    if 'DISCORD_TOKEN' in os.environ:
        return os.environ['DISCORD_TOKEN']
    
    try:
        with open(token_file, 'r') as f:
            data = json.load(f)
            return data.get('token', '')
    except Exception as e:
        print(f"[ERROR] Failed to load token: {e}")
        return None


def purge_messages(channel_id, count=5, delete_mode=False):
    """
    Fetch and optionally delete the last N messages from a Discord channel.
    
    Args:
        channel_id: Discord channel ID (numeric string)
        count: Number of messages to delete (default 5, max 100 per API batch)
        delete_mode: If True, actually delete messages; if False, dry-run only
    
    Returns:
        Tuple of (success: bool, message_count: int, deleted_ids: list)
    """
    # Get token
    token = get_token()
    if not token:
        return False, 0, None
    
    headers = {
        'Authorization': f'Bot {token}',
        'Content-Type': 'application/json',
        'User-Agent': 'Discord Bot/1.0 (discord-purge-tool)'
    }

    print(f"\n--- DISCORD BULK PURGE STARTED ---")
    print(f"[OK] Channel ID: {channel_id}")
    print(f"[OK] Count: {count} messages")
    if delete_mode:
        print("[OK] Delete mode enabled (will actually delete messages)")
    else:
        print("[INFO] Dry-run mode (no deletion, just preview)\n")

    # Calculate batch size (Discord API limit: max 100 per request)
    max_batch = min(count, 100)
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages?limit={max_batch}"
    
    print(f"[INFO] Fetching last {max_batch} messages...")
    
    try:
        req = urllib.request.Request(url, method="GET", headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                messages = json.loads(response.read().decode())
                
                if not messages or len(messages) == 0:
                    print("[WARN] No messages to delete")
                    return False, 0, None
                
                # Extract message IDs (max 100 per Discord API batch)
                message_ids = [msg['id'] for msg in messages[:100]]
                
                if len(message_ids) == 0:
                    print("[WARN] No message IDs extracted")
                    return False, 0, None
                
                print(f"[OK] Fetched {len(message_ids)} messages\n")
                
            else:
                error_body = response.read().decode()
                print(f"\n=== ERROR ===")
                print(f"[ERROR] HTTP Error: {response.status} - {error_body[:300]}")
                return False, 0, None
                
    except urllib.error.HTTPError as e:
        body = e.read().decode() if hasattr(e, 'read') else str(e)
        print(f"\n=== ERROR ===")
        print(f"[ERROR] HTTP Error: {e.code} - {body[:300]}")
        return False, 0, None
    except Exception as e:
        print(f"\n=== ERROR ===")
        print(f"[ERROR] Failed to fetch messages: {e}")
        return False, 0, None
    
    # Dry-run mode: show what would be deleted without deleting
    if not delete_mode:
        print("=== DRY-RUN MODE ===")
        print("[OK] Would delete the following messages:")
        
        for i, msg_id in enumerate(message_ids, 1):
            print(f"   {i}. {msg_id}")
        
        if len(message_ids) > 10:
            print(f"   ... and {len(message_ids) - 10} more")
        
        print()
        print("=== DELETION NOT PERFORMED ===")
        print("[INFO] Use --delete flag to actually delete messages\n")
        return False, len(message_ids), message_ids
    
    # Deletion mode: actually delete the messages
    print(f"\n[INFO] Deleting {len(message_ids)} messages using bulk delete API...")

    try:
        deleted_url = f"https://discord.com/api/v10/channels/{channel_id}/messages/bulk-delete"
        
        data_to_send = json.dumps({"messages": message_ids}).encode()
        req = urllib.request.Request(deleted_url, data=data_to_send, method="POST", headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 204:
                print("[OK] Bulk delete successful!")
                print("\n=== PURGE COMPLETE ===")
                print("[OK] Status: SUCCESS")
                print(f"[OK] Messages deleted: {len(message_ids)}")
                
                return True, len(message_ids), message_ids
            else:
                error = response.read().decode()
                print(f"\n=== ERROR ===")
                print(f"[ERROR] Status: HTTP {response.status}: {error[:200]}")
                return False, 0, None
        
    except urllib.error.HTTPError as e:
        body = e.read().decode() if hasattr(e, 'read') else str(e)
        print(f"\n=== ERROR ===")
        print(f"[ERROR] HTTP Error: {e.code} - {body[:300]}")
        return False, 0, None
    except Exception as e:
        print(f"\n=== ERROR ===")
        print(f"[ERROR] Failed to delete messages: {e}")
        return False, 0, None


def main():
    """Main entry point - parse command line arguments."""
    args_list = sys.argv[1:]
    
    # Parse arguments
    channel_id = None
    count = 5  # default
    delete_mode = False  # True only if --delete flag is present
    
    for i, arg in enumerate(args_list):
        if arg.startswith('--channel-id='):
            channel_id = arg.split('=', 1)[1]
        elif arg == '--channel-id' and i + 1 < len(args_list):
            channel_id = args_list[i + 1]
        elif arg in ('-d', '--delete'):
            delete_mode = True
        elif arg in ('purge',) and i + 1 < len(args_list):
            purge_mode = True
            count = int(args_list[i + 1])
        elif not arg.startswith('-') and channel_id is None:
            # First positional arg might be count (if no 'purge' prefix)
            try:
                count = int(arg)
            except ValueError:
                pass
    
    if not channel_id:
        print("Discord Bulk Message Purge Tool")
        print("=" * 50)
        print("[ERROR] No valid --channel-id specified")
        print("\nUSAGE:")
        print('  python discord-purge-tool.py purge <count> [OPTIONS] --channel-id <id>')
        print('  Options:')
        print('    -d, --delete     Enable deletion mode (default: dry-run)')
        return
    
    # Print debug info
    print("Discord Bulk Message Purge Tool")
    print("=" * 50)
    print("[INFO] Parsed arguments:")
    print(f"[OK] Channel ID: {channel_id}")
    print(f"[OK] Count: {count} messages")
    if delete_mode:
        print("[OK] Delete mode enabled (will actually delete messages)")
    else:
        print("[INFO] Dry-run mode (no deletion, just preview)\n")

    # Execute purge
    success, count_deleted, deleted_ids = purge_messages(channel_id, count, delete_mode)


if __name__ == "__main__":
    main()
