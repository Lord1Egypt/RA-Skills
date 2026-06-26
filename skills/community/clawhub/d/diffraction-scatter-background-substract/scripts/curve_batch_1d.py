#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
curve_batch_1d.py — 1D曲线批量处理脚本
Batch 1D curve processing script.

支持三种 transmission 来源：
1. 统一手动 T
2. 分别设置 T（CSV/JSON 映射）
3. 电离室自动计算 T

Supports three transmission sources:
1. Unified manual T
2. Per-file T (CSV/JSON mapping)
3. Ionchamber-derived T
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.curve_data import ProcessMode  # noqa: E402
from lib.curve_processor import CurveProcessorConfig  # noqa: E402
from lib.task_pipeline import PipelineContext, PipelineEngine, TaskItem  # noqa: E402
from lib.curve_io import inspect_curve_layout, save_curve_collection  # noqa: E402
from lib.common import build_transmission_map  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="批量处理 1D 曲线：算法背景估计或参考背景 T 修正扣除 / Batch-process 1D curves with algorithmic estimation or T-corrected reference subtraction."
    )
    parser.add_argument("input_dir", help="输入目录 / Input directory")
    parser.add_argument("--background", help="参考背景曲线 / Reference background curve")
    parser.add_argument("--method", choices=["morph", "poly", "rolling_ball"], default="morph")
    parser.add_argument("--radius", type=int, default=50)
    parser.add_argument("--iterations", type=int, default=1)
    parser.add_argument("--degree", type=int, default=4)
    parser.add_argument("--quantile", type=float, default=0.3)
    parser.add_argument("--pattern", default="*.xy")
    parser.add_argument(
        "--parse-mode",
        choices=["single", "xyxy", "xyyy"],
        default="single",
        help="列结构 / Column layout",
    )
    parser.add_argument("--skip-header", type=int, default=0)
    parser.add_argument(
        "--delimiter",
        choices=["auto", "comma", "tab", "space"],
        default="auto",
    )
    parser.add_argument("-o", "--output-dir", default="./output")
    parser.add_argument("--format", choices=["xy", "csv", "txt", "gr", "npy", "h5"], default="xy")
    parser.add_argument(
        "--output-mode",
        choices=["per-file", "merged"],
        default="per-file",
        help="输出模式 / Output mode",
    )
    parser.add_argument(
        "--merged-output",
        default="merged_curves.h5",
        help="合并输出文件名 / Merged output filename",
    )
    parser.add_argument("--save-bg", action="store_true")
    parser.add_argument("--save-sub", action="store_true", default=True)
    parser.add_argument(
        "-t",
        "--transmission",
        type=float,
        help="统一透过率(%%) / Unified transmission percent",
    )
    parser.add_argument(
        "--transmission-map",
        help="分别设置透过率映射文件(CSV/JSON) / Per-file transmission map CSV/JSON",
    )
    parser.add_argument("--ion-dir", help="电离室目录 / Ionchamber directory")
    parser.add_argument(
        "--sample-channel",
        default="Ionchamber1",
        choices=["Ionchamber0", "Ionchamber1", "Ionchamber2"],
    )
    parser.add_argument(
        "--background-channel",
        default="Ionchamber1",
        choices=["Ionchamber0", "Ionchamber1", "Ionchamber2"],
    )
    parser.add_argument(
        "--sample-method", default="median", choices=["mean", "median", "trimmed_mean"]
    )
    parser.add_argument(
        "--background-method", default="median", choices=["mean", "median", "trimmed_mean"]
    )
    parser.add_argument("--match-regex", default="")
    return parser


def _iter_curve_files(input_dir: Path, pattern: str) -> List[str]:
    return [str(path) for path in sorted(input_dir.glob(pattern)) if path.is_file()]


def _build_config(args: argparse.Namespace) -> CurveProcessorConfig:
    if args.background:
        return CurveProcessorConfig(
            process_mode=ProcessMode.T_BG_SUBTRACT, transmission=args.transmission or 100.0
        )
    if args.method == "morph":
        return CurveProcessorConfig(
            process_mode=ProcessMode.MORPH_1D,
            bg_method_1d="morph",
            morph_radius=args.radius,
            morph_iterations=args.iterations,
        )
    if args.method == "poly":
        return CurveProcessorConfig(
            process_mode=ProcessMode.FIT_1D,
            bg_method_1d="poly",
            poly_degree=args.degree,
            poly_quantile=args.quantile,
        )
    return CurveProcessorConfig(
        process_mode=ProcessMode.MORPH_1D,
        bg_method_1d="rolling_ball",
        rolling_ball_radius=float(args.radius),
    )


