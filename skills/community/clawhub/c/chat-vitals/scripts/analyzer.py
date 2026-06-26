#!/usr/bin/env python3
"""
Chat Vitals - Analyzer
分析会话数据，计算各项指标
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta

SKILL_DIR = Path.home() / ".openclaw" / "skills" / "chat-vitals"
DATA_DIR = SKILL_DIR / "data" / "sessions"
CONFIG_PATH = SKILL_DIR / "config.json"

def load_config():
    """加载配置"""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_session(session_id):
    """加载会话数据"""
    session_file = DATA_DIR / f"{session_id}.json"
    if session_file.exists():
        with open(session_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def load_all_sessions(days=7):
    """加载最近N天的所有会话"""
    sessions = []
    cutoff = datetime.now() - timedelta(days=days)
    
    for sf in DATA_DIR.glob("*.json"):
        with open(sf, 'r', encoding='utf-8') as f:
            data = json.load(f)
            start_time = datetime.fromisoformat(data.get("start_time", "2000-01-01"))
            if start_time >= cutoff:
                sessions.append(data)
    
    return sorted(sessions, key=lambda x: x.get("start_time", ""))

def analyze_session(session_data):
    """分析单个会话"""
    turns = session_data.get("turns", [])
    total_turns = len(turns)
    
    if total_turns == 0:
        return None
    
    # 基础统计
    total_tokens = session_data.get("total_tokens_in", 0) + session_data.get("total_tokens_out", 0)
    rework_count = session_data.get("rework_count", 0)
    
    # 首通率：如果没有返工，则首通
    first_try_success = rework_count == 0
    
    # 承诺相关
    promises_made = session_data.get("promises_made", [])
    promise_count = len(promises_made)
    
    # 检测承诺兑现（简化逻辑：如果有返工，可能承诺未兑现）
    # 更精确的检测需要在后续轮次中验证
    promises_fulfilled = promise_count
    if rework_count > 0 and promise_count > 0:
        promises_fulfilled = max(0, promise_count - rework_count)
    
    promise_fulfillment_rate = promises_fulfilled / promise_count if promise_count > 0 else 1.0
    
    # 计划膨胀指数：实际轮次 vs 预期轮次
    # 假设：如果有承诺，预期轮次应该与承诺的步骤数相关
    expected_turns = 1  # 默认为1轮
    if promise_count > 0:
        # 简单估计：每个承诺大概对应一轮
        expected_turns = promise_count
    
    plan_inflation_index = total_turns / expected_turns if expected_turns > 0 else total_turns
    
    # Token效率：假设每个task产出一定的"价值点"
    # 简化计算：总token / 轮次 = 每轮平均token
    token_efficiency = 1.0 / (total_tokens / total_turns) if total_tokens > 0 else 0
    
    # 健康评分计算
    health_score = calculate_health_score(
        first_try_success,
        rework_count,
        promise_fulfillment_rate,
        plan_inflation_index,
        token_efficiency
    )
    
    return {
        "session_id": session_data.get("session_id"),
        "model": session_data.get("model"),
        "total_turns": total_turns,
        "total_tokens": total_tokens,
        "rework_count": rework_count,
        "first_try_success": first_try_success,
        "first_try_success_rate": 100.0 if first_try_success else 0.0,
        "promise_count": promise_count,
        "promises_fulfilled": promises_fulfilled,
        "promise_fulfillment_rate": promise_fulfillment_rate * 100,
        "plan_inflation_index": plan_inflation_index,
        "token_efficiency": token_efficiency,
        "health_score": health_score,
        "status": get_health_status(health_score)
    }

def calculate_health_score(first_try, rework, promise_rate, inflation, token_eff):
    """计算综合健康评分 (0-100)"""
    score = 100
    
    # 首通扣分
    if not first_try:
        score -= 30
    
    # 返工扣分
    score -= min(rework * 10, 30)
    
    # 承诺兑现率加分/扣分
    if promise_rate < 0.6:
        score -= 20
    elif promise_rate > 0.8:
        score += 5
    
    # 计划膨胀扣分
    if inflation > 2.0:
        score -= 20
    elif inflation > 1.5:
        score -= 10
    
    return max(0, min(100, score))

def get_health_status(score):
    """根据分数返回健康状态"""
    if score >= 85:
        return "excellent"
    elif score >= 70:
        return "good"
    elif score >= 50:
        return "warning"
    else:
        return "danger"

def analyze_trend(sessions, days=7):
    """分析趋势"""
    if not sessions:
        return None
    
    # 按天聚合
    daily_stats = {}
    
    for session in sessions:
        start_time = datetime.fromisoformat(session.get("start_time", "2000-01-01"))
        day_key = start_time.strftime("%Y-%m-%d")
        
        if day_key not in daily_stats:
            daily_stats[day_key] = {
                "count": 0,
                "total_tokens": 0,
                "rework_count": 0,
                "first_try_count": 0,
                "health_scores": []
            }
        
        analysis = analyze_session(session)
        if analysis:
            daily_stats[day_key]["count"] += 1
            daily_stats[day_key]["total_tokens"] += analysis["total_tokens"]
            daily_stats[day_key]["rework_count"] += analysis["rework_count"]
            if analysis["first_try_success"]:
                daily_stats[day_key]["first_try_count"] += 1
            daily_stats[day_key]["health_scores"].append(analysis["health_score"])
    
    # 计算趋势
    trend = []
    for day, stats in sorted(daily_stats.items()):
        avg_health = sum(stats["health_scores"]) / len(stats["health_scores"]) if stats["health_scores"] else 0
        first_try_rate = stats["first_try_count"] / stats["count"] * 100 if stats["count"] > 0 else 0
        
        trend.append({
            "date": day,
            "session_count": stats["count"],
            "total_tokens": stats["total_tokens"],
            "avg_health_score": avg_health,
            "first_try_rate": first_try_rate,
            "total_rework": stats["rework_count"]
        })
    
    return trend

def main():
    """命令行入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: analyzer.py <command> [args...]")
        print("Commands:")
        print("  session <session_id>  - 分析单个会话")
        print("  trend [days]          - 分析趋势（默认7天）")
        print("  summary               - 汇总统计")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "session":
        if len(sys.argv) < 3:
            print("Usage: session <session_id>")
            return
        sid = sys.argv[2]
        session = load_session(sid)
        if session:
            result = analyze_session(session)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"Session {sid} not found")
    
    elif cmd == "trend":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        sessions = load_all_sessions(days)
        trend = analyze_trend(sessions, days)
        print(json.dumps(trend, ensure_ascii=False, indent=2))
    
    elif cmd == "summary":
        sessions = load_all_sessions(30)
        if not sessions:
            print("No sessions found in the last 30 days")
            return
        
        total_sessions = len(sessions)
        total_tokens = sum(s.get("total_tokens_in", 0) + s.get("total_tokens_out", 0) for s in sessions)
        total_rework = sum(s.get("rework_count", 0) for s in sessions)
        
        first_try_count = 0
        for s in sessions:
            analysis = analyze_session(s)
            if analysis and analysis["first_try_success"]:
                first_try_count += 1
        
        summary = {
            "total_sessions": total_sessions,
            "total_tokens": total_tokens,
            "total_rework": total_rework,
            "first_try_rate": first_try_count / total_sessions * 100 if total_sessions > 0 else 0,
            "avg_rework_per_session": total_rework / total_sessions if total_sessions > 0 else 0
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
