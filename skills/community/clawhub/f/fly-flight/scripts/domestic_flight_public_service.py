#!/usr/bin/env python3
"""Backward-compatible flight-only wrapper around the unified transport service."""

from __future__ import annotations

import argparse
import json
import sys
from http.server import ThreadingHTTPServer

from providers import flight_public_service
from transport_service import DEFAULT_HOST, DEFAULT_PORT, TransportHandler


def serve(args: argparse.Namespace) -> None:
    server = ThreadingHTTPServer((args.host, args.port), TransportHandler)
    print(
        json.dumps(
            {
                "ok": True,
                "host": args.host,
                "port": args.port,
                "mode": "flight",
                "search_example": (
                    f"http://{args.host}:{args.port}/search"
                    "?mode=flight&from=北京&to=上海&date=2026-03-20&sort_by=price&direct_only=1"
                ),
            },
            ensure_ascii=False,
        )
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser("search", help="Query flights and print JSON.")
    search.add_argument("--from", dest="origin", required=True, help="出发城市、机场名或三字码")
    search.add_argument("--to", dest="destination", required=True, help="到达城市、机场名或三字码")
    search.add_argument("--date", required=True, help="出发日期，格式 YYYY-MM-DD")
    search.add_argument("--return-date", help="返程日期，格式 YYYY-MM-DD")
    search.add_argument("--limit", type=int, default=10, help="最多返回多少条")
    search.add_argument("--timeout", type=int, default=20, help="页面抓取超时秒数")
    search.add_argument("--sort-by", default="price", help="排序方式: price/departure/arrival/duration")
    search.add_argument("--return-sort-by", help="返程排序方式，默认沿用 --sort-by")
    search.add_argument("--direct-only", action="store_true", help="仅保留直飞")
    search.add_argument("--airline", help="按航司代码或名称过滤，例如 MU / 东航")
    search.add_argument("--preferred-departure-airport", help="限定去程起飞机场，如 北京首都 / PKX")
    search.add_argument("--preferred-arrival-airport", help="限定去程到达机场，如 上海虹桥 / PVG")
    search.add_argument("--return-preferred-departure-airport", help="限定返程起飞机场")
    search.add_argument("--return-preferred-arrival-airport", help="限定返程到达机场")
    search.add_argument("--sample-state", help="使用本地 JSON 样例状态代替真实网页抓取")
    search.add_argument("--return-sample-state", help="返程使用本地 JSON 样例状态代替真实网页抓取")
    search.add_argument("--pretty", action="store_true", help="格式化输出 JSON")

    serve_parser = subparsers.add_parser("serve", help="Start a local HTTP service.")
    serve_parser.add_argument("--host", default=DEFAULT_HOST, help=f"监听地址，默认 {DEFAULT_HOST}")
    serve_parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"监听端口，默认 {DEFAULT_PORT}")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "search":
            payload = flight_public_service.run_search(args)
            if "outbound" in payload and "options" in payload["outbound"]:
                payload["outbound"]["flights"] = payload["outbound"]["options"]
            if "return" in payload and "options" in payload["return"]:
                payload["return"]["flights"] = payload["return"]["options"]
            print(json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None))
            return 0
        if args.command == "serve":
            serve(args)
            return 0
    except BrokenPipeError:
        return 0
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1

    parser.error("未知命令")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
