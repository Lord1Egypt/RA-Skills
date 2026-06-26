from __future__ import annotations

import argparse
import csv
import json
import os
import ssl
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

try:
    import certifi  # type: ignore
except Exception:
    certifi = None

API_BASE = "https://api-ssl.bitly.com/v4"
DEFAULT_ENV_FILE = Path(r"C:\Users\Big Dell\.openclaw\bitly.env")
LEGACY_JSON_FILE = Path(r"C:\Users\Big Dell\.openclaw\bitly-credentials.json")


class BitlyError(Exception):
    pass


def load_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def load_credentials() -> dict[str, Any]:
    env_path = Path(os.environ.get("BITLY_ENV_FILE", DEFAULT_ENV_FILE))
    file_env = load_dotenv(env_path)

    merged = {
        "client_id": os.environ.get("BITLY_CLIENT_ID") or file_env.get("BITLY_CLIENT_ID"),
        "client_secret": os.environ.get("BITLY_CLIENT_SECRET") or file_env.get("BITLY_CLIENT_SECRET"),
        "access_token": os.environ.get("BITLY_ACCESS_TOKEN") or file_env.get("BITLY_ACCESS_TOKEN"),
        "redirect_uri": os.environ.get("BITLY_REDIRECT_URI") or file_env.get("BITLY_REDIRECT_URI"),
        "default_group_guid": os.environ.get("BITLY_DEFAULT_GROUP_GUID") or file_env.get("BITLY_DEFAULT_GROUP_GUID"),
        "env_file": str(env_path),
    }

    if not merged["access_token"] and LEGACY_JSON_FILE.exists():
        data = json.loads(LEGACY_JSON_FILE.read_text(encoding="utf-8"))
        merged["client_id"] = merged["client_id"] or data.get("client_id")
        merged["client_secret"] = merged["client_secret"] or data.get("client_secret")
        merged["access_token"] = merged["access_token"] or data.get("access_token")
        merged["redirect_uri"] = merged["redirect_uri"] or data.get("redirect_uri")

    if not merged["access_token"]:
        raise BitlyError(f"No access token found. Set BITLY_ACCESS_TOKEN in {env_path}")
    return merged


def ssl_context() -> ssl.SSLContext:
    return ssl.create_default_context(cafile=certifi.where()) if certifi else ssl.create_default_context()


def request_json(method: str, endpoint: str, token: str, payload: dict[str, Any] | None = None, query: dict[str, Any] | None = None) -> dict[str, Any]:
    url = f"{API_BASE}/{endpoint.lstrip('/')}"
    if query:
        url += "?" + urllib.parse.urlencode({k: v for k, v in query.items() if v is not None and v != ''})
    data = None
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "OpenClaw-Bitly-URL-Shortner-and-Manager/0.3",
    }
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, context=ssl_context()) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise BitlyError(f"HTTP {e.code}: {body}") from e
    except urllib.error.URLError as e:
        raise BitlyError(f"Network/SSL error: {e}") from e
    try:
        return json.loads(body)
    except json.JSONDecodeError as e:
        raise BitlyError(f"Non-JSON response: {body}") from e


def emit(data: Any, as_csv: bool = False) -> None:
    if not as_csv:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return
    rows = data if isinstance(data, list) else data.get("links") or data.get("groups") or data.get("metrics") or data.get("results") or []
    if not isinstance(rows, list) or not rows:
        print("")
        return
    keys = sorted({k for row in rows if isinstance(row, dict) for k in row.keys()})
    writer = csv.DictWriter(__import__('sys').stdout, fieldnames=keys)
    writer.writeheader()
    for row in rows:
        if isinstance(row, dict):
            writer.writerow({k: row.get(k) for k in keys})


def write_output(path: str | None, data: Any) -> None:
    if not path:
        return
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def pick_group_guid(token: str, explicit: str | None, creds: dict[str, Any]) -> str:
    if explicit:
        return explicit
    if creds.get("default_group_guid"):
        return str(creds["default_group_guid"])
    groups = request_json("GET", "groups", token)
    items = groups.get("groups") or []
    if not items:
        raise BitlyError("No groups available for this token")
    guid = items[0].get("guid")
    if not guid:
        raise BitlyError("Could not determine a default group GUID")
    return str(guid)


def fetch_group_bitlinks(token: str, guid: str, limit: int, query: str | None = None) -> dict[str, Any]:
    return request_json("GET", f"groups/{guid}/bitlinks", token, query={"size": limit, "query": query})


