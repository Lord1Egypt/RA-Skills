# -*- coding: utf-8 -*-
"""
曙光 Proactive Agent v1.0

主动型Agent核心引擎：
- 时间线感知 (通过Cron触发)
- 决策回溯追踪
- 市场/系统状态主动推送
- Proactive Surprise 自发现

用法: 被 cron 消息唤醒时，先读此模块判断该干什么。
"""

import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", ""))
if not WORKSPACE.exists():
    WORKSPACE = Path.home() / ".openclaw" / "workspace"

STATE_FILE = WORKSPACE / "session-state.json"
DECISION_FILE = WORKSPACE / "memory" / "decision-registry.json"
PROACTIVE_LOG = WORKSPACE / "memory" / "proactive-log.md"


def load_state():
    """加载 session-state.json"""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except:
            return {}
    return {}


def save_state(state):
    """保存 session-state.json"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def load_decisions():
    """加载决策注册表"""
    if DECISION_FILE.exists():
        try:
            return json.loads(DECISION_FILE.read_text(encoding="utf-8"))
        except:
            return {"decisions": [], "last_check": None}
    return {"decisions": [], "last_check": None}


def save_decisions(registry):
    """保存决策注册表"""
    DECISION_FILE.parent.mkdir(parents=True, exist_ok=True)
    DECISION_FILE.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")


def log_proactive(action, detail, result=None):
    """记录主动行为日志"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"- [{now}] **{action}**: {detail}"
    if result:
        entry += f" → {result}"
    entry += "\n"
    
    PROACTIVE_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(PROACTIVE_LOG, "a", encoding="utf-8") as f:
        f.write(entry)


def classify_cron_message(message):
    """
    识别 cron 触发消息的类型
    
    返回: {
        "type": "morning_check" | "midday_check" | "afternoon_check" | 
                "evening_analysis" | "decision_backtrack" | "health_check" |
                "memory_sync" | "surprise_scan" | "unknown"
    }
    """
    msg = message.lower()
    
    if "早盘" in msg or "morning" in msg:
        return "morning_check"
    elif "午盘" in msg or "mid" in msg:
        return "midday_check"
    elif "收盘" in msg or "收盘扫描" in msg or "afternoon" in msg:
        return "afternoon_check"
    elif "盘后" in msg or "晚间" in msg or "evening" in msg:
        return "evening_analysis"
    elif "决策" in msg or "随访" in msg or "backtrack" in msg or "follow.up" in msg:
        return "decision_backtrack"
    elif "健康" in msg or "health" in msg or "代码" in msg:
        return "health_check"
    elif "记忆" in msg or "memory" in msg or "sync" in msg:
        return "memory_sync"
    elif "惊喜" in msg or "surprise" in msg or "主动发现" in msg:
        return "surprise_scan"
    else:
        return "unknown"


def register_decision(name, decision, expected_outcome, follow_up_days=7, category="general"):
    """
    注册一条决策用于后续回溯
    
    参数:
        name: 决策名称
        decision: 决策内容描述
        expected_outcome: 预期结果
        follow_up_days: 多少天后回溯
        category: 决策类别 (trading|system|strategy|general)
    """
    registry = load_decisions()
    now = datetime.now().isoformat()
    follow_up = (datetime.now() + timedelta(days=follow_up_days)).isoformat()
    
    entry = {
        "id": f"DEC-{datetime.now().strftime('%Y%m%d')}-{len(registry['decisions'])+1:03d}",
        "name": name,
        "decision": decision,
        "expected_outcome": expected_outcome,
        "category": category,
        "created": now,
        "follow_up_by": follow_up,
        "status": "active",  # active | verified | failed | superseded
        "verified_at": None,
        "actual_outcome": None,
        "learned": None
    }
    
    registry["decisions"].append(entry)
    registry["last_check"] = now
    save_decisions(registry)
    
    log_proactive("决策注册", f"{name}: {decision[:50]}...", f"follow_up: {follow_up_days}d")
    return entry["id"]


