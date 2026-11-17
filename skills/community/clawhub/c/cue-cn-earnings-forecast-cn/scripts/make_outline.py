#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_outline.py — 把业绩预告清单排成带形状的骨架（零网络、零计费、不读凭据）

输入：一份 JSONL 清单，一行一份预告／快报，字段（缺 date/type 就报错，不猜）：
    {"date": "2026-11-09", "type": "预增",
     "low": "32000", "high": "38000", "unit": "万元",
     "yoy": "比上年同期增长 45.12% 至 72.35%",
     "reason": "主要产品销量增长及毛利率提升",
     "revised": false, "title": "…", "url": "…", "asof": "2026-11-09"}

输出：一份六节骨架 .md。**六项与来源行按清单落位，能填的填原值，缺的留占位**——
骨架跑机检必然红在占位行上，这是设计：提醒你补完再交，不让空壳冒充成品。

**本脚本不取中值、不算同比、不拿修正前后相减。** 清单里没给的幅度一律留「未取到」，
清单里给的是原句就直接落位。这两条与 check_forecast.py 的 FC-CALC 同一套纪律。

用法：
    python3 scripts/make_outline.py 清单.jsonl 骨架.md
    python3 scripts/make_outline.py 清单.jsonl          # 打到 stdout

退码：0 排出骨骼 / 1 输入有坏行（逐行点名）/ 2 用法错 / 3 读不到输入。
"""

import json
import sys

TYPES = ("预增", "预减", "扭亏", "首亏", "续盈", "续亏", "略增", "略减", "不确定")

PLACEHOLDER_DATE = "待填基准日"
PLACEHOLDER = "未取到"

HEAD = """AI 整理初稿｜请回原文核对｜不构成投资建议｜判断位 [待人工]

基准日：%s
数据口径：业绩预告（单份预告文件逐项登记，不评已出财报，不推断正式数）

## 一、一句话结论

%s

## 二、预告要素

%s

## 三、修正沿革

%s

## 四、未决事项

- 正式财报尚未披露，最终数据以经审计报告为准 [待人工]

## 五、未取到与口径

%s
- 口径：区间与同比幅度均照抄披露原句，未取中值，未做前后相减 [S1]

## 六、来源

%s
"""


def load_rows(path):
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
        miss = [k for k in ("date", "type") if not obj.get(k)]
        if miss:
            errors.append("第 %d 行缺字段：%s" % (i, "、".join(miss)))
            continue
        if obj["type"] not in TYPES:
            errors.append("第 %d 行预告类型不在册：%s（在册：%s）"
                          % (i, obj["type"], "／".join(TYPES)))
            continue
        d = str(obj["date"]).strip()
        if len(d) != 10 or d[4] != "-" or d[7] != "-":
            errors.append("第 %d 行 date 不是 YYYY-MM-DD：%s" % (i, d))
            continue
        rows.append(obj)
    return rows, errors


def _q(val, src="[S1]"):
    """把清单里的值落成「原句」+ 锚；空值落成未取到。"""
    if val is None or str(val).strip() == "":
        return "「%s」%s" % (PLACEHOLDER, src)
    return "「%s」%s" % (str(val).strip(), src)


def build(rows, base=None, asof=None):
    if not rows:
        rows = [{}]
    r = rows[0]
    asof = asof or r.get("asof") or PLACEHOLDER_DATE
    # 基准日通常＝检索日；清单给了 asof 就直接用，没给才留占位
    base = base or (asof if asof != PLACEHOLDER_DATE else PLACEHOLDER_DATE)

    unit = r.get("unit") or ""
    low = r.get("low")
    high = r.get("high")
    low_s = ("%s %s" % (low, unit)).strip() if low else None
    high_s = ("%s %s" % (high, unit)).strip() if high else None

    concl = ("- 本份预告类型为「%s」，区间「%s 至 %s」[S1]。"
             % (r.get("type") or PLACEHOLDER, low_s or PLACEHOLDER, high_s or PLACEHOLDER))

    elems = [
        "- 预告类型：%s" % _q(r.get("type")),
        "- 区间下限：%s" % _q(low_s),
        "- 区间上限：%s" % _q(high_s),
        "- 同比变动幅度：%s" % _q(r.get("yoy")),
        "- 变动原因：%s" % _q(r.get("reason")),
        "- 披露日：%s" % _q(r.get("date")),
    ]

    if r.get("revised"):
        fix = ("- 修正前：%s\n- 修正后：%s\n- 修正说明：%s"
               % (_q(r.get("prev_low_s") or r.get("prev_value")),
                  _q(("%s 至 %s" % (low_s, high_s)) if (low_s and high_s) else None),
                  _q(r.get("revise_note"))))
    else:
        fix = "- 修正情况：%s" % _q("未发生修正／首次披露")

    miss = []
    for key, label in (("low", "区间下限"), ("high", "区间上限"),
                       ("yoy", "同比变动幅度"), ("reason", "变动原因")):
        if not r.get(key):
            miss.append("- 未取到 %s：披露文件未给这一项，需回原文核对 [S1]" % label)
    if not miss:
        miss.append("- 未取到 分季度拆分：预告一般只给合并口径区间 [S1]")

    srcs = ["- [S1] %s %s 检索日 %s"
            % (r.get("title") or "文件标题待补", r.get("url") or "URL待补", asof)]

    return HEAD % (base, concl, "\n".join(elems), fix, "\n".join(miss), "\n".join(srcs))


def main(argv):
    if len(argv) < 2 or len(argv) > 3:
        print(__doc__)
        return 2
    rows, errors = load_rows(argv[1])
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
        print("排出骨架：%s（%d 行清单，%d 字节）"
              % (argv[2], len(rows), len(text.encode("utf-8"))))
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
