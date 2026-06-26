from __future__ import annotations

import argparse

from deviantart_common import DeviantArtError, api_post_form, normalize_bool, sanitize_tags


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Create a DeviantArt journal post")
    p.add_argument("--title", required=True, help="Journal title")
    p.add_argument("--body", default="", help="Journal body")
    p.add_argument("--tags", nargs="*", default=[], help="Journal tags")
    p.add_argument("--is-mature", required=True, help="true/false")
    p.add_argument("--allow-comments", default="true")
    p.add_argument("--cover-image-deviation-id", default=None)
    p.add_argument("--embedded-image-deviation-id", default=None)
    return p


def main() -> int:
    args = build_parser().parse_args()
    payload = {
        "title": args.title,
        "body": args.body,
        "tags": sanitize_tags(args.tags),
        "is_mature": normalize_bool(args.is_mature),
        "allow_comments": normalize_bool(args.allow_comments),
        "cover_image_deviation_id": args.cover_image_deviation_id,
        "embedded_image_deviation_id": args.embedded_image_deviation_id,
    }
    resp = api_post_form("deviation/journal/create", payload)
    print("Journal created.")
    print(f"Deviation ID: {resp.get('deviationid')}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except DeviantArtError as e:
        message = f"ERROR: {e}"
        try:
            print(message)
        except UnicodeEncodeError:
            safe = message.encode("ascii", errors="backslashreplace").decode("ascii")
            print(safe)
        raise SystemExit(1)
