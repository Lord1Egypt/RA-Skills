#!/usr/bin/env python3
"""
Chat Vitals - Data Collector
采集每次对话的元数据，轻量级设计，最小化性能开销
"""

import json
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path

# 路径配置
SKILL_DIR = Path.home() / ".openclaw" / "skills" / "chat-vitals"
DATA_DIR = SKILL_DIR / "data" / "sessions"
CONFIG_PATH = SKILL_DIR / "config.json"

def load_config():
    """加载配置"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def ensure_session_dir():
    """确保会话目录存在"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def create_session(model="unknown"):
    """创建新会话记录"""
    ensure_session_dir()
    session_id = str(uuid.uuid4())[:8]
    session_data = {
        "session_id": session_id,
        "model": model,
        "start_time": datetime.now().isoformat(),
        "turns": [],
        "total_tokens_in": 0,
        "total_tokens_out": 0,
        "task_completed": False,
        "rework_count": 0,
        "promises_made": [],
        "promises_fulfilled": [],
        "status": "active"
    }
    
    session_file = DATA_DIR / f"{session_id}.json"
    with open(session_file, 'w', encoding='utf-8') as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)
    
    return session_id

def load_session(session_id):
    """加载会话数据"""
    session_file = DATA_DIR / f"{session_id}.json"
    if session_file.exists():
        with open(session_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_session(session_data):
    """保存会话数据"""
    session_file = DATA_DIR / f"{session_data['session_id']}.json"
    with open(session_file, 'w', encoding='utf-8') as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)

def detect_correction(user_input, config):
    """检测用户是否在进行修正"""
    keywords = config.get("patterns", {}).get("correction_keywords", [])
    user_lower = user_input.lower()
    
    for kw in keywords:
        if kw.lower() in user_lower:
            return True, kw
    return False, None

def detect_promises(model_output, config):
    """检测模型是否做出承诺"""
    patterns = config.get("patterns", {}).get("promise_patterns", [])
    over_promise = config.get("patterns", {}).get("over_promise_patterns", [])
    
    promises = []
    is_over_promise = False
    
    output_lower = model_output.lower()
    
    for pattern in patterns:
        if pattern.lower() in output_lower:
            promises.append(pattern)
    
    for op in over_promise:
        if op.lower() in output_lower:
            is_over_promise = True
            promises.append(f"[OVER_PROMISE] {op}")
    
    return len(promises) > 0, promises, is_over_promise

def record_turn(session_id, user_input, model_output, tokens_in=0, tokens_out=0):
    """记录一轮对话"""
    config = load_config()
    session = load_session(session_id)
    
    if not session:
        print(f"[ERROR] Session {session_id} not found")
        return False
    
    # 检测修正
    is_correction, correction_kw = detect_correction(user_input, config)
    if is_correction:
        session["rework_count"] += 1
    
    # 检测承诺
    has_promise, promises, is_over_promise = detect_promises(model_output, config)
    if has_promise:
        session["promises_made"].extend(promises)
    
    # 构建 turn 记录
    turn = {
        "turn_id": len(session["turns"]) + 1,
        "timestamp": datetime.now().isoformat(),
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "is_correction": is_correction,
        "correction_keyword": correction_kw if is_correction else None,
        "has_promise": has_promise,
        "promises": promises if has_promise else [],
        "is_over_promise": is_over_promise
    }
    
    session["turns"].append(turn)
    session["total_tokens_in"] += tokens_in
    session["total_tokens_out"] += tokens_out
    
    save_session(session)
    return True

def complete_session(session_id, success=True):
    """标记会话完成"""
    session = load_session(session_id)
    if session:
        session["task_completed"] = success
        session["status"] = "completed"
        session["end_time"] = datetime.now().isoformat()
        save_session(session)
        return True
    return False

def get_active_session():
    """获取当前活跃的会话"""
    ensure_session_dir()
    
    # 查找最新的活跃会话
    session_files = sorted(DATA_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    for sf in session_files:
        with open(sf, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if data.get("status") == "active":
                return data["session_id"]
    
    return None

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("Usage: collector.py <command> [args...]")
        print("Commands:")
        print("  create [model]     - 创建新会话")
        print("  record <session> <user_input> <model_output> [tokens_in] [tokens_out]")
        print("  complete <session> [success]")
        print("  active             - 获取当前活跃会话")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "create":
        model = sys.argv[2] if len(sys.argv) > 2 else "unknown"
        sid = create_session(model)
        print(f"Created session: {sid}")
    
    elif cmd == "record":
        if len(sys.argv) < 5:
            print("Usage: record <session_id> <user_input> <model_output> [tokens_in] [tokens_out]")
            return
        sid = sys.argv[2]
        user_input = sys.argv[3]
        model_output = sys.argv[4]
        tokens_in = int(sys.argv[5]) if len(sys.argv) > 5 else 0
        tokens_out = int(sys.argv[6]) if len(sys.argv) > 6 else 0
        
        if record_turn(sid, user_input, model_output, tokens_in, tokens_out):
            print(f"Recorded turn for session {sid}")
        else:
            print(f"Failed to record turn")
    
    elif cmd == "complete":
        if len(sys.argv) < 3:
            print("Usage: complete <session_id> [success]")
            return
        sid = sys.argv[2]
        success = sys.argv[3].lower() == "true" if len(sys.argv) > 3 else True
        
        if complete_session(sid, success):
            print(f"Completed session {sid}")
        else:
            print(f"Session {sid} not found")
    
    elif cmd == "active":
        sid = get_active_session()
        if sid:
            print(f"Active session: {sid}")
        else:
            print("No active session")

if __name__ == "__main__":
    main()
