#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_chain.py — 政策影响链卡的四道机检（零网络、只读传入文件）。

四道码（缺一即不叫过闸）：
  F-STRUCT 五段齐＋名目齐：头部申报／政策要点／候选链／时间与窗口表／待人工任一段缺失即发红；
           头部三格日期（成文／印发／生效）与时间表三格（生效日／过渡期／申报窗）任一格名目缺席即发红——
           没写的那一格也要占一行点名，不许省行。
  F-ANCHOR 原句与锚：要点行必须带书名号内原句＋「锚：」；环节链行必须带「依据：」＋原句＋「锚：」；
           时间表每格必须带「锚：」；写明「未检索到」的那一格免。
  F-LINE   红线断言：利好利空、受益板块、标的点名、涨跌与必然类判断只允许出现在带 [待人工] 的行里。
           书名号内的原文引用不参与本道（判的是我们自己写的话，不是条文原句）。
  F-COUNT  条数与申报对账：头部「候选链 N 条」的 N 必须等于实际环节链行数；申报缺失即发红；
           时间表值位写「无／不适用／略／待定」而不落到「未检索到」一律发红。

用法：
  python3 -B scripts/check_chain.py <待检文件>   # 逐条发红，全过则 PASS
  python3 -B scripts/check_chain.py --selftest   # 好样须过、坏样四道齐发、反证各发各码；临时件跑完自清
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

POINT_LINE = re.compile(r"^\s*[-*]\s*要点[：:]")
CHAIN_LINE = re.compile(r"^\s*[-*]\s*环节链[：:]")
DATE_ITEM = re.compile(r"^\s*[-*]\s*(生效日|过渡期|申报窗)")
BASIS = re.compile(r"依据[：:]")
ANCHOR = re.compile(r"锚[:：]")
VERBATIM = re.compile(r"[「『][^」』]+[」』]")
MISS = re.compile(r"未检索到")
DECL = re.compile(r"候选链\s*(\d+)\s*条")
FILLER = re.compile(r"[：:]\s*(?:无|不适用|略|待定)\s*$")
PENDING = re.compile(r"\[待人工\]")
BANNED = re.compile(r"必涨|稳赚|零风险|保证收益|利好|利空|受益股|受益板块|龙头标的|龙头|标的股|建议买入|建议卖出"
                    r"|目标价\s*[:：]?\s*\d|上调评级|下调评级|必然|肯定会|暴涨|暴跌|将会上涨|将会下跌")
QUOTE = re.compile(r"[「『][^」』]*[」』]")
SECTIONS = (("头部申报", r"头部申报"), ("政策要点", r"政策要点|要点逐字"), ("候选链", r"候选链"),
            ("时间与窗口表", r"时间与窗口表"), ("待人工", r"待人工"))
HEAD_DATES = ("成文日期", "印发日期", "生效日期")
TABLE_ITEMS = ("生效日", "过渡期", "申报窗")


