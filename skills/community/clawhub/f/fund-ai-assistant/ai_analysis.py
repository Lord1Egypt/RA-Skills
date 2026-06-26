"""
AI 量化分析模块
调用统一 LLM 接口（详见 llm.py）
支持深度多维量化分析 + 明确操作指引
宏观局势数据：通过 macro_fetcher 获取并注入 prompt
"""
import json
import os

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))


from llm import get_llm_config, call_llm


FUND_ANALYSIS_PROMPT = """你是一位资深基金量化分析师，拥有10年以上公募基金研究经验。请对基金 {fund_name}（代码：{fund_code}）进行**深度量化分析**，给出专业、明确、可操作的投资建议。

**输出要求：所有字段必须有实质内容，不要给出无意义的占位符。每个字段的输出长度不得少于对应字数要求（10字以内不得改为"无"或"—"）。**

## 【基金基本信息】
- 最新净值：{latest_nav:.4f}
- 日涨跌：{est_change:+.2f}%
- 最新日期：{latest_date}

## 【移动均线】
- MA5={ma5}  MA10={ma10}  MA20={ma20}  MA60={ma60}
- 价格vsMA5：{price_ma5_dist:.2f}%  MA5vsMA20：{ma5_ma20_cross:.2f}%

## 【技术指标】
- RSI(14)={rsi}（>70超买,<30超卖）
- MACD：DIF={macd_dif}  DEA={macd_dea}  MACD柱={macd_hist}
- KDJ：K={kdj_k}  D={kdj_d}  J={kdj_j}
- 布林带：上={boll_upper}  中={boll_middle}  下={boll_lower}  位置={boll_position}%

## 【风险收益】
- 波动率={volatility}%  最大回撤={max_drawdown}%  夏普={sharpe}

## 【阶段收益】
- 近1周={return_1w}%  近1月={return_1m}%  近3月={return_3m}%  近6月={return_6m}%  近1年={return_1y}%

## 【历史位置】
- 52周高回撤={from_52w_high}%  252日区间={price_percentile}%分位
- 252日高={price_252w_high}  低={price_252w_low}

{position_section}

{scene_section}

{macro_section}

---

请输出**完整** JSON（所有字段必填，博弈论放在同一结构最后）：

```json
{{
  "综合评分": {{
    "总分": <0-100>,
    "技术面得分": <0-100>,
    "风险得分": <0-100>,
    "收益得分": <0-100>,
    "综合评级": "<极强|强劲|良好|中性|偏弱|弱势>",
    "评分解读": "<20-40字，详细说明评分的核心依据及当前市场逻辑>"
  }},
  "技术面综合判断": {{
    "短期趋势": "<上升|下降|震荡偏强|震荡偏弱|震荡>",
    "中期趋势": "<同上>",
    "长期趋势": "<同上>",
    "MACD信号": "<金叉|死叉|底背离|顶背离|中性>",
    "KDJ信号": "<超买|超卖|金叉区域|死叉区域|中性>",
    "RSI信号": "<超买区|超卖区|中性>",
    "布林带信号": "<上轨附近|下轨附近|中轨上方|中轨下方|通道中部>",
    "均线系统": "<多头排列|空头排列|交织状态>",
    "综合结论": "<20-40字，综合性技术面总结>",
  }},
  "风险评估": {{
    "波动率评估": "<高波动|中等波动|低波动>",
    "回撤风险": "<高风险|中等风险|低风险>",
    "夏普比率评估": "<优秀|良好|一般|较差>",
    "风险预警": ["<2-3条，每条15-40字，描述具体风险内容>"],
    "风险等级": "<高风险|中风险|低风险>"
  }},
  "多时间维度操作建议": {{
    "短线（1-4周）": {{
      "建议": "<加仓|持有|减仓|观望>",
      "仓位建议": "<轻仓(<20%)|标准仓(20-40%)|偏高仓(40-60%)|满仓(>60%)>",
      "理由": "<30-60字，结合短期技术信号与当前市场情绪>",
      "触发加仓条件": "<具体价格或指标>",
      "触发减仓条件": "<具体价格或指标>"
    }},
    "中线（1-3月）": {{
      "建议": "<加仓|持有|减仓|观望>",
      "仓位建议": "<同上>",
      "理由": "<30-60字，结合中期趋势与宏观政策背景>",
      "触发加仓条件": "<具体价格或指标>",
      "触发减仓条件": "<具体价格或指标>"
    }},
    "长线（3月+）": {{
      "建议": "<配置|持有|逐步减仓|观望>",
      "仓位建议": "<同上>",
      "理由": "<30-60字，结合长期趋势、宏观格局与资金属性>",
      "触发加仓条件": "<具体价格或指标>",
      "触发减仓条件": "<具体价格或指标>"
    }}
  }},
  "操作建议": {{
    "行动": "<强烈买入|买入|持有|观望|减仓|强烈减仓>",
    "置信度": "<高|中|低>",
    "核心理由": "<30-80字，详细展开分析逻辑与市场背景>",
    "当前是否适合入场": "<是|否|需等待>",
    "建议仓位": "<10-20%>",
    "止损位": "<具体价格或-1>",
    "止盈参考": "<具体价格或描述>"
  }},
  "关键价位": {{
    "强支撑位1": "<价格>",
    "强支撑位2": "<价格>",
    "强压力位1": "<价格>",
    "强压力位2": "<价格>",
    "当前价格合理度": "<偏低|合理|偏高|严重偏高>"
  }},
  "重点提示": ["<2-4条，每条20-60字，必须包含对操作有实际指导意义的内容>"],
  "博弈论分析": {{
    "多空博弈": {{
      "多方逻辑": "<20-50字，描述做多资金的驱动逻辑与预期>",
      "空方逻辑": "<20-50字，描述做空资金的驱动逻辑与风险>",
      "当前均衡": "<描述当前博弈格局>",
      "突破方向": "<向上|向下|震荡>"
    }},
    "逆向机会": {{
      "是否存在": "<是|否>",
      "逆向资金": "<哪类资金会反向操作>",
      "触发条件": "<具体条件>"
    }},
    "关键博弈价位": "<具体价格>",
    "博弈论结论": "<2-4句话，给出有深度、有逻辑的博弈局面总结>",
  }}
}}
```

**要求：只输出JSON，不要任何其他文字。**"""


