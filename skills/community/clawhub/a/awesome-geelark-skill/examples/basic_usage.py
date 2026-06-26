#!/usr/bin/env python3
"""
Basic Usage Example - GeeLark API Skill

This example demonstrates basic operations:
1. List cloud phones
2. Check balance
3. Create cloud phone
4. Boot cloud phone and connect
5. Install app 
6. Stop cloud phone
"""

from scripts.geelark_boot_helper import list_cloud_phones, boot_and_connect
from scripts.geelark_client import GeeLarkClient


def main():
    # Initialize client
    print("🔧 Initializing GeeLark Client...")
    client = GeeLarkClient()

    # 1. Check balance
    print("\n[1] Checking account balance...")
    wallet = client.wallet()
    balance = wallet['data']['balance']
    gift_money = wallet['data'].get('giftMoney', 0)
    print(f"   Balance: ${balance:.2f}, Gift: ${gift_money:.2f}")

    if balance <= 0 and gift_money <= 0:
        print("   ❌ Insufficient balance!")
        return

    # 2. List cloud phones
    print("\n[2] Listing cloud phones...")
    phones = list_cloud_phones(client.token)
    print(f"   Found {len(phones)} cloud phone(s):")
    for phone in phones:
        status = 'Running' if phone['status'] == 0 else 'Stopped'
        print(f"   - {phone['serialName']} ({phone['id']}) - {phone['equipmentInfo']['osVersion']} - {status}")

    # 3. Create new cloud phone (commented out - requires Pro plan for batch)
    # print("\n[3] Creating new cloud phone...")
    # response = client.call("/open/v1/phone/addNew", {
    #     "mobileType": "Android 13",
    #     "data": [{"profileName": "TestPhone"}]
    # })
    # if response['code'] == 0:
    #     phone_id = response['data']['details'][0]['id']
    #     print(f"   ✅ Created: {phone_id}")
    # else:
    #     print(f"   ❌ Failed: {response}")
    #     return

    # Use existing phone for this example
    if phones:
        phone_id = phones[0]['id']
    else:
        print("   ❌ No cloud phones available")
        return

    # 4. Boot cloud phone and get ADB connection
    print(f"\n[4] Booting cloud phone {phone_id}...")
    token = client.token
    adb_info = boot_and_connect(phone_id, token)

    if not adb_info:
        print("   ❌ Boot failed")
        return

    print(f"   ✅ Connected: {adb_info['ip']}:{adb_info['port']}")

    # 5. Install app (commented out - requires app installation flow)
    # print("\n[5] Installing TikTok...")
    # response = client.call("/open/v1/app/installable/list", {
    #     "envId": phone_id,
    #     "name": "TikTok",
    #     "page": 1,
    #     "pageSize": 20
    # })
    # if response['code'] == 0 and response['data']['items']:
    #     app_version_id = response['data']['items'][0]['appVersionInfoList'][0]['id']
    #     response = client.call("/open/v1/app/install", {
    #         "envId": phone_id,
    #         "appVersionId": app_version_id
    #     })
    #     if response['code'] == 0:
    #         print("   ✅ TikTok installation started")
    #     else:
    #         print(f"   ❌ Installation failed: {response}")
    # else:
    #     print("   ❌ TikTok not found")

    # 6. Stop cloud phone
    print(f"\n[6] Stopping cloud phone {phone_id}...")
    response = client.phone_stop([phone_id])
    if response['code'] == 0:
        print("   ✅ Cloud phone stopped")
    else:
        print(f"   ❌ Stop failed: {response}")

    print("\n✅ Example completed!")


if __name__ == "__main__":
    main()