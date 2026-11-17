#!/usr/bin/env python3
"""Estimate the fair value of HK 07709 from KRX 000660 and Nasdaq SKHY."""

from __future__ import annotations

import argparse
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Optional


ZERO = Decimal("0")
ONE = Decimal("1")
HUNDRED = Decimal("100")


def positive_decimal(raw: str) -> Decimal:
    """Parse a strictly positive decimal for argparse."""
    try:
        value = Decimal(raw)
    except InvalidOperation as exc:
        raise argparse.ArgumentTypeError(f"invalid decimal: {raw}") from exc
    if not value.is_finite() or value <= ZERO:
        raise argparse.ArgumentTypeError(f"value must be finite and > 0: {raw}")
    return value


def decimal_value(raw: str) -> Decimal:
    """Parse any finite decimal for argparse."""
    try:
        value = Decimal(raw)
    except InvalidOperation as exc:
        raise argparse.ArgumentTypeError(f"invalid decimal: {raw}") from exc
    if not value.is_finite():
        raise argparse.ArgumentTypeError(f"value must be finite: {raw}")
    return value


def pct_change(current: Decimal, previous: Decimal) -> Decimal:
    return current / previous - ONE


def leveraged_fair(
    nav: Decimal,
    underlying_return: Decimal,
    leverage: Decimal,
    tracking_adjustment_pct: Decimal,
    hkd_fx_factor: Decimal,
) -> Decimal:
    multiplier = ONE + leverage * underlying_return + tracking_adjustment_pct / HUNDRED
    return max(ZERO, nav * multiplier * hkd_fx_factor)


def money(value: Decimal) -> str:
    return f"{value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):,.2f}"


def percent(value: Decimal) -> str:
    rendered = (value * HUNDRED).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"{rendered:+,.2f}%"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Estimate HK 07709 NAV fair value and carried-discount price."
    )
    parser.add_argument("--nav-hkd", type=positive_decimal, required=True)
    parser.add_argument("--product-prev-market", type=positive_decimal)
    parser.add_argument("--kr-prev-close", type=positive_decimal, required=True)
    parser.add_argument("--kr-open", type=positive_decimal)
    parser.add_argument("--kr-current", type=positive_decimal)
    parser.add_argument("--adr-prev-close", type=positive_decimal)
    parser.add_argument("--adr-close", type=positive_decimal)
    parser.add_argument("--usdkrw", type=positive_decimal)
    parser.add_argument("--ads-per-common", type=positive_decimal, default=Decimal("10"))
    parser.add_argument("--leverage", type=positive_decimal, default=Decimal("2"))
    parser.add_argument(
        "--tracking-adjustment-pct",
        type=decimal_value,
        default=ZERO,
        help="Percentage-point adjustment to the daily product return; default 0.",
    )
    parser.add_argument(
        "--hkd-fx-factor",
        type=positive_decimal,
        default=ONE,
        help="Current USD/HKD divided by prior NAV USD/HKD conversion rate; default 1.",
    )
    parser.add_argument(
        "--adr-premium-threshold-pct",
        type=positive_decimal,
        default=Decimal("5"),
    )
    return parser


def add_anchor_rows(
    rows: list[tuple[str, str, str, str]],
    name: str,
    price: Optional[Decimal],
    args: argparse.Namespace,
    carried_discount: Optional[Decimal],
) -> Optional[Decimal]:
    if price is None:
        return None
    underlying_return = pct_change(price, args.kr_prev_close)
    fair = leveraged_fair(
        args.nav_hkd,
        underlying_return,
        args.leverage,
        args.tracking_adjustment_pct,
        args.hkd_fx_factor,
    )
    carried = fair * (ONE + carried_discount) if carried_discount is not None else None
    rows.append(
        (
            name,
            money(price),
            percent(underlying_return),
            f"HK${money(fair)}"
            + (f"；折价延续 HK${money(carried)}" if carried is not None else ""),
        )
    )
    return underlying_return


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if (args.adr_prev_close is None) != (args.adr_close is None):
        parser.error("--adr-prev-close and --adr-close must be supplied together")
    if args.usdkrw is not None and args.adr_close is None:
        parser.error("--usdkrw requires --adr-close")
    if args.product_prev_market is not None and args.product_prev_market <= ZERO:
        parser.error("--product-prev-market must be > 0")

    carried_discount = None
    if args.product_prev_market is not None:
        carried_discount = pct_change(args.product_prev_market, args.nav_hkd)

    rows: list[tuple[str, str, str, str]] = []
    kr_open_return = add_anchor_rows(
        rows, "KRX开盘", args.kr_open, args, carried_discount
    )
    kr_current_return = add_anchor_rows(
        rows, "KRX最新", args.kr_current, args, carried_discount
    )

    warnings: list[str] = []
    if carried_discount is not None and abs(carried_discount) > Decimal("0.05"):
        warnings.append(
            f"07709昨日市场价相对NAV为{percent(carried_discount)}，交易价不能等同NAV。"
        )

    adr_return = None
    if args.adr_close is not None and args.adr_prev_close is not None:
        adr_return = pct_change(args.adr_close, args.adr_prev_close)
        adr_fair = leveraged_fair(
            args.nav_hkd,
            adr_return,
            args.leverage,
            args.tracking_adjustment_pct,
            args.hkd_fx_factor,
        )
        rows.append(("SKHY隔夜", money(args.adr_close), percent(adr_return), f"HK${money(adr_fair)}"))

    if args.usdkrw is not None and args.adr_close is not None:
        kr_anchor = args.kr_current or args.kr_open or args.kr_prev_close
        implied_krw = args.adr_close * args.ads_per_common * args.usdkrw
        adr_premium = pct_change(implied_krw, kr_anchor)
        threshold = args.adr_premium_threshold_pct / HUNDRED
        print(f"ADR隐含每股：KRW {money(implied_krw)}")
        print(f"ADR相对韩股锚点溢价：{percent(adr_premium)}")
        if abs(adr_premium) > threshold:
            warnings.append(
                "ADR绝对价格偏离韩股超过阈值；SKHY只能作为隔夜方向信号，不能作为平价锚。"
            )

    comparison_return = kr_current_return or kr_open_return
    if adr_return is not None and comparison_return is not None:
        if abs(adr_return - comparison_return) > Decimal("0.05"):
            warnings.append("SKHY与KRX涨幅相差超过5个百分点；以已开市的KRX为主。")

    if comparison_return is not None and abs(comparison_return) > Decimal("0.20"):
        warnings.append("KRX波动超过20%；开盘价、最新价和港股开盘前最后报价应分别复算。")

    print()
    print("| 锚点 | 锚点价格 | 标的涨跌 | 07709估值 |")
    print("|---|---:|---:|---:|")
    for name, price, change, estimate in rows:
        print(f"| {name} | {price} | {change} | {estimate} |")

    if carried_discount is not None:
        print(f"\n07709昨日折溢价：{percent(carried_discount)}")
    if args.tracking_adjustment_pct != ZERO:
        print(f"跟踪调整：{args.tracking_adjustment_pct:+.2f}个百分点")

    if warnings:
        print("\n风险提示：")
        for item in warnings:
            print(f"- {item}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        sys.stderr.close()
        raise SystemExit(1)

