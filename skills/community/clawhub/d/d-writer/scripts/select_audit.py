#!/usr/bin/env python3
"""select_audit — 根据体裁和章节标签选择激活的审计维度。

输入 genre、chapter tags、fanfic mode、chapter length 和 risk flags。
输出激活维度、severity、激活原因、缺失输入和跳过原因。
未知题材使用安全默认清单。尽量只依赖 Python 标准库。
"""

import argparse
import json
import sys
from typing import Dict, List, Optional


# 体裁裁剪矩阵（与 audit-dimensions.md 同步）
GENRE_MATRIX: Dict[str, dict] = {
    "仙侠": {
        "enabled": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 21, 22, 25, 26, 27, 32, 33, 38, 39, 40, 41, 42, 43],
        "severity_overrides": {38: "critical", 39: "critical"},
        "activation_reason": "体裁默认 + 架空前提(12)",
    },
    "修真": {
        "enabled": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 21, 22, 25, 26, 27, 32, 33, 38, 39, 40, 41, 42, 43],
        "severity_overrides": {38: "critical", 39: "critical"},
        "activation_reason": "体裁默认 + 架空前提(12)",
    },
    "升级流": {
        "enabled": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 21, 22, 25, 26, 27, 32, 33, 38, 39, 40, 41, 42, 43],
        "severity_overrides": {38: "critical", 39: "critical"},
        "activation_reason": "体裁默认 + 架空前提(12)",
    },
    "现代": {
        "enabled": [1, 2, 3, 7, 8, 9, 10, 11, 13, 14, 16, 17, 18, 19, 21, 22, 25, 26, 27, 32, 33, 38, 39, 40, 41, 42, 43],
        "severity_overrides": {39: "critical", 40: "critical", 41: "critical"},
        "activation_reason": "体裁默认",
    },
    "都市": {
        "enabled": [1, 2, 3, 7, 8, 9, 10, 11, 13, 14, 16, 17, 18, 19, 21, 22, 25, 26, 27, 32, 33, 38, 39, 40, 41, 42, 43],
        "severity_overrides": {39: "critical", 40: "critical", 41: "critical"},
        "activation_reason": "体裁默认",
    },
    "日常": {
        "enabled": [1, 2, 3, 7, 8, 9, 10, 11, 13, 14, 16, 17, 18, 19, 21, 22, 25, 26, 27, 32, 33, 38, 39, 40, 41, 42, 43],
        "severity_overrides": {39: "critical", 40: "critical", 41: "critical"},
        "activation_reason": "体裁默认",
    },
}

# 同人模式矩阵
FANFIC_MATRIX: Dict[str, dict] = {
    "canon": {
        "enabled": [1, 2, 3, 6, 7, 8, 9, 10, 16, 17, 19, 21, 22, 25, 26, 27, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43],
        "severity_overrides": {1: "critical", 34: "critical", 35: "critical", 37: "critical"},
        "activation_reason": "同人 canon 模式",
    },
    "ooc": {
        "enabled": [1, 2, 3, 6, 7, 8, 9, 10, 16, 17, 19, 21, 22, 25, 26, 27, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43],
        "severity_overrides": {1: "info", 34: "info", 35: "warning", 36: "warning", 37: "info", 40: "critical", 41: "critical"},
        "activation_reason": "同人 OOC 模式",
    },
    "cp": {
        "enabled": [1, 2, 3, 6, 7, 8, 9, 10, 16, 17, 19, 21, 22, 25, 26, 27, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43],
        "severity_overrides": {1: "warning", 34: "warning", 35: "warning", 36: "critical", 37: "info"},
        "activation_reason": "同人 CP 模式",
    },
    "au": {
        "enabled": [1, 2, 3, 6, 7, 8, 9, 10, 16, 17, 19, 21, 22, 25, 26, 27, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43],
        "severity_overrides": {1: "warning", 34: "critical", 35: "info", 36: "warning", 37: "info"},
        "activation_reason": "同人 AU 模式",
    },
}

# 始终激活的维度（体裁无关 critical）
ALWAYS_ENABLED = [27, 32, 33, 42, 43]

# 章节标签激活的维度
TAG_ACTIVATIONS = {
    "空间": [38],
    "战斗": [4, 38],
    "道具": [39],
    "感情": [36],
    "同人": [34, 35, 36, 37],
    "时代": [12],
    "穿越": [29],
    "重生": [29],
    "番外": [28, 29, 30, 31],
}

