#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


API_INFO_URL = "https://gw.datayes.com/aladdin_llm_mgmt/web/mgr/api"
GPT_MATERIALS_V2_URL = "https://gw.datayes.com/aladdin_info/web/gptMaterials/v2"
DEFAULT_TIMEOUT = 30
DEFAULT_TOP = 15
MAX_TOP = 50
ALLOWED_HTTP_HOSTS = {
    "api.datayes.com",
    "api.wmcloud.com",
    "gw.datayes.com",
    "r.datayes.com",
}
ALLOWED_QUERY_SCOPES = {
    "research",
    "announcement",
    "news",
    "meetingSummary",
    "indicator",
    "researchTable",
}


class DatayesError(RuntimeError):
    pass


def get_token() -> str:
    token = os.environ.get("DATAYES_TOKEN", "").strip()
    if not token:
        raise DatayesError("Missing DATAYES_TOKEN environment variable.")
    return token


def validate_http_url(url: str) -> str:
    parts = urlsplit(url)
    if parts.scheme != "https":
        raise DatayesError(f"Resolved httpUrl must use https: {url}")
    if not parts.netloc:
        raise DatayesError(f"Resolved httpUrl is missing a host: {url}")
    host = (parts.hostname or "").lower()
    if host not in ALLOWED_HTTP_HOSTS:
        allowed_hosts = ", ".join(sorted(ALLOWED_HTTP_HOSTS))
        raise DatayesError(
            f"Resolved httpUrl host {host or '<unknown>'} is not trusted. Allowed hosts: {allowed_hosts}"
        )
    return url


def request_json(url: str, *, method: str = "GET", payload: dict[str, Any] | None = None) -> Any:
    body = None
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "Accept": "application/json",
        "User-Agent": "datayes-web-search-skill/1.0",
    }
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = Request(url=url, data=body, headers=headers, method=method)
    try:
        with urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
            return json.load(resp)
    except HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="replace")
        raise DatayesError(f"HTTP {exc.code} for {url}: {body_text}") from exc
    except URLError as exc:
        raise DatayesError(f"Request failed for {url}: {exc}") from exc


def build_v2_spec() -> dict[str, Any]:
    return {
        "requestId": None,
        "code": 1,
        "message": "synthetic spec",
        "data": {
            "id": 3,
            "name": "AI搜索—召回元数据",
            "nameEn": "gptMaterials",
            "summary": "综合搜索，召回研报、公告、新闻、会议纪要与指标语料",
            "httpMethod": "POST",
            "httpUrl": GPT_MATERIALS_V2_URL,
            "internal": False,
            "active": True,
            "parametersInput": [
                {
                    "name": "用户问题",
                    "nameEn": "question",
                    "summary": "",
                    "direction": "INPUT",
                    "location": "Body",
                    "type": "String",
                    "defaultValue": "",
                    "mandatory": True,
                },
                {
                    "name": "指定范围",
                    "nameEn": "queryScope",
                    "summary": "research / announcement / news / meetingSummary / indicator / researchTable",
                    "direction": "INPUT",
                    "location": "Body",
                    "type": "String",
                    "defaultValue": "",
                    "mandatory": False,
                },
                {
                    "name": "改写开关",
                    "nameEn": "rewrite",
                    "summary": "是否改写问题，默认 false",
                    "direction": "INPUT",
                    "location": "Body",
                    "type": "Boolean",
                    "defaultValue": "false",
                    "mandatory": False,
                },
            ],
        },
    }


def fetch_api_spec() -> dict[str, Any]:
    validate_http_url(API_INFO_URL)
    return build_v2_spec()


def normalize_scope(query_scope: str | None) -> str | None:
    if query_scope is None:
        return None
    value = query_scope.strip()
    if not value:
        return None
    if value not in ALLOWED_QUERY_SCOPES:
        allowed = ", ".join(sorted(ALLOWED_QUERY_SCOPES))
        raise DatayesError(f"Invalid queryScope {value!r}. Allowed values: {allowed}")
    return value


def normalize_top(value: int) -> int:
    if value <= 0:
        raise DatayesError("--top must be a positive integer.")
    return min(value, MAX_TOP)


def extract_items(payload: Any, top: int) -> list[Any]:
    if not isinstance(payload, dict):
        raise DatayesError("Unexpected search response type.")
    data = payload.get("data")
    if not isinstance(data, list):
        raise DatayesError(f"Unexpected search response: {json.dumps(payload, ensure_ascii=False)}")
    return data[:top]


def search_materials(question: str, query_scope: str | None, top: int, rewrite: bool) -> list[Any]:
    question = question.strip()
    if not question:
        raise DatayesError("Question must not be empty.")

    payload: dict[str, Any] = {
        "question": question,
        "rewrite": rewrite,
    }
    normalized_scope = normalize_scope(query_scope)
    if normalized_scope:
        payload["queryScope"] = normalized_scope

    url = validate_http_url(fetch_api_spec()["data"]["httpUrl"])
    return extract_items(request_json(url, method="POST", payload=payload), normalize_top(top))


def print_output(payload: Any) -> None:
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Search Datayes gptMaterials/v2 with Python stdlib only.")
    parser.add_argument("--json", action="store_true", help="Accepted for compatibility; output is always JSON.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    spec_parser = subparsers.add_parser("spec", help="Show the gptMaterials/v2 API spec.")
    spec_parser.add_argument("--full", action="store_true", help="Print the full wrapped response instead of spec.data.")

    search_parser = subparsers.add_parser("search", help="Search Datayes materials.")
    search_parser.add_argument("question")
    search_parser.add_argument("--query-scope")
    search_parser.add_argument("--top", type=int, default=DEFAULT_TOP)
    search_parser.add_argument(
        "--rewrite",
        action="store_true",
        help="Allow backend rewrite. Default is false to preserve the original query.",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "spec":
            spec = fetch_api_spec()
            print_output(spec if args.full else spec["data"])
            return 0

        if args.command == "search":
            results = search_materials(
                question=args.question,
                query_scope=args.query_scope,
                top=args.top,
                rewrite=bool(args.rewrite),
            )
            print_output(results)
            return 0
    except DatayesError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
