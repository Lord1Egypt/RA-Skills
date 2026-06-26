#!/usr/bin/env python3
"""
CSV Merge Utility for Review Analyzer
Merges original CSV with tagged data
"""

import csv
import json
import sys
import os
from datetime import datetime


def main():
    if len(sys.argv) < 3:
        print("Usage: merge_csv.py <original_csv> <tagged_json> <output_csv>")
        sys.exit(1)

    original_csv = sys.argv[1]
    tagged_json = sys.argv[2]
    output_csv = sys.argv[3]

    # Load tagged data
    try:
        with open(tagged_json, 'r', encoding='utf-8') as f:
            tagged_data = json.load(f)
    except Exception as e:
        print(f"Error loading tagged data: {e}")
        sys.exit(1)

    # Create lookup
    tagged_lookup = {item.get('review_id', ''): item for item in tagged_data}

    # Read original CSV and append tags
    try:
        with open(original_csv, 'r', encoding='utf-8', errors='ignore') as infile, \
             open(output_csv, 'w', encoding='utf-8', newline='', errors='ignore') as outfile:

            reader = csv.DictReader(infile)
            fieldnames = list(reader.fieldnames or [])

            # Add new columns
            new_columns = ['情感_总体评价', '评论价值打分', '打标时间']

            # Collect all tag keys
            all_tag_keys = set()
            for item in tagged_data:
                for tag_key in item.get('tags', {}).keys():
                    all_tag_keys.add(tag_key)

            # Sort tag keys for consistency
            new_columns.extend(sorted(all_tag_keys))

            # Write header
            fieldnames.extend(new_columns)
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            # Process rows
            written_count = 0
            for row in reader:
                # Find review ID
                rid = (row.get('review_id') or
                       row.get('id') or
                       row.get('Id') or
                       row.get('ID') or
                       f"row_{written_count + 1}")

                tagged_item = tagged_lookup.get(rid)

                if tagged_item:
                    # Add basic fields
                    row['情感_总体评价'] = tagged_item.get('sentiment', '')
                    row['评论价值打分'] = tagged_item.get('info_score', '')
                    row['打标时间'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Add tags
                    tags = tagged_item.get('tags', {})
                    for tag_key in all_tag_keys:
                        tag_value = tags.get(tag_key, '未提及')
                        row[tag_key] = tag_value
                    written_count += 1
                else:
                    # Add empty columns
                    row['情感_总体评价'] = ''
                    row['评论价值打分'] = ''
                    row['打标时间'] = ''
                    for tag_key in all_tag_keys:
                        row[tag_key] = '未提及'

                writer.writerow(row)

        print(f"Merged {written_count} tagged reviews to {output_csv}")

    except Exception as e:
        print(f"Error processing CSV: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
