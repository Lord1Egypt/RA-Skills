import google_search
import json
import sys

def run_verification():
    print("Running verification for Google Search skill...")
    print("This script will open a browser window for each search query (headless=False).")
    print("-" * 50)

    queries = [
        "python tutorial",      # Simple English with space
        "python 教程",          # Mixed English and Chinese
        "C++ vs Rust",          # Special characters
        "what is the meaning of life" # Longer query
    ]

    for q in queries:
        print(f"\n🔍 Searching for: '{q}'")
        try:
            results = google_search.google_search(q)
            
            if not results:
                print("❌ No results found.")
            else:
                print(f"✅ Found {len(results)} results.")
                print("Top 2 results:")
                for i, res in enumerate(results[:2]):
                    print(f"  {i+1}. Title: {res['title']}")
                    print(f"     Link:  {res['link']}")
                    print(f"     Snippet: {res['snippet'][:100]}...")
            
        except Exception as e:
            print(f"❌ Error during search: {e}")

    print("\n" + "-" * 50)
    print("Verification complete.")

if __name__ == "__main__":
    run_verification()
