#!/usr/bin/env python3
"""
Test Everything HTTP API endpoints.
"""

import urllib.request
import json

PORT = 2853
BASE = f"http://127.0.0.1:{PORT}"

print("=" * 60)
print("Testing Everything API Endpoints")
print("=" * 60)
print()

# Test endpoints
endpoints = [
    ("/", "Base URL"),
    ("/?search=test&json=1", "Search API"),
    ("/?search=数据资产&json=1", "Chinese Search"),
    ("/?search=test&json=1&size=1", "Search with Size"),
]

for endpoint, description in endpoints:
    url = BASE + endpoint
    print(f"Testing: {description}")
    print(f"  URL: {endpoint}")
    
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        with urllib.request.urlopen(req, timeout=5) as response:
            print(f"  Status: {response.status}")
            
            # Parse JSON if applicable
            if "json=1" in endpoint:
                data = json.loads(response.read().decode())
                if "totalResults" in data:
                    print(f"  Results: {data.get('totalResults', 0)}")
                print(f"  ✓ Success")
            else:
                print(f"  ✓ Success")
                
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    print()

print("=" * 60)
print("Test Complete!")
print("=" * 60)
