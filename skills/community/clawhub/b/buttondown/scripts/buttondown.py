#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


DEFAULT_API_BASE = "https://api.buttondown.com/v1"


def die(message, code=2):
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(code)


def get_api_key(required=True):
    api_key = os.environ.get("BUTTONDOWN_API_KEY", "").strip()
    if api_key:
        return api_key
    if required:
        die("set BUTTONDOWN_API_KEY in the environment or configure it through your runtime secret store")
    return ""


def redact(text, api_key):
    if api_key:
        text = text.replace(api_key, "[REDACTED]")
    return text


def read_body(path, editor_mode):
    with open(path, "r", encoding="utf-8") as handle:
        body = handle.read()
    if body.startswith("---\n"):
        die("body starts with YAML frontmatter; strip it before uploading to Buttondown")
    if editor_mode:
        marker = f"<!-- buttondown-editor-mode: {editor_mode} -->"
        if not body.startswith("<!-- buttondown-editor-mode:"):
            body = marker + body
    return body


def parse_metadata(raw):
    if not raw:
        return None
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        die(f"--metadata-json must be valid JSON: {exc}")
    if not isinstance(value, dict):
        die("--metadata-json must decode to an object")
    return value


def add_common_email_fields(parser, require_subject=False):
    parser.add_argument("--subject", required=require_subject)
    parser.add_argument("--body-file")
    parser.add_argument("--editor-mode", choices=["plaintext", "fancy"])
    parser.add_argument("--slug")
    parser.add_argument("--description")
    parser.add_argument("--canonical-url")
    parser.add_argument("--image")
    parser.add_argument("--archival-mode", choices=[
        "disabled",
        "enabled",
        "enabled_for_paid_subscribers",
        "enabled_for_subscribers",
    ])
    parser.add_argument("--commenting-mode", choices=[
        "disabled",
        "enabled",
        "enabled_for_paid_subscribers",
    ])
    parser.add_argument("--metadata-json")
    parser.add_argument("--secondary-id", type=int)
    parser.add_argument("--featured", action="store_true")
    parser.add_argument("--related-email-id", action="append", default=[])
    parser.add_argument("--dry-run", action="store_true")


def build_email_payload(args, create=False):
    payload = {}
    if create:
        payload["status"] = "draft"
    for attr, key in [
        ("subject", "subject"),
        ("slug", "slug"),
        ("description", "description"),
        ("canonical_url", "canonical_url"),
        ("image", "image"),
        ("archival_mode", "archival_mode"),
        ("commenting_mode", "commenting_mode"),
        ("secondary_id", "secondary_id"),
    ]:
        value = getattr(args, attr, None)
        if value is not None:
            payload[key] = value
    if getattr(args, "body_file", None):
        payload["body"] = read_body(args.body_file, args.editor_mode)
    metadata = parse_metadata(getattr(args, "metadata_json", None))
    if metadata is not None:
        payload["metadata"] = metadata
    if getattr(args, "featured", False):
        payload["featured"] = True
    if getattr(args, "related_email_id", None):
        payload["related_email_ids"] = args.related_email_id
    if create and not payload.get("subject"):
        die("--subject is required")
    if create and "body" not in payload:
        die("--body-file is required")
    return payload


def request(method, path, payload=None, query=None, context=None, dry_run=False):
    api_key = get_api_key(required=not dry_run)
    base = os.environ.get("BUTTONDOWN_API_BASE", DEFAULT_API_BASE).rstrip("/")
    url = f"{base}{path}"
    if query:
        url += "?" + urllib.parse.urlencode(query)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    if api_key:
        headers["Authorization"] = f"Token {api_key}"
    context = context or os.environ.get("BUTTONDOWN_CONTEXT")
    if context:
        headers["Buttondown-Context"] = context

    body = None if payload is None else json.dumps(payload).encode()
    if dry_run:
        preview = {
            "method": method,
            "url": url,
            "headers": {**headers, "Authorization": "[REDACTED]" if api_key else "[unset]"},
            "json": payload,
        }
        print(json.dumps(preview, indent=2, ensure_ascii=False))
        return None

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            text = response.read().decode()
            if not text:
                return {}
            return json.loads(text)
    except urllib.error.HTTPError as exc:
        text = exc.read().decode(errors="replace")
        safe = redact(text, api_key)
        try:
            data = json.loads(safe)
            detail = data.get("detail") or data
        except Exception:
            detail = safe
        die(f"Buttondown HTTP {exc.code}: {detail}", code=1)
    except urllib.error.URLError as exc:
        die(f"Buttondown request failed: {exc}", code=1)


def print_json(data):
    if data is not None:
        print(json.dumps(data, indent=2, ensure_ascii=False))


def command_create_draft(args):
    payload = build_email_payload(args, create=True)
    print_json(request("POST", "/emails", payload, context=args.context, dry_run=args.dry_run))


def command_update_draft(args):
    payload = build_email_payload(args, create=False)
    if not payload:
        die("nothing to update")
    print_json(request("PATCH", f"/emails/{args.email_id}", payload, context=args.context, dry_run=args.dry_run))


def command_get(args):
    print_json(request("GET", f"/emails/{args.email_id}", context=args.context))


def command_render(args):
    print_json(request("GET", f"/emails/{args.email_id}/renders", context=args.context))


def command_list(args):
    query = {}
    if args.status:
        query["status"] = args.status
    print_json(request("GET", "/emails", query=query, context=args.context))


def command_send_draft(args):
    payload = {}
    if args.recipient:
        payload["recipients"] = args.recipient
    if args.subscriber:
        payload["subscribers"] = args.subscriber
    if not payload:
        die("provide --recipient or --subscriber")
    print_json(request("POST", f"/emails/{args.email_id}/send-draft", payload, context=args.context, dry_run=args.dry_run))


def main():
    parser = argparse.ArgumentParser(description="Buttondown API helper for draft-first email workflows.")
    parser.add_argument("--context", help="Buttondown newsletter username for Buttondown-Context header")
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create-draft", help="Create a Buttondown draft email")
    add_common_email_fields(create, require_subject=True)
    create.set_defaults(func=command_create_draft)

    update = sub.add_parser("update-draft", help="Update an existing Buttondown email")
    update.add_argument("email_id")
    add_common_email_fields(update, require_subject=False)
    update.set_defaults(func=command_update_draft)

    get = sub.add_parser("get", help="Retrieve an email")
    get.add_argument("email_id")
    get.set_defaults(func=command_get)

    render = sub.add_parser("render", help="Retrieve rendered HTML for an email")
    render.add_argument("email_id")
    render.set_defaults(func=command_render)

    list_cmd = sub.add_parser("list", help="List emails")
    list_cmd.add_argument("--status")
    list_cmd.set_defaults(func=command_list)

    send = sub.add_parser("send-draft", help="Send a draft preview to recipients or subscribers")
    send.add_argument("email_id")
    send.add_argument("--recipient", action="append", default=[])
    send.add_argument("--subscriber", action="append", default=[])
    send.add_argument("--dry-run", action="store_true")
    send.set_defaults(func=command_send_draft)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
