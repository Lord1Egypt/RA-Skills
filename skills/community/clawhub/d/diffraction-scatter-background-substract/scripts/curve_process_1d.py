#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
curve_process_1d.py — 1D曲线处理脚本
Single-file 1D curve processing script.

支持两类工作流：
1. 算法背景估计：morph / poly / rolling_ball
2. 传统参考背景扣除：sample / (T/100) - background

Supports two workflows:
1. Algorithmic background estimation: morph / poly / rolling_ball
2. Traditional reference subtraction: sample / (T/100) - background
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.curve_data import Curve1D, CurveMetadata, ProcessMode  # noqa: E402
from lib.curve_processor import CurveProcessorConfig  # noqa: E402
from lib.task_pipeline import PipelineContext, PipelineEngine  # noqa: E402
from lib.curve_io import (  # noqa: E402
    inspect_curve_layout,
    save_curve_collection,
    save_curve_with_background,
)
from lib.common import (  # noqa: E402
    build_transmission_map,
    calc_ion_intensity,
    load_ionchamber_table,
)


METHOD_LABELS = {
    "morph": "形态学 / Morphological",
    "poly": "多项式 / Polynomial",
    "rolling_ball": "滚球 / Rolling Ball",
}


def build_parser() -> argparse.ArgumentParser:
    """构建参数解析器。Build the argument parser."""
    parser = argparse.ArgumentParser(
        description="单条 1D 曲线处理：算法背景估计或参考背景 T 修正扣除 / Process one 1D curve with algorithmic background estimation or T-corrected reference subtraction."
    )
    parser.add_argument("input", help="输入曲线文件 / Input curve file")
    parser.add_argument("--background", help="参考背景曲线文件 / Reference background curve")
    parser.add_argument(
        "--parse-mode",
        choices=["single", "xyxy", "xyyy"],
        default="single",
        help="列结构 / Column layout",
    )
    parser.add_argument("--skip-header", type=int, default=0, help="跳过头部行数 / Skip header")
    parser.add_argument(
        "--delimiter",
        choices=["auto", "comma", "tab", "space"],
        default="auto",
        help="分隔符 / Delimiter",
    )
    parser.add_argument(
        "--method",
        choices=["morph", "poly", "rolling_ball"],
        default="morph",
        help="算法背景模式下的方法 / Method for algorithmic background mode",
    )
    parser.add_argument("--radius", type=int, default=50, help="半径参数 / Radius parameter")
    parser.add_argument(
        "--iterations", type=int, default=1, help="形态学迭代次数 / Morph iterations"
    )
    parser.add_argument("--degree", type=int, default=4, help="多项式阶数 / Polynomial degree")
    parser.add_argument(
        "--quantile", type=float, default=0.3, help="多项式分位数 / Polynomial quantile"
    )
    parser.add_argument(
        "-t",
        "--transmission",
        type=float,
        help="手动透过率(%%) / Manual transmission percent",
    )
    parser.add_argument("--ion-dir", help="电离室文件目录 / Ionchamber directory")
    parser.add_argument(
        "--ion-files",
        nargs="+",
        help="额外指定电离室文件列表 / Additional explicit ionchamber files",
    )
    parser.add_argument(
        "--sample-ion", help="显式指定样品电离室文件 / Explicit sample ionchamber file"
    )
    parser.add_argument(
        "--background-ion", help="显式指定背景电离室文件 / Explicit background ionchamber file"
    )
    parser.add_argument(
        "--sample-channel",
        default="Ionchamber1",
        choices=["Ionchamber0", "Ionchamber1", "Ionchamber2"],
        help="样品通道 / Sample channel",
    )
    parser.add_argument(
        "--background-channel",
        default="Ionchamber1",
        choices=["Ionchamber0", "Ionchamber1", "Ionchamber2"],
        help="背景通道 / Background channel",
    )
    parser.add_argument(
        "--sample-method",
        default="median",
        choices=["mean", "median", "trimmed_mean"],
        help="样品统计方法 / Sample summary method",
    )
    parser.add_argument(
        "--background-method",
        default="median",
        choices=["mean", "median", "trimmed_mean"],
        help="背景统计方法 / Background summary method",
    )
    parser.add_argument(
        "--match-regex", default="", help="可选自定义匹配正则 / Optional custom matching regex"
    )
    parser.add_argument("-o", "--output", help="输出文件路径 / Output file path")
    parser.add_argument(
        "--format",
        choices=["auto", "xy", "csv", "txt", "gr", "npy", "h5"],
        default="auto",
        help="输出格式 / Output format",
    )
    parser.add_argument(
        "--output-mode",
        choices=["merged", "per-file"],
        default="merged",
        help="输出模式 / Output mode",
    )
    parser.add_argument(
        "--preview", action="store_true", help="显示 matplotlib 预览 / Show matplotlib preview"
    )
    return parser


