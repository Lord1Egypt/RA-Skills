#!/usr/bin/env python3
import argparse
import json
import os
import sys
from typing import Any, Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_URL = "https://open.bigmodel.cn/api"
WEB_SEARCH_URL = f"{BASE_URL}/paas/v4/web_search"
CHAT_URL = f"{BASE_URL}/paas/v4/chat/completions"
RECENCY_CHOICES = ["oneDay", "oneWeek", "oneMonth", "oneYear", "noLimit"]
ENGINE_CHOICES = ["search_std", "search_pro", "search_pro_sogou", "search_pro_quark"]
CONTENT_SIZE_CHOICES = ["medium", "high"]
DEFAULT_MODEL = "glm-4.7-flash"


def get_api_key() -> Optional[str]:
    return (
        os.environ.get("ZAI_API_KEY")
        or os.environ.get("ZHIPUAI_API_KEY")
        or os.environ.get("BIGMODEL_API_KEY")
    )


def post_json(url: str, payload: Dict[str, Any], api_key: str, timeout: int) -> Dict[str, Any]:
    req = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            data = json.loads(body)
            return {"ok": True, "status": resp.status, "data": data}
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {
            "ok": False,
            "stage": "http",
            "status": e.code,
            "error": body,
        }
    except URLError as e:
        return {"ok": False, "stage": "network", "error": str(e)}
    except Exception as e:  # pragma: no cover - defensive
        return {"ok": False, "stage": "exception", "error": repr(e)}


def build_web_search_payload(args: argparse.Namespace) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "search_query": args.query,
        "search_engine": args.engine,
        "search_intent": bool(args.intent),
        "count": args.count,
        "content_size": args.content_size,
    }
    if args.domain_filter:
        payload["search_domain_filter"] = args.domain_filter
    if args.recency:
        payload["search_recency_filter"] = args.recency
    if args.user_id:
        payload["user_id"] = args.user_id
    if args.request_id:
        payload["request_id"] = args.request_id
    return payload


def build_chat_payload(args: argparse.Namespace) -> Dict[str, Any]:
    web_search: Dict[str, Any] = {
        "enable": True,
        "search_engine": args.engine,
        "search_result": True,
        "count": args.count,
        "content_size": args.content_size,
    }
    if args.prompt:
        web_search["search_prompt"] = args.prompt
    if args.domain_filter:
        web_search["search_domain_filter"] = args.domain_filter
    if args.recency:
        web_search["search_recency_filter"] = args.recency

    payload: Dict[str, Any] = {
        "model": args.model,
        "messages": [{"role": "user", "content": args.query}],
        "tools": [{"type": "web_search", "web_search": web_search}],
        "stream": False,
    }
    return payload


def normalize_web_search_response(data: Dict[str, Any]) -> Dict[str, Any]:
    results = data.get("search_result") or []
    return {
        "request_id": data.get("request_id"),
        "intent": data.get("search_intent"),
        "result_count": len(results),
        "results": [
            {
                "title": item.get("title"),
                "link": item.get("link"),
                "media": item.get("media"),
                "publish_date": item.get("publish_date"),
                "content": item.get("content"),
                "refer": item.get("refer"),
            }
            for item in results
        ],
    }


def normalize_chat_response(data: Dict[str, Any]) -> Dict[str, Any]:
    choices = data.get("choices") or []
    choice = choices[0] if choices else {}
    message = choice.get("message") or {}
    return {
        "request_id": data.get("request_id"),
        "model": data.get("model"),
        "finish_reason": choice.get("finish_reason"),
        "answer": message.get("content"),
        "usage": data.get("usage"),
    }


def emit(obj: Dict[str, Any], pretty: bool) -> None:
    if pretty:
        print(json.dumps(obj, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(obj, ensure_ascii=False))


def main() -> int:
    parser = argparse.ArgumentParser(description="Zhipu web search wrapper for OpenClaw skills")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    raw = subparsers.add_parser("raw", help="Call Zhipu Web Search API directly")
    raw.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    raw.add_argument("--timeout", type=int, default=60, help="HTTP timeout in seconds")
    raw.add_argument("--query", required=True, help="Search query")
    raw.add_argument("--engine", default="search_std", choices=ENGINE_CHOICES)
    raw.add_argument("--count", type=int, default=5)
    raw.add_argument("--intent", action="store_true", help="Enable intent recognition before search")
    raw.add_argument("--domain-filter")
    raw.add_argument("--recency", default="noLimit", choices=RECENCY_CHOICES)
    raw.add_argument("--content-size", default="medium", choices=CONTENT_SIZE_CHOICES)
    raw.add_argument("--request-id")
    raw.add_argument("--user-id")

    chat = subparsers.add_parser("chat", help="Call chat/completions with web_search tool")
    chat.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    chat.add_argument("--timeout", type=int, default=60, help="HTTP timeout in seconds")
    chat.add_argument("--query", required=True, help="User question")
    chat.add_argument("--engine", default="search_std", choices=ENGINE_CHOICES)
    chat.add_argument("--count", type=int, default=5)
    chat.add_argument("--domain-filter")
    chat.add_argument("--recency", default="noLimit", choices=RECENCY_CHOICES)
    chat.add_argument("--content-size", default="medium", choices=CONTENT_SIZE_CHOICES)
    chat.add_argument("--model", default=DEFAULT_MODEL)
    chat.add_argument(
        "--prompt",
        help="Optional search_prompt passed to the web_search tool for answer style control",
    )

    args = parser.parse_args()
    api_key = get_api_key()
    if not api_key:
        emit(
            {
                "ok": False,
                "stage": "auth",
                "error": "Missing API key. Set ZAI_API_KEY, ZHIPUAI_API_KEY, or BIGMODEL_API_KEY.",
            },
            args.pretty,
        )
        return 1

    if args.mode == "raw":
        result = post_json(WEB_SEARCH_URL, build_web_search_payload(args), api_key, args.timeout)
        if not result.get("ok"):
            emit(result, args.pretty)
            return 2
        emit({"ok": True, **normalize_web_search_response(result["data"])}, args.pretty)
        return 0

    result = post_json(CHAT_URL, build_chat_payload(args), api_key, args.timeout)
    if not result.get("ok"):
        emit(result, args.pretty)
        return 2
    emit({"ok": True, **normalize_chat_response(result["data"])}, args.pretty)
    return 0


if __name__ == "__main__":
    sys.exit(main())
