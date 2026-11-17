#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
博主数据准备与快速转换辅助工具 (Data Preparation & Format Helper)
- 支持从纯文本列表、Markdown、剪贴板文本快速解析并生成标准博主 JSON
- 智能提取序号、博主名称、粉丝量 (如 100w、50万)、子分类
- 支持校验现有博主 JSON 文件的格式完整性
"""

import os
import sys
import re
import json
import argparse
from typing import List, Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from storage import infer_industry


def parse_raw_text(text: str, default_industry: str = "", default_category: str = "默认") -> List[Dict]:
    """
    智能解析自由格式文本（支持换行、逗号、顿号、编号列表等）
    例如：
    1. 极客湾Geekerwan - 数码硬件 (350万粉)
    2. 影视飓风 - 影视后期 500w
    3. 差评君
    """
    lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
    if not lines:
        return []

    # 如果只有单行且包含逗号/顿号/空格，尝试按分隔符拆分
    if len(lines) == 1:
        single_line = lines[0]
        if "," in single_line or "，" in single_line or "、" in single_line:
            parts = re.split(r"[,，、]+", single_line)
            lines = [p.strip() for p in parts if p.strip()]

    results = []
    fans_pattern = re.compile(r"(\d+(?:\.\d+)?\s*(?:[wW万kK]|万粉|粉丝)?)")

    for idx, raw_line in enumerate(lines, 1):
        # 1. 过滤开头的序号 (例如 "1.", "1、", "[1]", "一、", "- ")
        cleaned = re.sub(r"^[\d一二三四五六七八九十]+[\.、\s\-\–\]\)]+", "", raw_line).strip()
        cleaned = re.sub(r"^[\-\*\•]\s*", "", cleaned).strip()

        if not cleaned:
            continue

        fans = ""
        category = default_category
        name = cleaned

        # 2. 提取括号中的备注 (粉丝数或子分类)
        bracket_match = re.search(r"[\(（\[【](.*?)[\)）\]】]", cleaned)
        if bracket_match:
            bracket_content = bracket_match.group(1).strip()
            name = cleaned.replace(bracket_match.group(0), "").strip()
            # 检查括号内是否是粉丝数
            if any(k in bracket_content for k in ["万", "w", "W", "粉", "获赞", "k", "K"]):
                fans = bracket_content
            else:
                category = bracket_content

        # 3. 提取连字符分隔的内容 (例如: "博主名 - 分类/粉丝")
        if " - " in name or " -- " in name or " ｜ " in name or " | " in name:
            parts = re.split(r"\s*[-–—|｜]+\s*", name)
            if len(parts) >= 2:
                name = parts[0].strip()
                extra = parts[1].strip()
                if any(k in extra for k in ["万", "w", "W", "粉", "获赞"]):
                    fans = extra
                else:
                    category = extra

        # 4. 如果单独匹配到粉丝数
        if not fans:
            fans_matches = fans_pattern.findall(name)
            if fans_matches:
                for fm in fans_matches:
                    if any(k in fm for k in ["万", "w", "W", "粉"]):
                        fans = fm
                        name = name.replace(fm, "").strip()
                        break

        # 清洗最终博主名
        name = name.strip(" ,，、:：-")
        if not name:
            continue

        industry = default_industry if default_industry else infer_industry(name, category, "")

        results.append({
            "id": len(results) + 1,
            "name": name,
            "industry": industry,
            "category": category,
            "fans": fans
        })

    return results


def validate_json_file(file_path: str) -> bool:
    """校验已有 JSON 文件是否符合博主列表格式规范"""
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            print(f"❌ 格式错误: JSON 根节点必须为数组 (List)。")
            return False

        print(f"✅ 校验通过！共包含 {len(data)} 位博主。")
        for i, item in enumerate(data[:5], 1):
            print(f"   [{i}] 名称: {item.get('name')} | 行业: {item.get('industry', '未指定')} | 分类: {item.get('category', '默认')}")
        if len(data) > 5:
            print(f"   ... (剩余 {len(data) - 5} 位)")
        return True
    except Exception as e:
        print(f"❌ JSON 解析失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="博主数据准备与快速转换辅助工具")
    parser.add_argument("-t", "--text", type=str, default="",
                        help="直接传入博主名称文本 (支持逗号、换行分隔)")
    parser.add_argument("-i", "--input-file", type=str, default="",
                        help="输入的纯文本/名单文件路径")
    parser.add_argument("-o", "--output-file", type=str, default="",
                        help="输出的 JSON 文件路径 (默认保存至 examples/custom_bloggers.json)")
    parser.add_argument("--industry", type=str, default="",
                        help="指定默认行业大类")
    parser.add_argument("--category", type=str, default="默认",
                        help="指定默认细分子类")
    parser.add_argument("-v", "--validate", type=str, default="",
                        help="校验指定的 JSON 文件格式")

    args = parser.parse_args()

    # 1. 校验文件模式
    if args.validate:
        validate_json_file(args.validate)
        return

    # 2. 文本解析转换模式
    raw_content = ""
    if args.text.strip():
        raw_content = args.text.strip()
    elif args.input_file:
        if not os.path.exists(args.input_file):
            print(f"❌ 输入文件不存在: {args.input_file}")
            sys.exit(1)
        with open(args.input_file, "r", encoding="utf-8") as f:
            raw_content = f.read()
    else:
        print("💡 请输入或粘贴博主清单（支持多行或以逗号分隔，输入完成后按 Ctrl+D 或单独一行输入 EOF 结束）：\n")
        lines = []
        try:
            while True:
                line = input()
                if line.strip() == "EOF":
                    break
                lines.append(line)
        except EOFError:
            pass
        raw_content = "\n".join(lines)

    if not raw_content.strip():
        print("❌ 未检测到任何博主输入文本。")
        sys.exit(1)

    parsed = parse_raw_text(raw_content, default_industry=args.industry, default_category=args.category)
    if not parsed:
        print("❌ 未能解析出有效的博主列表。")
        sys.exit(1)

    # 确定输出路径
    out_path = args.output_file.strip()
    if not out_path:
        out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "examples", "custom_bloggers.json")

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(parsed, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 64)
    print(f"🎉 成功解析并生成 {len(parsed)} 位博主数据！")
    print(f"💾 输出文件: {out_path}")
    print("=" * 64)
    print("\n📋 数据预览 (前 5 位):")
    for b in parsed[:5]:
        print(f"   - ID: {b['id']} | 【{b['name']}】 | 行业: {b['industry']} | 分类: {b['category']} | 粉丝: {b['fans'] or '未知'}")
    if len(parsed) > 5:
        print(f"   ... (共 {len(parsed)} 位)")

    print(f"\n🚀 接下来您可以直接运行批量关注:")
    print(f"   python3 scripts/blogger_auto_follow.py -p douyin -f {out_path}\n")


if __name__ == "__main__":
    main()
