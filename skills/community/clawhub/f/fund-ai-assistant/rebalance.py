#!/usr/bin/env python3
"""
基金组合再平衡检测引擎
用于计算实际持仓偏离度，并生成调仓建议

使用方式:
  python3 rebalance.py              # 完整报告（含推送）
  python3 rebalance.py --dry-run     # 仅输出，不推送
  python3 rebalance.py --threshold  # 仅显示超阈值项
"""

import json
import sys
from datetime import datetime
from typing import Dict, List

# ============ 配置区 ============
TOTALPortfolio = 10000  # 示例总投资金额（元），请替换为你的实际总投入

# 目标仓位矩阵（示例模板：稳健型，1-3年）
TARGET_ALLOCATION = {
    "000001": {"name": "示例混合型基金A",   "target": 0.25, "threshold": 0.05, "category": "混合型"},
    "000002": {"name": "示例混合型基金B",   "target": 0.15, "threshold": 0.05, "category": "混合型"},
    "000003": {"name": "示例债券型基金",     "target": 0.30, "threshold": 0.05, "category": "债券型"},
    "000004": {"name": "示例黄金ETF联接",   "target": 0.15, "threshold": 0.05, "category": "黄金"},
    "000005": {"name": "示例养老FOF",       "target": 0.10, "threshold": 0.03, "category": "养老FOF"},
    "000006": {"name": "示例白银LOF",       "target": 0.05, "threshold": 0.03, "category": "白银"},
}

# ============ 数据加载 ============

def load_positions():
    """从 positions.json 加载当前持仓"""
    pos_path = os.path.join(os.path.dirname(__file__), "positions.json")
    try:
        with open(pos_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] 读取持仓失败: {e}")
        return {}

def load_fund_navs():
    """从 latest_nav.json 加载最新净值"""
    nav_path = os.path.join(os.path.dirname(__file__), "latest_nav.json")
    try:
        with open(nav_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] 读取净值失败: {e}")
        return {}

def fetch_latest_navs():
    """实时获取基金净值"""
    import urllib.request
    import json as json_lib

    navs = {}
    tracked = list(TARGET_ALLOCATION.keys())

    for code in tracked:
        try:
            url = f"https://fundgz.1234567.com.cn/js/{code}.js?rt=1700000000"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                text = resp.read().decode("utf-8")
            # 格式: jsonpgz({"code":"000001","name":"...","gsz":"2.3080","gztime":"..."});
            # 需要去掉 "jsonpgz(" 前缀和尾部 ");"
            json_str = text.strip()
            if json_str.startswith("jsonpgz("):
                json_str = json_str[len("jsonpgz("):]
            json_str = json_str.rstrip(");").rstrip(";")
            data = json_lib.loads(json_str)
            gsz = data.get("gsz", "")
            jz = data.get("jz", "")
            nav = float(gsz) if gsz else (float(jz) if jz else 0)
            navs[code] = nav
        except Exception as e:
            print(f"[WARN] 获取 {code} 净值失败: {e}")
            navs[code] = None
    return navs

# ============ 核心计算 ============

def calculate_current_value(positions: Dict, navs: Dict) -> Dict:
    """计算每个基金的当前市值和占比"""
    holdings = {}
    total_value = 0.0

    for code, records in positions.items():
        if code not in TARGET_ALLOCATION:
            continue
        total_shares = sum(r["quantity"] for r in records if r["type"] == "buy")
        sell_shares = sum(r["quantity"] for r in records if r["type"] == "sell")
        net_shares = total_shares - sell_shares

        nav = navs.get(code)
        if nav is None or nav <= 0:
            # 兜底：用持仓记录中的最新买入价
            if records:
                nav = records[-1]["price"]
            else:
                nav = 0

        market_value = net_shares * nav
        total_value += market_value
        holdings[code] = {
            "shares": net_shares,
            "nav": nav,
            "market_value": market_value,
            "name": TARGET_ALLOCATION[code]["name"]
        }

    # 计算实际占比
    if total_value > 0:
        for code in holdings:
            holdings[code]["actual_ratio"] = holdings[code]["market_value"] / total_value
    else:
        for code in holdings:
            holdings[code]["actual_ratio"] = 0.0

    return holdings, total_value

