#!/usr/bin/env python3
"""
GeeLark Cloud Phone - App Installer

Installs apps on cloud phones using appVersionId (NOT appName).
Automatically selects the best candidate and avoids ambiguous matches.

Usage:
    python scripts/install_app.py --phone-id <phone_id> --name TikTok
    python scripts/install_app.py --phone-id <phone_id> --name TikTok --exclude Lite
    python scripts/install_app.py --phone-id <phone_id> --name Instagram --version-id <appVersionId>
"""

import sys
import os
import json
import argparse
from typing import Optional, List, Dict

# Add project root to path
_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_script_dir)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from scripts.geelark_client import GeeLarkClient
from scripts.utils import get_token, get_base_url


# ============================================
# App Installer
# ============================================
def find_app(client: GeeLarkClient, phone_id: str, name: str, exclude: Optional[str] = None) -> Optional[Dict]:
    """
    Find app by name and return the best match.
    
    Args:
        client: GeeLarkClient instance
        phone_id: Cloud phone ID
        name: App name to search for (e.g., "TikTok")
        exclude: Optional keyword to exclude (e.g., "Lite")
    
    Returns:
        dict with app info or None
    """
    print(f"  🔍 Searching for app: {name}", flush=True)
    if exclude:
        print(f"  🚫 Excluding: {exclude}", flush=True)
    
    try:
        response = client.call("/open/v1/app/installable/list", {
            "envId": phone_id,
            "name": name,
            "page": 1,
            "pageSize": 20
        })
        
        if response.get('code') != 0:
            print(f"  ❌ Search failed: {response.get('msg', 'Unknown error')}", flush=True)
            return None
        
        items = response.get('data', {}).get('items', [])
        
        if not items:
            print(f"  ❌ No apps found matching '{name}'", flush=True)
            return None
        
        print(f"  📦 Found {len(items)} candidate(s):", flush=True)
        
        # Filter and display candidates
        candidates = []
        for i, item in enumerate(items, 1):
            app_name = item.get('appName', item.get('name', 'N/A'))
            
            # Skip if matches exclude keyword
            if exclude and exclude.lower() in app_name.lower():
                print(f"  {i}. ❌ {app_name} (excluded)", flush=True)
                continue
            
            # Check for appVersionInfoList
            version_info = item.get('appVersionInfoList', [])
            if not version_info:
                print(f"  {i}. ⚠️  {app_name} (no version info)", flush=True)
                continue

            # Sort by versionCode descending, take the highest version as latest
            sorted_versions = sorted(version_info, key=lambda v: v.get('versionCode', 0), reverse=True)
            latest_version = sorted_versions[0]
            app_version_id = latest_version.get('id')
            version_name = latest_version.get('versionName', 'N/A')
            
            candidates.append({
                'name': app_name,
                'appVersionId': app_version_id,
                'versionName': version_name,
                'item': item
            })
            
            print(f"  {i}. ✅ {app_name} (v{version_name}, ID: {app_version_id})", flush=True)
        
        if not candidates:
            print(f"  ❌ No valid candidates after filtering", flush=True)
            return None
        
        # If only one candidate, auto-select
        if len(candidates) == 1:
            selected = candidates[0]
            print(f"\n  ✅ Auto-selected: {selected['name']} v{selected['versionName']}", flush=True)
            return selected

        # Multiple candidates - error out, don't guess
        print(f"\n  ❌ Multiple candidates found ({len(candidates)}), cannot auto-select:", flush=True)
        for c in candidates:
            print(f"     - {c['name']} v{c['versionName']} (ID: {c['appVersionId']})", flush=True)
        print(f"\n  💡 Resolve ambiguity by:", flush=True)
        print(f"     1. Using --exclude to filter: --exclude Lite", flush=True)
        print(f"     2. Using a more specific --name: --name 'TikTok(Asia)'", flush=True)
        print(f"     3. Providing direct --version-id: --version-id <appVersionId>", flush=True)
        return None
    
    except Exception as e:
        print(f"  ❌ Error searching for app: {e}", flush=True)
        return None


def install_app(client: GeeLarkClient, phone_id: str, app_version_id: str) -> bool:
    """
    Install app using appVersionId.
    
    Args:
        client: GeeLarkClient instance
        phone_id: Cloud phone ID
        app_version_id: App version ID to install
    
    Returns:
        True if successful, False otherwise
    """
    print(f"  📦 Installing app (version ID: {app_version_id})...", flush=True)
    
    try:
        response = client.call("/open/v1/app/install", {
            "envId": phone_id,
            "appVersionId": app_version_id
        })
        
        if response.get('code') == 0:
            print(f"  ✅ Install task created successfully", flush=True)
            
            # Check if there's a taskId for tracking
            data = response.get('data', {})
            task_id = data.get('taskId')
            if task_id:
                print(f"  📋 Task ID: {task_id}", flush=True)
                print(f"  💡 Track progress with: client.call('/open/v1/task/detail', {{'taskId': '{task_id}'}})", flush=True)
            
            return True
        else:
            print(f"  ❌ Install failed: {response.get('msg', 'Unknown error')}", flush=True)
            return False
    
    except Exception as e:
        print(f"  ❌ Error installing app: {e}", flush=True)
        return False


# ============================================
# Main CLI
# ============================================
def main():
    parser = argparse.ArgumentParser(
        description="GeeLark Cloud Phone - App Installer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search and install TikTok
  python scripts/install_app.py --phone-id <phone_id> --name TikTok

  # Exclude TikTok Lite
  python scripts/install_app.py --phone-id <phone_id> --name TikTok --exclude Lite

  # Install specific version
  python scripts/install_app.py --phone-id <phone_id> --name Instagram --version-id <appVersionId>
        """
    )
    
    parser.add_argument("--phone-id", required=True, help="Cloud phone ID")
    parser.add_argument("--name", required=True, help="App name to search for")
    parser.add_argument("--exclude", help="Keyword to exclude from results (e.g., 'Lite')")
    parser.add_argument("--version-id", help="Direct appVersionId (skip search)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("📱 GeeLark Cloud Phone - App Installer")
    print("=" * 70)
    print(f"  Phone ID:    {args.phone_id}")
    print(f"  App Name:    {args.name}")
    print(f"  Exclude:     {args.exclude or 'None'}")
    print(f"  Version ID:  {args.version_id or 'Auto-select'}")
    print("=" * 70)
    
    # Initialize client
    try:
        client = GeeLarkClient(task_name="install_app", phone_id=args.phone_id)
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}", flush=True)
        sys.exit(1)
    
    # Install using direct version ID or search
    if args.version_id:
        # Direct install
        print(f"\n📦 Installing app with version ID: {args.version_id}", flush=True)
        success = install_app(client, args.phone_id, args.version_id)
    else:
        # Search and install
        app_info = find_app(client, args.phone_id, args.name, args.exclude)
        
        if not app_info:
            print(f"\n❌ No app found matching '{args.name}'", flush=True)
            sys.exit(1)
        
        print(f"\n📦 Installing: {app_info['name']} v{app_info['versionName']}", flush=True)
        success = install_app(client, args.phone_id, app_info['appVersionId'])
    
    # Summary
    print("\n" + "=" * 70)
    if success:
        print("✅ App install task created successfully")
        print("💡 Note: Installation runs asynchronously. Check phone status to verify.")
    else:
        print("❌ App install failed")
    print("=" * 70)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
