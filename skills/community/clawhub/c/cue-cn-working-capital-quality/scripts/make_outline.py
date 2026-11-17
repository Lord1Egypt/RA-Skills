#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_outline.py — 零通道那一头：把一份材料清单排成「存货与应收质量卡」的待挂骨架。

一条命令（默认路径，零通道也能独立跑通）：
    python3 -B scripts/make_outline.py --sources <材料清单.jsonl> --out <骨架.md>
    可选：--subject <公司名>　--window <检索窗口>

材料行**必需三键** title / url / asof（asof 是检索日，YYYY-MM-DD）；id 可省，缺省按行序给 S1／S2…
非法 JSON 行、缺键行、asof 不合形**逐行点名，不采信、不静默跳行**。
一条可用行都没有时退 1 —— **空清单不出骨架**，那是没有出处，不是待填。

第二输入模式（可选）：`--outline <章节树.json>`，从章节树摊出五节。**默认必须是 --sources**——
本脚本存在的唯一理由是零通道，而零通道时根本没有 parsed-doc 的 outline；
让 --outline 当默认，等于在最需要它的时候没有输入。

它只做什么（写在件首防后人夸大）：
  1) 把五节标题按契约排好，每节留待挂行位；
  2) 把来源逐条排进末节，编号与 --sources 行序一致；
  3) 未取到逐条点名，一条不省。
它不做什么：不发请求、不取数、不填原句、不填锚。
**骨架过不了 check_working_capital.py 是设计**——占位行会红，提醒你补完再交，
不让一张空壳冒充成品。

退码：0 出骨架；1 无可用材料行（逐行点名为什么不可用）；2 用法错；3 读不到输入。
零网络、纯标准库。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REQUIRED = ("title", "url", "asof")
# 五节契约（与 SKILL.md、check_working_capital.py 的 SECTIONS 同序同名）
SECTIONS = ("存货", "应收账款", "合同资产", "计提与转回", "口径与未取到")
# 每节要留的待挂行位（写成「待挂」，不写「未取到」——骨架的缺口由末节逐条点名，
# 每节都写真“未取到”会让申报数与正文缺口行对不上，凭空多出一堆缺口）
SLOTS = {
    "存货": ("存货账面余额", "存货跌价准备期末余额", "本期计提跌价准备",
             "存货周转天数", "存货同比增速"),
    "应收账款": ("应收账款账面余额", "坏账准备期末余额", "本期计提坏账准备",
                 "应收账款周转天数", "账龄结构（1 年以内）"),
    "合同资产": ("合同资产账面价值", "合同资产减值准备期末余额", "合同资产周转天数"),
    "计提与转回": ("本期计提合计", "本期转回或收回"),
}
MISSING = ("存货周转天数", "应收账款周转天数", "合同资产周转天数",
           "存货同比增速", "账龄结构（1 年以内）")


