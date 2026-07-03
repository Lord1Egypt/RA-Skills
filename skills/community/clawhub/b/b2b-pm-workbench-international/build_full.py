#!/usr/bin/env python3
"""Build the complete international SKILL.md by appending chunks."""
import os

DEST = "/Users/macos/Desktop/【0616 skill升级工程】/international/b2b-pm-workbench-international/SKILL.md"

# Clear the file first
with open(DEST, 'w', encoding='utf-8') as f:
    f.write('')

def append(content):
    with open(DEST, 'a', encoding='utf-8') as f:
        f.write(content)
    return len(content)

total = 0

# Read all chunks from separate files
chunk_dir = os.path.dirname(os.path.abspath(__file__))

for i in range(1, 10):
    chunk_file = os.path.join(chunk_dir, f"chunk_{i}.txt")
    if os.path.exists(chunk_file):
        with open(chunk_file, 'r', encoding='utf-8') as f:
            content = f.read()
        n = append(content)
        total += n
        print(f"Chunk {i} appended: {n} chars")

print(f"\nTotal: {total} chars written to {DEST}")
print(f"File size: {os.path.getsize(DEST)} bytes")