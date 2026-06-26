#!/usr/bin/env python3
"""
Debug script to examine EPO API response structure
"""

import sys
import os
import json
import base64
import requests

# Load environment variables
env_path = '/root/.openclaw/workspace/skills/epo-patent-intelligence/.env'
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if 'export ' in line:
                    line = line.replace('export ', '')
                if '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")

consumer_key = os.environ.get('EPO_CONSUMER_KEY')
secret_key = os.environ.get('EPO_SECRET_KEY')

if not consumer_key or not secret_key:
    print("❌ Missing credentials")
    sys.exit(1)

# Authenticate
auth_string = base64.b64encode(f"{consumer_key}:{secret_key}".encode()).decode()
headers = {
    'Authorization': f'Basic {auth_string}',
    'Content-Type': 'application/x-www-form-urlencoded'
}
data = {'grant_type': 'client_credentials'}

print("🔍 Authenticating...")
response = requests.post(
    'https://ops.epo.org/3.2/auth/accesstoken',
    headers=headers,
    data=data,
    timeout=30
)
response.raise_for_status()
token_data = response.json()
access_token = token_data.get('access_token')

# Make a simple request
headers = {
    'Authorization': f'Bearer {access_token}',
    'Accept': 'application/json'
}

params = {
    'q': 'pa=IBM',
    'Range': '1-1'
}

print("🔍 Fetching patent data...")
response = requests.get(
    'https://ops.epo.org/3.2/rest-services/published-data/search/biblio',
    headers=headers,
    params=params,
    timeout=30
)
response.raise_for_status()

data = response.json()
print("\n=== RAW RESPONSE STRUCTURE ===")
print(json.dumps(data, indent=2)[:2000])  # First 2000 chars

# Look for publication reference
print("\n=== LOOKING FOR PUBLICATION REFERENCE ===")
try:
    # Navigate to search results
    search_results = data.get('ops:world-patent-data', {}).get('ops:biblio-search', {}).get('ops:search-result', {})
    print(f"Search results type: {type(search_results)}")
    
    exchange_docs = search_results.get('exchange-documents', [])
    print(f"Exchange docs type: {type(exchange_docs)}")
    
    if isinstance(exchange_docs, list) and len(exchange_docs) > 0:
        first_doc = exchange_docs[0]
        print(f"First exchange doc type: {type(first_doc)}")
        
        if isinstance(first_doc, dict):
            exchange_document = first_doc.get('exchange-document', [])
            print(f"Exchange document type: {type(exchange_document)}")
            
            if isinstance(exchange_document, list) and len(exchange_document) > 0:
                doc = exchange_document[0]
                print(f"\n=== SINGLE PATENT DOC ===")
                print(json.dumps(doc, indent=2)[:1500])
                
                # Look for publication reference
                biblio = doc.get('bibliographic-data', {})
                pub_ref = biblio.get('publication-reference', {})
                print(f"\n=== PUBLICATION REFERENCE ===")
                print(json.dumps(pub_ref, indent=2))
                
                # Look for document-id list
                doc_ids = pub_ref.get('document-id', [])
                print(f"\n=== DOCUMENT IDs ({len(doc_ids)}) ===")
                for i, doc_id in enumerate(doc_ids):
                    print(f"\nDocument ID {i}:")
                    print(json.dumps(doc_id, indent=2))
                    
                    # Check document-id-type
                    doc_type = doc_id.get('@document-id-type', 'unknown')
                    doc_number = doc_id.get('doc-number', {})
                    if isinstance(doc_number, dict):
                        doc_number_val = doc_number.get('$', 'N/A')
                    else:
                        doc_number_val = str(doc_number)
                    
                    print(f"  Type: {doc_type}")
                    print(f"  Number: {doc_number_val}")
                    
                    # Check for country code
                    country = doc_id.get('country', {})
                    if isinstance(country, dict):
                        country_code = country.get('$', 'N/A')
                    else:
                        country_code = str(country)
                    print(f"  Country: {country_code}")
                    
                    # Check for kind code
                    kind = doc_id.get('kind', {})
                    if isinstance(kind, dict):
                        kind_code = kind.get('$', 'N/A')
                    else:
                        kind_code = str(kind)
                    print(f"  Kind: {kind_code}")
                    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()