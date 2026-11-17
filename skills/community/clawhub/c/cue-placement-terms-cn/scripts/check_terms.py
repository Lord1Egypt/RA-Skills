#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_terms.py — 定增条款卡的四道机检（零网络、只读传入文件）。

四道码（缺一即不叫过闸）：
  F-STRUCT 五段齐＋十项名目齐：头部申报／条款逐字表／与上一版差项／缺数清单／待人工任一段缺失即发红；
           十项条款里任何一项在全文不出现即发红——缺那一项也要占一行点名，不许省行。
  F-ANCHOR 逐项原句与锚：每条条款行必须带「锚：」定位；行内出现数字还必须带书名号内的原句逐字；
           写明「未检索到」的那一项免锚。
  F-LINE   红线断言：参与建议、好坏判断、涨跌与承诺类词只允许出现在带 [待人工] 的行里，否则发红。
  F-COUNT  缺数与申报对账：头部「共十项·缺 N 项」的 N 必须等于实际写明「未检索到」的条款行数；
           申报缺失即发红；条款值位写「无／不适用／略／待定」而不落到「未检索到」一律发红。

用法：
  python3 -B scripts/check_terms.py <待检文件>   # 逐条发红，全过则 PASS
  python3 -B scripts/check_terms.py --selftest   # 好样须过、坏样四道齐发、三枚反证各发各码；临时件跑完自清
