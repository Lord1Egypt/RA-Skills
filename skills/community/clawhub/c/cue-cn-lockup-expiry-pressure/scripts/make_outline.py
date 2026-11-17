#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_outline.py — 把解禁清单排成带形状的骨架（零网络、零计费、不读凭据）

输入：一份 JSONL 清单，一行一轮解禁，字段（缺一个就报错，不猜）：
    {"date": "2026-12-20", "type": "定增对象", "shares": "180000000",
     "pct": "4.50", "total": "4000000000", "price": "6.80", "note": "…"}

输出：一份七节骨架 .md。**日历与来源行按清单落位，结论、占比出处与成本区间留占位**——
骨架跑机检必然红在占位行上，这是设计：提醒你补完再交，不让空壳冒充成品。

用法：
    python3 scripts/make_outline.py 清单.jsonl 骨架.md
    python3 scripts/make_outline.py 清单.jsonl          # 打到 stdout

退码：0 排出骨骼 / 1 输入有坏行（逐行点名）/ 2 用法错 / 3 读不到输入。
"""

import json
import sys

TYPES = ("控股股东", "实际控制人", "董监高", "定增对象", "股权激励对象",
         "首发原股东", "战略投资者", "其他")

PLACEHOLDER_DATE = "待填基准日"
PLACEHOLDER = "待填"

HEAD = """AI 整理初稿｜请回原文核对｜不构成投资建议｜判断位 [待人工]

基准日：%s
跟踪口径：解禁（未来解禁的时间表与可算的压力比值，同一只股票的限售股逐轮串起来）

## 一、一句话结论

[待人工] 补完日历与占比后写一句话结论。

## 二、解禁总览

- 总股本：%s 股 [S3]
- 第 N 轮成本区间：%s 元／股 [S1]

## 三、解禁日历

%s

## 四、压力测算

%s

## 五、未决事项

- [待人工] 下一轮解禁日是否确定、相关股东是否已作承诺，回原文补齐。

## 六、未取到与口径

- 未取到 占比出处：本骨架占比取自清单，未回原文核对，补完须逐行改标。
- 口径：分母总股本 %s，时点待回原文核准；不同时点总股本不一样。

## 七、来源

%s
"""


def load_sources(path):
    """逐行读 JSONL。返回 (rows, errors)。"""
    rows, errors = [], []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except (IOError, OSError) as exc:
        return None, ["读不到输入：%s（%s）" % (path, exc)]

    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        if not s:
            continue
        try:
            obj = json.loads(s)
        except ValueError as exc:
            errors.append("第 %d 行不是合法 JSON（%s）" % (i, exc))
            continue
        if not isinstance(obj, dict):
            errors.append("第 %d 行不是对象" % i)
            continue
        miss = [k for k in ("date", "type", "shares", "total") if not obj.get(k)]
        if miss:
            errors.append("第 %d 行缺字段：%s" % (i, "、".join(miss)))
            continue
        if obj["type"] not in TYPES:
            errors.append("第 %d 行解禁方类型不在册：%s（在册：%s）"
                          % (i, obj["type"], "／".join(TYPES)))
            continue
        d = str(obj["date"]).strip()
        if len(d) != 10 or d[4] != "-" or d[7] != "-":
            errors.append("第 %d 行 date 不是 YYYY-MM-DD：%s" % (i, d))
            continue
        rows.append(obj)
    return rows, errors


def build(rows, base=None, total=None):
    ordered = sorted(rows, key=lambda r: str(r["date"]))
    total = total or (ordered[0].get("total") if ordered else None) or PLACEHOLDER
    base = base or PLACEHOLDER_DATE

    cal = []
    for r in ordered:
        note = r.get("note") or "一句话事实待补"
        cal.append("- %s｜%s｜%s [S1]" % (r["date"], r["type"], note))

    press = []
    for n, r in enumerate(ordered, 1):
        pct = r.get("pct")
        if pct:
            press.append(
                "- 第 %d 轮 %s｜解禁 %s 股／占总股本 %s%%（分母总股本 %s 股）"
                "｜占比出处：%s [S1][S2]"
                % (n, r["date"], r["shares"], pct, r.get("total") or total, PLACEHOLDER))
        else:
            press.append(
                "- 第 %d 轮 %s｜解禁 %s 股／占总股本 %s%%（分母总股本 %s 股）"
                "｜占比出处：%s [S1][S2]"
                % (n, r["date"], r["shares"], PLACEHOLDER, r.get("total") or total,
                   PLACEHOLDER))

    prices = [r.get("price") for r in ordered if r.get("price")]
    price_line = prices[0] if prices else PLACEHOLDER

    srcs = ["- [S1] %s %s 检索日 %s" % (r.get("title") or "公告标题待补",
                                        r.get("url") or "URL待补",
                                        r.get("asof") or PLACEHOLDER_DATE)
            for r in ordered]
    srcs.append("- [S2] 总股本来源（三季报或最近一次股本变动公告）URL待补 检索日 %s"
                % PLACEHOLDER_DATE)

    return HEAD % (base, total, price_line, "\n".join(cal),
                   "\n".join(press), total, "\n".join(srcs))


def main(argv):
    if len(argv) < 2 or len(argv) > 3:
        print(__doc__)
        return 2
    rows, errors = load_sources(argv[1])
    if rows is None:
        for e in errors:
            print("坏 " + e)
        return 3
    if errors:
        for e in errors:
            print("坏 " + e)
        print("——\n共 %d 行坏行，未排骨架（改完再跑）" % len(errors))
        return 1
    if not rows:
        print("坏 输入没有可用行")
        return 1

    text = build(rows)
    if len(argv) == 3:
        with open(argv[2], "w", encoding="utf-8") as fh:
            fh.write(text)
        print("排出骨架：%s（%d 轮解禁，%d 字节）" % (argv[2], len(rows), len(text.encode("utf-8"))))
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
