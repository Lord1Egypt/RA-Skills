#!/usr/bin/env python3
"""CLI entrypoint for CLS unified telegraph queries."""

from __future__ import annotations

import argparse
import json
import sys

from cls_service import ClsService


def main():
    parser = argparse.ArgumentParser(
        description="Unified Cailian Press (CLS) telegraph query CLI"
    )
    subparsers = parser.add_subparsers(dest="query_type", required=True)

    # telegraph subcommand
    p_telegraph = subparsers.add_parser("telegraph", help="Get raw telegraph items")
    p_telegraph.add_argument("--hours", type=int, help="Filter by last N hours")
    p_telegraph.add_argument("--limit", type=int, help="Limit number of results")
    p_telegraph.add_argument(
        "--format", choices=["json", "text", "markdown"], default="json"
    )

    # red subcommand
    p_red = subparsers.add_parser("red", help="Get red/highlighted items (level A/B)")
    p_red.add_argument("--hours", type=int, help="Filter by last N hours")
    p_red.add_argument("--limit", type=int, help="Limit number of results")
    p_red.add_argument(
        "--format", choices=["json", "text", "markdown"], default="json"
    )

    # hot subcommand
    p_hot = subparsers.add_parser("hot", help="Get hot items by reading count")
    p_hot.add_argument("--hours", type=int, help="Filter by last N hours")
    p_hot.add_argument(
        "--min-reading", type=int, default=10000, help="Minimum reading count"
    )
    p_hot.add_argument("--limit", type=int, help="Limit number of results")
    p_hot.add_argument(
        "--format", choices=["json", "text", "markdown"], default="json"
    )

    # article subcommand
    p_article = subparsers.add_parser("article", help="Get article by ID")
    p_article.add_argument("--id", type=int, required=True, help="Article ID")
    p_article.add_argument(
        "--format", choices=["json", "text", "markdown"], default="json"
    )

    args = parser.parse_args()

    service = ClsService()

    # Route to appropriate method
    if args.query_type == "telegraph":
        result = service.get_telegraph(hours=args.hours, limit=args.limit)
    elif args.query_type == "red":
        result = service.get_red(hours=args.hours, limit=args.limit)
    elif args.query_type == "hot":
        result = service.get_hot(
            hours=args.hours, min_reading=args.min_reading, limit=args.limit
        )
    elif args.query_type == "article":
        result = service.get_article(article_id=args.id)
    else:
        parser.print_help()
        sys.exit(1)

    # Output
    if args.format == "json":
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    elif args.format == "text":
        from formatters.text_formatter import format_as_text
        print(format_as_text(result))
    elif args.format == "markdown":
        from formatters.markdown_formatter import format_as_markdown
        print(format_as_markdown(result))


if __name__ == "__main__":
    main()
