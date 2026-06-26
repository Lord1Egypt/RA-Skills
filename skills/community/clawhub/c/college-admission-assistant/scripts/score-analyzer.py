#!/usr/bin/env python3
"""
分数分析和志愿梯度计算工具
使用方式：由AI智能体在需要分数分析时调用
"""

import sys
import json
from typing import Dict, List, Optional

# 参考分数线数据（全国通用参考）
SCORE_BANDS = {
    "physics": {  # 物理类
        "top": {"min": 680, "label": "C9院校", "detail": "北大/清华/复旦/上交/浙大"},
        "high_985": {"min": 650, "max": 679, "label": "中上游985", "detail": ""},
        "mid_985": {"min": 620, "max": 649, "label": "中下游985/头部211", "detail": ""},
        "high_211": {"min": 590, "max": 619, "label": "中上游211", "detail": ""},
        "mid_211": {"min": 560, "max": 589, "label": "中游211/双一流", "detail": ""},
        "first_uni": {"min": 530, "max": 559, "label": "普通一本", "detail": ""},
        "second_uni": {"min": 500, "max": 529, "label": "公办二本", "detail": ""},
        "third_uni": {"min": 450, "max": 499, "label": "民办本科/独立学院", "detail": ""},
    },
    "history": {  # 历史类
        "top": {"min": 650, "label": "C9院校", "detail": "北大/清华/复旦/上交/浙大"},
        "high_985": {"min": 620, "max": 649, "label": "中上游985", "detail": ""},
        "mid_985": {"min": 590, "max": 619, "label": "中下游985/头部211", "detail": ""},
        "high_211": {"min": 560, "max": 589, "label": "中上游211", "detail": ""},
        "mid_211": {"min": 530, "max": 559, "label": "中游211/双一流", "detail": ""},
        "first_uni": {"min": 500, "max": 529, "label": "普通一本", "detail": ""},
        "second_uni": {"min": 470, "max": 499, "label": "公办二本", "detail": ""},
        "third_uni": {"min": 430, "max": 469, "label": "民办本科", "detail": ""},
    },
}


def analyze_score(score: int, category: str = "physics") -> Dict:
    """
    根据分数分析适合的院校层次

    Args:
        score: 高考分数（750总分）
        category: "physics" 或 "history"
    
    Returns:
        分析结果字典
    """
    bands = SCORE_BANDS.get(category, SCORE_BANDS["physics"])
    
    for key, band in bands.items():
        if score >= band.get("min", 0):
            if "max" in band and score > band["max"]:
                continue
            return {
                "category": category,
                "score": score,
                "matched_band": key,
                "label": band["label"],
                "detail": band.get("detail", ""),
            }
    
    return {
        "category": category,
        "score": score,
        "matched_band": "below_line",
        "label": "本科线以下，建议考虑专科（高职高专）",
        "detail": "",
    }


def suggest_volunteer_gradient(score: int, category: str = "physics") -> Dict:
    """
    建议冲稳保志愿梯度

    推荐：30%冲刺 + 50%稳妥 + 20%保底
    """
    result = analyze_score(score, category)
    band_min = 0
    band_max = 0

    bands = SCORE_BANDS.get(category, SCORE_BANDS["physics"])
    for key, band in bands.items():
        if key == result["matched_band"]:
            band_min = band.get("min", 0)
            band_max = band.get("max", 0)
            break

    return {
        "strategy": "30%冲刺 + 50%稳妥 + 20%保底",
        "sprint": {  # 冲刺
            "range": f"{score+5}-{score+20}分",
            "ratio": "30%",
            "advice": "选择略高于自身水平的院校/专业组"
        },
        "stable": {  # 稳妥
            "range": f"{score-5}-{score+5}分",
            "ratio": "50%",
            "advice": "选择与自身水平相当的院校/专业组"
        },
        "safe": {  # 保底
            "range": f"{score-20}-{score-5}分",
            "ratio": "20%",
            "advice": "选择录取概率大的院校/专业组"
        },
        "disclaimer": "以上为一般性参考，具体到各省份差异较大，请结合省教育考试院官方数据填报"
    }


def estimate_equivalent_score(score: int, from_year: int, to_year: int, 
                               province: str, category: str = "physics") -> Dict:
    """
    估算等效分（不同年份之间的分数换算）

    简化的批处理算法：
    等效分 = 目标年分数 + (目标年批次线 - 来源年批次线)
    
    Args:
        score: 来源年份的分数
        from_year: 来源年份
        to_year: 目标年份
        province: 省份名称
        category: 物理类或历史类
    """
    # 注：实际使用时应传入各省历年的批次线数据
    # 这里提供计算框架
    return {
        "from_year": from_year,
        "to_year": to_year,
        "original_score": score,
        "note": "等效分计算需要接入各省历年批次线数据。请配置商用API以获得精确计算。",
        "method": "批次线差值法：等效分 = 目标年分数 + (目标年批次线 - 来源年批次线)",
    }


if __name__ == "__main__":
    # CLI 使用方式
    if len(sys.argv) < 2:
        print("使用: python score-analyzer.py <分数> [物理类/历史类]")
        print("示例: python score-analyzer.py 580 physics")
        sys.exit(1)
    
    score = int(sys.argv[1])
    category = sys.argv[2] if len(sys.argv) > 2 else "physics"
    
    result = analyze_score(score, category)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    gradient = suggest_volunteer_gradient(score, category)
    print("\n--- 志愿梯度建议 ---")
    print(json.dumps(gradient, ensure_ascii=False, indent=2))
