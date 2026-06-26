#!/usr/bin/env python3
"""
Re-fetch all patents with correct patent ID format
"""

import sys
import os
import sqlite3
from datetime import datetime

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
from scripts.database_manager import DatabaseManager

def refetch_patents():
    """Clear database and re-fetch patents with correct format."""
    print("🔍 Re-fetching patents with correct patent ID format...")
    
    # Create mapper and database manager
    mapper = EPODataMapper()
    db = DatabaseManager()
    
    # Clear existing patents
    print("  Clearing existing patents...")
    conn = sqlite3.connect('data/patents.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patents")
    conn.commit()
    conn.close()
    
    print("  Database cleared")
    
    # Define queries to fetch (based on what was previously collected)
    queries = [
        'pa=IBM',
        'pa=Microsoft', 
        'pa=TRUMPF',
        'pa=OKUMA',
        'pa="YAMAZAKI MAZAK"',
        'pa=HAAS'
    ]
    
    total_patents = 0
    
    for query in queries:
        print(f"\n  Fetching: {query}")
        try:
            patents = mapper.fetch_patents(query, 1, 10)  # Fetch up to 10 per query
            print(f"    Fetched {len(patents)} patents")
            
            # Save to database
            for patent in patents:
                db.save_patent(patent)
                total_patents += 1
                
        except Exception as e:
            print(f"    ⚠️ Error fetching {query}: {e}")
    
    print(f"\n✅ Total patents in database: {total_patents}")
    
    # Verify some samples
    print("\n🔍 Sample patents with correct format:")
    conn = sqlite3.connect('data/patents.db')
    cursor = conn.cursor()
    cursor.execute("SELECT patent_id, title, company FROM patents LIMIT 5")
    samples = cursor.fetchall()
    conn.close()
    
    for i, (patent_id, title, company) in enumerate(samples):
        print(f"  {i+1}. {patent_id}")
        print(f"     Title: {title[:60]}...")
        print(f"     Company: {company[:40]}...")
        
        # Check format
        if patent_id and len(patent_id) > 8:
            if any(prefix in patent_id for prefix in ['US', 'EP', 'DE', 'WO']):
                print(f"     ✅ Format correct")
            else:
                print(f"     ⚠️  Format may be wrong")
    
    return total_patents

if __name__ == "__main__":
    refetch_patents()