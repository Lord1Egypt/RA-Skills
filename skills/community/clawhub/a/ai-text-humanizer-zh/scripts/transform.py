#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Command-line interface for AI text rewriting."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.rewrite import AIRewriter
from core.utils import read_file, write_file


def main():
    parser = argparse.ArgumentParser(
        description="Rewrite AI-generated text to sound more natural."
    )
    parser.add_argument("input", nargs="?", help="Input file (or read from stdin)")
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    parser.add_argument("-a", "--aggressive", action="store_true", 
                        help="Enable aggressive rewriting (e.g., break long sentences)")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress change log output")
    parser.add_argument("-r", "--rules", help="Path to user-defined rules JSON file")
    
    args = parser.parse_args()
    
    if args.input:
        try:
            text = read_file(args.input)
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        text = sys.stdin.read()
    
    if not text:
        print("Error: No input text provided", file=sys.stderr)
        sys.exit(1)
    
    rewriter = AIRewriter(user_rules_path=args.rules)
    rewritten, changes = rewriter.rewrite(text, aggressive=args.aggressive)
    
    if not args.quiet and changes:
        print(f"Changes ({len(changes)}):", file=sys.stderr)
        for c in changes:
            print(f" • {c}", file=sys.stderr)
    
    if args.output:
        write_file(args.output, rewritten)
        if not args.quiet:
            print(f"→ Saved to {args.output}", file=sys.stderr)
    else:
        print(rewritten)


if __name__ == "__main__":
    main()
