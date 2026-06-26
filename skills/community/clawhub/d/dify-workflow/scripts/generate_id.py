#!/usr/bin/env python3
"""
Generate unique node IDs for Dify workflows.

Node IDs are Unix timestamps in milliseconds as strings.
"""

import time
import sys


def generate_node_id() -> str:
    """Generate a unique node ID based on current timestamp."""
    return str(int(time.time() * 1000))


def generate_multiple_ids(count: int) -> list:
    """Generate multiple unique node IDs."""
    ids = []
    for i in range(count):
        ids.append(str(int(time.time() * 1000) + i))
        # Small delay to ensure uniqueness
        if i < count - 1:
            time.sleep(0.001)
    return ids


def main():
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
            ids = generate_multiple_ids(count)
            for node_id in ids:
                print(node_id)
        except ValueError:
            print("Usage: python generate_id.py [count]")
            sys.exit(1)
    else:
        print(generate_node_id())


if __name__ == '__main__':
    main()
