#!/usr/bin/env python3
"""
Test the fixed EPO data mapper
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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

from scripts.epo_data_mapper import EPODataMapper

print("🔍 Testing fixed EPO data mapper...")
try:
    mapper = EPODataMapper()
    patents = mapper.fetch_patents('pa=IBM', 1, 2)
    
    print(f"\n✅ Fetched {len(patents)} patents")
    
    for i, patent in enumerate(patents):
        print(f"\n=== Patent {i+1} ===")
        print(f"Patent ID: {patent.get('patent_id', 'N/A')}")
        print(f"Title: {patent.get('title', 'N/A')[:80]}...")
        print(f"Company: {patent.get('company', 'N/A')}")
        print(f"Publication Date: {patent.get('publication_date', 'N/A')}")
        print(f"Image URL: {patent.get('image_url', 'N/A')}")
        
        # Check if patent_id looks correct
        patent_id = patent.get('patent_id', '')
        if patent_id and patent_id != 'Unknown':
            if len(patent_id) > 8 and any(prefix in patent_id for prefix in ['US', 'EP', 'DE', 'WO']):
                print(f"✅ Patent ID format looks good: {patent_id}")
            else:
                print(f"⚠️  Patent ID format may be wrong: {patent_id}")
        
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()