import os
import argparse
from pathlib import Path
import fnmatch

def find_files(search_path, pattern, recursive=True, content_query=None):
    """
    Finds files and folders matching the pattern in the given path.
    Optionally filters by content if content_query is provided.
    """
    root = Path(search_path).expanduser().resolve()
    if not root.exists():
        print(f"Error: Search path {root} does not exist.")
        return []

    matches = []
    
    gen = root.rglob(pattern) if recursive else root.glob(pattern)
    
    for item in gen:
        if content_query:
            if item.is_file():
                try:
                    # Simple text search for small/medium files
                    if item.stat().st_size < 10 * 1024 * 1024: # 10MB limit
                        with open(item, 'r', encoding='utf-8', errors='ignore') as f:
                            if content_query.lower() in f.read().lower():
                                matches.append(str(item))
                except Exception:
                    pass
        else:
            matches.append(str(item))

    return matches

def main():
    parser = argparse.ArgumentParser(description="Find files and folders on the local system.")
    parser.add_argument("pattern", help="Glob pattern to search for (e.g., '*.pdf', 'report*')")
    parser.add_argument("--path", default="~", help="Base path to start searching from (default: user home)")
    parser.add_argument("--no-recursive", action="store_false", dest="recursive", help="Do not search subdirectories")
    parser.add_argument("--content", help="Search for this text within files")
    parser.set_defaults(recursive=True)

    args = parser.parse_args()

    # Determine start path
    start_path = args.path
    if start_path == "~":
        start_path = str(Path.home())
    elif start_path in ["Desktop", "Documents", "Downloads"]:
        start_path = str(Path.home() / start_path)

    print(f"Searching for '{args.pattern}' in {start_path}" + (f" containing '{args.content}'" if args.content else "") + "...")
    
    results = find_files(start_path, args.pattern, args.recursive, args.content)
    
    if not results:
        print("No matches found.")
    else:
        print(f"Found {len(results)} match(es):")
        for r in results:
            print(r)

if __name__ == "__main__":
    main()
