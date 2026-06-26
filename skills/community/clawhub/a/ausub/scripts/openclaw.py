import json
import math
import os
import re
from dataclasses import dataclass
from statistics import mean
from typing import List, Optional


try:
    import tushare as ts
except ImportError:  # pragma: no cover
    ts = None


@dataclass
class Bar:
    trade_date: str
    close: float


@dataclass
class ReferenceQuote:
    symbol: str
    trade_date: str
    close: float
    prev_close: Optional[float] = None


@dataclass
class Recommendation:
    state: str
    multiplier: float
    suggested_amount: float
    summary: str
    rationale: str
    risk_note: str
    action_text: str
    account_summary: str
    account_action: str
    details: dict


DEFAULT_CONFIG = {
    "symbol": "518880.SH",
    "base_amount": 1000,
    "min_multiplier": 0.6,
    "max_multiplier": 1.8,
    "rules": {
        "oversold_rsi": 35,
        "weak_rsi_max": 45,
        "neutral_rsi_max": 60,
        "hot_rsi": 68,
        "discount_to_ma20": -0.03,
        "premium_to_ma20": 0.05,
        "ma20_near_band": 0.01,
        "drawdown_weak": 0.04,
        "deep_drawdown": 0.08,
    },
}


def project_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def ensure_within_project(path: str) -> str:
    resolved = os.path.abspath(path)
    root = project_root()
    if os.path.commonpath([resolved, root]) != root:
        raise RuntimeError(f"Path escapes project root: {resolved}")
    return resolved


def sanitize_user_id(user_id: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_-]+", user_id):
        raise RuntimeError("OPENCLAW_USER_ID contains invalid characters.")
    return user_id


def load_config(path: Optional[str] = None) -> dict:
    config = json.loads(json.dumps(DEFAULT_CONFIG))
    if path and os.path.exists(path):
        safe_path = ensure_within_project(path)
        with open(safe_path, "r", encoding="utf-8") as fh:
            user_config = json.load(fh)
        merge_dict(config, user_config)
    return config


def load_user_memory(user_id: Optional[str]) -> Optional[dict]:
    if not user_id:
        return None
    safe_user_id = sanitize_user_id(user_id)
    memory_path = ensure_within_project(
        os.path.join(project_root(), "memory", "users", f"{safe_user_id}.json")
    )
    if not os.path.exists(memory_path):
        raise RuntimeError(f"User memory file not found: {memory_path}")
    with open(memory_path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def merge_dict(base: dict, extra: dict) -> None:
    for key, value in extra.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            merge_dict(base[key], value)
        else:
            base[key] = value


def get_tushare_client():
    token = os.getenv("TUSHARE_TOKEN")
    if not token:
        raise RuntimeError("Missing TUSHARE_TOKEN environment variable.")
    if ts is None:
        raise RuntimeError("tushare is not installed. Run `pip install tushare` first.")
    ts.set_token(token)
    return ts.pro_api()


def fetch_daily_bars(symbol: str, limit: int = 120) -> List[Bar]:
    pro = get_tushare_client()
    df = pro.fund_daily(ts_code=symbol, limit=limit)
    if df is None or df.empty:
        df = pro.daily(ts_code=symbol, limit=limit)
    if df is None or df.empty:
        raise RuntimeError(f"No data returned for symbol {symbol}.")

    bars = [
        Bar(trade_date=row["trade_date"], close=float(row["close"]))
        for _, row in df.sort_values("trade_date").iterrows()
    ]
    if len(bars) < 60:
        raise RuntimeError("Not enough history to compute indicators.")
    return bars


def fetch_au9999_reference() -> Optional[ReferenceQuote]:
    pro = get_tushare_client()
    candidates = ["Au99.99", "au99.99", "Au9999", "au9999"]
    for symbol in candidates:
        try:
            df = pro.sge_daily(ts_code=symbol, limit=2)
        except Exception:
            continue
        if df is None or df.empty:
            continue
        sorted_df = df.sort_values("trade_date")
        row = sorted_df.iloc[-1]
        prev_close = float(sorted_df.iloc[-2]["close"]) if len(sorted_df) >= 2 else None
        return ReferenceQuote(
            symbol=symbol,
            trade_date=str(row["trade_date"]),
            close=float(row["close"]),
            prev_close=prev_close,
        )
    return None


def sma(values: List[float], window: int) -> float:
    return mean(values[-window:])


def stddev(values: List[float], window: int) -> float:
    window_values = values[-window:]
    avg = mean(window_values)
    variance = sum((value - avg) ** 2 for value in window_values) / len(window_values)
    return math.sqrt(variance)


def compute_rsi(values: List[float], period: int = 14) -> float:
    deltas = [values[i] - values[i - 1] for i in range(1, len(values))]
    gains = [max(delta, 0.0) for delta in deltas[-period:]]
    losses = [abs(min(delta, 0.0)) for delta in deltas[-period:]]
    avg_gain = mean(gains) if gains else 0.0
    avg_loss = mean(losses) if losses else 0.0
    if math.isclose(avg_loss, 0.0):
        return 100.0
    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))


