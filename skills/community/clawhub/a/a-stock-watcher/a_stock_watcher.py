#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股盯盘技能 - 多数据源增强版
功能：实时查价、价格预警、持续监控、风险提示、操盘建议、技术分析

数据源架构：
- 主数据源：东方财富 API (延迟 1-3 秒，A 股最优)
- 备用数据源：腾讯财经 API (延迟 5-15 秒，支持港股/美股)
- 降级方案：新浪财经 API (延迟 5-20 秒，备份)

所有数据源均完全免费，无需 API Key
"""

import requests
import time
import threading
import json
import re
from datetime import datetime
from typing import Dict, Optional, List, Tuple

# 导入技术分析模块
from technical_analysis import analyze_technical, format_analysis_report
# 导入历史数据模块
from historical_data import get_stock_history
# 导入自动化报告模块
from auto_report import (
    generate_daily_report, 
    generate_holdings_report, 
    generate_comprehensive_daily_report,
    add_to_watchlist, 
    remove_from_watchlist,
    add_holding,
    set_price_alert
)
# 导入智能投顾模块
from investment_advisor import (
    assess_risk_profile,
    format_risk_assessment,
    calculate_stop_loss_stop_profit,
    format_stop_loss_report,
    pe_relative_valuation,
    format_valuation_report,
    calculate_portfolio_optimization,
    format_portfolio_optimization,
    RISK_QUESTIONS
)

# ============== 全局状态 ==============
watch_tasks: Dict[str, dict] = {}
task_lock = threading.Lock()

# 数据源优先级
DATA_SOURCES = ["eastmoney", "tencent", "sina"]

# ============== 风险提示配置 ==============
RISK_THRESHOLDS = {
    "surge": 7.0,      # 暴涨提醒：涨幅 >= 7%
    "plunge": -7.0,    # 暴跌提醒：涨幅 <= -7%
    "high_volatility": 5.0,  # 高波动：涨跌幅绝对值 >= 5%
}

# ============== 操盘建议规则 ==============
def get_trading_advice(stock_data: dict) -> str:
    """
    基于简单规则给出操盘建议
    注意：仅供参考，不构成投资建议
    """
    change_pct = stock_data.get("change_pct", 0)
    current_price = stock_data.get("current_price", 0)
    pre_close = stock_data.get("pre_close", 0)
    high = stock_data.get("high", 0)
    low = stock_data.get("low", 0)
    
    advice = []
    
    # 涨跌幅建议
    if change_pct >= 9.5:
        advice.append("⚠️ 涨停附近，注意回调风险")
    elif change_pct >= 7:
        advice.append("📈 强势上涨，持有者可继续持有")
    elif change_pct >= 3:
        advice.append("📈 温和上涨，趋势向好")
    elif change_pct <= -9.5:
        advice.append("⚠️ 跌停附近，注意风险")
    elif change_pct <= -7:
        advice.append("📉 大幅下跌，注意止损位")
    elif change_pct <= -3:
        advice.append("📉 弱势下跌，观望为主")
    
    # 高低点判断
    if pre_close > 0:
        high_ratio = (high - pre_close) / pre_close * 100
        low_ratio = (low - pre_close) / pre_close * 100
        
        if high_ratio >= 5 and change_pct < 2:
            advice.append("⚠️ 冲高回落，上方压力大")
        if low_ratio <= -5 and change_pct > -2:
            advice.append("💪 探底回升，下方有支撑")
    
    # 综合建议
    if not advice:
        advice.append("➖ 震荡整理，方向不明")
    
    return " | ".join(advice)

# ============== 东方财富 API ==============
def get_stock_eastmoney(stock_code: str) -> dict:
    """
    东方财富 API - 主数据源（A 股最优）
    延迟：1-3 秒
    支持：A 股、基金、债券
    
    接口文档：http://push2.eastmoney.com/api/qt/stock/get
    
    字段说明 (价格单位：分，需要除以 100):
    f43: 现价 | f44: 开盘 | f45: 昨收
    f49: 成交量 (手) | f50: 换手率 | f55: 涨幅%
    f57: 代码 | f58: 名称 | f169: 涨跌额 (分) | f170: 涨幅%*100
    """
    try:
        # 适配股票代码格式
        if stock_code.startswith('6'):
            secid = f"1.{stock_code}"  # 上证
            market = "上证"
        elif stock_code.startswith(('0', '3')):
            secid = f"0.{stock_code}"  # 深证
            market = "深证"
        else:
            return None  # 不支持的代码格式
        
        # 东方财富 API 字段
        fields = "f43,f44,f45,f49,f50,f55,f57,f58,f169,f170"
        url = f"http://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields={fields}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://quote.eastmoney.com/"
        }
        
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        
        if data.get("rc") == 0 and data.get("data"):
            stock = data["data"]
            current_price = stock.get("f43", 0) / 100  # 价格除以 100
            pre_close = stock.get("f45", 0) / 100
            open_price = stock.get("f44", 0) / 100
            volume = stock.get("f49", 0)  # 成交量 (手)
            turnover_rate = stock.get("f50", 0)  # 换手率%
            change_pct = stock.get("f55", 0)  # 涨幅%
            name = stock.get("f58", "").strip()
            
            # 计算涨跌额
            change = stock.get("f169", 0) / 100 if stock.get("f169") else current_price - pre_close
            
            # 如果 API 返回的涨幅为 0，手动计算
            if change_pct == 0 and pre_close > 0:
                change_pct = (change / pre_close) * 100
            
            # 最高/最低价暂时用开盘价代替（东方财富快照 API 限制）
            high = open_price if open_price > current_price else current_price
            low = open_price if open_price < current_price else current_price
            
            # 估算成交额 (成交量 * 均价，单位：万元)
            amount = (volume * current_price) / 100  # 手 * 元 / 100 = 万元
            
            return {
                "success": True,
                "source": "eastmoney",
                "code": stock_code,
                "market": market,
                "name": name,
                "current_price": current_price,
                "change": change,
                "change_pct": change_pct,
                "pre_close": pre_close,
                "open": open_price,
                "high": high,
                "low": low,
                "volume": volume,
                "amount": amount,
                "turnover_rate": turnover_rate,
                "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            return None
    
    except Exception as e:
        print(f"[东方财富 API 错误]: {e}")
        return None


# ============== 腾讯财经 API ==============
def get_stock_tencent(stock_code: str) -> dict:
    """
    腾讯财经 API - 主数据源（数据最完整）
    延迟：5-15 秒
    支持：A 股、港股、美股、期货、外汇
    
    接口文档：http://qt.gtimg.cn/q=[市场代码]
    
    字段说明 (~分隔):
    [0]未知 [1]名称 [2]代码 [3]现价 [4]昨收 [5]开盘 [6]成交量 (手)
    [33]最高 [34]最低 [37]成交额 (万元)
    """
    try:
        # 适配股票代码格式
        if stock_code.startswith('6'):
            tencent_code = f"sh{stock_code}"
            market = "上证"
            response_prefix = "v_sh"
        elif stock_code.startswith(('0', '3')):
            tencent_code = f"sz{stock_code}"
            market = "深证"
            response_prefix = "v_sz"
        elif stock_code.startswith('hk'):
            tencent_code = stock_code  # hk00700
            market = "港股"
            response_prefix = "v_hk"
        elif stock_code.startswith('us'):
            tencent_code = stock_code  # usAAPL
            market = "美股"
            response_prefix = "v_us"
        else:
            return None
        
        url = f"http://qt.gtimg.cn/q={tencent_code}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://stockapp.finance.qq.com/"
        }
        
        response = requests.get(url, headers=headers, timeout=5)
        # 手动解码 GBK
        content = response.content.decode('gbk', errors='replace')
        
        # 解析腾讯数据格式：v_sh600036="..."
        # 注意：response_prefix 已经是 "v_sh"，tencent_code 是 "sh600036"
        # 所以匹配模式应该是 v_sh600036，即 response_prefix + stock_code
        match = re.search(rf'{response_prefix}{stock_code}="([^"]+)"', content)
        if match:
            data_str = match.group(1)
            fields = data_str.split('~')
            
            if len(fields) >= 40:
                name = fields[1] if len(fields) > 1 else ""
                current_price = float(fields[3]) if len(fields) > 3 and fields[3] else 0
                pre_close = float(fields[4]) if len(fields) > 4 and fields[4] else 0
                open_price = float(fields[5]) if len(fields) > 5 and fields[5] else 0
                high = float(fields[33]) if len(fields) > 33 and fields[33] else current_price
                low = float(fields[34]) if len(fields) > 34 and fields[34] else current_price
                volume = int(float(fields[6])) if len(fields) > 6 and fields[6] else 0
                amount = float(fields[37]) if len(fields) > 37 and fields[37] else 0
                
                # 计算涨跌幅
                change = current_price - pre_close
                change_pct = (change / pre_close) * 100 if pre_close > 0 else 0
                
                return {
                    "success": True,
                    "source": "tencent",
                    "code": stock_code,
                    "market": market,
                    "name": name,
                    "current_price": current_price,
                    "change": change,
                    "change_pct": change_pct,
                    "pre_close": pre_close,
                    "open": open_price,
                    "high": high,
                    "low": low,
                    "volume": volume,
                    "amount": amount,
                    "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
        
        return None
    
    except Exception as e:
        print(f"[腾讯财经 API 错误]: {e}")
        return None


# ============== 新浪财经 API ==============
def get_stock_sina(stock_code: str) -> dict:
    """
    新浪财经 API - 降级方案（备份）
    延迟：5-20 秒
    支持：A 股
    
    接口文档：http://hq.sinajs.cn/list=[市场代码]
    """
    try:
        # 适配代码格式
        if stock_code.startswith('6'):
            sina_code = f"sh{stock_code}"
            market = "上证"
        elif stock_code.startswith(('0', '3')):
            sina_code = f"sz{stock_code}"
            market = "深证"
        else:
            return None
        
        url = f"http://hq.sinajs.cn/list={sina_code}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'gbk'
        
        content = response.text
        if f'var hq_str_{sina_code}="' in content:
            data_str = content.split(f'var hq_str_{sina_code}="')[1].split('";')[0]
            fields = data_str.split(',')
            
            if len(fields) >= 32:
                name = fields[0]
                current_price = float(fields[3])
                pre_close = float(fields[2])
                open_price = float(fields[1])
                high = float(fields[4])
                low = float(fields[5])
                volume = int(fields[8])
                amount = float(fields[9])
                
                change = current_price - pre_close
                change_pct = (change / pre_close) * 100 if pre_close > 0 else 0
                
                return {
                    "success": True,
                    "source": "sina",
                    "code": stock_code,
                    "sina_code": sina_code,
                    "market": market,
                    "name": name,
                    "current_price": current_price,
                    "change": change,
                    "change_pct": change_pct,
                    "pre_close": pre_close,
                    "open": open_price,
                    "high": high,
                    "low": low,
                    "volume": volume,
                    "amount": amount / 10000,
                    "date": fields[30],
                    "time": fields[31],
                    "update_time": f"{fields[30]} {fields[31]}"
                }
        
        return None
    
    except Exception as e:
        print(f"[新浪财经 API 错误]: {e}")
        return None


# ============== 多数据源智能选择 ==============
def get_stock_realtime(stock_code: str, prefer_source: str = None) -> dict:
    """
    获取 A 股实时行情 - 多数据源智能选择
    
    策略：
    1. 优先尝试腾讯财经（数据最完整：含最高/最低/成交额）
    2. 其次东方财富（实时性好，但缺少高低点）
    3. 最后新浪财经（备份）
    
    Args:
        stock_code: 股票代码
        prefer_source: 优先数据源 (可选)
    
    Returns:
        dict: 包含股票信息的字典
    """
    # 确定数据源顺序：腾讯优先（数据完整）
    sources = ["tencent", "eastmoney", "sina"]
    if prefer_source and prefer_source in sources:
        sources.remove(prefer_source)
        sources.insert(0, prefer_source)
    
    # 依次尝试各数据源
    for source in sources:
        try:
            if source == "eastmoney":
                result = get_stock_eastmoney(stock_code)
            elif source == "tencent":
                result = get_stock_tencent(stock_code)
            elif source == "sina":
                result = get_stock_sina(stock_code)
            else:
                continue
            
            if result and result.get("success"):
                return result
        
        except Exception as e:
            print(f"[{source} 失败]: {e}")
            continue
    
    # 所有数据源都失败
    return {
        "error": f"所有数据源均失败（尝试：{', '.join(sources)}），请检查网络或股票代码"
    }


# ============== 格式化输出 ==============
def format_stock_info(data: dict) -> str:
    """格式化股票信息输出"""
    if "error" in data:
        return f"❌ {data['error']}"
    
    # 数据源标识
    source_map = {
        "eastmoney": "东方财富",
        "tencent": "腾讯财经",
        "sina": "新浪财经"
    }
    source_name = source_map.get(data.get("source", ""), "未知")
    
    # 涨跌幅颜色
    if data["change_pct"] > 0:
        change_str = f"+{data['change']:.2f} (+{data['change_pct']:.2f}%)"
    elif data["change_pct"] < 0:
        change_str = f"{data['change']:.2f} ({data['change_pct']:.2f}%)"
    else:
        change_str = "0.00 (0.00%)"
    
    output = f"""
