#!/usr/bin/env python3
"""
Verify Feishu bot bindings in openclaw.json
"""
import json

CONFIG_PATH = f"{os.path.expanduser('~')}/.openclaw/openclaw.json"

def verify_bindings():
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
        
        feishu_config = config.get('channels', {}).get('feishu', {})
        bindings = feishu_config.get('bindings', {})
        accounts = feishu_config.get('accounts', {})
        
        print("🔍 Current Feishu Bot Bindings:")
        print("-" * 50)
        
        if not bindings:
            print("No bindings found.")
            return

        for account_id, agent_id in bindings.items():
            app_id = accounts.get(account_id, {}).get('appId', '❌ Missing')
            print(f"Account: {account_id}")
            print(f"  └─ App ID: {app_id}")
            print(f"  └─ Agent:  {agent_id}")
            print()
            
    except Exception as e:
        print(f"Error reading config: {e}")

if __name__ == "__main__":
    verify_bindings()