def compute_ema(values: List[float], period: int) -> List[float]:
    multiplier = 2 / (period + 1)
    ema_values = [values[0]]
    for value in values[1:]:
        ema_values.append((value - ema_values[-1]) * multiplier + ema_values[-1])
    return ema_values


def compute_macd(values: List[float]) -> dict:
    ema12 = compute_ema(values, 12)
    ema26 = compute_ema(values, 26)
    dif = [short - long for short, long in zip(ema12, ema26)]
    dea = compute_ema(dif, 9)
    hist = [d - e for d, e in zip(dif, dea)]
    return {
        "dif": dif[-1],
        "dea": dea[-1],
        "hist": hist[-1],
        "hist_series": hist[-3:],
    }


def compute_metrics(bars: List[Bar]) -> dict:
    closes = [bar.close for bar in bars]
    last_close = closes[-1]
    ma20 = sma(closes, 20)
    ma60 = sma(closes, 60)
    rsi14 = compute_rsi(closes, 14)
    recent_high = max(closes[-60:])
    drawdown = (recent_high - last_close) / recent_high if recent_high else 0.0
    vs_ma20 = (last_close - ma20) / ma20 if ma20 else 0.0
    vs_ma60 = (last_close - ma60) / ma60 if ma60 else 0.0
    boll_std = stddev(closes, 20)
    boll_upper = ma20 + 2 * boll_std
    boll_lower = ma20 - 2 * boll_std
    boll_width = boll_upper - boll_lower
    boll_pos = (last_close - boll_lower) / boll_width if boll_width > 0 else 0.5
    macd = compute_macd(closes)
    return {
        "last_close": last_close,
        "ma20": ma20,
        "ma60": ma60,
        "rsi14": rsi14,
        "drawdown_60": drawdown,
        "vs_ma20": vs_ma20,
        "vs_ma60": vs_ma60,
        "boll_upper": boll_upper,
        "boll_lower": boll_lower,
        "boll_pos": boll_pos,
        "boll_width": boll_width,
        "macd_dif": macd["dif"],
        "macd_dea": macd["dea"],
        "macd_hist": macd["hist"],
        "macd_hist_series": macd["hist_series"],
        "latest_trade_date": bars[-1].trade_date,
    }


def classify_core_state(metrics: dict, config: dict) -> tuple[str, float, List[str]]:
    rules = config["rules"]
    oversold_hits = []
    if metrics["vs_ma20"] <= rules["discount_to_ma20"]:
        oversold_hits.append("收盘价低于 MA20 超过 3%")
    if metrics["rsi14"] <= rules["oversold_rsi"]:
        oversold_hits.append("RSI14 小于等于 35")
    if metrics["drawdown_60"] >= rules["deep_drawdown"]:
        oversold_hits.append("60 日回撤大于等于 8%")
    if metrics["vs_ma60"] < 0:
        oversold_hits.append("收盘价位于 MA60 下方")
    if len(oversold_hits) >= 2:
        return "oversold", 1.6, oversold_hits

    hot_hits = []
    if metrics["vs_ma20"] >= rules["premium_to_ma20"]:
        hot_hits.append("收盘价高于 MA20 超过 5%")
    if metrics["rsi14"] >= rules["hot_rsi"]:
        hot_hits.append("RSI14 大于等于 68")
    if metrics["vs_ma60"] > 0:
        hot_hits.append("收盘价位于 MA60 上方")
    if metrics["drawdown_60"] < rules["drawdown_weak"]:
        hot_hits.append("价格接近 60 日高点")
    if len(hot_hits) >= 2:
        return "hot", 0.7, hot_hits

    weak_hits = []
    if metrics["vs_ma20"] < 0:
        weak_hits.append("收盘价位于 MA20 下方")
    if rules["oversold_rsi"] <= metrics["rsi14"] <= rules["weak_rsi_max"]:
        weak_hits.append("RSI14 位于 35 到 45 之间")
    if rules["drawdown_weak"] <= metrics["drawdown_60"] < rules["deep_drawdown"]:
        weak_hits.append("60 日回撤位于 4% 到 8% 之间")
    if len(weak_hits) >= 2:
        return "weak", 1.2, weak_hits

    neutral_hits = []
    if abs(metrics["vs_ma20"]) <= rules["ma20_near_band"]:
        neutral_hits.append("收盘价接近 MA20")
    if rules["weak_rsi_max"] < metrics["rsi14"] <= rules["neutral_rsi_max"]:
        neutral_hits.append("RSI14 位于 45 到 60 之间")
    if metrics["drawdown_60"] < rules["drawdown_weak"]:
        neutral_hits.append("60 日回撤小于 4%")
    return "neutral", 1.0, neutral_hits or ["市场整体处于均衡区间"]


