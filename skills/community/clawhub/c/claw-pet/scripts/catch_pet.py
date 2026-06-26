#!/usr/bin/env python3
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

SKILL_DIR = Path(__file__).resolve().parent.parent
META_PATH = SKILL_DIR / "_meta.json"


class ConfigError(RuntimeError):
    pass


def load_meta_config() -> Dict[str, Any]:
    if not META_PATH.exists():
        return {}
    with META_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_config() -> Dict[str, str]:
    meta = load_meta_config()
    config = {
        "CATCH_API_URL": os.environ.get("CATCH_API_URL") or meta.get("CATCH_API_URL") or "",
        "API_KEY": os.environ.get("API_KEY") or meta.get("API_KEY") or "",
    }
    if not config["CATCH_API_URL"]:
        raise ConfigError("Missing CATCH_API_URL. Set env var CATCH_API_URL or add it to _meta.json.")
    if not config["API_KEY"]:
        raise ConfigError("Missing API_KEY. Set env var API_KEY or add it to _meta.json.")
    return config


def build_request(url: str, api_key: str) -> urllib.request.Request:
    payload = json.dumps({"action": "catch"}).encode("utf-8")
    return urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )


def fetch_result(config: Dict[str, str]) -> Tuple[int, Dict[str, Any]]:
    req = build_request(config["CATCH_API_URL"], config["API_KEY"])
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            status = getattr(resp, "status", 200)
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        parsed = safe_json(body)
        return e.code, parsed or {"error": {"message": body or str(e), "code": e.code}}
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e.reason}") from e

    parsed = safe_json(body)
    if parsed is None:
        raise RuntimeError("Backend returned non-JSON response")
    return status, parsed


def safe_json(text: str) -> Optional[Dict[str, Any]]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else {"data": data}


def classify(data: Dict[str, Any], status: int) -> Dict[str, Any]:
    pet = data.get("pet")
    item = data.get("item")
    message = data.get("message") or data.get("detail") or data.get("status") or ""
    error = data.get("error")

    if status >= 400 or error:
        return {
            "kind": "error",
            "message": message or extract_error_message(error) or f"Request failed with HTTP {status}",
            "status": status,
            "raw": data,
        }
    if isinstance(pet, dict) and pet:
        return {"kind": "pet", "message": message, "pet": pet, "raw": data}
    if isinstance(item, dict) and item:
        return {"kind": "item", "message": message, "item": item, "raw": data}
    if data.get("empty") is True or data.get("result") == "empty" or not (pet or item):
        return {"kind": "empty", "message": message or "Nothing was caught this time.", "raw": data}
    return {"kind": "error", "message": "Unrecognized response shape", "status": status, "raw": data}


def extract_error_message(error: Any) -> str:
    if isinstance(error, dict):
        return str(error.get("message") or error.get("detail") or error.get("code") or "")
    return str(error or "")


def format_pet(pet: Dict[str, Any], message: str) -> str:
    rarity = pet.get("rarity", "Unknown rarity")
    name = pet.get("name", "Unknown pet")
    level = pet.get("level", "?")
    extra = pet.get("description") or pet.get("title") or ""
    base = f"{message + ' ' if message else ''}Caught a {rarity} pet: {name} (Lv.{level})."
    return f"{base} {extra}".strip()


def format_item(item: Dict[str, Any], message: str) -> str:
    rarity = item.get("rarity", "Unknown rarity")
    name = item.get("name", "Unknown item")
    qty = item.get("quantity") or item.get("count") or 1
    extra = item.get("description") or ""
    base = f"{message + ' ' if message else ''}Caught an item: {name} x{qty} [{rarity}]."
    return f"{base} {extra}".strip()


def format_result(result: Dict[str, Any]) -> str:
    kind = result["kind"]
    if kind == "pet":
        return format_pet(result["pet"], result.get("message", ""))
    if kind == "item":
        return format_item(result["item"], result.get("message", ""))
    if kind == "empty":
        return result.get("message", "Nothing was caught this time.")
    return f"Catch failed: {result.get('message', 'Unknown error')}"


def main() -> int:
    debug = "--debug" in sys.argv
    try:
        config = load_config()
        status, data = fetch_result(config)
        result = classify(data, status)
        if debug:
            print(json.dumps({"status": status, "result": result}, ensure_ascii=False, indent=2))
        else:
            print(format_result(result))
        return 0 if result["kind"] != "error" else 1
    except ConfigError as e:
        print(f"Config error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Runtime error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
