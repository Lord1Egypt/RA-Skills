#!/usr/bin/env python3
"""
D&D 5e SRD Context Expansion Tool

This tool expands the context around search results from search_with_positions.py,
providing larger, structured views of the source material. Designed for LLM consumption.

Usage:
    # Expand specific result from a search
    python expand_context.py "fireball" --result 3 --mode section --all

    # Expand multiple results
    python expand_context.py "fireball" --results 1,3,5 --mode paragraph --all

    # Direct expansion from file position
    python expand_context.py --file "DND5eSRD_121-137.md" --position 1234 --mode section

    # Get full document structure with position
    python expand_context.py --file "DND5eSRD_121-137.md" --position 1234 --mode document
"""

import argparse
import json
import os
import re

# Import from search tool in the same directory
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
from search_with_positions import (
    get_all_reference_files,
    get_files_by_page_range,
    get_references_dir,
    search_files,
)


@dataclass
class HeadingNode:
    """Represents a heading in the document hierarchy."""

    level: int
    text: str
    start_pos: int
    end_pos: int
    content: str = ""
    children: List["HeadingNode"] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []


@dataclass
class ExpandedContext:
    """Represents expanded context around a position."""

    file_path: str
    original_match: str
    match_start: int
    match_end: int
    expanded_text: str
    expansion_start: int
    expansion_end: int
    mode: str
    heading_path: List[str]
    metadata: Dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class DocumentParser:
    """Parses markdown documents with structure awareness."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        with open(file_path, "r", encoding="utf-8") as f:
            self.content = f.read()
        self.headings = self._parse_headings()
        self.paragraphs = self._parse_paragraphs()

    def _parse_headings(self) -> List[Dict]:
        """Parse all headings with their positions."""
        headings: List[Dict] = []
        pattern = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)

        for match in pattern.finditer(self.content):
            level = len(match.group(1))
            text = match.group(2).strip()
            start_pos = match.start()

            headings.append(
                {
                    "level": level,
                    "text": text,
                    "start_pos": start_pos,
                    "end_pos": match.end(),
                }
            )

        return headings

    def _parse_paragraphs(self) -> List[Tuple[int, int]]:
        """Parse paragraph boundaries (text blocks separated by blank lines)."""
        paragraphs: List[Tuple[int, int]] = []

        in_paragraph = False
        para_start = 0

        lines = self.content.split("\n")
        line_pos = 0

        for line in lines:
            line_start = line_pos
            line_end = line_pos + len(line)
            line_pos = line_end + 1  # +1 for newline

            if line.strip():
                if not in_paragraph:
                    para_start = line_start
                    in_paragraph = True
            else:
                if in_paragraph:
                    paragraphs.append((para_start, line_start))
                    in_paragraph = False

        if in_paragraph:
            paragraphs.append((para_start, len(self.content)))

        return paragraphs

    def get_heading_path(self, position: int) -> List[str]:
        """Get the breadcrumb trail of headings for a position."""
        path: List[str] = []
        current_levels: Dict[int, str] = {}

        for heading in self.headings:
            if heading["start_pos"] > position:
                break

            level = heading["level"]
            keys_to_remove = [k for k in current_levels.keys() if k >= level]
            for k in keys_to_remove:
                del current_levels[k]

            current_levels[level] = heading["text"]

        for level in sorted(current_levels.keys()):
            path.append(current_levels[level])

        return path

    def get_section_bounds(
        self, position: int, include_subsections: bool = True
    ) -> Tuple[int, int]:
        """Get the bounds of the section containing the position."""
        containing_heading = None
        containing_level = None

        for i, heading in enumerate(self.headings):
            if heading["start_pos"] <= position:
                containing_heading = i
                containing_level = heading["level"]
            else:
                break

        if containing_heading is None:
            if self.headings:
                return (0, self.headings[0]["start_pos"])
            return (0, len(self.content))

        section_start = self.headings[containing_heading]["start_pos"]
        section_end = len(self.content)

        for i in range(containing_heading + 1, len(self.headings)):
            next_heading = self.headings[i]
            if include_subsections:
                if next_heading["level"] <= containing_level:
                    section_end = next_heading["start_pos"]
                    break
            else:
                section_end = next_heading["start_pos"]
                break

        return (section_start, section_end)

    def get_paragraph_bounds(self, position: int) -> Tuple[int, int]:
        """Get the bounds of the paragraph containing the position."""
        for para_start, para_end in self.paragraphs:
            if para_start <= position < para_end:
                return (para_start, para_end)

        return (max(0, position - 500), min(len(self.content), position + 500))

    def get_document_structure(self, focus_position: Optional[int] = None) -> Dict:
        """Get the full document structure with optional focus on a position."""
        structure: Dict = {
            "file": os.path.basename(self.file_path),
            "total_chars": len(self.content),
            "headings": [],
        }

        for heading in self.headings:
            heading_info = {
                "level": heading["level"],
                "text": heading["text"],
                "position": heading["start_pos"],
                "is_focus": False,
            }

            if focus_position is not None:
                start = heading["start_pos"]
                end = len(self.content)
                for next_h in self.headings:
                    if (
                        next_h["start_pos"] > start
                        and next_h["level"] <= heading["level"]
                    ):
                        end = next_h["start_pos"]
                        break

                if start <= focus_position < end:
                    heading_info["is_focus"] = True

            structure["headings"].append(heading_info)

        return structure


def expand_context(
    file_path: Path,
    position: int,
    match_text: str,
    mode: str = "paragraph",
    match_end: Optional[int] = None,
) -> ExpandedContext:
    """Expand context around a position with various modes."""
    if match_end is None:
        match_end = position + len(match_text)

    parser = DocumentParser(file_path)
    heading_path = parser.get_heading_path(position)

    if mode == "char":
        char_context = 1000
        start = max(0, position - char_context)
        end = min(len(parser.content), match_end + char_context)
        expanded_text = parser.content[start:end]
    elif mode == "paragraph":
        start, end = parser.get_paragraph_bounds(position)
        expanded_text = parser.content[start:end]
    elif mode == "section":
        start, end = parser.get_section_bounds(position, include_subsections=True)
        expanded_text = parser.content[start:end]
    elif mode == "section-only":
        start, end = parser.get_section_bounds(position, include_subsections=False)
        expanded_text = parser.content[start:end]
    elif mode == "document":
        start = 0
        end = len(parser.content)
        expanded_text = parser.content
    else:
        raise ValueError(f"Unknown mode: {mode}")

    return ExpandedContext(
        file_path=str(file_path),
        original_match=match_text,
        match_start=position,
        match_end=match_end,
        expanded_text=expanded_text,
        expansion_start=start,
        expansion_end=end,
        mode=mode,
        heading_path=heading_path,
        metadata={
            "file_size": len(parser.content),
            "expansion_size": len(expanded_text),
            "num_headings_in_path": len(heading_path),
        },
    )


def format_expanded_context(
    context: ExpandedContext, format_type: str = "human"
) -> str:
    """Format expanded context for output."""

    if format_type == "json":
        return json.dumps(asdict(context), indent=2)
    elif format_type == "human":
        output: List[str] = []
        output.append("=" * 80)
        output.append(f"File: {os.path.basename(context.file_path)}")
        output.append(f"Mode: {context.mode}")
        output.append(f"Original Match: '{context.original_match}'")
        output.append(f"Match Position: {context.match_start}-{context.match_end}")
        output.append(
            f"Expanded Range: {context.expansion_start}-{context.expansion_end}"
        )
        output.append(f"Expansion Size: {context.metadata['expansion_size']} chars")

        if context.heading_path:
            output.append("\nHeading Path:")
            for i, heading in enumerate(context.heading_path, 1):
                output.append(f"  {'  ' * (i - 1)}→ {heading}")

        output.append("\n" + "-" * 80)
        output.append("EXPANDED CONTENT:")
        output.append("-" * 80)
        output.append(context.expanded_text)
        output.append("=" * 80)

        return "\n".join(output)
    elif format_type == "llm":
        output: List[str] = []
        output.append("### EXPANDED CONTEXT")
        output.append(f"**Source**: {os.path.basename(context.file_path)}")
        output.append(
            f"**Character Range**: {context.expansion_start}-{context.expansion_end}"
        )
        output.append(
            f"**Original Match** at position {context.match_start}: `{context.original_match}`"
        )

        if context.heading_path:
            breadcrumb = " → ".join(context.heading_path)
            output.append(f"**Location**: {breadcrumb}")

        output.append("\n---\n")
        output.append(context.expanded_text)
        output.append("\n---\n")

        return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description=("Expand context around search results from D&D 5e SRD references"),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            """
