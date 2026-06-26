#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化报告模块

功能：
- 每日收盘报告
- 持仓股票日报
- 价格预警推送
- 异动股票监控
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# 避免循环导入，延迟导入
def _import_modules():
    from a_stock_watcher import get_stock_realtime, format_stock_info, check_risk_alert
    from historical_data import get_stock_history
    return get_stock_realtime, format_stock_info, check_risk_alert, get_stock_history

# ============== 配置文件 ==============
CONFIG_FILE = "stock_config.json"

def load_config() -> Dict:
    """加载配置文件"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"[加载配置失败]: {e}")
    
    # 默认配置
    return {
        "watchlist": ["600036", "000858", "300059"],  # 自选股
        "holdings": {  # 持仓
            "002892": {"name": "科力尔", "cost": 10.5, "shares": 1000}
        },
        "alerts": {  # 预警设置
            "price_targets": {},  # 目标价预警
            "change_threshold": 5.0,  # 涨跌幅预警阈值 (%)
            "volume_threshold": 200  # 成交量异常阈值 (%)
        },
        "notification": {  # 通知设置
            "enabled": True,
            "channel": "dingtalk",  # dingtalk/wechat/email
            "dingtalk_user_id": "235135121537852951"
        }
    }


def save_config(config: Dict):
    """保存配置文件"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[保存配置失败]: {e}")


# ============== 每日收盘报告 ==============
def generate_daily_report(stock_codes: List[str] = None) -> str:
    """
    生成每日收盘报告
    
    Args:
        stock_codes: 股票代码列表，默认使用配置中的自选股
    
    Returns:
        格式化的报告字符串
    """
    get_stock_realtime, _, _, _ = _import_modules()
    
    config = load_config()
    if not stock_codes:
        stock_codes = config.get("watchlist", [])
    
    if not stock_codes:
        return "❌ 未设置自选股列表"
    
    report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 A 股收盘报告
📅 日期：{datetime.now().strftime('%Y-%m-%d %H:%M')}
━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    summary = {
        "total": 0,
        "up": 0,
        "down": 0,
        "flat": 0,
        "best": None,
        "worst": None
    }
    
    stock_reports = []
    
    for code in stock_codes:
        result = get_stock_realtime(code)
        if not result.get("success"):
            continue
        
        summary["total"] += 1
        
        change_pct = result.get("change_pct", 0)
        if change_pct > 0:
            summary["up"] += 1
        elif change_pct < 0:
            summary["down"] += 1
        else:
            summary["flat"] += 1
        
        # 记录最佳/最差表现
        if summary["best"] is None or change_pct > summary["best"]["change_pct"]:
            summary["best"] = {"code": code, "name": result["name"], "change_pct": change_pct}
        if summary["worst"] is None or change_pct < summary["worst"]["change_pct"]:
            summary["worst"] = {"code": code, "name": result["name"], "change_pct": change_pct}
        
        # 简略信息
        stock_reports.append({
            "code": code,
            "name": result["name"],
            "price": result["current_price"],
            "change_pct": change_pct,
            "volume": result.get("volume", 0)
        })
    
    # 市场概览
    report += f"""
📈 市场概览:
  监控股票：{summary['total']}只
  上涨：{summary['up']}只 ({summary['up']/summary['total']*100:.1f}%)
  下跌：{summary['down']}只 ({summary['down']/summary['total']*100:.1f}%)
  平盘：{summary['flat']}只
"""
    
    if summary["best"]:
        report += f"\n🏆 最佳表现：{summary['best']['name']} ({summary['best']['code']}) {summary['best']['change_pct']:+.2f}%"
    if summary["worst"]:
        report += f"\n📉 最差表现：{summary['worst']['name']} ({summary['worst']['code']}) {summary['worst']['change_pct']:+.2f}%"
    
    # 个股详情
    report += f"\n\n📋 个股详情:\n"
    report += "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    
    # 按涨跌幅排序
    stock_reports.sort(key=lambda x: x["change_pct"], reverse=True)
    
    for stock in stock_reports:
        change_str = f"{stock['change_pct']:+.2f}%"
        arrow = "📈" if stock["change_pct"] > 0 else "📉" if stock["change_pct"] < 0 else "➖"
        report += f"{arrow} {stock['name']} ({stock['code']}): ¥{stock['price']:.2f} {change_str}\n"
    
    report += "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    
    return report


# ============== 持仓股票日报 ==============
def generate_holdings_report() -> str:
    """
    生成持仓股票日报
    
    Returns:
        格式化的持仓报告
    """
    get_stock_realtime, _, _, _ = _import_modules()
    
    config = load_config()
    holdings = config.get("holdings", {})
    
    if not holdings:
        return "❌ 未设置持仓信息"
    
    report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━
