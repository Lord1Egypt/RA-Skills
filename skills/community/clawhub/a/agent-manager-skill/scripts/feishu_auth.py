#!/usr/bin/env python3
"""
Feishu Authorization URL Generation and Polling Script
"""
import sys
import argparse
import requests
import json
import time
import os

DEVICE_CODE_FILE = "/tmp/feishu_device_code.txt"

def generate_url():
    try:
        resp = requests.post('https://accounts.feishu.cn/oauth/v1/app/registration',
            data={'action': 'begin', 'archetype': 'PersonalAgent', 'auth_method': 'client_secret', 'request_user_info': 'open_id'},
            headers={'Content-Type': 'application/x-www-form-urlencoded'})
        resp.raise_for_status()
        data = resp.json()
        
        device_code = data.get('device_code')
        user_code = data.get('user_code')
        
        if not device_code or not user_code:
            print("Error: Failed to get authorization codes.")
            return

        with open(DEVICE_CODE_FILE, "w") as f:
            f.write(device_code)

        url = f"https://open.feishu.cn/page/openclaw?user_code={user_code}"
        print(f"URL={url}")
        
    except Exception as e:
        print(f"Error generating URL: {e}")

def poll_result():
    if not os.path.exists(DEVICE_CODE_FILE):
        print("Error: No device code found. Please run 'generate' first.")
        return

    with open(DEVICE_CODE_FILE, "r") as f:
        device_code = f.read().strip()

    print("Polling Feishu for authorization result...")
    for i in range(20):
        try:
            resp = requests.post('https://accounts.feishu.cn/oauth/v1/app/registration',
                data={'action': 'poll', 'device_code': device_code},
                headers={'Content-Type': 'application/x-www-form-urlencoded'}, timeout=10)
            result = resp.json()
            
            if 'client_id' in result:
                app_id = result['client_id']
                app_secret = result['client_secret']
                print("\n✅ Authorization successful!")
                print(f"App ID: {app_id}")
                print(f"App Secret: {app_secret}")
                print("\nYou can now pass these credentials to the manage_agent.py script.")
                
                # Cleanup
                os.remove(DEVICE_CODE_FILE)
                if os.path.exists("/tmp/feishu_qr.png"):
                    os.remove("/tmp/feishu_qr.png")
                return
                
            print(f"Waiting... (Attempt {i+1}/20)")
            time.sleep(5)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(5)
            
    print("\n❌ Polling timeout. User may not have completed authorization.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["generate", "poll"])
    args = parser.parse_args()

    if args.action == "generate":
        generate_url()
    elif args.action == "poll":
        poll_result()
