#!/usr/bin/env python3
"""Credential Vault CLI - Encrypted credential storage for OpenClaw agents."""
import sys
import argparse
import getpass
from pathlib import Path

# Add parent directory to path for lib imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.store import Store, VaultError, VaultLocked, VaultNotInitialized
from lib.audit import AuditLogger
from lib.expiry import get_expiring_credentials


def cmd_init(args, store: Store, audit: AuditLogger):
    """Initialize a new vault."""
    password = getpass.getpass("Enter master password: ")
    confirm = getpass.getpass("Confirm master password: ")
    
    if password != confirm:
        print("❌ Passwords do not match")
        return 1
    
    if len(password) < 8:
        print("❌ Password must be at least 8 characters")
        return 1
    
    try:
        store.init(password)
        audit.log("init", "vault", {"action": "initialized"})
        return 0
    except VaultError as e:
        print(f"❌ {e}")
        return 1


def cmd_unlock(args, store: Store, audit: AuditLogger):
    """Unlock the vault."""
    password = getpass.getpass("Enter master password: ")
    
    try:
        store.unlock(password)
        audit.log("unlock", "vault", {"action": "unlocked"})
        return 0
    except (VaultError, VaultNotInitialized) as e:
        print(f"❌ {e}")
        return 1


def cmd_lock(args, store: Store, audit: AuditLogger):
    """Lock the vault."""
    store.lock()
    audit.log("lock", "vault", {"action": "locked"})
    return 0


def cmd_status(args, store: Store, audit: AuditLogger):
    """Show vault status."""
    status = store.status()
    
    if not status["initialized"]:
        print("❌ Vault not initialized. Run 'vault init' to create one.")
        return 1
    
    print(f"📊 Vault Status")
    print(f"   Path: {status['path']}")
    print(f"   State: {'🔓 Unlocked' if not status['locked'] else '🔒 Locked'}")
    print(f"   Credentials: {status['count']}")
    return 0


def cmd_add(args, store: Store, audit: AuditLogger):
    """Add a credential."""
    try:
        # Read value from stdin if not provided
        value = args.value
        if not value:
            value = getpass.getpass(f"Enter value for {args.key_name}: ")
        
        store.add(
            key_name=args.key_name,
            value=value,
            tags=args.tag,
            expires=args.expires
        )
        audit.log("add", args.key_name, {"tags": args.tag, "expires": args.expires})
        return 0
    except (VaultLocked, VaultError) as e:
        print(f"❌ {e}")
        return 1


def cmd_get(args, store: Store, audit: AuditLogger):
    """Get a credential."""
    try:
        value = store.get(args.key_name)
        print(value)
        audit.log("get", args.key_name)
        return 0
    except (VaultLocked, KeyError, VaultError) as e:
        print(f"❌ {e}")
        return 1


def cmd_list(args, store: Store, audit: AuditLogger):
    """List credentials."""
    try:
        credentials = store.list(tag=args.tag)
        
        if not credentials:
            print("No credentials found.")
            return 0
        
        print(f"📋 Credentials ({len(credentials)}):\n")
        for cred in credentials:
            print(f"  🔑 {cred['name']}")
            if cred['tags']:
                print(f"     Tags: {', '.join(cred['tags'])}")
            if cred['expires']:
                print(f"     Expires: {cred['expires']}")
            print()
        
        return 0
    except VaultError as e:
        print(f"❌ {e}")
        return 1


def cmd_remove(args, store: Store, audit: AuditLogger):
    """Remove a credential."""
    try:
        # Confirm deletion
        if not args.yes:
            confirm = input(f"Remove credential '{args.key_name}'? (y/N): ")
            if confirm.lower() != 'y':
                print("Cancelled.")
                return 0
        
        store.remove(args.key_name)
        audit.log("remove", args.key_name)
        return 0
    except (VaultLocked, KeyError, VaultError) as e:
        print(f"❌ {e}")
        return 1


def cmd_env(args, store: Store, audit: AuditLogger):
    """Export credentials as environment variables."""
    try:
        credentials = store.list(tag=args.tag)
        
        for cred in credentials:
            value = store.get(cred['name'])
            print(f"{cred['name']}={value}")
        
        audit.log("env", f"tag:{args.tag or 'all'}", {"count": len(credentials)})
        return 0
    except (VaultLocked, VaultError) as e:
        print(f"❌ {e}")
        return 1


def cmd_audit(args, store: Store, audit: AuditLogger):
    """View audit log."""
    entries = audit.read(last=args.last)
    
    if not entries:
        print("No audit entries.")
        return 0
    
    print(f"📝 Audit Log (last {len(entries)} entries):\n")
    for entry in entries:
        print(f"  [{entry['timestamp']}] {entry['action']}: {entry['key_name']}")
        if entry.get('details'):
            print(f"     Details: {entry['details']}")
    
    return 0


