#!/usr/bin/env python3
"""Minimal Polymarket Trading Client.

Core trading features:
- initialize with private key (loaded from private.env / env)
- market buy / sell
- limit order buy / sell
- get open orders / get single order
- cancel single / cancel all
"""

import argparse
import json
import os
import sys
from pathlib import Path

from eth_account import Account
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import (
    AssetType,
    BalanceAllowanceParams,
    MarketOrderArgs,
    OpenOrderParams,
    OrderArgs,
    OrderType,
)
from py_clob_client.order_builder.constants import BUY, SELL

CLOB_HOST = "https://clob.polymarket.com"
CHAIN_ID = 137


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ[key.strip()] = value.strip().strip('"').strip("'")


def getenv_required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required env var: {name}")
    return value


class SimplePolymarketTrader:
    def __init__(self, private_key: str):
        self.private_key = private_key
        self.wallet = Account.from_key(private_key)
        self.host = os.getenv("POLYMARKET_CLOB_HOST", CLOB_HOST)
        self.chain_id = int(os.getenv("POLYMARKET_CHAIN_ID", str(CHAIN_ID)))
        self.signature_type = int(os.getenv("POLYMARKET_SIGNATURE_TYPE", "0"))
        self.funder = os.getenv("POLYMARKET_FUNDER") or None

        client_kwargs = {
            "host": self.host,
            "chain_id": self.chain_id,
            "key": private_key,
            "signature_type": self.signature_type,
        }
        if self.funder:
            client_kwargs["funder"] = self.funder

        self.client = ClobClient(**client_kwargs)
        self.creds = None

    # ------------------------------------------------
    # Initialize API key (签名授权)
    # ------------------------------------------------
    def initialize(self):
        self.creds = self.client.create_or_derive_api_creds()
        client_kwargs = {
            "host": self.host,
            "chain_id": self.chain_id,
            "key": self.private_key,
            "creds": self.creds,
            "signature_type": self.signature_type,
        }
        if self.funder:
            client_kwargs["funder"] = self.funder
        self.client = ClobClient(**client_kwargs)

    def _allowance_values(self, allowance_resp: dict) -> list[int]:
        allowances = (allowance_resp or {}).get("allowances", {})
        vals = []
        for v in allowances.values():
            try:
                vals.append(int(v))
            except Exception:
                pass
        return vals

    def _ensure_allowance(self, asset_type: AssetType, token_id: str | None = None):
        params = BalanceAllowanceParams(
            asset_type=asset_type,
            token_id=token_id,
            signature_type=self.signature_type,
        )
        current = self.client.get_balance_allowance(params)
        values = self._allowance_values(current)
        if values and max(values) > 0:
            return current
        # 自动授权
        self.client.update_balance_allowance(params)
        return self.client.get_balance_allowance(params)

    # ------------------------------------------------
    # Market Order
    # ------------------------------------------------
    def market_buy(self, token_id: str, amount: float):
        self._ensure_allowance(AssetType.COLLATERAL)
        order = self.client.create_market_order(
            MarketOrderArgs(token_id=token_id, side=BUY, amount=amount),
        )
        return self.client.post_order(order, OrderType.FOK)

    def market_sell(self, token_id: str, amount: float):
        self._ensure_allowance(AssetType.CONDITIONAL, token_id=token_id)
        order = self.client.create_market_order(
            MarketOrderArgs(token_id=token_id, side=SELL, amount=amount),
        )
        return self.client.post_order(order, OrderType.FOK)

    # ------------------------------------------------
    # Limit Order
    # ------------------------------------------------
    def limit_buy(self, token_id: str, price: float, size: float):
        self._ensure_allowance(AssetType.COLLATERAL)
        return self.client.create_and_post_order(
            OrderArgs(token_id=token_id, side=BUY, price=price, size=size),
        )

    def limit_sell(self, token_id: str, price: float, size: float):
        self._ensure_allowance(AssetType.CONDITIONAL, token_id=token_id)
        return self.client.create_and_post_order(
            OrderArgs(token_id=token_id, side=SELL, price=price, size=size),
        )

    # ------------------------------------------------
    # Orders
    # ------------------------------------------------
    def get_open_orders(self):
        return self.client.get_orders(OpenOrderParams())

    def get_order(self, order_id: str):
        return self.client.get_order(order_id)

    # ------------------------------------------------
    # Cancel
    # ------------------------------------------------
    def cancel_order(self, order_id: str):
        return self.client.cancel_orders([order_id])

    def cancel_all(self):
        return self.client.cancel_market_orders(None)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Minimal Polymarket trading client")
    default_env = Path(__file__).resolve().parents[1] / "private.env"
    parser.add_argument("--env-file", default=str(default_env), help="Env file path")

    sub = parser.add_subparsers(dest="command", required=True)

    mb = sub.add_parser("market-buy")
    mb.add_argument("--token-id", required=True)
    mb.add_argument("--amount", type=float, required=True)

    ms = sub.add_parser("market-sell")
    ms.add_argument("--token-id", required=True)
    ms.add_argument("--amount", type=float, required=True)

    lb = sub.add_parser("limit-buy")
    lb.add_argument("--token-id", required=True)
    lb.add_argument("--price", type=float, required=True)
    lb.add_argument("--size", type=float, required=True)

    ls = sub.add_parser("limit-sell")
    ls.add_argument("--token-id", required=True)
    ls.add_argument("--price", type=float, required=True)
    ls.add_argument("--size", type=float, required=True)

    sub.add_parser("open-orders")

    go = sub.add_parser("get-order")
    go.add_argument("--order-id", required=True)

    co = sub.add_parser("cancel-order")
    co.add_argument("--order-id", required=True)

    sub.add_parser("cancel-all")

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    load_env_file(Path(args.env_file))

    private_key = getenv_required("POLYMARKET_PRIVATE_KEY")
    trader = SimplePolymarketTrader(private_key)
    trader.initialize()

    if args.command == "market-buy":
        result = trader.market_buy(args.token_id, args.amount)
    elif args.command == "market-sell":
        result = trader.market_sell(args.token_id, args.amount)
    elif args.command == "limit-buy":
        result = trader.limit_buy(args.token_id, args.price, args.size)
    elif args.command == "limit-sell":
        result = trader.limit_sell(args.token_id, args.price, args.size)
    elif args.command == "open-orders":
        result = trader.get_open_orders()
    elif args.command == "get-order":
        result = trader.get_order(args.order_id)
    elif args.command == "cancel-order":
        result = trader.cancel_order(args.order_id)
    elif args.command == "cancel-all":
        result = trader.cancel_all()
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
