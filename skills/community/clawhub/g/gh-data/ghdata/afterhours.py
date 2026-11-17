"""
盘后固定价格交易数据分析模块

数据源：腾讯行情 qt.gtimg.cn → fields[58]=盘后成交额(万元), fields[59]=盘后成交量(手)
采集：daily_update.py 步3c，每日1541只ETF，35秒完成
存储：etf_flow 表 → after_hours_vol, after_hours_amt

三类盘后信号：
  🔴活跃  (>100万) — 收盘后机构大举跟进，次日延续概率较高
  🟡有量  (>20万)  — 有一定盘后关注度
  ⚪清淡  (≤20万)  — 无参考价值

用法示例：
  from ghdata.afterhours import etf_afterhours_signal, sector_afterhours_ranking
  
  # 个股盘后信号
  signal = etf_afterhours_signal("688981")
  
  # 全市场盘后活跃板块排名
  rankings = sector_afterhours_ranking("2026-07-10")
  
  # 盘后因子（供预测引擎用）
  factor = afterhours_factor("688981")
"""

import sys
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime, date, timedelta

# ===== 导入依赖（分路径适配）=====
import os, sys

try:
    from . import db_manager as db
    from . import config
except ImportError:
    _BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _BASE not in sys.path:
        sys.path.insert(0, _BASE)
    from ghdata import db_manager as db
    from ghdata import config

# ===== 盘后活跃度阈值 =====
AFTER_HOURS_THRESHOLDS = {
    "active": 100,    # 🔴 活跃（万元）
    "moderate": 20,   # 🟡 有量（万元）
}


def _intensity_label(amt: float) -> Tuple[str, str]:
    """返回 (表情标签, 文字描述)"""
    if amt > AFTER_HOURS_THRESHOLDS["active"]:
        return "🔴", "活跃"
    elif amt > AFTER_HOURS_THRESHOLDS["moderate"]:
        return "🟡", "有量"
    return "⚪", "清淡"


# ====================================================================
# 公开 API
# ====================================================================

def etf_afterhours_signal(code: str, days: int = 5) -> dict:
    """
    查询个股关联ETF的盘后数据 + 信号
    
    Args:
        code: 股票代码（纯数字，如 "688981"）
        days: 查询最近N天，默认5
    
    Returns:
        {
            "code": "688981",
            "matched_etfs": [{"code": "512480", "name": "半导体ETF"}, ...],
            "after_hours": {
                "total_vol": 26580,        # 近N日盘后总成交量(手)
                "total_amt": 363.88,       # 近N日盘后总成交额(万元)
                "latest_vol": 26580,       # 最新一日盘后量
                "latest_amt": 363.88,      # 最新一日盘后额
                "latest_net_inflow": -740677968,  # 最新一日ETF净流入
                "intensity": "🔴",          # 活跃度表情
                "intensity_label": "活跃",   # 活跃度文字
                "daily_breakdown": [...]     # 每日明细
            },
            "signal": {
                "direction": "偏多",         # 盘后信号方向
                "confidence": "高",           # 置信度
                "note": "收盘后机构跟进买入，次日延续概率较高"
            }
        }
    """
    result = {
        "code": code,
        "matched_etfs": [],
        "after_hours": {},
        "signal": {}
    }

    # 获取ETF数据
    etf_data = db.get_etf_flow(code, days)
    if not etf_data:
        return result

    matched = etf_data.get("matched_etfs", [])
    result["matched_etfs"] = matched

    etf_dict = etf_data.get("etf_flow", {})
    if not etf_dict:
        return result

    # 汇总盘后数据
    total_vol = 0
    total_amt = 0
    daily_breakdown = []

    for ecode, rows in etf_dict.items():
        if not rows:
            continue
        for r in rows:
            vol = r.get("after_hours_vol", 0) or 0
            amt = r.get("after_hours_amt", 0) or 0
            total_vol += vol
            total_amt += amt
            daily_breakdown.append({
                "etf_code": ecode,
                "trade_date": r.get("trade_date", ""),
                "net_inflow": r.get("net_inflow", 0),
                "after_hours_vol": vol,
                "after_hours_amt": amt,
            })

    # 最新一天数据
    latest = daily_breakdown[-1] if daily_breakdown else {}
    latest_vol = latest.get("after_hours_vol", 0)
    latest_amt = latest.get("after_hours_amt", 0)
    latest_inflow = latest.get("net_inflow", 0)

    intensity_icon, intensity_text = _intensity_label(total_amt)

    # 信号判断
    signal = _judge_signal(total_amt, latest_inflow)

    result["after_hours"] = {
        "total_vol": total_vol,
        "total_amt": round(total_amt, 2),
        "latest_vol": latest_vol,
        "latest_amt": round(latest_amt, 2),
        "latest_net_inflow": latest_inflow,
        "intensity": intensity_icon,
        "intensity_label": intensity_text,
        "daily_breakdown": daily_breakdown,
    }
    result["signal"] = signal

    return result


