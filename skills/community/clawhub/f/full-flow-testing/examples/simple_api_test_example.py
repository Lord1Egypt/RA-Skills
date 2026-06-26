#!/usr/bin/env python3
"""
Simple API test example.
This is a generic API testing template you can modify based on your business needs.
"""

import requests
import json

def test_api_endpoint():
    """Example test for an API endpoint."""
    
    print("="*60)
    print("🔧 Simple API Test Example")
    print("="*60)
    
    # Configure your API information
    base_url = "https://your-api-domain.com"  # Replace with your API domain
    endpoint = "/api/v1/test"                  # Replace with your endpoint path
    url = f"{base_url}{endpoint}"
    
    # Request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_TOKEN_HERE"  # If authentication is required
    }
    
    # Request payload (example)
    payload = {
        "param1": "value1",
        "param2": 123
    }
    
    print(f"\n📤 Sending request to: {url}")
    print(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        print(f"\n📥 Response status code: {response.status_code}")
        print(f"⏱️  Response time: {response.elapsed.total_seconds()*1000:.0f}ms")
        
        try:
            resp_json = response.json()
            print(f"\n📊 Response content:")
            print(json.dumps(resp_json, ensure_ascii=False, indent=2))
            
            # Simple assertion
            if response.status_code == 200:
                print(f"\n✅ Test passed!")
                return True
            else:
                print(f"\n❌ Test failed!")
                return False
                
        except Exception as e:
            print(f"⚠️  Failed to parse response: {e}")
            print(f"Response content: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"\n❌ Request error: {e}")
        return False

if __name__ == "__main__":
    test_api_endpoint()