def calculate_deviation(holdings: Dict, total_value: float) -> List[Dict]:
    """计算偏离度"""
    deviations = []

    for code, cfg in TARGET_ALLOCATION.items():
        target = cfg["target"]
        threshold = cfg["threshold"]
        holding = holdings.get(code, {"market_value": 0, "actual_ratio": 0, "shares": 0, "nav": 0})

        actual_ratio = holding.get("actual_ratio", 0)
        actual_value = holding.get("market_value", 0)
        deviation = actual_ratio - target

        status = "✅" if abs(deviation) <= threshold else "⚠️"

        deviations.append({
            "code": code,
            "name": cfg["name"],
            "category": cfg["category"],
            "target_ratio": target,
            "actual_ratio": actual_ratio,
            "target_value": TOTALPortfolio * target,
            "actual_value": actual_value,
            "deviation": deviation,
            "threshold": threshold,
            "status": status,
            "action_needed": abs(deviation) > threshold,
            "action": get_action(deviation, threshold, cfg["category"]),
        })

    # 计算总体偏离度（相对于目标总额）
    total_deviation = sum(abs(d["deviation"]) * TOTALPortfolio for d in deviations)
    return deviations, total_deviation

    # 按偏离度排序（超阈值优先）
    deviations.sort(key=lambda x: -abs(x["deviation"]))
    return deviations

def get_action(deviation: float, threshold: float, category: str) -> str:
    """生成调仓建议"""
    if abs(deviation) <= threshold:
        return "持有"

    direction = "减仓" if deviation > 0 else "加仓"
    amount = abs(deviation) * TOTALPortfolio
    action_word = "卖出" if deviation > 0 else "买入"

    return f"建议{direction} {amount:.0f}元"

# ============ 报告生成 ============

def generate_report(deviations: List[Dict], total_deviation: float, total_value: float, dry_run: bool = False) -> str:
    """生成再平衡报告"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"📊 组合健康度报告 | {now}",
        f"━━━━━━━━━━━━━━━━━━━━━━",
        f"当前总市值：{total_value:.2f} 元（目标 {TOTALPortfolio:.2f} 元）",
        f"总体偏离度：{total_deviation:.0f} 元",
        f"偏离度阈值：混合/债券/黄金 ±5% | 养老FOF ±3% | 白银 ±2%",
        "",
    ]

    # 按品类分组显示
    categories = {}
    for d in deviations:
        cat = d["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(d)

    for cat, items in categories.items():
        lines.append(f"【{cat}】")
        for item in items:
            dev_pct = item["deviation"] * 100
            sign = "+" if dev_pct > 0 else ""
            target_pct = item["target_ratio"] * 100
            actual_pct = item["actual_ratio"] * 100

            if item["action_needed"]:
                lines.append(
                    f"  {item['status']} {item['code']} {item['name']}\n"
                    f"     实际 {actual_pct:.1f}% ↔ 目标 {target_pct:.1f}% {sign}{dev_pct:.1f}%\n"
                    f"     {item['action']}"
                )
            else:
                lines.append(
                    f"  {item['status']} {item['code']} {item['name']}\n"
                    f"     实际 {actual_pct:.1f}% ↔ 目标 {target_pct:.1f}% {sign}{dev_pct:.1f}% 正常"
                )
        lines.append("")

    # 汇总
    alert_items = [d for d in deviations if d["action_needed"]]
    if alert_items:
        lines.append(f"⚠️ 共 {len(alert_items)} 项需要关注")
    else:
        lines.append("✅ 组合状态正常，无需调整")

    if dry_run:
        lines.append("")
        lines.append("[dry-run 模式，未推送]")

    return "\n".join(lines)

# ============ 主流程 ============

def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    threshold_only = "--threshold" in args

    # 加载数据
    positions = load_positions()
    navs = fetch_latest_navs()

    if not navs:
        print("[ERROR] 无法获取净值，退出")
        sys.exit(1)

    # 计算
    holdings, total_value = calculate_current_value(positions, navs)
    deviations, total_deviation = calculate_deviation(holdings, total_value)

    # 输出
    if threshold_only:
        for d in deviations:
            if d["action_needed"]:
                print(f"{d['code']} {d['name']}: {d['action']}")
    else:
        report = generate_report(deviations, total_deviation, total_value, dry_run)
        print(report)

    # 返回退出码：0=正常，1=有超阈值
    if any(d["action_needed"] for d in deviations):
        sys.exit(0 if threshold_only else 1)
    sys.exit(0)

if __name__ == "__main__":
    main()
