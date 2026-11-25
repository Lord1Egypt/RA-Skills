#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""B站发布包装体检：标题、封面大字、标签、简介与三连话术。"""

import argparse
import re
import sys


def main():
    parser = argparse.ArgumentParser(description="B站发布包装体检")
    parser.add_argument("--title", action="append", default=[], help="标题，可重复")
    parser.add_argument("--cover-text", action="append", default=[], help="封面大字，可重复")
    parser.add_argument("--tags", default="", help="英文逗号分隔")
    parser.add_argument("--desc", default="", help="简介")
    parser.add_argument("--sanche", default="", help="三连话术")
    args = parser.parse_args()

    errors = []
    warnings = []

    for title in args.title:
        length = len(title.strip())
        if length > 25:
            errors.append(f"标题「{title}」{length} 字，超过 25 字")
        elif length > 20:
            warnings.append(f"标题「{title}」{length} 字，建议压到 20 字内")

    for text in args.cover_text:
        if len(text.strip()) > 12:
            warnings.append(f"封面大字「{text}」{len(text)} 字，建议 ≤10 字")

    tags = [t.strip().lstrip("#") for t in args.tags.split(",") if t.strip()]
    if len(tags) < 3:
        warnings.append(f"标签 {len(tags)} 个，建议 3-5 个")
    elif len(tags) > 8:
        warnings.append(f"标签 {len(tags)} 个，超过 8 个，建议精简")

    desc_length = len(re.sub(r"\s", "", args.desc))
    if desc_length and desc_length < 50:
        warnings.append(f"简介 {desc_length} 字，偏短，建议补结论与时间戳")
    if desc_length > 500:
        warnings.append(f"简介 {desc_length} 字，偏长，建议压到 300 字内")

    if args.sanche:
        if "三连" in args.sanche and not re.search(r"因为|理由|这期|如果|查了|省了|需要", args.sanche):
            warnings.append("三连话术像硬喊，建议补一个具体理由")
        if re.search(r"不三连|白嫖|没动力", args.sanche):
            errors.append("三连话术含情绪绑架，必须重写")

    if re.search(r"最好|最佳|最强|第一|国家级|世界级|100%", " ".join(args.title)):
        warnings.append("标题含绝对化用语，B站虽宽松但会影响可信度")

    print("=== B站发布包装体检 ===")
    if errors:
        print("\n[ERROR] 必须修改：")
        for item in errors:
            print(f"- {item}")
    if warnings:
        print("\n[WARN] 建议修改：")
        for item in warnings:
            print(f"- {item}")
    if not errors and not warnings:
        print("\n[OK] 基础体检通过。")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
