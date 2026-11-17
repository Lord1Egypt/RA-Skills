#!/usr/bin/env python3
"""Compute GDT-to-warehouse landed cost (入仓价) per the user's formulas.

Formulas (contract 2 = main contract, delivery 1-2 months out):

    AMF:  (contract2_price + 165) * FX * 1.13 + 300
    WMP:  (contract2_price + 115) * FX * 1.13 + 300
    SMP:  (contract2_price + 115) * FX * 1.13 + 300

Args:
    --contract2-amf <USD/t>     contract-2 AMF auction price
    --contract2-wmp <USD/t>     contract-2 WMP auction price
    --contract2-smp <USD/t>     contract-2 SMP auction price
    --fx <CNY/USD>              CNY per USD midpoint
    --out <csv>                 optional CSV output path
    --markdown                  also print a markdown table to stdout

If a price argument is omitted, that product is skipped (marked N/A).
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass


FREIGHT_USD_PER_T = {"AMF": 165.0, "WMP": 115.0, "SMP": 115.0}
DUTY_VAT_MULT = 1.13
IMPORT_MISC_CNY_PER_T = 300.0


@dataclass
class LandedRow:
    product: str
    contract2_usd_per_t: float | None
    freight_usd_per_t: float
    fx_cny_per_usd: float
    landed_cny_per_t: float | None

    def to_dict(self) -> dict:
        return {
            "product": self.product,
            "contract2_usd_per_t": (
                "" if self.contract2_usd_per_t is None else self.contract2_usd_per_t
            ),
            "freight_usd_per_t": self.freight_usd_per_t,
            "fx_cny_per_usd": self.fx_cny_per_usd,
            "landed_cny_per_t": (
                "" if self.landed_cny_per_t is None else self.landed_cny_per_t
            ),
        }


def compute(
    contract2_amf: float | None,
    contract2_wmp: float | None,
    contract2_smp: float | None,
    fx: float,
) -> list[LandedRow]:
    rows: list[LandedRow] = []
    for product, c2 in (
        ("AMF", contract2_amf),
        ("WMP", contract2_wmp),
        ("SMP", contract2_smp),
    ):
        if c2 is None:
            rows.append(LandedRow(product, None, FREIGHT_USD_PER_T[product], fx, None))
            continue
        landed = (c2 + FREIGHT_USD_PER_T[product]) * fx * DUTY_VAT_MULT + IMPORT_MISC_CNY_PER_T
        rows.append(LandedRow(product, c2, FREIGHT_USD_PER_T[product], fx, landed))
    return rows


def render_markdown(rows: list[LandedRow], fx: float) -> str:
    head = (
        f"汇率: 1 USD = {fx:.4f} CNY (央行中间价月均); 关税+增值税复合 1.13; "
        f"进口杂费 300 元/吨\n\n"
    )
    table = (
        "| 产品 | 合约 2 (USD/吨) | 海运 (USD/吨) | 入仓成本 (CNY/吨) |\n"
        "|---|---|---|---|\n"
    )
    for r in rows:
        c2 = "数据待补充" if r.contract2_usd_per_t is None else f"{r.contract2_usd_per_t:,.0f}"
        landed = "数据待补充" if r.landed_cny_per_t is None else f"{r.landed_cny_per_t:,.0f}"
        table += f"| {r.product} | {c2} | {r.freight_usd_per_t:.0f} | {landed} |\n"
    return head + table


def main() -> int:
    p = argparse.ArgumentParser(description="GDT → 入仓成本计算")
    p.add_argument("--contract2-amf", type=float, default=None)
    p.add_argument("--contract2-wmp", type=float, default=None)
    p.add_argument("--contract2-smp", type=float, default=None)
    p.add_argument("--fx", type=float, required=True, help="CNY per USD midpoint")
    p.add_argument("--out", type=str, default=None, help="optional CSV output path")
    p.add_argument(
        "--markdown",
        action="store_true",
        help="print markdown table to stdout (in addition to JSON)",
    )
    args = p.parse_args()

    rows = compute(
        args.contract2_amf,
        args.contract2_wmp,
        args.contract2_smp,
        args.fx,
    )

    if args.out:
        with open(args.out, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "product",
                    "contract2_usd_per_t",
                    "freight_usd_per_t",
                    "fx_cny_per_usd",
                    "landed_cny_per_t",
                ],
            )
            writer.writeheader()
            for r in rows:
                writer.writerow(r.to_dict())

    if args.markdown or not args.out:
        print(render_markdown(rows, args.fx))
    else:
        # JSON to stdout for machine consumption
        print(json.dumps([r.to_dict() for r in rows], ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
