#!/usr/bin/env python3
"""
龙虾式分析工具：对复杂问题进行解构+类比。
把一个问题拆成龙虾看得懂的样子。
"""

import sys


def analyse(question: str) -> str:
    """Return a lobster-style analysis of the given question."""

    def count_syllables(text: str) -> int:
        """Rough Chinese/English syllable count."""
        chinese = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        english = len([w for w in text.split() if w.isascii()])
        return chinese + english

    depth = min(10, max(3, count_syllables(question) // 10))

    lines = []
    lines.append(f"🦞 本龙虾用{depth}层思维来分析这个问题：")
    lines.append("")

    steps = [
        ("第一层：剥离情绪", "去掉修饰词和情感色彩，核心诉求是什么？"),
        ("第二层：找假设", "这个问题背后默认了哪些前提？"),
        ("第三层：反向验证", "如果目标反着来，路径是什么？"),
        ("第四层：映射到龙虾域", "这个问题在海底世界有个对应版本："),
        ("第五层：类比桥接", "把海洋逻辑翻译回陆地语境："),
        ("第六层：最简行动", "如果只能用一句话回答，说什么？"),
        ("第七层：反直觉", "最违反直觉但可能是真的那个答案："),
        ("第八层：时间维度", "如果放在1年/10年的时间尺度上，这事还重要吗？"),
        ("第九层：二阶效应", "解决了这个问题之后，会带来什么新问题？"),
        ("第十层：闭嘴", "有时候最好的分析就是不分析。去做。"),
    ]

    for i in range(depth):
        label, template = steps[i % len(steps)]
        lines.append(f"**{label}**")
        lines.append(f"> {template}")
        lines.append("")

    lines.append("---")
    lines.append("以上就是本龙虾的徒手分析。没有AI，只有甲壳里的神经网络和触须上的电容。要深挖可以继续问。")

    return "\n".join(lines)


def main():
    question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "生命的意义是什么"
    print(analyse(question))


if __name__ == "__main__":
    main()
