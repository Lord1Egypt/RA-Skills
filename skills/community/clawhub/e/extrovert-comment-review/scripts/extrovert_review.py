#!/usr/bin/env python3
"""Read-only Extrovert campaign and comment review. Python standard library only."""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.goextrovert.com/client/v2"
MAX_BYTES = 4 * 1024 * 1024
VIEWS = ("Need approval", "Pending", "Error", "Posted", "Skipped")
UUID = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\Z")


class ReviewError(Exception):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ReviewError("Redirect refused; API key was not forwarded.")


def identifier(value):
    if not UUID.fullmatch(value):
        raise argparse.ArgumentTypeError("Expected an exact UUID; no URL or path accepted.")
    return value


def bounded(minimum, maximum):
    def parse(value):
        number = int(value)
        if not minimum <= number <= maximum:
            raise argparse.ArgumentTypeError(f"Expected {minimum}..{maximum}.")
        return number
    return parse


def request_json(path, params, key):
    # No arbitrary endpoints, base overrides, proxies, redirects, or mutations.
    if path not in ("/campaign", "/comments"):
        raise ReviewError("Endpoint is not allowlisted.")
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"X-API-Key": key, "Accept": "application/json"}, method="GET")
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    try:
        with opener.open(req, timeout=30) as response:
            if response.status != 200:
                raise ReviewError("Unexpected API status.")
            raw = response.read(MAX_BYTES + 1)
            if len(raw) > MAX_BYTES:
                raise ReviewError("API response exceeds the 4 MiB safety limit.")
    except urllib.error.HTTPError as exc:
        hints = {401: "Check your API key.", 403: "Check account permissions and plan access.", 429: "Rate limited; retry later manually."}
        code = exc.code
        exc.close()
        raise ReviewError(f"API HTTP {code}. {hints.get(code, 'No automatic retry was made.')}") from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise ReviewError("API connection failed; no automatic retry was made.") from None
    try:
        result = json.loads(raw)
    except (ValueError, UnicodeError):
        raise ReviewError("API returned invalid JSON.") from None
    if not isinstance(result, dict) or result.get("status") != "success" or "data" not in result:
        raise ReviewError("API response did not contain a successful data envelope.")
    return result["data"]


def campaigns(key):
    data = request_json("/campaign", {}, key)
    if not isinstance(data, list):
        raise ReviewError("Campaign response shape changed; consult the API docs.")
    # Avoid exposing full user, outreach configuration and workspace records.
    return [{"id": c["id"], "name": c["name"], "ownerId": c["owner"]["id"],
             "ownerName": c["owner"].get("name"), "isActive": c["isActive"]}
            for c in data if not c.get("isDeleted", False)]


def review(args, key):
    visible = campaigns(key)
    campaign = next((c for c in visible if c["id"] == args.campaign), None)
    if campaign is None or campaign["ownerId"] != args.owner:
        raise ReviewError("Campaign/owner pair does not match a visible, non-deleted campaign.")
    params = {"ownerId": args.owner, "campaignId": args.campaign, "view": args.view,
              "limit": args.limit, "offset": args.offset}
    data = request_json("/comments", params, key)
    if not isinstance(data, dict) or not isinstance(data.get("comments"), list) or not isinstance(data.get("pagination"), dict):
        raise ReviewError("Comment response shape changed; consult the API docs.")
    comments = []
    for item in data["comments"]:
        if item["ownerId"] != args.owner or item["campaign"]["id"] != args.campaign:
            raise ReviewError("Returned comment does not match requested campaign/owner.")
        comments.append({k: item.get(k) for k in ("postId", "ownerId", "campaign", "author", "post", "draft", "reactionBehavior", "state", "allowedActions", "plannedAt", "updatedAt", "error")})
    return {"readOnly": True, "campaign": campaign, "view": args.view,
            "pagination": data["pagination"], "comments": comments}


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("campaigns", help="List accessible campaigns and their owner IDs.")
    q = sub.add_parser("queue", help="Read one page for an explicitly selected campaign and owner.")
    q.add_argument("--campaign", required=True, type=identifier)
    q.add_argument("--owner", required=True, type=identifier)
    q.add_argument("--view", choices=VIEWS, default="Need approval")
    q.add_argument("--limit", type=bounded(1, 50), default=10)
    q.add_argument("--offset", type=bounded(0, 2147483647), default=0)
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    key = os.environ.get("EXTROVERT_API_KEY", "")
    if not key or any(ord(c) < 33 or ord(c) > 126 for c in key):
        print("Set EXTROVERT_API_KEY securely to a nonempty ASCII API key (no spaces).", file=sys.stderr)
        return 2
    try:
        output = campaigns(key) if args.command == "campaigns" else review(args, key)
        # Defensive redaction if an upstream field happens to contain the key.
        rendered = json.dumps(output, ensure_ascii=True, indent=2).replace(
            json.dumps(key, ensure_ascii=True)[1:-1], "[REDACTED]")
        print(rendered)
        return 0
    except ReviewError as exc:
        print(str(exc).replace(key, "[REDACTED]"), file=sys.stderr)
        return 1
    except (KeyError, TypeError, ValueError):
        print("Unexpected API data shape; consult the API docs. No changes were made.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
