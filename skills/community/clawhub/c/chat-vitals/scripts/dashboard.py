#!/usr/bin/env python3
"""
Chat Vitals - Real-time Dashboard
实时仪表盘，显示当前会话状态和关键指标
"""

import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime

# 添加脚本路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

import collector
import analyzer

# ANSI 颜色代码
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    ORANGE = '\033[38;5;208m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def clear_screen():
    """清屏"""
    os.system('clear' if os.name != 'nt' else 'cls')

def get_health_color(score):
    """根据分数返回颜色"""
    if score >= 85:
        return Colors.GREEN
    elif score >= 70:
        return Colors.YELLOW
    elif score >= 50:
        return Colors.ORANGE
    else:
        return Colors.RED

def get_health_emoji(score):
    """根据分数返回表情"""
    if score >= 85:
        return "🟢"
    elif score >= 70:
        return "🟡"
    elif score >= 50:
        return "🟠"
    else:
        return "🔴"

def draw_progress_bar(value, max_val=100, width=30):
    """绘制进度条"""
    filled = int(value / max_val * width)
    empty = width - filled
    
    color = get_health_color(value)
    bar = "█" * filled + "░" * empty
    
    return f"{color}[{bar}]{Colors.RESET} {value}%"

def get_active_session_data():
    """获取当前活跃会话数据"""
    sid = collector.get_active_session()
    if not sid:
        return None
    
    session = collector.load_session(sid)
    if not session:
        return None
    
    # 使用 analyzer 计算完整指标
    analysis = analyzer.analyze_session(session)
    
    return {
        "session_id": sid,
        "session": session,
        "analysis": analysis
    }

def render_dashboard(data):
    """渲染仪表盘"""
    clear_screen()
    
    if not data:
        print(f"\n{Colors.GRAY}No active monitoring session.{Colors.RESET}")
        print(f"{Colors.GRAY}Start one with: monitor start <model>{Colors.RESET}\n")
        return
    
    session = data.get("session")
    analysis = data.get("analysis")
    
    if not analysis:
        print(f"\n{Colors.GRAY}No analysis data available.{Colors.RESET}\n")
        return
    
    score = analysis.get("health_score", 0)
    color = get_health_color(score)
    emoji = get_health_emoji(score)
    
    # 头部
    print(f"\n{Colors.BOLD}{Colors.CYAN}📊 Chat Vitals Dashboard{Colors.RESET}")
    print(f"{Colors.GRAY}{'─' * 50}{Colors.RESET}\n")
    
    # 会话信息
    print(f"{Colors.BOLD}Session:{Colors.RESET} {session.get('session_id', 'N/A')}")
    print(f"{Colors.BOLD}Model:{Colors.RESET}   {session.get('model', 'unknown')}")
    print(f"{Colors.BOLD}Started:{Colors.RESET} {session.get('start_time', 'N/A')[:19]}")
    print()
    
    # 健康评分（大字显示）
    status_text = get_status_text(score)
    print(f"{Colors.BOLD}Health Score:{Colors.RESET}")
    print(f"{emoji} {color}{Colors.BOLD}{score}/100{Colors.RESET} - {color}{status_text}{Colors.RESET}")
    print(f"{draw_progress_bar(score)}")
    print()
    
    # 核心指标网格
    print(f"{Colors.BOLD}Key Metrics:{Colors.RESET}")
    print(f"{Colors.GRAY}{'─' * 50}{Colors.RESET}")
    
    # 指标1: 首通率
    fts_rate = analysis.get("first_try_success_rate", 0)
    fts_emoji = "✅" if fts_rate >= 70 else "⚠️" if fts_rate >= 50 else "🔴"
    print(f"  {fts_emoji} First-Try Success: {fts_rate:.0f}%")
    
    # 指标2: 返工次数
    rework = analysis.get("rework_count", 0)
    rework_emoji = "✅" if rework == 0 else "⚠️" if rework <= 2 else "🔴"
    print(f"  {rework_emoji} Rework Count: {rework}")
    
    # 指标3: 承诺兑现率
    promise_rate = analysis.get("promise_fulfillment_rate", 0)
    promise_emoji = "✅" if promise_rate >= 80 else "⚠️" if promise_rate >= 60 else "🔴"
    print(f"  {promise_emoji} Promise Fulfillment: {promise_rate:.0f}%")
    
    # 指标4: 计划膨胀
    inflation = analysis.get("plan_inflation_index", 1.0)
    inflation_emoji = "✅" if inflation <= 1.3 else "⚠️" if inflation <= 2.0 else "🔴"
    print(f"  {inflation_emoji} Plan Inflation: {inflation:.1f}x")
    
    # 指标5: Token 效率
    efficiency = analysis.get("token_efficiency", 0)
    efficiency_emoji = "✅" if efficiency >= 0.15 else "⚠️" if efficiency >= 0.08 else "🔴"
    print(f"  {efficiency_emoji} Token Efficiency: {efficiency:.4f}")
    
    # 会话统计
    turns = analysis.get("total_turns", 0)
    tokens = analysis.get("total_tokens", 0)
    print()
    print(f"{Colors.BOLD}Session Stats:{Colors.RESET}")
    print(f"  💬 Total Turns: {turns}")
    print(f"  🔢 Total Tokens: {tokens:,}")
    print(f"  📊 Avg Tokens/Turn: {tokens // turns if turns > 0 else 0:,}")
    
    # 警报区域
    alerts = generate_alerts(analysis)
    if alerts:
        print()
        print(f"{Colors.BOLD}{Colors.RED}⚠️  Alerts:{Colors.RESET}")
        print(f"{Colors.GRAY}{'─' * 50}{Colors.RESET}")
        for alert in alerts:
            print(f"  {alert}")
    
    # 底部提示
    print()
    print(f"{Colors.GRAY}{'─' * 50}{Colors.RESET}")
    print(f"{Colors.GRAY}Press Ctrl+C to exit | Refresh: 2s{Colors.RESET}\n")