def filter_links(rows: list[dict[str, Any]], *, tag: str | None = None, domain: str | None = None, text: str | None = None) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        if tag:
            tags = [str(t).lower() for t in (row.get("tags") or [])]
            if tag.lower() not in tags:
                continue
        if domain:
            long_url = str(row.get("long_url") or "")
            if domain.lower() not in long_url.lower() and domain.lower() not in str(row.get("link") or "").lower():
                continue
        if text:
            blob = " ".join([str(row.get("title") or ""), str(row.get("long_url") or ""), str(row.get("link") or "")])
            if text.lower() not in blob.lower():
                continue
        out.append(row)
    return out


def cmd_whoami(args: argparse.Namespace) -> int:
    creds = load_credentials()
    data = request_json("GET", "user", creds["access_token"])
    emit(data, args.csv)
    return 0


def cmd_groups(args: argparse.Namespace) -> int:
    creds = load_credentials()
    data = request_json("GET", "groups", creds["access_token"])
    emit(data, args.csv)
    return 0


def cmd_bitlinks(args: argparse.Namespace) -> int:
    creds = load_credentials()
    guid = pick_group_guid(creds["access_token"], args.group_guid, creds)
    data = fetch_group_bitlinks(creds["access_token"], guid, args.limit, args.query)
    rows = data.get("links") or []
    rows = filter_links(rows, tag=args.tag, domain=args.domain, text=args.contains)
    out = {"links": rows, "pagination": data.get("pagination")}
    write_output(args.output, out)
    emit(out, args.csv)
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    return cmd_bitlinks(args)


def cmd_shorten(args: argparse.Namespace) -> int:
    creds = load_credentials()
    guid = pick_group_guid(creds["access_token"], args.group_guid, creds)
    payload: dict[str, Any] = {"long_url": args.long_url, "group_guid": guid}
    if args.domain:
        payload["domain"] = args.domain
    if args.title:
        payload["title"] = args.title
    data = request_json("POST", "shorten", creds["access_token"], payload=payload)
    emit(data, args.csv)
    return 0


def cmd_expand(args: argparse.Namespace) -> int:
    creds = load_credentials()
    bitlink = args.bitlink.replace("https://", "").replace("http://", "")
    data = request_json("GET", f"bitlinks/{bitlink}", creds["access_token"])
    emit(data, args.csv)
    return 0


def cmd_clicks(args: argparse.Namespace) -> int:
    creds = load_credentials()
    bitlink = args.bitlink.replace("https://", "").replace("http://", "")
    data = request_json("GET", f"bitlinks/{bitlink}/clicks", creds["access_token"], query={"unit": args.unit, "units": args.units, "size": args.limit})
    emit(data, args.csv)
    return 0


def cmd_create_custom(args: argparse.Namespace) -> int:
    creds = load_credentials()
    bitlink = args.bitlink.replace("https://", "").replace("http://", "")
    payload = {"bitlink_id": bitlink}
    data = request_json("POST", "custom_bitlinks", creds["access_token"], payload=payload, query={"custom_bitlink": args.custom_bitlink})
    emit(data, args.csv)
    return 0


def cmd_bulk_shorten(args: argparse.Namespace) -> int:
    creds = load_credentials()
    guid = pick_group_guid(creds["access_token"], args.group_guid, creds)
    urls = [line.strip() for line in Path(args.input).read_text(encoding="utf-8").splitlines() if line.strip()]
    results = []
    for url in urls:
        payload = {"long_url": url, "group_guid": guid}
        if args.domain:
            payload["domain"] = args.domain
        try:
            data = request_json("POST", "shorten", creds["access_token"], payload=payload)
            results.append({"long_url": url, "link": data.get("link"), "id": data.get("id")})
        except Exception as e:
            results.append({"long_url": url, "error": str(e)})
    out = {"results": results}
    write_output(args.output, out)
    emit(results, args.csv)
    return 0


