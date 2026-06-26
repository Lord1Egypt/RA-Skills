#!/usr/bin/env python3
"""
Garmin CN → Global Sync Tool
Syncs activities from Garmin China to Garmin Global using local timestamps + distance to avoid duplicates.

Features:
- Retries failed records once in next sync
- Only syncs new records after last sync time
- Tracks failed records and sync state
"""
import os
import sys
import json
import io
import time
import argparse
import zipfile

import garth
from garth import configure, Client
from garth.sso import login

CONFIG_DIR = os.path.expanduser('~/.config/garmin-sync')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'credentials.json')
STATE_FILE = os.path.join(CONFIG_DIR, 'sync_state.json')
FAILED_FILE = os.path.join(CONFIG_DIR, 'failed_records.json')

def load_json(path, default=None):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return default

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def load_credentials():
    """Load credentials - supports same or different credentials for CN and Global"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            creds = json.load(f)
            # Backward compatibility: if only one email/password, use for both
            if 'email' in creds and 'password' in creds:
                return {
                    'email_cn': creds.get('email'),
                    'password_cn': creds.get('password'),
                    'email_global': creds.get('email'),
                    'password_global': creds.get('password')
                }
            return creds
    return None

def save_credentials(email_cn, password_cn, email_global=None, password_global=None):
    """Save credentials - supports same or different credentials for CN and Global"""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    creds = {
        'email_cn': email_cn,
        'password_cn': password_cn,
    }
    # If different credentials for Global
    if email_global and password_global:
        creds['email_global'] = email_global
        creds['password_global'] = password_global
    else:
        # Use same credentials
        creds['email_global'] = email_cn
        creds['password_global'] = password_cn
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(creds, f)
    os.chmod(CONFIG_FILE, 0o600)

def login_garmin(email, password, domain):
    configure(domain=domain)
    result = login(email, password)
    client = Client()
    client.oauth1_token, client.oauth2_token = result
    client.domain = domain
    return client

def get_all_activities(client, max_limit=5000):
    """Get all activities from Garmin"""
    activities = []
    start = 0
    limit = 100
    while start < max_limit:
        resp = client.connectapi('/activitylist-service/activities', params={'start': start, 'limit': limit})
        batch = resp.get('activityList', [])
        if not batch:
            break
        activities.extend(batch)
        start += limit
    return activities

def sync_activity(client_cn, client_int, activity):
    """Sync a single activity from CN to Global"""
    act_id = activity.get('activityId')
    
    # Download from CN (returns zip file)
    fit_url = f"/download-service/files/activity/{act_id}"
    fit_zip = client_cn.download(fit_url)
    
    # Save zip to temp file
    zip_path = f'/tmp/garmin_sync_{act_id}.zip'
    with open(zip_path, 'wb') as f:
        f.write(fit_zip)
    
    # Extract
    with zipfile.ZipFile(zip_path, 'r') as z:
        fit_filename = [n for n in z.namelist() if n.endswith('.fit')][0]
        fit_data = z.read(fit_filename)
    
    os.remove(zip_path)
    
    # Upload to Global
    fit_file = io.BytesIO(fit_data)
    fit_file.name = f'activity_{act_id}.fit'
    
    result = client_int.upload(fit_file)
    return result['detailedImportResult']['uploadId']

def sync(email_cn, password_cn, email_global=None, password_global=None, new_only=False):
    """Main sync function
    
    Args:
        email_cn: Garmin China email
        password_cn: Garmin China password
        email_global: Garmin Global email (optional, defaults to CN credentials)
        password_global: Garmin Global password (optional, defaults to CN credentials)
        new_only: If True, only sync records newer than last sync time
    """
    # Use CN credentials for Global if not specified
    if not email_global:
        email_global = email_cn
    if not password_global:
        password_global = password_cn
    
    client_cn = login_garmin(email_cn, password_cn, 'garmin.cn')
    client_int = login_garmin(email_global, password_global, 'garmin.com')
    
    # Load state
    state = load_json(STATE_FILE, {'last_sync': None, 'last_activity_time': None})
    failed_records = load_json(FAILED_FILE, {})
    
    # Get CN activities
    cn_activities = get_all_activities(client_cn)
    
    # Get Global activities
    int_activities = get_all_activities(client_int)
    
    # Use startTimeLocal + distance as unique key
    int_keys = set((a.get('startTimeLocal'), a.get('distance')) for a in int_activities)
    
    # Get last sync time
    last_sync = state.get('last_activity_time')
    
    # Step 1: Retry failed records (only once each)
    retry_keys = list(failed_records.keys())
    
    retry_success = 0
    for key in retry_keys:
        activity = failed_records[key]
        date = activity.get('startTimeLocal', 'Unknown')
        dist = (activity.get('distance', 0) / 1000) if activity.get('distance') else 0
        print(f"Retrying: {date} | {dist:.2f}km", end=' ... ')
        
        try:
            new_id = sync_activity(client_cn, client_int, activity)
            print(f"✓ Success! Global ID: {new_id}")
            del failed_records[key]
            retry_success += 1
        except Exception as e:
            err_msg = str(e)[:30]
            print(f"✗ Failed again: {err_msg}")
            # Remove from failed - don't retry anymore
            del failed_records[key]
        
        time.sleep(1)
    
    # Save updated failed records
    save_json(FAILED_FILE, failed_records)
    
    # Step 2: Sync new records
    # Filter activities
    if new_only and last_sync:
        to_sync = [a for a in cn_activities 
                   if a.get('startTimeLocal') > last_sync 
                   and (a.get('startTimeLocal'), a.get('distance')) not in int_keys]
    else:
        to_sync = [a for a in cn_activities 
                   if (a.get('startTimeLocal'), a.get('distance')) not in int_keys]
    
    # If nothing to retry and nothing to sync, exit silently (no output = no notification)
    if len(to_sync) == 0 and retry_success == 0 and len(retry_keys) == 0:
        sys.exit(0)
    
    # Now print progress - only if there's something to do
    print(f"\n=== Garmin Sync ===")
    if retry_keys:
        print(f"Retrying {len(retry_keys)} failed records")
    
    failed = 0
    synced = 0
    latest_time = last_sync
    
    for i, a in enumerate(to_sync):
        act_id = a.get('activityId')
        date = a.get('startTimeLocal')
        dist = (a.get('distance', 0) / 1000) if a.get('distance') else 0
        
        # Track latest activity time
        if not latest_time or date > latest_time:
            latest_time = date
        
        print(f"[{i+1}/{len(to_sync)}] {date} | {dist:.2f}km", end=' ... ')
        
        try:
            new_id = sync_activity(client_cn, client_int, a)
            print(f"✓ {new_id}")
            synced += 1
        except Exception as e:
            err_msg = str(e)[:50]
            print(f"✗ {err_msg}")
            # Track failed for next retry
            key = (date, a.get('distance'))
            failed_records[str(key)] = a
            failed += 1
        
        time.sleep(1)
    
    # Save failed records
    save_json(FAILED_FILE, failed_records)
    
    # If nothing to sync and no retries, exit silently (no output = no notification)
    if synced == 0 and retry_success == 0 and failed == 0:
        sys.exit(0)
    
    # Update state
    state['last_sync'] = time.strftime('%Y-%m-%d %H:%M:%S')
    state['last_activity_time'] = latest_time
    save_json(STATE_FILE, state)
    
    # Always output in English
    print(f"\n=== Garmin Sync Done ===")
    print(f"Retried: {retry_success}")
    print(f"Synced: {synced}")
    print(f"Failed: {failed}")
    print(f"Last activity time: {latest_time}")

def main():
    parser = argparse.ArgumentParser(description='Garmin CN → Global Sync')
    parser.add_argument('--new-only', action='store_true', help='Only sync records newer than last sync')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Sync command
    sync_parser = subparsers.add_parser('sync', help='Sync activities from CN to Global')
    sync_parser.add_argument('--new-only', action='store_true', help='Only sync new records since last sync')
    
    # Set credentials command
    cred_parser = subparsers.add_parser('set-credentials', help='Set credentials')
    cred_parser.add_argument('--email-cn', required=True, help='Garmin China email')
    cred_parser.add_argument('--password-cn', required=True, help='Garmin China password')
    cred_parser.add_argument('--email-global', help='Garmin Global email (optional, defaults to CN)')
    cred_parser.add_argument('--password-global', help='Garmin Global password (optional, defaults to CN)')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show sync status')
    
    args = parser.parse_args()
    
    if args.command == 'set-credentials':
        save_credentials(args.email_cn, args.password_cn, args.email_global, args.password_global)
        print("Credentials saved!")
        if args.email_global:
            print(f"  CN: {args.email_cn}")
            print(f"  Global: {args.email_global}")
        else:
            print(f"  (Using same credentials for both)")
    
    elif args.command == 'sync':
        creds = load_credentials()
        if not creds:
            print("No credentials found. Run: garmin-sync set-credentials --email-cn YOUR_EMAIL --password-cn YOUR_PASSWORD")
            sys.exit(1)
        
        sync(
            creds['email_cn'], 
            creds['password_cn'], 
            creds.get('email_global'),
            creds.get('password_global'),
            new_only=args.new_only
        )
    
    elif args.command == 'status':
        state = load_json(STATE_FILE, {})
        failed = load_json(FAILED_FILE, {})
        print("=== Sync Status ===")
        print(f"Last sync: {state.get('last_sync', 'Never')}")
        print(f"Last activity time: {state.get('last_activity_time', 'Unknown')}")
        print(f"Failed records (will retry): {len(failed)}")
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
