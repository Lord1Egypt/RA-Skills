# -*- coding: utf-8 -*-
"""因子实验台账入口。

只提供实验查询与人工 verdict 写入。因子挖掘的确定性摘要由
factor_backtest.py 自动登记；脚本不判断结论、不修改生产阈值。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import factor_experiment as fx  # noqa: E402


def _print_json(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def cmd_experiments(args: argparse.Namespace) -> int:
    if args.set_verdict:
        result = fx.set_verdict(args.set_verdict, args.verdict, args.note)
        print("[set-verdict] 已更新 verdict 与 verdict_note：")
        _print_json(result)
        return 0

    rows = fx.list_experiments(recent=args.recent)
    if not rows:
        print("（实验台账为空——先跑一次 factor_backtest.py 挖矿）")
        return 0
    print(f"最近 {len(rows)} 条挖矿实验（脚本只列事实，采不采纳由人判）：\n")
    for row in rows:
        verdict = row["verdict"] or "未判"
        print(
            f"  {row['group_key']}@{row['window_end']}  spec={row['spec_hash'][:8]}  "
            f"命中{row['n_signals']}/{row['n_unique_stocks']}只  "
            f"过闸 单{row['n_singles_passed']}/配{row['n_pairs_passed']}  [{verdict}]"
        )
        if row["verdict_note"]:
            print(f"        note: {row['verdict_note']}")
    print(
        "\n判分：factor_lab.py experiments --set-verdict <group>@<window>@<hash前缀> "
        "--verdict adopted|rejected|observing [--note ...]"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="因子挖掘实验台账")
    sub = parser.add_subparsers(dest="cmd", required=True)
    experiments = sub.add_parser("experiments", help="查最近挖矿实验 / 人工判分")
    experiments.add_argument("--recent", type=int, default=20, help="列最近 N 条")
    experiments.add_argument(
        "--set-verdict",
        default=None,
        metavar="SEL",
        help="<group_key>@<window_end>@<spec_hash前缀> 判分该实验",
    )
    experiments.add_argument(
        "--verdict",
        default=None,
        choices=list(fx.VERDICT_ENUM),
        help="adopted / rejected / observing（留空=清空判定）",
    )
    experiments.add_argument("--note", default=None, help="判分理由")
    experiments.set_defaults(func=cmd_experiments)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
