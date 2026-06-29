#!/usr/bin/env python3
"""Query Ahrefs' free public Domain Rating endpoint.

No API key required.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

ENDPOINT = "https://api.ahrefs.com/v3/public/domain-rating-free"
USER_AGENT = "ahrefs-domain-rating-free-skill/1.0 (+https://github.com/AIGC-Hackers/ahrefs-domain-rating-free-skill)"


def fetch_domain_rating(target: str, timeout: float) -> dict[str, Any]:
    url = f"{ENDPOINT}?{urllib.parse.urlencode({'target': target})}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            data = json.loads(body)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        try:
            payload = json.loads(body)
            message = payload.get("error", body)
        except json.JSONDecodeError:
            message = body or str(exc)
        return {"target": target, "ok": False, "status": exc.code, "error": message}
    except urllib.error.URLError as exc:
        return {"target": target, "ok": False, "error": str(exc.reason)}
    except TimeoutError:
        return {"target": target, "ok": False, "error": "request timed out"}
    except json.JSONDecodeError as exc:
        return {"target": target, "ok": False, "error": f"invalid JSON response: {exc}"}

    try:
        rating = data["domain_rating"]["domain_rating"]
    except (KeyError, TypeError) as exc:
        return {"target": target, "ok": False, "raw": data, "error": f"unexpected response shape: {exc}"}

    return {"target": target, "ok": True, "domain_rating": rating, "raw": data}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check Ahrefs Domain Rating using the free public endpoint. No API key required."
    )
    parser.add_argument("targets", nargs="+", help="Domain or URL, e.g. ahrefs.com or https://example.com/page")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    parser.add_argument("--raw", action="store_true", help="Print raw Ahrefs JSON response per target")
    parser.add_argument("--timeout", type=float, default=20.0, help="HTTP timeout in seconds, default: 20")
    args = parser.parse_args()

    results = [fetch_domain_rating(target, args.timeout) for target in args.targets]

    if args.raw:
        for result in results:
            if result.get("ok"):
                print(json.dumps(result["raw"], ensure_ascii=False))
            else:
                print(json.dumps(result, ensure_ascii=False), file=sys.stderr)
    elif args.json:
        print(json.dumps([{k: v for k, v in r.items() if k != "raw"} for r in results], ensure_ascii=False, indent=2))
    else:
        width = max(len(r["target"]) for r in results)
        for result in results:
            if result.get("ok"):
                print(f"{result['target']:<{width}}  {result['domain_rating']}")
            else:
                print(f"{result['target']:<{width}}  ERROR: {result.get('error', 'unknown error')}", file=sys.stderr)

    return 0 if all(r.get("ok") for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
