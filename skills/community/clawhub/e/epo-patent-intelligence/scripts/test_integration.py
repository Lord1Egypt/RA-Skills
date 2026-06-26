#!/usr/bin/env python3
"""
Test the complete EPO data mapper with database integration
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from epo_data_mapper import EPODataMapper
from database_manager import DatabaseManager

# Test with a simple query
mapper = EPODataMapper()
patents = mapper.fetch_patents("pa=IBM", 1, 2)

print(f"Fetched {len(patents)} patents")
for i, patent in enumerate(patents):
    print(f"\nPatent {i+1}:")
    for key, value in patent.items():
        if key == 'abstract' and len(str(value)) > 100:
            print(f"  {key}: {str(value)[:100]}...")
        else:
            print(f"  {key}: {type(value)} = {value}")

# Test database save
db = DatabaseManager()
print(f"\nDatabase path: {db.db_path}")

for patent in patents:
    try:
        success = db.save_patent(patent)
        print(f"Saved patent {patent.get('patent_id')}: {success}")
    except Exception as e:
        print(f"Error saving patent {patent.get('patent_id')}: {e}")
        import traceback
        traceback.print_exc()

print(f"\nTotal patents in database: {db.get_patent_count()}")