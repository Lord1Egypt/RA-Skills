#!/usr/bin/env python3
"""Build financial inventory for divorce."""
import json
import os
import uuid
import argparse
from datetime import datetime

DIVORCE_DIR = os.path.expanduser("~/.openclaw/workspace/memory/divorce")

def ensure_dir():
    os.makedirs(DIVORCE_DIR, exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description='Build financial inventory')
    parser.add_argument('--type', required=True, 
                        choices=['asset', 'debt', 'account', 'property', 'retirement'],
                        help='Type of financial item')
    parser.add_argument('--description', required=True, help='Description')
    parser.add_argument('--value', type=float, help='Current value')
    parser.add_argument('--joint', action='store_true', help='Jointly owned')
    
    args = parser.parse_args()
    
    item_id = f"FIN-{str(uuid.uuid4())[:6].upper()}"
    
    item = {
        "id": item_id,
        "type": args.type,
        "description": args.description,
        "value": args.value,
        "joint": args.joint,
        "added_at": datetime.now().isoformat()
    }
    
    # Load and save
    inventory_file = os.path.join(DIVORCE_DIR, "financial_inventory.json")
    data = {"items": []}
    if os.path.exists(inventory_file):
        with open(inventory_file, 'r') as f:
            data = json.load(f)
    
    data['items'].append(item)
    
    ensure_dir()
    with open(inventory_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Financial item logged: {item_id}")
    print(f"  Type: {args.type}")
    print(f"  Description: {args.description}")
    if args.value:
        print(f"  Value: ${args.value:,.2f}")
    print(f"  Joint: {'Yes' if args.joint else 'No'}")
    
    # Count totals
    total_items = len(data['items'])
    print(f"\n📊 Inventory: {total_items} items logged")

if __name__ == '__main__':
    main()
