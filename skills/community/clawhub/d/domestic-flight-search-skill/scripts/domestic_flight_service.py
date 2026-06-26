#!/usr/bin/env python3
"""Query China domestic flights from the Juhe flight API and expose a local HTTP service."""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "assets" / "data"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
API_URL = "https://apis.juhe.cn/flight/query"
API_KEY_ENV_NAMES = ("JUHE_FLIGHT_API_KEY", "JUHE_API_KEY")


def load_json(path: Path) -> dict[str, str]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


CITY_CODES = load_json(DATA_DIR / "domestic_city_codes.json")
AIRPORT_ALIASES = load_json(DATA_DIR / "airport_aliases.json")


@dataclass(frozen=True)
class Place:
    raw: str
    query: str
    code: str
    resolved_as: str


def normalize_place_name(value: str) -> str:
    cleaned = value.strip()
    for suffix in ("机场", "国际机场"):
        if cleaned.endswith(suffix):
            break
    return cleaned


def canonicalize_place(value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("地点不能为空")
    if len(cleaned) == 3 and cleaned.isalpha():
        return cleaned.upper()
    for suffix in ("特别行政区", "自治区", "自治州", "省", "市"):
        if cleaned.endswith(suffix):
            cleaned = cleaned[: -len(suffix)]
            break
    return cleaned.replace(" ", "")


def resolve_place(value: str) -> Place:
    normalized = canonicalize_place(value)
    if len(normalized) == 3 and normalized.isalpha():
        code = normalized.upper()
        return Place(raw=value, query=normalized, code=code, resolved_as="iata")

    if normalized in AIRPORT_ALIASES:
        code = AIRPORT_ALIASES[normalized]
        return Place(raw=value, query=normalized, code=code, resolved_as="airport")

    if normalized in CITY_CODES:
        code = CITY_CODES[normalized]
        return Place(raw=value, query=normalized, code=code, resolved_as="city")

    raise ValueError(
        f"无法识别地点“{value}”。请改用常见城市名、具体机场名，或直接提供三字码。"
    )


def validate_date(value: str) -> str:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("日期必须是 YYYY-MM-DD 格式") from exc
    return value


def get_api_key() -> str:
    for env_name in API_KEY_ENV_NAMES:
        value = os.getenv(env_name)
        if value:
            return value
    raise RuntimeError(
        "缺少聚合数据 API Key。请设置 JUHE_FLIGHT_API_KEY 或 JUHE_API_KEY。"
    )


class JuheFlightClient:
    def __init__(self, api_key: str, timeout: int = 20) -> None:
        self.api_key = api_key
        self.timeout = timeout

    def query(
        self,
        departure: str,
        arrival: str,
        departure_date: str,
        flight_no: str = "",
        max_segments: int = 1,
    ) -> dict[str, Any]:
        params = {
            "key": self.api_key,
            "departure": departure,
            "arrival": arrival,
            "departureDate": departure_date,
            "flightNo": flight_no,
            "maxSegments": max_segments,
        }
        url = f"{API_URL}?{urlencode(params)}"
        request = Request(url, headers={"User-Agent": "OpenClaw-DomesticFlightSearch/1.0"})
        with urlopen(request, timeout=self.timeout) as response:
            return json.loads(response.read().decode("utf-8"))


def simplify_flight(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "airline_code": item.get("airline"),
        "airline_name": item.get("airlineName"),
        "flight_no": item.get("flightNo"),
        "equipment": item.get("equipment"),
        "is_codeshare": bool(item.get("isCodeShare")),
        "departure_code": item.get("departure"),
        "departure_name": item.get("departureName"),
        "departure_date": item.get("departureDate"),
        "departure_time": item.get("departureTime"),
        "arrival_code": item.get("arrival"),
        "arrival_name": item.get("arrivalName"),
        "arrival_date": item.get("arrivalDate"),
        "arrival_time": item.get("arrivalTime"),
        "duration": item.get("duration"),
        "segments": item.get("transferNum"),
        "ticket_price": item.get("ticketPrice"),
        "raw": item,
    }


def normalize_provider_response(
    provider_payload: dict[str, Any],
    origin: Place,
    destination: Place,
    departure_date: str,
    limit: int,
) -> dict[str, Any]:
    error_code = provider_payload.get("error_code", -1)
    if error_code != 0:
        raise RuntimeError(
            f"聚合接口返回失败: error_code={error_code}, reason={provider_payload.get('reason')}"
        )

    result = provider_payload.get("result") or {}
    flights = [
        simplify_flight(item)
        for item in (result.get("flightInfo") or [])
    ]
    flights.sort(key=lambda item: (item.get("ticket_price") is None, item.get("ticket_price", 0)))
    trimmed = flights[:limit]

    return {
        "provider": "juhe",
        "provider_reference": result.get("orderid"),
        "reason": provider_payload.get("reason"),
        "route": {
            "from": {"input": origin.raw, "query": origin.query, "code": origin.code, "resolved_as": origin.resolved_as},
            "to": {
                "input": destination.raw,
                "query": destination.query,
                "code": destination.code,
                "resolved_as": destination.resolved_as,
            },
            "date": departure_date,
        },
        "count": len(trimmed),
        "total_found": len(flights),
        "flights": trimmed,
    }


def run_search(args: argparse.Namespace) -> dict[str, Any]:
    origin = resolve_place(args.origin)
    destination = resolve_place(args.destination)
    departure_date = validate_date(args.date)

    if args.sample_response:
        with open(args.sample_response, "r", encoding="utf-8") as handle:
            provider_payload = json.load(handle)
    else:
        client = JuheFlightClient(get_api_key(), timeout=args.timeout)
        provider_payload = client.query(
            departure=origin.code,
            arrival=destination.code,
            departure_date=departure_date,
            flight_no=args.flight_no,
            max_segments=args.max_segments,
        )

    return normalize_provider_response(
        provider_payload=provider_payload,
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        limit=args.limit,
    )


class FlightHandler(BaseHTTPRequestHandler):
    server_version = "DomesticFlightSearch/1.0"

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self.send_json(200, {"ok": True, "service": "domestic-flight-search"})
            return

        if parsed.path != "/search":
            self.send_json(404, {"ok": False, "error": "not_found"})
            return

        params = parse_qs(parsed.query, keep_blank_values=False)
        try:
            args = argparse.Namespace(
                origin=self.require_param(params, "from"),
                destination=self.require_param(params, "to"),
                date=self.require_param(params, "date"),
                limit=int(params.get("limit", ["10"])[0]),
                max_segments=int(params.get("max_segments", ["1"])[0]),
                flight_no=params.get("flight_no", [""])[0],
                timeout=int(params.get("timeout", ["20"])[0]),
                sample_response=params.get("sample_response", [None])[0],
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
    server = ThreadingHTTPServer((args.host, args.port), FlightHandler)
    print(
        json.dumps(
            {
                "ok": True,
                "host": args.host,
                "port": args.port,
                "search_example": f"http://{args.host}:{args.port}/search?from=北京&to=上海&date=2026-03-20",
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
    search.add_argument("--flight-no", default="", help="可选，指定航班号")
    search.add_argument("--max-segments", type=int, default=1, help="最大航段数，默认 1")
    search.add_argument("--limit", type=int, default=10, help="最多返回多少条")
    search.add_argument("--timeout", type=int, default=20, help="接口超时秒数")
    search.add_argument(
        "--sample-response",
        help="使用本地 JSON 样例响应代替真实 API，便于调试和测试",
    )
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
            output = json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None)
            print(output)
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