def _load_transmission_map(path: str, sample_paths: List[str]) -> Dict[str, float]:
    transmission_by_name: Dict[str, float] = {}
    file_path = Path(path)
    if file_path.suffix.lower() == ".json":
        data = json.loads(file_path.read_text(encoding="utf-8"))
        transmission_by_name = {str(key): float(value) for key, value in data.items()}
    else:
        with open(file_path, "r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                name = row.get("file") or row.get("filename") or row.get("path")
                value = row.get("transmission") or row.get("transmission_percent")
                if name and value:
                    transmission_by_name[str(name)] = float(value)

    resolved: Dict[str, float] = {}
    missing: List[str] = []
    for sample_path in sample_paths:
        basename = Path(sample_path).name
        if sample_path in transmission_by_name:
            resolved[sample_path] = transmission_by_name[sample_path]
        elif basename in transmission_by_name:
            resolved[sample_path] = transmission_by_name[basename]
        else:
            missing.append(basename)
    if missing:
        raise RuntimeError(
            f"透过率映射缺少条目 / Missing transmission entries: {', '.join(missing)}"
        )
    return resolved


def _collect_ion_paths(ion_dir: Optional[str]) -> List[str]:
    if not ion_dir:
        return []
    base = Path(ion_dir)
    if not base.is_dir():
        raise RuntimeError(f"电离室目录不存在 / Ionchamber directory not found: {ion_dir}")
    return [
        str(path)
        for path in sorted(base.rglob("*"))
        if path.is_file() and path.suffix.lower() in {".ionchamber", ".txt"}
    ]


def _resolve_transmissions(
    args: argparse.Namespace, sample_paths: List[str]
) -> Tuple[Optional[float], Optional[Dict[str, float]]]:
    if not args.background:
        return None, None
    if args.transmission_map:
        return None, _load_transmission_map(args.transmission_map, sample_paths)
    if args.ion_dir:
        ion_paths = _collect_ion_paths(args.ion_dir)
        transmissions, match_results, background_result = build_transmission_map(
            sample_paths=sample_paths,
            background_path=args.background,
            ion_paths=ion_paths,
            background_channel=args.background_channel,
            background_method=args.background_method,
            sample_channel=args.sample_channel,
            sample_method=args.sample_method,
            user_regex=args.match_regex or None,
        )
        if background_result is None or not background_result.success:
            raise RuntimeError(
                background_result.error_message if background_result else "背景电离室匹配失败"
            )
        for result in match_results:
            if result.success and result.transmission_percent is not None:
                print(f"[ION] {result.sample_name}: T={result.transmission_percent:.2f}%")
            else:
                print(f"[SKIP] {result.sample_name}: {result.error_message}")
        if not transmissions:
            raise RuntimeError("没有样品获得有效透过率 / No valid ionchamber transmission found")
        return None, transmissions
    return args.transmission or 100.0, None


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        input_dir = Path(args.input_dir)
        if not input_dir.is_dir():
            raise RuntimeError(f"输入目录不存在 / Input directory not found: {input_dir}")

        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        sample_paths = _iter_curve_files(input_dir, args.pattern)
        if args.background:
            background_resolved = str(Path(args.background).resolve())
            sample_paths = [
                path for path in sample_paths if str(Path(path).resolve()) != background_resolved
            ]

        if args.parse_mode != "single" and args.ion_dir:
            raise RuntimeError("多列 XYXY/XYYY 模式暂不支持 T-背景扣除中的电离室自动匹配")

        if not sample_paths:
            print("未找到可处理样品文件 / No sample files found")
            return 0

        config = _build_config(args)
        transmission, transmissions = _resolve_transmissions(args, sample_paths)
        if args.background and transmissions is not None:
            sample_paths = [path for path in sample_paths if path in transmissions]
        context = PipelineContext(
            processor_config=config,
            output_dir=str(output_dir),
            output_format=args.format,
            save_results=args.output_mode == "per-file",
            export_raw=True,
            export_bg=args.save_bg,
            export_sub=args.save_sub,
        )
        tasks: List[TaskItem] = []
        delimiter = None if args.delimiter == "auto" else args.delimiter
        for sample_path in sample_paths:
            layout = inspect_curve_layout(
                path=sample_path,
                parse_mode=args.parse_mode,
                skip_header=args.skip_header,
                delimiter=delimiter,
            )
            for spec in layout["curve_specs"]:
                task = TaskItem(
                    source_path=sample_path,
                    background_path=args.background,
                    transmission=(
                        transmissions.get(sample_path)
                        if transmissions is not None and sample_path in transmissions
                        else transmission
                    ),
                    process_mode=config.process_mode,
                    x_column=spec.x_column,
                    y_column=spec.y_column,
                    skip_header=args.skip_header,
                    delimiter=delimiter,
                    extra={
                        "curve_label": spec.label,
                        "output_suffix": spec.label if args.parse_mode != "single" else "",
                    },
                )
                tasks.append(task)
        engine = PipelineEngine(context)
        success = 0
        collected_curves = []
        for result in engine.run(tasks):
            name = Path(result.source_path).name
            if result.curve is not None:
                success += 1
                collected_curves.append(result.curve)
                transmission_note = result.curve.metadata.extra.get("transmission_percent")
                if transmission_note is not None:
                    print(f"[OK] {name} | T={float(transmission_note):.2f}%")
                else:
                    print(f"[OK] {name}")
            else:
                print(f"[FAIL] {name}: {result.error_msg}")

        if args.output_mode == "merged" and collected_curves:
            merged_path = output_dir / args.merged_output
            if not save_curve_collection(
                curves=collected_curves,
                path=str(merged_path),
                fmt=args.format,
                include_bg=args.save_bg,
                include_subtracted=args.save_sub,
            ):
                raise RuntimeError(f"合并保存失败 / Failed to save merged output: {merged_path}")
            print(f"[MERGED] {merged_path}")

        print(f"完成 / Complete: {success}/{len(tasks)}")
        return 0 if success == len(tasks) else 1
    except Exception as exc:
        print(f"批处理失败: {exc} / Batch processing failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
