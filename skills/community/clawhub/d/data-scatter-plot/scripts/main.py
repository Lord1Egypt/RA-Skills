# -*- coding: utf-8 -*-
"""
命令行入口模块
"""

import argparse
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from data_loader import ExcelDataLoader
from scatter_generator import ScatterPlotGenerator
from config import DEFAULT_OUTPUT_DIR, DEFAULT_OUTPUT_FORMAT


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='数据散点图生成工具（支持CSV/Excel）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python -m scripts.main -i Test.xls
  python -m scripts.main -i Test.xls -o output/plots
  python -m scripts.main -i Test.xls -o output --dpi 150
        """
    )

    parser.add_argument(
        '-i', '--input',
        required=True,
        help='输入数据文件路径（支持.csv/.xls/.xlsx）'
    )

    parser.add_argument(
        '-o', '--output-dir',
        default=DEFAULT_OUTPUT_DIR,
        help=f'输出目录（默认: {DEFAULT_OUTPUT_DIR}）'
    )

    parser.add_argument(
        '-f', '--format',
        default=DEFAULT_OUTPUT_FORMAT,
        help=f'输出图片格式（默认: {DEFAULT_OUTPUT_FORMAT}）'
    )

    parser.add_argument(
        '--dpi',
        type=int,
        default=300,
        help='图片分辨率（默认: 300）'
    )

    parser.add_argument(
        '--show',
        action='store_true',
        help='显示图片（不保存）'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='仅列出将要生成的散点图，不实际生成'
    )

    return parser.parse_args()


def main():
    """主函数"""
    args = parse_args()

    print("=" * 60)
    print("数据散点图生成工具（支持CSV/Excel）")
    print("=" * 60)

    # 1. 加载数据
    print(f"\n[1/4] 加载数据文件: {args.input}")
    try:
        loader = ExcelDataLoader(args.input)
        df = loader.load()
        print(f"      数据加载成功，共 {len(df)} 行")
    except Exception as e:
        print(f"      数据加载失败: {str(e)}")
        sys.exit(1)

    # 2. 获取散点图配置
    print("\n[2/4] 分析散点图配置...")
    try:
        configs = loader.get_scatter_configs()
        print(f"      发现 {len(configs)} 个散点图配置")
    except Exception as e:
        print(f"      配置分析失败: {str(e)}")
        sys.exit(1)

    if not configs:
        print("      未发现有效的散点图配置")
        sys.exit(0)

    # 3. Dry run模式
    if args.dry_run:
        print("\n[3/4] Dry Run模式 - 列出将要生成的散点图:")
        for i, config in enumerate(configs, 1):
            print(f"      {i}. {config.item_name} + {config.column_title}")
            print(f"         Y轴: {config.y_label}")
            print(f"         Min: {config.min_limit}, Max: {config.max_limit}")
            print(f"         数据点数: {len(config.result_data)}")
        print(f"\n      共 {len(configs)} 个散点图")
        return

    # 4. 生成散点图
    print(f"\n[4/4] 生成散点图...")
    print(f"      输出目录: {args.output_dir}")
    print(f"      输出格式: {args.format}")
    print(f"      分辨率: {args.dpi} DPI")
    print()

    generator = ScatterPlotGenerator(
        output_dir=args.output_dir,
        output_format=args.format,
        dpi=args.dpi
    )

    saved_paths = generator.generate_batch(configs, show=args.show)

    # 总结
    print()
    print("=" * 60)
    print(f"完成！成功生成 {len(saved_paths)} 个散点图")
    print("=" * 60)


if __name__ == '__main__':
    main()