📈 {data['name']} ({data['code']}) | {data['market']}
━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 最新价：¥{data['current_price']:.2f}
📊 涨跌：{change_str}
📉 昨收：¥{data['pre_close']:.2f}
📈 今开：¥{data['open']:.2f}
📊 最高：¥{data['high']:.2f}
📉 最低：¥{data['low']:.2f}
📦 成交量：{data['volume']:,} 手
💵 成交额：{data['amount']:.2f} 万

📡 数据源：{source_name}
🕐 更新时间：{data['update_time']}
━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    return output


def check_risk_alert(stock_data: dict) -> Optional[str]:
    """检查是否需要风险提示"""
    change_pct = stock_data.get("change_pct", 0)
    
    alerts = []
    
    if change_pct >= RISK_THRESHOLDS["surge"]:
        alerts.append(f"⚠️【暴涨预警】涨幅已达 {change_pct:.2f}%，注意回调风险")
    elif change_pct <= RISK_THRESHOLDS["plunge"]:
        alerts.append(f"⚠️【暴跌预警】跌幅已达 {change_pct:.2f}%，注意风险")
    elif abs(change_pct) >= RISK_THRESHOLDS["high_volatility"]:
        alerts.append(f"⚠️【高波动】涨跌幅 {change_pct:.2f}%，注意波动风险")
    
    return "\n".join(alerts) if alerts else None