def sector_afterhours_ranking(
    trade_date: Optional[str] = None,
    min_amt: float = 100,
    top_n: int = 20
) -> List[dict]:
    """
    查询指定日期全市场盘后活跃板块排名（WebAPI通道）

    Args:
        trade_date: 日期 YYYY-MM-DD（默认当天）
        min_amt:    最低盘后成交额门槛（万元），默认100=🔴活跃
        top_n:      返回前N条，默认20

    Returns:
        [{
            "rank": 1,
            "etf_code": "588170",
            "etf_name": "科创半导体ETF华夏",
            "net_inflow": -50000000,
            "after_hours_vol": 116692,
            "after_hours_amt": 1507.66,
            "intensity": "🔴",
            "signal": "⚠️ 分歧（净流出但盘后有人接）"
        }, ...]
    """
    raw = db.get_afterhours_ranking(trade_date or "", min_amt, top_n)
    if not raw:
        return []

    rankings = []
    for item in raw:
        inflow = item.get("net_inflow", 0) or 0
        amt = item.get("after_hours_amt", 0) or 0
        intensity_icon, _ = _intensity_label(amt)

        # 综合信号
        if inflow > 0 and amt > 500:
            signal = "🔥 强关注"
        elif inflow > 0:
            signal = "✅ 关注"
        elif amt > 500:
            signal = "⚠️ 分歧（净流出但盘后有人接）"
        else:
            signal = "👀 观察"

        rankings.append({
            "rank": item.get("rank", 0),
            "etf_code": item.get("etf_code", ""),
            "etf_name": item.get("etf_name", ""),
            "net_inflow": inflow,
            "after_hours_vol": int(item.get("after_hours_vol", 0) or 0),
            "after_hours_amt": round(amt, 2),
            "intensity": intensity_icon,
            "signal": signal,
        })

    return rankings


def afterhours_factor(code: str, days: int = 3) -> dict:
    """
    计算盘后因子（供T+1预测引擎使用）
    
    Args:
        code: 股票代码（纯数字）
        days: 取最近N天均值，默认3天
    
    Returns:
        {
            "factor": 0.5,           # 修正值：±0.5/±0.2/0
            "intensity": "🔴",        # 活跃度表情
            "label": "活跃",
            "total_amt": 363.88,     # N日盘后总额(万元)
            "note": "盘后活跃 → 偏多信心+0.5"
        }
    """
    signal = etf_afterhours_signal(code, days)
    ah = signal.get("after_hours", {})
    total_amt = ah.get("total_amt", 0)

    if total_amt > AFTER_HOURS_THRESHOLDS["active"]:
        factor = 0.5
        label = "活跃"
        note = "盘后活跃 → 偏多信心+0.5"
    elif total_amt > AFTER_HOURS_THRESHOLDS["moderate"]:
        factor = 0.2
        label = "有量"
        note = "盘后有量 → 偏多信心+0.2"
    else:
        factor = 0
        label = "清淡"
        note = "盘后清淡 → 不修正"

    return {
        "factor": factor,
        "intensity": "🔴" if factor >= 0.5 else "🟡" if factor >= 0.2 else "⚪",
        "label": label,
        "total_amt": total_amt,
        "note": note,
    }


