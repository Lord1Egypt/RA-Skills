#!/usr/bin/env python3
"""
Search for photos of a specific person.

Usage:
    python examples/search_photos.py "张三"
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from everything_search import EverythingSearch


def main():
    if len(sys.argv) < 2:
        print("Usage: python search_photos.py <person_name>")
        print("Example: python search_photos.py 张三")
        sys.exit(1)

    person_name = sys.argv[1]

    print(f"📸 Searching for photos of: {person_name}")
    print("=" * 60)

    # Initialize search client
    search = EverythingSearch(port=2853)

    # Check connection
    if not search.check_connection():
        print("❌ Error: Cannot connect to Everything HTTP Server")
        sys.exit(1)

    # Search for photos
    try:
        results = search.search_photos(person_name)

        print(f"✅ Found {results.total} photos")
        print()

        if results.total == 0:
            print("No photos found. Try different name or check spelling.")
        else:
            # Group by type
            jpg_photos = [
                item for item in results.items if item.name.lower().endswith(".jpg")
            ]
            png_photos = [
                item for item in results.items if item.name.lower().endswith(".png")
            ]

            print(f"📊 Breakdown:")
            print(f"   - JPG files: {len(jpg_photos)}")
            print(f"   - PNG files: {len(png_photos)}")
            print()

            print(f"📋 Top {len(results.items[:15])} results:")
            print("-" * 60)

            for i, item in enumerate(results.items[:15], 1):
                icon = "🖼️"
                print(f"{i:2}. {icon} {item.name}")
                print(f"    Path: {item.full_path}")
                print(f"    Size: {item.format_size()}")
                print()

    except Exception as e:
        print(f"❌ Search failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
