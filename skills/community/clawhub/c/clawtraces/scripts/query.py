# FILE_META
# INPUT:  API key
# OUTPUT: JSON list of submitted sessions with metadata
# POS:    skill scripts — utility, depends on lib/auth.py
# MISSION: Query the server for previously submitted sessions.

#!/usr/bin/env python3
"""Query submitted trajectories from the ClawTraces server.

Usage:
    python query.py [--page N] [--page-size N]
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from lib.auth import get_server_url, get_stored_key, handle_401, get_ssl_context, _format_connection_error
from lib.version import default_headers, exit_if_upgrade_required


def query_submissions(server_url: str, secret_key: str,
                      page: int = 1, page_size: int = 100) -> dict:
    """Query submissions from server."""
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError

    url = f"{server_url}/submissions?page={page}&page_size={page_size}"
    req = Request(url, headers=default_headers(secret_key), method="GET")

    try:
        with urlopen(req, timeout=30, context=get_ssl_context()) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        if e.code == 401:
            handle_401()
            return {"error": "unauthorized"}
        error_body = e.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(error_body)
            exit_if_upgrade_required(parsed)
            if "error" not in parsed:
                parsed["error"] = f"HTTP {e.code}"
            return parsed
        except (json.JSONDecodeError, ValueError):
            return {"error": f"HTTP {e.code}", "detail": error_body}
    except URLError as e:
        return {"error": _format_connection_error(e.reason)}


def main():
    parser = argparse.ArgumentParser(description="Query ClawTraces submissions")
    parser.add_argument("--page", type=int, default=1, help="Page number")
    parser.add_argument("--page-size", type=int, default=100, help="Items per page")
    args = parser.parse_args()

    key = get_stored_key()
    if not key:
        print("Not authenticated. Please run /clawtraces to authenticate first.", file=sys.stderr)
        sys.exit(1)

    server_url = get_server_url()

    result = query_submissions(server_url, key, args.page, args.page_size)

    if "error" in result:
        print(f"Error: {result.get('message') or result['error']}", file=sys.stderr)
        sys.exit(1)

    # Output formatted result
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
