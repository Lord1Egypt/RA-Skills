#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本地任务箱：断网可跑的任务存储与同步（纯标准库，无外部依赖）。

用于「跨机任务箱」的离线闭环模式：两台机器各持一份本地任务箱，
通过交换「同步包.json」合并，不依赖任何云端 API，断网也能完整工作。

用法：
  python local_taskbox.py add "标题" "详情" [--priority 1-9] [--source a|b]
  python local_taskbox.py list
  python local_taskbox.py done <id> "结果文本"
  python local_taskbox.py fail <id> "失败原因"
  python local_taskbox.py delete <id>
  python local_taskbox.py export <path>
  python local_taskbox.py import <path>
"""
import json
import os
import sys
import argparse
import datetime

BOX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "taskbox.json")
STATUSES = ("queued", "running", "done", "failed")


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load():
    """读取任务箱。文件不存在返回空；文件损坏给出明确提示（不闪退）。"""
    if not os.path.exists(BOX_PATH):
        return []
    try:
        with open(BOX_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError):
        print(f"[错误] 任务箱文件 {BOX_PATH} 已损坏或编码异常，无法读取。")
        print("      若需恢复：请用最近的同步包执行 import 重建，或手动检查该文件。")
        sys.exit(1)


def save(tasks):
    with open(BOX_PATH, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def next_id(tasks):
    return max([t.get("id", 0) for t in tasks], default=0) + 1


def add(title, detail="", priority=5, source="a"):
    if not title or not title.strip():
        print("[错误] 标题不能为空。用法：add \"标题\" [\"详情\"]")
        sys.exit(1)
    if priority < 1 or priority > 9:
        print("[错误] 优先级需在 1-9 之间（数字越大越优先）。")
        sys.exit(1)
    tasks = load()
    t = {
        "id": next_id(tasks),
        "title": title.strip(),
        "detail": detail,
        "status": "queued",
        "priority": priority,
        "source": source,
        "created_at": now(),
        "updated_at": now(),
        "result": "",
    }
    tasks.append(t)
    save(tasks)
    print(f"已添加任务 #{t['id']}：{t['title']}")
    return t


def find_task(tasks, tid):
    for t in tasks:
        if t["id"] == tid:
            return t
    return None


def list_tasks():
    tasks = load()
    if not tasks:
        print("（任务箱为空）")
        return
    for t in tasks:
        print(
            f"[{t['id']}] {t['status']:7} P{t.get('priority',5)} "
            f"{t['title']}  ({t.get('source','?')})"
        )


def mark_done(tid, result):
    tasks = load()
    t = find_task(tasks, tid)
    if not t:
        print(f"未找到任务 #{tid}（可用 list 查看现有任务 id）")
        return
    t["status"] = "done"
    t["result"] = result
    t["updated_at"] = now()
    save(tasks)
    print(f"任务 #{tid} 已标记完成")


def mark_fail(tid, reason):
    tasks = load()
    t = find_task(tasks, tid)
    if not t:
        print(f"未找到任务 #{tid}（可用 list 查看现有任务 id）")
        return
    t["status"] = "failed"
    t["result"] = reason
    t["updated_at"] = now()
    save(tasks)
    print(f"任务 #{tid} 已标记失败")


def delete_task(tid):
    tasks = load()
    t = find_task(tasks, tid)
    if not t:
        print(f"未找到任务 #{tid}（可用 list 查看现有任务 id）")
        return
    tasks = [x for x in tasks if x["id"] != tid]
    save(tasks)
    print(f"任务 #{tid} 已删除")


def export_pack(path):
    """导出同步包（含全部任务），供对方机器 import 合并。"""
    tasks = load()
    pack = {"exported_at": now(), "tasks": tasks}
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pack, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"[错误] 导出失败：{e}（请检查路径是否可写）")
        sys.exit(1)
    print(f"已导出 {len(tasks)} 个任务到 {path}")


def import_pack(path):
    """导入对方同步包，按 id 去重，保留 updated_at 较新者。"""
    if not os.path.exists(path):
        print(f"[错误] 导入文件不存在：{path}（请检查文件名/路径是否正确）")
        sys.exit(1)
    try:
        with open(path, "r", encoding="utf-8") as f:
            pack = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError, OSError) as e:
        print(f"[错误] 导入文件无法解析：{path}（{e}）")
        print("      请确认该文件是有效的同步包（export 命令产物）。")
        sys.exit(1)
    incoming = pack.get("tasks", [])
    tasks = load()
    by_id = {t["id"]: t for t in tasks}
    merged = 0
    for t in incoming:
        tid = t["id"]
        if tid not in by_id or t["updated_at"] > by_id[tid]["updated_at"]:
            by_id[tid] = t
            merged += 1
    tasks = sorted(by_id.values(), key=lambda x: x["id"])
    save(tasks)
    print(f"已合并 {merged} 个任务（来自 {path}），当前共 {len(tasks)} 个")


def main():
    p = argparse.ArgumentParser(description="本地任务箱（断网闭环）v1.0.1")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("list")
    a = sub.add_parser("add")
    a.add_argument("title")
    a.add_argument("detail", nargs="?", default="")
    a.add_argument("--priority", type=int, default=5)
    a.add_argument("--source", default="a")
    d = sub.add_parser("done")
    d.add_argument("id", type=int)
    d.add_argument("result", nargs="?", default="")
    f = sub.add_parser("fail")
    f.add_argument("id", type=int)
    f.add_argument("reason", nargs="?", default="")
    dl = sub.add_parser("delete")
    dl.add_argument("id", type=int)
    e = sub.add_parser("export")
    e.add_argument("path")
    i = sub.add_parser("import")
    i.add_argument("path")
    args = p.parse_args()

    if args.cmd == "list" or args.cmd is None:
        list_tasks()
    elif args.cmd == "add":
        add(args.title, args.detail, args.priority, args.source)
    elif args.cmd == "done":
        mark_done(args.id, args.result)
    elif args.cmd == "fail":
        mark_fail(args.id, args.reason)
    elif args.cmd == "delete":
        delete_task(args.id)
    elif args.cmd == "export":
        export_pack(args.path)
    elif args.cmd == "import":
        import_pack(args.path)


if __name__ == "__main__":
    main()