def _detect_format(output_path: str, requested_format: str) -> str:
    if requested_format != "auto":
        return requested_format
    suffix = Path(output_path).suffix.lower().lstrip(".")
    return suffix if suffix in {"xy", "csv", "txt", "gr", "npy"} else "xy"


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


def _collect_ion_paths(args: argparse.Namespace) -> List[str]:
    ion_paths: List[str] = []
    if args.ion_dir:
        ion_dir = Path(args.ion_dir)
        if ion_dir.is_dir():
            for path in sorted(ion_dir.rglob("*")):
                if path.is_file() and path.suffix.lower() in {".ionchamber", ".txt"}:
                    ion_paths.append(str(path))
    if args.ion_files:
        for path in args.ion_files:
            if path not in ion_paths:
                ion_paths.append(path)
    return ion_paths


def _compute_explicit_transmission(args: argparse.Namespace) -> Optional[float]:
    if not args.sample_ion or not args.background_ion:
        return None
    sample_table = load_ionchamber_table(args.sample_ion)
    background_table = load_ionchamber_table(args.background_ion)
    if sample_table is None or background_table is None:
        raise RuntimeError("显式电离室文件读取失败 / Failed to read explicit ionchamber files")
    sample_intensity = calc_ion_intensity(sample_table, args.sample_channel, args.sample_method)
    background_intensity = calc_ion_intensity(
        background_table, args.background_channel, args.background_method
    )
    if sample_intensity is None or background_intensity in (None, 0):
        raise RuntimeError(
            "显式电离室强度计算失败 / Failed to calculate explicit ionchamber intensity"
        )
    return sample_intensity / background_intensity * 100.0


