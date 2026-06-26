#!/usr/bin/env python3
"""Query Datayes APIs with Python standard library only."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

API_INFO_URL = "https://gw.datayes.com/aladdin_llm_mgmt/web/mgr/api"
TOKEN_ENV = "DATAYES_TOKEN"
TIMEOUT = 30
PATH_PARAM_RE = re.compile(r"\{([^{}]+)\}")
ALLOWED_HTTP_HOSTS = {
    "api.datayes.com",
    "api.wmcloud.com",
    "gw.datayes.com",
    "r.datayes.com",
}


class DatayesError(RuntimeError):
    """Raised when the Datayes workflow cannot be completed."""


def _load_token() -> str:
    token = os.environ.get(TOKEN_ENV, "").strip()
    if not token:
        raise DatayesError(f"Missing {TOKEN_ENV} environment variable")
    return token


def _request_json(url: str, *, token: str, method: str = "GET", payload: Any = None) -> Any:
    body = None
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url=url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return json.loads(response.read().decode(charset))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise DatayesError(f"HTTP {exc.code} for {url}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise DatayesError(f"Request failed for {url}: {exc.reason}") from exc


def fetch_spec(name_en: str, token: str) -> dict[str, Any]:
    query = urllib.parse.urlencode({"nameEn": name_en})
    data = _request_json(f"{API_INFO_URL}?{query}", token=token)
    if not isinstance(data, dict):
        raise DatayesError("Unexpected API spec response type")
    if not data.get("data"):
        raise DatayesError(f"No API spec returned for nameEn={name_en}")
    return data


def _parse_value(raw: str) -> Any:
    value = raw.strip()
    if not value:
        return ""
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def _parse_kv_pairs(items: list[str]) -> dict[str, Any]:
    params: dict[str, Any] = {}
    for item in items:
        if "=" not in item:
            raise DatayesError(f"Invalid --param value: {item!r}; expected key=value")
        key, raw_value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise DatayesError(f"Invalid --param key in {item!r}")
        params[key] = _parse_value(raw_value)
    return params


def _normalize_params(spec: dict[str, Any], params: dict[str, Any]) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    meta = spec.get("data") or {}
    input_params = meta.get("parametersInput") or []
    allowed = {item.get("nameEn"): item for item in input_params if item.get("nameEn")}

    unknown = sorted(key for key in params if key not in allowed)
    if unknown:
        allowed_text = ", ".join(sorted(allowed)) or "<none>"
        raise DatayesError(
            f"Unknown parameters for nameEn={meta.get('nameEn')}: {', '.join(unknown)}. Allowed: {allowed_text}"
        )

    normalized = dict(params)
    missing_required: list[str] = []
    for key, item in allowed.items():
        if key in normalized:
            continue
        default = item.get("defaultValue")
        mandatory = bool(item.get("mandatory"))
        if mandatory and default not in (None, ""):
            normalized[key] = _parse_value(str(default))
        elif mandatory:
            missing_required.append(key)

    if missing_required:
        raise DatayesError(
            f"Missing required parameters for nameEn={meta.get('nameEn')}: {', '.join(sorted(missing_required))}"
        )

    return normalized, allowed


def _partition_params(params: dict[str, Any], allowed: dict[str, dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    query_params: dict[str, Any] = {}
    body_params: dict[str, Any] = {}
    path_params: dict[str, Any] = {}

    for key, value in params.items():
        location = str(allowed[key].get("location") or "Query").lower()
        if location == "query":
            query_params[key] = value
        elif location == "body":
            body_params[key] = value
        elif location == "path":
            path_params[key] = value
        else:
            query_params[key] = value

    return query_params, body_params, path_params


def _apply_path_params(http_url: str, path_params: dict[str, Any]) -> str:
    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in path_params:
            raise DatayesError(f"Missing path parameter: {key}")
        return urllib.parse.quote(str(path_params[key]), safe="")

    return PATH_PARAM_RE.sub(replace, http_url)


def _validate_http_url(http_url: str) -> str:
    parsed = urllib.parse.urlparse(http_url)
    if parsed.scheme != "https":
        raise DatayesError(f"Resolved httpUrl must use https: {http_url}")
    if not parsed.netloc:
        raise DatayesError(f"Resolved httpUrl is missing a host: {http_url}")
    host = (parsed.hostname or "").lower()
    if host not in ALLOWED_HTTP_HOSTS:
        allowed_hosts = ", ".join(sorted(ALLOWED_HTTP_HOSTS))
        raise DatayesError(
            f"Resolved httpUrl host {host or '<unknown>'} is not trusted. Allowed hosts: {allowed_hosts}"
        )
    return http_url


def call_api(spec: dict[str, Any], params: dict[str, Any], token: str) -> Any:
    meta = spec.get("data") or {}
    http_url = meta.get("httpUrl")
    http_method = str(meta.get("httpMethod") or "GET").upper()
    if not http_url:
        raise DatayesError("API spec missing httpUrl")

    normalized_params, allowed = _normalize_params(spec, params)
    query_params, body_params, path_params = _partition_params(normalized_params, allowed)
    resolved_url = _validate_http_url(_apply_path_params(http_url, path_params))

    if http_method == "GET":
        query = urllib.parse.urlencode(query_params, doseq=True)
        url = resolved_url if not query else f"{resolved_url}?{query}"
        return _request_json(url, token=token)

    if http_method == "POST":
        query = urllib.parse.urlencode(query_params, doseq=True)
        url = resolved_url if not query else f"{resolved_url}?{query}"
        payload = body_params if body_params else query_params or None
        return _request_json(url, token=token, method="POST", payload=payload)

    raise DatayesError(f"Unsupported httpMethod: {http_method}")


def _extract_field(data: Any, field_path: str) -> Any:
    current = data
    for part in field_path.split("."):
        if isinstance(current, list):
            if not part.isdigit():
                raise DatayesError(f"Field path segment {part!r} is not a valid list index")
            index = int(part)
            try:
                current = current[index]
            except IndexError as exc:
                raise DatayesError(f"List index out of range in field path: {part}") from exc
        elif isinstance(current, dict):
            if part not in current:
                raise DatayesError(f"Field path not found: {field_path}")
            current = current[part]
        else:
            raise DatayesError(f"Cannot descend into field path {field_path!r}")
    return current


def _select_output(spec: dict[str, Any], result: Any, *, spec_only: bool, result_only: bool, field_path: str | None) -> Any:
    if spec_only:
        output: Any = spec
    elif result_only:
        output = result
    else:
        output = {
            "spec": spec.get("data"),
            "result": result,
        }

    if field_path:
        output = _extract_field(output, field_path)
    return output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Resolve a Datayes API by nameEn, print its latest spec, and optionally execute it. "
            f"Reads the token from {TOKEN_ENV}."
        )
    )
    parser.add_argument("name_en", help="Datayes API nameEn, for example market_snapshot")
    parser.add_argument(
        "--param",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Request parameter. Values may be plain strings or JSON literals.",
    )
    parser.add_argument(
        "--spec-only",
        action="store_true",
        help="Only fetch and print the API spec; do not execute the business API.",
    )
    parser.add_argument(
        "--result-only",
        action="store_true",
        help="Only print the business API response body; omit the resolved spec metadata.",
    )
    parser.add_argument(
        "--field",
        metavar="PATH",
        help="Print a nested field using dot-path syntax, for example result.data.0.ticker or data.hits.0.entity_id.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.spec_only and args.result_only:
        print("--spec-only and --result-only cannot be used together", file=sys.stderr)
        return 1

    try:
        token = _load_token()
        params = _parse_kv_pairs(args.param)
        spec = fetch_spec(args.name_en, token)
        result = None if args.spec_only else call_api(spec, params, token)
        output = _select_output(
            spec,
            result,
            spec_only=args.spec_only,
            result_only=args.result_only,
            field_path=args.field,
        )
    except DatayesError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.pretty:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(output, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
