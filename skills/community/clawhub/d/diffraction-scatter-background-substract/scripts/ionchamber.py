#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ionchamber.py — 电离室数据分析工具
Ionchamber data analysis utility.

支持两种模式：
1. 单文件统计
2. 样品/背景双文件透过率计算

Supports two modes:
1. Single-file statistics
2. Sample/background transmission calculation
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.common import calc_ion_intensity, load_ionchamber_table  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="电离室分析 / Ionchamber analysis")
    parser.add_argument("ionchamber", help="样品电离室文件 / Sample ionchamber file")
    parser.add_argument("--background-ion", help="背景电离室文件 / Background ionchamber file")
    parser.add_argument(
        "-c",
        "--channel",
        choices=["Ionchamber0", "Ionchamber1", "Ionchamber2", "all"],
        default="Ionchamber2",
    )
    parser.add_argument("--method", choices=["mean", "median", "trimmed_mean"], default="median")
    parser.add_argument(
        "--background-channel",
        choices=["Ionchamber0", "Ionchamber1", "Ionchamber2"],
        default="Ionchamber1",
    )
    parser.add_argument(
        "--sample-channel",
        choices=["Ionchamber0", "Ionchamber1", "Ionchamber2"],
        default="Ionchamber1",
    )
    parser.add_argument(
        "--background-method", choices=["mean", "median", "trimmed_mean"], default="median"
    )
    parser.add_argument(
        "--sample-method", choices=["mean", "median", "trimmed_mean"], default="median"
    )
    return parser.parse_args()


def print_stats(name: str, values: np.ndarray) -> None:
    print(f"\n{name} 统计 / Statistics:")
    print(f"  mean   = {np.mean(values):.6e}")
    print(f"  median = {np.median(values):.6e}")
    print(f"  std    = {np.std(values):.6e}")
    print(f"  min    = {np.min(values):.6e}")
    print(f"  max    = {np.max(values):.6e}")


def main() -> int:
    args = parse_args()
    try:
        data = load_ionchamber_table(args.ionchamber)
        if data is None:
            raise RuntimeError("电离室文件中没有有效数据 / No valid ionchamber data found")

        print(f"文件 / File: {args.ionchamber}")
        print(f"数据行数 / Rows: {len(data)}")

        if args.channel == "all":
            for name in ["Ionchamber0", "Ionchamber1", "Ionchamber2"]:
                print_stats(name, data[name].to_numpy(dtype=float))
        else:
            print_stats(args.channel, data[args.channel].to_numpy(dtype=float))

        summary_channel = args.channel if args.channel != "all" else args.sample_channel
        summary_intensity = calc_ion_intensity(
            data, summary_channel, args.method if args.channel != "all" else args.sample_method
        )
        if summary_intensity is not None:
            print(
                f"\n摘要强度 / Summary intensity ({summary_channel}, {args.method}): {summary_intensity:.6e}"
            )

        if args.background_ion:
            background_data = load_ionchamber_table(args.background_ion)
            if background_data is None:
                raise RuntimeError(
                    "背景电离室文件中没有有效数据 / No valid background ionchamber data found"
                )

            sample_intensity = calc_ion_intensity(data, args.sample_channel, args.sample_method)
            background_intensity = calc_ion_intensity(
                background_data,
                args.background_channel,
                args.background_method,
            )
            if sample_intensity is None or background_intensity in (None, 0):
                raise RuntimeError("透过率计算失败 / Failed to calculate transmission")
            transmission = sample_intensity / background_intensity * 100.0
            print(f"\n样品/背景透过率 / Sample-vs-background transmission: {transmission:.4f}%")
            print(
                f"公式 / Formula: T = {args.sample_channel}_{args.sample_method}(sample) / {args.background_channel}_{args.background_method}(background) × 100%"
            )
        return 0
    except Exception as exc:
        print(f"处理失败: {exc} / Processing failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
