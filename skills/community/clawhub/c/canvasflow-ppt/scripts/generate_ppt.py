#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Magazine PPT Generator - Unified Entry
Author: WuWenBin-BeiJing-ST
Version: 1.0.0

统一入口：支持 HTML 和 PPTX 双格式输出
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# 添加脚本目录到路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from generate_html import generate_full_html, THEMES as HTML_THEMES
from generate_pptx import generate_pptx, THEMES as PPTX_THEMES


def generate_ppt(
    content: str,
    output_format: str = "html",
    theme: str = "ink-classic",
    output_dir: str = "./output",
    outline_data: dict = None,
) -> dict:
    """
    生成 PPT 的统一接口

    Args:
        content: PPT 主题/内容描述
        output_format: 输出格式 (html/pptx/both)
        theme: 主题色名称
        output_dir: 输出目录
        outline_data: 大纲数据（可选）

    Returns:
        包含生成文件路径的字典
    """
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 如果没有提供大纲，生成默认大纲
    if not outline_data:
        outline_data = {
            "title": content,
            "slides": [
                {"layout": "L01", "title": content, "subtitle": "演示文稿"},
                {
                    "layout": "L05",
                    "title": "核心要点",
                    "content": [
                        {"title": "要点一", "description": "第一项核心内容"},
                        {"title": "要点二", "description": "第二项核心内容"},
                        {"title": "要点三", "description": "第三项核心内容"},
                    ],
                },
                {"layout": "L01", "title": "感谢观看"},
            ],
        }

    # 保存大纲
    outline_file = output_path / f"outline_{timestamp}.json"
    with open(outline_file, "w", encoding="utf-8") as f:
        json.dump(outline_data, f, ensure_ascii=False, indent=2)

    results = {"outline": str(outline_file), "html": None, "pptx": None}

    # 生成 HTML
    if output_format in ["html", "both"]:
        html_file = output_path / f"presentation_{timestamp}.html"
        html_path = generate_full_html(outline_data, theme, str(html_file))
        results["html"] = html_path
        print(f"✅ HTML 已生成: {html_path}")

    # 生成 PPTX
    if output_format in ["pptx", "both"]:
        pptx_file = output_path / f"presentation_{timestamp}.pptx"
        pptx_path = generate_pptx(outline_data, theme, str(pptx_file))
        results["pptx"] = pptx_path
        print(f"✅ PPTX 已生成: {pptx_path}")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Magazine PPT 生成器 - 支持 HTML 和 PPTX 双格式"
    )
    parser.add_argument("--content", required=True, help="PPT 主题/内容描述")
    parser.add_argument("--outline", help="大纲 JSON 文件路径")
    parser.add_argument(
        "--output",
        "-o",
        default="html",
        choices=["html", "pptx", "both"],
        help="输出格式 (default: html)",
    )
    parser.add_argument(
        "--theme",
        "-t",
        default="ink-classic",
        choices=list(HTML_THEMES.keys()),
        help="主题色 (default: ink-classic)",
    )
    parser.add_argument(
        "--output-dir", "-d", default="./output", help="输出目录 (default: ./output)"
    )

    args = parser.parse_args()

    # 加载大纲（如果提供）
    outline_data = None
    if args.outline:
        with open(args.outline, "r", encoding="utf-8") as f:
            outline_data = json.load(f)

    # 生成 PPT
    results = generate_ppt(
        content=args.content,
        output_format=args.output,
        theme=args.theme,
        output_dir=args.output_dir,
        outline_data=outline_data,
    )

    # 自动打开（macOS）
    if sys.platform == "darwin":
        if results["html"]:
            os.system(f'open "{results["html"]}"')
        elif results["pptx"]:
            os.system(f'open "{results["pptx"]}"')


if __name__ == "__main__":
    main()
