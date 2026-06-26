#!/usr/bin/env python3
"""
调度链路日志 — 每次 dispatch → report 写入COLD级记忆

存储: memory/dispatch-log.json
逐条记录：谁在哪个通道发起了什么调度，派给了谁，结果如何

sync_to_engine(): 引擎调用，将新记录注入engine_v2状态（COLD级）
"""

import json, sys, argparse
from pathlib import Path
from datetime import datetime, timezone

LOG_FILE = Path.home() / '.agent-mem/dispatch-log.json'
MAX_ENTRIES = 200


def _load() -> list:
    if LOG_FILE.exists():
        try:
            return json.load(open(LOG_FILE))
        except:
            return []
    return []


def _save(entries: list):
    json.dump(entries, open(LOG_FILE, 'w'), indent=2, ensure_ascii=False)


def log_dispatch(from_channel: str, from_agent: str, to_agent: str,
                 task: str, intent: str, result: str,
                 duration: float = 0, detail: str = ""):
    """
    记录一次调度链路
    
    from_channel: 从哪个通道发起的 (webchat/feishu/...)
    from_agent: 谁发起的调度 (通常是main)
    to_agent: 派给了谁
    task: 任务描述
    intent: 意图分类
    result: success/fail
    duration: 耗时秒数
    detail: 补充信息
    """
    entries = _load()
    
    entry = {
        "from_channel": from_channel,
        "from_agent": from_agent,
        "to_agent": to_agent,
        "task": task[:200],
        "intent": intent,
        "result": result,
        "duration": round(duration, 1),
        "detail": detail[:500],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    
    entries.insert(0, entry)
    entries = entries[:MAX_ENTRIES]
    _save(entries)
    return len(entries)


def query_recent(limit: int = 20, agent: str = "", result_filter: str = ""):
    """查询最近调度记录"""
    entries = _load()
    
    result = []
    for e in entries:
        if agent and e.get("to_agent", "") != agent:
            continue
        if result_filter and e.get("result", "") != result_filter:
            continue
        result.append(e)
        if len(result) >= limit:
            break
    
    return result


def get_stats() -> dict:
    """统计调度数据"""
    entries = _load()
    stats = {"total": len(entries), "agents": {}, "channels": {}, "results": {}}
    
    for e in entries:
        ag = e.get("to_agent", "unknown")
        ch = e.get("from_channel", "unknown")
        rs = e.get("result", "unknown")
        
        stats["agents"][ag] = stats["agents"].get(ag, 0) + 1
        stats["channels"][ch] = stats["channels"].get(ch, 0) + 1
        stats["results"][rs] = stats["results"].get(rs, 0) + 1
    
    return stats


def sync_to_engine():
    """
    将新调度日志注入 engine_v2 状态文件（COLD级）
    引擎调用，每次process_daily时执行
    """
    entries = _load()
    if not entries:
        return 0
    
    engine_state_file = Path.home() / '.agent-mem/memory-engine-state.json'
    if not engine_state_file.exists():
        return 0
    
    try:
        state = json.load(open(engine_state_file))
    except:
        return 0
    
    # 检查最后同步的调度日志ID
    last_synced = state.get("dispatch", {}).get("last_synced_ts", "")
    
    count = 0
    dispatch_facts = state.setdefault("dispatch", {})
    synced = dispatch_facts.get("synced", [])
    
    for e in entries:
        # 跳过已同步的
        if e["timestamp"] in synced:
            continue
        # 只同步成功的调度，失败的也记
        if e["result"] == "success":
            synced.append(e["timestamp"])
            count += 1
    
    if count > 0:
        dispatch_facts["synced"] = synced[-100:]  # 只保留最近100条同步记录
        dispatch_facts["last_synced_ts"] = entries[0]["timestamp"]
        dispatch_facts["total_synced"] = dispatch_facts.get("total_synced", 0) + count
        json.dump(state, open(engine_state_file, 'w'), indent=2, ensure_ascii=False)
    
    return count


# === CLI ===

def main():
    parser = argparse.ArgumentParser(description="调度链路日志")
    sub = parser.add_subparsers(dest="cmd")
    
    p_record = sub.add_parser("record")
    p_record.add_argument("--from-channel", default="webchat")
    p_record.add_argument("--from-agent", default="main")
    p_record.add_argument("--to-agent", required=True)
    p_record.add_argument("--task", default="")
    p_record.add_argument("--intent", default="")
    p_record.add_argument("--result", default="success")
    p_record.add_argument("--duration", type=float, default=0)
    p_record.add_argument("--detail", default="")
    
    p_query = sub.add_parser("query")
    p_query.add_argument("--limit", type=int, default=20)
    p_query.add_argument("--agent", default="")
    p_query.add_argument("--result", default="")
    
    sub.add_parser("stats")
    sub.add_parser("sync")
    
    args = parser.parse_args()
    
    if args.cmd == "record":
        n = log_dispatch(args.from_channel, args.from_agent, args.to_agent,
                         args.task, args.intent, args.result,
                         args.duration, args.detail)
        print(json.dumps({"ok": True, "entries": n}))
    
    elif args.cmd == "query":
        result = query_recent(args.limit, args.agent, args.result)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.cmd == "stats":
        stats = get_stats()
        print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    elif args.cmd == "sync":
        n = sync_to_engine()
        print(json.dumps({"ok": True, "synced": n}))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