def _judge_signal(total_amt: float, latest_inflow: float) -> dict:
    """盘后信号判断逻辑"""
    intensity_icon, intensity_text = _intensity_label(total_amt)

    if total_amt > AFTER_HOURS_THRESHOLDS["active"]:
        if latest_inflow > 0:
            return {
                "direction": "偏多",
                "confidence": "高",
                "note": f"ETF净流入 + 盘后{intensity_text}（{total_amt:.0f}万元），收盘后机构跟进买入，次日延续概率较高",
            }
        else:
            return {
                "direction": "分歧偏多",
                "confidence": "中",
                "note": f"ETF净流出但盘后{intensity_text}（{total_amt:.0f}万元），底部有机构试探性接盘，关注次日反弹信号",
            }
    elif total_amt > AFTER_HOURS_THRESHOLDS["moderate"]:
        return {
            "direction": "中性偏多",
            "confidence": "低",
            "note": f"盘后有一定成交（{total_amt:.0f}万元），关注度尚可",
        }
    else:
        return {
            "direction": "无信号",
            "confidence": "低",
            "note": "盘后成交清淡，无参考价值",
        }


# ====================================================================
# 便捷格式化输出
# ====================================================================

def format_afterhours_signal(signal: dict) -> str:
    """格式化盘后信号为可读文本（供LLM直接输出）"""
    ah = signal.get("after_hours", {})
    sig = signal.get("signal", {})
    matched = signal.get("matched_etfs", [])

    if not matched:
        return "该股票未关联行业ETF"

    etf_names = "、".join([e.get("name", "") for e in matched])
    intensity = ah.get("intensity", "⚪")
    label = ah.get("intensity_label", "清淡")
    amt = ah.get("latest_amt", 0)
    vol = ah.get("latest_vol", 0)
    inflow = ah.get("latest_net_inflow", 0)
    inflow_label = "净流入" if inflow >= 0 else "净流出"

    lines = [
        f"📊 ETF盘后信号（{etf_names}）",
        f"  · 关联ETF: {etf_names}",
        f"  · 当日ETF资金: {inflow_label} {abs(inflow)/10000:.0f}万元",
        f"  · 盘后成交: {intensity} {vol:.0f}手 / {amt:.1f}万元（{label}）",
        f"  · 信号方向: {sig.get('direction', '无')}",
        f"  · 说明: {sig.get('note', '')}",
    ]
    return "\n".join(lines)


def format_sector_ranking(rankings: List[dict], title: str = "📊 盘后活跃板块排名") -> str:
    """格式化板块排名为表格文本"""
    if not rankings:
        return "当日无盘后活跃板块"

    lines = [title, f"{'#':>3} {'ETF名称':<24} {'净流入(万)':>12} {'盘后量(手)':>12} {'盘后额(万)':>12} {'信号':<20}",
             "-" * 85]
    for r in rankings:
        inflow_wan = r["net_inflow"] / 10000
        lines.append(
            f"{r['rank']:>3} {r['etf_name']:<24} {inflow_wan:>+10.0f}万 "
            f"{r['after_hours_vol']:>10.0f} {r['after_hours_amt']:>10.1f}万 "
            f"{r['intensity']} {r['signal']:<16}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    # 命令行测试
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "signal"
    code = sys.argv[2] if len(sys.argv) > 2 else "688981"

    if cmd == "signal":
        s = etf_afterhours_signal(code)
        print(format_afterhours_signal(s))
    elif cmd == "factor":
        f = afterhours_factor(code)
        print(f"盘后因子: {f['factor']:+.1f} ({f['intensity']}{f['label']}) — {f['note']}")
    elif cmd == "ranking":
        date_str = sys.argv[2] if len(sys.argv) > 2 else "2026-07-10"
        r = sector_afterhours_ranking(date_str)
        print(format_sector_ranking(r))
    else:
        print("用法: python afterhours.py [signal|factor|ranking] [code|date]")
