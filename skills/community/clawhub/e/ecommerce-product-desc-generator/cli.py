#!/usr/bin/env python3
"""
电商产品描述批量生成器 - CLI 入口
用法示例:
  python cli.py "蓝牙耳机" "3C数码" --keywords "无线,降噪,运动" --platforms amazon,tiktok
  python cli.py --csv products.csv --format markdown --output desc.md
  python cli.py --batch --product "充电宝" "电子产品" --all-platforms
"""

import sys
import argparse
from generator import (
    ProductDescGenerator, parse_csv_input, __version__
)


def main():
    parser = argparse.ArgumentParser(
        prog="ecommerce-product-desc",
        description="电商产品描述批量生成器 — 支持亚马逊/淘宝/拼多多/TikTok Shop/Shopify",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "蓝牙耳机" "3C数码" --keywords "无线,降噪" --platforms amazon,tiktok
  %(prog)s --csv products.csv --format markdown --output result.md
  %(prog)s --batch --product "充电宝" "电子产品" --all-platforms
  %(prog)s "真丝围巾" "服饰" --platforms taobao,pinduoduo --format txt
        """
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("product", nargs="?", help="产品名称（必填）")
    parser.add_argument("category", nargs="?", help="品类/类目")
    parser.add_argument("--keywords", "-k", default="", help="关键词，多个用逗号分隔")
    parser.add_argument("--brand", "-b", default="", help="品牌名")
    parser.add_argument("--price", "-p", default="", help="目标价格/价格区间")
    parser.add_argument(
        "--platforms",
        default="all",
        help="目标平台，逗号分隔: amazon,taobao,pinduoduo,tiktok,shopify 或 'all' (默认: all)"
    )
    parser.add_argument("--all-platforms", action="store_true",
                        help="生成所有5个平台")
    parser.add_argument(
        "--format", "-f",
        choices=["markdown", "txt", "csv"],
        default="markdown",
        help="输出格式 (默认: markdown)"
    )
    parser.add_argument("--output", "-o", default="",
                        help="输出到文件（默认打印到 stdout）")
    parser.add_argument("--csv", help="从 CSV 文件读取产品列表进行批量生成")
    parser.add_argument("--batch", action="store_true",
                        help="批量模式（可与 --product 配合）")
    parser.add_argument("--seed", type=int, default=None,
                        help="随机种子（用于复现结果）")

    args = parser.parse_args()
    import random
    if args.seed is not None:
        random.seed(args.seed)

    # 解析平台列表
    if args.all_platforms or args.platforms == "all":
        platforms = None  # None 表示全平台
    else:
        platforms = [p.strip() for p in args.platforms.split(",") if p.strip()]
        if not platforms:
            platforms = None

    gen = ProductDescGenerator()

    output = ""

    if args.csv:
        # CSV 批量模式
        try:
            with open(args.csv, "r", encoding="utf-8") as f:
                csv_text = f.read()
        except FileNotFoundError:
            print(f"错误：找不到 CSV 文件 '{args.csv}'", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"错误：读取 CSV 失败 - {e}", file=sys.stderr)
            sys.exit(1)

        products = parse_csv_input(csv_text)
        if not products:
            print("错误：CSV 中没有找到有效产品数据（需要 'product_name' 列）", file=sys.stderr)
            sys.exit(1)
        print(f"正在批量生成 {len(products)} 个产品描述...", file=sys.stderr)
        output = gen.generate_batch(products, platforms=platforms, output_format=args.format)

    elif args.batch and args.product:
        # 命令行指定批量
        products = [{
            "product_name": args.product,
            "category": args.category or "",
            "keywords": args.keywords,
            "brand": args.brand,
            "price": args.price,
        }]
        output = gen.generate_batch(products, platforms=platforms, output_format=args.format)

    elif args.product:
        # 单产品生成
        results = gen.generate_single(
            product_name=args.product,
            category=args.category or "",
            keywords=args.keywords,
            brand=args.brand,
            price=args.price,
            platforms=platforms,
        )
        if args.format == "markdown":
            output = gen.to_markdown(results, args.product)
        elif args.format == "txt":
            output = gen.to_txt(results, args.product)
        else:
            output = gen.to_csv(results)
    else:
        parser.print_help()
        sys.exit(0)

    # 输出
    if output:
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"✅ 已保存到 {args.output}")
        else:
            print(output)


if __name__ == "__main__":
    main()