def _fmt(v) -> str:
    if v is None:
        return "—"
    if isinstance(v, float):
        return f"{v:.4f}"
    return str(v)


def _level(pct: float) -> str:
    if pct is None:
        return "数据不足"
    if pct > 15:
        return "强"
    elif pct > 5:
        return "良好"
    elif pct > 0:
        return "小幅正收益"
    elif pct > -5:
        return "小幅亏损"
    elif pct > -15:
        return "较大亏损"
    else:
        return "严重亏损"


def _price_percentile(price: float, prices: list) -> float:
    """计算价格在历史区间的百分位"""
    if not prices or price == 0:
        return 50.0
    valid = [p for p in prices if p > 0]
    if not valid:
        return 50.0
    below = sum(1 for p in valid if p < price)
    return round(below / len(valid) * 100, 1)


def _from_52w_high(current: float, prices: list) -> float:
    """当前价格距离52周高点的跌幅"""
    if not prices:
        return 0.0
    high = max(prices)
    if high == 0:
        return 0.0
    return round((current - high) / high * 100, 2)


def _price_ma_dist(current: float, ma: float) -> float:
    if ma is None or ma == 0:
        return 0.0
    return round((current - ma) / ma * 100, 2)


def _ma_cross(ma5: float, ma20: float) -> float:
    if ma5 is None or ma20 is None or ma20 == 0:
        return 0.0
    return round((ma5 - ma20) / ma20 * 100, 2)


def _boll_position(price: float, upper: float, lower: float) -> float:
    if upper is None or lower is None or upper == lower:
        return 50.0
    return round((price - lower) / (upper - lower) * 100, 1)


