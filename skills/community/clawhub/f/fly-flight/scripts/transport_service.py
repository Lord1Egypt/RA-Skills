#!/usr/bin/env python3
"""Unified transport lookup entrypoint for flight and train modes."""

from __future__ import annotations

import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, urlparse

from providers import flight_public_service, train_public_service


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8766
TRANSPORT_MODES = {"auto", "flight", "train"}


def resolve_mode(mode: str) -> str:
    normalized = (mode or "auto").strip().lower()
    if normalized not in TRANSPORT_MODES:
        raise ValueError(f"mode 仅支持 {', '.join(sorted(TRANSPORT_MODES))}")
    if normalized == "auto":
        return "flight"
    return normalized


def run_search(args: argparse.Namespace) -> dict[str, Any]:
    mode = resolve_mode(args.mode)
    if mode == "flight":
        return flight_public_service.run_search(flight_public_service.build_search_namespace(args))
    if mode == "train":
        return train_public_service.run_search(train_public_service.build_search_namespace(args))
    raise ValueError(f"未知 mode: {mode}")


class TransportHandler(BaseHTTPRequestHandler):
    server_version = "TransportSearch/1.0"

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self.send_json(200, {"ok": True, "service": "fly-flight", "modes": ["flight", "train"]})
            return
        if parsed.path != "/search":
            self.send_json(404, {"ok": False, "error": "not_found"})
            return

        params = parse_qs(parsed.query, keep_blank_values=False)
        try:
            args = argparse.Namespace(
                mode=params.get("mode", ["auto"])[0],
                origin=self.require_param(params, "from"),
                destination=self.require_param(params, "to"),
                date=self.require_param(params, "date"),
                limit=int(params.get("limit", ["10"])[0]),
                timeout=int(params.get("timeout", ["20"])[0]),
                sort_by=params.get("sort_by", ["price"])[0],
                return_sort_by=params.get("return_sort_by", [""])[0] or None,
                return_date=params.get("return_date", [""])[0] or None,
                direct_only=params.get("direct_only", ["0"])[0] in {"1", "true", "yes"},
                airline=params.get("airline", [""])[0] or None,
                preferred_departure_airport=params.get("preferred_departure_airport", [""])[0] or None,
                preferred_arrival_airport=params.get("preferred_arrival_airport", [""])[0] or None,
                return_preferred_departure_airport=params.get("return_preferred_departure_airport", [""])[0] or None,
                return_preferred_arrival_airport=params.get("return_preferred_arrival_airport", [""])[0] or None,
                train_type=params.get("train_type", [""])[0] or None,
                seat_type=params.get("seat_type", [""])[0] or None,
                preferred_departure_station=params.get("preferred_departure_station", [""])[0] or None,
                preferred_arrival_station=params.get("preferred_arrival_station", [""])[0] or None,
                return_preferred_departure_station=params.get("return_preferred_departure_station", [""])[0] or None,
                return_preferred_arrival_station=params.get("return_preferred_arrival_station", [""])[0] or None,
                sample_state=params.get("sample_state", [None])[0],
                return_sample_state=params.get("return_sample_state", [None])[0],
                sample_train_query=params.get("sample_train_query", [None])[0],
                sample_train_price=params.get("sample_train_price", [None])[0],
                return_sample_train_query=params.get("return_sample_train_query", [None])[0],
                return_sample_train_price=params.get("return_sample_train_price", [None])[0],
            )
            payload = run_search(args)
            self.send_json(200, {"ok": True, "data": payload})
        except Exception as exc:  # noqa: BLE001
            self.send_json(400, {"ok": False, "error": str(exc)})

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        return

    @staticmethod
    def require_param(params: dict[str, list[str]], key: str) -> str:
        values = params.get(key)
        if not values or not values[0].strip():
            raise ValueError(f"缺少参数: {key}")
        return values[0]

    def send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def serve(args: argparse.Namespace) -> None:
    server = ThreadingHTTPServer((args.host, args.port), TransportHandler)
    print(
        json.dumps(
            {
                "ok": True,
                "host": args.host,
                "port": args.port,
                "modes": ["flight", "train"],
                "search_example": (
                    f"http://{args.host}:{args.port}/search"
                    "?mode=train&from=北京&to=上海&date=2026-03-20&sort_by=price&seat_type=second_class"
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

    search = subparsers.add_parser("search", help="Query transport options and print JSON.")
    search.add_argument("--mode", default="auto", help="交通方式: auto/flight/train")
    search.add_argument("--from", dest="origin", required=True, help="出发城市、机场名、车站名或代码")
    search.add_argument("--to", dest="destination", required=True, help="到达城市、机场名、车站名或代码")
    search.add_argument("--date", required=True, help="出发日期，格式 YYYY-MM-DD")
    search.add_argument("--return-date", help="返程日期，格式 YYYY-MM-DD")
    search.add_argument("--limit", type=int, default=10, help="最多返回多少条")
    search.add_argument("--timeout", type=int, default=20, help="页面抓取超时秒数")
    search.add_argument("--sort-by", default="price", help="排序方式: price/departure/arrival/duration")
    search.add_argument("--return-sort-by", help="返程排序方式，默认沿用 --sort-by")
    search.add_argument("--direct-only", action="store_true", help="flight 模式仅保留直飞")
    search.add_argument("--airline", help="flight 模式按航司代码或名称过滤")
    search.add_argument("--preferred-departure-airport", help="flight 模式限制去程起飞机场")
    search.add_argument("--preferred-arrival-airport", help="flight 模式限制去程到达机场")
    search.add_argument("--return-preferred-departure-airport", help="flight 模式限制返程起飞机场")
    search.add_argument("--return-preferred-arrival-airport", help="flight 模式限制返程到达机场")
    search.add_argument("--train-type", help="train 模式按车次类型过滤，例如 G,D,C 或 G,D")
    search.add_argument("--seat-type", help="train 模式选定席别: business_class/first_class/second_class")
    search.add_argument("--preferred-departure-station", help="train 模式限制去程出发站")
    search.add_argument("--preferred-arrival-station", help="train 模式限制去程到达站")
    search.add_argument("--return-preferred-departure-station", help="train 模式限制返程出发站")
    search.add_argument("--return-preferred-arrival-station", help="train 模式限制返程到达站")
    search.add_argument("--sample-state", help="flight 模式使用本地 JSON 样例状态代替真实网页抓取")
    search.add_argument("--return-sample-state", help="flight 模式返程使用本地 JSON 样例状态代替真实网页抓取")
    search.add_argument("--sample-train-query", help="train 模式使用本地 JSON 样例余票查询代替真实网页抓取")
    search.add_argument("--sample-train-price", help="train 模式使用本地 JSON 样例票价查询代替真实网页抓取")
    search.add_argument("--return-sample-train-query", help="train 模式返程使用本地 JSON 样例余票查询代替真实网页抓取")
    search.add_argument("--return-sample-train-price", help="train 模式返程使用本地 JSON 样例票价查询代替真实网页抓取")
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
            payload = run_search(args)
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
