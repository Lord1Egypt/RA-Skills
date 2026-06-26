#!/usr/bin/env python3
import argparse
import os
import re
import time
from decimal import Decimal
from datetime import datetime


def need(name: str) -> str:
    v = os.getenv(name, "").strip()
    if not v:
        raise ValueError(f"Missing env: {name}")
    return v


def log(msg: str):
    print(f"[{datetime.utcnow().isoformat()}Z] {msg}")


def parse_decimal(name: str, default: str = None) -> Decimal:
    raw = os.getenv(name, default if default is not None else "")
    if raw is None or raw == "":
        raise ValueError(f"Missing numeric env: {name}")
    return Decimal(str(raw))


def validate_pk(pk: str):
    if not re.fullmatch(r"0x[a-fA-F0-9]{64}", pk):
        raise ValueError("EVM_PRIVATE_KEY must be 0x + 64 hex chars")


def mock_get_price(token_in: str, token_out: str) -> Decimal:
    # TODO: replace with real quote source (e.g. 0x/1inch/Pancake quote API)
    # keep deterministic fallback for testing
    base = Decimal("1.0")
    return base


def mock_swap(side: str, amount_bnb: Decimal, dry_run: bool):
    if dry_run:
        log(f"[DRY-RUN] swap {side} {amount_bnb} BNB")
        return
    # TODO: implement real tx signing + router call with web3.py
    log(f"[LIVE-PLACEHOLDER] swap {side} {amount_bnb} BNB")


def run(dry_run: bool):
    pk = need("EVM_PRIVATE_KEY")
    validate_pk(pk)
    need("BNB_RPC_URL")
    token_in = os.getenv("TOKEN_IN", "WBNB")
    token_out = need("TOKEN_OUT")

    buy_trigger = parse_decimal("BUY_TRIGGER_PRICE")
    size_bnb = parse_decimal("BUY_SIZE_BNB")
    tp = parse_decimal("TAKE_PROFIT_PCT", "0.05")
    sl = parse_decimal("STOP_LOSS_PCT", "0.03")
    poll = int(os.getenv("POLL_SECONDS", "10"))

    in_position = False
    entry = Decimal("0")

    log(f"Start bot token={token_out} trigger={buy_trigger} size={size_bnb} tp={tp} sl={sl} dry={dry_run}")

    while True:
        price = mock_get_price(token_in, token_out)
        log(f"price={price}")

        if not in_position:
            if price >= buy_trigger:
                mock_swap("BUY", size_bnb, dry_run)
                entry = price
                in_position = True
                log(f"entered at {entry}")
        else:
            tp_price = entry * (Decimal("1") + tp)
            sl_price = entry * (Decimal("1") - sl)
            if price >= tp_price:
                mock_swap("SELL_TP", size_bnb, dry_run)
                log(f"take profit hit: {price} >= {tp_price}")
                break
            if price <= sl_price:
                mock_swap("SELL_SL", size_bnb, dry_run)
                log(f"stop loss hit: {price} <= {sl_price}")
                break

        time.sleep(poll)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["dry-run", "run"], default="dry-run")
    args = ap.parse_args()
    run(dry_run=(args.mode == "dry-run"))
