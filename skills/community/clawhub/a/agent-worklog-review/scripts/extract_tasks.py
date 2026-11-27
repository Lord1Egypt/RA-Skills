#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统一会话任务提取器（适配器架构）。

遍历 scripts/adapters/ 下所有适配器，汇总任务记录，统一去重后输出。
新增 Agent 只需加一个适配器文件，不用改本脚本。
输出：$OUTPUT_DIR/all_tasks.jsonl
"""
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import out_dir, load_jsonl
from adapters.base import discover

OUT = os.path.join(out_dir(), "all_tasks.jsonl")


def main():
    adapters = discover()
    # L3 启发式兜底必须最后跑：它要读扫描报告并排除已被其他适配器覆盖的 agent
    adapters.sort(key=lambda a: (getattr(a, "name", "") == "HeuristicFallback",
                                 getattr(a, "name", "")))
    if os.path.exists(OUT):
        os.remove(OUT)
    total = 0
    for a in adapters:
        try:
            rows = a.extract_tasks() or []
            with open(OUT, "a", encoding="utf-8") as f:
                for r in rows:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
            total += len(rows)
            print(f"{a.name}: {len(rows)}")
        except Exception as e:
            print(f"{a.name} FAILED: {str(e)[:120]}")
    # 去重：只去掉 agent+source+session_id+title+timestamp+cwd 完全相同的记录；
    # 不按 session_id 去重（resume 会生成多个文件，是不同任务）。
    seen, dedup = set(), []
    for r in load_jsonl(OUT):
        k = json.dumps([r.get("agent"), r.get("source"), r.get("session_id"),
                        r.get("title"), r.get("timestamp"), r.get("cwd")], ensure_ascii=False)
        if k in seen:
            continue
        seen.add(k)
        dedup.append(r)
    if len(dedup) != total:
        with open(OUT, "w", encoding="utf-8") as f:
            for r in dedup:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"去重: {total} -> {len(dedup)}")
        total = len(dedup)
    print(f"TOTAL: {total} -> {OUT}")


if __name__ == "__main__":
    main()
