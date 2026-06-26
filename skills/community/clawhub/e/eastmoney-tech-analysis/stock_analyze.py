#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
东方财富股票分析 - 命令行入口
"""

import sys
import json
from eastmoney_spider import EastmoneySpider
from indicators import calculate_kdj, calculate_macd, calculate_boll, calculate_ma, get_latest_signals


def analyze_stock(code: str, days: int = 100) -> dict:
    """
    完整分析一只股票

    Args:
        code: 股票代码
        days: 分析天数

    Returns:
        dict: 完整的分析结果
    """
    spider = EastmoneySpider()

    # 获取K线数据
    df = spider.get_stock_kline(code, days=days)

    if df.empty:
        return {'error': f'无法获取股票 {code} 的数据'}

    # 计算各指标
    kdj = calculate_kdj(df)
    macd = calculate_macd(df)
    boll = calculate_boll(df)
    ma = calculate_ma(df)
    signals = get_latest_signals(df)

    # 获取最新行情
    latest = df.iloc[-1]

    return {
        'code': code,
        'name': df.iloc[0]['name'] if 'name' in df.columns else code,
        'date': latest['date'],
        'price': {
            'close': latest['close'],
            'open': latest['open'],
            'high': latest['high'],
            'low': latest['low'],
            'volume': latest['volume'],
            'pct_chg': latest.get('pct_chg', 0)
        },
        'indicators': {
            'kdj': {
                'k': round(kdj['k'][-1], 2) if kdj['k'] else None,
                'd': round(kdj['d'][-1], 2) if kdj['d'] else None,
                'j': round(kdj['j'][-1], 2) if kdj['j'] else None,
            },
            'macd': {
                'dif': round(macd['dif'][-1], 4) if macd['dif'] else None,
                'dea': round(macd['dea'][-1], 4) if macd['dea'] else None,
                'macd': round(macd['macd'][-1], 4) if macd['macd'] else None,
            },
            'boll': {
                'upper': round(boll['upper'][-1], 2) if boll['upper'] else None,
                'middle': round(boll['middle'][-1], 2) if boll['middle'] else None,
                'lower': round(boll['lower'][-1], 2) if boll['lower'] else None,
            },
            'ma': {
                'ma5': round(ma['ma5'][-1], 2) if 'ma5' in ma else None,
                'ma10': round(ma['ma10'][-1], 2) if 'ma10' in ma else None,
                'ma20': round(ma['ma20'][-1], 2) if 'ma20' in ma else None,
                'ma60': round(ma['ma60'][-1], 2) if 'ma60' in ma else None,
            }
        },
        'signals': signals
    }


def safe_fmt(value, fmt="{:.2f}", default="--"):
    """安全格式化数字"""
    try:
        if value is None:
            return default
        return fmt.format(value)
    except Exception:
        return default


def format_text(result: dict, use_color: bool = True, use_emoji: bool = True) -> str:
    """简洁版输出"""
    if 'error' in result:
        return f"错误: {result['error']}"

    # 基本信息
    name = result.get('name', result.get('code', '未知'))
    code = result.get('code', '--')
    date = result.get('date', '--')

    price = result.get('price', {})
    close = price.get('close')
    open_ = price.get('open')
    high = price.get('high')
    low = price.get('low')
    volume = price.get('volume')
    pct_chg = price.get('pct_chg')

    # 指标
    ind = result.get('indicators', {})
    kdj = ind.get('kdj', {})
    macd = ind.get('macd', {})
    boll = ind.get('boll', {})
    ma = ind.get('ma', {})

    # 信号
    signals = result.get('signals', {})
    kdj_sig = signals.get('kdj', {})
    macd_sig = signals.get('macd', {})
    boll_sig = signals.get('boll', '--')

    # 一些符号控制
    title_icon = "📈 " if use_emoji else ""
    price_icon = "💰 " if use_emoji else ""
    indicator_icon = "📊 " if use_emoji else ""
    signal_icon = "🔔 " if use_emoji else ""

    # 颜色（ANSI）
    def color(text, code):
        if not use_color:
            return text
        return f"\033[{code}m{text}\033[0m"

    # 涨跌颜色
    if isinstance(pct_chg, (int, float)):
        pct_str = f"{pct_chg:+.2f}%"
        if pct_chg > 0:
            pct_str = color(pct_str, "31")  # 红色
        elif pct_chg < 0:
            pct_str = color(pct_str, "32")  # 绿色
    else:
        pct_str = "--"

    # 成交量格式化（简单转为万 / 亿）
    def fmt_volume(v):
        if not isinstance(v, (int, float)):
            return "--"
        if v >= 1e8:
            return f"{v / 1e8:.2f} 亿"
        if v >= 1e4:
            return f"{v / 1e4:.2f} 万"
        return str(v)

    lines = [
        f"{title_icon}{name} ({code}) - {date}",
        "",
        f"{price_icon}价格: {safe_fmt(close)} ({pct_str})",
        f"   开盘: {safe_fmt(open_)} | 最高: {safe_fmt(high)} | 最低: {safe_fmt(low)} | 成交量: {fmt_volume(volume)}",
        "",
        f"{indicator_icon}技术指标:",
        f"   KDJ : K={safe_fmt(kdj.get('k'))}  D={safe_fmt(kdj.get('d'))}  J={safe_fmt(kdj.get('j'))}",
        f"   MACD: DIF={safe_fmt(macd.get('dif'), '{:.4f}')}  DEA={safe_fmt(macd.get('dea'), '{:.4f}')}  MACD={safe_fmt(macd.get('macd'), '{:.4f}')}",
        f"   BOLL: 上轨={safe_fmt(boll.get('upper'))}  中轨={safe_fmt(boll.get('middle'))}  下轨={safe_fmt(boll.get('lower'))}",
        f"   MA  : MA5={safe_fmt(ma.get('ma5'))}  MA10={safe_fmt(ma.get('ma10'))}  MA20={safe_fmt(ma.get('ma20'))}  MA60={safe_fmt(ma.get('ma60'))}",
        "",
        f"{signal_icon}交易信号:",
        f"   KDJ : {kdj_sig.get('status', '--')} (J={safe_fmt(kdj_sig.get('j'))})",
        f"   MACD: {macd_sig.get('trend', '--')}",
        f"   BOLL: {boll_sig}",
    ]

    return "\n".join(lines)


# ---------- 技术分析报告 & 买入建议部分 ----------

def judge_operation(price: dict, signals: dict):
    """
    根据技术指标给出一个简要操作建议（示例策略，可按你自己的策略调整）

    假定 signals 结构大致为：
    signals = {
        "kdj": {"status": "多头/空头/震荡", "j": float, "cross": "金叉/死叉/无"},
        "macd": {"trend": "多头/空头/震荡", "cross": "金叉/死叉/无", "hist_state": "放大/缩小/平稳"},
        "boll": "上轨附近/中轨附近/下轨附近/轨道外/..."
    }
    """
    kdj_sig = signals.get("kdj", {})
    macd_sig = signals.get("macd", {})
    boll_sig = signals.get("boll", "")

    kdj_status = kdj_sig.get("status", "")
    kdj_cross = kdj_sig.get("cross", "")
    j_val = kdj_sig.get("j", None)
    macd_trend = macd_sig.get("trend", "")
    macd_cross = macd_sig.get("cross", "")
    hist_state = macd_sig.get("hist_state", "")
    close = price.get("close")

    rating = "中性观望"
    reason_parts = []
    entry_hint = "暂不建议主动买入，等待更明确的技术信号。"

    # 条件一：下跌/调整后出现 KDJ 低位金叉
    low_kdj_buy = (
            kdj_cross == "金叉"
            and isinstance(j_val, (int, float)) and j_val < 40
    )

    # 条件二：MACD 由空转多，或刚金叉
    macd_turning_bull = (
            macd_trend == "多头"
            or macd_cross == "金叉"
            or (macd_trend == "震荡" and hist_state == "缩小")
    )

    # 条件三：价格在 BOLL 中轨/下轨一带
    near_support = ("下轨" in str(boll_sig)) or ("中轨" in str(boll_sig))

    if low_kdj_buy and macd_turning_bull and near_support:
        rating = "谨慎买入"
        reason_parts.append("KDJ 低位金叉，短线存在技术性反弹或资金进场迹象")
        reason_parts.append("MACD 显示多头或由空头转多头，趋势有转强信号")
        reason_parts.append("股价在布林中轨或下轨附近，技术上属于相对低位区域")
        if isinstance(close, (int, float)):
            entry_hint = f"可考虑在 {close * 0.97:.2f} ~ {close * 1.02:.2f} 区间分批试探性建仓，控制好仓位和止损。"
        else:
            entry_hint = "可考虑在当前价附近分批试探性建仓，控制好仓位和止损。"

    elif macd_trend == "多头" and kdj_status == "多头":
        rating = "趋势持有"
        reason_parts.append("KDJ、MACD 均处多头格局，整体趋势偏强")
        reason_parts.append("但 KDJ 可能已接近高位，短线存在一定回调压力")
        entry_hint = "已有仓位可继续持有，新仓建议等待回调或缩量整理后再考虑介入。"

    elif kdj_status == "空头" or macd_trend == "空头":
        rating = "谨慎观望"
        reason_parts.append("KDJ 或 MACD 显示空头格局，短线仍有下行或调整风险")
        entry_hint = "不建议追高买入，可等待指标企稳、出现金叉等明显转强信号后再考虑。"

    else:
        rating = "中性观望"
        reason_parts.append("主要技术指标信号中性或方向不明确")
        entry_hint = "可小仓位试探，重点观察后续量能变化及重要均线支撑是否有效。"

    reason = "；".join(reason_parts) if reason_parts else "技术信号较为中性。"
    return rating, reason, entry_hint


def format_tech_report(result: dict, use_color: bool = True) -> str:
    """专业版：技术分析报告 + 操作建议/买入节点"""
    if 'error' in result:
        return f"错误: {result['error']}"

    name = result.get('name', result.get('code', '未知'))
    code = result.get('code', '--')
    date = result.get('date', '--')

    price = result.get('price', {})
    close = price.get('close')
    open_ = price.get('open')
    high = price.get('high')
    low = price.get('low')
    volume = price.get('volume')
    pct_chg = price.get('pct_chg')

    ind = result.get('indicators', {})
    kdj = ind.get('kdj', {})
    macd = ind.get('macd', {})
    boll = ind.get('boll', {})
    ma = ind.get('ma', {})

    signals = result.get('signals', {})

    # 颜色函数
    def color(text, code):
        if not use_color:
            return text
        return f"\033[{code}m{text}\033[0m"

    # 涨跌颜色
    if isinstance(pct_chg, (int, float)):
        pct_str_raw = f"{pct_chg:+.2f}%"
        if pct_chg > 0:
            pct_str = color(pct_str_raw, "31")  # 红
        elif pct_chg < 0:
            pct_str = color(pct_str_raw, "32")  # 绿
        else:
            pct_str = pct_str_raw
    else:
        pct_str = "--"

    # 成交量简单格式化
    def fmt_volume(v):
        if not isinstance(v, (int, float)):
            return "--"
        if v >= 1e8:
            return f"{v / 1e8:.2f} 亿"
        if v >= 1e4:
            return f"{v / 1e4:.2f} 万"
        return str(v)

    # 操作建议（重点）
    rating, reason, entry_hint = judge_operation(price, signals)

    title = f"{name} ({code}) 技术分析报告 - {date}"

    # KDJ / MACD / BOLL 解读
    kdj_sig = signals.get("kdj", {})
    macd_sig = signals.get("macd", {})
    boll_sig = signals.get("boll", "--")

    kdj_status = kdj_sig.get("status", "—")
    kdj_cross = kdj_sig.get("cross", "—")
    j_val = kdj_sig.get("j", None)

    kdj_comment = f"- KDJ 当前处于 {kdj_status} 状态，近期 {kdj_cross}；J 值为 {safe_fmt(j_val)}。"
    if isinstance(j_val, (int, float)):
        if j_val > 80:
            kdj_comment += " 指标偏高，短线存在超买风险，需警惕回调。"
        elif j_val < 20:
            kdj_comment += " 指标偏低，短线处于超卖区，存在技术反弹的可能。"

    macd_trend = macd_sig.get("trend", "—")
    macd_cross = macd_sig.get("cross", "—")
    hist_state = macd_sig.get("hist_state", "—")
    macd_comment = (
        f"- MACD 当前整体为 {macd_trend} 格局，近期 {macd_cross}，柱状图变化为 {hist_state}。"
    )

    boll_comment = f"- 股价相对布林带位置：{boll_sig}。"

    lines = [
        "=" * len(title),
        title,
        "=" * len(title),
        "",
        "一、行情概览",
        f"1. 收盘价：{safe_fmt(close)} 元，涨跌幅：{pct_str}",
        f"2. 当日振幅：最高 {safe_fmt(high)} / 最低 {safe_fmt(low)}，开盘价：{safe_fmt(open_)}",
        f"3. 成交量：{fmt_volume(volume)}",
        "",
        "二、主要技术指标",
        f"1. KDJ 指标：K={safe_fmt(kdj.get('k'))}，D={safe_fmt(kdj.get('d'))}，J={safe_fmt(kdj.get('j'))}",
        f"2. MACD 指标：DIF={safe_fmt(macd.get('dif'), '{:.4f}')}, "
        f"DEA={safe_fmt(macd.get('dea'), '{:.4f}')}, MACD={safe_fmt(macd.get('macd'), '{:.4f}')}",
        f"3. 布林带(BOLL)：上轨={safe_fmt(boll.get('upper'))}，中轨={safe_fmt(boll.get('middle'))}，下轨={safe_fmt(boll.get('lower'))}",
        f"4. 均线(收盘价)：MA5={safe_fmt(ma.get('ma5'))}，MA10={safe_fmt(ma.get('ma10'))}，"
        f"MA20={safe_fmt(ma.get('ma20'))}，MA60={safe_fmt(ma.get('ma60'))}",
        "",
        "三、技术形态解读",
        kdj_comment,
        macd_comment,
        boll_comment,
        "",
        "四、综合判断与操作建议",
        f"【综合评级】{rating}",
        f"【技术依据】{reason}",
        f"【操作建议】{entry_hint}",
        "",
        "风险提示：以上内容仅为基于历史数据和技术指标的分析，不构成任何投资建议，"
        "股市有风险，投资需谨慎。",
    ]

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("用法: python stock_analyze.py <股票代码> [天数] [--json] [--report]")
        print("示例: python stock_analyze.py 600519 100 --report")
        sys.exit(1)

    code = sys.argv[1]
    days = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 100

    print(f"正在分析股票 {code}...")
    result = analyze_stock(code, days)

    args = sys.argv[3:]
    if "--json" in args:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif "--report" in args:
        print(format_tech_report(result))
    else:
        print(format_text(result))


if __name__ == "__main__":
    main()