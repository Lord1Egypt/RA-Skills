#!/usr/bin/env python3
"""Query the Deepsky aviation search API and print cited results.

Open, no-auth endpoint. Coverage: ICAO, FAA (14 CFR), EASA, CASA regulations
and aviation manuals. See https://www.deepskyai.com/llms.txt for the full
agent manifest.

Usage:
    deepsky_search.py "minimum fuel requirements for IFR flight"
    deepsky_search.py "EDTO critical fuel scenarios" --count 10
    deepsky_search.py "pilot rest rules" --country US --json
"""

import argparse
import json
import sys
import urllib.error
import urllib.request

API_URL = "https://www.deepskyai.com/api/v1/search"
TIMEOUT_S = 30


def search(query: str, match_count: int = 8) -> dict:
    """POST to the Deepsky search endpoint and return the parsed JSON response.

    Args:
        query: Natural-language aviation query.
        match_count: Number of matches to request (1-20).

    Returns:
        The parsed JSON body as a dict.

    Raises:
        urllib.error.HTTPError on non-2xx responses.
    """
    payload = json.dumps({"query": query, "matchCount": match_count}).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "deepsky-aviation-api-skill/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
        return json.loads(resp.read().decode("utf-8"))


def filter_by_country(matches: list, country: str) -> list:
    """Client-side substring filter on metadata.Country (case-insensitive)."""
    needle = country.lower()
    return [
        m for m in matches
        if needle in str(m.get("metadata", {}).get("Country", "")).lower()
    ]


def format_matches(data: dict) -> str:
    """Render matches as human-readable citations."""
    lines = []
    lines.append(f"Query: {data.get('query')}")
    lines.append(f"Matches: {len(data.get('matches', []))} "
                 f"(source: {data.get('source', 'unknown')})")
    lines.append("=" * 72)
    for i, match in enumerate(data.get("matches", []), start=1):
        meta = match.get("metadata", {}) or {}
        country = meta.get("Country", "?")
        pages = meta.get("Page Numbers")
        heading = match.get("heading_path", "(no heading)")
        content = (match.get("content") or "").strip()
        if len(content) > 600:
            content = content[:600].rstrip() + " ..."
        lines.append(f"\n[{i}] {heading}")
        lines.append(f"    Country: {country}"
                     + (f"  Pages: {pages}" if pages else ""))
        lines.append("")
        for para in content.split("\n"):
            lines.append(f"    {para}")
    lines.append("\n" + "=" * 72)
    lines.append("Source: https://www.deepskyai.com/api/v1/search")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Query the Deepsky aviation search API."
    )
    parser.add_argument("query", help="Natural-language aviation query")
    parser.add_argument(
        "--count", "-n", type=int, default=8,
        help="Number of matches to request (1-20, default 8)",
    )
    parser.add_argument(
        "--country", "-c", default=None,
        help="Client-side filter on metadata.Country (substring, case-insensitive)",
    )
    parser.add_argument(
        "--json", dest="as_json", action="store_true",
        help="Emit raw JSON instead of the formatted view",
    )
    args = parser.parse_args()

    if not 1 <= args.count <= 20:
        print("error: --count must be between 1 and 20", file=sys.stderr)
        return 2

    try:
        data = search(args.query, match_count=args.count)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.reason}", file=sys.stderr)
        try:
            print(e.read().decode("utf-8"), file=sys.stderr)
        except Exception:
            pass
        return 1
    except urllib.error.URLError as e:
        print(f"Network error: {e.reason}", file=sys.stderr)
        return 1

    if args.country:
        data["matches"] = filter_by_country(data.get("matches", []), args.country)

    if args.as_json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(format_matches(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
