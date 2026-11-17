#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pan idle — 闲时下载队列与守护（v0.20.0 F2）。

设计（方案 §四F2）：
- `pan idle add <url> [同 get 的参数]`：把任务写进队列（STATE_DIR/queue/*.json），标记 idle_only。
- `pan idle-daemon`（即 `pan idle run`）：前台常驻循环，每 30 秒检查一次：
  在 http.idle_window（默认 ["00:00","08:00"]）窗口内逐个投递队列任务（子进程跑
  `pan.py get ...`，同一 (drive,source,target) 的单实例锁天然防重复下载）；
  窗口外只睡觉，不占白天带宽。
- PAN_IDLE_FORCE=1：视为永远在窗口内（仅自测用）。
- `pan idle run --print-crontab`：输出一行现成的 cron 条目——**只打印不安装**，
  系统级定时器的修改权在用户手里。
- `--once`：只跑一轮投递循环（自测/手动触发用）。

不做的事：不写 crontab/launchd，不后台化自身（前台进程，Ctrl-C 即停）；
断点续传兜底，daemon 被杀后重启自动接续。
"""
from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_here = _boot_os.path.dirname(_boot_os.path.abspath(__file__))
    _boot_parent = _boot_os.path.dirname(_boot_here)
    for _boot_dir in (_boot_here, _boot_parent):
        if _boot_dir not in _boot_sys.path:
            _boot_sys.path.insert(0, _boot_dir)
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass


import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

try:
    from pancli.engine import STATE_DIR, load_config
except Exception:  # 独立导入（自测）
    STATE_DIR = Path(os.environ.get("PAN_STATE_DIR") or (Path.home() / ".local" / "share" / "pan-downloader"))

    def load_config(*_a, **_k):
        return {}

try:
    from pancli.report import log_line
except Exception:
    def log_line(msg, *a, **k):
        print(msg, flush=True)


def queue_dir(cfg=None) -> Path:
    d = Path(STATE_DIR) / "queue"
    d.mkdir(parents=True, exist_ok=True)
    return d


def idle_window(cfg=None):
    """返回 (start_minutes, end_minutes)；支持跨午夜（如 22:00-06:00）。"""
    cfg = cfg or load_config()
    win = (cfg.get("http") or {}).get("idle_window") or ["00:00", "08:00"]
    def _mm(s):
        try:
            h, m = str(s).split(":", 1)
            return int(h) * 60 + int(m)
        except Exception:
            return None
    a, b = _mm(win[0]), _mm(win[1])
    if a is None or b is None:
        return 0, 8 * 60
    return a, b


def in_window(cfg=None, now=None) -> bool:
    if os.environ.get("PAN_IDLE_FORCE") == "1":
        return True
    a, b = idle_window(cfg)
    t = now or datetime.now()
    cur = t.hour * 60 + t.minute
    if a <= b:
        return a <= cur < b
    return cur >= a or cur < b  # 跨午夜


def cmd_idle(args) -> int:
    sub = getattr(args, "idle_cmd", "")
    cfg = load_config()
    qd = queue_dir(cfg)

    if sub == "add":
        url = args.url
        item = {
            "schema": 1,
            "id": datetime.now().strftime("%Y%m%d%H%M%S") + "-%04d" % (int(time.time() * 1000) % 10000),
            "url": url,
            "argv": args.pass_through or [],
            "created": datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
            "idle_only": True,
        }
        out = qd / (item["id"] + ".json")
        out.write_text(json.dumps(item, ensure_ascii=False, indent=2), encoding="utf-8")
        print("已入闲时队列：%s" % out, flush=True)
        print("窗口：%s" % (cfg.get("http") or {}).get("idle_window", ["00:00", "08:00"]), flush=True)
        return 0

    if sub == "list":
        items = sorted(qd.glob("*.json"))
        if getattr(args, "json", False):
            print(json.dumps({"queued": [json.loads(p.read_text(encoding="utf-8")) for p in items]},
                             ensure_ascii=False, indent=2))
        else:
            if not items:
                print("闲时队列为空")
            for p in items:
                d = json.loads(p.read_text(encoding="utf-8"))
                print("%s  %s" % (d.get("id"), d.get("url")))
        return 0

    if sub == "delete":
        target = None
        for p in sorted(qd.glob("*.json")):
            d = json.loads(p.read_text(encoding="utf-8"))
            if d.get("id") == args.id:
                target = p
                break
        if target is None:
            print("未找到队列任务：%s（pan idle list 查看）" % args.id)
            return 2
        target.unlink()
        print("已删除：%s" % args.id)
        return 0

    if sub == "run":
        return run_daemon(args, cfg, qd)

    print("用法：pan idle add|list|delete|run")
    return 2


def _dispatch_one(item: dict, cfg, qd: Path) -> int:
    """用子进程投递一个队列任务（复用 pan get 的全部既有逻辑与单实例锁）。"""
    pan_py = Path(__file__).resolve().parent.parent / "pan.py"
    argv = [sys.executable, str(pan_py), "get", item["url"]] + list(item.get("argv") or [])
    log_dir = qd / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / (item["id"] + ".log")
    log_line("IDLE_DISPATCH id=%s argv=%s" % (item["id"], " ".join(argv)))
    print("▶ 投递闲时任务 %s（日志 %s）" % (item["id"], log_path), flush=True)
    with log_path.open("a", encoding="utf-8") as lf:
        lf.write("\n==== %s dispatch ====\n" % datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
        lf.flush()
        rc = subprocess.call(argv, stdout=lf, stderr=lf)
    dest = qd / ("done" if rc == 0 else "failed")
    dest.mkdir(parents=True, exist_ok=True)
    try:
        (qd / (item["id"] + ".json")).replace(dest / (item["id"] + ".json"))
    except OSError:
        pass
    log_line("IDLE_DONE id=%s rc=%s" % (item["id"], rc))
    return rc


def run_daemon(args, cfg, qd: Path) -> int:
    once = bool(getattr(args, "once", False))
    print_crontab = bool(getattr(args, "print_crontab", False))
    if print_crontab:
        # 只输出，不安装——装不装、装到哪由用户自己决定（方案 §五边界 3）。
        pan_py = Path(__file__).resolve().parent.parent / "pan.py"
        print("# 每天窗口起点拉起一轮闲时投递（示例：08:00 收尾前兜底；常规用常驻 idle-daemon 即可）")
        print("17 * * * * %s %s idle run --once >> %s/queue/logs/daemon.log 2>&1" % (
            "", sys.executable, pan_py.parent))
        print("# 更简做法：nohup %s %s idle run >> %s/queue/logs/daemon.log 2>&1 &" % (
            sys.executable, pan_py, pan_py.parent))
        return 0

    # daemon 单实例：TaskLock 语义复用（drive=idle, source=daemon, target=queue）
    try:
        from pancli.tasklock import TaskLock
        lock = TaskLock("idle", "daemon", str(qd), note="idle-daemon")
        if not lock.acquire():
            held = lock.held_by or {}
            print("⚠️ 已有 idle-daemon 在跑（pid=%s），退出。" % held.get("pid"))
            return 2
    except Exception:
        lock = None

    a, b = idle_window(cfg)
    print("idle-daemon 启动：窗口 %02d:%02d-%02d:%02d，队列 %s" % (
        a // 60, a % 60, b // 60, b % 60, qd), flush=True)
    if os.environ.get("PAN_IDLE_FORCE") == "1":
        print("PAN_IDLE_FORCE=1：跳过窗口判断（仅自测）", flush=True)
    try:
        while True:
            if in_window(cfg):
                items = sorted(qd.glob("*.json"))
                if items:
                    item = json.loads(items[0].read_text(encoding="utf-8"))
                    _dispatch_one(item, cfg, qd)
                    if once:
                        return 0
                    continue  # 立刻看下一个，不睡
                elif once:
                    print("窗口内但队列为空（--once 退出）")
                    return 0
            elif once:
                a2, b2 = idle_window(cfg)
                print("当前不在闲时窗口 %02d:%02d-%02d:%02d（--once 退出）" % (
                    a2 // 60, a2 % 60, b2 // 60, b2 % 60))
                return 1
            time.sleep(30)
    except KeyboardInterrupt:
        print("idle-daemon 退出（Ctrl-C）。队列保留，重启自动接续。", flush=True)
        return 0
    finally:
        if lock is not None:
            lock.release()
