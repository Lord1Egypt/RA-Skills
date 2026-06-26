#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
地址分类器启动脚本
Usage: python run.py <input_file> [output_file]
"""

import sys
import os
from pathlib import Path

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from address_classifier import AddressClassifier


def main():
    if len(sys.argv) < 2:
        print("用法: python run.py <输入文件> [输出文件]")
        print("示例: python run.py examples/sample_data.txt output/result.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output/result.txt"

    # 检查输入文件
    if not os.path.exists(input_file):
        print(f"错误: 输入文件不存在: {input_file}")
        sys.exit(1)

    # 确保输出目录存在
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 初始化并运行
    print("正在初始化地址分类器...")
    classifier = AddressClassifier()

    print(f"正在处理文件: {input_file}")
    stats = classifier.process_file(input_file, output_file)

    print("\n处理完成！统计结果:")
    print("=" * 50)
    print(f"总计处理: {stats['total']} 条")
    print(f"本省本市: {stats['本省本市']} 条")
    print(f"本省外市: {stats['本省外市']} 条")
    print(f"外省: {stats['外省']} 条")
    print(f"地址不全: {stats['地址不全']} 条")
    if stats['未知'] > 0:
        print(f"未知: {stats['未知']} 条")
    print("=" * 50)
    print(f"输出文件: {output_file}")


if __name__ == "__main__":
    main()