def get_status_text(score):
    """获取状态文本"""
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 50:
        return "Warning"
    else:
        return "Critical"

def generate_alerts(analysis):
    """生成警报列表"""
    alerts = []
    
    if analysis.get("rework_count", 0) >= 2:
        alerts.append(f"{Colors.ORANGE}Multiple reworks detected ({analysis['rework_count']}){Colors.RESET}")
    
    if analysis.get("plan_inflation_index", 1.0) > 2.0:
        alerts.append(f"{Colors.RED}Severe plan inflation ({analysis['plan_inflation_index']:.1f}x){Colors.RESET}")
    
    if analysis.get("first_try_success_rate", 100) < 50:
        alerts.append(f"{Colors.RED}Low first-try success rate{Colors.RESET}")
    
    if analysis.get("promise_fulfillment_rate", 100) < 60:
        alerts.append(f"{Colors.ORANGE}Poor promise fulfillment{Colors.RESET}")
    
    return alerts

def watch_mode(refresh_interval=2):
    """持续监控模式"""
    try:
        while True:
            data = get_active_session_data()
            render_dashboard(data)
            time.sleep(refresh_interval)
    except KeyboardInterrupt:
        print(f"\n{Colors.GRAY}Dashboard closed.{Colors.RESET}\n")

def snapshot_mode():
    """单次快照模式"""
    data = get_active_session_data()
    render_dashboard(data)

def main():
    """主入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Chat Vitals Real-time Dashboard")
    parser.add_argument(
        "--mode",
        choices=["watch", "snapshot"],
        default="watch",
        help="Dashboard mode: watch (continuous) or snapshot (single)"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=2,
        help="Refresh interval in seconds (watch mode only)"
    )
    
    args = parser.parse_args()
    
    if args.mode == "watch":
        watch_mode(args.interval)
    else:
        snapshot_mode()

if __name__ == "__main__":
    main()
