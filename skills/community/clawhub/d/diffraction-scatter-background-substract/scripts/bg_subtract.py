#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bg_subtract.py — 有参考背景扣除
Background subtraction with reference image.

命令行脚本：加载样品图像与背景图像，按给定透射率或电离室文件自动计算透射率，
执行二维图像背景扣除，并保存输出结果。
Command-line script: load sample and background images, compute transmission from a
provided value or matching ionchamber files, perform 2D image background subtraction,
and save the output result.
"""

import argparse
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.image_io import load_image_file, save_image


def load_ionchamber(path: str):
    """加载电离室文件 / Load ionchamber file"""
    values = {"Ionchamber0": [], "Ionchamber1": [], "Ionchamber2": []}
    try:
        with open(path, "r", encoding="utf-8") as handle:
            for raw_line in handle:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split()
                if len(parts) < 5:
                    continue
                try:
                    floats = [float(parts[-3]), float(parts[-2]), float(parts[-1])]
                except ValueError:
                    continue
                values["Ionchamber0"].append(floats[0])
                values["Ionchamber1"].append(floats[1])
                values["Ionchamber2"].append(floats[2])
    except OSError:
        return None

    if not values["Ionchamber0"]:
        return None

    return {key: float(np.mean(channel_values)) for key, channel_values in values.items()}


def match_ionchamber(filename: str, ion_dir: str) -> str:
    """匹配电离室文件 / Match ionchamber file to image filename"""
    base_name = os.path.basename(filename)
    stem, _ = os.path.splitext(base_name)
    candidates = []

    match = re.search(r"(\d+)(?!.*\d)", stem)
    if match:
        number = match.group(1)
        stripped = str(int(number))
        three_digit = f"{int(number):03d}"
        candidates.extend(
            [
                f"_{number}",
                f"_{three_digit}",
                f"_{stripped}",
                number,
                three_digit,
                stripped,
            ]
        )

    try:
        ion_files = [
            os.path.join(ion_dir, name)
            for name in os.listdir(ion_dir)
            if name.lower().endswith(".ionchamber")
        ]
    except OSError:
        return None

    stem_lower = stem.lower()
    for path in ion_files:
        ion_stem = os.path.splitext(os.path.basename(path))[0].lower()
        if ion_stem == stem_lower:
            return path
        for candidate in candidates:
            candidate_lower = candidate.lower()
            if ion_stem.endswith(candidate_lower) or candidate_lower in ion_stem:
                return path
    return None


def format_shape(data: np.ndarray) -> str:
    """格式化图像尺寸 / Format image shape"""
    if data.ndim < 2:
        return "unknown"
    return f"{data.shape[0]}x{data.shape[1]}"


def crop_to_common_shape(sample: np.ndarray, background: np.ndarray):
    """裁剪到共同尺寸 / Crop to common shape"""
    height = min(sample.shape[0], background.shape[0])
    width = min(sample.shape[1], background.shape[1])
    return sample[:height, :width], background[:height, :width]


def resolve_transmission(args, sample_path: str, background_path: str):
    """解析透射率 / Resolve transmission"""
    if args.transmission is not None:
        return float(args.transmission)

    if not args.ion_dir:
        return 1.0

    sample_ion = match_ionchamber(sample_path, args.ion_dir)
    background_ion = match_ionchamber(background_path, args.ion_dir)
    if not sample_ion or not background_ion:
        raise ValueError(
            "无法匹配样品或背景的电离室文件 / Could not match ionchamber file for sample or background"
        )

    sample_data = load_ionchamber(sample_ion)
    background_data = load_ionchamber(background_ion)
    if sample_data is None or background_data is None:
        raise ValueError("电离室文件解析失败 / Failed to parse ionchamber file")

    denominator = background_data["Ionchamber2"]
    if denominator == 0:
        raise ValueError(
            "背景电离室均值为 0，无法计算透射率 / Background ionchamber mean is 0, cannot compute transmission"
        )

    return float(sample_data["Ionchamber2"] / denominator)


def parse_args():
    """解析命令行参数 / Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="有参考背景扣除 / Background subtraction with reference image"
    )
    parser.add_argument("sample", help="样品图像路径 / sample image path")
    parser.add_argument("background", help="背景图像路径 / background image path")
    parser.add_argument("-o", "--output", help="输出文件路径 / output file path")
    parser.add_argument(
        "-t",
        "--transmission",
        type=float,
        help="透射率（0-1） / transmission (0-1)",
    )
    parser.add_argument("--ion-dir", help="电离室文件目录 / ionchamber directory")
    return parser.parse_args()


def main():
    """主函数 / Main entry point"""
    args = parse_args()

    try:
        sample_data, _ = load_image_file(args.sample)
        if sample_data is None:
            print(f"加载失败: {args.sample} / Failed to load: {args.sample}")
            return 1

        background_data, _ = load_image_file(args.background)
        if background_data is None:
            print(f"加载失败: {args.background} / Failed to load: {args.background}")
            return 1

        sample_array = np.asarray(sample_data, dtype=np.float64)
        background_array = np.asarray(background_data, dtype=np.float64)

        print(
            f"加载成功: {os.path.basename(args.sample)} ({format_shape(sample_array)}) / "
            f"Loaded: {os.path.basename(args.sample)} ({format_shape(sample_array)})"
        )
        print(
            f"加载成功: {os.path.basename(args.background)} ({format_shape(background_array)}) / "
            f"Loaded: {os.path.basename(args.background)} ({format_shape(background_array)})"
        )

        transmission = resolve_transmission(args, args.sample, args.background)
        if transmission <= 0:
            print("透射率必须大于 0 / Transmission must be greater than 0")
            return 1

        print(
            f"透射率: T={transmission:.4f} ({transmission * 100:.2f}%) / "
            f"Transmission: T={transmission:.4f} ({transmission * 100:.2f}%)"
        )

        sample_array, background_array = crop_to_common_shape(sample_array, background_array)
        result = sample_array / transmission - background_array

        if args.output:
            ok = save_image(result, args.output, format="auto", header=None)
            if not ok:
                print(f"保存失败: {args.output} / Failed to save: {args.output}")
                return 1
            print(f"已保存: {args.output} / Saved: {args.output}")
        else:
            print(
                f"结果统计: min={result.min():.6g}, max={result.max():.6g}, mean={result.mean():.6g} / "
                f"Result statistics: min={result.min():.6g}, max={result.max():.6g}, mean={result.mean():.6g}"
            )

        return 0
    except Exception as exc:
        print(f"处理失败: {exc} / Processing failed: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