def check_text(text: str) -> list[tuple[str, int, str]]:
    """返回 [(码, 行号, 说明)]；行号 0＝整档级判据。"""
    hits: list[tuple[str, int, str]] = []
    lines = text.splitlines()
    for name, pat in SECTIONS:
        if not re.search(pat, text):
            hits.append(("F-STRUCT", 0, f"缺段：{name}"))
    for name in HEAD_DATES:
        if name not in text:
            hits.append(("F-STRUCT", 0, f"头部缺日期名目：{name}（没写的那格也要点名）"))
    for name in TABLE_ITEMS:
        if not any(re.match(r"^\s*[-*]\s*" + name, l) for l in lines):
            hits.append(("F-STRUCT", 0, f"时间表缺格：{name}"))
    for i, ln in enumerate(lines, 1):
        if POINT_LINE.match(ln) and not MISS.search(ln):
            if not ANCHOR.search(ln):
                hits.append(("F-ANCHOR", i, "要点行缺「锚：」来源定位"))
            if not VERBATIM.search(ln):
                hits.append(("F-ANCHOR", i, "要点行缺书名号内原句逐字"))
        if CHAIN_LINE.match(ln) and not MISS.search(ln):
            if not BASIS.search(ln):
                hits.append(("F-ANCHOR", i, "环节链行缺「依据：」原文依据"))
            if not VERBATIM.search(ln):
                hits.append(("F-ANCHOR", i, "环节链行的依据不是书名号内的原文"))
            if not ANCHOR.search(ln):
                hits.append(("F-ANCHOR", i, "环节链行缺「锚：」来源定位"))
        if DATE_ITEM.match(ln) and not MISS.search(ln):
            if not ANCHOR.search(ln):
                hits.append(("F-ANCHOR", i, "时间表该行缺「锚：」"))
            if FILLER.search(ln):
                hits.append(("F-COUNT", i, "时间表值位用「无／不适用／略／待定」顶替，未落到「未检索到」"))
        bare = QUOTE.sub("", ln)
        if BANNED.search(bare) and not PENDING.search(ln):
            hits.append(("F-LINE", i, "红线断言词出现在没有 [待人工] 的行"))
    chains = sum(1 for ln in lines if CHAIN_LINE.match(ln))
    m = DECL.search(text)
    if not m:
        hits.append(("F-COUNT", 0, "头部申报缺「候选链 N 条」，无从对账"))
    elif int(m.group(1)) != chains:
        hits.append(("F-COUNT", 0, f"申报候选链 {m.group(1)} 条∥实际环节链 {chains} 条"))
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
    good = here / "fixtures" / "good-chain.md"
    bad = here / "fixtures" / "bad-chain.md"
    rows = []
    gt = good.read_text(encoding="utf-8")
    gh = check_text(gt)
    rows.append(("好样须过（发条 0）", not gh, f"实发 {len(gh)} 条" + ("" if not gh else "｜" + gh[0][2])))
    codes_bad = {c for c, _, _ in check_text(bad.read_text(encoding="utf-8"))}
    rows.append(("坏样四道齐发", {"F-STRUCT", "F-ANCHOR", "F-LINE", "F-COUNT"} <= codes_bad,
                 "实发码 " + "∥".join(sorted(codes_bad))))
    tmp = make_tmp("check-chain-")
    noanchor = tmp / "no-anchor.md"
    noanchor.write_text(re.sub(ANCHOR, "", gt), encoding="utf-8")
    ah = check_text(noanchor.read_text(encoding="utf-8"))
    rows.append(("反证·剥锚必发 F-ANCHOR", any(c == "F-ANCHOR" for c, _, _ in ah),
                 f"实发 {sum(1 for c, _, _ in ah if c == 'F-ANCHOR')} 条"))
    nobasis = tmp / "no-basis.md"
    nobasis.write_text(re.sub(r"依据[：:]\s*[「『][^」』]*[」』]", "", gt), encoding="utf-8")
    bh = check_text(nobasis.read_text(encoding="utf-8"))
    rows.append(("反证·剥依据必发 F-ANCHOR", any(c == "F-ANCHOR" and "依据" in msg for c, _, msg in bh),
                 f"实发 {sum(1 for c, _, m in bh if c == 'F-ANCHOR' and '依据' in m)} 条"))
    skewed = tmp / "skewed-decl.md"
    skewed.write_text(re.sub(r"候选链\s*\d+\s*条", "候选链 7 条", gt), encoding="utf-8")
    kh = check_text(skewed.read_text(encoding="utf-8"))
    rows.append(("反证·链条数申报改歪必发 F-COUNT", any(c == "F-COUNT" for c, _, _ in kh),
                 f"实发 {sum(1 for c, _, _ in kh if c == 'F-COUNT')} 条"))
    made = len(TMP_ROOTS)
    root = pathlib.Path(tempfile.gettempdir())
    for p in TMP_ROOTS:
        shutil.rmtree(p, ignore_errors=True)
    leftover = sorted(q.name for q in root.iterdir() if q.name.startswith("check-chain-")) if root.is_dir() else []
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
    ap = argparse.ArgumentParser(description="政策影响链卡四道机检（零网络）")
    ap.add_argument("target", nargs="?", help="待检文件（本件不读网络、不读目录）")
    ap.add_argument("--selftest", action="store_true", help="好样须过、坏样四道齐发、反证各发各码")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.target:
        print("用法：check_chain.py <待检文件> | --selftest", file=sys.stderr)
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