💼 持仓股票日报
📅 日期：{datetime.now().strftime('%Y-%m-%d %H:%M')}
━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    total_cost = 0
    total_market_value = 0
    total_profit = 0
    
    stock_reports = []
    
    for code, holding in holdings.items():
        result = get_stock_realtime(code)
        if not result.get("success"):
            continue
        
        cost_price = holding.get("cost", 0)
        shares = holding.get("shares", 0)
        current_price = result["current_price"]
        change_pct = result.get("change_pct", 0)
        
        cost_value = cost_price * shares
        market_value = current_price * shares
        profit = market_value - cost_value
        profit_pct = profit / cost_value * 100 if cost_value > 0 else 0
        
        total_cost += cost_value
        total_market_value += market_value
        total_profit += profit
        
        stock_reports.append({
            "code": code,
            "name": result["name"],
            "cost_price": cost_price,
            "current_price": current_price,
            "shares": shares,
            "cost_value": cost_value,
            "market_value": market_value,
            "profit": profit,
            "profit_pct": profit_pct,
            "change_pct": change_pct
        })
        
        # 个股详情
        report += f"""
📈 {result['name']} ({code})
  持仓：{shares:,}股
  成本：¥{cost_price:.2f} → 当前：¥{current_price:.2f}
  市值：¥{market_value:,.2f}
  盈亏：¥{profit:+,.2f} ({profit_pct:+.2f}%)
  今日：{change_pct:+.2f}%
"""
    
    # 汇总
    total_profit_pct = total_profit / total_cost * 100 if total_cost > 0 else 0
    report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 持仓汇总:
  总成本：¥{total_cost:,.2f}
  总市值：¥{total_market_value:,.2f}
  总盈亏：¥{total_profit:+,.2f} ({total_profit_pct:+.2f}%)
━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return report


# ============== 价格预警检查 ==============
def check_price_alerts() -> List[str]:
    """
    检查价格预警
    
    Returns:
        预警消息列表
    """
    get_stock_realtime, _, _, _ = _import_modules()
    
    config = load_config()
    alerts = []
    
    price_targets = config.get("alerts", {}).get("price_targets", {})
    
    for code, target in price_targets.items():
        result = get_stock_realtime(code)
        if not result.get("success"):
            continue
        
        current_price = result["current_price"]
        target_price = target.get("price", 0)
        direction = target.get("direction", "up")
        
        triggered = False
        if direction == "up" and current_price >= target_price:
            triggered = True
            msg = f"🚨【预警触发】{result['name']} ({code})\n"
            msg += f"当前价：¥{current_price:.2f} | 目标价：¥{target_price:.2f} (涨至)\n"
            msg += f"⏰ 触发时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            alerts.append(msg)
        
        elif direction == "down" and current_price <= target_price:
            triggered = True
            msg = f"🚨【预警触发】{result['name']} ({code})\n"
            msg += f"当前价：¥{current_price:.2f} | 目标价：¥{target_price:.2f} (跌至)\n"
            msg += f"⏰ 触发时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            alerts.append(msg)
    
    return alerts


# ============== 异动股票监控 ==============
def check_abnormal_stocks(stock_codes: List[str] = None) -> List[Dict]:
    """
    监控异动股票（涨跌幅/成交量异常）
    
    Args:
        stock_codes: 股票代码列表
    
    Returns:
        异动股票列表
    """
    get_stock_realtime, _, _, get_stock_history = _import_modules()
    
    config = load_config()
    if not stock_codes:
        stock_codes = config.get("watchlist", [])
    
    change_threshold = config.get("alerts", {}).get("change_threshold", 5.0)
    volume_threshold = config.get("alerts", {}).get("volume_threshold", 200)
    
    abnormal_stocks = []
    
    for code in stock_codes:
        result = get_stock_realtime(code)
        if not result.get("success"):
            continue
        
        change_pct = abs(result.get("change_pct", 0))
        volume = result.get("volume", 0)
        
        # 获取 5 日平均成交量
        history = get_stock_history(code, days=6)
        if history.get("success") and len(history["volume"]) >= 2:
            avg_volume = sum(history["volume"][-5:-1]) / 5
            volume_ratio = volume / avg_volume * 100 if avg_volume > 0 else 100
        else:
            volume_ratio = 100
        
        is_abnormal = False
        reasons = []
        
        # 检查涨跌幅异常
        if change_pct >= change_threshold:
            is_abnormal = True
            reasons.append(f"涨跌幅 {result['change_pct']:+.2f}%")
        
        # 检查成交量异常
        if volume_ratio >= volume_threshold:
            is_abnormal = True
            reasons.append(f"成交量 {volume_ratio:.0f}% (5 日均)")
        
        if is_abnormal:
            abnormal_stocks.append({
                "code": code,
                "name": result["name"],
                "price": result["current_price"],
                "change_pct": result["change_pct"],
                "volume": volume,
                "volume_ratio": volume_ratio,
                "reasons": reasons
            })
    
    return abnormal_stocks


