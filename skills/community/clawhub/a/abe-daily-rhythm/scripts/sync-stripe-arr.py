#!/usr/bin/env python3
"""
ARR Sync - Fetches active subscriptions and calculates ARR via SkillBoss API Hub
"""
import os
import json
import requests
import warnings
from datetime import datetime

# Suppress urllib3 SSL warning on macOS (LibreSSL vs OpenSSL)
warnings.filterwarnings('ignore', category=UserWarning, module='urllib3')

SKILLBOSS_API_KEY = os.environ.get("SKILLBOSS_API_KEY")
API_BASE = "https://api.heybossai.com/v1"

def pilot(body: dict) -> dict:
    r = requests.post(
        f"{API_BASE}/pilot",
        headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    return r.json()

def fetch_active_subscriptions():
    """Fetch all active subscriptions via SkillBoss shopping service admin API.

    Requires PROJECT_ID env var (get from .skillboss file after deploying with serve-build.js).
    The SkillBoss shopping service manages Stripe subscriptions; use its admin endpoint.
    """
    project_id = os.environ.get("SKILLBOSS_PROJECT_ID")
    if not SKILLBOSS_API_KEY:
        print("❌ No SKILLBOSS_API_KEY found")
        return None
    if not project_id:
        print("❌ No SKILLBOSS_PROJECT_ID found — deploy with serve-build.js first")
        return None

    try:
        r = requests.get(
            f"https://shopping.heybossai.com/admin-subscriptions?status=active&limit=100",
            headers={
                "Authorization": f"Bearer {SKILLBOSS_API_KEY}",
                "X-Project-ID": project_id,
            },
            timeout=60,
        )
        r.raise_for_status()
        return r.json().get("data", [])
    except Exception as e:
        print(f"❌ SkillBoss shopping service error: {e}")
        return None

def calculate_arr(subscriptions):
    """Calculate ARR from active subscriptions."""
    if not subscriptions:
        return 0, 0, []
    
    customer_subscriptions = {}
    
    for sub in subscriptions:
        customer = sub.get('customer')
        if isinstance(customer, dict):
            customer_id = customer.get('id')
        else:
            customer_id = customer
        
        if not customer_id:
            continue
        
        # Calculate subscription amount
        amount_cents = 0
        for item in sub.get('items', {}).get('data', []):
            amount_cents += item.get('price', {}).get('unit_amount', 0) * item.get('quantity', 1)
        
        amount_gbp = amount_cents / 100
        interval = sub.get('items', {}).get('data', [{}])[0].get('price', {}).get('recurring', {}).get('interval', 'month')
        
        if interval == 'month':
            annual_amount = amount_gbp * 12
        elif interval == 'year':
            annual_amount = amount_gbp
        elif interval == 'week':
            annual_amount = amount_gbp * 52
        else:
            annual_amount = amount_gbp * 12
        
        if customer_id in customer_subscriptions:
            customer_subscriptions[customer_id] += annual_amount
        else:
            customer_subscriptions[customer_id] = annual_amount
    
    total_arr = round(sum(customer_subscriptions.values()))
    customer_count = len(customer_subscriptions)
    
    return total_arr, customer_count, list(customer_subscriptions.keys())

def sync_stripe():
    """Main sync function."""
    subscriptions = fetch_active_subscriptions()
    if subscriptions is None:
        return False
    
    arr, customer_count, customer_ids = calculate_arr(subscriptions)
    
    # Save detailed data
    output_dir = '/Users/tom/.openclaw/workspace/memory'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'stripe-data.json')
    
    data = {
        'synced_at': datetime.now().isoformat(),
        'arr': arr,
        'customer_count': customer_count,
        'customer_ids': customer_ids,
        'subscription_count': len(subscriptions),
        'method': 'active_subscriptions_only'
    }
    
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    # Update heartbeat state
    heartbeat_path = os.path.join(output_dir, 'heartbeat-state.json')
    if os.path.exists(heartbeat_path):
        with open(heartbeat_path, 'r') as f:
            hb_data = json.load(f)
    else:
        hb_data = {}
    
    hb_data['arrCurrent'] = arr
    hb_data['customerCount'] = customer_count
    hb_data['arrLastSynced'] = datetime.now().isoformat()
    
    with open(heartbeat_path, 'w') as f:
        json.dump(hb_data, f, indent=2)
    
    print(f"✅ Updated ARR: £{arr:,} ({customer_count} active customers)")
    return True

if __name__ == '__main__':
    sync_stripe()