def get_trading_suggestion(stock_data: dict) -> str:
    """获取操盘建议"""
    advice = get_trading_advice(stock_data)
    return f"💡 操盘建议：{advice}\n\n⚠️ 风险提示：以上建议仅供参考，不构成投资建议。股市有风险，投资需谨慎。"


def get_technical_analysis(stock_code: str) -> str:
    """
    获取股票技术分析（完整版）
    
    Args:
        stock_code: 股票代码
    
    Returns:
        格式化的技术分析报告
    """
    # 获取实时数据
    realtime = get_stock_realtime(stock_code)
    if not realtime.get("success"):
        return f"❌ 获取实时数据失败：{realtime.get('error', '未知错误')}"
    
    # 获取历史数据（用于计算技术指标）
    history = get_stock_history(stock_code, days=60)
    if not history.get("success"):
        # 如果历史数据失败，返回基础信息
        return f"{format_stock_info(realtime)}\n\n⚠️ 历史数据获取失败，无法计算完整技术指标。\n请检查网络或稍后重试。"
    
    # 执行技术分析
    analysis = analyze_technical(
        history['high'],
        history['low'],
        history['close'],
        history['volume']
    )
    
    # 生成报告
    report = format_analysis_report(
        stock_code,
        realtime['name'],
        realtime['current_price'],
        analysis
    )
    
    return report


