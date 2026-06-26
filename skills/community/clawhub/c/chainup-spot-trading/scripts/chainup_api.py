#!/usr/bin/env python3
"""ChainUp/OpenAPI V2 wrapper for spot and margin endpoints.

Design goals:
- Keep request/signing logic centralized.
- Expose stable action names so the skill can call APIs directly with low reasoning overhead.
- Leave unknown required fields as TODO placeholders for future refinement.
"""

import argparse
from decimal import Decimal, InvalidOperation, ROUND_DOWN
import hashlib
import hmac
import json
import os
import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

USER_AGENT = "chainup-spot/1.1.0 (Skill)"
DEFAULT_TIMEOUT = 30
DEFAULT_TOOLS_FILE = "/root/TOOLS.md"

# TODO: refine required fields after real exchange validation.
TODO_REQUIRED_FIELDS: Dict[str, List[str]] = {
    "spot_depth": ["symbol", "limit(optional, default=10, max=100)"],
    "spot_ticker": [
        "symbol(optional)",
        "symbols(optional, comma-separated, e.g. btcusdt,ethusdt)",
        "timeZone(optional)",
    ],
    "spot_trades": ["symbol"],
    "spot_klines": [
        "symbol",
        "interval(required: 1min, 5min, 15min, 30min, 60min, 1day, 1week, 1month)",
        "startTime(optional)",
        "endTime(optional)",
        "timezone(optional, e.g. UTC-09)",
        "limit(optional, default=10)",
    ],
    "spot_create_order": [
        "symbol",
        "volume",
        "side",
        "type",
        "MARKET BUY uses volume as quote quantity, e.g. ETH/USDT volume=1 side=BUY means 1 USDT",
        "MARKET SELL uses volume as base quantity, e.g. ETH/USDT volume=0.1 side=SELL means 0.1 ETH",
    ],
    "spot_test_order": [
        "symbol",
        "volume",
        "side",
        "type",
        "MARKET BUY uses volume as quote quantity, e.g. ETH/USDT volume=1 side=BUY means 1 USDT",
        "MARKET SELL uses volume as base quantity, e.g. ETH/USDT volume=0.1 side=SELL means 0.1 ETH",
    ],
    "spot_batch_orders": ["orders"],
    "spot_get_order": ["symbol", "orderId or newClientOrderId"],
    "spot_cancel_order": ["symbol", "orderId or newClientOrderId"],
    "spot_batch_cancel": ["symbol", "orderIds or clientOrderIds"],
    "spot_open_orders": ["symbol(optional in some gateways)"],
    "spot_my_trades": ["symbol"],
    "asset_transfer": ["fromAccountType", "toAccountType", "asset", "amount"],
    "asset_transfer_query": [],
    "margin_create_order": [
        "symbol",
        "volume",
        "side",
        "type",
        "price(required when type=LIMIT)",
        "LIMIT volume follows spot_create_order logic: base-asset quantity",
        "isolated(optional, default=true; true=isolated,false=cross)",
        "newClientOrderId(optional)",
    ],
    "margin_get_order": [
        "symbol",
        "orderId or newClientOrderId",
        "isolated(optional, default=true; true=isolated,false=cross)",
    ],
    "margin_cancel_order": [
        "symbol",
        "orderId or newClientOrderId",
        "isolated(optional, default=true; true=isolated,false=cross)",
    ],
    "margin_open_orders": [
        "symbol(optional in some gateways)",
        "limit(optional, default=10, max=1000)",
        "isolated(optional, default=true; true=isolated,false=cross)",
    ],
    "margin_my_trades": [
        "symbol",
        "limit(optional, default=10, max=1000)",
        "fromId(optional)",
    ],
}