def bollinger_adjustment(metrics: dict) -> tuple[float, str]:
    if metrics["boll_width"] <= 0:
        return 0.0, "布林带宽度异常，忽略布林修正"
    pos = metrics["boll_pos"]
    if pos <= 0:
        return 0.2, "价格触及或跌破布林下轨"
    if pos <= 0.25:
        return 0.1, "价格靠近布林下轨"
    if pos < 0.75:
        return 0.0, "价格位于布林中部区域"
    if pos < 1:
        return -0.1, "价格靠近布林上轨"
    return -0.2, "价格触及或突破布林上轨"


def macd_adjustment(metrics: dict, state: str) -> tuple[float, str]:
    hist_series = metrics["macd_hist_series"]
    if len(hist_series) < 3:
        return 0.0, "MACD 历史不足，忽略确认修正"

    h2, h1, h0 = hist_series[0], hist_series[1], hist_series[2]
    bearish_momentum_easing = h0 < 0 and abs(h0) < abs(h1) < abs(h2)
    bullish_momentum_easing = h0 > 0 and abs(h0) < abs(h1) < abs(h2)

    if state == "oversold":
        if bearish_momentum_easing:
            return 0.1, "MACD 空头动能已连续两期减弱"
        return 0.0, "MACD 暂未确认更强的低位加仓信号"
    if state == "hot":
        if bullish_momentum_easing:
            return -0.1, "MACD 多头动能已连续两期减弱"
        return 0.0, "MACD 暂未确认进一步降档"
    return 0.0, "MACD 仅用于极端状态确认"


def build_recommendation(metrics: dict, config: dict) -> Recommendation:
    base_amount = float(config["base_amount"])
    min_multiplier = float(config["min_multiplier"])
    max_multiplier = float(config["max_multiplier"])

    state, core_multiplier, core_reasons = classify_core_state(metrics, config)
    boll_adjustment, boll_reason = bollinger_adjustment(metrics)
    macd_adj, macd_reason = macd_adjustment(metrics, state)
    raw_multiplier = core_multiplier + boll_adjustment + macd_adj
    multiplier = round(max(min_multiplier, min(max_multiplier, raw_multiplier)), 2)
    suggested_amount = round(base_amount * multiplier, 2)

    state_text = {
        "oversold": "市场处于偏弱且具备较高配置价值的区间",
        "weak": "市场处于偏弱区间",
        "neutral": "市场处于中性区间",
        "hot": "市场处于偏热区间",
    }[state]

    summary = (
        f"{metrics['latest_trade_date']} 收盘后，"
        f"最新价 {metrics['last_close']:.3f}，"
        f"MA20 {metrics['ma20']:.3f}，MA60 {metrics['ma60']:.3f}，"
        f"RSI14 {metrics['rsi14']:.1f}，"
        f"60日回撤 {metrics['drawdown_60']:.1%}，"
        f"布林位置 {metrics['boll_pos']:.2f}，"
        f"MACD柱体 {metrics['macd_hist']:.4f}。"
    )
    risk_note = "本结果仅用于纪律化定投辅助，不构成任何收益承诺或投资保证。"
    rationale = (
        f"{state_text}。"
        f"核心倍率为 {core_multiplier:.1f}，原因是：{'；'.join(core_reasons)}。"
        f"布林线修正 {boll_adjustment:+.1f}，原因是：{boll_reason}。"
        f"MACD 修正 {macd_adj:+.1f}，原因是：{macd_reason}。"
    )
    action_text = (
        f"建议本期按 {multiplier:.2f} 倍执行，"
        f"投入金额约 {suggested_amount:.2f} 元。"
    )

    return Recommendation(
        state=state,
        multiplier=multiplier,
        suggested_amount=suggested_amount,
        summary=summary,
        rationale=rationale,
        risk_note=risk_note,
        action_text=action_text,
        account_summary="未读取用户账户配置，本次仅输出市场层建议。",
        account_action="如需结合持仓、盈利和场内/场外分配，请提供用户记忆配置。",
        details={
            "core_multiplier": core_multiplier,
            "core_reasons": core_reasons,
            "bollinger_adjustment": boll_adjustment,
            "bollinger_reason": boll_reason,
            "macd_adjustment": macd_adj,
            "macd_reason": macd_reason,
            "raw_multiplier": round(raw_multiplier, 2),
        },
    )


