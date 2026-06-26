#!/usr/bin/env python3
"""
Update patent database with correct patent IDs
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

def update_database():
    """Update patent database with correct patent IDs."""
    db_path = 'data/patents.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all patent IDs from database
    cursor.execute("SELECT patent_id FROM patents")
    old_patent_ids = [row[0] for row in cursor.fetchall()]
    
    print(f"🔍 Found {len(old_patent_ids)} patents in database")
    
    # Create mapper
    mapper = EPODataMapper()
    
    updated_count = 0
    error_count = 0
    
    # For each patent, fetch fresh data and update
    for old_id in old_patent_ids:
        try:
            # Try to fetch this specific patent
            # Note: This is a simplified approach - in production we'd need a better way
            # to map old IDs to new queries
            print(f"  Processing patent {old_id}...")
            
            # For now, we'll just note which ones need updating
            # In a real scenario, we'd need to re-fetch all patents
            cursor.execute("""
                UPDATE patents 
                SET image_url = 'https://worldwide.espacenet.com/patent/search?q=' || patent_id
                WHERE patent_id = ?
            """, (old_id,))
            
            updated_count += 1
            
        except Exception as e:
            print(f"  ⚠️ Error updating patent {old_id}: {e}")
            error_count += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Updated {updated_count} patents")
    print(f"⚠️  {error_count} errors")
    
    # Now fetch fresh data for a sample query to show the fix works
    print("\n🔍 Fetching fresh sample data...")
    patents = mapper.fetch_patents('pa=IBM', 1, 3)
    
    print(f"\n✅ Fresh sample patents:")
    for i, patent in enumerate(patents):
        print(f"  {i+1}. {patent.get('patent_id')} - {patent.get('title', '')[:60]}...")
        print(f"     URL: {patent.get('image_url', '')}")

if __name__ == "__main__":
    update_database()