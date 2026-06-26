#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
format_convert.py — 二维图像格式转换
2D image format conversion.

命令行脚本：探测输入文件类型，加载 TIFF、EDF 或 H5 图像数据，并导出为目标格式。
对于 H5 多帧数据，可选择指定帧进行导出。
Command-line script: probe the input file type, load TIFF, EDF, or H5 image data,
and export it to the target format. For H5 multi-frame data, a specific frame can
be selected for export.
"""

import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.image_io import load_h5_stack, load_image_file, probe_image_file, save_image


def parse_args():
    """解析命令行参数 / Parse command-line arguments"""
    parser = argparse.ArgumentParser(description="二维图像格式转换 / 2D image format conversion")
    parser.add_argument("input", help="输入文件路径 / input file path")
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="输出文件路径 / output file path",
    )
    parser.add_argument(
        "--format",
        choices=["edf", "tif", "tiff"],
        help="输出格式 / output format",
    )
    parser.add_argument(
        "--frame",
        type=int,
        default=0,
        help="H5 导出帧索引 / frame index for H5 export",
    )
    return parser.parse_args()


def detect_output_format(args) -> str:
    """解析输出格式 / Resolve output format"""
    if args.format:
        return args.format
    ext = os.path.splitext(args.output)[1].lower()
    if ext in {".edf", ".tif", ".tiff"}:
        return ext.lstrip(".")
    return "auto"


def extract_h5_frame(stack_info, frame_index: int):
    """从 H5 结构中提取帧 / Extract frame from H5 structure"""
    if not isinstance(stack_info, dict):
        raise ValueError("H5 数据结构无效 / Invalid H5 data structure")

    arrays = []
    for value in stack_info.values():
        if isinstance(value, np.ndarray) and value.ndim >= 2:
            arrays.append(value)

    if not arrays:
        raise ValueError("未在 H5 文件中找到图像数据 / No image data found in H5 file")

    data = arrays[0]
    if data.ndim == 2:
        if frame_index != 0:
            raise ValueError("二维 H5 数据仅支持 frame=0 / 2D H5 data only supports frame=0")
        return np.asarray(data), None

    if frame_index < 0 or frame_index >= data.shape[0]:
        raise ValueError(f"帧索引超出范围: {frame_index} / Frame index out of range: {frame_index}")
    return np.asarray(data[frame_index]), None


def main():
    """主函数 / Main entry point"""
    args = parse_args()

    try:
        probe, probe_meta = probe_image_file(args.input)
        if probe is None and probe_meta is None:
            print(f"无法识别输入文件: {args.input} / Could not probe input file: {args.input}")
            return 1

        lower_path = args.input.lower()
        if lower_path.endswith(".h5") or lower_path.endswith(".hdf5"):
            stack_info = load_h5_stack(args.input)
            if stack_info is None:
                print(f"H5 加载失败: {args.input} / Failed to load H5: {args.input}")
                return 1
            data, header = extract_h5_frame(stack_info, args.frame)
        else:
            data, header = load_image_file(args.input)
            if data is None:
                print(f"图像加载失败: {args.input} / Failed to load image: {args.input}")
                return 1

        output_format = detect_output_format(args)
        ok = save_image(np.asarray(data), args.output, format=output_format, header=header)
        if not ok:
            print(f"保存失败: {args.output} / Failed to save: {args.output}")
            return 1

        print(
            f"转换成功: {args.input} -> {args.output} / "
            f"Conversion succeeded: {args.input} -> {args.output}"
        )
        return 0
    except Exception as exc:
        print(f"转换失败: {exc} / Conversion failed: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
