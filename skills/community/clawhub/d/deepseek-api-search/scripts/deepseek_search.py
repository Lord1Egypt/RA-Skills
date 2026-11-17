#!/usr/bin/env python3
"""DeepSeek Search API and shared transport, using the standard library."""

import argparse
import ipaddress
import json
import math
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Optional

SEARCH_URL = "https://api.deepseek.com/v1/tools/search"


class SearchError(RuntimeError):
    """A configuration, transport, or API response error."""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Keep the Bearer token on the documented endpoint only."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def validate_text(value: str, name: str) -> None:
    if not isinstance(value, str) or not value.strip() or len(value) > 128:
        raise ValueError(f"{name} 必须为 1～128 个 Unicode 字符，且不能全为空白。")


def retry_delay(attempt: int, headers) -> float:
    value = headers.get("Retry-After", "") if headers else ""
    try:
        delay = float(value)
    except (TypeError, ValueError):
        try:
            date = parsedate_to_datetime(value)
            if date.tzinfo is None:
                date = date.replace(tzinfo=timezone.utc)
            delay = (date - datetime.now(timezone.utc)).total_seconds()
        except (TypeError, ValueError, OverflowError):
            delay = 2 ** attempt
    return min(30.0, max(0.0, delay)) if math.isfinite(delay) else 2 ** attempt


def api_error(status: int, body: bytes, key: str) -> str:
    hints = {
        400: "请求参数无效，请检查 query、count 或 url 等字段。",
        403: "网页抓取被安全策略拒绝。",
        404: "未能获取可用的网页正文，请检查 URL 或站点访问限制。",
        401: "鉴权失败，请检查 DEEPSEEK_API_KEY。",
        402: "账户余额不足。",
        429: "请求限流，请稍后重试。",
    }
    detail = ""
    try:
        obj = json.loads(body)
        error = obj.get("error") if isinstance(obj, dict) else None
        if isinstance(error, dict) and isinstance(error.get("message"), str):
            detail = error["message"]
    except (ValueError, UnicodeError):
        pass
    # Do not echo raw HTML, request headers, or credentials on errors.
    detail = " ".join(detail.replace(key, "[REDACTED]").split())[:500]
    message = f"DeepSeek HTTP {status}: {hints.get(status, 'API 请求失败。')}"
    return message + (f" {detail}" if detail else "")


def request_json(endpoint: str, payload: dict, timeout: float, retries: int) -> dict:
    """Send an authenticated request to a documented DeepSeek tool endpoint."""
    if (
        isinstance(timeout, bool) or not isinstance(timeout, (int, float))
        or not math.isfinite(timeout) or timeout <= 0
    ):
        raise ValueError("timeout 必须为有限正数。")
    if type(retries) is not int or not 0 <= retries <= 5:
        raise ValueError("retries 必须为 0～5 的整数。")


    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not key:
        raise SearchError("未找到 DEEPSEEK_API_KEY，请在配置该变量的终端执行。")
    if any(ord(char) < 33 or ord(char) > 126 for char in key):
        raise SearchError("DEEPSEEK_API_KEY 格式无效，请检查本地配置。")

    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    opener = urllib.request.build_opener(NoRedirect())
    for attempt in range(retries + 1):
        try:
            with opener.open(request, timeout=timeout) as response:
                body = response.read()
            break
        except urllib.error.HTTPError as exc:
            status, headers = exc.code, exc.headers
            error_body = exc.read()
            exc.close()
            if attempt < retries and (status in (408, 429) or 500 <= status <= 599):
                time.sleep(retry_delay(attempt, headers))
                continue
            raise SearchError(api_error(status, error_body, key)) from None
        except (urllib.error.URLError, OSError) as exc:
            if attempt < retries:
                time.sleep(2 ** attempt)
                continue
            reason = exc.reason if isinstance(exc, urllib.error.URLError) else exc
            raise SearchError(
                f"网络连接失败或超时（{type(reason).__name__}），请检查域名解析、代理与 TLS 配置。"
            ) from None

    try:
        result = json.loads(body)
    except (ValueError, UnicodeError):
        raise SearchError("DeepSeek 返回了非 JSON 响应。") from None
    return result