# 维度名称映射
DIMENSION_NAMES = {
    1: "OOC 检查", 2: "时间线检查", 3: "设定冲突", 4: "战力崩坏", 5: "数值检查",
    6: "伏笔检查", 7: "节奏检查", 8: "文风检查", 9: "信息越界", 10: "词汇疲劳",
    11: "利益链断裂", 12: "年代考据", 13: "配角降智", 14: "配角工具人化",
    15: "爽点虚化", 16: "台词失真", 17: "流水账", 18: "知识库污染",
    19: "视角一致性", 20: "段落等长", 21: "套话密度", 22: "公式化转折",
    23: "列表式结构", 24: "支线停滞", 25: "弧线平坦", 26: "节奏单调",
    27: "敏感词检查", 28: "正传事件冲突", 29: "未来信息泄露", 30: "世界规则跨书一致性",
    31: "番外伏笔隔离", 32: "读者期待管理", 33: "章节备忘偏离", 34: "角色还原度",
    35: "世界规则遵守", 36: "关系动态", 37: "正典事件一致性", 38: "空间一致性",
    39: "道具追踪", 40: "服装外貌与随身物件", 41: "常识检查",
    42: "跨章重复检测", 43: "去 AI 味检查",
}


def select_audit(genre: str, chapter_tags: Optional[List[str]] = None,
                 fanfic_mode: Optional[str] = None, chapter_length: int = 3000,
                 risk_flags: Optional[List[str]] = None) -> dict:
    """选择激活的审计维度。"""
    chapter_tags = chapter_tags or []
    risk_flags = risk_flags or []

    # 确定基础清单
    if fanfic_mode and fanfic_mode in FANFIC_MATRIX:
        matrix = FANFIC_MATRIX[fanfic_mode]
        enabled = set(matrix["enabled"])
        severity_overrides = dict(matrix["severity_overrides"])
        activation_reasons = {d: matrix["activation_reason"] for d in enabled}
    elif genre in GENRE_MATRIX:
        matrix = GENRE_MATRIX[genre]
        enabled = set(matrix["enabled"])
        severity_overrides = dict(matrix["severity_overrides"])
        activation_reasons = {d: matrix["activation_reason"] for d in enabled}
    else:
        # 未知题材使用安全默认清单
        enabled = set(ALWAYS_ENABLED + [1, 2, 3, 6, 7, 9])
        severity_overrides = {}
        activation_reasons = {d: "未知题材默认策略" for d in enabled}

    # 始终激活
    for d in ALWAYS_ENABLED:
        if d not in enabled:
            enabled.add(d)
            activation_reasons[d] = "始终激活"

    # 章节标签激活
    for tag in chapter_tags:
        for d in TAG_ACTIVATIONS.get(tag, []):
            if d not in enabled:
                enabled.add(d)
                activation_reasons[d] = f"章节标签：{tag}"

    # 短篇裁剪
    skipped = {}
    if chapter_length < 3000:
        # 短篇可跳过 info 级维度
        for d in list(enabled):
            if d in (20, 23, 10, 21) and d not in ALWAYS_ENABLED:
                skipped[d] = "短篇（<3000 字）跳过 info 级"

    # 构建结果
    dimensions = []
    for d in sorted(enabled):
        if d in skipped:
            continue
        dimensions.append({
            "dimension": d,
            "name": DIMENSION_NAMES.get(d, f"维度 {d}"),
            "severity": severity_overrides.get(d, "warning"),
            "activation_reason": activation_reasons.get(d, "默认激活"),
        })

    # 缺失输入
    missing_inputs = []
    if not genre:
        missing_inputs.append("genre（题材）")

    return {
        "genre": genre,
        "fanfic_mode": fanfic_mode,
        "chapter_tags": chapter_tags,
        "chapter_length": chapter_length,
        "activated_count": len(dimensions),
        "dimensions": dimensions,
        "skipped": [{"dimension": d, "name": DIMENSION_NAMES.get(d, f"维度 {d}"), "reason": r}
                     for d, r in skipped.items()],
        "missing_inputs": missing_inputs,
    }


def main():
    parser = argparse.ArgumentParser(description="选择激活的审计维度")
    parser.add_argument("--genre", default="", help="题材")
    parser.add_argument("--tags", nargs="*", default=[], help="章节标签")
    parser.add_argument("--fanfic-mode", choices=["canon", "ooc", "cp", "au"], help="同人模式")
    parser.add_argument("--chapter-length", type=int, default=3000, help="章节字数")
    parser.add_argument("--risk-flags", nargs="*", default=[], help="风险标记")
    parser.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    args = parser.parse_args()

    result = select_audit(
        genre=args.genre,
        chapter_tags=args.tags,
        fanfic_mode=args.fanfic_mode,
        chapter_length=args.chapter_length,
        risk_flags=args.risk_flags,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"激活维度（共 {result['activated_count']} 维）：")
        for d in result["dimensions"]:
            print(f"  [{d['dimension']:2d}] {d['name']} ({d['severity']}) — {d['activation_reason']}")
        if result.get("skipped"):
            print(f"\n跳过维度（{len(result['skipped'])} 维）：")
            for s in result["skipped"]:
                print(f"  [{s['dimension']:2d}] {s['name']} — {s['reason']}")
        if result.get("missing_inputs"):
            print(f"\n缺失输入：{', '.join(result['missing_inputs'])}")


if __name__ == "__main__":
    main()
