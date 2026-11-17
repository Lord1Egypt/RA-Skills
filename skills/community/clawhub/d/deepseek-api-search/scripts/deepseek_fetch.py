#!/usr/bin/env python3
"""Fetch one webpage as Markdown through the DeepSeek Fetch API."""

import argparse
import json
import sys
from urllib.parse import urlsplit

from deepseek_search import SearchError as FetchError, request_json

FETCH_URL = "https://api.deepseek.com/v1/tools/fetch"


def validate_url(url: str) -> None:
    if not isinstance(url, str) or not url or len(url) > 8192:
        raise ValueError("url 必须为 1～8192 个字符。")
    if any(char.isspace() or ord(char) < 32 or ord(char) == 127 for char in url):
        raise ValueError("url 不能包含空白或控制字符，请先进行 URL 编码。")
    try:
        parsed = urlsplit(url)
        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            raise ValueError
        if parsed.username is not None or parsed.password is not None:
            raise ValueError
        # Accessing .port validates malformed and out-of-range port numbers.
        parsed.port
    except ValueError:
        raise ValueError("url 必须为包含 host 的 HTTP/HTTPS 地址，且不能携带用户名或密码。") from None


def fetch(url: str, timeout: float = 60.0, retries: int = 2) -> dict:
    """Return {title, content} from the API; raise FetchError / ValueError on failure."""
    validate_url(url)
    result = request_json(FETCH_URL, {"url": url}, timeout, retries)
    if (
        not isinstance(result, dict)
        or "error" in result
        or not isinstance(result.get("title"), str)
        or not isinstance(result.get("content"), str)
    ):
        raise FetchError("DeepSeek 响应结构异常：预期字符串 title 和 content。")
    return result


def to_markdown(result: dict) -> str:
    # Preserve the API's Markdown, including headings, tables, and code blocks.
    return result["content"]


def main() -> int:
    parser = argparse.ArgumentParser(description="通过 DeepSeek Fetch API 抓取网页正文")
    parser.add_argument("-u", "--url", required=True, help="不含用户名或密码的 HTTP/HTTPS URL，最多 8192 字符")
    parser.add_argument("--format", choices=("raw", "md"), default="raw")
    parser.add_argument("--timeout", type=float, default=60.0, help="单次请求超时秒数（默认 60）")
    parser.add_argument("--retries", type=int, default=2, help="额外重试次数，0～5（默认 2）")
    args = parser.parse_args()
    try:
        result = fetch(args.url, timeout=args.timeout, retries=args.retries)
    except (ValueError, FetchError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    if args.format == "md":
        sys.stdout.write(to_markdown(result))
    else:
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
