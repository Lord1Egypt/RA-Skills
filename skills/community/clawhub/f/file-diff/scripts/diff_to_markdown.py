#!/usr/bin/env python3
"""
File Diff to Markdown - Convert diff output to readable markdown format

Usage:
    diff_to_markdown.py <source_file> <target_file>

Example:
    diff_to_markdown.py /path/to/original.md /path/to/modified.md
"""

import subprocess
import sys
from pathlib import Path


def run_diff(source, target):
    """Run diff command and return unified output."""
    try:
        result = subprocess.run(
            ["diff", "-u", source, target],
            capture_output=True,
            text=True
        )
        return result.stdout, result.returncode
    except FileNotFoundError:
        print("[ERROR] diff command not found")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)


def parse_diff_to_markdown(source, target, diff_output, returncode):
    """Convert diff output to markdown format."""
    
    lines = diff_output.split("\n")
    
    output = []
    output.append(f"**File A**: `{source}`")
    output.append(f"**File B**: `{target}`")
    output.append("")
    output.append("## Differences")
    output.append("")
    
    if returncode == 0:
        output.append("_No differences found._")
        return "\n".join(output)
    
    # Skip the first two lines (--- and +++)
    content_lines = lines[3:] if len(lines) > 3 else []
    
    current_hunk = []
    changes = []
    
    for line in content_lines:
        if line.startswith("@@"):
            if current_hunk:
                changes.append("\n".join(current_hunk))
            current_hunk = [line]
        else:
            current_hunk.append(line)
    
    if current_hunk:
        changes.append("\n".join(current_hunk))
    
    if changes:
        output.append("```diff")
        for change in changes:
            output.append(change)
        output.append("```")
    else:
        output.append("_No differences found._")
    
    return "\n".join(output)


def main():
    if len(sys.argv) != 3:
        print("Usage: diff_to_markdown.py <source_file> <target_file>")
        sys.exit(1)
    
    source = sys.argv[1]
    target = sys.argv[2]
    
    # Verify files exist
    if not Path(source).exists():
        print(f"[ERROR] Source file not found: {source}")
        sys.exit(1)
    if not Path(target).exists():
        print(f"[ERROR] Target file not found: {target}")
        sys.exit(1)
    
    diff_output, returncode = run_diff(source, target)
    markdown = parse_diff_to_markdown(source, target, diff_output, returncode)
    
    print(markdown)


if __name__ == "__main__":
    main()