Examples:
  # Expand the 3rd search result by section
  python expand_context.py "fireball" --result 3 --mode section --all

  # Expand multiple results by paragraph
  python expand_context.py "wizard" --results 1,3,5 --mode paragraph --all

  # Direct expansion from file position
  python expand_context.py --file "DND5eSRD_121-137.md" --position 1234 --mode section

  # Get document structure
  python expand_context.py --file "DND5eSRD_121-137.md" --position 1234 --mode document

  # Output as JSON for machine processing
  python expand_context.py "fireball" --result 1 --all --format json

Expansion Modes:
  char         - Expand by ±1000 characters (simple)
  paragraph    - Expand to paragraph boundaries (blank line separated)
  section      - Expand to full section including subsections
  section-only - Expand to section excluding subsections
  document     - Show entire document (use with caution)

Output Formats:
  human        - Human-readable formatted output
  llm          - Optimized for LLM consumption (default)
  json         - Machine-readable JSON
            """
        ),
    )

    # Search parameters (for finding results to expand)
    parser.add_argument("search_term", nargs="?", help="Term to search for")
    parser.add_argument("--result", type=int, help="Result number to expand (1-based)")
    parser.add_argument(
        "--results", help="Comma-separated result numbers to expand (e.g., '1,3,5')"
    )
    parser.add_argument(
        "--all-search",
        action="store_true",
        dest="search_all",
        help="Search all reference files",
    )
    parser.add_argument("--pages", help="Search files in page range (e.g., 001-120)")
    parser.add_argument("--files", nargs="+", help="Specific files to search")

    # Direct expansion parameters
    parser.add_argument("--file", help="Direct file path for expansion")
    parser.add_argument(
        "--position", type=int, help="Character position for direct expansion"
    )

    # Expansion options
    parser.add_argument(
        "--mode",
        choices=["char", "paragraph", "section", "section-only", "document"],
        default="paragraph",
        help="Expansion mode (default: paragraph)",
    )
    parser.add_argument(
        "--format",
        choices=["human", "llm", "json"],
        default="llm",
        help="Output format (default: llm)",
    )

    # Search options
    parser.add_argument(
        "--case-sensitive", action="store_true", help="Case-sensitive search"
    )
    parser.add_argument(
        "--max-search-results",
        type=int,
        default=50,
        help="Maximum search results to find (default: 50)",
    )

    args = parser.parse_args()

    # Direct expansion mode
    if args.file and args.position is not None:
        file_path = Path(args.file)
        if not file_path.exists():
            refs_dir = get_references_dir()
            file_path = refs_dir / args.file

        if not file_path.exists():
            print(f"Error: File not found: {args.file}")
            return

        context = expand_context(
            file_path=file_path,
            position=args.position,
            match_text="[direct position]",
            mode=args.mode,
        )

        print(format_expanded_context(context, args.format))
        return

    # Search-based expansion mode
    if not args.search_term:
        print("Error: Provide either search_term + result, or --file + --position")
        parser.print_help()
        return

    if not args.result and not args.results:
        print("Error: Specify which result(s) to expand with --result or --results")
        return

    # Determine files to search
    files_to_search: List[Path] = []
    refs_dir = get_references_dir()

    if args.search_all:
        files_to_search = get_all_reference_files()
    elif args.pages:
        files_to_search = get_files_by_page_range(args.pages)
    elif args.files:
        for filename in args.files:
            file_path = refs_dir / filename
            if file_path.exists():
                files_to_search.append(file_path)
            else:
                print(f"Warning: File not found: {filename}")
    else:
        files_to_search = get_all_reference_files()

    if not files_to_search:
        print("Error: No files to search")
        return

    # Perform search
    print(f"Searching for '{args.search_term}'...", file=sys.stderr)
    search_results = search_files(
        files_to_search,
        args.search_term,
        case_sensitive=args.case_sensitive,
        max_results=args.max_search_results,
        context_chars=50,
    )

    if not search_results:
        print(f"No results found for '{args.search_term}'")
        return

    print(f"Found {len(search_results)} results\n", file=sys.stderr)

    # Determine which results to expand
    results_to_expand: List[int] = []
    if args.results:
        result_nums = [int(x.strip()) for x in args.results.split(",")]
        results_to_expand = result_nums
    elif args.result:
        results_to_expand = [args.result]

    # Expand specified results
    for result_num in results_to_expand:
        if result_num < 1 or result_num > len(search_results):
            print(
                f"Warning: Result {result_num} out of range (1-{len(search_results)})"
            )
            continue

        search_result = search_results[result_num - 1]

        print(f"\n{'=' * 80}", file=sys.stderr)
        print(f"EXPANDING RESULT {result_num}/{len(search_results)}", file=sys.stderr)
        print(f"{'=' * 80}\n", file=sys.stderr)

        context = expand_context(
            file_path=Path(search_result.file_path),
            position=search_result.start_pos,
            match_text=search_result.match_text,
            mode=args.mode,
            match_end=search_result.end_pos,
        )

        print(format_expanded_context(context, args.format))

        if len(results_to_expand) > 1 and result_num != results_to_expand[-1]:
            print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
