#!/usr/bin/env python3
"""DropFiles upload wrapper.

Uploads HTML/Markdown content to DropFiles and returns a shareable link.
Encapsulates all curl / JSON / temp-file / WAF-workaround logic so callers
(agents or humans) only need one Shell invocation.

Usage:
  echo "content" | python3 scripts/upload.py [options]
  python3 scripts/upload.py --file path/to/file.md [options]
  python3 scripts/upload.py --content "# Hello" [options]

Run with --help for full options.
"""

import argparse
import json
import os
import random
import subprocess
import sys
import tempfile

API_URL = "https://dropfiles.tokendealhub.com/api/v1/upload"

VALID_TYPES = ("html", "markdown", "auto")
VALID_EXPIRES = ("1h", "1d", "7d", "30d")
VALID_LANGS = ("en", "zh", "auto")


def parse_args():
    p = argparse.ArgumentParser(
        prog="upload.py",
        description="Upload HTML/Markdown content to DropFiles and return a shareable link.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  # From stdin (preferred for piped content)
  echo '# Hello' | python3 scripts/upload.py --type markdown --json

  # From file
  python3 scripts/upload.py --file report.md --expire 7d --json

  # With auto-generated 6-digit password
  python3 scripts/upload.py --file secret.html --generate-password --json
""",
    )
    src = p.add_argument_group("content source (priority: --file > --content > stdin)")
    src.add_argument("--file", metavar="PATH", help="Read content from file")
    src.add_argument("--content", metavar="TEXT", help="Inline content (avoid for large text)")

    opt = p.add_argument_group("upload options")
    opt.add_argument("--type", choices=VALID_TYPES, default="auto",
                     help="Content type (default: auto)")
    opt.add_argument("--expire", choices=VALID_EXPIRES, default="7d",
                     help="Expiry (default: 7d)")
    opt.add_argument("--title", default=None, help="Optional title shown on share page")
    opt.add_argument("--lang", choices=VALID_LANGS, default="auto",
                     help="Language hint (default: auto)")

    pw = p.add_argument_group("password")
    g = pw.add_mutually_exclusive_group()
    g.add_argument("--password", metavar="PWD", help="Use a user-supplied password")
    g.add_argument("--generate-password", action="store_true",
                   help="Generate a random 6-digit numeric password")

    out = p.add_argument_group("output")
    out.add_argument("--json", action="store_true",
                     help="Output full JSON response (for programmatic use)")
    return p.parse_args()


def read_content(args):
    """Read content from --file, --content, or stdin (in priority order)."""
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                return f.read()
        except OSError as e:
            fail(f"Cannot read file {args.file}: {e}", args.json)
    if args.content is not None:
        return args.content
    if not sys.stdin.isatty():
        return sys.stdin.read()
    fail("No content provided. Use --file, --content, or pipe via stdin.", args.json)


def fail(message, json_mode=False, code="LOCAL_ERROR"):
    """Print error to stdout (JSON) or stderr (human) and exit 1."""
    if json_mode:
        print(json.dumps(
            {"success": False, "error": {"code": code, "message": message}},
            ensure_ascii=False,
        ))
    else:
        print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def generate_password():
    """Return a random 6-digit numeric string, e.g. '482917'."""
    return "%06d" % random.randint(0, 999999)


def upload(content, args, generated_password):
    """Build payload, call curl, return parsed JSON response dict."""
    payload = {
        "content": content,
        "type": args.type,
        "expire": args.expire,
        "lang": args.lang,
    }
    if args.title:
        payload["title"] = args.title
    if args.password:
        payload["password"] = args.password
    elif generated_password:
        payload["password"] = generated_password

    tmp_path = None
    try:
        # Always write payload to a temp file — avoids shell-escaping issues
        # regardless of content size or special characters.
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as tmp:
            json.dump(payload, tmp, ensure_ascii=False)
            tmp_path = tmp.name

        # Use curl (not urllib) because Cloudflare WAF blocks Python's HTTP
        # client with HTTP 403 error code 1010. curl is the only reliable client.
        cmd = [
            "curl", "-s", "-S",
            "-X", "POST", API_URL,
            "-H", "Content-Type: application/json",
            "-d", f"@{tmp_path}",
            "-w", "\n%{http_code}",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            fail(
                f"curl failed (exit {result.returncode}): {result.stderr.strip()}",
                args.json, code="NETWORK_ERROR",
            )

        # curl appends "\n<http_code>" via -w. Split on the last newline.
        output = result.stdout
        if "\n" in output:
            body, _, code_str = output.rpartition("\n")
        else:
            body, code_str = "", output

        try:
            http_code = int(code_str.strip())
        except ValueError:
            fail(
                f"Could not parse HTTP status from curl output: {code_str!r}",
                args.json, code="PARSE_ERROR",
            )

        try:
            resp = json.loads(body) if body.strip() else {}
        except json.JSONDecodeError:
            fail(
                f"Could not parse response JSON: {body[:200]!r}",
                args.json, code="PARSE_ERROR",
            )

        if http_code == 201 and resp.get("success"):
            return resp

        # Server returned an error. In JSON mode, pass the server response
        # through as-is (it already has the {success:false, error:{...}} shape).
        if args.json:
            print(json.dumps(resp, ensure_ascii=False))
        else:
            err = resp.get("error", {})
            msg = err.get("message", f"HTTP {http_code}")
            if http_code == 429:
                msg += " (rate limited — wait and retry)"
            elif http_code == 403:
                msg += " (blocked by WAF — retry)"
            print(f"Error: {msg}", file=sys.stderr)
        sys.exit(1)
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass


def main():
    args = parse_args()
    content = read_content(args)
    if not content:
        fail("Content is empty.", args.json, code="CONTENT_REQUIRED")

    generated_password = generate_password() if args.generate_password else None
    resp = upload(content, args, generated_password)
    data = resp.get("data", {})

    if args.json:
        # Pass through server JSON; surface generated password for the agent.
        if generated_password:
            resp["password"] = generated_password
        print(json.dumps(resp, ensure_ascii=False))
    else:
        url = data.get("url", "")
        preview = data.get("preview_url", "")
        expire_at = data.get("expire_at", "")
        print(f"URL: {url}")
        if preview:
            print(f"Preview: {preview}")
        if expire_at:
            print(f"Expires: {expire_at}")
        if generated_password:
            print(f"Password: {generated_password}")
        elif args.password:
            print(f"Password: {args.password}")


if __name__ == "__main__":
    main()
