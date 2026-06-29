#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Color Toolkit - CLI入口
命令行颜色工具
"""

import argparse
import json
import sys
from typing import Optional

from color_toolkit import (
    convert_color, get_contrast, get_complementary,
    get_palette, ColorCore
)
from preview_generator import (
    generate_full_preview_html, generate_palette_page_html
)
from color_recommender import recommend_color, format_recommendation_output


def cmd_convert(args):
    """转换颜色"""
    try:
        result = convert_color(args.color)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_contrast(args):
    """计算对比度"""
    try:
        result = get_contrast(args.color1, args.color2, args.algorithm)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_complementary(args):
    """获取互补色"""
    try:
        result = get_complementary(args.color)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_palette(args):
    """生成调色板"""
    try:
        result = get_palette(args.color, args.type)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_preview(args):
    """生成预览"""
    try:
        output_path = args.output or f"color_preview_{args.color.replace('#', '')}.html"
        generate_full_preview_html(
            args.color,
            title=args.title or "颜色预览",
            show_complementary=not args.no_complementary,
            show_contrast=not args.no_contrast,
            output_path=output_path
        )
        print(f"预览文件已生成: {output_path}")
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_recommend(args):
    """推荐配色"""
    try:
        output_path = args.output if args.preview else None
        result = recommend_color(
            args.description,
            generate_preview=args.preview,
            output_path=output_path
        )

        if args.format == "json":
            # 输出JSON
            if args.preview:
                # 移除HTML内容以保持输出简洁
                result_copy = result.copy()
                result_copy.pop("preview_html", None)
                print(json.dumps(result_copy, indent=2, ensure_ascii=False))
            else:
                print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            # 输出格式化文本
            print(format_recommendation_output(result))

            if args.preview and result.get("preview_path"):
                print(f"\n📄 预览文件: {result['preview_path']}")

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_random(args):
    """生成随机颜色"""
    try:
        colors = [ColorCore.generate_random_color() for _ in range(args.count)]

        if args.preview:
            output_path = f"random_palette_{args.count}.html"
            generate_palette_page_html(colors, f"随机配色 ({args.count}色)", output_path)
            print(f"随机颜色: {' | '.join(colors)}")
            print(f"预览文件: {output_path}")
        else:
            print(json.dumps(colors, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_validate(args):
    """验证颜色格式"""
    try:
        is_valid = ColorCore.is_valid_hex(args.color)
        if is_valid:
            print(f"✅ 有效颜色: {args.color}")
            info = convert_color(args.color)
            print(json.dumps(info, indent=2, ensure_ascii=False))
        else:
            print(f"❌ 无效颜色格式: {args.color}")
            sys.exit(1)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_compare(args):
    """比较多个颜色"""
    try:
        colors = args.colors
        print(f"比较 {len(colors)} 个颜色:\n")

        results = []
        for color in colors:
            info = convert_color(color)
            results.append({
                "color": color,
                "hex": info["hex"],
                "family": info["family"],
                "temperature": info["temperature"],
                "luminance": info["luminance"]
            })

        for r in results:
            print(f"• {r['hex']} | {r['family']} | {r['temperature']} | 亮度: {r['luminance']}")

        # 生成对比预览
        if len(colors) >= 2:
            output_path = f"compare_{'_'.join(c.replace('#', '') for c in colors[:3])}.html"
            generate_palette_page_html(colors, "颜色对比", output_path)
            print(f"\n📄 对比预览: {output_path}")

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def create_parser():
    """创建参数解析器"""
    parser = argparse.ArgumentParser(
        description="Color Toolkit - 专业颜色工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 转换颜色
  python cli.py convert "#3498db"
  python cli.py convert "rgb(52, 152, 219)"
  python cli.py convert "hsl(204, 70%, 53%)"

  # 计算对比度
  python cli.py contrast "#000000" "#ffffff"
  python cli.py contrast "#FF0000" "#00FF00" --algorithm apca

  # 生成调色板
  python cli.py palette "#3498db" --type triadic

  # 颜色推荐
  python cli.py recommend "科技感 蓝色" --preview

  # 生成预览
  python cli.py preview "#3498db" --output my_color.html

  # 随机颜色
  python cli.py random --count 5 --preview
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # convert
    parser_convert = subparsers.add_parser("convert", help="转换颜色到所有格式")
    parser_convert.add_argument("color", help="颜色值 (HEX/RGB/HSL)")
    parser_convert.set_defaults(func=cmd_convert)

    # contrast
    parser_contrast = subparsers.add_parser("contrast", help="计算颜色对比度")
    parser_contrast.add_argument("color1", help="颜色1")
    parser_contrast.add_argument("color2", help="颜色2")
    parser_contrast.add_argument("--algorithm", "-a", default="all",
                                  choices=["all", "wcag2", "apca", "cielab", "ciede2000"],
                                  help="对比度算法")
    parser_contrast.set_defaults(func=cmd_contrast)

    # complementary
    parser_comp = subparsers.add_parser("complementary", help="获取互补色")
    parser_comp.add_argument("color", help="颜色值")
    parser_comp.set_defaults(func=cmd_complementary)

    # palette
    parser_palette = subparsers.add_parser("palette", help="生成调色板")
    parser_palette.add_argument("color", help="基准颜色")
    parser_palette.add_argument("--type", "-t", default="triadic",
                                 choices=["triadic", "tetradic", "analogous", "complementary"],
                                 help="调色板类型")
    parser_palette.set_defaults(func=cmd_palette)

    # preview
    parser_preview = subparsers.add_parser("preview", help="生成HTML预览")
    parser_preview.add_argument("color", help="颜色值")
    parser_preview.add_argument("--output", "-o", help="输出文件路径")
    parser_preview.add_argument("--title", "-t", help="页面标题")
    parser_preview.add_argument("--no-complementary", action="store_true", help="不显示互补色")
    parser_preview.add_argument("--no-contrast", action="store_true", help="不显示对比度")
    parser_preview.set_defaults(func=cmd_preview)

    # recommend
    parser_recommend = subparsers.add_parser("recommend", help="智能颜色推荐")
    parser_recommend.add_argument("description", help="描述（如：科技感蓝色、春天主题）")
    parser_recommend.add_argument("--preview", "-p", action="store_true", help="生成预览")
    parser_recommend.add_argument("--output", "-o", help="预览文件路径")
    parser_recommend.add_argument("--format", "-f", choices=["json", "text"], default="text",
                                  help="输出格式")
    parser_recommend.set_defaults(func=cmd_recommend)

    # random
    parser_random = subparsers.add_parser("random", help="生成随机颜色")
    parser_random.add_argument("--count", "-c", type=int, default=5, help="颜色数量")
    parser_random.add_argument("--preview", "-p", action="store_true", help="生成预览")
    parser_random.set_defaults(func=cmd_random)

    # validate
    parser_validate = subparsers.add_parser("validate", help="验证颜色格式")
    parser_validate.add_argument("color", help="颜色值")
    parser_validate.set_defaults(func=cmd_validate)

    # compare
    parser_compare = subparsers.add_parser("compare", help="比较多个颜色")
    parser_compare.add_argument("colors", nargs="+", help="颜色列表")
    parser_compare.set_defaults(func=cmd_compare)

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
