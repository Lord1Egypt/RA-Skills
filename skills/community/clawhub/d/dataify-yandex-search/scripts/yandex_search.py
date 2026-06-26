#!/usr/bin/env python3
"""Call the Dataify Yandex search API and print the raw response body."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


API_URL = "https://scraperapi.dataify.com/request"

PARAMETERS = [
    {
        "name": "engine",
        "default": "yandex",
        "description": "搜索引擎，固定为 yandex。",
    },
    {
        "name": "text",
        "default": None,
        "description": "搜索查询内容，来自用户需求。",
    },
    {
        "name": "json",
        "default": "1",
        "description": "输出格式：1 JSON，2 JSON+HTML，3 HTML，4 Light JSON。说明默认 JSON，即 1。",
    },
    {
        "name": "yandex_domain",
        "default": "yandex.com",
        "description": "使用的 Yandex 域名。说明默认 yandex.com。",
    },
    {
        "name": "lang",
        "default": "en",
        "description": "搜索语言；当 yandex_domain 为 yandex.com 时说明默认 en。",
    },
    {
        "name": "lr",
        "default": None,
        "description": "限制搜索结果的国家或地区 ID；说明未给出默认值。",
    },
    {
        "name": "p",
        "default": None,
        "description": "页码，从 0 开始；说明未给出默认值。",
    },
    {
        "name": "family_mode",
        "default": "1",
        "description": "家庭/安全搜索：0 关闭，1 中等，2 严格；说明默认中等，即 1。",
    },
    {
        "name": "fix_typo",
        "default": "true",
        "description": "是否启用自动拼写纠正；说明默认 true。",
    },
    {
        "name": "groups_on_page",
        "default": "20",
        "description": "单页最大结果组数；说明默认 20。",
    },
    {
        "name": "no_cache",
        "default": "false",
        "description": "是否跳过缓存；说明 false 使用缓存且为默认，true 跳过缓存。",
    },
]

JSON_FORMAT_ALIASES = {
    "json": "1",
    "json+html": "2",
    "json_html": "2",
    "json-html": "2",
    "html": "3",
    "light-json": "4",
    "light_json": "4",
    "light json": "4",
}

FAMILY_MODE_ALIASES = {
    "off": "0",
    "close": "0",
    "closed": "0",
    "false": "0",
    "0": "0",
    "moderate": "1",
    "medium": "1",
    "middle": "1",
    "1": "1",
    "strict": "2",
    "strong": "2",
    "2": "2",
}

BOOLEAN_ALIASES = {
    "1": "true",
    "true": "true",
    "yes": "true",
    "y": "true",
    "on": "true",
    "0": "false",
    "false": "false",
    "no": "false",
    "n": "false",
    "off": "false",
}


def normalize_authorization(token: str) -> str:
    token = token.strip()
    if token.lower().startswith("bearer "):
        return token
    return f"Bearer {token}"


def normalize_json_format(value: str) -> str:
    value = value.strip()
    return JSON_FORMAT_ALIASES.get(value.lower(), value)


def normalize_family_mode(value: str) -> str:
    value = value.strip()
    return FAMILY_MODE_ALIASES.get(value.lower(), value)


def normalize_boolean(value: str) -> str:
    value = value.strip()
    return BOOLEAN_ALIASES.get(value.lower(), value.lower())


def parse_params_json(raw: str) -> dict[str, str | None]:
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"--params-json must be a JSON object: {exc}") from exc
    if not isinstance(parsed, dict):
        raise SystemExit("--params-json must be a JSON object.")
    return {
        str(key): None if value is None else str(value)
        for key, value in parsed.items()
    }


def default_body() -> dict[str, str]:
    return {
        parameter["name"]: str(parameter["default"])
        for parameter in PARAMETERS
        if parameter["default"] is not None
    }


def build_body(args: argparse.Namespace) -> dict[str, str]:
    body = default_body()

    if args.params_json:
        for key, value in parse_params_json(args.params_json).items():
            if value is None:
                body.pop(key, None)
            else:
                body[key] = value

    field_updates = {
        "text": args.text or args.query,
        "json": args.json_format,
        "yandex_domain": args.yandex_domain,
        "lang": args.lang,
        "lr": args.lr,
        "p": args.p,
        "family_mode": args.family_mode,
        "fix_typo": args.fix_typo,
        "groups_on_page": args.groups_on_page,
        "no_cache": args.no_cache,
    }

    for key, value in field_updates.items():
        if value is not None:
            body[key] = str(value)

    if body.get("json"):
        body["json"] = normalize_json_format(body["json"])
    if body.get("family_mode"):
        body["family_mode"] = normalize_family_mode(body["family_mode"])
    if body.get("fix_typo"):
        body["fix_typo"] = normalize_boolean(body["fix_typo"])
    if body.get("no_cache"):
        body["no_cache"] = normalize_boolean(body["no_cache"])

    if not body.get("engine"):
        body["engine"] = "yandex"
    if not body.get("text"):
        raise SystemExit("Missing search text. Provide --text or --query.")

    return body


def markdown_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def preview_table(body: dict[str, str]) -> str:
    rows = ["| 参数名 | 当前值 | 默认值 | 说明 |", "| --- | --- | --- | --- |"]
    for parameter in PARAMETERS:
        name = parameter["name"]
        current = body.get(name, "不传")
        default = parameter["default"] if parameter["default"] is not None else "无"
        rows.append(
            "| {name} | {current} | {default} | {description} |".format(
                name=markdown_escape(name),
                current=markdown_escape(current),
                default=markdown_escape(default),
                description=markdown_escape(parameter["description"]),
            )
        )
    return "\n".join(rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Call the Dataify Yandex search API and print the raw response body."
    )
    parser.add_argument("--text", help="Yandex search query.")
    parser.add_argument("--query", help="Alias for --text.")
    parser.add_argument(
        "--token",
        help="Dataify API token. If omitted, DATAIFY_API_TOKEN is used when available.",
    )
    parser.add_argument(
        "--json",
        dest="json_format",
        help="Output format: 1, 2, 3, 4, json, json+html, html, or light-json.",
    )
    parser.add_argument("--yandex-domain", help="Yandex domain, for example yandex.com or yandex.ru.")
    parser.add_argument("--lang", help="Yandex search language.")
    parser.add_argument("--lr", help="Country or region ID.")
    parser.add_argument("--p", help="Page number, starting from 0.")
    parser.add_argument("--family-mode", help="Safe search mode: 0/off, 1/moderate, 2/strict.")
    parser.add_argument("--fix-typo", help="Enable typo correction: true or false.")
    parser.add_argument("--groups-on-page", help="Maximum result groups per page.")
    parser.add_argument("--no-cache", help="Bypass cache: true or false.")
    parser.add_argument("--params-json", help="JSON object containing raw API field overrides. Use null to omit a defaulted field.")
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Print the request-parameter preview table and do not call the API.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    body = build_body(args)

    if args.preview:
        print(preview_table(body))
        return 0

    token = args.token or os.environ.get("DATAIFY_API_TOKEN", "")
    if not token.strip():
        print(
            "Missing Dataify API token. Please provide a token or register at https://dashboard.dataify.com/login?utm_source=skill.",
            file=sys.stderr,
        )
        return 2

    payload = urllib.parse.urlencode(body).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=payload,
        method="POST",
        headers={
            "Authorization": normalize_authorization(token),
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    try:
        with urllib.request.urlopen(request) as response:
            sys.stdout.buffer.write(response.read())
    except urllib.error.HTTPError as exc:
        sys.stdout.buffer.write(exc.read())
        return exc.code

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
