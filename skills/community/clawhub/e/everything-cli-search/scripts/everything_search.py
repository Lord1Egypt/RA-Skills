#!/usr/bin/env python3
"""
Everything CLI Search Script
Fast file and folder search using Everything's command line interface.
Supports advanced search: operators, wildcards, macros, modifiers, functions (size, date, attributes, regex, content search, and more).
"""

import subprocess
import json
import sys
import re
from typing import List, Dict, Optional
from pathlib import Path


class EverythingSearch:
    """Everything CLI Search wrapper."""

    def __init__(self, es_path: str = "es.exe"):
        """
        Initialize EverythingSearch.

        Args:
            es_path: Path to es.exe (default: "es.exe")
        """
        self.es_path = es_path

    def search(
        self,
        query: str,
        path: Optional[str] = None,
        regex: bool = False,
        case: bool = False,
        whole_word: bool = False,
        match_path: bool = False,
        sort: Optional[str] = None,
        sort_descending: bool = False,
        details: bool = False,
        limit: Optional[int] = None,
        functions: Optional[Dict[str, str]] = None,
        modifiers: Optional[List[str]] = None,
    ) -> List[Dict[str, str]]:
        """
        Search files/folders using Everything CLI.

        Args:
            query: Search query
            path: Search in specific path
            regex: Enable regex search
            case: Enable case-sensitive search
            whole_word: Match whole word only
            match_path: Match full path
            sort: Sort by field (name, size, "Date Modified", etc.)
            sort_descending: Sort in descending order
            details: Show details view
            limit: Limit number of results
            functions: Dictionary of search functions (size, date, attrib, etc.)
            modifiers: List of modifiers (case, wfn, ww, etc.)

        Returns:
            List of search results with metadata
        """
        cmd = [self.es_path]

        # Add search options
        if path:
            cmd.extend(["-p", path])
        if regex:
            cmd.append("-regex")
        if case:
            cmd.append("-case")
        else:
            cmd.append("-nocase")
        if whole_word:
            cmd.append("-wholeword")
        if match_path:
            cmd.append("-matchpath")
        if sort:
            cmd.extend(["-sort", sort])
        if sort_descending:
            cmd.append("-sort-descending")
        if details:
            cmd.append("-details")

        # Build query with modifiers, functions, and main query
        query_parts = []

        # Add modifiers
        if modifiers:
            for modifier in modifiers:
                query_parts.append(f"{modifier}:")

        # Add functions
        if functions:
            for func_name, func_value in functions.items():
                query_parts.append(f"{func_name}:{func_value}")

        # Add main query
        if query:
            query_parts.append(query)

        # Combine query parts
        final_query = " ".join(query_parts)
        cmd.append(final_query)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=30,
            )
            output = result.stdout

            # Parse output
            results = self._parse_output(output, details)

            # Apply limit
            if limit and len(results) > limit:
                results = results[:limit]

            return results

        except subprocess.CalledProcessError as e:
            print(f"Error running es.exe: {e}", file=sys.stderr)
            if e.stderr:
                print(f"stderr: {e.stderr}", file=sys.stderr)
            return []
        except subprocess.TimeoutExpired:
            print("Search timed out", file=sys.stderr)
            return []
        except FileNotFoundError:
            print(
                f"Error: {self.es_path} not found. Please install Everything from https://www.voidtools.com",
                file=sys.stderr,
            )
            return []

    def _parse_output(self, output: str, details: bool) -> List[Dict[str, str]]:
        """
        Parse Everything CLI output.

        Args:
            output: Raw output from es.exe
            details: Whether output is in details view

        Returns:
            List of parsed results
        """
        results = []
        lines = output.strip().split("\n")

        for line in lines:
            if not line.strip():
                continue

            if details:
                # Parse details view output
                # Format: "filename.ext | size | date modified | path"
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 4:
                    results.append(
                        {
                            "name": parts[0],
                            "size": parts[1],
                            "date_modified": parts[2],
                            "path": parts[3],
                            "full_path": f"{parts[3]}\\{parts[0]}",
                        }
                    )
            else:
                # Parse simple output (just filenames)
                results.append(
                    {
                        "name": line.strip(),
                        "path": "",
                        "full_path": line.strip(),
                    }
                )

        return results

    def search_by_size(
        self,
        size_query: str,
        path: Optional[str] = None,
        **kwargs,
    ) -> List[Dict[str, str]]:
        """
        Search files by size.

        Args:
            size_query: Size query (e.g., ">1mb", "10mb..100mb", "tiny", "huge")
            path: Search in specific path
            **kwargs: Additional search options

        Returns:
            List of search results
        """
        functions = {"size": size_query}
        return self.search("", path=path, functions=functions, **kwargs)

    def search_by_date(
        self,
        date_query: str,
        date_type: str = "datemodified",
        path: Optional[str] = None,
        **kwargs,
    ) -> List[Dict[str, str]]:
        """
        Search files by date.

        Args:
            date_query: Date query (e.g., "today", "yesterday", "lastweek", "2024")
            date_type: Date type (datemodified, datecreated, dateaccessed, daterun)
            path: Search in specific path
            **kwargs: Additional search options

        Returns:
            List of search results
        """
        functions = {date_type: date_query}
        return self.search("", path=path, functions=functions, **kwargs)

    def search_by_attributes(
        self,
        attributes: str,
        path: Optional[str] = None,
        **kwargs,
    ) -> List[Dict[str, str]]:
        """
        Search files by attributes.

        Args:
            attributes: Attribute query (e.g., "H", "R", "S", "HR")
            path: Search in specific path
            **kwargs: Additional search options

        Returns:
            List of search results
        """
        functions = {"attrib": attributes}
        return self.search("", path=path, functions=functions, **kwargs)

    def search_by_content(
        self,
        content_query: str,
        encoding: str = "utf8",
        path: Optional[str] = None,
        **kwargs,
    ) -> List[Dict[str, str]]:
        """
        Search files by content.

        Args:
            content_query: Content to search for
            encoding: Content encoding (utf8, utf16, utf16be, ansi)
            path: Search in specific path
            **kwargs: Additional search options

        Returns:
            List of search results
        """
        func_name = f"{encoding}content"
        functions = {func_name: content_query}
        return self.search("", path=path, functions=functions, **kwargs)

    def search_images(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        orientation: Optional[str] = None,
        bitdepth: Optional[int] = None,
        path: Optional[str] = None,
        **kwargs,
    ) -> List[Dict[str, str]]:
        """
        Search images by dimensions.

        Args:
            width: Image width in pixels
            height: Image height in pixels
            orientation: Image orientation (landscape, portrait)
            bitdepth: Image bit depth
            path: Search in specific path
            **kwargs: Additional search options

        Returns:
            List of search results
        """
        functions = {}
        if width:
            functions["width"] = str(width)
        if height:
            functions["height"] = str(height)
        if orientation:
            functions["orientation"] = orientation
        if bitdepth:
            functions["bitdepth"] = str(bitdepth)

        return self.search("", path=path, functions=functions, **kwargs)

    def search_media(
        self,
        album: Optional[str] = None,
        artist: Optional[str] = None,
        genre: Optional[str] = None,
        title: Optional[str] = None,
        track: Optional[int] = None,
        comment: Optional[str] = None,
        path: Optional[str] = None,
        **kwargs,
    ) -> List[Dict[str, str]]:
        """
        Search media files by metadata.

        Args:
            album: Album name
            artist: Artist name
            genre: Genre
            title: Title
            track: Track number
            comment: Comment
            path: Search in specific path
            **kwargs: Additional search options

        Returns:
            List of search results
        """
        functions = {}
        if album:
            functions["album"] = album
        if artist:
            functions["artist"] = artist
        if genre:
            functions["genre"] = genre
        if title:
            functions["title"] = title
        if track:
            functions["track"] = str(track)
        if comment:
            functions["comment"] = comment

        return self.search("", path=path, functions=functions, **kwargs)

    def search_by_macro(
        self,
        macro: str,
        path: Optional[str] = None,
        **kwargs,
    ) -> List[Dict[str, str]]:
        """
        Search by macro.

        Args:
            macro: Macro name (audio, zip, doc, exe, pic, video)
            path: Search in specific path
            **kwargs: Additional search options

        Returns:
            List of search results
        """
        return self.search(f"{macro}:", path=path, **kwargs)

    def search_files_by_extension(
        self,
        extensions: List[str],
        path: Optional[str] = None,
        **kwargs,
    ) -> List[Dict[str, str]]:
        """
        Search files by extension.

        Args:
            extensions: List of file extensions (e.g., [".pdf", ".docx"])
            path: Search in specific path
            **kwargs: Additional search options

        Returns:
            List of search results
        """
        # Build wildcard pattern
        pattern = ";".join(f"*{ext}" for ext in extensions)
        return self.search(pattern, path=path, **kwargs)

    def search_in_directory(
        self,
        path: str,
        query: str,
        recursive: bool = True,
        **kwargs,
    ) -> List[Dict[str, str]]:
        """
        Search in specific directory.

        Args:
            path: Directory path
            query: Search query
            recursive: Search subdirectories (default: True)
            **kwargs: Additional search options

        Returns:
            List of search results
        """
        if not recursive:
            kwargs["parent"] = path
            return self.search(query, **kwargs)
        else:
            return self.search(query, path=path, **kwargs)


