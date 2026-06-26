#!/usr/bin/env python3
"""Search arXiv papers by keyword."""

from __future__ import annotations

import argparse
import json
import sys
import textwrap
from dataclasses import asdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from arxiv_api import DEFAULT_LIMIT, SearchResponse, safe_dir_name, search_papers  # noqa: E402


def default_output_dir(query: str, sort_by: str | None, start_date: str | None, end_date: str | None) -> Path:
    label = safe_dir_name(query) or "search"
    if sort_by:
        label = f"{label}-{sort_by}"
    if start_date and end_date:
        label = f"{label}-{start_date}-to-{end_date}"
    return Path.cwd() / "artifacts" / "arxiv-search" / safe_dir_name(label)


def render_markdown(response: SearchResponse) -> str:
    lines = [
        "# arXiv Search Results",
        "",
        f"- Search query: `{response.search_query}`",
        f"- Sort: `{response.sort_by}`",
        f"- Order: `{response.sort_order}`",
        f"- Start date: `{response.start_date}`" if response.start_date else "- Start date: none",
        f"- End date: `{response.end_date}`" if response.end_date else "- End date: none",
        f"- Total matches: {response.total_results}",
        f"- Returned results: {response.returned_results}",
        "",
    ]

    if not response.entries:
        lines.extend(
            [
                "No papers matched the search.",
                "",
                "Try a broader keyword or switch the sort order.",
            ]
        )
        return "\n".join(lines).strip() + "\n"

    for index, entry in enumerate(response.entries, start=1):
        lines.extend(
            [
                f"{index}. {entry.title} (`{entry.paper_id}`)",
                f"   - Authors: {', '.join(entry.authors) if entry.authors else 'Unknown'}",
                f"   - Categories: {', '.join(entry.categories) if entry.categories else 'Unknown'}",
                f"   - Published: {entry.published or 'Unknown'}",
                f"   - Updated: {entry.updated or 'Unknown'}",
                f"   - Abstract URL: {entry.abstract_url}",
                f"   - PDF: {entry.pdf_url}",
                f"   - Abstract: {entry.abstract or 'No abstract available.'}",
                "",
            ]
        )

    return "\n".join(lines).strip() + "\n"


def write_search_outputs(output_dir: Path, response: SearchResponse) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "search_results.json"
    md_path = output_dir / "search_results.md"
    payload = {
        "search_query": response.search_query,
        "sort_by": response.sort_by,
        "sort_order": response.sort_order,
        "start_date": response.start_date,
        "end_date": response.end_date,
        "total_results": response.total_results,
        "returned_results": response.returned_results,
        "results": [asdict(entry) for entry in response.entries],
    }
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(response), encoding="utf-8")
    return {"json": json_path, "md": md_path}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Search arXiv by keyword, then write JSON and Markdown result files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
            Examples:
              python search_arxiv.py --query transformer
              python search_arxiv.py --query transformer --sort submittedDate --limit 5
              python search_arxiv.py --query "computer vision diffusion" --sort submittedDate
              python search_arxiv.py --query "agent security" --start-date 2026-03-01 --end-date 2026-03-07 --sort submittedDate
            """
        ),
    )
    parser.add_argument("--query", help="plain text keywords to search", required=True)
    parser.add_argument("--start-date", help="inclusive submittedDate lower bound in YYYY-MM-DD", default=None)
    parser.add_argument("--end-date", help="inclusive submittedDate upper bound in YYYY-MM-DD", default=None)
    parser.add_argument("--sort", choices=["relevance", "submittedDate", "lastUpdatedDate"], default=None)
    parser.add_argument("--order", choices=["ascending", "descending"], default="descending")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--output-dir", type=Path, help="directory for search_results.json and search_results.md")
    parser.add_argument("--timeout", type=float, default=30.0, help="network timeout in seconds")
    args = parser.parse_args(argv)

    try:
        response = search_papers(
            args.query,
            start_date=args.start_date,
            end_date=args.end_date,
            sort_by=args.sort,
            sort_order=args.order,
            limit=args.limit,
            timeout=args.timeout,
        )
        output_dir = args.output_dir or default_output_dir(args.query, response.sort_by, response.start_date, response.end_date)
        outputs = write_search_outputs(output_dir, response)
        print(
            json.dumps(
                {
                    "output_dir": str(output_dir),
                    "search_results_json": str(outputs["json"]),
                    "search_results_md": str(outputs["md"]),
                    "search_query": response.search_query,
                    "sort_by": response.sort_by,
                    "sort_order": response.sort_order,
                    "start_date": response.start_date,
                    "end_date": response.end_date,
                    "total_results": response.total_results,
                    "returned_results": response.returned_results,
                },
                ensure_ascii=False,
            )
        )
        return 0
    except Exception as error:  # pragma: no cover - surfaced in CLI output
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
