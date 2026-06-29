#!/usr/bin/env python3
"""Minimal FinXData curl wrapper for MCP-aligned HTTP JSON endpoints."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
import urllib.parse
from typing import Any

DEFAULT_BASE_URL = "https://api.finxdata.ai"
TIMEOUT_SECONDS = 30
RETRY_COUNT = 3
RETRY_DELAY_SECONDS = 2
RETRY_MAX_TIME_SECONDS = 60
REQUEST_DELAY_SECONDS = 3
BATCH_CODE_ENDPOINTS = {
    ("stock", "quote"),
    ("market", "price"),
    ("agent", "market-price"),
    ("agent", "stock-quote"),
}
FANOUT_CODE_ENDPOINTS = {("stock", "kline")}
AGENT_ENDPOINTS = {
    ("agent", "market-price"),
    ("agent", "stock-quote"),
    ("agent", "hot-sectors"),
    ("agent", "hot-sector"),
    ("agent", "hot-reason"),
    ("agent", "dragon-tiger"),
    ("agent", "track-news"),
    ("agent", "track-market"),
    ("agent", "track-notice"),
    ("agent", "economy-calendar"),
    ("agent", "ontology-abstract"),
    ("agent", "financial"),
}

ENDPOINTS: dict[tuple[str, str], dict[str, Any]] = {
    ("stock", "summary"): {
        "path": "/api/v1/http/stock/summary",
        "parameters": [("code", True, None)],
    },
    ("stock", "quote"): {
        "path": "/api/v1/http/stock/quote",
        "parameters": [("code", True, None)],
    },
    ("stock", "financial"): {
        "path": "/api/v1/http/stock/financial",
        "parameters": [("code", True, None), ("sections", False, "reports")],
    },
    ("stock", "financial-quick-analysis"): {
        "path": "/api/v1/http/stock/financial/quick-analysis",
        "parameters": [
            ("code", True, None),
            ("periods", False, 4),
            ("refresh", False, None),
        ],
    },
    ("stock", "mainops"): {
        "path": "/api/v1/http/stock/mainops",
        "parameters": [("code", True, None), ("years", False, 3)],
    },
    ("stock", "kline"): {
        "path": "/api/v1/http/stock/kline",
        "parameters": [("code", True, None), ("period", False, "daily")],
    },
    ("stock", "moneyflow"): {
        "path": "/api/v1/http/stock/moneyflow",
        "parameters": [("code", True, None), ("days", False, 20)],
    },
    ("stock", "hot-reason"): {
        "path": "/api/v1/http/stock/hot_reason",
        "parameters": [
            ("code", True, None),
            ("days", False, 30),
            ("refresh_today", False, None),
        ],
    },
    ("stock", "dragon-tiger-seats"): {
        "path": "/api/v1/http/stock/dragon_tiger/seats",
        "parameters": [
            ("code", True, None),
            ("trade_date", False, None),
            ("look_back", False, 30),
            ("refresh", False, None),
        ],
    },
    ("stock", "notice-summary"): {
        "path": "/api/v1/http/stock/notice/summary",
        "parameters": [("code", True, None), ("refresh", False, None)],
    },
    ("stock", "lockup"): {
        "path": "/api/v1/http/stock/lockup",
        "parameters": [
            ("code", True, None),
            ("trade_date", False, None),
            ("forward_days", False, 90),
            ("refresh", False, None),
        ],
    },
    ("stock", "ontology"): {
        "path": "/api/v1/http/stock/ontology",
        "parameters": [("code", True, None)],
    },
    ("stock", "listing"): {
        "path": "/api/v1/http/stock/listing",
        "parameters": [("limit", False, 20)],
    },
    ("stock", "forecast"): {
        "path": "/api/v1/http/stock/forecast",
        "parameters": [
            ("page", False, 1),
            ("page_size", False, 50),
            ("refresh", False, None),
        ],
    },
    ("stock", "trade-calendar"): {
        "path": "/api/v1/http/stock/trade_calendar",
        "parameters": [
            ("year", False, None),
            ("month", False, None),
            ("months", False, 3),
        ],
    },
    ("market", "price"): {
        "path": "/api/v1/http/market/price",
        "parameters": [("code", True, None)],
    },
    ("market", "kline"): {
        "path": "/api/v1/http/market/kline",
        "parameters": [
            ("code", True, None),
            ("period", False, "daily"),
            ("limit", False, 30),
        ],
    },
    ("market", "hot-sectors"): {
        "path": "/api/v1/http/market/hot_sectors",
        "parameters": [],
    },
    ("market", "hot-sector"): {
        "path": "/api/v1/http/market/hot_sector",
        "parameters": [
            ("name", False, None),
            ("theme_id", False, None),
            ("days", False, 1),
            ("track_date", False, None),
        ],
    },
    ("market", "hot-stocks"): {
        "path": "/api/v1/http/market/hot_stocks",
        "parameters": [
            ("track_date", False, None),
            ("limit", False, 100),
            ("refresh", False, None),
        ],
    },
    ("market", "dragon-tiger"): {
        "path": "/api/v1/http/market/dragon_tiger",
        "parameters": [
            ("trade_date", False, None),
            ("min_net_buy", False, None),
            ("limit", False, 100),
            ("refresh", False, None),
        ],
    },
    ("market", "northbound-intraday"): {
        "path": "/api/v1/http/market/northbound/intraday",
        "parameters": [
            ("trade_date", False, None),
            ("refresh", False, None),
        ],
    },
    ("market", "northbound-history"): {
        "path": "/api/v1/http/market/northbound/history",
        "parameters": [("days", False, 20)],
    },
    ("agent", "market-price"): {
        "path": "/api/v1/http/agent/market/price",
        "parameters": [("code", True, None)],
    },
    ("agent", "stock-quote"): {
        "path": "/api/v1/http/agent/stock/quote",
        "parameters": [("code", True, None)],
    },
    ("agent", "hot-sectors"): {
        "path": "/api/v1/http/agent/market/hot_sectors",
        "parameters": [],
    },
    ("agent", "hot-sector"): {
        "path": "/api/v1/http/agent/market/hot_sector",
        "parameters": [
            ("name", False, None),
            ("theme_id", False, None),
            ("days", False, 1),
            ("track_date", False, None),
        ],
    },
    ("agent", "hot-reason"): {
        "path": "/api/v1/http/agent/stock/hot_reason",
        "parameters": [("code", True, None), ("days", False, 30)],
    },
    ("agent", "dragon-tiger"): {
        "path": "/api/v1/http/agent/market/dragon_tiger",
        "parameters": [
            ("trade_date", False, None),
            ("min_net_buy", False, None),
            ("limit", False, 100),
            ("refresh", False, None),
        ],
    },
    ("agent", "track-news"): {
        "path": "/api/v1/http/agent/track/news",
        "parameters": [],
    },
    ("agent", "track-market"): {
        "path": "/api/v1/http/agent/track/market",
        "parameters": [],
    },
    ("agent", "track-notice"): {
        "path": "/api/v1/http/agent/track/notice",
        "parameters": [],
    },
    ("agent", "economy-calendar"): {
        "path": "/api/v1/http/agent/economy/calendar",
        "parameters": [
            ("year", False, None),
            ("month", False, None),
            ("months", False, 3),
        ],
    },
    ("agent", "ontology-abstract"): {
        "path": "/api/v1/http/agent/ontology/abstract",
        "parameters": [("code", True, None)],
    },
    ("agent", "financial"): {
        "path": "/api/v1/http/agent/financial",
        "parameters": [("code", True, None)],
    },
    ("alternative", "default"): {
        "path": "/api/v1/http/alternative",
        "parameters": [("type", True, None), ("refresh", False, None)],
    },
    ("economy", "china"): {
        "path": "/api/v1/http/economy/china",
        "parameters": [("type", True, None)],
    },
    ("economy", "china-types"): {
        "path": "/api/v1/http/economy/china/types",
        "parameters": [],
    },
    ("economy", "us"): {
        "path": "/api/v1/http/economy/us",
        "parameters": [("type", True, None)],
    },
    ("economy", "us-types"): {
        "path": "/api/v1/http/economy/us/types",
        "parameters": [],
    },
    ("economy", "calendar"): {
        "path": "/api/v1/http/economy/calendar",
        "parameters": [
            ("year", False, None),
            ("month", False, None),
            ("months", False, 3),
        ],
    },
    ("track", "news"): {"path": "/api/v1/http/track/news", "parameters": []},
    ("track", "market"): {"path": "/api/v1/http/track/market", "parameters": []},
    ("track", "notice"): {"path": "/api/v1/http/track/notice", "parameters": []},
    ("fred", "series-list"): {"path": "/api/v1/http/fred/series", "parameters": []},
    ("fred", "series"): {
        "path": "/api/v1/http/fred/series/{series_id}",
        "parameters": [
            ("series_id", True, None),
            ("observation_start", False, None),
            ("observation_end", False, None),
            ("limit", False, None),
        ],
    },
    ("fred", "key-indicators"): {
        "path": "/api/v1/http/fred/key-indicators",
        "parameters": [
            ("observation_start", False, None),
            ("observation_end", False, None),
        ],
    },
}

HTTP_ENDPOINTS = {
    key: (spec["path"], tuple(param[0] for param in spec["parameters"]))
    for key, spec in ENDPOINTS.items()
}


def env_base_url() -> str:
    return (
        os.environ.get("FINXDATA_BASE_URL")
        or os.environ.get("FINDATA_BASE_URL")
        or DEFAULT_BASE_URL
    ).rstrip("/")


def env_api_key(required: bool = True) -> str | None:
    key = os.environ.get("FINXDATA_API_KEY") or os.environ.get("FINDATA_API_KEY")
    if required and not key:
        fail("FINXDATA_API_KEY is not set", code="missing_api_key", exit_code=2)
    return key


def env_agent_type() -> str | None:
    agent_type = os.environ.get("FINXDATA_AGENT_TYPE") or os.environ.get("AGENT_TYPE")
    if agent_type:
        return agent_type
    return None


def sanitize(message: str) -> str:
    key = os.environ.get("FINXDATA_API_KEY") or os.environ.get("FINDATA_API_KEY")
    if key:
        message = message.replace(key, f"{key[:8]}...")
    return message


def fail(message: str, code: str = "error", exit_code: int = 1) -> None:
    print(
        json.dumps(
            {"ok": False, "code": code, "message": sanitize(message)},
            ensure_ascii=False,
        )
    )
    raise SystemExit(exit_code)


def friendly_http_error(status: int, body: str) -> tuple[str, str]:
    detail = body.strip()
    try:
        parsed = json.loads(detail)
        if isinstance(parsed, dict):
            detail = str(
                parsed.get("message")
                or parsed.get("detail")
                or parsed.get("error")
                or detail
            )
    except json.JSONDecodeError:
        pass

    if status in {401, 403}:
        return (
            "auth_failed",
            "API Key 无效或无权访问该接口。请确认 FINXDATA_API_KEY 是否正确、未过期，并且账号已开通对应权限。",
        )
    if status == 404:
        return (
            "not_found",
            "接口或数据不存在。请先运行 summary 确认接口名称，或检查股票代码、日期、指标类型是否正确。",
        )
    if status == 429:
        return (
            "quota_limited",
            "当前 API Key 已触发额度或频率限制。请先运行 quota 查看剩余额度；如果额度不足，需要等待重置、减少调用频率或升级/充值。",
        )
    if status in {500, 502, 503, 504}:
        return (
            "service_unavailable",
            "FinXData 服务或上游数据源暂时不可用，脚本已经自动重试但仍失败。请稍后再试。",
        )

    message = f"HTTP {status} 请求失败。"
    if detail:
        message = f"{message} 服务返回：{detail}"
    return "http_failed", message


def friendly_curl_error(returncode: int, stderr: str) -> tuple[str, str]:
    error_map = {
        6: (
            "network_dns_failed",
            "无法解析 FinXData 域名，请检查网络或 FINXDATA_BASE_URL。",
        ),
        7: (
            "network_connect_failed",
            "无法连接 FinXData 服务，请检查网络、代理或服务地址。",
        ),
        28: (
            "network_timeout",
            "请求超时。脚本已经自动重试但仍未成功，请稍后再试或缩小查询范围。",
        ),
        35: ("network_tls_failed", "TLS/SSL 连接失败，请检查网络代理或本机证书配置。"),
        56: (
            "network_interrupted",
            "网络连接中断。脚本已经自动重试但仍失败，请稍后再试。",
        ),
    }
    code, message = error_map.get(
        returncode,
        ("curl_failed", f"请求未完成，curl 退出码为 {returncode}。"),
    )
    if os.environ.get("FINXDATA_DEBUG") and stderr.strip():
        message = f"{message} 原始错误：{stderr.strip()}"
    return code, message


def build_url(path: str, params: dict[str, Any] | None = None) -> str:
    path_params = {}
    remaining = {}
    for key, value in (params or {}).items():
        if value is None:
            continue
        placeholder = "{" + key + "}"
        if placeholder in path:
            path_params[key] = str(value)
        else:
            remaining[key] = value
    for key, value in path_params.items():
        path = path.replace("{" + key + "}", urllib.parse.quote(value, safe=""))
    cleaned = remaining
    query = urllib.parse.urlencode(cleaned, doseq=True)
    url = f"{env_base_url()}{path}"
    return f"{url}?{query}" if query else url


def build_curl_args(
    path: str,
    params: dict[str, Any] | None = None,
    *,
    api_key_required: bool = True,
    idempotency_key: str | None = None,
    agent_type: str | None = None,
) -> list[str]:
    args = [
        "curl",
        "-sS",
        "--max-time",
        str(TIMEOUT_SECONDS),
        "--retry",
        str(RETRY_COUNT),
        "--retry-delay",
        str(RETRY_DELAY_SECONDS),
        "--retry-max-time",
        str(RETRY_MAX_TIME_SECONDS),
        "--retry-connrefused",
        "-H",
        "Accept: application/json",
        "-w",
        "\n__HTTP_STATUS__:%{http_code}",
    ]
    api_key = env_api_key(required=api_key_required)
    if api_key:
        args.extend(["-H", f"X-API-Key: {api_key}"])
    if idempotency_key:
        args.extend(["-H", f"Idempotency-Key: {idempotency_key}"])
    if agent_type:
        args.extend(["-H", f"x-agent-type: {agent_type}"])
    args.append(build_url(path, params))
    return args


def run_curl(args: list[str]) -> None:
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        code, message = friendly_curl_error(result.returncode, result.stderr)
        fail(message, code=code, exit_code=result.returncode)

    marker = "\n__HTTP_STATUS__:"
    body, separator, status_text = result.stdout.rpartition(marker)
    if not separator:
        fail("请求完成但无法读取 HTTP 状态码，请检查 curl 输出。", code="bad_response")

    try:
        status = int(status_text.strip())
    except ValueError:
        fail("请求完成但 HTTP 状态码格式异常。", code="bad_response")

    if 200 <= status < 300:
        print(body, end="" if body.endswith("\n") else "\n")
        return

    code, message = friendly_http_error(status, body)
    fail(message, code=code, exit_code=1)


def normalize_codes(value: Any) -> list[str]:
    values = value if isinstance(value, list) else [value]
    codes: list[str] = []
    for item in values:
        for code in str(item).split(","):
            normalized = code.strip()
            if normalized:
                codes.append(normalized)
    return codes


def command_health(_args: argparse.Namespace) -> None:
    run_curl(build_curl_args("/health", api_key_required=False))


def command_quota(_args: argparse.Namespace) -> None:
    run_curl(build_curl_args("/api/quota/api-key"))


def command_summary(_args: argparse.Namespace) -> None:
    run_curl(build_curl_args("/api/v1/summary", api_key_required=False))


def command_data(args: argparse.Namespace) -> None:
    spec = ENDPOINTS[(args.group, args.action)]
    params = {
        name: getattr(args, name) for name, _required, _default in spec["parameters"]
    }
    is_agent = (args.group, args.action) in AGENT_ENDPOINTS
    agent_type = None
    if is_agent:
        agent_type = getattr(args, "agent_type", None) or env_agent_type()
        if agent_type is None:
            fail(
                "Agent endpoint requires --agent-type, e.g. openclaw, hermes, or opencode",
                code="missing_agent_type",
                exit_code=2,
            )

    if (args.group, args.action) in BATCH_CODE_ENDPOINTS:
        codes = normalize_codes(params.get("code"))
        if not codes:
            fail("code is required", code="missing_code", exit_code=2)
        params["code"] = codes
        run_curl(
            build_curl_args(
                spec["path"],
                params,
                api_key_required=not is_agent,
                idempotency_key=getattr(args, "idempotency_key", None),
                agent_type=agent_type,
            )
        )
        return

    if (args.group, args.action) in FANOUT_CODE_ENDPOINTS:
        codes = normalize_codes(params.get("code"))
        if not codes:
            fail("code is required", code="missing_code", exit_code=2)
        for index, code in enumerate(codes):
            request_params = {**params, "code": code}
            run_curl(
                build_curl_args(
                    spec["path"],
                    request_params,
                    api_key_required=not is_agent,
                    idempotency_key=getattr(args, "idempotency_key", None),
                    agent_type=agent_type,
                )
            )
            if index < len(codes) - 1:
                time.sleep(REQUEST_DELAY_SECONDS)
        return

    run_curl(
        build_curl_args(
            spec["path"],
            params,
            api_key_required=not is_agent,
            idempotency_key=getattr(args, "idempotency_key", None),
            agent_type=agent_type,
        )
    )


def add_data_commands(subparsers: argparse._SubParsersAction) -> None:
    grouped: dict[str, list[tuple[str, dict[str, Any]]]] = {}
    for key, spec in ENDPOINTS.items():
        grouped.setdefault(key[0], []).append((key[1], spec))

    for group, actions in sorted(grouped.items()):
        group_parser = subparsers.add_parser(group, help=f"{group} data commands")
        action_parsers = group_parser.add_subparsers(dest="action", required=True)
        for action, spec in sorted(actions):
            action_parser = action_parsers.add_parser(action)
            for name, required, default in spec["parameters"]:
                kwargs: dict[str, Any] = {"dest": name, "required": required}
                if (
                    (group, action) in BATCH_CODE_ENDPOINTS
                    or (group, action) in FANOUT_CODE_ENDPOINTS
                ) and name == "code":
                    kwargs["nargs"] = "+"
                if name in {"refresh", "refresh_today"}:
                    kwargs["action"] = "store_true"
                    kwargs["default"] = default
                elif default is not None:
                    kwargs["default"] = default
                action_parser.add_argument(f"--{name.replace('_', '-')}", **kwargs)
            if (group, action) in AGENT_ENDPOINTS:
                action_parser.add_argument("--agent-type", "-agent-type")
            else:
                action_parser.add_argument("--idempotency-key")
            action_parser.set_defaults(func=command_data, group=group, action=action)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Call FinXData HTTP JSON APIs via curl."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    health = subparsers.add_parser("health", help="GET /health")
    health.set_defaults(func=command_health)

    quota = subparsers.add_parser("quota", help="GET /api/quota/api-key")
    quota.set_defaults(func=command_quota)

    summary = subparsers.add_parser("summary", help="GET /api/v1/summary")
    summary.set_defaults(func=command_summary)

    add_data_commands(subparsers)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