def _build_position_section(position: dict, current_nav: float) -> str:
    """构建持仓段落，若无持仓则返回提示"""
    if not position:
        return "（暂无持仓记录）"

    qty = position.get("total_quantity", 0)
    avg_cost = position.get("avg_cost", 0)
    total_cost = position.get("total_cost", 0)
    hold_days = position.get("hold_days", 0)
    current_value = current_nav * qty if current_nav and qty else 0
    profit = (current_nav - avg_cost) * qty if current_nav and avg_cost else 0
    profit_pct = (current_nav / avg_cost - 1) * 100 if current_nav and avg_cost else 0

    buy_records = [r for r in position.get("records", []) if r["type"] == "buy"]

    lines = [
        f"- 当前持仓：{qty}份",
        f"- 成本价：{avg_cost:.4f}元/份",
        f"- 总成本：{total_cost:.2f}元",
        f"- 当前市值：{current_value:.2f}元",
        f"- 浮动盈亏：{profit:+.2f}元（{profit_pct:+.2f}%）",
        f"- 持仓天数：{hold_days}天",
        f"- 买入次数：{position.get('buy_count', 0)}次 | 卖出次数：{position.get('sell_count', 0)}次",
        f"- 各笔买入：",
    ]
    for r in buy_records:
        lines.append(f"  · {r['date']} 买入 {r['quantity']}份 @ {r['price']:.4f}元 {'（' + r.get('note','') + '）' if r.get('note') else ''}")

    return "\n".join(lines)


def _build_macro_section(macro_data: dict) -> str:
    """从 macro_fetcher 导入并构建宏观局势区块"""
    try:
        from macro_fetcher import format_macro_section
        return format_macro_section(macro_data) if macro_data else ""
    except Exception:
        return ""


# ============ 场景模板映射（示例）============
# 请替换为你的实际基金代码
SCENE_TEMPLATES = {
    # 债券策略
    "000003": "债券策略",
    # 黄金/白银策略
    "000004": "黄金择时",
    "000006": "黄金择时",
    # 养老FOF策略
    "000005": "养老FOF策略",
    # 混合型（暂无专属模板，保留空）
    "000001": "",
    "000002": "",
}


def _build_scene_section(fund_code: str) -> str:
    """
    根据基金代码加载专属场景模板
    场景文件位于 memory-tdai 的 scene_blocks 目录
    """
    scene_name = SCENE_TEMPLATES.get(fund_code, "")
    if not scene_name:
        return ""

    scene_dir = os.environ.get(
        "FUND_SCENE_DIR",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenes")
    )
    scene_path = os.path.join(scene_dir, f"{scene_name}.md")
    try:
        with open(scene_path, "r", encoding="utf-8") as f:
            content = f.read()
        return (
            f"\n\n{'='*20}\n"
            f"【专属分析模板：{scene_name}】\n"
            f"{'='*20}\n"
            f"{content}\n"
            f"{'='*20}\n\n"
        )
    except Exception:
        return ""


