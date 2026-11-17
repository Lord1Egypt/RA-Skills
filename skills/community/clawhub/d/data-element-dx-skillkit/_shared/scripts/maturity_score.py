"""
DCMM 8 域成熟度评分脚本（演示版）
=================================

用途：dx-data-baseline 跑完摸底后，按 8 域输入 1-5 分，自动汇总：
- 总分（8 域加权）
- 雷达图数据
- 等级判定（初始/受管理/稳健/量化/优化）

输入：CLI 参数或 stdin JSON，格式：
{
  "name": "数据战略",
  "score": 3
}

输出：JSON + 可视化提示。

注：本脚本为骨架示例。生产用请按 DCMM GB/T 36073 标准细化指标权重。
"""

import json
import sys
from typing import Dict


# DCMM 8 域（GB/T 36073）
DOMAINS = [
    "数据战略",
    "数据治理",
    "数据架构",
    "数据应用",
    "数据安全",
    "数据质量",
    "数据标准",
    "数据生命周期",
]

# 权重（默认等权，可按集团侧重点调整）
WEIGHTS = {
    "数据战略": 0.12,
    "数据治理": 0.15,
    "数据架构": 0.15,
    "数据应用": 0.13,
    "数据安全": 0.10,
    "数据质量": 0.15,
    "数据标准": 0.10,
    "数据生命周期": 0.10,
}

LEVEL_MAP = [
    (1.0, 1.5, "初始级（1 级）"),
    (1.5, 2.5, "受管理级（2 级）"),
    (2.5, 3.5, "稳健级（3 级）"),
    (3.5, 4.5, "量化级（4 级）"),
    (4.5, 5.01, "优化级（5 级）"),
]


def judge_level(avg: float) -> str:
    for lo, hi, name in LEVEL_MAP:
        if lo <= avg < hi:
            return name
    return "优化级（5 级）"


def score(scores: Dict[str, float]) -> Dict:
    missing = [d for d in DOMAINS if d not in scores]
    if missing:
        raise ValueError(f"缺少域：{missing}")

    for d, s in scores.items():
        if not (1.0 <= s <= 5.0):
            raise ValueError(f"{d} 分数必须在 1-5 之间，当前 {s}")

    total = sum(scores[d] * WEIGHTS[d] for d in DOMAINS)
    avg = total  # 加权平均
    return {
        "scores": scores,
        "weights": WEIGHTS,
        "weighted_total": round(total, 3),
        "level": judge_level(total),
        "radar": [
            {"domain": d, "value": scores[d]} for d in DOMAINS
        ],
    }


def main():
    if len(sys.argv) > 1:
        # utf-8-sig：兼容 Windows（PowerShell Set-Content 写入的 UTF-8 带 BOM）
        with open(sys.argv[1], "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    result = score(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()