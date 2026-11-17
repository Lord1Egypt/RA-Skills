#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
曙光盘中监控 v1.0 — 比赛版
用途: 实时监控持仓ETF，生成可执行建议
数据源: 腾讯GT(实时价) + HTSC query-indicator(技术指标/资金流)
"""

import os, sys, json, datetime, subprocess, re, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dawn_knowledge import DAWN_KNOWLEDGE

try:
    import requests
except ImportError:
    print("[ERROR] 需要 requests 库: pip install requests")
    sys.exit(1)

# ==================== 配置 ====================

HOLDINGS = {
    "515580": {"name": "科技100ETF", "weight": 0.416, "risk_limit": 0.40, "tag": "core"},
    "588090": {"name": "科创50ETF", "weight": 0.331, "risk_limit": 0.35, "tag": "core", "alert_level": 1.94},
    "560910": {"name": "电池ETF", "weight": 0.200, "risk_limit": 0.25, "tag": "satellite"},
    "513110": {"name": "纳指ETF", "weight": 0.054, "risk_limit": 0.07, "tag": "small"},
}

TOTAL_ASSETS = 1001718  # 昨日收盘总资产
INITIAL_CAPITAL = 997760
HIGH_WATER = 1023928

HTSC_QUERY = os.path.join(
    os.path.expanduser("~"), ".openclaw", "skills", "query-indicator", "query_indicator.py"
)


# ==================== 数据获取 ====================

def get_real_time(code: str) -> dict:
    """从腾讯GT获取实时行情"""
    if code.isdigit():
        prefix = "sh" if code.startswith(("5", "6")) else "sz"
        gt_code = f"{prefix}{code}"
    else:
        gt_code = code

    url = f"https://qt.gtimg.cn/q={gt_code}"
    try:
        r = requests.get(url, timeout=5)
        r.encoding = "gbk"
        parts = r.text.split("~")
        if len(parts) < 38:
            return {"error": f"数据不完整({len(parts)}字段)"}
        
        return {
            "code": code,
            "name": parts[1],
            "price": float(parts[3]),
            "prev_close": float(parts[4]),
            "open": float(parts[5]),
            "high": float(parts[33]),
            "low": float(parts[34]),
            "change_pct": float(parts[32]),
            "volume": int(float(parts[6])),
            "amount_yi": round(float(parts[37]) / 1e8, 2) if parts[37] else 0,
        }
    except Exception as e:
        return {"error": str(e)}


def get_technicals(code: str, name: str) -> dict:
    """从HTSC query-indicator获取技术指标"""
    if not os.path.exists(HTSC_QUERY):
        return {"error": "query-indicator不可用"}
    
    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(
            ["py", "-X", "utf8", HTSC_QUERY, "queryIndicator", 
             "--query", f"{code}{name}今天MACD、KDJ、RSI、换手率、主力资金流向"],
            capture_output=True, text=True, encoding="utf-8", timeout=30,
        )
        output = result.stdout or result.stderr
        data = json.loads(output)
        if data.get("ok"):
            answer = data["data"]["answer"]
            return {"raw": answer, "parsed": _parse_technical(answer)}
        return {"error": data.get("error", {}).get("message", "未知错误")}
    except Exception as e:
        return {"error": str(e)}


def _parse_technical(text: str) -> dict:
    """从自然语言回答中提取结构化指标（支持多种格式）"""
    tech = {}
    
    # MACD: "MACD为0.023" / "MACD指标为0.048" / "MACD:0.023"
    m = re.search(r'MACD[是为：:]*\s*([-\d.]+)', text)
    if m: tech["macd"] = float(m.group(1))
    
    # KDJ J值: "KDJ的J值为103.706" / "J值103.706" / "J:103.706"
    m = re.search(r'(?:KDJ的|KDJ[是])?J\s*值?[是为：:]*\s*([\d.]+)', text)
    if m: tech["kdj_j"] = float(m.group(1))
    
    # RSI: "RSI为73.134" / "RSI:73.134" / "RSI73.134"
    m = re.search(r'RSI[是为：:]*\s*([\d.]+)', text)
    if m: tech["rsi"] = float(m.group(1))
    
    # 换手率: "换手率2.92%" / "换手率为2.92%"
    m = re.search(r'换手率[是为：:]*\s*([\d.]+)%', text)
    if m: tech["turnover"] = float(m.group(1))
    
    # 成交量: "成交量9.16万手" / "成交量2580.13万手"
    m = re.search(r'成交量\s*([\d.]+)万手', text)
    if m: tech["volume_wan"] = float(m.group(1))
    
    # 主力净流入: "主力净流入17.61万元" / "主力净流出XX万元"
    m_in = re.search(r'主力净流入\s*([\d.]+)万', text)
    m_out = re.search(r'主力净流出\s*([\d.]+)万', text)
    if m_in:
        tech["main_flow"] = float(m_in.group(1))
    elif m_out:
        tech["main_flow"] = -float(m_out.group(1))
    
    # 超大单净流入/流出
    m_in = re.search(r'超大单净流入\s*([\d.]+)万', text)
    m_out = re.search(r'超大单净流出\s*([\d.]+)万', text)
    if m_in:
        tech["super_large_flow"] = float(m_in.group(1))
    elif m_out:
        tech["super_large_flow"] = -float(m_out.group(1))
    
    # 涨跌幅: "涨跌幅2.27%" / "涨跌幅1.53%"
    m = re.search(r'涨跌幅\s*([-\d.]+)%', text)
    if m: tech["change_pct"] = float(m.group(1))
    
    # 大单净流入/流出
    m_in = re.search(r'(?:^|[^超])大单净流入\s*([\d.]+)万', text)
    m_out = re.search(r'(?:^|[^超])大单净流出\s*([\d.]+)万', text)
    if m_in:
        tech["large_flow"] = -float(m_in.group(1)) if 'out' in text else float(m_in.group(1))
    elif m_out:
        tech["large_flow"] = -float(m_out.group(1))
    
    return tech


def get_market_overview() -> dict:
    """大盘概况"""
    indices = {
        "上证指数": "sh000001", "深证成指": "sz399001",
        "创业板指": "sz399006", "科创50": "sh000688",
    }
    result = {}
    for name, code in indices.items():
        url = f"https://qt.gtimg.cn/q={code}"
        try:
            r = requests.get(url, timeout=5)
            r.encoding = "gbk"
            parts = r.text.split("~")
            if len(parts) > 32:
                result[name] = {
                    "price": float(parts[3]),
                    "change_pct": float(parts[32]),
                    "high": float(parts[33]) if parts[33] else 0,
                    "low": float(parts[34]) if parts[34] else 0,
                }
        except:
            pass
    return result


# ==================== 分析引擎 ====================

def analyze_position(code: str, rt: dict, tech: dict) -> dict:
    """分析单个持仓"""
    info = HOLDINGS.get(code, {})
    signals = []
    risk_level = "green"
    
    if "error" in rt:
        return {"error": rt["error"]}
    
    change_pct = rt.get("change_pct", 0)
    
    # === 风险信号 ===
    # 1. 科创50警戒线
    alert_level = info.get("alert_level")
    if alert_level and rt["price"] <= alert_level:
        signals.append({
            "type": "CRITICAL",
            "msg": f"{info['name']}跌破{alert_level}警戒线! 当前{rt['price']}",
            "action": "收盘确认，跌破次日减仓50%"
        })
        risk_level = "red"
    elif alert_level and rt["price"] <= alert_level * 1.02:
        signals.append({
            "type": "WARN",
            "msg": f"{info['name']}接近{alert_level}警戒线",
            "action": "密切关注，不操作"
        })
        risk_level = "yellow"
    
    # 2. 日内急拉>3%
    if change_pct > 3:
        signals.append({
            "type": "SIGNAL",
            "msg": f"{info['name']}日内急拉{change_pct:+.2f}%",
            "action": "考虑小波段减3-5%仓位"
        })
    elif change_pct > 2:
        signals.append({
            "type": "INFO",
            "msg": f"{info['name']}涨幅{change_pct:+.2f}%，走势良好"
        })
    
    # 3. 日内急跌>2%
    if change_pct < -2:
        signals.append({
            "type": "WARN",
            "msg": f"{info['name']}急跌{change_pct:+.2f}%",
            "action": "不恐慌加仓，等收盘确认"
        })
    
    # 4. 仓位超限
    if info.get("weight", 0) > info.get("risk_limit", 1):
        signals.append({
            "type": "WARN",
            "msg": f"{info['name']}仓位{info['weight']*100:.1f}%超上限{info['risk_limit']*100:.0f}%",
            "action": "收盘前减至上限以下"
        })
    
    # === 技术面分析 ===
    tech_parsed = tech.get("parsed", {})
    if tech_parsed:
        kdj = tech_parsed.get("kdj_j", 0)
        rsi = tech_parsed.get("rsi", 0)
        macd = tech_parsed.get("macd", 0)
        
        if kdj > 100:
            signals.append({
                "type": "WARN",
                "msg": f"{info['name']} KDJ-J值{kdj:.1f}，超买区域",
                "action": "短期有回调压力，不追高"
            })
        if rsi > 70:
            signals.append({
                "type": "INFO",
                "msg": f"{info['name']} RSI{rsi:.1f}，临近超买"
            })
        if macd and change_pct > 0:
            signals.append({
                "type": "INFO",
                "msg": f"{info['name']} MACD上行，多头动能持续"
            })
    
    return {
        "code": code,
        "name": info.get("name", rt.get("name", code)),
        "price": rt.get("price", 0),
        "change_pct": change_pct,
        "weight": info.get("weight", 0),
        "risk_level": risk_level,
        "signals": signals,
        "technicals": tech_parsed,
    }


def total_summary(positions: list, market: dict) -> dict:
    """全仓汇总"""
    total_gain = 0
    position_details = []
    
    for p in positions:
        if "error" in p:
            continue
        gain = TOTAL_ASSETS * p["weight"] * p["change_pct"] / 100
        total_gain += gain
        position_details.append(p)
    
    est_total = TOTAL_ASSETS + total_gain
    
    return {
        "timestamp": datetime.datetime.now().strftime("%H:%M"),
        "market": market,
        "positions": position_details,
        "total_gain": round(total_gain),
        "est_total_assets": round(est_total),
        "day_return": round(total_gain / TOTAL_ASSETS * 100, 2),
        "cumulative_return": round((est_total - INITIAL_CAPITAL) / INITIAL_CAPITAL * 100, 2),
        "to_high_water": round(est_total - HIGH_WATER),
        "critical_signals": sum(1 for p in position_details if p["risk_level"] == "red"),
        "warn_signals": sum(1 for p in position_details if p["risk_level"] == "yellow"),
    }


# ==================== 输出 ====================

def format_trading_suggestion(summary: dict) -> str:
    """生成简洁的操盘建议"""
    lines = []
    now = datetime.datetime.now()
    now_str = now.strftime('%m-%d %H:%M')
    lines.append(f"曙光监控 | {now_str}")
    assets_str = f"{summary['est_total_assets']:,}"
    lines.append(f"总资产: ~{assets_str} | 今日: {summary['day_return']:+.2f}% | 累计: {summary['cumulative_return']:+.2f}%")
    hw = f"{summary['to_high_water']:+,}"
    lines.append(f"距新高: {hw} | 警戒/预警: {summary['critical_signals']}/{summary['warn_signals']}")
    lines.append("")
    
    # 大盘
    lines.append("【大盘】")
    for name, idx in summary.get("market", {}).items():
        pct = idx.get("change_pct", 0)
        arrow = "↑" if pct > 0 else "↓" if pct < 0 else "→"
        lines.append(f"  {name}: {idx['price']} {arrow} {pct:+.2f}%")
    lines.append("")
    
    # 持仓
    lines.append("【持仓】")
    for p in summary["positions"]:
        arrow = "↑" if p["change_pct"] > 0 else "↓" if p["change_pct"] < 0 else "→"
        level_icon = {"green": "○", "yellow": "△", "red": "●"}.get(p["risk_level"], "○")
        name = f"{p['name']}({p['code']})"
        line = f"  {level_icon} {name}: {p['price']} {arrow} {p['change_pct']:+.2f}% | 仓位{p['weight']*100:.1f}%"
        lines.append(line)
    lines.append("")
    
    # 信号
    has_signals = False
    for p in summary["positions"]:
        for sig in p.get("signals", []):
            has_signals = True
            icon = {"CRITICAL": "!!!", "WARN": "!!", "SIGNAL": "!", "INFO": "i"}.get(sig["type"], "?")
            lines.append(f"  [{icon}] {sig['msg']}")
            if sig.get("action"):
                lines.append(f"      建议: {sig['action']}")
    
    if not has_signals:
        lines.append("  无操作信号，持仓不动")
    
    # 技术面
    lines.append("")
    lines.append("【技术面】")
    for p in summary["positions"]:
        t = p.get("technicals", {})
        if t:
            parts = []
            if "macd" in t: parts.append(f"MACD:{t['macd']}")
            if "kdj_j" in t: parts.append(f"J:{t['kdj_j']:.0f}")
            if "rsi" in t: parts.append(f"RSI:{t['rsi']:.0f}")
            if "turnover" in t: parts.append(f"换手:{t['turnover']:.1f}%")
            if "main_flow" in t: parts.append(f"主力:{t['main_flow']:+.0f}万")
            lines.append(f"  {p['name']}: {' | '.join(parts)}")
    
    if now.hour >= 14 and now.hour < 15:
        lines.append("")
        lines.append("【尾盘提醒】距收盘<30分钟，暂不操作，等收盘再决定")
    
    return "\n".join(lines)


# ==================== 主流程 ====================

def run_monitor() -> dict:
    """执行一轮完整监控"""
    print("[OK] 开始监控扫描...", flush=True)
    
    # 1. 大盘
    market = get_market_overview()
    print(f"[OK] 大盘 {len(market)}/4 获取完成", flush=True)
    
    # 2. 持仓行情
    positions = []
    for code in HOLDINGS:
        rt = get_real_time(code)
        tech = get_technicals(code, HOLDINGS[code]["name"])
        status = "OK" if "error" not in rt else rt["error"]
        print(f"  {HOLDINGS[code]['name']}({code}): {status}", flush=True)
        pos = analyze_position(code, rt, tech)
        positions.append(pos)
    
    # 3. 汇总
    summary = total_summary(positions, market)
    return summary


def main():
    summary = run_monitor()
    report = format_trading_suggestion(summary)
    # Print to stderr to avoid GBK issues on Windows
    sys.stderr.write("\n" + "=" * 50 + "\n")
    sys.stderr.write(report + "\n")
    sys.stderr.write("=" * 50 + "\n")
    
    # 保存到临时文件，供其他脚本读取
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "_latest_monitor.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"\n[OK] 监控数据已保存: {out_path}")
    
    # 也写入html报告给兄弟看
    report_path = os.path.join(out_dir, "_monitor_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"[OK] 报告已保存: {report_path}")


if __name__ == "__main__":
    main()
