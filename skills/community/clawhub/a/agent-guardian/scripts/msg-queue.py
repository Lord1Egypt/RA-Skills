#!/usr/bin/env python3
"""
消息队列管理器 - 追踪消息处理状态
用法:
  msg-queue.py add "消息内容"    # 新消息入队
  msg-queue.py start "消息内容"  # 标记处理中
  msg-queue.py done              # 标记已完成
  msg-queue.py report            # 生成状态报告
  msg-queue.py reset             # 重置队列
"""
import json, os, sys, time

QUEUE_FILE = "/tmp/agent-msg-queue.json"

def load():
    if os.path.exists(QUEUE_FILE):
        try:
            with open(QUEUE_FILE) as f:
                return json.load(f)
        except:
            pass
    return {"date": "", "msgs": [], "done_today": 0}

def save(data):
    with open(QUEUE_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def clean_date(data):
    today = time.strftime("%Y-%m-%d")
    now = int(time.time())
    if data["date"] != today:
        data["date"] = today
        data["msgs"] = []
        data["done_today"] = 0
    # 自动超时：processing 超5分钟自动标记 done
    for m in data["msgs"]:
        if m["status"] == "processing" and now - m.get("start_at", now) > 300:
            m["status"] = "done"
            m["done_at"] = now
            data["done_today"] = data.get("done_today", 0) + 1
    # 清理超1小时已完成消息
    data["msgs"] = [m for m in data["msgs"]
                    if not (m["status"] == "done" and now - m.get("done_at", 0) > 3600)]
    if len(data["msgs"]) > 30:
        active = [m for m in data["msgs"] if m["status"] in ("processing", "waiting")]
        done_msgs = [m for m in data["msgs"] if m["status"] == "done"]
        data["msgs"] = active + done_msgs[-10:]
    return data

def add(msg):
    data = clean_date(load())
    short = msg[:50] + "..." if len(msg) > 50 else msg
    data["msgs"].append({"msg": short, "status": "waiting", "added_at": int(time.time())})
    save(data)

def start(msg):
    data = clean_date(load())
    for m in data["msgs"]:
        if m["status"] == "waiting":
            m["status"] = "processing"
            m["start_at"] = int(time.time())
            break
    save(data)

def done(msg=None):
    data = clean_date(load())
    now = int(time.time())
    for m in data["msgs"]:
        if m["status"] == "processing":
            m["status"] = "done"
            m["done_at"] = now
            data["done_today"] = data.get("done_today", 0) + 1
            break
    save(data)

def reset():
    today = time.strftime("%Y-%m-%d")
    old = load()
    keep_done = old.get("done_today", 0) if old.get("date") == today else 0
    done_msgs = [m for m in old.get("msgs", []) if m.get("status") == "done"]
    data = {"date": today, "msgs": done_msgs, "done_today": keep_done}
    save(data)
    print(f"OK: queue reset (kept {keep_done} done records)")

def report():
    data = clean_date(load())
    save(data)
    now = int(time.time())
    processing = [m for m in data["msgs"] if m["status"] == "processing"]
    waiting = [m for m in data["msgs"] if m["status"] == "waiting"]
    done_msgs = [m for m in data["msgs"] if m["status"] == "done"]
    recent_done = [m for m in done_msgs if now - m.get("done_at", 0) < 1800]

    lines = []
    lines.append(f"处理中: {len(processing)} 条 | 等待中: {len(waiting)} 条 | 已完成: {data.get('done_today', 0)} 条")

    if processing:
        lines.append("")
        for m in processing:
            elapsed = now - m.get("start_at", now)
            t = f"{elapsed}秒" if elapsed < 60 else f"{elapsed//60}分{elapsed%60}秒"
            tag = "⚠️" if elapsed > 300 else "🔄"
            lines.append(f"{tag} {m['msg']}（已{t}）")

    if waiting:
        lines.append("")
        for i, m in enumerate(waiting[:3]):
            wait_sec = now - m.get("added_at", now)
            wt = f"{wait_sec}秒" if wait_sec < 60 else f"{wait_sec//60}分钟"
            lines.append(f"⏳ #{i+1} {m['msg']}（等{wt}）")
        if len(waiting) > 3:
            lines.append(f"   +{len(waiting)-3}条排队")

    if recent_done:
        lines.append("")
        for m in recent_done[-3:]:
            ago = now - m.get("done_at", now)
            at = f"{ago}秒前" if ago < 60 else f"{ago//60}分钟前"
            cost = ""
            if m.get("start_at") and m.get("done_at"):
                c = m["done_at"] - m["start_at"]
                cost = f" {c}秒" if c < 60 else f" {c//60}分{c%60}秒"
            lines.append(f"✅ {m['msg']}（{at}{cost}）")

    if not processing and not waiting and not recent_done:
        lines.append("💤 空闲中")

    print("\n".join(lines))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: msg-queue.py add|start|done|report|reset [msg]")
        sys.exit(1)
    action = sys.argv[1]
    msg = sys.argv[2] if len(sys.argv) > 2 else ""
    {"add": add, "start": start, "done": done, "report": report, "reset": reset}[action](msg) if action in ("add", "start") else {"done": done, "report": report, "reset": reset}.get(action, lambda: print("Unknown action"))()
