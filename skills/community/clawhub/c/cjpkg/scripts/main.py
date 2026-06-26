#!/usr/bin/env python3
"""Search or download Cangjie packages per devdoc.md."""

from __future__ import annotations

import argparse
import json
import os
import pprint
import sys
import urllib.error
import urllib.parse
import urllib.request

import toml

SEARCH_URL = "https://pkg.cangjie-lang.cn/v1/artifact/searchPackages"
REGISTRY_BASE = "https://pkg.cangjie-lang.cn/registry/pkg"
DOWNLOAD_DIR = os.path.expanduser("~/Downloads")

def _build_toml_key_parts(key_args: list[str]) -> list[str] | None:
    """One CLI arg: allow dots (e.g. owner.name). Multiple args: each is one level (owner name)."""
    if not key_args:
        return None
    cleaned = [a.strip() for a in key_args if a.strip()]
    if not cleaned:
        return None
    if len(cleaned) == 1:
        parts = [p for p in cleaned[0].split(".") if p != ""]
    else:
        parts = cleaned
    return parts if parts else None


def _lookup_toml_nested(data: object, parts: list[str]) -> tuple[object | None, str | None]:
    """Walk like fileobj[key1], then fileobj[key1][key2], …; return (value, None) or (None, error)."""
    cur: object = data
    prefix: list[str] = []
    for i, segment in enumerate(parts):
        if not isinstance(cur, dict):
            loc = ".".join(prefix) if prefix else "<root>"
            return None, f"Not a table at '{loc}'; cannot look up '{segment}'."
        if segment not in cur:
            if i == 0:
                return None, f"Top-level key does not exist: {segment}"
            return None, f"Key does not exist under '{'.'.join(prefix)}': {segment}"
        prefix.append(segment)
        cur = cur[segment]
    return cur, None


def cmd_toml_get(toml_path: str, key_args: list[str]) -> int:
    toml_path = toml_path.strip()
    if not toml_path:
        print("TOML path must not be empty.")
        return 1

    parts = _build_toml_key_parts(key_args)
    if not parts:
        print("At least one key segment is required (e.g. KEY1 or KEY1 KEY2).")
        return 1

    path = os.path.expanduser(toml_path)
    if not os.path.isfile(path):
        print(f"File not found: {path}")
        return 1

    try:
        with open(path, encoding="utf-8") as f:
            data = toml.load(f)
    except toml.TomlDecodeError as e:
        print(f"Invalid TOML: {e}")
        return 1
    except OSError as e:
        print(f"Cannot read file: {e}")
        return 1

    value, err = _lookup_toml_nested(data, parts)
    if err is not None:
        print(err)
        return 1

    if isinstance(value, (dict, list)):
        pprint.pprint(value, width=120)
    else:
        print(value)
    return 0


def _parse_toml_value_literal(value_str: str) -> object:
    """Parse CLI value: JSON scalars/arrays/objects, else plain string."""
    s = value_str.strip()
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        return value_str


def _ensure_parent_for_set(data: dict, parts: list[str]) -> tuple[dict | None, str | None, str | None]:
    """Descend path parts[:-1], creating missing tables; return (parent, last_key, error_message)."""
    if not parts:
        return None, None, "Key path is empty."
    cur: dict = data
    prefix: list[str] = []
    for segment in parts[:-1]:
        if segment not in cur:
            cur[segment] = {}
        elif not isinstance(cur[segment], dict):
            loc = ".".join(prefix + [segment])
            return None, None, f"Cannot set nested key: '{loc}' exists and is not a table."
        prefix.append(segment)
        cur = cur[segment]
    last = parts[-1]
    return cur, last, None