def generate_abnormal_report(abnormal_stocks: List[Dict]) -> str:
    """
    生成异动股票报告
    
    Args:
        abnormal_stocks: 异动股票列表
    
    Returns:
        格式化的报告
    """
    if not abnormal_stocks:
        return "✅ 无异动股票"
    
    report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 异动股票监控
📅 时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    for stock in abnormal_stocks:
        report += f"""
📈 {stock['name']} ({stock['code']})
  当前价：¥{stock['price']:.2f} ({stock['change_pct']:+.2f}%)
  成交量：{stock['volume']:,}手 ({stock['volume_ratio']:.0f}% vs 5 日均)
  异动原因：{' | '.join(stock['reasons'])}
"""
    
    report += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    
    return report


# ============== 综合日报 ==============
def generate_comprehensive_daily_report() -> str:
    """
    生成综合日报（收盘报告 + 持仓报告 + 异动监控）
    
    Returns:
        完整的日报
    """
    config = load_config()
    
    report = f"""
╔══════════════════════════════════════╗
║        A 股投资日报                  ║
║        {datetime.now().strftime('%Y-%m-%d %H:%M')}                    ║
╚══════════════════════════════════════╝
"""
    
    # 1. 收盘报告
    report += "\n" + generate_daily_report()
    
    # 2. 持仓报告
    if config.get("holdings"):
        report += "\n" + generate_holdings_report()
    
    # 3. 异动监控
    abnormal = check_abnormal_stocks()
    report += "\n" + generate_abnormal_report(abnormal)
    
    # 4. 预警检查
    alerts = check_price_alerts()
    if alerts:
        report += "\n🚨 价格预警:\n"
        for alert in alerts:
            report += f"{alert}\n\n"
    
    report += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    report += "⚠️ 风险提示：本报告仅供参考，不构成投资建议\n"
    report += "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    
    return report


# ============== 配置管理 ==============
def add_to_watchlist(stock_code: str, stock_name: str = None) -> str:
    """添加到自选股"""
    config = load_config()
    
    if stock_code not in config["watchlist"]:
        config["watchlist"].append(stock_code)
        save_config(config)
        return f"✅ 已将 {stock_name or stock_code} 添加到自选股"
    else:
        return f"⚠️ {stock_code} 已在自选股中"


def remove_from_watchlist(stock_code: str) -> str:
    """从自选股移除"""
    config = load_config()
    
    if stock_code in config["watchlist"]:
        config["watchlist"].remove(stock_code)
        save_config(config)
        return f"✅ 已将 {stock_code} 从自选股移除"
    else:
        return f"❌ {stock_code} 不在自选股中"


def add_holding(stock_code: str, cost: float, shares: int, stock_name: str = None) -> str:
    """添加持仓"""
    config = load_config()
    
    config["holdings"][stock_code] = {
        "name": stock_name,
        "cost": cost,
        "shares": shares
    }
    save_config(config)
    
    return f"✅ 已添加持仓：{stock_name or stock_code} 成本¥{cost:.2f} × {shares}股"


def set_price_alert(stock_code: str, direction: str, target_price: float) -> str:
    """设置价格预警"""
    config = load_config()
    
    if "alerts" not in config:
        config["alerts"] = {"price_targets": {}}
    if "price_targets" not in config["alerts"]:
        config["alerts"]["price_targets"] = {}
    
    config["alerts"]["price_targets"][stock_code] = {
        "direction": direction,
        "price": target_price,
        "set_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    save_config(config)
    
    direction_str = "涨至" if direction == "up" else "跌至"
    return f"✅ 已设置 {stock_code} 预警：{direction_str} ¥{target_price:.2f}"


# ============== 测试 ==============
if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("=" * 60)
    print("自动化报告模块测试")
    print("=" * 60)
    
    # 测试收盘报告
    print("\n[测试] 每日收盘报告")
    print("-" * 60)
    report = generate_daily_report(["600036", "000858", "300059"])
    print(report)
    
    # 测试持仓报告
    print("\n[测试] 持仓股票日报")
    print("-" * 60)
    report = generate_holdings_report()
    print(report)
    
    # 测试异动监控
    print("\n[测试] 异动股票监控")
    print("-" * 60)
    abnormal = check_abnormal_stocks(["600036", "000858", "300059", "002892"])
    print(generate_abnormal_report(abnormal))