# ============== 盯盘任务 ==============
def start_watch(stock_code: str, target_price: float, direction: str, 
                interval: int = 5, callback=None) -> str:
    """
    启动盯盘任务
    
    Args:
        stock_code: 股票代码
        target_price: 目标价格
        direction: 'up' (涨至) 或 'down' (跌至)
        interval: 刷新间隔（秒）
        callback: 触发时的回调函数
    
    Returns:
        str: 任务状态信息
    """
    with task_lock:
        if stock_code in watch_tasks:
            return f"⚠️ {stock_code} 已有盯盘任务运行中"
        
        task_info = {
            "running": True,
            "stock_code": stock_code,
            "target_price": target_price,
            "direction": direction,
            "interval": interval,
            "thread": None
        }
        
        def watch_loop():
            print(f"🔍 开始盯盘 {stock_code}，{direction} ¥{target_price:.2f}，每{interval}秒刷新")
            
            while task_info["running"]:
                try:
                    result = get_stock_realtime(stock_code)
                    
                    if result.get("success"):
                        current_price = result["current_price"]
                        
                        # 检查是否触发
                        triggered = False
                        if direction == "up" and current_price >= target_price:
                            triggered = True
                            msg = f"🚨【预警触发】{result['name']} ({stock_code})\n"
                            msg += f"当前价：¥{current_price:.2f} | 目标价：¥{target_price:.2f}\n"
                            msg += f"⏰ 触发时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                            print(msg)
                            if callback:
                                callback(msg)
                        
                        elif direction == "down" and current_price <= target_price:
                            triggered = True
                            msg = f"🚨【预警触发】{result['name']} ({stock_code})\n"
                            msg += f"当前价：¥{current_price:.2f} | 目标价：¥{target_price:.2f}\n"
                            msg += f"⏰ 触发时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                            print(msg)
                            if callback:
                                callback(msg)
                        
                        if triggered:
                            break
                    
                    time.sleep(interval)
                    
                except Exception as e:
                    print(f"盯盘出错：{e}")
                    time.sleep(interval)
            
            # 清理任务
            with task_lock:
                if stock_code in watch_tasks:
                    del watch_tasks[stock_code]
        
        # 启动线程
        task_info["thread"] = threading.Thread(target=watch_loop, daemon=True)
        task_info["thread"].start()
        
        watch_tasks[stock_code] = task_info
        
        return f"✅ 已启动 {stock_code} 盯盘任务：{direction} ¥{target_price:.2f}（每{interval}秒刷新）"


