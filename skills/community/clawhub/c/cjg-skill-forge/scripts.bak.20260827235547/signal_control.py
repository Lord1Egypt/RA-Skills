#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""技能信号透明控制（查看 / 导出 / 删除 / 状态）。

让用户对自己被记录的方法层信号拥有完全知情权与控制权：
  - view    查看已记录信号的汇总（仅方法层标签，零原文）
  - status  查看本地记录 / 云端同步开关当前值
  - export  把 signals-log.jsonl 复制到指定路径（不改原文件）
  - delete  清空本机信号产物（signals-log.jsonl / .anon_id / .uploaded_ids.txt）

默认作用于本技能目录；用 --dir <技能目录> 指定其他技能。
失败静默、零阻塞，不影响主链路。
"""
import os
import sys
import json
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DIR = os.path.dirname(HERE)  # skill-forge/scripts -> skill-forge


def _p(dir_, name):
    return os.path.join(dir_, name)


def _read_lines(dir_):
    path = _p(dir_, "signals-log.jsonl")
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [json.loads(l) for l in f if l.strip()]
    except Exception:
        return []


def _read_flag(dir_, name, default):
    path = _p(dir_, name)
    if not os.path.exists(path):
        return default
    try:
        return open(path, "r", encoding="utf-8").read().strip().lower() or default
    except Exception:
        return default


def cmd_view(dir_):
    lines = _read_lines(dir_)
    if not lines:
        print("[view] 本机暂无记录的进化信号（本地记录默认开，但还没产生，或已清空）。")
        return
    ts = [l.get("ts", "") for l in lines if l.get("ts")]
    layers = {}
    events = {}
    for l in lines:
        k = l.get("method_layer", "?")
        layers[k] = layers.get(k, 0) + 1
        e = l.get("event", "?")
        events[e] = events.get(e, 0) + 1
    print(f"[view] 共 {len(lines)} 条方法层信号")
    if ts:
        print(f"       时间跨度：{min(ts)} ~ {max(ts)}")
    print("       方法层分布：" + "，".join(f"{k}×{v}" for k, v in sorted(layers.items())))
    print("       事件分布  ：" + "，".join(f"{k}×{v}" for k, v in sorted(events.items())))
    print("       （仅方法层标签，零原文、零身份；说\"删除我的信号\"可清空本机记录）")


def cmd_status(dir_):
    optin = _read_flag(dir_, ".optin", "on")
    cloud = _read_flag(dir_, ".cloud_optin", "off")
    print(f"[status] 本地记录（.optin）：{optin}")
    print(f"[status] 云端同步（.cloud_optin）：{cloud}")
    print(f"[status] 信号文件：{_p(dir_, 'signals-log.jsonl')}")


def cmd_export(dir_, dest):
    src = _p(dir_, "signals-log.jsonl")
    if not os.path.exists(src):
        print("[export] 没有可导出的信号文件。")
        return
    try:
        shutil.copy2(src, dest)
        print(f"[export] 已复制 {src} -> {dest}")
    except Exception as e:
        print(f"[export] 导出失败：{e}")


def cmd_delete(dir_, force):
    targets = ["signals-log.jsonl", ".anon_id", ".uploaded_ids.txt"]
    if not force:
        try:
            ans = input("[delete] 确认清空本机信号产物（signals-log.jsonl/.anon_id/.uploaded_ids.txt）？[y/N] ").strip().lower()
        except Exception:
            ans = ""
        if ans not in ("y", "yes"):
            print("[delete] 已取消。")
            return
    for t in targets:
        p = _p(dir_, t)
        if os.path.exists(p):
            try:
                os.remove(p)
                print(f"[delete] 已删除 {p}")
            except Exception as e:
                print(f"[delete] 删除失败 {p}：{e}")
    print("[delete] 完成。本地记录已清空；说\"再开\"可恢复（从空重新累积）。")


def main():
    args = sys.argv[1:]
    dir_ = DEFAULT_DIR
    rest = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--dir":
            if i + 1 < len(args):
                dir_ = args[i + 1]
            i += 2
        else:
            rest.append(a)
            i += 1
    cmd = rest[0] if rest else None
    if cmd == "view":
        cmd_view(dir_)
    elif cmd == "status":
        cmd_status(dir_)
    elif cmd == "export":
        paths = [a for a in rest if a != "export"]
        if not paths:
            print("[export] 用法：python signal_control.py export <目标路径> [--dir <技能目录>]")
            return
        cmd_export(dir_, paths[0])
    elif cmd == "delete":
        cmd_delete(dir_, "--force" in rest)
    else:
        print(__doc__)
        print("用法：")
        print("  python signal_control.py view    [--dir <技能目录>]")
        print("  python signal_control.py status  [--dir <技能目录>]")
        print("  python signal_control.py export <目标路径> [--dir <技能目录>]")
        print("  python signal_control.py delete  [--force] [--dir <技能目录>]")


if __name__ == "__main__":
    main()
