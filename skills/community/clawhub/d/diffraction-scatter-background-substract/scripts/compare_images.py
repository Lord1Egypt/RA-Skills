#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compare_images.py — 使用 silx CompareImages 对比两张图像
Compare two images with silx CompareImages.

命令行脚本：加载两张二维图像，并使用 silx 的 CompareImages 组件弹出交互式对比窗口。
Command-line script: load two 2D images and open an interactive comparison window
using silx CompareImages.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.image_io import load_image_file


def parse_args():
    """解析命令行参数 / Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="使用 silx CompareImages 对比两张图像 / Compare two images with silx CompareImages"
    )
    parser.add_argument("image1", help="第一张图像 / first image")
    parser.add_argument("image2", help="第二张图像 / second image")
    return parser.parse_args()


def main():
    """主函数 / Main entry point"""
    args = parse_args()

    try:
        try:
            from silx.gui.compare import CompareImages
            from silx.gui import qt
        except ImportError:
            print("错误: silx 未安装 / Error: silx is not installed")
            print("安装: pip install silx / Install: pip install silx")
            return 1

        data1, _ = load_image_file(args.image1)
        if data1 is None:
            print(f"加载失败: {args.image1} / Failed to load: {args.image1}")
            return 1

        data2, _ = load_image_file(args.image2)
        if data2 is None:
            print(f"加载失败: {args.image2} / Failed to load: {args.image2}")
            return 1

        app = qt.QApplication([])
        widget = CompareImages()
        widget.setData(data1, data2)
        widget.show()
        app.exec()
        return 0
    except Exception as exc:
        print(f"对比失败: {exc} / Comparison failed: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