def ai_analyze_fund(fund_code: str, fund_name: str, analysis: dict, valuation: dict = None, position: dict = None, macro_data: dict = None) -> str:
    """
    对单只基金进行深度 AI 量化分析
    analysis: technical.py 输出的技术分析字典（含 prices 列表）
    valuation: 实时净值数据
    macro_data: 宏观局势数据（来自 macro_fetcher.fetch_macro_data）
    """
    model, api_key = get_llm_config()
    if not model or not api_key:
        return "⚠️ 未配置 LLM_MODEL 或 LLM_API_KEY，无法进行 AI 分析"

    nav = analysis.get("latest_nav", 0)
    est_change = analysis.get("est_change", 0) if valuation else 0
    latest_date = analysis.get("latest_date", "")

    prices = analysis.get("prices", [])
    ma5 = analysis.get("ma5")
    ma10 = analysis.get("ma10")
    ma20 = analysis.get("ma20")
    ma60 = analysis.get("ma60")

    prices_252 = prices[:252] if prices else []
    price_252w_high = max(prices_252) if prices_252 else None
    price_252w_low = min(prices_252) if prices_252 else None

    # 构建宏观局势区块
    macro_section = _build_macro_section(macro_data)

    # 构建场景专属模板（债券策略/黄金择时/养老FOF）
    scene_section = _build_scene_section(fund_code)

    prompt = FUND_ANALYSIS_PROMPT.format(
        fund_name=fund_name or fund_code,
        fund_code=fund_code,
        latest_nav=nav,
        est_change=est_change,
        latest_date=latest_date,
        ma5=_fmt(ma5),
        ma10=_fmt(ma10),
        ma20=_fmt(ma20),
        scene_section=scene_section,
        ma60=_fmt(analysis.get("ma60")),
        rsi=_fmt(analysis.get("rsi14")),
        macd_dif=_fmt(analysis.get("macd_dif")),
        macd_dea=_fmt(analysis.get("macd_dea")),
        macd_hist=_fmt(analysis.get("macd_hist")),
        kdj_k=_fmt(analysis.get("kdj_k")),
        kdj_d=_fmt(analysis.get("kdj_d")),
        kdj_j=_fmt(analysis.get("kdj_j")),
        boll_upper=_fmt(analysis.get("boll_upper")),
        boll_middle=_fmt(analysis.get("boll_middle")),
        boll_lower=_fmt(analysis.get("boll_lower")),
        boll_position=_boll_position(nav, analysis.get("boll_upper"), analysis.get("boll_lower")),
        price_ma5_dist=_price_ma_dist(nav, ma5),
        price_ma20_dist=_price_ma_dist(nav, ma20),
        ma5_ma20_cross=_ma_cross(ma5, ma20),
        volatility=_fmt(analysis.get("volatility")),
        max_drawdown=_fmt(analysis.get("max_drawdown")),
        sharpe=_fmt(analysis.get("sharpe_ratio")),
        return_1w=analysis.get("return_1w"),
        return_1w_level=_level(analysis.get("return_1w")),
        return_1m=analysis.get("return_1m"),
        return_1m_level=_level(analysis.get("return_1m")),
        return_3m=analysis.get("return_3m"),
        return_3m_level=_level(analysis.get("return_3m")),
        return_6m=analysis.get("return_6m"),
        return_6m_level=_level(analysis.get("return_6m")),
        return_1y=analysis.get("return_1y"),
        return_1y_level=_level(analysis.get("return_1y")),
        from_52w_high=_from_52w_high(nav, prices_252),
        price_252w_high=_fmt(price_252w_high),
        price_252w_low=_fmt(price_252w_low),
        price_percentile=_price_percentile(nav, prices_252),
        position_section=_build_position_section(position, nav),
        macro_section=macro_section,
    )

    raw = call_llm(model, prompt, api_key)

    try:
        cleaned = raw.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        data = json.loads(cleaned.strip())
        text = _render_report(data, fund_name, fund_code, nav, est_change)
        return {"data": data, "text": text}
    except json.JSONDecodeError:
        return {"data": None, "text": raw}


