#!/usr/bin/env python3
"""
Etsy Auto-Lister — creates digital products on Etsy.
Requires: ETSY_CLIENT_KEY, ETSY_CLIENT_SECRET (from developer.etsy.com)
Then: OAuth token via etsy-oauth-helper.py
API docs: https://developer.etsy.com/documentation/
"""

import os, json, requests, base64

ETSY_CLIENT_KEY = os.environ.get("ETSY_CLIENT_KEY", "")
ETSY_CLIENT_SECRET = os.environ.get("ETSY_CLIENT_SECRET", "")
ETSY_SHOP_ID = os.environ.get("ETSY_SHOP_ID", "")  # Your shop ID
BASE_URL = "https://api.etsy.com/v3"

# OAuth token (set manually after running oauth helper)
ETSY_ACCESS_TOKEN = os.environ.get("ETSY_ACCESS_TOKEN", "")

LISTINGS = [
    {
        "title": "Options Trading Brain — PDF Strategy Guide",
        "description": "Professional options trading brain system. Includes whale flow scanner setup, Elliott Wave analysis, liquidity map strategy, and 6-hour mean reversion system. Used by serious traders to identify high-probability setups. Instant digital delivery.",
        "price": 27.00,
        "tags": ["options trading", "trading strategy", "whale alert", " Elliott Wave", "finance"],
        "taxonomy_id": 1903,  # Finance > Investing
    },
    {
        "title": "DeFi Sniper Bot Setup Guide + Scripts",
        "description": "Complete DeFi sniper bot setup guide. Learn to trade new token launches, read whale flow, and build your own trading bots. Includes ready-to-use Python scripts and configuration templates. Digital delivery — download immediately.",
        "price": 37.00,
        "tags": ["defi", "crypto bot", "snipe bot", "solana", "trading bot", "smart contract"],
        "taxonomy_id": 1903,
    },
    {
        "title": "Smart Contract Audit Checklist — Developer Tool",
        "description": "Professional smart contract audit checklist used by blockchain developers. Covers 47-point security review, gas optimization checklist, and common vulnerability patterns. Used by auditors and DeFi teams worldwide.",
        "price": 47.00,
        "tags": ["smart contract", "audit", "blockchain", "security", "solidity", "developer tool"],
        "taxonomy_id": 1903,
    },
]

def get_headers():
    token = os.environ.get("ETSY_ACCESS_TOKEN", "")
    if not token:
        return {}
    return {
        "x-api-key": f"{ETSY_CLIENT_KEY}:{ETSY_CLIENT_SECRET}",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

def create_listing(listing):
    if not ETSY_ACCESS_TOKEN:
        print("❌ No ETSY_ACCESS_TOKEN. Run: python scripts/oauth_helper.py")
        return None
    
    if not ETSY_SHOP_ID:
        print("❌ No ETSY_SHOP_ID. Set ETSY_SHOP_ID in secrets.")
        return None
    
    payload = {
        "quantity": 999,
        "title": listing["title"],
        "description": listing["description"],
        "price": listing["price"],
        "who_made": "i_did",
        "when_made": "2020_2024",
        "taxonomy_id": listing.get("taxonomy_id", 1903),
        "shipping_profile_id": None,
        "is_supply": True,
        "state": "draft",
    }
    
    resp = requests.post(
        f"{BASE_URL}/applications/shops/{ETSY_SHOP_ID}/listings",
        headers=get_headers(),
        json=payload,
        timeout=15
    )
    
    if resp.status_code in (200, 201, 204):
        data = resp.json()
        listing_id = data.get("listing_id", data.get("listing", {}).get("listing_id", ""))
        print(f"  ✅ Created: {listing['title']} (ID: {listing_id})")
        return listing_id
    else:
        print(f"  ❌ {listing['title']}: {resp.status_code} — {resp.text[:150]}")
        return None

def main():
    print("🚀 Etsy Auto-Lister\n")
    
    if not ETSY_CLIENT_KEY:
        print("❌ Missing ETSY_CLIENT_KEY — go to developer.etsy.com, register app, save as secret")
        print("   Also need ETSY_CLIENT_SECRET and ETSY_ACCESS_TOKEN (OAuth)")
        print("\nSTEPS:")
        print("1. Go to https://www.etsy.com/developers")
        print("2. Register your app → get API key + secret")
        print("3. Save both as secrets: ETSY_CLIENT_KEY, ETSY_CLIENT_SECRET")
        print("4. Run: python scripts/oauth_helper.py to get access token")
        print("5. Then re-run this script\n")
        return
    
    created = 0
    for listing in LISTINGS:
        lid = create_listing(listing)
        if lid:
            created += 1
    print(f"\n✅ Created {created}/{len(LISTINGS)} listings (as drafts)")

if __name__ == "__main__":
    main()