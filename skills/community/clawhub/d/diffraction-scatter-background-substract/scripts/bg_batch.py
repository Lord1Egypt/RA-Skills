#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bg_batch.py — 批量二维图像背景扣除
Batch 2D image background subtraction.

命令行脚本：对目录中的样品图像批量执行有参考背景扣除，可使用统一透射率，
或通过电离室文件自动匹配并计算每个样品的透射率。
Command-line script: perform reference-based background subtraction for all sample
images in a directory, using either a fixed transmission value or per-sample
transmission computed from matched ionchamber files.
"""

import argparse
import glob
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


def crop_to_common_shape(sample: np.ndarray, background: np.ndarray):
    """裁剪到共同尺寸 / Crop to common shape"""
    height = min(sample.shape[0], background.shape[0])
    width = min(sample.shape[1], background.shape[1])
    return sample[:height, :width], background[:height, :width]


def resolve_transmission(sample_path: str, args, background_ion_data):
    """解析单个样品透射率 / Resolve transmission for one sample"""
    if args.transmission is not None:
        return float(args.transmission)

    if not args.ion_dir:
        return 1.0

    if background_ion_data is None:
        raise ValueError("背景电离室文件不可用 / Background ionchamber file is unavailable")

    sample_ion = match_ionchamber(sample_path, args.ion_dir)
    if not sample_ion:
        raise ValueError("未匹配到样品电离室文件 / No matching sample ionchamber file found")

    sample_ion_data = load_ionchamber(sample_ion)
    if sample_ion_data is None:
        raise ValueError("样品电离室文件解析失败 / Failed to parse sample ionchamber file")

    denominator = background_ion_data["Ionchamber2"]
    if denominator == 0:
        raise ValueError(
            "背景电离室均值为 0，无法计算透射率 / Background ionchamber mean is 0, cannot compute transmission"
        )

    return float(sample_ion_data["Ionchamber2"] / denominator)


def parse_args():
    """解析命令行参数 / Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="批量二维图像背景扣除 / Batch 2D image background subtraction"
    )
    parser.add_argument("sample_dir", help="样品图像目录 / sample directory")
    parser.add_argument("background", help="背景图像路径 / background image path")
    parser.add_argument(
        "-o",
        "--output-dir",
        default="./output",
        help="输出目录 / output directory",
    )
    parser.add_argument(
        "--pattern",
        default="*.tif",
        help="文件匹配模式 / file matching pattern",
    )
    parser.add_argument("--ion-dir", help="电离室文件目录 / ionchamber directory")
    parser.add_argument(
        "-t",
        "--transmission",
        type=float,
        help="统一透射率覆盖值 / transmission override",
    )
    return parser.parse_args()


def main():
    """主函数 / Main entry point"""
    args = parse_args()

    try:
        sample_files = sorted(glob.glob(os.path.join(args.sample_dir, args.pattern)))
        if not sample_files:
            print(
                f"未找到样品文件: {args.sample_dir} ({args.pattern}) / "
                f"No sample files found: {args.sample_dir} ({args.pattern})"
            )
            return 1

        os.makedirs(args.output_dir, exist_ok=True)

        background_data, _ = load_image_file(args.background)
        if background_data is None:
            print(f"加载失败: {args.background} / Failed to load: {args.background}")
            return 1

        background_array = np.asarray(background_data, dtype=np.float64)
        background_ion_data = None
        if args.ion_dir and args.transmission is None:
            background_ion = match_ionchamber(args.background, args.ion_dir)
            if not background_ion:
                print("未匹配到背景电离室文件 / No matching background ionchamber file found")
                return 1
            background_ion_data = load_ionchamber(background_ion)
            if background_ion_data is None:
                print("背景电离室文件解析失败 / Failed to parse background ionchamber file")
                return 1

        success = 0
        total = len(sample_files)
        for sample_path in sample_files:
            name = os.path.basename(sample_path)
            try:
                sample_data, _ = load_image_file(sample_path)
                if sample_data is None:
                    raise ValueError("图像加载失败 / Image loading failed")

                transmission = resolve_transmission(sample_path, args, background_ion_data)
                if transmission <= 0:
                    raise ValueError("透射率必须大于 0 / Transmission must be greater than 0")

                sample_array = np.asarray(sample_data, dtype=np.float64)
                sample_array, cropped_background = crop_to_common_shape(
                    sample_array, background_array
                )
                result = sample_array / transmission - cropped_background

                stem, _ = os.path.splitext(name)
                output_path = os.path.join(args.output_dir, f"{stem}_bgsub.tif")
                if not save_image(result, output_path, format="auto", header=None):
                    raise ValueError("结果保存失败 / Failed to save result")

                success += 1
                print(
                    f"[OK] {name} -> T={transmission * 100:.2f}% / [OK] {name} -> T={transmission * 100:.2f}%"
                )
            except Exception as exc:
                print(f"[FAIL] {name} - {exc} / [FAIL] {name} - {exc}")

        print(f"完成: {success}/{total} 成功 / Complete: {success}/{total} succeeded")
        return 0 if success == total else 1
    except Exception as exc:
        print(f"批量处理失败: {exc} / Batch processing failed: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
