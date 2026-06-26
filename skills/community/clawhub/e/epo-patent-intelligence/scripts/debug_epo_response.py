#!/usr/bin/env python3
"""
Debug script to check EPO API response structure
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
import base64
import json

# Load credentials
from dotenv import load_dotenv
load_dotenv('/root/.openclaw/workspace/skills/epo-patent-intelligence/.env')

consumer_key = os.environ.get('EPO_CONSUMER_KEY')
secret_key = os.environ.get('EPO_SECRET_KEY')

print(f"Consumer key: {consumer_key[:10]}...")
print(f"Secret key: {secret_key[:10]}...")

# Authenticate
auth_string = base64.b64encode(f"{consumer_key}:{secret_key}".encode()).decode()
headers = {
    'Authorization': f'Basic {auth_string}',
    'Content-Type': 'application/x-www-form-urlencoded'
}
data = {'grant_type': 'client_credentials'}

response = requests.post(
    'https://ops.epo.org/3.2/auth/accesstoken',
    headers=headers,
    data=data,
    timeout=30
)
response.raise_for_status()
token_data = response.json()
access_token = token_data.get('access_token')
print(f"Access token: {access_token[:20]}...")

# Make test request
headers = {
    'Authorization': f'Bearer {access_token}',
    'Accept': 'application/json'
}
params = {
    'q': 'pa=IBM',
    'Range': '1-2'
}

response = requests.get(
    'https://ops.epo.org/3.2/rest-services/published-data/search/biblio',
    headers=headers,
    params=params,
    timeout=30
)
response.raise_for_status()

# Save response for inspection
data = response.json()
with open('/tmp/epo_response.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Response saved to /tmp/epo_response.json")
print(f"Response keys: {list(data.keys())}")

# Check structure
if 'ops:world-patent-data' in data:
    world_data = data['ops:world-patent-data']
    print(f"world-patent-data keys: {list(world_data.keys())}")
    
    if 'ops:biblio-search' in world_data:
        biblio_search = world_data['ops:biblio-search']
        print(f"biblio-search keys: {list(biblio_search.keys())}")
        
        if 'ops:search-result' in biblio_search:
            search_result = biblio_search['ops:search-result']
            print(f"search-result type: {type(search_result)}")
            print(f"search-result keys: {list(search_result.keys()) if isinstance(search_result, dict) else 'Not a dict'}")
            
            if 'exchange-documents' in search_result:
                exchange_docs = search_result['exchange-documents']
                print(f"exchange-documents type: {type(exchange_docs)}")
                print(f"exchange-documents keys: {list(exchange_docs.keys()) if isinstance(exchange_docs, dict) else 'Not a dict'}")