def _resolve_transmission(args: argparse.Namespace) -> Optional[float]:
    if not args.background:
        return None
    if args.transmission is not None:
        return args.transmission

    explicit_transmission = _compute_explicit_transmission(args)
    if explicit_transmission is not None:
        return explicit_transmission

    ion_paths = _collect_ion_paths(args)
    if not ion_paths:
        return 100.0

    transmissions, match_results, background_result = build_transmission_map(
        sample_paths=[args.input],
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
    if args.input not in transmissions:
        reason = match_results[0].error_message if match_results else "样品电离室匹配失败"
        raise RuntimeError(reason)
    return transmissions[args.input]


def _run_pipeline(
    args: argparse.Namespace,
    config: CurveProcessorConfig,
) -> List[Curve1D]:
    transmission = _resolve_transmission(args)
    layout = inspect_curve_layout(
        path=args.input,
        parse_mode=args.parse_mode,
        skip_header=args.skip_header,
        delimiter=None if args.delimiter == "auto" else args.delimiter,
    )
    ctx = PipelineContext(
        processor_config=config,
        output_dir="",
        save_results=False,
        export_raw=True,
        export_bg=True,
        export_sub=True,
    )
    engine = PipelineEngine(ctx)
    tasks = []
    for spec in layout["curve_specs"]:
        tasks.extend(
            PipelineEngine.build_tasks(
                paths=[args.input],
                process_mode=config.process_mode,
                background_path=args.background,
                transmission=transmission,
                x_column=spec.x_column,
                y_column=spec.y_column,
                skip_header=args.skip_header,
                delimiter=None if args.delimiter == "auto" else args.delimiter,
            )
        )
        tasks[-1].extra["curve_label"] = spec.label
        tasks[-1].extra["output_suffix"] = spec.label if args.parse_mode != "single" else ""
    results = engine.run_all(tasks)
    curves: List[Curve1D] = []
    for result in results:
        if result.curve is None:
            raise RuntimeError(result.error_msg or "处理失败 / Processing failed")
        if transmission is not None:
            result.curve.metadata.extra["transmission_source"] = (
                "manual" if args.transmission is not None else "ionchamber"
            )
        curves.append(result.curve)
    return curves


def _show_preview(curve: Curve1D) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(f"无法导入 matplotlib / Failed to import matplotlib: {exc}") from exc

    fig, axes = plt.subplots(1, 3, figsize=(15, 4), constrained_layout=True)
    axes[0].plot(curve.x, curve.y, color="tab:blue", lw=1.2)
    axes[0].set_title("原始曲线 / Raw")
    axes[1].plot(curve.x, curve.y, color="0.75", lw=1.0, label="Raw")
    if curve.background is not None:
        axes[1].plot(curve.x, curve.background, color="tab:orange", lw=1.2, label="Background")
    axes[1].set_title("背景 / Background")
    axes[1].legend()
    if curve.subtracted is not None:
        axes[2].plot(curve.x, curve.subtracted, color="tab:green", lw=1.2)
    axes[2].set_title("扣除后 / Subtracted")
    plt.show()


def _save_outputs(curves: List[Curve1D], output_path: str, fmt: str, output_mode: str) -> None:
    if output_mode == "merged" or len(curves) == 1:
        target_curve = curves[0] if len(curves) == 1 and output_mode != "merged" else None
        if target_curve is not None:
            save_curve_with_background(
                curve=target_curve,
                path=output_path,
                include_bg=target_curve.background is not None,
                include_subtracted=target_curve.subtracted is not None,
                fmt=fmt,
            )
            return
        if not save_curve_collection(
            curves=curves,
            path=output_path,
            fmt=fmt,
            include_bg=True,
            include_subtracted=True,
        ):
            raise RuntimeError("合并保存失败 / Failed to save merged output")
        return

    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    for curve in curves:
        label = curve.metadata.extra.get("curve_label", "curve")
        base_name = f"{Path(curve.metadata.source_file).stem}_{label}"
        ext = ".h5" if fmt == "h5" else f".{fmt if fmt != 'auto' else 'xy'}"
        path = output_dir / f"{base_name}{ext}"
        save_curve_with_background(
            curve=curve,
            path=str(path),
            include_bg=curve.background is not None,
            include_subtracted=curve.subtracted is not None,
            fmt=fmt,
        )


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        config = _build_config(args)
        if args.parse_mode != "single" and args.background and (args.ion_dir or args.sample_ion):
            raise RuntimeError("多列 XYXY/XYYY 模式暂不支持 T-背景扣除中的电离室自动匹配")
        results = _run_pipeline(args, config)
        result = results[0]

        if args.background:
            transmission = result.metadata.extra.get(
                "transmission_percent", args.transmission or 100.0
            )
            print(
                f"参考背景模式 / Reference mode: T = {float(transmission):.4f}% | 背景文件 / Background = {Path(args.background).name}"
            )
        else:
            print(f"算法背景模式 / Algorithmic mode: {METHOD_LABELS[args.method]}")

        if args.output:
            fmt = _detect_format(args.output, args.format)
            _save_outputs(results, args.output, fmt, args.output_mode)
            print(f"已保存结果 / Saved result: {args.output}")
        else:
            print(f"曲线数量 / Curves: {len(results)}")
            print(f"点数 / Points: {result.n_points}")
            if result.subtracted is not None:
                print(
                    f"扣除后最小/最大值 / Subtracted min/max: {result.subtracted.min():.6g} / {result.subtracted.max():.6g}"
                )

        if args.preview:
            _show_preview(result)
        return 0
    except Exception as exc:
        print(f"处理失败: {exc} / Processing failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