def get_overdue_decisions():
    """获取已到期但未验证的决策"""
    registry = load_decisions()
    now = datetime.now()
    overdue = []
    
    for d in registry["decisions"]:
        if d["status"] != "active":
            continue
        follow_up = datetime.fromisoformat(d["follow_up_by"])
        if follow_up <= now:
            overdue.append(d)
    
    return overdue


def verify_decision(decision_id, actual_outcome, learned=None):
    """验证一条决策的结果"""
    registry = load_decisions()
    now = datetime.now().isoformat()
    
    for d in registry["decisions"]:
        if d["id"] == decision_id:
            d["status"] = "verified"
            d["verified_at"] = now
            d["actual_outcome"] = actual_outcome
            d["learned"] = learned
            save_decisions(registry)
            log_proactive("决策验证", f"{d['name']}: {actual_outcome[:50]}")
            return True
    return False


def get_market_hours_status():
    """判断当前是否在A股交易时段"""
    now = datetime.now()
    weekday = now.weekday()
    hour = now.hour
    minute = now.minute
    
    # 周末
    if weekday >= 5:
        return "weekend"
    
    # 交易时段
    time_total = hour * 100 + minute
    if 915 <= time_total < 1130:
        return "trading_morning"
    elif 1300 <= time_total < 1500:
        return "trading_afternoon"
    elif 1130 <= time_total < 1300:
        return "lunch_break"
    elif 1500 <= time_total < 1600:
        return "post_market"
    elif 900 <= time_total < 915:
        return "pre_open"
    else:
        return "closed"


# ─── Cron Handler 模板 ───

def handle_morning_check():
    """早盘检查 (09:25 触发)"""
    return {
        "action": "早盘检查",
        "tasks": [
            "检查大盘指数状态 (上证/科创/创业板)",
            "检查持仓ETF盘前价格",
            "检查隔夜重大新闻",
            "如有异动 → 主动推送预警"
        ],
        "push_if": "持仓跌幅>2% 或 大盘异动"
    }


def handle_midday_check():
    """午盘复盘 (11:30 触发)"""
    return {
        "action": "午盘复盘",
        "tasks": [
            "检查上午持仓表现",
            "对比早盘策略预期",
            "判断下午是否需要调整"
        ],
        "push_if": "半日浮亏>3% 或 策略信号变化"
    }


def handle_afternoon_check():
    """收盘扫描 (15:00 触发)"""
    return {
        "action": "收盘扫描",
        "tasks": [
            "检查收盘持仓表现",
            "记录当日盈亏",
            "评估是否触发止损/止盈条件"
        ],
        "push_if": "触发止损线 或 单日浮亏>5%"
    }


def handle_evening_analysis():
    """盘后分析 (20:00 触发)"""
    return {
        "action": "盘后分析",
        "tasks": [
            "全量盘后分析",
            "更新MEMORY.md",
            "检查明日策略"
        ],
        "push_if": "重要发现（板块轮动/策略信号）"
    }


def handle_decision_backtrack():
    """决策回溯 (每日检查)"""
    overdue = get_overdue_decisions()
    if overdue:
        text = "📋 **决策随访提醒**\n"
        for d in overdue:
            text += f"- {d['name']} (ID: {d['id']}, {d['category']})\n  决策: {d['decision'][:80]}...\n  预期: {d['expected_outcome'][:80]}...\n"
        return {
            "action": "决策回溯",
            "overdue_count": len(overdue),
            "summary": text
        }
    return {"action": "决策回溯", "overdue_count": 0, "summary": "无逾期决策"}


if __name__ == "__main__":
    # 测试
    print("[OK] Dawn Proactive Agent v1.0 loaded")
    print(f"市场状态: {get_market_hours_status()}")
    print(f"决策数: {len(load_decisions()['decisions'])}")
    print(f"逾期决策: {len(get_overdue_decisions())}")