def stop_watch(stock_code: str) -> str:
    """停止盯盘任务"""
    with task_lock:
        if stock_code in watch_tasks:
            watch_tasks[stock_code]["running"] = False
            return f"🛑 已停止 {stock_code} 的盯盘任务"
        else:
            return f"❌ 未找到 {stock_code} 的盯盘任务"


def list_watch_tasks() -> str:
    """列出所有盯盘任务"""
    with task_lock:
        if not watch_tasks:
            return "📋 当前没有运行中的盯盘任务"
        
        output = "📋 运行中的盯盘任务:\n"
        output += "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        for code, task in watch_tasks.items():
            direction_str = "涨至" if task["direction"] == "up" else "跌至"
            output += f"  {code} | {direction_str} ¥{task['target_price']:.2f} | "
            output += f"刷新：{task['interval']}秒 | ✅ 运行中\n"
        
        output += "━━━━━━━━━━━━━━━━━━━━━━━━━━"
        return output


# ============== OpenClaw 技能入口 ==============
def handler(event: dict, context) -> str:
    """
    OpenClaw 技能处理函数
    
    支持的指令格式：
    1. 查询 600036 行情
    2. 盯盘 600036 涨至 35 元
    3. 盯盘 000858 跌至 180 元
    4. 停止盯盘 600036
    5. 查看盯盘任务
    6. 600036 风险提示
    7. 600036 操盘建议
    8. 600036 技术分析
    9. 600036 指标
    """
    try:
        command = event.get('input', '').strip()
        
        # 查询行情
        if '查询' in command and '行情' in command:
            stock_code = command.replace('查询', '').replace('行情', '').strip()
            result = get_stock_realtime(stock_code)
            return format_stock_info(result)
        
        # 启动盯盘
        elif '盯盘' in command and ('涨至' in command or '跌至' in command):
            parts = command.replace('盯盘', '').strip().split()
            stock_code = parts[0]
            direction = 'up' if '涨至' in command else 'down'
            price_str = command.split('至')[1].replace('元', '').strip()
            target_price = float(price_str)
            return start_watch(stock_code, target_price, direction)
        
        # 停止盯盘
        elif '停止盯盘' in command:
            stock_code = command.replace('停止盯盘', '').strip()
            return stop_watch(stock_code)
        
        # 查看任务
        elif '查看盯盘' in command or '盯盘任务' in command:
            return list_watch_tasks()
        
        # 风险提示
        elif '风险提示' in command:
            stock_code = command.replace('风险提示', '').strip()
            result = get_stock_realtime(stock_code)
            if result.get("success"):
                risk_alert = check_risk_alert(result)
                if risk_alert:
                    return f"{format_stock_info(result)}\n{risk_alert}"
                else:
                    return f"{format_stock_info(result)}\n✅ 暂无特殊风险提醒"
            else:
                return format_stock_info(result)
        
        # 操盘建议
        elif '操盘建议' in command:
            stock_code = command.replace('操盘建议', '').strip()
            result = get_stock_realtime(stock_code)
            if result.get("success"):
                suggestion = get_trading_suggestion(result)
                return f"{format_stock_info(result)}\n{suggestion}"
            else:
                return format_stock_info(result)
        
        # 技术分析（新增）
        elif '技术分析' in command or '指标' in command:
            stock_code = command.replace('技术分析', '').replace('指标', '').strip()
            return get_technical_analysis(stock_code)
        
        # 自动化报告（新增）
        elif '收盘报告' in command or '日报' in command:
            return generate_comprehensive_daily_report()
        
        elif '持仓报告' in command:
            return generate_holdings_report()
        
        elif '添加到自选' in command or '加入自选' in command:
            # 格式：添加到自选 600036 或 加入自选 600036 招商银行
            parts = command.replace('添加到自选', '').replace('加入自选', '').strip().split()
            if len(parts) >= 1:
                code = parts[0]
                name = parts[1] if len(parts) > 1 else None
                return add_to_watchlist(code, name)
            return "❌ 格式错误，例：添加到自选 600036 招商银行"
        
        elif '设置持仓' in command or '添加持仓' in command:
            # 格式：设置持仓 002892 成本 10.5 数量 1000 科力尔
            import re
            match = re.search(r'(\d{6}).*?成本 ([\d.]+).*?数量 (\d+)', command)
            if match:
                code = match.group(1)
                cost = float(match.group(2))
                shares = int(match.group(3))
                # 尝试提取股票名
                name_match = re.search(r'数量 \d+ (.+)', command)
                name = name_match.group(1).strip() if name_match else None
                return add_holding(code, cost, shares, name)
            return "❌ 格式错误，例：设置持仓 002892 成本 10.5 数量 1000 科力尔"
        
        elif '设置预警' in command or '价格预警' in command:
            # 格式：设置预警 600036 涨至 40 元 或 设置预警 600036 跌至 35 元
            import re
            match = re.search(r'(\d{6}).*?(涨至 | 跌至) ([\d.]+) 元', command)
            if match:
                code = match.group(1)
                direction = "up" if "涨至" in command else "down"
                price = float(match.group(3))
                return set_price_alert(code, direction, price)
            return "❌ 格式错误，例：设置预警 600036 涨至 40 元"
        
        # 智能投顾（新增）
        elif '风险评估' in command or '风险测评' in command:
            # 检查是否包含答案（逗号分隔）
            if ',' in command:
                # 处理风险评估答案
                try:
                    parts = command.replace('风险评估', '').replace('风险测评', '').strip().split(',')
                    answers = [int(p.strip()) for p in parts]
                    if len(answers) != len(RISK_QUESTIONS):
                        return f"❌ 需要{len(RISK_QUESTIONS)}个答案，当前{len(answers)}个"
                    assessment = assess_risk_profile(answers)
                    return format_risk_assessment(assessment)
                except Exception as e:
                    return f"❌ 格式错误：{e}"
            else:
                # 显示风险评估问卷
                report = "📊 投资风险画像评估问卷\n\n请回答以下问题（1-5 分）:\n\n"
                for i, q in enumerate(RISK_QUESTIONS, 1):
                    report += f"{i}. {q['question']}\n"
                    for j, opt in enumerate(q['options'], 1):
                        report += f"   {j}. {opt['text']}\n"
                    report += "\n"
                report += "💡 回复格式：风险评估 3,3,3,3,3（每题得分）"
                return report
        
        elif '止损止盈' in command or '止盈止损' in command:
            # 格式：止损止盈 入场价 10.5 当前价 11.2 仓位 10000
            import re
            match = re.search(r'入场价 ([\d.]+).*?当前价 ([\d.]+).*?仓位 ([\d.]+)', command)
            if match:
                entry = float(match.group(1))
                current = float(match.group(2))
                position = float(match.group(3))
                calc = calculate_stop_loss_stop_profit(entry, current, position_size=position)
                return format_stop_loss_report(calc)
            return "❌ 格式错误，例：止损止盈 入场价 10.5 当前价 11.2 仓位 10000"
        
        elif '估值分析' in command or '股票估值' in command:
            # 格式：估值分析 600036 PE 15 行业 PE 20 增长 15
            import re
            match = re.search(r'(\d{6}).*?PE ([\d.]+).*?行业 PE ([\d.]+).*?增长 ([\d.]+)', command)
            if match:
                code = match.group(1)
                stock_pe = float(match.group(2))
                industry_pe = float(match.group(3))
                growth = float(match.group(4))
                market_pe = 18.0  # 默认市场 PE
                valuation = pe_relative_valuation(stock_pe, industry_pe, market_pe, growth)
                # 获取股票名称
                result = get_stock_realtime(code)
                name = result.get('name', '') if result.get('success') else ''
                return format_valuation_report(valuation, f"{name} ({code})")
            return "❌ 格式错误，例：估值分析 600036 PE 15 行业 PE 20 增长 15"
        
        elif '投资组合' in command or '资产配置' in command:
            # 显示投资组合优化示例
            assets = [
                {"name": "大盘股", "expected_return": 0.10, "volatility": 0.20},
                {"name": "成长股", "expected_return": 0.15, "volatility": 0.30},
                {"name": "债券", "expected_return": 0.05, "volatility": 0.05},
                {"name": "黄金", "expected_return": 0.06, "volatility": 0.15}
            ]
            optimization = calculate_portfolio_optimization(assets)
            return format_portfolio_optimization(optimization)
        
        # 默认帮助
        else:
            return """
📌 A 股盯盘技能 - 支持指令：

📈 行情查询:
  • 查询 [股票代码] 行情
  • 例：查询 600036 行情

🔔 价格预警:
  • 盯盘 [股票代码] 涨至 [价格] 元
  • 盯盘 [股票代码] 跌至 [价格] 元
  • 例：盯盘 600036 涨至 35 元

📋 任务管理:
  • 查看盯盘任务
  • 停止盯盘 [股票代码]

⚠️ 风险提示:
  • [股票代码] 风险提示

💡 操盘建议:
  • [股票代码] 操盘建议

📊 技术分析:
  • [股票代码] 技术分析
  • [股票代码] 指标
  • 支持：MA/RSI/MACD/KDJ/BOLL 等 20+ 指标

📰 自动报告:
  • 收盘报告 / 日报 - 生成综合日报
  • 持仓报告 - 查看持仓盈亏

⚙️ 配置管理:
  • 添加到自选 [代码] [名称] - 加入自选股
  • 设置持仓 [代码] 成本 [价] 数量 [股] [名称]
  • 设置预警 [代码] 涨至/跌至 [价] 元

🤖 智能投顾 (新增):
  • 风险评估 - 投资风险画像测评
  • 风险评估 3,3,3,3,3 - 提交答案
  • 止损止盈 入场价 X 当前价 X 仓位 X
  • 估值分析 [代码] PE X 行业 PE X 增长 X
  • 投资组合 - 资产配置建议

━━━━━━━━━━━━━━━━━━━━━━━━━━
数据源：腾讯财经 (主) | 新浪财经 (备) | 东方财富 (降)
✅ 完全免费，无需 API Key | 延迟 5-15 秒
⚠️ 风险提示：以上信息仅供参考，不构成投资建议
"""
    
    except Exception as e:
        return f"❌ 指令执行失败：{str(e)}"


