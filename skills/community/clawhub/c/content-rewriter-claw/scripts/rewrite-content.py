#!/usr/bin/env python3
"""
content-rewriter-claw: 内容改写主程序
用法：
  python3 rewrite-content.py --input "原文内容" --depth deep --style "轻松幽默" --platform xiaohongshu
  python3 rewrite-content.py --input-file content.txt --depth medium
"""

import argparse
import sys
import json

def parse_args():
    parser = argparse.ArgumentParser(description="内容改写工具")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input", type=str, help="原文内容（直接输入）")
    group.add_argument("--input-file", type=str, help="原文文件路径")
    parser.add_argument("--depth", choices=["shallow", "medium", "deep", "full"],
                        default="medium", help="改写深度")
    parser.add_argument("--style", type=str, default="", help="目标风格描述")
    parser.add_argument("--platform", type=str, default="",
                        help="目标平台（douyin/xiaohongshu/wechat/bilibili）")
    parser.add_argument("--keep", type=str, default="", help="必须保留的要素（逗号分隔）")
    parser.add_argument("--avoid", type=str, default="", help="需要规避的要素（逗号分隔）")
    parser.add_argument("--output", type=str, default="", help="输出文件路径（不填则打印到stdout）")
    return parser.parse_args()

def build_prompt(content: str, depth: str, style: str, platform: str, keep: str, avoid: str) -> str:
    depth_map = {
        "shallow": "浅层改写：同义词替换、句式调整，保留原有结构",
        "medium": "中层改写：段落重组、案例替换、表达方式转换",
        "deep": "深度重构：角度转换、逻辑重建、情绪基调调整、人称视角转换",
        "full": "完全原创：仅保留核心观点，全新创作",
    }

    prompt_parts = [
        f"请对以下内容进行改写。",
        f"\n改写深度：{depth_map[depth]}",
    ]
    if style:
        prompt_parts.append(f"目标风格：{style}")
    if platform:
        prompt_parts.append(f"目标平台：{platform}（请适配该平台的内容规范和用户习惯）")
    if keep:
        prompt_parts.append(f"必须保留：{keep}")
    if avoid:
        prompt_parts.append(f"需要规避：{avoid}")

    prompt_parts.append("\n改写要求：")
    prompt_parts.append("1. 保留爆款基因（钩子类型、情绪触发点、传播结构）")
    prompt_parts.append("2. 确保原创性，目标重复率 < 10%")
    prompt_parts.append("3. 输出格式：先输出改写后的内容，再输出一段简短的改写说明（说明做了哪些改动）")
    prompt_parts.append(f"\n原文：\n{content}")

    return "\n".join(prompt_parts)

def main():
    args = parse_args()

    # 读取原文
    if args.input:
        content = args.input
    else:
        try:
            with open(args.input_file, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            print(f"错误：找不到文件 {args.input_file}", file=sys.stderr)
            sys.exit(1)

    if not content.strip():
        print("错误：原文内容为空", file=sys.stderr)
        sys.exit(1)

    prompt = build_prompt(
        content=content,
        depth=args.depth,
        style=args.style,
        platform=args.platform,
        keep=args.keep,
        avoid=args.avoid,
    )

    # 输出结构化 prompt 供 AI agent 使用
    result = {
        "action": "rewrite",
        "depth": args.depth,
        "style": args.style,
        "platform": args.platform,
        "keep": args.keep,
        "avoid": args.avoid,
        "original_length": len(content),
        "prompt": prompt,
    }

    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"已输出到 {args.output}")
    else:
        print(output)

if __name__ == "__main__":
    main()
