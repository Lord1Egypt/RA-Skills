#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业技能 Evolution Log 维护器（Continuous Evolution Logger）

为某个技能追加一条 Evolution Log 条目，固化为结构化记录（evolution.jsonl），
并输出可直接粘进 SKILL.md「Evolution Log」段的 markdown 行。方法论见
`references/evolution.md`。

纯标准库，无外部依赖。

用法：
  python evolution_log.py --skill <技能目录> --version v0.4 --change "新增事务安全检查" --trigger "用户 Q1 需求"
  （--skill 省略则写入当前目录；--date 省略则取今天）
"""
import argparse
import datetime as dt
import json
import os
import sys


def main():
    ap = argparse.ArgumentParser(description="企业技能 Evolution Log 维护器")
    ap.add_argument("--skill", default=".", help="技能目录（写入其中的 evolution.jsonl）")
    ap.add_argument("--version", required=True, help="版本号，如 v0.4")
    ap.add_argument("--change", required=True, help="变更内容")
    ap.add_argument("--trigger", default="", help="触发原因")
    ap.add_argument("--date", default=dt.date.today().isoformat(), help="日期 YYYY-MM-DD")
    args = ap.parse_args()

    d = args.skill
    if not os.path.isdir(d):
        print(f"错误: 目录不存在: {d}", file=sys.stderr)
        return 2

    entry = {
        "date": args.date,
        "version": args.version,
        "change": args.change,
        "trigger": args.trigger,
    }
    log_path = os.path.join(d, "evolution.jsonl")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    md = f"- {args.version} ({args.date}) {args.change}" + \
         (f"（触发：{args.trigger}）" if args.trigger else "")
    print("已追加到:", log_path)
    print("Markdown 条目（粘入 SKILL.md Evolution Log）:")
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