# (method, path, signed, params_location)
# params_location: "query" for GET querystring, "body" for JSON body, "none" for no params.
ACTIONS: Dict[str, Tuple[str, str, bool, str]] = {
    # public
    "spot_ping": ("GET", "/sapi/v2/ping", False, "query"),
    "spot_time": ("GET", "/sapi/v2/time", False, "query"),
    "spot_symbols": ("GET", "/sapi/v2/symbols", False, "query"),
    "spot_depth": ("GET", "/sapi/v2/depth", False, "query"),
    "spot_ticker": ("GET", "/sapi/v2/ticker", False, "query"),
    "spot_trades": ("GET", "/sapi/v2/trades", False, "query"),
    "spot_klines": ("GET", "/sapi/v2/klines", False, "query"),
    # spot signed trade
    "spot_create_order": ("POST", "/sapi/v2/order", True, "body"),
    "spot_test_order": ("POST", "/sapi/v2/order/test", True, "body"),
    "spot_batch_orders": ("POST", "/sapi/v2/batchOrders", True, "body"),
    "spot_get_order": ("GET", "/sapi/v2/order", True, "query"),
    "spot_cancel_order": ("POST", "/sapi/v2/cancel", True, "body"),
    "spot_batch_cancel": ("POST", "/sapi/v2/batchCancel", True, "body"),
    "spot_open_orders": ("GET", "/sapi/v2/openOrders", True, "query"),
    "spot_my_trades": ("GET", "/sapi/v2/myTrades", True, "query"),
    # account signed
    "spot_account": ("GET", "/sapi/v1/account", True, "query"),
    "asset_transfer": ("POST", "/sapi/v1/asset/transfer", True, "body"),
    "asset_transfer_query": ("POST", "/sapi/v1/asset/transferQuery", True, "body"),
    # margin signed
    "margin_create_order": ("POST", "/sapi/v2/margin/order", True, "body"),
    "margin_get_order": ("GET", "/sapi/v2/margin/order", True, "query"),
    "margin_cancel_order": ("POST", "/sapi/v2/margin/cancel", True, "body"),
    "margin_open_orders": ("GET", "/sapi/v2/margin/openOrders", True, "query"),
    "margin_my_trades": ("GET", "/sapi/v2/margin/myTrades", True, "query"),
}

MUTATING_ACTIONS = {
    "spot_create_order",
    "spot_test_order",
    "spot_batch_orders",
    "spot_cancel_order",
    "spot_batch_cancel",
    "asset_transfer",
    "asset_transfer_query",
    "margin_create_order",
    "margin_cancel_order",
}

ORDER_ACTIONS = {
    "spot_create_order",
    "spot_test_order",
    "margin_create_order",
}

LIMIT_DEFAULT_ACTIONS = {
    "spot_depth",
    "spot_klines",
    "margin_open_orders",
    "margin_my_trades",
}


@dataclass
class ChainUpConfig:
    base_url: str
    api_key: str
    secret_key: str
    timeout: int = DEFAULT_TIMEOUT


@dataclass
class SymbolRule:
    symbol: str
    display_symbol: str
    price_precision: int
    quantity_precision: int
    limit_price_min: Optional[str]
    limit_volume_min: Optional[str]


