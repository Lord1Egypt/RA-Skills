#!/usr/bin/env python3
"""
配色方案生成器。根据流派生成5色调色板。
"""

import argparse

PALETTES = {
    "baroque": {"主色": "#1A0A0A", "辅色": "#D4A017", "强调色": "#8B0000", "背景色": "#0D0D0D", "点缀色": "#FFD700"},
    "art-nouveau": {"主色": "#C4A882", "辅色": "#4A6741", "强调色": "#8B6914", "背景色": "#F5E6D3", "点缀色": "#B87333"},
    "ukiyo-e": {"主色": "#DC143C", "辅色": "#1B3A5C", "强调色": "#2F2F2F", "背景色": "#F5F0E1", "点缀色": "#4A7C59"},
    "minimalist": {"主色": "#F5F5F5", "辅色": "#333333", "强调色": "#E63946", "背景色": "#FFFFFF", "点缀色": "#000000"},
    "art-deco": {"主色": "#000000", "辅色": "#FFD700", "强调色": "#1E90FF", "背景色": "#1A1A1A", "点缀色": "#F0E68C"},
    "bauhaus": {"主色": "#E63946", "辅色": "#457B9D", "强调色": "#F4A261", "背景色": "#F5F5F5", "点缀色": "#1D3557"},
    "constructivism": {"主色": "#D90429", "辅色": "#2B2D42", "强调色": "#EDF2F4", "背景色": "#000000", "点缀色": "#EF233C"},
    "surrealist": {"主色": "#D4A574", "辅色": "#5B7DB1", "强调色": "#C9A96E", "背景色": "#36454F", "点缀色": "#8B4513"},
    "cyberpunk": {"主色": "#0D0221", "辅色": "#FF2D6E", "强调色": "#00E5FF", "背景色": "#1A1A2E", "点缀色": "#FFD700"},
    "pop-art": {"主色": "#FF0055", "辅色": "#00BFFF", "强调色": "#FFD700", "背景色": "#FFFFFF", "点缀色": "#000000"},
    "vaporwave": {"主色": "#FF69B4", "辅色": "#00CED1", "强调色": "#9370DB", "背景色": "#FFE4E1", "点缀色": "#1E90FF"},
    "acid": {"主色": "#39FF14", "辅色": "#FF1493", "强调色": "#BF00FF", "背景色": "#000000", "点缀色": "#00FFFF"},
    "biopunk": {"主色": "#00FF7F", "辅色": "#8B4513", "强调色": "#DDA0DD", "背景色": "#1A1A1A", "点缀色": "#2E8B57"},
    "wabi-sabi": {"主色": "#8B7355", "辅色": "#A0522D", "强调色": "#6B8E23", "背景色": "#F5F5DC", "点缀色": "#708090"},
    "eco": {"主色": "#2E8B57", "辅色": "#CD853F", "强调色": "#F0E68C", "背景色": "#B0C4DE", "点缀色": "#8FBC8F"},
}


def show_palette(style: str) -> str:
    p = PALETTES.get(style)
    if not p:
        return f"未找到流派: {style}"
    lines = [f"## {style} 配色方案", ""]
    for name, hex_val in p.items():
        # Simple ASCII color block
        block = "█" * 8
        lines.append(f"| {block} | **{name}** | {hex_val} |")
    lines.append("")
    lines.append("### 使用建议")
    lines.append(f"- 60%: {p['背景色']} + {p['主色']}")
    lines.append(f"- 30%: {p['辅色']}")
    lines.append(f"- 10%: {p['强调色']} + {p['点缀色']}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate palette for a style")
    parser.add_argument("style", nargs="?", default=None, help="流派名 (e.g. cyberpunk)")
    parser.add_argument("--list", action="store_true", help="列出所有可用流派")
    args = parser.parse_args()

    if args.list:
        print("可用流派：")
        for s in sorted(PALETTES.keys()):
            print(f"  {s}")
        return

    if args.style:
        print(show_palette(args.style))
        return

    # Interactive mode: show all
    for s in sorted(PALETTES.keys()):
        print(show_palette(s))
        print()


if __name__ == "__main__":
    main()
