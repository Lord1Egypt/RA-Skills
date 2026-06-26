#!/usr/bin/env python3
"""
Chat Vitals - Auto Collector (OpenClaw Hook)
自动采集 OpenClaw 对话数据，无需手动干预
"""

import json
import os
import sys
import re
from pathlib import Path
from datetime import datetime

# 添加脚本路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

import collector

# 全局状态
_active_session = None
_last_user_input = None
_last_model_output = None

def extract_tokens_from_log(log_line):
    """从 OpenClaw 日志中提取 token 信息"""
    # 匹配常见的 token 统计格式
    patterns = [
        r'(\d+)\s*tokens?\s*(?:in|input)',
        r'input[:\s]*(\d+)',
        r'output[:\s]*(\d+)',
        r'tokens[:\s]*(\d+)',
    ]
    
    tokens_in = 0
    tokens_out = 0
    
    for pattern in patterns:
        matches = re.findall(pattern, log_line, re.IGNORECASE)
        if matches:
            # 简单启发式：第一个数字通常是 input
            if not tokens_in:
                tokens_in = int(matches[0])
            elif not tokens_out:
                tokens_out = int(matches[0])
    
    return tokens_in, tokens_out

def estimate_tokens(text):
    """估算 token 数（粗略：1 token ≈ 4 字符）"""
    return len(text) // 4

def auto_start_session(model_hint="unknown"):
    """自动开始新会话"""
    global _active_session
    
    # 检查是否已有活跃会话
    active = collector.get_active_session()
    if active:
        _active_session = active
        return _active_session
    
    # 创建新会话
    _active_session = collector.create_session(model_hint)
    return _active_session

def auto_record_turn(user_input, model_output, tokens_in=None, tokens_out=None):
    """自动记录一轮对话"""
    global _active_session, _last_user_input, _last_model_output
    
    # 确保有活跃会话
    if not _active_session:
        _active_session = auto_start_session()
    
    # 估算 token（如果没有提供）
    if tokens_in is None:
        tokens_in = estimate_tokens(user_input)
    if tokens_out is None:
        tokens_out = estimate_tokens(model_output)
    
    # 记录
    success = collector.record_turn(
        _active_session,
        user_input,
        model_output,
        tokens_in,
        tokens_out
    )
    
    if success:
        _last_user_input = user_input
        _last_model_output = model_output
    
    return success

def auto_complete_session(success=True):
    """自动完成当前会话"""
    global _active_session
    
    if _active_session:
        collector.complete_session(_active_session, success)
        session_id = _active_session
        _active_session = None
        return session_id
    
    return None

def get_session_summary():
    """获取当前会话摘要（用于实时显示）"""
    global _active_session
    
    # 如果没有活跃会话变量，尝试从 collector 获取
    if not _active_session:
        _active_session = collector.get_active_session()
    
    if not _active_session:
        return None
    
    session = collector.load_session(_active_session)
    if not session:
        return None
    
    turns = session.get("turns", [])
    total_tokens = session.get("total_tokens_in", 0) + session.get("total_tokens_out", 0)
    rework_count = session.get("rework_count", 0)
    
    # 计算健康分（简化版）
    score = 100
    if rework_count > 0:
        score -= rework_count * 15
    if len(turns) > 3:
        score -= (len(turns) - 3) * 5
    
    score = max(0, min(100, score))
    
    return {
        "session_id": _active_session,
        "model": session.get("model", "unknown"),
        "turns": len(turns),
        "total_tokens": total_tokens,
        "rework_count": rework_count,
        "health_score": score,
        "status": get_status_emoji(score)
    }

def get_status_emoji(score):
    """根据分数返回状态表情"""
    if score >= 85:
        return "🟢"
    elif score >= 70:
        return "🟡"
    elif score >= 50:
        return "🟠"
    else:
        return "🔴"

# Hook 集成点 - 供 OpenClaw 调用
def on_user_message(message):
    """用户发送消息时调用"""
    global _last_user_input
    _last_user_input = message
    
    # 检查是否是新会话的开始
    if not _active_session:
        auto_start_session()

def on_assistant_message(message, metadata=None):
    """助手回复时调用"""
    global _last_user_input, _active_session
    
    tokens_in = 0
    tokens_out = 0
    
    if metadata:
        tokens_in = metadata.get("tokens_in", 0)
        tokens_out = metadata.get("tokens_out", 0)
    
    if _last_user_input:
        auto_record_turn(_last_user_input, message, tokens_in, tokens_out)
        _last_user_input = None  # 重置

def on_session_end(success=True):
    """会话结束时调用"""
    return auto_complete_session(success)

# 命令行接口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Chat Vitals Auto Collector")
    parser.add_argument("action", choices=["start", "status", "summary", "complete"])
    parser.add_argument("model", nargs="?", default="unknown", help="Model name")
    parser.add_argument("--success", action="store_true", help="Mark as successful")
    
    args = parser.parse_args()
    
    if args.action == "start":
        sid = auto_start_session(args.model)
        print(f"Started auto-monitoring session: {sid}")
    
    elif args.action == "status":
        summary = get_session_summary()
        if summary:
            print(json.dumps(summary, indent=2, ensure_ascii=False))
        else:
            print("No active session")
    
    elif args.action == "summary":
        summary = get_session_summary()
        if summary:
            print(f"Session: {summary['session_id']}")
            print(f"Model: {summary['model']}")
            print(f"Turns: {summary['turns']}")
            print(f"Tokens: {summary['total_tokens']:,}")
            print(f"Rework: {summary['rework_count']}")
            print(f"Health: {summary['status']} {summary['health_score']}/100")
        else:
            print("No active session")
    
    elif args.action == "complete":
        sid = auto_complete_session(args.success)
        if sid:
            print(f"Completed session: {sid}")
        else:
            print("No active session to complete")