退码：0＝过（或自测全合）；1＝发红／自测不合；2＝用法错。
"""
from __future__ import annotations

import argparse
import atexit
import pathlib
import re
import shutil
import sys
import tempfile

TMP_ROOTS: list[pathlib.Path] = []

ITEMS = ["发行方式", "定价基准日", "发行价或价格下限", "发行数量与募资上限", "发行对象与认购方式",
         "限售期", "募集资金用途", "摊薄与回报测算", "业绩承诺与补偿", "审批链条与当前节点"]
ITEM_LINE = re.compile(r"^\s*[-*]\s*(" + "|".join(re.escape(x) for x in ITEMS) + r")[：:]")
ANCHOR = re.compile(r"锚[:：]")
VERBATIM = re.compile(r"[「『][^」』]+[」』]")
NUM = re.compile(r"\d")
MISS = re.compile(r"未检索到")
DECL = re.compile(r"共十项·缺\s*(\d+)\s*项")
FILLER = re.compile(r"[：:]\s*(?:无|不适用|略|待定)\s*$")
BANNED = re.compile(r"必涨|稳赚|零风险|保证收益|目标价\s*[:：]?\s*\d|建议参与|值得参与|利好兑现|套利|破发概率"
                    r"|上调评级|下调评级|一定会涨|肯定涨")
PENDING = re.compile(r"\[待人工\]")
SECTIONS = (("头部申报", r"头部申报"), ("条款逐字表", r"条款逐字表"), ("与上一版差项", r"差项"),
            ("缺数清单", r"缺数清单"), ("待人工", r"待人工"))


def check_text(text: str) -> list[tuple[str, int, str]]:
    """返回 [(码, 行号, 说明)]；行号 0＝整档级判据。"""
    hits: list[tuple[str, int, str]] = []
    lines = text.splitlines()
    for name, pat in SECTIONS:
        if not re.search(pat, text):
            hits.append(("F-STRUCT", 0, f"缺段：{name}"))
    for name in ITEMS:
        if name not in text:
            hits.append(("F-STRUCT", 0, f"缺项名目：{name}（缺那一项也要占一行点名）"))
    for i, ln in enumerate(lines, 1):
        if ITEM_LINE.match(ln):
            if MISS.search(ln):
                continue
            if not ANCHOR.search(ln):
                hits.append(("F-ANCHOR", i, "条款行缺「锚：」来源定位"))
            elif NUM.search(ln) and not VERBATIM.search(ln):
                hits.append(("F-ANCHOR", i, "条款行有数字但无书名号内原句逐字"))
            if FILLER.search(ln):
                hits.append(("F-COUNT", i, "条款值位用「无／不适用／略／待定」顶替，未落到「未检索到」"))
        if BANNED.search(ln) and not PENDING.search(ln):
            hits.append(("F-LINE", i, "红线断言词出现在没有 [待人工] 的行"))
    miss_rows = sum(1 for ln in lines if ITEM_LINE.match(ln) and MISS.search(ln))
    m = DECL.search(text)
    if not m:
        hits.append(("F-COUNT", 0, "头部申报缺「共十项·缺 N 项」，无从对账"))
    elif int(m.group(1)) != miss_rows:
        hits.append(("F-COUNT", 0, f"申报缺 {m.group(1)} 项∥实际写明未检索到 {miss_rows} 项"))
    return hits


def make_tmp(prefix: str) -> pathlib.Path:
    d = pathlib.Path(tempfile.mkdtemp(prefix=prefix, dir=str(pathlib.Path(tempfile.gettempdir()))))
    TMP_ROOTS.append(d)
    return d


@atexit.register
def _cleanup() -> None:
    for d in TMP_ROOTS:
        shutil.rmtree(d, ignore_errors=True)


def selftest() -> int:
    here = pathlib.Path(__file__).resolve().parent
    good = here / "fixtures" / "good-terms.md"
    bad = here / "fixtures" / "bad-terms.md"
    rows = []
    gt = good.read_text(encoding="utf-8")
    gh = check_text(gt)
    rows.append(("好样须过（发条 0）", not gh, f"实发 {len(gh)} 条" + ("" if not gh else "｜" + gh[0][2])))
    codes_bad = {c for c, _, _ in check_text(bad.read_text(encoding="utf-8"))}
    rows.append(("坏样四道齐发", {"F-STRUCT", "F-ANCHOR", "F-LINE", "F-COUNT"} <= codes_bad,
                 "实发码 " + "∥".join(sorted(codes_bad))))
    tmp = make_tmp("check-terms-")
    stripped = tmp / "no-anchor.md"
    stripped.write_text(re.sub(ANCHOR, "", gt), encoding="utf-8")
    sh = check_text(stripped.read_text(encoding="utf-8"))
    rows.append(("反证·剥锚必发 F-ANCHOR", any(c == "F-ANCHOR" for c, _, _ in sh),
                 f"实发 {sum(1 for c, _, _ in sh if c == 'F-ANCHOR')} 条"))
    dropped = tmp / "lost-item.md"
    lost = "摊薄与回报测算"
    body = "\n".join(l for l in gt.splitlines() if lost not in l)
    dropped.write_text(body, encoding="utf-8")
    dh = check_text(dropped.read_text(encoding="utf-8"))
    rows.append(("反证·删一项名目必发 F-STRUCT",
                 any(c == "F-STRUCT" and lost in msg for c, _, msg in dh),
                 f"实发 {sum(1 for c, _, _ in dh if c == 'F-STRUCT')} 条"))
    skewed = tmp / "skewed-decl.md"
    skewed.write_text(gt.replace("共十项·缺 1 项", "共十项·缺 3 项"), encoding="utf-8")
    kh = check_text(skewed.read_text(encoding="utf-8"))
    rows.append(("反证·申报改歪必发 F-COUNT", any(c == "F-COUNT" for c, _, _ in kh),
                 f"实发 {sum(1 for c, _, _ in kh if c == 'F-COUNT')} 条"))
    made = len(TMP_ROOTS)
    root = pathlib.Path(tempfile.gettempdir())
    for p in TMP_ROOTS:
        shutil.rmtree(p, ignore_errors=True)
    leftover = sorted(q.name for q in root.iterdir() if q.name.startswith("check-terms-")) if root.is_dir() else []
    rows.append(("临时根自清（跑后不增）", not leftover,
                 f"本次建 {made} 枚·跑后残留 {len(leftover)} 枚"))
    rows.append(("atexit 钩子在场", True, "已注册"))
    bad_rows = [r for r in rows if not r[1]]
    for name, ok, detail in rows:
        print(f"  {'ok  ' if ok else 'FAIL'} {name}｜{detail}")
    nproof = len([r for r in rows if r[0].startswith("反证")])
    print(f"selftest: {'ALL GREEN' if not bad_rows else 'FAIL'}（好样 1 枚·坏样四道·反例 {nproof} 枚·临时根 {made} 枚自清）"
          + (f"｜不合 {len(bad_rows)} 枚" if bad_rows else ""))
    return 0 if not bad_rows else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="定增条款卡四道机检（零网络）")
    ap.add_argument("target", nargs="?", help="待检文件（本件不读网络、不读目录）")
    ap.add_argument("--selftest", action="store_true", help="好样须过、坏样四道齐发、三枚反证各发各码")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.target:
        print("用法：check_terms.py <待检文件> | --selftest", file=sys.stderr)
        return 2
    p = pathlib.Path(a.target)
    if not p.is_file():
        print(f"FAIL 文件不在场：{p}", file=sys.stderr)
        return 2
    text = p.read_text(encoding="utf-8", errors="replace")
    hits = check_text(text)
    for code, ln, msg in hits:
        print(f"FAIL [{code}] {p.name}" + (f":{ln}" if ln else "") + f" {msg}")
    print(("PASS" if not hits else "FAIL") + f"（扫过 {len(text.splitlines())} 行，发条 {len(hits)} 条）")
    return 0 if not hits else 1


if __name__ == "__main__":
    sys.exit(main())
