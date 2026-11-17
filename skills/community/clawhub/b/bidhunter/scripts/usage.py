#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BidHunter 本地埋点模块
======================

用途
----
记录「用户走到哪一步就断了」，用于定位首跑漏斗的断裂点。

设计约束（硬性）
----------------
1. **零云成本、绝不外传**：只写本地文件 `~/.config/bidhunter/usage.jsonl`
2. **不含用户输入内容**：只记录事件名 + 时间戳（+ 可选的非敏感字段），
   不记录主体名称、行业词、地区、文件内容等任何用户输入
3. **永不中断主流程**：任何异常静默吞掉，埋点失败不得影响功能
4. 仅用标准库

事件定义
--------
    demo_start    开始跑 demo
    demo_done     demo 跑完
    init_start    开始 init 引导
    init_done     init 引导完成（生成配置成功）
    first_result  首次产出研判结果
    paste_done    paste 零配置兜底完成

用法
----
    python3 usage.py --selftest          # 自检
    python3 usage.py --stats             # 查看本地统计
    python3 usage.py dump                # 输出原始记录

    代码中：
    from usage import track
    track("demo_start")
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

USAGE_PATH = Path.home() / ".config" / "bidhunter" / "usage.jsonl"

EVENTS = (
    "demo_start",
    "demo_done",
    "init_start",
    "init_done",
    "first_result",
    "paste_done",
)

# 允许附加的字段白名单——只能是枚举型，绝不能是自由文本
ALLOWED_FIELDS = ("ok", "channel")


def track(event, **fields):
    """记录一个事件。任何失败静默返回 False，绝不抛异常。"""
    try:
        if event not in EVENTS:
            return False
        rec = {"event": event, "ts": datetime.now().isoformat(timespec="seconds")}
        for k, v in fields.items():
            if k in ALLOWED_FIELDS and isinstance(v, (bool, int, str)):
                rec[k] = v
        USAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(USAGE_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        return True
    except Exception:
        return False


def load():
    """读取全部记录，文件不存在或损坏时返回空列表。"""
    if not USAGE_PATH.exists():
        return []
    out = []
    try:
        with open(USAGE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except Exception:
                    continue
    except Exception:
        return []
    return out


def stats():
    """按事件聚合计数，并给出漏斗转化率。"""
    recs = load()
    counts = {e: 0 for e in EVENTS}
    for r in recs:
        e = r.get("event")
        if e in counts:
            counts[e] += 1
    return {"total": len(recs), "counts": counts, "path": str(USAGE_PATH)}


def funnel():
    """首跑漏斗：demo 完成率 / init 完成率 / 是否出过结果。"""
    c = stats()["counts"]
    out = {}
    if c.get("demo_start"):
        out["demo_done_rate"] = round(c.get("demo_done", 0) / c["demo_start"] * 100, 1)
    if c.get("init_start"):
        out["init_done_rate"] = round(c.get("init_done", 0) / c["init_start"] * 100, 1)
    out["first_result"] = c.get("first_result", 0)
    return out


def selftest():
    ok = True

    def check(name, cond):
        nonlocal ok
        print(f"  {'✓' if cond else '✗'} {name}")
        if not cond:
            ok = False

    print("usage.py 自检")
    check("事件白名单非空", len(EVENTS) > 0)
    check("未注册事件被拒", track("__not_an_event__") is False)
    # 自由文本字段必须被过滤
    check("敏感字段被过滤", track("demo_start", secret="我的公司名") is True)
    recs = load()
    last = recs[-1] if recs else {}
    check("记录内不含 secret", "secret" not in last)
    check("记录含事件名", last.get("event") == "demo_start")
    check("记录含时间戳", "ts" in last)
    check("统计可用", isinstance(stats()["total"], int))
    check("漏斗可用", isinstance(funnel(), dict))
    print("\n" + ("自检全部通过 ✓" if ok else "存在失败项 ✗"))
    return 0 if ok else 1


def main():
    import argparse
    ap = argparse.ArgumentParser(description="BidHunter 本地埋点（仅写本地，绝不外传）")
    ap.add_argument("cmd", nargs="?", choices=["dump", "stats", "funnel"],
                    help="dump=原始记录 stats=计数 funnel=漏斗")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--stats", action="store_true", help="同 stats 子命令")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    cmd = args.cmd or ("stats" if args.stats else "stats")
    if cmd == "dump":
        for r in load():
            print(json.dumps(r, ensure_ascii=False))
        return 0
    if cmd == "funnel":
        print(json.dumps(funnel(), ensure_ascii=False, indent=2))
        return 0

    s = stats()
    print(f"本地埋点文件: {s['path']}")
    print(f"总事件数: {s['total']}")
    for e in EVENTS:
        print(f"  {e:<14} {s['counts'].get(e, 0)}")
    print("\n漏斗:")
    print(json.dumps(funnel(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
