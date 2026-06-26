#!/usr/bin/env python3
"""
D&D 5e SRD Search Tool with Character Positions

This tool searches through the D&D 5e SRD reference files and returns
results with exact character positions for precise source citation.

Usage:
    python search_with_positions.py "search term" [--files file1.md file2.md]
    python search_with_positions.py "search term" --all
    python search_with_positions.py "search term" --pages 001-120
"""

import argparse
import os
import re
from pathlib import Path
from typing import List


class SearchResult:
    """Represents a single search result with character positions."""

    def __init__(
        self,
        file_path: str,
        match_text: str,
        start_pos: int,
        end_pos: int,
        context_before: str = "",
        context_after: str = "",
    ):
        self.file_path = file_path
        self.match_text = match_text
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.context_before = context_before
        self.context_after = context_after

    def __str__(self):
        filename = os.path.basename(self.file_path)
        return (
            f"File: {filename}\n"
            f"Position: chars {self.start_pos}-{self.end_pos}\n"
            f"Match: {self.match_text}\n"
            f"Context: ...{self.context_before}[{self.match_text}]{self.context_after}...\n"
        )


def get_references_dir() -> Path:
    """Resolve the path to the references directory.

    Returns the ./references directory alongside this script's parent directory.
    """
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent
    local_refs = skill_dir / "references"
    return local_refs


def get_all_reference_files() -> List[Path]:
    """Get all markdown files in the references directory."""
    refs_dir = get_references_dir()
    return sorted(refs_dir.glob("*.md"))


def get_files_by_page_range(page_range: str) -> List[Path]:
    """
    Get files that match a page range pattern (e.g., '090-223').
    This handles both exact matches and range spans.
    """
    refs_dir = get_references_dir()

    # Try exact pattern match first
    pattern = f"*{page_range}*.md"
    exact_matches = sorted(refs_dir.glob(pattern))
    if exact_matches:
        return exact_matches

    # Parse the range to find all files that fall within it
    try:
        start_page, end_page = map(int, page_range.split("-"))
    except ValueError:
        # If not a valid range, try as a simple substring pattern
        return sorted(refs_dir.glob(f"*{page_range}*.md"))

    # Find all files whose page ranges overlap with the requested range
    matching_files = []
    for file_path in refs_dir.glob("*.md"):
        # Extract page range from filename suffix like ..._123-456.md
        match = re.search(r"(\d{3})-(\d{3})\.md$", file_path.name)
        if match:
            file_start = int(match.group(1))
            file_end = int(match.group(2))
            if not (file_end < start_page or file_start > end_page):
                matching_files.append(file_path)

    return sorted(matching_files)


def search_in_file(
    file_path: Path,
    search_term: str,
    case_sensitive: bool = False,
    context_chars: int = 50,
) -> List[SearchResult]:
    """
    Search for a term in a file and return results with character positions.
    """
    results: List[SearchResult] = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        flags = 0 if case_sensitive else re.IGNORECASE
        pattern = re.compile(re.escape(search_term), flags)

        for match in pattern.finditer(content):
            start_pos = match.start()
            end_pos = match.end()
            match_text = match.group()

            context_start = max(0, start_pos - context_chars)
            context_end = min(len(content), end_pos + context_chars)

            context_before = content[context_start:start_pos]
            context_after = content[end_pos:context_end]

            results.append(
                SearchResult(
                    file_path=str(file_path),
                    match_text=match_text,
                    start_pos=start_pos,
                    end_pos=end_pos,
                    context_before=context_before,
                    context_after=context_after,
                )
            )
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return results


def search_files(
    files: List[Path],
    search_term: str,
    case_sensitive: bool = False,
    max_results: int = 20,
    context_chars: int = 50,
) -> List[SearchResult]:
    """Search for a term across multiple files."""
    all_results: List[SearchResult] = []
    for file_path in files:
        results = search_in_file(file_path, search_term, case_sensitive, context_chars)
        all_results.extend(results)
        if len(all_results) >= max_results:
            break
    return all_results[:max_results]


def format_results_for_citation(results: List[SearchResult]) -> str:
    """Format results in a citation-friendly way."""
    if not results:
        return "No results found."

    output = f"\nFound {len(results)} result(s):\n"
    output += "=" * 80 + "\n\n"

    for i, result in enumerate(results, 1):
        output += f"Result {i}:\n"
        output += f"  File: {os.path.basename(result.file_path)}\n"
        output += f"  Character Range: {result.start_pos}-{result.end_pos}\n"
        output += f"  Citation: [{os.path.basename(result.file_path)}, chars {result.start_pos}-{result.end_pos}]\n"
        output += "\n  Context:\n"
        output += f"  ...{result.context_before.strip()}\n"
        output += f"  >> {result.match_text} <<\n"
        output += f"  {result.context_after.strip()}...\n"
        output += "\n" + "---" + "\n\n"

    return output


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Search D&D 5e SRD references with character positions for citation"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            """
Examples:
  # Search all files
  python search_with_positions.py "fireball" --all

  # Search specific page range
  python search_with_positions.py "wizard" --pages 121-200

  # Search specific files
  python search_with_positions.py "grapple" --files "DND5eSRD_087-103.md"

  # Case-sensitive search with more context
  python search_with_positions.py "Attack" --all --case-sensitive --context 100
            """
        ),
    )

    parser.add_argument("search_term", help="Term to search for")
    parser.add_argument("--files", nargs="+", help="Specific files to search")
    parser.add_argument("--all", action="store_true", help="Search all reference files")
    parser.add_argument("--pages", help="Search files in page range (e.g., 001-120)")
    parser.add_argument(
        "--case-sensitive", action="store_true", help="Case-sensitive search"
    )
    parser.add_argument(
        "--max-results", type=int, default=20, help="Maximum results (default: 20)"
    )
    parser.add_argument(
        "--context", type=int, default=100, help="Characters of context (default: 100)"
    )

    args = parser.parse_args()

    # Determine which files to search
    refs_dir = get_references_dir()
    files_to_search: List[Path] = []

    if args.all:
        files_to_search = get_all_reference_files()
    elif args.pages:
        files_to_search = get_files_by_page_range(args.pages)
    elif args.files:
        # Convert provided filenames to full paths
        for filename in args.files:
            file_path = refs_dir / filename
            if file_path.exists():
                files_to_search.append(file_path)
            else:
                print(f"Warning: File not found: {filename}")
    else:
        files_to_search = get_all_reference_files()

    if not files_to_search:
        print("Error: No files to search. Use --all, --pages, or --files")
        return

    print(f"Searching {len(files_to_search)} file(s) for '{args.search_term}'...")

    # Perform search
    results = search_files(
        files_to_search,
        args.search_term,
        case_sensitive=args.case_sensitive,
        max_results=args.max_results,
        context_chars=args.context,
    )

    # Display results
    print(format_results_for_citation(results))


if __name__ == "__main__":
    main()