def main():
    """Main entry point for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Fast file search using Everything CLI"
    )
    parser.add_argument("query", help="Search query", nargs="?", default="")
    parser.add_argument("-p", "--path", help="Search in specific path")
    parser.add_argument("-r", "--regex", action="store_true", help="Enable regex")
    parser.add_argument("-c", "--case", action="store_true", help="Case-sensitive")
    parser.add_argument("-w", "--whole-word", action="store_true", help="Match whole word")
    parser.add_argument("-m", "--match-path", action="store_true", help="Match full path")
    parser.add_argument("-s", "--sort", help="Sort by field")
    parser.add_argument("-d", "--descending", action="store_true", help="Sort descending")
    parser.add_argument("--details", action="store_true", help="Show details")
    parser.add_argument("-l", "--limit", type=int, help="Limit results")
    parser.add_argument("-j", "--json", action="store_true", help="Output as JSON")

    # Function arguments
    parser.add_argument("--size", help="Search by size (e.g., >1mb, 10mb..100mb)")
    parser.add_argument("--date", help="Search by date (e.g., today, yesterday, lastweek)")
    parser.add_argument("--date-type", default="datemodified", help="Date type (datemodified, datecreated, dateaccessed, daterun)")
    parser.add_argument("--attrib", help="Search by attributes (e.g., H, R, S, HR)")
    parser.add_argument("--content", help="Search by content")
    parser.add_argument("--encoding", default="utf8", help="Content encoding (utf8, utf16, utf16be, ansi)")
    parser.add_argument("--width", type=int, help="Search images by width")
    parser.add_argument("--height", type=int, help="Search images by height")
    parser.add_argument("--orientation", help="Search images by orientation (landscape, portrait)")
    parser.add_argument("--bitdepth", type=int, help="Search images by bit depth")
    parser.add_argument("--album", help="Search media by album")
    parser.add_argument("--artist", help="Search media by artist")
    parser.add_argument("--genre", help="Search media by genre")
    parser.add_argument("--title", help="Search media by title")
    parser.add_argument("--track", type=int, help="Search media by track number")
    parser.add_argument("--comment", help="Search media by comment")
    parser.add_argument("--macro", help="Search by macro (audio, zip, doc, exe, pic, video)")

    # Modifier arguments
    parser.add_argument("--wfn", action="store_true", help="Match whole filename")
    parser.add_argument("--ww", action="store_true", help="Match whole word")
    parser.add_argument("--startwith", help="Match filenames starting with text")
    parser.add_argument("--endwith", help="Match filenames ending with text")
    parser.add_argument("--file-only", action="store_true", help="Match files only")
    parser.add_argument("--folder-only", action="store_true", help="Match folders only")

    args = parser.parse_args()

    # Create searcher
    searcher = EverythingSearch()

    # Build functions
    functions = {}
    if args.size:
        functions["size"] = args.size
    if args.date:
        functions[args.date_type] = args.date
    if args.attrib:
        functions["attrib"] = args.attrib
    if args.content:
        func_name = f"{args.encoding}content"
        functions[func_name] = args.content
    if args.width:
        functions["width"] = str(args.width)
    if args.height:
        functions["height"] = str(args.height)
    if args.orientation:
        functions["orientation"] = args.orientation
    if args.bitdepth:
        functions["bitdepth"] = str(args.bitdepth)
    if args.album:
        functions["album"] = args.album
    if args.artist:
        functions["artist"] = args.artist
    if args.genre:
        functions["genre"] = args.genre
    if args.title:
        functions["title"] = args.title
    if args.track:
        functions["track"] = str(args.track)
    if args.comment:
        functions["comment"] = args.comment

    # Build modifiers
    modifiers = []
    if args.wfn:
        modifiers.append("wfn")
    if args.ww:
        modifiers.append("ww")
    if args.startwith:
        modifiers.append(f"startwith:{args.startwith}")
    if args.endwith:
        modifiers.append(f"endwith:{args.endwith}")
    if args.file_only:
        modifiers.append("file")
    if args.folder_only:
        modifiers.append("folder")

    # Perform search
    if args.macro:
        results = searcher.search_by_macro(args.macro, path=args.path, **vars(args))
    else:
        results = searcher.search(
            query=args.query,
            path=args.path,
            regex=args.regex,
            case=args.case,
            whole_word=args.whole_word,
            match_path=args.match_path,
            sort=args.sort,
            sort_descending=args.descending,
            details=args.details,
            limit=args.limit,
            functions=functions if functions else None,
            modifiers=modifiers if modifiers else None,
        )

    # Output results
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for result in results:
            if args.details:
                print(
                    f"{result['name']} | {result['size']} | {result['date_modified']} | {result['path']}"
                )
            else:
                print(result["full_path"])


if __name__ == "__main__":
    main()