def cmd_expiring(args, store: Store, audit: AuditLogger):
    """Check for expiring credentials."""
    try:
        all_creds = store.list()
        expiring = get_expiring_credentials(all_creds, days=args.days)
        
        if not expiring:
            print(f"✅ No credentials expiring within {args.days} days.")
            return 0
        
        print(f"⚠️  Credentials expiring within {args.days} days:\n")
        for cred in expiring:
            status = "❌ EXPIRED" if cred['is_expired'] else f"⚠️  {cred['days_until_expiry']} days"
            print(f"  {status} - {cred['name']}")
            print(f"     Expires: {cred['expires']}")
            if cred['tags']:
                print(f"     Tags: {', '.join(cred['tags'])}")
            print()
        
        return 0
    except VaultError as e:
        print(f"❌ {e}")
        return 1


def cmd_rotate(args, store: Store, audit: AuditLogger):
    """Rotate a credential (replace with new value)."""
    try:
        # Get new value
        new_value = args.new_value
        if not new_value:
            new_value = getpass.getpass(f"Enter new value for {args.key_name}: ")
        
        # Get existing metadata
        old_cred = [c for c in store.list() if c['name'] == args.key_name]
        if not old_cred:
            print(f"❌ Credential not found: {args.key_name}")
            return 1
        
        old_cred = old_cred[0]
        
        # Update with new value
        store.add(
            key_name=args.key_name,
            value=new_value,
            tags=old_cred.get('tags', []),
            expires=old_cred.get('expires')
        )
        
        audit.log("rotate", args.key_name)
        print(f"🔄 Rotated credential: {args.key_name}")
        return 0
    except (VaultLocked, VaultError) as e:
        print(f"❌ {e}")
        return 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Credential Vault - Encrypted credential storage for OpenClaw agents"
    )
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # init
    subparsers.add_parser('init', help='Initialize a new vault')
    
    # unlock
    subparsers.add_parser('unlock', help='Unlock the vault')
    
    # lock
    subparsers.add_parser('lock', help='Lock the vault')
    
    # status
    subparsers.add_parser('status', help='Show vault status')
    
    # add
    parser_add = subparsers.add_parser('add', help='Add a credential')
    parser_add.add_argument('key_name', help='Credential name')
    parser_add.add_argument('value', nargs='?', help='Credential value (or prompt if omitted)')
    parser_add.add_argument('--tag', action='append', help='Tag(s) for categorization')
    parser_add.add_argument('--expires', help='Expiry date (YYYY-MM-DD)')
    
    # get
    parser_get = subparsers.add_parser('get', help='Get a credential')
    parser_get.add_argument('key_name', help='Credential name')
    
    # list
    parser_list = subparsers.add_parser('list', help='List credentials')
    parser_list.add_argument('--tag', help='Filter by tag')
    
    # remove
    parser_remove = subparsers.add_parser('remove', help='Remove a credential')
    parser_remove.add_argument('key_name', help='Credential name')
    parser_remove.add_argument('-y', '--yes', action='store_true', help='Skip confirmation')
    
    # env
    parser_env = subparsers.add_parser('env', help='Export credentials as KEY=VALUE')
    parser_env.add_argument('--tag', help='Export only credentials with this tag')
    
    # audit
    parser_audit = subparsers.add_parser('audit', help='View audit log')
    parser_audit.add_argument('--last', type=int, default=20, help='Number of entries to show')
    
    # expiring
    parser_expiring = subparsers.add_parser('expiring', help='Check for expiring credentials')
    parser_expiring.add_argument('--days', type=int, default=7, help='Days threshold')
    
    # rotate
    parser_rotate = subparsers.add_parser('rotate', help='Rotate a credential')
    parser_rotate.add_argument('key_name', help='Credential name')
    parser_rotate.add_argument('new_value', nargs='?', help='New value (or prompt if omitted)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Initialize store and audit logger
    store = Store()
    audit = AuditLogger()
    
    # Dispatch to command handler
    commands = {
        'init': cmd_init,
        'unlock': cmd_unlock,
        'lock': cmd_lock,
        'status': cmd_status,
        'add': cmd_add,
        'get': cmd_get,
        'list': cmd_list,
        'remove': cmd_remove,
        'env': cmd_env,
        'audit': cmd_audit,
        'expiring': cmd_expiring,
        'rotate': cmd_rotate,
    }
    
    handler = commands.get(args.command)
    if not handler:
        print(f"❌ Unknown command: {args.command}")
        return 1
    
    return handler(args, store, audit)


if __name__ == '__main__':
    sys.exit(main())