def _render_report(data: dict, fund_name: str, fund_code: str, nav: float, est_change: float) -> str:
    """将 JSON 分析结果渲染为易读的文本报告"""
    score = data.get("综合评分", {})
    tech = data.get("技术面综合判断", {})
    risk = data.get("风险评估", {})
    ops = data.get("多时间维度操作建议", {})
    action = data.get("操作建议", {})
    levels = data.get("关键价位", {})
    tips = data.get("重点提示", [])
    game = data.get("博弈论分析", {})

    rating_map = {"极强": "🟢🟢", "强劲": "🟢", "良好": "🟡", "中性": "🟡", "偏弱": "🔴", "弱势": "🔴🔴"}
    rating_emoji = rating_map.get(score.get("综合评级", "中性"), "🟡")

    lines = [
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"📊 {fund_name}（{fund_code}）深度分析",
        f"净值 {nav:.4f}  日涨跌 {est_change:+.2f}%",
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"",
        f"【综合评分】{rating_emoji} {score.get('总分', '?')}/100  {score.get('综合评级', '')}",
        f"  技术面 {score.get('技术面得分', '?')} | 风险 {score.get('风险得分', '?')} | 收益 {score.get('收益得分', '?')}",
        f"  {score.get('评分解读', '')}",
        f"",
        f"【技术面】{tech.get('综合结论', '')}",
        f"  趋势：短线{tech.get('短期趋势', '—')} | 中线{tech.get('中期趋势', '—')} | 长线{tech.get('长期趋势', '—')}",
        f"  MACD {tech.get('MACD信号', '—')} | KDJ {tech.get('KDJ信号', '—')} | RSI {tech.get('RSI信号', '—')}",
        f"  布林 {tech.get('布林带信号', '—')} | 均线 {tech.get('均线系统', '—')}",
        f"",
        f"【风险评估】⚠️ {risk.get('风险等级', '?')}",
        f"  波动率 {risk.get('波动率评估', '—')} | 回撤风险 {risk.get('回撤风险', '—')} | 夏普比率 {risk.get('夏普比率评估', '—')}",
    ]

    if risk.get("风险预警"):
        for w in risk["风险预警"]:
            lines.append(f"  🔺 {w}")

    lines += ["", "【操作建议】"]
    action_emoji = {"强烈买入": "🟢🟢", "买入": "🟢", "持有": "🟡", "观望": "⚪", "减仓": "🔴", "强烈减仓": "🔴🔴"}
    ae = action_emoji.get(action.get("行动", ""), "⚪")
    lines.append(f"  {ae} {action.get('行动', '')}  置信度：{action.get('置信度', '?')}")
    lines.append(f"  核心逻辑：{action.get('核心理由', '—')}")
    lines.append(f"  建议仓位：{action.get('建议仓位', '—')}")
    if action.get("止损位") and action.get("止损位") != -1:
        lines.append(f"  止损位：{action['止损位']}")
    if action.get("止盈参考"):
        lines.append(f"  止盈参考：{action.get('止盈参考', '—')}")
    lines.append(f"  当前是否适合入场：{action.get('当前是否适合入场', '—')}")

    lines += ["", "【多时间维度操作建议】"]
    for label, info in [("短线（1-4周）", ops.get("短线（1-4周）", {})),
                         ("中线（1-3月）", ops.get("中线（1-3月）", {})),
                         ("长线（3月+）", ops.get("长线（3月+）", {}))]:
        if info:
            lines.append(f"  {label}：{info.get('建议', '—')} | 仓位{info.get('仓位建议', '—')}")
            lines.append(f"    理由：{info.get('理由', '—')}")
            if info.get('触发加仓条件'):
                lines.append(f"    ➕加仓条件：{info['触发加仓条件']}")
            if info.get('触发减仓条件'):
                lines.append(f"    ➖减仓条件：{info['触发减仓条件']}")

    lines += ["", "【关键价位】"]
    lines.append(f"  强支撑：{levels.get('强支撑位1', '—')} / {levels.get('强支撑位2', '—')}")
    lines.append(f"  强压力：{levels.get('强压力位1', '—')} / {levels.get('强压力位2', '—')}")
    lines.append(f"  当前价格合理度：{levels.get('当前价格合理度', '—')}")

    if tips:
        lines += ["", "【重点提示】"]
        for t in tips:
            lines.append(f"  ⚡ {t}")

    if game:
        mp = game.get("多空博弈", {})
        rev = game.get("逆向机会", {})
        lines += [
            "",
            "【博弈论视角】🎯",
            f"  结论：{game.get('博弈论结论', '—')}",
            f"  多空：{mp.get('多方逻辑', '—')} vs {mp.get('空方逻辑', '—')}",
            f"  均衡：{mp.get('当前均衡', '—')} | 突破方向：{mp.get('突破方向', '—')}",
            f"  逆向机会：{rev.get('是否存在', '—')}（{rev.get('逆向资金', '—')}）触发：{rev.get('触发条件', '—')}",
            f"  关键博弈价位：{game.get('关键博弈价位', '—')}",
        ]

    lines.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from fund_api import fetch_otc_fund_valuation, fetch_otc_fund_history
    from technical import analyze_fund as tech_analyze

    # 检查 LLM 配置
    model, api_key = get_llm_config()
    if not model or not api_key:
        print("=" * 50)
        print("【错误】LLM 模型未配置")
        print("请配置以下环境变量：")
        print("  export LLM_MODEL=your_model_name")
        print("  export LLM_API_KEY=your_api_key")
        print("=" * 50)
        sys.exit(1)

    code = "161226"
    val = fetch_otc_fund_valuation(code)
    hist = fetch_otc_fund_history(code, days=90)
    if not hist:
        print("获取历史数据失败")
        sys.exit(1)

    analysis = tech_analyze(code, hist)
    info = {"latest_nav": hist[0]["nav"], "est_change": hist[0].get("change", 0), "latest_date": hist[0].get("date", "")}
    combined = {**analysis, **info}

    print(f"正在进行深度 AI 分析（{code}）...")
    result = ai_analyze_fund(code, "国投瑞银白银期货(LOF)A", combined, val)
    print(result)
