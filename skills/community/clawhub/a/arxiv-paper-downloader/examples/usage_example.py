#!/usr/bin/env python3
"""
Example usage of the arXiv Paper Downloader Skill
"""

from src.skill import (
    download_papers,
    download_by_arxiv_ids,
    list_categories,
    get_category_info
)

# Example 1: List available categories
print("=" * 60)
print("Example 1: List Categories")
print("=" * 60)
categories = list_categories()
print(f"Available categories: {categories}")

# Example 2: Get category info
print("\n" + "=" * 60)
print("Example 2: Get Category Info")
print("=" * 60)
info = get_category_info("agent_testing")
print(f"Category: {info['name']}")
print(f"Paper count: {info['paper_count']}")
print("\nFirst 5 papers:")
for paper in info['papers'][:5]:
    print(f"  - {paper['arxiv_id']}: {paper['title'][:50]}...")

# Example 3: Download papers (commented out to avoid actual download)
print("\n" + "=" * 60)
print("Example 3: Download Papers")
print("=" * 60)
print("""
# Download agent testing papers
result = download_papers("agent_testing", output_dir="./papers", delay=1.5)
print(f"Downloaded: {result['downloaded']} papers")

# Download all categories
result = download_papers("all", output_dir="./complete_papers")
for cat, stats in result['categories'].items():
    print(f"{cat}: {stats['downloaded']} papers")

# Download specific papers by IDs
result = download_by_arxiv_ids([
    "2310.06129",  # SWE-agent
    "2402.01031",  # SWE-bench
    "1706.03762",  # Transformer
])
""")

print("\n" + "=" * 60)
print("Uncomment the code above to actually download papers!")
print("=" * 60)