def cmd_export_links(args: argparse.Namespace) -> int:
    creds = load_credentials()
    guid = pick_group_guid(creds["access_token"], args.group_guid, creds)
    data = fetch_group_bitlinks(creds["access_token"], guid, args.limit, args.query)
    rows = data.get("links") or []
    rows = filter_links(rows, tag=args.tag, domain=args.domain, text=args.contains)
    out = {"links": rows}
    if not args.output:
        raise BitlyError("--output is required for export-links")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    if args.format == 'json':
        output.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding='utf-8')
    elif args.format == 'txt':
        output.write_text("\n".join(str(r.get('link')) for r in rows if r.get('link')) + "\n", encoding='utf-8')
    elif args.format == 'csv':
        keys = sorted({k for row in rows if isinstance(row, dict) for k in row.keys()})
        with output.open('w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for row in rows:
                writer.writerow({k: row.get(k) for k in keys})
    print(str(output))
    return 0


def cmd_env_template(args: argparse.Namespace) -> int:
    template = "\n".join([
        "BITLY_CLIENT_ID=",
        "BITLY_CLIENT_SECRET=",
        "BITLY_ACCESS_TOKEN=",
        "BITLY_REDIRECT_URI=http://127.0.0.1:8765/callback",
        "BITLY_DEFAULT_GROUP_GUID=",
        "",
    ])
    if args.output:
        Path(args.output).write_text(template, encoding='utf-8')
        print(args.output)
    else:
        print(template, end='')
    return 0


def add_common_format_arg(p: argparse.ArgumentParser) -> None:
    p.add_argument("--csv", action="store_true", help="Emit flat CSV instead of JSON when possible")


def add_link_filters(p: argparse.ArgumentParser) -> None:
    p.add_argument("--tag", default=None, help="Filter links by exact tag value")
    p.add_argument("--domain", default=None, help="Filter links by domain fragment in long/short URL")
    p.add_argument("--contains", default=None, help="Filter links by text contained in title or URLs")
    p.add_argument("--output", default=None, help="Optional output file path")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Bitly URL Shortner and Manager")
    sub = p.add_subparsers(dest="command", required=True)

    who = sub.add_parser("whoami", help="Verify auth and show account info")
    add_common_format_arg(who)
    who.set_defaults(func=cmd_whoami)

    groups = sub.add_parser("groups", help="List accessible groups")
    add_common_format_arg(groups)
    groups.set_defaults(func=cmd_groups)

    bitlinks = sub.add_parser("bitlinks", help="List recent bitlinks")
    bitlinks.add_argument("--limit", type=int, default=10)
    bitlinks.add_argument("--group-guid", default=None)
    bitlinks.add_argument("--query", default=None)
    add_link_filters(bitlinks)
    add_common_format_arg(bitlinks)
    bitlinks.set_defaults(func=cmd_bitlinks)

    search = sub.add_parser("search", help="Search bitlinks by text query")
    search.add_argument("--query", required=True)
    search.add_argument("--limit", type=int, default=10)
    search.add_argument("--group-guid", default=None)
    add_link_filters(search)
    add_common_format_arg(search)
    search.set_defaults(func=cmd_search)

    shorten = sub.add_parser("shorten", help="Create a short link")
    shorten.add_argument("--long-url", required=True)
    shorten.add_argument("--group-guid", default=None)
    shorten.add_argument("--domain", default=None)
    shorten.add_argument("--title", default=None)
    add_common_format_arg(shorten)
    shorten.set_defaults(func=cmd_shorten)

    expand = sub.add_parser("expand", help="Inspect a bitlink")
    expand.add_argument("--bitlink", required=True)
    add_common_format_arg(expand)
    expand.set_defaults(func=cmd_expand)

    clicks = sub.add_parser("clicks", help="Show click metrics for a bitlink")
    clicks.add_argument("--bitlink", required=True)
    clicks.add_argument("--unit", default="day", choices=["minute", "hour", "day", "week", "month"])
    clicks.add_argument("--units", type=int, default=-1)
    clicks.add_argument("--limit", type=int, default=50)
    add_common_format_arg(clicks)
    clicks.set_defaults(func=cmd_clicks)

    custom = sub.add_parser("create-custom", help="Create a custom bitlink alias")
    custom.add_argument("--bitlink", required=True, help="Existing bitlink, e.g. bit.ly/abc123")
    custom.add_argument("--custom-bitlink", required=True, help="Desired custom alias, e.g. yourdomain.com/campaign")
    add_common_format_arg(custom)
    custom.set_defaults(func=cmd_create_custom)

    bulk = sub.add_parser("bulk-shorten", help="Shorten many URLs from a txt file")
    bulk.add_argument("--input", required=True, help="Path to txt file with one URL per line")
    bulk.add_argument("--output", default=None, help="Optional JSON output path")
    bulk.add_argument("--group-guid", default=None)
    bulk.add_argument("--domain", default=None)
    add_common_format_arg(bulk)
    bulk.set_defaults(func=cmd_bulk_shorten)

    export = sub.add_parser("export-links", help="Export filtered links to json/txt/csv")
    export.add_argument("--limit", type=int, default=100)
    export.add_argument("--group-guid", default=None)
    export.add_argument("--query", default=None)
    export.add_argument("--format", choices=["json", "txt", "csv"], default="json")
    add_link_filters(export)
    export.set_defaults(func=cmd_export_links)

    env = sub.add_parser("env-template", help="Print or write a local .env template")
    env.add_argument("--output", default=None)
    env.set_defaults(func=cmd_env_template)
    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