def cmd_toml_set(toml_path: str, key: str, value_str: str) -> int:
    toml_path = toml_path.strip()
    key = key.strip()
    if not toml_path or not key:
        print("TOML path and key must not be empty.")
        return 1

    parts = [p for p in key.split(".") if p != ""]
    if not parts:
        print("Key must contain at least one segment (e.g. name or section.field).")
        return 1

    path = os.path.expanduser(toml_path)
    if not os.path.isfile(path):
        print(f"File not found: {path}")
        return 1

    try:
        with open(path, encoding="utf-8") as f:
            data = toml.load(f)
    except toml.TomlDecodeError as e:
        print(f"Invalid TOML: {e}")
        return 1
    except OSError as e:
        print(f"Cannot read file: {e}")
        return 1

    if not isinstance(data, dict):
        print("TOML root must be a table.")
        return 1

    parent, last, err = _ensure_parent_for_set(data, parts)
    if err is not None:
        print(err)
        return 1

    parent[last] = _parse_toml_value_literal(value_str)

    try:
        with open(path, "w", encoding="utf-8") as f:
            toml.dump(data, f)
    except OSError as e:
        print(f"Cannot write file: {e}")
        return 1

    print(f"Set '{'.'.join(parts)}' and saved: {path}")
    return 0


def _quote_path_segment(s: str) -> str:
    return urllib.parse.quote(s, safe="-._~")


def search_packages(name: str, page_num: int = 1, page_size: int = 9) -> dict:
    params = {
        "pageNum": page_num,
        "pageSize": page_size,
        "orderField": 2,
        "sortType": 2,
        "name": name,
    }
    url = SEARCH_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = resp.read().decode("utf-8")
    return json.loads(body)


def build_download_url(package_name: str, version: str, organization: str | None) -> str:
    path = f"{_quote_path_segment(package_name)}/{_quote_path_segment(version)}"
    base = f"{REGISTRY_BASE}/{path}"
    if organization and organization != "default":
        return base + "?" + urllib.parse.urlencode({"organization": organization})
    return base


def download_to_file(url: str, dest_path: str) -> None:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()
    with open(dest_path, "wb") as f:
        f.write(data)


def _format_publisher(pub: object) -> str:
    if not isinstance(pub, dict):
        return ""
    nick = pub.get("nickname")
    user = pub.get("username")
    if nick:
        s = str(nick)
        if user and str(user) != s:
            s = f"{s} ({user})"
        return s
    if user:
        return str(user)
    return ""


def print_results_table(results: list) -> None:
    headers = ("#", "Name", "Latest version", "Organization", "Publisher", "Downloads", "Description")
    rows = []
    for i, item in enumerate(results):
        name = str(item.get("name") or "")
        ver = str(item.get("latestVersion") or "")
        organization = str(item.get("organization") or item.get("group") or "")
        publisher = _format_publisher(item.get("publisher"))
        dc = item.get("downloadCount")
        download_count = "" if dc is None else str(dc)
        desc = str(item.get("description") or "")
        if len(desc) > 40:
            desc = desc[:37] + "..."
        if len(publisher) > 36:
            publisher = publisher[:33] + "..."
        rows.append((str(i), name, ver, organization, publisher, download_count, desc))

    widths = [len(h) for h in headers]
    for row in rows:
        for j, cell in enumerate(row):
            widths[j] = max(widths[j], len(cell))

    def fmt_row(cells: tuple[str, ...]) -> str:
        parts = [cells[j].ljust(widths[j]) for j in range(len(cells))]
        return " | ".join(parts)

    print(fmt_row(headers))
    print("-+-".join("-" * w for w in widths))
    for row in rows:
        print(fmt_row(row))


def parse_download_spec(spec: str) -> tuple[str, str, str] | None:
    """Parse -d: package_name:version (org default) or organization::package_name:version."""
    s = spec.strip()
    if not s:
        return None
    if "::" in s:
        org_part, rest = s.split("::", 1)
        organization = org_part.strip()
        rest = rest.strip()
        if not organization or ":" not in rest:
            return None
        name, ver = rest.split(":", 1)
        name, ver = name.strip(), ver.strip()
        if not name or not ver:
            return None
        return name, ver, organization
    if ":" not in s:
        return None
    name, ver = s.split(":", 1)
    name, ver = name.strip(), ver.strip()
    if not name or not ver:
        return None
    return name, ver, "default"