def apply_account_overlay(recommendation: Recommendation, user_memory: Optional[dict]) -> Recommendation:
    if not user_memory:
        return recommendation

    plan = user_memory.get("plan", {})
    execution_preferences = user_memory.get("execution_preferences", {})
    risk_preferences = user_memory.get("risk_preferences", {})

    base_amount = float(plan.get("base_amount", recommendation.suggested_amount) or recommendation.suggested_amount)
    max_single_period = float(risk_preferences.get("max_multiplier", recommendation.multiplier) or recommendation.multiplier)
    min_single_period = float(risk_preferences.get("min_multiplier", recommendation.multiplier) or recommendation.multiplier)
    prefer_etf = bool(execution_preferences.get("prefer_etf", True))
    allow_otc_accumulation = bool(execution_preferences.get("allow_otc_accumulation", True))
    transfer_threshold = float(execution_preferences.get("transfer_threshold", 0) or 0)
    schedule = plan.get("schedule", "weekly_thursday_if_trading")

    account_adjustment = 0.0
    account_reasons = ["当前采用轻量配置模式，仅依据用户定投方案给出执行建议"]

    final_multiplier = round(max(min_single_period, min(max_single_period, recommendation.multiplier + account_adjustment)), 2)
    final_amount = round(final_multiplier * base_amount, 2)

    schedule_text_map = {
        "weekly_thursday_if_trading": "每周四执行，前提是周四为交易日",
        "weekly_thursday": "每周四执行",
    }
    schedule_text = schedule_text_map.get(schedule, schedule)

    account_summary_parts = [
        f"用户 {user_memory.get('display_name', user_memory.get('user_id', 'unknown'))}",
        f"基础定投金额 {base_amount:.2f} 元",
        f"执行节奏：{schedule_text}",
    ]

    account_action_parts = []
    if prefer_etf:
        account_action_parts.append("本期新增资金优先投向场内 ETF。")
    elif allow_otc_accumulation:
        account_action_parts.append("本期可继续通过场外基金积累。")

    if allow_otc_accumulation and transfer_threshold > 0:
        account_action_parts.append(f"若场外资金累计达到 {transfer_threshold:.0f} 元，可考虑转入场内 ETF。")

    if not account_action_parts:
        account_action_parts.append("本期按默认路径执行，不额外调整场内外分配。")

    recommendation.multiplier = final_multiplier
    recommendation.suggested_amount = final_amount
    recommendation.action_text = f"建议本期按 {final_multiplier:.2f} 倍执行，投入金额约 {final_amount:.2f} 元。"
    recommendation.account_summary = "；".join(account_summary_parts) + "。"
    recommendation.account_action = "".join(account_action_parts)
    recommendation.rationale = (
        recommendation.rationale
        + f" 账户层修正 {account_adjustment:+.1f}。"
        + ("账户层原因：" + "；".join(account_reasons) + "。" if account_reasons else "账户层未触发额外修正。")
    )
    recommendation.details["account_adjustment"] = account_adjustment
    recommendation.details["account_reasons"] = account_reasons
    recommendation.details["final_multiplier_after_account"] = final_multiplier
    recommendation.details["plan_base_amount"] = base_amount
    recommendation.details["plan_schedule"] = schedule
    return recommendation