class ChainUpClient:
    def __init__(self, cfg: ChainUpConfig):
        self.cfg = cfg

    def _sign(self, ts_ms: str, method: str, request_path: str, body_str: Optional[str]) -> str:
        method_u = method.upper()
        if method_u == "GET":
            payload = f"{ts_ms}{method_u}{request_path}"
        else:
            payload = f"{ts_ms}{method_u}{request_path}{body_str if body_str is not None else '{}'}"
        digest = hmac.new(
            self.cfg.secret_key.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return digest

    @staticmethod
    def _json_dumps_compact(data: Dict[str, Any]) -> str:
        return json.dumps(data, separators=(",", ":"), ensure_ascii=False)

    def request(
        self,
        method: str,
        path: str,
        *,
        signed: bool,
        query: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        method_u = method.upper()
        query = query or {}

        query = {k: v for k, v in query.items() if v is not None}
        body = {k: v for k, v in (body or {}).items() if v is not None}

        query_str = urlencode(query, doseq=True)
        request_path = path + (f"?{query_str}" if query_str else "")
        url = urljoin(self.cfg.base_url.rstrip("/") + "/", request_path.lstrip("/"))

        payload_bytes = None
        body_str_for_sign = None
        if method_u != "GET":
            body_str_for_sign = self._json_dumps_compact(body) if body else "{}"
            payload_bytes = body_str_for_sign.encode("utf-8")

        headers = {
            "Content-Type": "application/json",
            "admin-language": "en_US",
            "User-Agent": USER_AGENT,
        }

        if signed:
            ts_ms = str(int(time.time() * 1000))
            headers["X-CH-APIKEY"] = self.cfg.api_key
            headers["X-CH-TS"] = ts_ms
            headers["X-CH-SIGN"] = self._sign(ts_ms, method_u, request_path, body_str_for_sign)

        req = Request(url=url, data=payload_bytes, method=method_u, headers=headers)

        try:
            with urlopen(req, timeout=self.cfg.timeout) as resp:
                raw = resp.read().decode("utf-8")
                return _parse_json_or_text(raw)
        except HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace") if exc.fp else exc.reason
            return {
                "httpStatus": exc.code,
                "error": _parse_json_or_text(raw),
            }
        except URLError as exc:
            return {"error": str(exc)}


def _parse_json_or_text(raw: str) -> Dict[str, Any]:
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            return parsed
        return {"data": parsed}
    except json.JSONDecodeError:
        return {"raw": raw}


def _is_positive_amount(value: Any) -> bool:
    try:
        return Decimal(str(value)) > 0
    except (InvalidOperation, TypeError, ValueError):
        return False


def _decimal_to_plain_string(value: Decimal) -> str:
    plain = format(value, "f")
    if "." in plain:
        plain = plain.rstrip("0").rstrip(".")
    return plain or "0"


def _quantize_down(value: Any, precision: int) -> str:
    decimal_value = Decimal(str(value))
    quant = Decimal("1").scaleb(-precision)
    adjusted = decimal_value.quantize(quant, rounding=ROUND_DOWN)
    return _decimal_to_plain_string(adjusted)


def _post_process_result(action: str, result: Dict[str, Any]) -> Dict[str, Any]:
    if action != "spot_account":
        return result

    balances = result.get("balances")
    if not isinstance(balances, list):
        return result

    filtered_balances = [
        balance
        for balance in balances
        if isinstance(balance, dict)
        and (
            _is_positive_amount(balance.get("free"))
            or _is_positive_amount(balance.get("locked"))
        )
    ]
    result["balances"] = filtered_balances
    return result


def _normalize_symbol_token(value: str) -> str:
    return value.strip().replace("/", "").replace("-", "").replace("_", "").lower()


def _display_symbol_for_humans(value: str) -> str:
    token = value.strip().upper().replace("-", "/").replace("_", "/")
    if "/" in token:
        return token
    return token


def _normalize_symbol_fields(data: Any) -> Any:
    if isinstance(data, dict):
        normalized: Dict[str, Any] = {}
        for key, value in data.items():
            normalized_value = _normalize_symbol_fields(value)
            key_lower = key.lower()
            if key_lower == "symbol" and isinstance(normalized_value, str):
                normalized_value = _normalize_symbol_token(normalized_value)
            elif key_lower == "symbols":
                if isinstance(normalized_value, str):
                    normalized_value = ",".join(
                        _normalize_symbol_token(item)
                        for item in normalized_value.split(",")
                        if item.strip()
                    )
                elif isinstance(normalized_value, list):
                    normalized_value = [
                        _normalize_symbol_token(item) if isinstance(item, str) else item
                        for item in normalized_value
                    ]
            normalized[key] = normalized_value
        return normalized
    if isinstance(data, list):
        return [_normalize_symbol_fields(item) for item in data]
    return data


def _strip_empty_timezone_fields(data: Any) -> Any:
    if isinstance(data, dict):
        cleaned: Dict[str, Any] = {}
        for key, value in data.items():
            cleaned_value = _strip_empty_timezone_fields(value)
            if key in {"timezone", "timeZone"}:
                if cleaned_value is None:
                    continue
                if isinstance(cleaned_value, str) and not cleaned_value.strip():
                    continue
            cleaned[key] = cleaned_value
        return cleaned
    if isinstance(data, list):
        return [_strip_empty_timezone_fields(item) for item in data]
    return data


def _apply_action_defaults(action: str, query: Dict[str, Any], body: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    if action in LIMIT_DEFAULT_ACTIONS and "limit" not in query:
        query["limit"] = 10
    return query, body


def _normalize_action_inputs(query: Dict[str, Any], body: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    normalized_query = _normalize_symbol_fields(query)
    normalized_body = _normalize_symbol_fields(body)
    return _strip_empty_timezone_fields(normalized_query), _strip_empty_timezone_fields(normalized_body)


def _load_json_arg(json_str: Optional[str], arg_name: str) -> Dict[str, Any]:
    if not json_str:
        return {}
    try:
        obj = json.loads(json_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{arg_name} must be valid JSON: {exc}") from exc
    if not isinstance(obj, dict):
        raise ValueError(f"{arg_name} must be a JSON object")
    return obj


def _load_tools_config(path: str = DEFAULT_TOOLS_FILE) -> Dict[str, str]:
    if not os.path.exists(path):
        return {}

    config: Dict[str, str] = {}
    with open(path, "r", encoding="utf-8") as fh:
        for raw_line in fh:
            line = raw_line.strip()
            if not line or ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip().upper()
            value = value.strip()
            if key in {"BASE_URL", "API_KEY", "SECRET_KEY"} and value:
                config[key] = value
    return config


def _load_symbol_rule(client: ChainUpClient, symbol: str) -> SymbolRule:
    normalized_symbol = _normalize_symbol_token(symbol)
    result = client.request("GET", "/sapi/v2/symbols", signed=False, query={}, body={})
    symbols = result.get("symbols")
    if not isinstance(symbols, list):
        raise ValueError("failed to load symbol metadata from spot_symbols")

    for item in symbols:
        if not isinstance(item, dict):
            continue
        item_symbol = item.get("symbol")
        if not isinstance(item_symbol, str):
            continue
        if _normalize_symbol_token(item_symbol) != normalized_symbol:
            continue
        return SymbolRule(
            symbol=item_symbol,
            display_symbol=item.get("SymbolName") or _display_symbol_for_humans(symbol),
            price_precision=int(item.get("pricePrecision", 0)),
            quantity_precision=int(item.get("quantityPrecision", 0)),
            limit_price_min=item.get("limitPriceMin"),
            limit_volume_min=item.get("limitVolumeMin"),
        )

    raise ValueError(f"symbol not found in spot_symbols: {symbol}")


def _prepare_order_body(action: str, body: Dict[str, Any], rule: SymbolRule) -> Dict[str, Any]:
    prepared = dict(body)
    adjustments: List[Dict[str, Any]] = []

    if action not in ORDER_ACTIONS:
        return {
            "preparedBody": prepared,
            "adjustments": adjustments,
            "symbolRule": {},
        }

    prepared["symbol"] = rule.display_symbol

    for field_name, precision in (("price", rule.price_precision), ("volume", rule.quantity_precision)):
        if field_name not in prepared:
            continue
        original = prepared[field_name]
        adjusted = _quantize_down(original, precision)
        if str(original) != adjusted:
            adjustments.append(
                {
                    "field": field_name,
                    "original": original,
                    "adjusted": adjusted,
                    "precision": precision,
                }
            )
        prepared[field_name] = adjusted

    if "volume" in prepared and _is_positive_amount(body.get("volume")) and not _is_positive_amount(prepared["volume"]):
        raise ValueError(
            f"volume becomes 0 after applying quantityPrecision={rule.quantity_precision}; increase order size"
        )
    if "price" in prepared and _is_positive_amount(body.get("price")) and not _is_positive_amount(prepared["price"]):
        raise ValueError(
            f"price becomes 0 after applying pricePrecision={rule.price_precision}; increase order price"
        )

    return {
        "preparedBody": prepared,
        "adjustments": adjustments,
        "symbolRule": {
            "symbol": rule.symbol,
            "displaySymbol": rule.display_symbol,
            "pricePrecision": rule.price_precision,
            "quantityPrecision": rule.quantity_precision,
            "limitPriceMin": rule.limit_price_min,
            "limitVolumeMin": rule.limit_volume_min,
        },
    }


def _build_config(args: argparse.Namespace) -> ChainUpConfig:
    tools_cfg = _load_tools_config()

    base_url = (
        args.base_url
        or tools_cfg.get("BASE_URL", "")
        or os.getenv("CHAINUP_BASE_URL", "")
    )
    api_key = (
        args.api_key
        or tools_cfg.get("API_KEY", "")
        or os.getenv("CHAINUP_API_KEY", "")
    )
    secret_key = (
        args.secret_key
        or tools_cfg.get("SECRET_KEY", "")
        or os.getenv("CHAINUP_SECRET_KEY", "")
    )

    if not base_url:
        raise ValueError("missing base_url: use --base-url or CHAINUP_BASE_URL")

    if args.signed_required:
        if not api_key:
            raise ValueError("missing api_key: use --api-key or CHAINUP_API_KEY")
        if not secret_key:
            raise ValueError("missing secret_key: use --secret-key or CHAINUP_SECRET_KEY")

    return ChainUpConfig(
        base_url=base_url,
        api_key=api_key,
        secret_key=secret_key,
        timeout=args.timeout,
    )


def _assert_confirm(args: argparse.Namespace) -> None:
    if not args.require_confirm:
        return
    if args.confirm != "CONFIRM":
        raise ValueError("mutating action blocked: pass --confirm CONFIRM to continue")


def main() -> int:
    parser = argparse.ArgumentParser(description="ChainUp OpenAPI V2 wrapper")
    parser.add_argument("action", choices=sorted(ACTIONS.keys()))
    parser.add_argument("--query-json", help="JSON object for query params")
    parser.add_argument("--body-json", help="JSON object for request body")
    parser.add_argument("--base-url", help="API base url, e.g. https://openapi.example.com")
    parser.add_argument("--api-key", help="API key (or CHAINUP_API_KEY)")
    parser.add_argument("--secret-key", help="Secret key (or CHAINUP_SECRET_KEY)")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument(
        "--confirm",
        default="",
        help="For mutating requests, must be exactly CONFIRM when required",
    )
    parser.add_argument(
        "--no-confirm-gate",
        action="store_true",
        help="Disable CONFIRM gate for mutating requests",
    )
    parser.add_argument(
        "--show-todo",
        action="store_true",
        help="Show placeholder required fields for this action",
    )
    parser.add_argument(
        "--prepare-only",
        action="store_true",
        help="For order actions, fetch symbol precision and return prepared params without sending the order",
    )

    args = parser.parse_args()

    method, path, signed, params_location = ACTIONS[args.action]
    args.signed_required = signed and (not args.prepare_only)
    args.require_confirm = (args.action in MUTATING_ACTIONS) and (not args.no_confirm_gate)

    try:
        query = _load_json_arg(args.query_json, "--query-json")
        body = _load_json_arg(args.body_json, "--body-json")
        query, body = _normalize_action_inputs(query, body)
        query, body = _apply_action_defaults(args.action, query, body)
        cfg = _build_config(args)
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2

    if args.show_todo:
        print(
            json.dumps(
                {
                    "action": args.action,
                    "todoRequiredFields": TODO_REQUIRED_FIELDS.get(args.action, []),
                    "note": "Placeholder list; refine after validating exchange-side schema.",
                },
                ensure_ascii=False,
            )
        )

    client = ChainUpClient(cfg)

    if args.action in ORDER_ACTIONS:
        try:
            symbol_value = body.get("symbol")
            if not isinstance(symbol_value, str) or not symbol_value.strip():
                raise ValueError("order action requires symbol in --body-json")
            original_body = dict(body)
            prepared = _prepare_order_body(
                args.action,
                body,
                _load_symbol_rule(client, symbol_value),
            )
            body = prepared["preparedBody"]
        except ValueError as exc:
            print(json.dumps({"error": str(exc)}, ensure_ascii=False))
            return 2

        if args.prepare_only:
            print(
                json.dumps(
                    {
                        "action": args.action,
                        "originalBody": original_body,
                        **prepared,
                        "readyForConfirm": True,
                    },
                    ensure_ascii=False,
                )
            )
            return 0

    try:
        _assert_confirm(args)
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2

    req_query: Dict[str, Any] = query if params_location == "query" else {}
    req_body: Dict[str, Any] = body if params_location == "body" else {}

    result = client.request(
        method,
        path,
        signed=signed,
        query=req_query,
        body=req_body,
    )
    result = _post_process_result(args.action, result)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
