#!/usr/bin/env python3
"""
Create Cloud Phone Script for GeeLark

This script handles cloud phone creation with proper proxy configuration.
Key requirement: Use 'proxyNumber' (proxy serial number), NOT 'proxyId'.

Usage:
    python3 create_phone.py --profile "MyPhone" --os "Android 15"
    python3 create_phone.py --profile "Phone1" --os "Android 14" --proxy 10

Error 45006 - Wrong Argument:
    - Common cause: Using proxyId instead of proxyNumber
    - Solution: Use proxy serial number (proxyNumber) from proxy list
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.geelark_client import GeeLarkClient

# Constants
DEFAULT_OUTPUT_PATH = Path.home() / '.geelark' / 'last_created_phone_id.txt'
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
PROFILE_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9_-]{1,50}$')


def mask_sensitive(value, visible_chars=3, mask_char='*'):
    """Mask sensitive information, showing only first few characters."""
    if not value or value == 'N/A':
        return value
    value_str = str(value)
    if len(value_str) <= visible_chars:
        return mask_char * len(value_str)
    return value_str[:visible_chars] + mask_char * (len(value_str) - visible_chars)


def list_proxies(client, show_details=False):
    """List available proxies and return proxy list."""
    print("🔍 Querying available proxies...")

    response = client.call('/open/v1/proxy/list', {'page': 1, 'pageSize': 50})

    if response.get('code') == 0:
        proxies = response['data'].get('list', [])
        print(f"✅ Found {len(proxies)} proxy(ies):")
        for proxy in proxies:
            serial_no = proxy['serialNo']
            if show_details:
                print(f"   Serial No {serial_no}: {proxy['scheme']}://{proxy['server']}:{proxy['port']}")
            else:
                # Mask sensitive proxy info
                server_masked = mask_sensitive(proxy['server'], visible_chars=2)
                print(f"   Serial No {serial_no}: {proxy['scheme']}://{server_masked}:{proxy['port']}")
        return proxies
    else:
        print(f"❌ Failed to list proxies: {response.get('msg', 'Unknown error')}")
        return []


def create_cloud_phone(profile_name, os_version="Android 15", proxy_number=None, auto_start=False, output_path=None, show_details=False, energy_saving_mode=1):
    """
    Create a new cloud phone.

    Args:
        profile_name: Name for the cloud phone
        os_version: Android version (default: Android 15)
        proxy_number: Proxy serial number (optional, will prompt to select if not provided)
        auto_start: Whether to start the phone after creation (default: False)
        output_path: Path to save phone ID (default: ~/.geelark/last_created_phone_id.txt)
        show_details: Whether to show full sensitive details (default: False)
        energy_saving_mode: Energy saving mode (default: 1)

    Returns:
        dict: Phone information or None if failed
    """
    if output_path is None:
        output_path = DEFAULT_OUTPUT_PATH

    # Validate profile name
    if not PROFILE_NAME_PATTERN.match(profile_name):
        print(f"❌ Invalid profile name: '{profile_name}'")
        print(f"   Must match pattern: {PROFILE_NAME_PATTERN.pattern}")
        print(f"   Allowed: alphanumeric, hyphen, underscore (1-50 chars)")
        return None

    client = GeeLarkClient(task_name='create_phone', phone_id='batch')

    # Get proxies
    proxies = list_proxies(client, show_details=show_details)

    if not proxies:
        print("❌ No proxies available. Cannot create cloud phone.")
        return None

    # Auto-select proxy if not provided
    if proxy_number is None:
        # Show available proxies and prompt for selection
        print("\n⚠️  No proxy specified. Available proxies:")
        for i, proxy in enumerate(proxies, 1):
            serial_no = proxy['serialNo']
            server_masked = mask_sensitive(proxy['server'], visible_chars=2)
            print(f"   {i}. Serial No {serial_no}: {proxy['scheme']}://{server_masked}:{proxy['port']}")
        
        print(f"\n� Auto-selecting first proxy (Serial No {proxies[0]['serialNo']})")
        print(f"   Use --proxy <serial_no> to specify a different proxy")
        proxy_number = proxies[0]['serialNo']

    # Validate proxy_number
    proxy_exists = any(str(p['serialNo']) == str(proxy_number) for p in proxies)
    if not proxy_exists:
        print(f"❌ Proxy Serial No {proxy_number} not found!")
        print(f"   Available proxy serial numbers: {[p['serialNo'] for p in proxies]}")
        return None

    # Create phone with proxyNumber (NOT proxyId!)
    print(f"\n🚀 Creating cloud phone: {profile_name}")
    print(f"   OS: {os_version}")
    print(f"   Proxy Serial No: {proxy_number}")

    # Retry mechanism for API call
    response = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.call('/open/v1/phone/addNew', {
                'mobileType': os_version,
                'data': [{
                    'profileName': profile_name,
                    'proxyNumber': proxy_number  # CRITICAL: Use proxyNumber, not proxyId
                }]
            })
            break  # Success, exit retry loop
        except Exception as e:
            print(f"⚠️  Attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                wait_time = RETRY_DELAY * attempt
                print(f"   Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"❌ All {MAX_RETRIES} attempts failed")
                return None

    if response is None:
        print("❌ No response from API")
        return None

    # Check response
    if response.get('code') == 0 and response.get('data', {}).get('successAmount', 0) > 0:
        # Phone details are in the first item of details array
        phone_detail = response['data']['details'][0]
        phone_id = phone_detail['id']
        phone_name = phone_detail.get('profileName', profile_name)

        print(f"\n✅ Cloud phone created successfully!")
        print(f"   ID: {phone_id}")
        print(f"   Name: {phone_name}")
        print(f"   Serial No: {phone_detail.get('envSerialNo', 'N/A')}")
        print(f"   Device: {phone_detail.get('equipmentInfo', {}).get('deviceBrand', 'N/A')} {phone_detail.get('equipmentInfo', {}).get('deviceModel', 'N/A')}")
        print(f"   OS: {phone_detail.get('equipmentInfo', {}).get('osVersion', 'N/A')}")
        print(f"   Country: {phone_detail.get('equipmentInfo', {}).get('countryName', 'N/A')}")
        
        # Mask sensitive phone number
        phone_number = phone_detail.get('equipmentInfo', {}).get('phoneNumber', 'N/A')
        if show_details:
            print(f"   Phone: {phone_number}")
        else:
            print(f"   Phone: {mask_sensitive(phone_number)}")

        # Save phone ID to file with restricted permissions
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(phone_id)
        # Set file permissions to owner read/write only (600)
        os.chmod(output_path, 0o600)
        print(f"📝 Phone ID saved to {output_path} (permissions: 600)")

        # Build phone info dict
        phone_info = {
            'id': phone_id,
            'profileName': phone_name,
            'envSerialNo': phone_detail.get('envSerialNo'),
            'equipmentInfo': phone_detail.get('equipmentInfo', {})
        }

        # Auto-start if requested
        if auto_start:
            print(f"\n🔄 Starting cloud phone...")
            start_response = client.call('/open/v1/phone/start', {
                'ids': [phone_id],
                'energySavingMode': energy_saving_mode  # Enable energy saving to save costs
            })

            if start_response.get('code') == 0 and start_response.get('data', {}).get('successAmount', 0) > 0:
                access_url = start_response['data']['successDetails'][0]['url']
                print(f"✅ Cloud phone started!")
                print(f"\\n🔗 Access URL:")
                print(f"   {access_url}")
                phone_info['access_url'] = access_url
            else:
                print(f"❌ Failed to start phone")

        # Save log
        client.save_log()
        
        return phone_info

    else:
        # Failed - show error details
        details = response.get('data', {}).get('details', [{}])[0]
        error_code = details.get('code', 'Unknown')
        error_msg = details.get('msg', 'Unknown error')

        print(f"\n❌ Failed to create cloud phone")
        print(f"   Error Code: {error_code}")
        print(f"   Error Message: {error_msg}")

        # Save log even on failure
        client.save_log()

        # Provide helpful hints for common errors
        if error_code == 45006:
            print(f"\n💡 Hint: Error 45006 = 'Wrong Argument'")
            print(f"   - Check that proxyNumber is correct")
            print(f"   - proxyNumber should be an integer, not a string")
            print(f"   - Available proxy serial numbers: {[p['serialNo'] for p in proxies]}")
        elif error_code == 47002:
            print(f"\n💡 Hint: Error 47002 = 'Cloud phone resource shortage'")
            print(f"   - Try again later")
            print(f"   - Check your account package limits")
        else:
            print(f"\n💡 Tip: Check {Path.home() / '.geelark' / 'logs' / 'cloudphone'} for detailed logs")

        return None


def main():
    parser = argparse.ArgumentParser(
        description='Create a GeeLark cloud phone',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create phone with auto-selected proxy
  python3 create_phone.py --profile "MyPhone" --os "Android 15"

  # Create phone with specific proxy
  python3 create_phone.py --profile "Phone1" --os "Android 14" --proxy 10

  # Create and auto-start
  python3 create_phone.py --profile "TestPhone" --os "Android 15" --auto-start

  # Create multiple phones
  for i in range(1, 6); do
      python3 create_phone.py --profile "Phone_${i}" --os "Android 15"
  done
        """
    )

    parser.add_argument('--profile', required=True, help='Profile name for the cloud phone (alphanumeric, hyphen, underscore, 1-50 chars)')
    parser.add_argument('--os', default='Android 15', help='Android version (default: Android 15)')
    parser.add_argument('--proxy', type=int, help='Proxy serial number (auto-selects first if not provided)')
    parser.add_argument('--auto-start', action='store_true', help='Start the phone after creation')
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT_PATH,
                       help=f'Path to save phone ID (default: {DEFAULT_OUTPUT_PATH})')
    parser.add_argument('--show-details', action='store_true', help='Show full sensitive details (phone numbers, proxy servers)')
    parser.add_argument('--energy-saving', type=int, default=1, choices=[0, 1],
                       help='Energy saving mode: 0=off, 1=on (default: 1)')

    args = parser.parse_args()

    # Create phone
    phone = create_cloud_phone(
        profile_name=args.profile,
        os_version=args.os,
        proxy_number=args.proxy,
        auto_start=args.auto_start,
        output_path=args.output,
        show_details=args.show_details,
        energy_saving_mode=args.energy_saving
    )

    if phone:
        print(f"\n✅ Done! Phone ID saved to {args.output}")
        sys.exit(0)
    else:
        print(f"\n❌ Failed to create cloud phone")
        sys.exit(1)


if __name__ == '__main__':
    main()