def build_text_report(
    config: dict,
    recommendation: Recommendation,
    etf_indicator_table: dict,
    au9999_section: dict,
) -> str:
    etf_lines = [
        "518880.SH 主行情指标表",
        f"- 交易日期：{etf_indicator_table['交易日期']}",
        f"- 最新价：{etf_indicator_table['最新价']}",
        f"- MA20：{etf_indicator_table['MA20']}",
        f"- MA60：{etf_indicator_table['MA60']}",
        f"- RSI14：{etf_indicator_table['RSI14']}",
        f"- 60日回撤：{etf_indicator_table['60日回撤']}",
        f"- 布林位置：{etf_indicator_table['布林位置']}",
        f"- MACD柱体：{etf_indicator_table['MACD柱体']}",
    ]

    au_lines = ["Au99.99 参考行情"]
    if "品种" in au9999_section:
        au_lines.extend(
            [
                f"- 交易日期：{au9999_section['交易日期']}",
                f"- 收盘价：{au9999_section['收盘价']}",
                f"- 涨跌：{au9999_section['涨跌']}",
            ]
        )
    else:
        au_lines.append(f"- {au9999_section['说明']}")

    lines = [
        "OpenClaw 黄金定投日报",
        f"主执行标的：{config['symbol']}",
        "",
        "市场概览",
        f"- 市场状态：{recommendation.state}",
        f"- 日报摘要：{recommendation.summary}",
        "",
        *etf_lines,
        "",
        *au_lines,
        "",
        "定投建议",
        f"- {recommendation.action_text}",
        f"- 触发说明：{recommendation.rationale}",
        "",
        "账户建议",
        f"- 账户摘要：{recommendation.account_summary}",
        f"- 资金分配建议：{recommendation.account_action}",
        "",
        "风险提示",
        f"- {recommendation.risk_note}",
    ]
    return "\n".join(lines)


def main() -> None:
    config_path = os.getenv("OPENCLAW_CONFIG", os.path.join(os.path.dirname(__file__), "..", "config.example.json"))
    config = load_config(config_path)
    user_id = os.getenv("OPENCLAW_USER_ID")
    user_memory = load_user_memory(user_id)
    bars = fetch_daily_bars(config["symbol"])
    au9999_reference = fetch_au9999_reference()
    metrics = compute_metrics(bars)
    recommendation = build_recommendation(metrics, config)
    recommendation = apply_account_overlay(recommendation, user_memory)
    etf_indicator_table = {
        "说明": f"以下指标表基于场内黄金 ETF {config['symbol']}",
        "交易日期": metrics["latest_trade_date"],
        "最新价": round(metrics["last_close"], 3),
        "MA20": round(metrics["ma20"], 3),
        "MA60": round(metrics["ma60"], 3),
        "RSI14": round(metrics["rsi14"], 1),
        "60日回撤": f"{metrics['drawdown_60']:.1%}",
        "布林位置": round(metrics["boll_pos"], 2),
        "MACD柱体": round(metrics["macd_hist"], 4),
    }
    if au9999_reference:
        change_value = None
        change_pct = None
        if au9999_reference.prev_close and au9999_reference.prev_close != 0:
            change_value = au9999_reference.close - au9999_reference.prev_close
            change_pct = change_value / au9999_reference.prev_close
        change_text = "暂无法计算"
        if change_value is not None and change_pct is not None:
            direction = "上涨" if change_value > 0 else "下跌" if change_value < 0 else "持平"
            change_text = f"{change_value:+.2f} 元（{change_pct:+.2%}，{direction}）"
        au9999_section = {
            "说明": "以下数据为上海黄金交易所 Au99.99，仅作为黄金现货行情参考，不直接参与当前定投倍率计算",
            "品种": au9999_reference.symbol,
            "交易日期": au9999_reference.trade_date,
            "收盘价": f"{au9999_reference.close:.2f} 元/克",
            "涨跌": change_text,
        }
    else:
        au9999_section = {
            "说明": "上海黄金交易所 Au99.99 参考行情暂不可用，不影响当前基于 518880.SH 的策略建议。"
        }
    text_report = build_text_report(config, recommendation, etf_indicator_table, au9999_section)
    print(
        json.dumps(
            {
                "日报文本": text_report,
                "标的": config["symbol"],
                "主行情指标表": etf_indicator_table,
                "Au99.99参考行情": au9999_section,
                "市场状态": recommendation.state,
                "建议倍率": recommendation.multiplier,
                "建议投入金额": recommendation.suggested_amount,
                "日报摘要": recommendation.summary,
                "操作建议": recommendation.action_text,
                "账户摘要": recommendation.account_summary,
                "资金分配建议": recommendation.account_action,
                "触发说明": recommendation.rationale,
                "风险提示": recommendation.risk_note,
                "details": recommendation.details,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