# ============== 本地测试 ==============
if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("=" * 60)
    print("A 股盯盘技能 - 多数据源增强版测试")
    print("=" * 60)
    
    # 测试各数据源
    test_codes = ["600036", "000858", "300059"]
    
    for code in test_codes:
        print(f"\n[测试] {code}")
        print("-" * 40)
        
        # 测试东方财富
        result_em = get_stock_eastmoney(code)
        if result_em:
            print(f"✅ 东方财富：¥{result_em['current_price']:.2f} ({result_em['change_pct']:+.2f}%)")
        else:
            print("❌ 东方财富：失败")
        
        # 测试腾讯财经
        result_tc = get_stock_tencent(code)
        if result_tc:
            print(f"✅ 腾讯财经：¥{result_tc['current_price']:.2f} ({result_tc['change_pct']:+.2f}%)")
        else:
            print("❌ 腾讯财经：失败")
        
        # 测试新浪财经
        result_sina = get_stock_sina(code)
        if result_sina:
            print(f"✅ 新浪财经：¥{result_sina['current_price']:.2f} ({result_sina['change_pct']:+.2f}%)")
        else:
            print("❌ 新浪财经：失败")
        
        # 测试智能选择
        result = get_stock_realtime(code)
        print(f"\n📊 智能选择结果:")
        print(format_stock_info(result))
    
    print("=" * 60)
    print("测试完成")
    print("=" * 60)
