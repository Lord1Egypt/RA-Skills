#!/usr/bin/env python3
"""Call Bitrix24 REST methods using saved config or explicit URL.

Features:
    --param key=value      Standard parameter passing (repeat for multiple)
    --params-file FILE     Pass parameters from a JSON file (safer for complex data)
    --dry-run              Validate request without executing
    --iterate              Auto-paginate list methods (collect all pages)
    --max-items N          Limit total items when iterating
    --confirm-write        Required flag for write operations (add, update, set)
    --confirm-destructive  Required flag for destructive operations (delete, remove)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib import error, parse, request

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from bitrix24_config import load_url, normalize_url, validate_url, cache_user_data  # noqa: E402

# Operation classification patterns
WRITE_SUFFIXES = re.compile(
    r"(?:^|\.)(add|update|set|register|bind|import|complete|start|stop|move|clear|confirm|attach|send|mute|pin)$",
    re.IGNORECASE,
)
DESTRUCTIVE_SUFFIXES = re.compile(
    r"(?:^|\.)(delete|remove|recyclebin|unregister|unbind)$",
    re.IGNORECASE,
)

MAX_PAGES = 200  # Safety limit for auto-pagination


def classify_operation(method: str) -> str:
    """Classify method as 'read', 'write', or 'destructive'."""
    if DESTRUCTIVE_SUFFIXES.search(method):
        return "destructive"
    if WRITE_SUFFIXES.search(method):
        return "write"
    return "read"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Call a Bitrix24 REST method.")
    parser.add_argument("method", help="REST method, e.g. user.current or calendar.event.get")
    parser.add_argument(
        "--param",
        action="append",
        default=[],
        help="Request parameter in key=value form; repeat as needed",
    )
    parser.add_argument(
        "--params-file",
        help="Path to a JSON file with method parameters (alternative to --param)",
    )
    parser.add_argument("--timeout", type=float, default=20.0, help="HTTP timeout in seconds")
    parser.add_argument("--json", action="store_true", help="Pretty-print JSON response")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be called without executing")
    parser.add_argument("--iterate", action="store_true", help="Auto-paginate list methods (collect all pages)")
    parser.add_argument("--max-items", type=int, default=None, help="Max items to collect when iterating")
    parser.add_argument("--confirm-write", action="store_true", help="Confirm write operation (add/update/set)")
    parser.add_argument("--confirm-destructive", action="store_true", help="Confirm destructive operation (delete/remove)")
    return parser.parse_args()


def parse_params(raw_params: list[str]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for item in raw_params:
        if "=" not in item:
            raise ValueError(f"Invalid --param '{item}'. Use key=value.")
        key, value = item.split("=", 1)
        out.append((key, value))
    return out


def do_request(url: str, data: bytes, timeout: float, source: str) -> dict:
    """Execute HTTP request and return structured result."""
    req = request.Request(url, data=data, headers={"Accept": "application/json"})
    try:
        with request.urlopen(req, timeout=timeout) as response:
            payload = response.read().decode("utf-8", errors="replace")
            status = response.getcode()
    except error.HTTPError as exc:
        payload = exc.read().decode("utf-8", errors="replace")
        status = exc.code
    except Exception as exc:
        return {"ok": False, "error": str(exc), "source": source}

    try:
        body = json.loads(payload)
    except Exception:
        body = {"raw": payload}

    return {"ok": status < 400, "status": status, "source": source, "body": body}


def main() -> int:
    args = parse_args()
    raw_url, source = load_url()
    if not raw_url:
        print(json.dumps({"ok": False, "error": "No Bitrix24 webhook configured", "source": source}, ensure_ascii=True, indent=2))
        return 1

    normalized_url = validate_url(raw_url)

    method = args.method[:-5] if args.method.endswith(".json") else args.method

    # --- Resolve parameters ---
    # --params-file takes priority (safer for complex JSON)
    if args.params_file:
        try:
            params_json = json.loads(Path(args.params_file).read_text(encoding="utf-8"))
        except FileNotFoundError:
            print(json.dumps({"ok": False, "error": f"Params file not found: {args.params_file}"}, indent=2))
            return 1
        except json.JSONDecodeError as e:
            print(json.dumps({"ok": False, "error": f"Invalid JSON in {args.params_file}: {e}"}, indent=2))
            return 1
        if not isinstance(params_json, dict):
            print(json.dumps({"ok": False, "error": "params-file must contain a JSON object"}), indent=2)
            return 1
        # Convert JSON dict to URL-encoded pairs (flat)
        params = _flatten_json(params_json)
    else:
        try:
            params = parse_params(args.param)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1

    # --- Operation classification & safety checks ---
    op_type = classify_operation(method)

    if args.dry_run:
        dry = {
            "dry_run": True,
            "method": method,
            "operation": op_type,
            "params_count": len(params),
            "source": source,
        }
        print(json.dumps(dry, ensure_ascii=True, indent=2))
        return 0

    if op_type == "write" and not args.confirm_write:
        print(json.dumps({
            "ok": False,
            "error": f"Write operation '{method}' requires --confirm-write flag",
            "operation": op_type,
        }, ensure_ascii=True, indent=2))
        return 2

    if op_type == "destructive" and not args.confirm_destructive:
        print(json.dumps({
            "ok": False,
            "error": f"Destructive operation '{method}' requires --confirm-destructive flag",
            "operation": op_type,
        }, ensure_ascii=True, indent=2))
        return 2

    base_url = normalize_url(normalized_url)

    # --- Auto-pagination ---
    if args.iterate and method.endswith(".list"):
        all_items: list = []
        start = 0
        total = None
        for page in range(1, MAX_PAGES + 1):
            page_params = params + [("start", str(start))]
            url = base_url + f"{method}.json"
            data = parse.urlencode(page_params).encode("utf-8")
            result = do_request(url, data, args.timeout, source)

            if not result.get("ok"):
                print(json.dumps(result, ensure_ascii=True, indent=2 if args.json else None))
                return 1

            body = result.get("body", {})
            page_result = body.get("result", [])
            if isinstance(page_result, dict):
                # Some methods return {tasks: [...]} instead of [...]
                for v in page_result.values():
                    if isinstance(v, list):
                        page_result = v
                        break
                else:
                    page_result = []

            all_items.extend(page_result)

            if total is None:
                total = body.get("total", len(all_items))

            if args.max_items and len(all_items) >= args.max_items:
                all_items = all_items[:args.max_items]
                break

            next_start = body.get("next")
            if next_start is None:
                break
            start = next_start

        result = {
            "ok": True,
            "status": 200,
            "source": source,
            "body": {"result": all_items, "total": total, "fetched": len(all_items)},
        }
        print(json.dumps(result, ensure_ascii=True, indent=2 if args.json else None))
        return 0

    # --- Single request ---
    url = base_url + f"{method}.json"
    data = parse.urlencode(params).encode("utf-8")
    result = do_request(url, data, args.timeout, source)

    # Auto-cache user_id and timezone after successful user.current call
    status = result.get("status", 0)
    body = result.get("body", {})
    if method == "user.current" and status and status < 400 and isinstance(body, dict):
        user_result = body.get("result", {})
        uid = user_result.get("ID")
        tz = user_result.get("TIME_ZONE", "")
        if uid:
            try:
                cache_user_data(int(uid), tz)
            except Exception:
                pass

    if args.json:
        print(json.dumps(result, ensure_ascii=True, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=True))
    return 0 if result.get("ok") else 1


def _flatten_json(obj: dict, prefix: str = "") -> list[tuple[str, str]]:
    """Flatten nested JSON dict into URL-encoded key=value pairs.

    {"fields": {"TITLE": "X"}} → [("fields[TITLE]", "X")]
    {"select": ["ID", "TITLE"]} → [("select[]", "ID"), ("select[]", "TITLE")]
    """
    pairs: list[tuple[str, str]] = []
    for key, value in obj.items():
        full_key = f"{prefix}[{key}]" if prefix else key
        if isinstance(value, dict):
            pairs.extend(_flatten_json(value, full_key))
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    pairs.extend(_flatten_json(item, f"{full_key}[]"))
                else:
                    pairs.append((f"{full_key}[]", str(item)))
        else:
            pairs.append((full_key, str(value)))
    return pairs


if __name__ == "__main__":
    sys.exit(main())
