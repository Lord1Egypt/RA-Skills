#!/usr/bin/env python3
"""
HOT 层 — 实时会话缓存
跨通道互通的核心：同一Agent在不同通道的对话能互相感知

存储: memory/hot_cache/{agent_id}.json
每条: {text, channel, timestamp, importance, dispatch_from}

写: 对话结束时立即写入
查: 按agent_id获取所有通道的近期会话
"""

import json, sys, argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta

CACHE_DIR = Path.home() / '.agent-mem/hot_cache'
MAX_PER_AGENT = 20
HOT_TTL_HOURS = 2  # working tier对应2小时


def _ensure_dir():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _file_path(agent_id: str) -> Path:
    return CACHE_DIR / f"{agent_id}.json"


def _load(agent_id: str) -> list:
    path = _file_path(agent_id)
    if path.exists():
        try:
            return json.load(open(path))
        except:
            return []
    return []


def _save(agent_id: str, entries: list):
    json.dump(entries, open(_file_path(agent_id), 'w'), indent=2, ensure_ascii=False)


def write_conversation(agent_id: str, channel: str, text: str,
                       importance: int = 5, dispatch_from: str = ""):
    """
    写入一次对话摘要到HOT层
    - agent_id: 哪个Agent的对话
    - channel: 哪个通道 (webchat/feishu/signal/...)
    - text: 对话内容摘要
    - importance: 重要度 1-10
    - dispatch_from: 调度来源 (可选)
    """
    _ensure_dir()
    entries = _load(agent_id)
    
    entry = {
        "text": text[:300],
        "channel": channel,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "importance": importance,
        "dispatch_from": dispatch_from
    }
    
    entries.insert(0, entry)
    entries = entries[:MAX_PER_AGENT]
    _save(agent_id, entries)
    return len(entries)


def query_recent(agent_id: str, channel: str = "", limit: int = 5):
    """
    查询某Agent的最新HOT记忆
    - channel="" 时查所有通道（跨通道互通的关键）
    - channel="webchat" 时只查webchat
    """
    entries = _load(agent_id)
    now = datetime.now(timezone.utc)
    
    result = []
    for e in entries:
        # 跳过超时的 (hot TTL = 2h)
        try:
            ts = datetime.fromisoformat(e["timestamp"])
            if (now - ts).total_seconds() > HOT_TTL_HOURS * 3600:
                continue
        except:
            continue
        
        if channel and e.get("channel", "") != channel:
            continue
        
        result.append(e)
        if len(result) >= limit:
            break
    
    return result


def clear_agent(agent_id: str):
    """清除某Agent的HOT缓存"""
    path = _file_path(agent_id)
    if path.exists():
        path.unlink()
        return True
    return False


def cleanup_expired():
    """清理所有过期HOT缓存"""
    _ensure_dir()
    now = datetime.now(timezone.utc)
    count = 0
    for f in CACHE_DIR.glob("*.json"):
        entries = json.load(open(f))
        fresh = [e for e in entries
                 if (now - datetime.fromisoformat(e["timestamp"])).total_seconds()
                 <= HOT_TTL_HOURS * 3600]
        if len(fresh) != len(entries):
            _save(f.stem, fresh)
            count += len(entries) - len(fresh)
    return count


# === CLI ===

def main():
    parser = argparse.ArgumentParser(description="HOT层：实时会话缓存")
    sub = parser.add_subparsers(dest="cmd")
    
    p_write = sub.add_parser("write")
    p_write.add_argument("--agent", required=True)
    p_write.add_argument("--channel", required=True)
    p_write.add_argument("--text", required=True)
    p_write.add_argument("--importance", type=int, default=5)
    p_write.add_argument("--dispatch-from", default="")
    
    p_query = sub.add_parser("query")
    p_query.add_argument("--agent", required=True)
    p_query.add_argument("--channel", default="")
    p_query.add_argument("--limit", type=int, default=5)
    
    p_clear = sub.add_parser("clear")
    p_clear.add_argument("--agent", required=True)
    
    sub.add_parser("cleanup")
    sub.add_parser("status")
    
    args = parser.parse_args()
    
    if args.cmd == "write":
        n = write_conversation(args.agent, args.channel, args.text, args.importance, args.dispatch_from)
        print(json.dumps({"ok": True, "entries": n}))
    
    elif args.cmd == "query":
        result = query_recent(args.agent, args.channel, args.limit)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.cmd == "clear":
        ok = clear_agent(args.agent)
        print(json.dumps({"ok": ok}))
    
    elif args.cmd == "cleanup":
        n = cleanup_expired()
        print(json.dumps({"ok": True, "cleaned": n}))
    
    elif args.cmd == "status":
        _ensure_dir()
        files = list(CACHE_DIR.glob("*.json"))
        total = 0
        agents = []
        for f in files:
            entries = json.load(open(f))
            total += len(entries)
            agents.append(f"{f.stem}: {len(entries)}条")
        print(json.dumps({
            "agents": len(files),
            "total_entries": total,
            "details": agents
        }, indent=2, ensure_ascii=False))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
