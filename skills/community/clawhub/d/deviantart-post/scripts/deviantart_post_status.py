from __future__ import annotations

import argparse

from deviantart_common import DeviantArtError, api_post_form


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Post a DeviantArt status update")
    p.add_argument("--body", required=True, help="Status body text")
    return p


def main() -> int:
    args = build_parser().parse_args()
    resp = api_post_form("user/statuses/post", {"body": args.body})
    print("Status posted.")
    print(f"Response: {resp}")
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
