#!/usr/bin/env python3
"""
Generate rag-index.jsonl from rag-index.json.
Usage: python3 gen_jsonl.py <input_json_path> <output_jsonl_path>
"""
import json
import sys
import os

def generate_jsonl(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        records = json.load(f)

    if not isinstance(records, list):
        print(f"Error: Expected a JSON array in {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(output_path, 'w', encoding='utf-8') as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')

    print(f"Generated {len(records)} records → {output_path}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 gen_jsonl.py <input.json> <output.jsonl>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    generate_jsonl(input_path, output_path)