def search(
    query: str,
    count: int = 5,
    ori_question: Optional[str] = None,
    localization: Optional[str] = None,
    need_content: bool = False,
    timeout: float = 60.0,
    retries: int = 2,
) -> dict:
    """Return the unchanged API JSON, or raise ValueError / SearchError."""
    validate_text(query, "query")
    if type(count) is not int or not 1 <= count <= 50:
        raise ValueError("count 必须为 1～50 的整数。")
    if ori_question is not None:
        validate_text(ori_question, "ori_question")
    if localization is not None and not isinstance(localization, str):
        raise ValueError("localization 必须为 IP 地址字符串。")
    if localization is not None and localization != "":
        try:
            ipaddress.ip_address(localization)
        except ValueError:
            raise ValueError("localization 必须为有效的 IP 地址。") from None
    if type(need_content) is not bool:
        raise ValueError("need_content 必须为布尔值。")

    payload = {"query": query, "count": count, "need_content": need_content}
    if ori_question is not None:
        payload["ori_question"] = ori_question
    if localization is not None:
        payload["localization"] = localization
    result = request_json(SEARCH_URL, payload, timeout, retries)
    if (
        not isinstance(result, dict)
        or "error" in result
        or not isinstance(result.get("results"), list)
        or any(
            not isinstance(item, dict)
            or not isinstance(item.get("title"), str)
            or not isinstance(item.get("url"), str)
            for item in result["results"]
        )
    ):
        raise SearchError("DeepSeek 响应结构异常：预期 results 数组及条目标题、链接。")
    return result


def to_brave_like(result: dict, query: str) -> dict:
    return {
        "query": query,
        "results": [
            {"title": r["title"], "url": r["url"], "snippet": r.get("snippet", "")}
            for r in result["results"]
        ],
    }


def to_markdown(result: dict) -> str:
    if not result["results"]:
        return "未找到匹配结果。\n"
    lines = []
    fields = (("站点", "site_name"), ("发布时间", "date"),
              ("排序分数", "rerank_score"), ("权威性", "authority"))
    for index, item in enumerate(result["results"], 1):
        lines.extend([f"{index}. {item['title']}", f"   {item['url']}"])
        for label, field in fields:
            value = item.get(field)
            if value is not None:
                lines.append(f"   {label}: {value}")
        summary = item.get("summary") or item.get("snippet")
        if summary:
            lines.extend(["", str(summary)])
        if item.get("content"):
            lines.extend(["", "网页正文：", item["content"]])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="通过 DeepSeek Search API 搜索网页")
    parser.add_argument("-q", "--query", required=True, help="搜索词，1～128 个 Unicode 字符")
    parser.add_argument("-n", "--count", "--max-results", type=int, default=5, help="结果条数，1～50（默认 5）")
    parser.add_argument("--ori-question", help="触发搜索的原始问题，1～128 个字符")
    parser.add_argument("--localization", help="用于优先返回本地化结果的 IP 地址")
    parser.add_argument("--need-content", action="store_true", help="返回可用的网页正文")
    parser.add_argument("--format", choices=("raw", "brave", "md"), default="raw")
    parser.add_argument("--timeout", type=float, default=60.0, help="单次请求超时秒数（默认 60）")
    parser.add_argument("--retries", type=int, default=2, help="额外重试次数，0～5（默认 2）")
    args = parser.parse_args()
    try:
        result = search(
            query=args.query, count=args.count, ori_question=args.ori_question,
            localization=args.localization, need_content=args.need_content,
            timeout=args.timeout, retries=args.retries,
        )
    except (ValueError, SearchError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    if args.format == "md":
        sys.stdout.write(to_markdown(result))
    else:
        if args.format == "brave":
            result = to_brave_like(result, args.query)
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