def load_sources(path: Path):
    """逐行读 JSONL。返回 (rows, rejected)。坏行逐行点名，不静默跳行。"""
    ok, rejected = [], []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (IOError, OSError) as exc:
        return None, [("读不到输入：%s（%s）" % (path, exc))]
    for no, raw in enumerate(text.split("\n"), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as e:
            rejected.append((no, "非法 JSON（%s）" % e.msg))
            continue
        if not isinstance(row, dict):
            rejected.append((no, "不是对象行"))
            continue
        miss = [k for k in REQUIRED if not str(row.get(k) or "").strip()]
        if miss:
            rejected.append((no, "缺键 " + "／".join(miss)))
            continue
        if not DATE_RE.match(str(row["asof"]).strip()):
            rejected.append((no, "asof 不是 YYYY-MM-DD（现值「%s」）" % row["asof"]))
            continue
        ok.append(row)
    return ok, rejected


def build_from_sources(rows, subject, window):
    out = []
    out.append("AI 整理初稿｜请回原文核对｜不构成投资建议｜判断位 [待人工]")
    out.append("")
    out.append("主体：%s｜检索窗口：%s｜材料 %d 条（见末节来源）" % (subject, window, len(rows)))
    out.append("")
    out.append("口径：骨架只排了材料清单，原句、锚与计提事实**全部待挂**；"
               "周转、增速、占比一律待回原句，原句没有就标〔自算〕并交代分子分母。")
    out.append("")
    for k, sec in enumerate(SECTIONS, 1):
        out.append("## %s、%s" % ("一二三四五"[k - 1], sec))
        out.append("")
        if sec == "口径与未取到":
            out.append("- 共 0 项·未取到 0 项")
            out.append("- 未取到 0 项：无。")
            out.append("- 口径：同比基准、周转天数基准（360／365）、余额口径（期末／平均）待回原文核准。")
            out.append("- [待人工] 三块资产的计提节奏、是否存在跨期调节，全部留人工；本件不代判断。")
        else:
            for slot in SLOTS[sec]:
                out.append("- %s：待挂（回原文抄原句并挂锚）" % slot)
        out.append("")
    out.append("## 六、来源索引")
    out.append("")
    for k, row in enumerate(rows, 1):
        sid = str(row.get("id") or "S%d" % k).strip()
        out.append("- [%s] %s｜%s｜检索日 %s"
                   % (sid, str(row["title"]).strip(), str(row["url"]).strip(),
                      str(row["asof"]).strip()))
    out.append("")
    return "\n".join(out)


def build_from_outline(node, subject, window):
    """第二输入模式：把章节树摊成五节。章节名能对上的收进对应节，对不上的收进末节。"""
    def walk(x, acc):
        if isinstance(x, str):
            acc.append(x)
        elif isinstance(x, dict):
            for key, val in x.items():
                name = str(key)
                kids = []
                walk(val, kids)
                acc.append((name, kids))
        elif isinstance(x, list):
            for it in x:
                walk(it, acc)
        return acc

    tree = walk(node, [])
    out = ["AI 整理初稿｜请回原文核对｜不构成投资建议｜判断位 [待人工]", "",
           "主体：%s｜检索窗口：%s｜来源：章节树（--outline 模式，无材料清单；"
           "来源索引须自行补 URL 与检索日）" % (subject, window), ""]
    for k, sec in enumerate(SECTIONS, 1):
        out.append("## %s、%s" % ("一二三四五"[k - 1], sec))
        out.append("")
        hit = [x for x in tree if isinstance(x, tuple) and sec in x[0]]
        if sec == "口径与未取到":
            out.append("- 共 0 项·未取到 0 项")
            out.append("- 未取到 0 项：无。")
            out.append("- 口径：--outline 模式未带材料清单，来源 URL 与检索日待补。")
        elif hit:
            for name, kids in hit:
                out.append("- %s：待挂（章节树命中「%s」，回原文抄原句并挂锚）" % (name, name))
                for kid in kids:
                    if isinstance(kid, tuple):
                        out.append("  - %s：待挂" % kid[0])
        else:
            for slot in SLOTS.get(sec, ()):
                out.append("- %s：待挂（章节树未命中该节，回原文补）" % slot)
        out.append("")
    out.append("## 六、来源索引")
    out.append("")
    out.append("- [S1] 待补｜URL 待补｜检索日 待补")
    out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(
        prog="make_outline.py", add_help=False,
        description="零通道骨架：把材料清单（或章节树）排成存货与应收质量卡的待挂骨架")
    ap.add_argument("--sources", help="材料清单 JSONL（默认路径；三键 title/url/asof）")
    ap.add_argument("--outline", help="章节树 JSON（第二输入模式，与 --sources 二选一）")
    ap.add_argument("--out", help="输出骨架路径")
    ap.add_argument("--subject", default="（待填：公司名与代码）")
    ap.add_argument("--window", default="（待填：检索窗口）")
    ap.add_argument("-h", "--help", action="store_true")
    a = ap.parse_args()

    if a.help or not a.out:
        print(__doc__)
        return 0 if a.help else 2
    if bool(a.sources) == bool(a.outline):
        print("用法错：--sources 与 --outline 必须二选一（默认走 --sources）")
        return 2

    if a.outline:
        src = Path(a.outline)
        if not src.is_file():
            print("取值域故障：读不到章节树 %s（不当「零条可用」读）" % src)
            return 3
        try:
            node = json.loads(src.read_text(encoding="utf-8"))
        except (ValueError, IOError, OSError) as exc:
            print("取值域故障：章节树不可解析（%s）" % exc)
            return 3
        text = build_from_outline(node, a.subject, a.window)
        Path(a.out).write_text(text, encoding="utf-8")
        print("PASS: 骨架已出 %s（--outline 模式）" % a.out)
        print("       代价：没有材料清单，来源索引须自行补 URL 与检索日")
        print("       骨架过不了机检是设计，不是待补的疏漏——别把它当成品交付")
        return 0

    src = Path(a.sources)
    if not src.is_file():
        print("取值域故障：读不到材料清单 %s（不当「零条可用」读）" % src)
        return 3
    rows, rejected = load_sources(src)
    if rows is None:
        for why in rejected:
            print("  " + why)
        return 3
    for no, why in rejected:
        print("  未采信 第 %d 行：%s" % (no, why))
    if not rows:
        print("FAIL: %s 一条可用材料行都没有（未采信 %d 行）——空清单不出骨架，"
              "那是没有出处，不是待填" % (src.name, len(rejected)))
        return 1

    text = build_from_sources(rows, a.subject, a.window)
    Path(a.out).write_text(text, encoding="utf-8")
    print("PASS: 骨架已出 %s（可用 %d 条·未采信 %d 条）" % (a.out, len(rows), len(rejected)))
    print("       代价：缺公告检索与原文解析那一层，骨架只有形状、没有原句与锚")
    print("       骨架过不了机检是设计，不是待补的疏漏——别把它当成品交付")
    return 0


if __name__ == "__main__":
    sys.exit(main())
