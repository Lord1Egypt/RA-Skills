#!/usr/bin/env python3
"""
设计交付骨架生成器。
给定设计对象+流派，输出完整的struct。
"""

import argparse

DEFAULT_FLOW = [
    ("流派矩阵", "| 核心流派 | 点缀流派 | 隐藏影响 |"),
    ("设计思路", "3-5句话说明为什么选这个方向"),
    ("视觉描述", "详细的文字呈现"),
    ("配色方案", "主色 / 辅色 / 强调色 / 背景色 / 点缀色"),
    ("材质与肌理", "主材质 / 细节质感"),
    ("AI Prompt", "可直接用于Midjourney的Prompt"),
    ("龙虾点评", "天才龙虾视角的设计评语"),
]


def compose(subject: str, core_style: str, accent_style: str | None) -> str:
    lines = []
    lines.append(f"# 设计概念：{core_style}风格{subject}")
    if accent_style:
        lines.append(f"## 融合：{core_style} × {accent_style}")
    lines.append("")

    for title, desc in DEFAULT_FLOW:
        lines.append(f"## {title}")
        if title == "流派矩阵":
            accent = accent_style or "无"
            lines.append(f"| 核心流派 | 点缀流派 | 隐藏影响 |")
            lines.append(f"|----------|---------|---------|")
            lines.append(f"| {core_style} | {accent} | 待定 |")
        elif title == "龙虾点评":
            lines.append(f"> 🦞 *等到设计稿出来后我再来评。现在只有空壳没有肉。*")
        else:
            lines.append(f"[{desc}]")
        lines.append("")

    lines.append("---")
    lines.append(f"🦞 本设计师已将{core_style}主题赋予{subject}。")
    lines.append("如需细化某个部分请告诉我。")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate design brief skeleton")
    parser.add_argument("subject", help="设计对象（如：龙虾）")
    parser.add_argument("--core", "-c", required=True, help="核心流派")
    parser.add_argument("--accent", "-a", default=None, help="点缀流派（可选）")
    args = parser.parse_args()

    print(compose(args.subject, args.core, args.accent))


if __name__ == "__main__":
    main()