def _download_pkg(pkg_name: str, version: str, organization: str | None) -> int:
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    safe_file = f"{pkg_name}-{version}.pkg".replace("/", "_").replace("\\", "_")
    dest = os.path.join(DOWNLOAD_DIR, safe_file)
    dl_url = build_download_url(pkg_name, version, organization)

    try:
        download_to_file(dl_url, dest)
    except urllib.error.HTTPError as e:
        try:
            detail = e.read().decode("utf-8", errors="replace")
        except Exception:
            detail = str(e)
        print(f"Download failed (HTTP {e.code}): {detail}")
        return 1
    except urllib.error.URLError as e:
        print(f"Download failed (network error): {e.reason}")
        return 1

    print(f"Saved to: {dest}")
    return 0


def cmd_search(name_query: str) -> int:
    name_query = name_query.strip()
    if not name_query:
        print("Package name cannot be empty.")
        return 1

    try:
        payload = search_packages(name_query)
    except urllib.error.HTTPError as e:
        try:
            detail = e.read().decode("utf-8", errors="replace")
        except Exception:
            detail = str(e)
        print(f"Search request failed (HTTP {e.code}): {detail}")
        return 1
    except urllib.error.URLError as e:
        print(f"Search request failed (network error): {e.reason}")
        return 1
    except json.JSONDecodeError as e:
        print(f"Search response is not valid JSON: {e}")
        return 1

    if payload.get("code") != 200:
        msg = payload.get("msg") or payload.get("err") or "Unknown error"
        print(f"Search failed: {msg}")
        if payload.get("traceId"):
            print(f"traceId: {payload['traceId']}")
        return 1

    data = payload.get("data") or {}
    results = data.get("results") or []
    if not results:
        print("No matching packages found.")
        return 0

    total = data.get("totalRecords")
    pages = data.get("totalPages")
    extra = []
    if total is not None:
        extra.append(f"{total} record(s) total")
    if pages is not None:
        extra.append(f"{pages} page(s) total")
    suffix = f" ({', '.join(extra)})" if extra else ""
    print(f"Page 1 results{suffix}:")
    print()
    print_results_table(results)
    return 0


def cmd_download(spec: str) -> int:
    parsed = parse_download_spec(spec)
    if not parsed:
        print(
            "Expected download format: package_name:version (organization defaults to default), "
            "or organization::package_name:version."
        )
        return 1
    pkg_name, version, organization = parsed
    return _download_pkg(pkg_name, version, organization)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Search packages, download packages, or read/write TOML values.",
    )
    mx = parser.add_mutually_exclusive_group(required=True)
    mx.add_argument(
        "-s",
        "--search",
        metavar="package_name",
        help="Search packages and print the page-1 results table",
    )
    mx.add_argument(
        "-d",
        "--download",
        metavar="[organization::]package_name:version",
        help="Download directly, e.g. demo:1.1.7 (org default); with org: opencj::multipart:0.1.3",
    )
    mx.add_argument(
        "-g",
        "--get",
        nargs="+",
        metavar="ARG",
        dest="toml_get",
        help=(
            "Load TOML from path, then resolve nested keys like fileobj[key1][key2]… "
            "Usage: TOML_PATH KEY1 [KEY2 ...] or TOML_PATH key1.key2"
        ),
    )
    mx.add_argument(
        "-e",
        "--set",
        nargs=3,
        metavar=("TOML_PATH", "KEY", "VALUE"),
        dest="toml_set",
        help=(
            "Set TOML KEY to VALUE and save the file; missing keys and parent tables are created. "
            "KEY uses dots for nesting (e.g. owner.name). VALUE can be JSON (numbers, booleans, arrays)."
        ),
    )
    args = parser.parse_args(argv)

    if args.search is not None:
        return cmd_search(args.search)
    if args.download is not None:
        return cmd_download(args.download)
    if args.toml_set is not None:
        p, k, v = args.toml_set
        return cmd_toml_set(p, k, v)
    tg = args.toml_get
    if tg is None or len(tg) < 2:
        parser.error("-g requires TOML_PATH and at least one key.")
    return cmd_toml_get(tg[0], tg[1:])


if __name__ == "__main__":
    sys.exit(main())
