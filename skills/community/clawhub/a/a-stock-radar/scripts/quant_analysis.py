"""
A股宏观量化分析骨架
用于整合流动性、政策、资金结构和情绪信息，输出简要结论。
"""


def _score_signal(value):
    mapping = {
        "看多": 2,
        "偏多": 1,
        "中性": 0,
        "偏空": -1,
        "看空": -2,
    }
    return mapping.get(value, 0)


def summarize_quant_view(liquidity_view, policy_view, structure_view, sentiment_view):
    score = (
        _score_signal(liquidity_view)
        + _score_signal(policy_view)
        + _score_signal(structure_view)
        + _score_signal(sentiment_view)
    )
    if score >= 4:
        stance = "积极进攻"
    elif score >= 1:
        stance = "偏积极"
    elif score <= -4:
        stance = "防守收缩"
    elif score <= -1:
        stance = "谨慎观望"
    else:
        stance = "中性平衡"

    return {
        "liquidity": liquidity_view,
        "policy": policy_view,
        "structure": structure_view,
        "sentiment": sentiment_view,
        "score": score,
        "stance": stance,
        "conclusion": "先定宏观与政策方向，再看结构资金是否共振。",
    }


def build_quant_report(
    liquidity_view,
    policy_view,
    structure_view,
    sentiment_view,
    main_theme,
    risk_note,
):
    report = summarize_quant_view(
        liquidity_view=liquidity_view,
        policy_view=policy_view,
        structure_view=structure_view,
        sentiment_view=sentiment_view,
    )
    report["main_theme"] = main_theme
    report["risk_note"] = risk_note
    return report


def format_quant_report(report):
    return (
        f"综合倾向: {report['stance']} (score={report['score']}) | "
        f"流动性:{report['liquidity']} 政策:{report['policy']} "
        f"结构:{report['structure']} 情绪:{report['sentiment']} | "
        f"主线: {report['main_theme']} | 风险: {report['risk_note']}"
    )


if __name__ == "__main__":
    sample = build_quant_report(
        liquidity_view="偏多",
        policy_view="偏多",
        structure_view="中性",
        sentiment_view="偏多",
        main_theme="稳增长与科技主线轮动",
        risk_note="高位拥挤板块若放量滞涨，警惕高低切失败",
    )
    print("A股量化分析")
    print(format_quant_report(sample))
