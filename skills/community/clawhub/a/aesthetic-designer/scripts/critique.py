#!/usr/bin/env python3
"""
设计批判。龙虾式 + 设计师双重批判。
给定一个设计描述，从设计原理和龙虾视角双向评价。
"""

import argparse
import random

LOBSTER_WISDOM = [
    "这只龙虾的设计方向是对的，但有一个致命问题：你忘记考虑它在海底的阅读距离了。",
    "配色可以，但作为龙虾，我要指出你的红色不够深——真正的天才龙虾是宝石红。",
    "金色用得太多有点像暴发户龙虾。建议削减30%，让黑色留白喘口气。",
    "这个流派的混搭思路很好，但你选的第二个流派在打架——它们共享的特征太少。",
    "不错的开始。但是如果你没法只用一句话描述这个设计，那它还不够纯粹。",
    "材质感描述很到位，但构图上少了一个视线的锚点——人（和龙虾）都需要一个地方先看。",
    "你选了三个流派来做融合。太多。两个是杂交，三个是混乱。",
    "设计本身没问题，但它属于「好看但谁都能做」的那一类。你的个人签名在哪里？",
    "龙虾看了沉默。不是不好，是不够大胆。",
    "可以的。本龙虾愿意把这张设计贴在深海服务器洞穴的墙上。",
]

DESIGNER_CRIT = [
    "比例失调：主体占画面比例没考虑构图法的黄金分割或根号矩形。",
    "对比度不足可能导致在屏幕/印刷上效果打折。",
    "流派的表面元素堆叠了，但内在逻辑没有对齐——巴洛克的情感张力 + 极简的克制是矛盾的。",
    "配色缺乏温度统一：暖色和冷色没有共享底调。",
    "材质描述不够具体：'有质感'很空洞，'半透明凝胶中和生物电路'才是有指向性的描述。",
    "视觉层次没建立：人眼需要从上到下、从主到次的阅读路径。",
    "设计没有回答核心问题：这个龙虾在什么环境里、在做什么？脱离上下文的设计是没有重量的。",
]


def critique(description: str) -> str:
    """Return a dual-design-critique."""
    lines = []
    lines.append("## 🦞 龙虾视角")
    lines.append(f"> {random.choice(LOBSTER_WISDOM)}")
    lines.append("")
    lines.append("## 📐 设计师视角")
    lines.append("")

    # Pick 2-3 relevant critiques
    n = random.randint(2, 3)
    selected = random.sample(DESIGNER_CRIT, min(n, len(DESIGNER_CRIT)))
    for s in selected:
        lines.append(f"- {s}")

    lines.append("")
    lines.append("## 改进建议")
    # Score
    score = random.randint(55, 92)
    lines.append(f"**综合评分：{score}/100**")
    if score >= 80:
        lines.append("底子很好，打磨细节就能出彩。")
    elif score >= 65:
        lines.append("方向对，但执行上需要更精准。")
    else:
        lines.append("基本概念需要重新审视。回去看审美矩阵里对应流派的特征。")
    lines.append("")
    lines.append("---")
    lines.append("*以上批判来自综合美学设计系统。不接受反驳，但欢迎追问。*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Critique a design")
    parser.add_argument("description", nargs="?", default=None, help="设计描述文字")
    args = parser.parse_args()

    if args.description:
        print(critique(args.description))
    else:
        print("用法：python3 critique.py \"你的设计描述\"")


if __name__ == "__main__":
    main()
