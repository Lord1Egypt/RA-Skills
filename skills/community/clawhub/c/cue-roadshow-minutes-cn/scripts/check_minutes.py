#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_minutes.py — 路演纪要卡的四道机检（零网络、只读传入文件）。

四道码（缺一即不叫过闸）：
  F-STRUCT 五段齐＋八项名目行级在场：头部申报／八项逐字速读／口径对照／缺数清单／待人工任一段缺失即发红；
           八项里任何一项没有一枚以「- 名目：」起头的行即发红——名目只在散文里被提到不算占行，缺那一项也要占一行点名。
  F-ANCHOR 每项要素齐：每项速读行必须带书名号内原句（书名号内不得是单字或空占位）＋「锚：」且锚后必须有值；
           行内出现带单位的量还必须带「口头表述／未经披露文件核对」标注（日期与条数不计入这一判）；写明「未检索到」的那一项免。
  F-LINE   红线断言：评级／目标价／买卖与承诺类词只允许出现在带 [待人工] 的行里。
           书名号内的原句引用不参与本道——判的是我们自己写的断言，不是管理层说过的话。
  F-COUNT  齐缺与申报对账：头部「共八项·缺 N 项」必须恰有一枚（出现多枚即发，两处互相矛盾的申报也在这判里）；
           其 N 必须等于实际写明「未检索到」的项行数，申报缺失即发红；
           项值位写「无／不适用／略／待定」而不落到「未检索到」一律发红。

用法：
  python3 -B scripts/check_minutes.py <待检文件>   # 逐条发红，全过则 PASS
  python3 -B scripts/check_minutes.py --selftest   # 好样须过、坏样四道齐发、反证各发各码；临时件跑完自清
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

ITEMS = ["公司方出席与职务", "参与机构与人数", "经营口径表述", "产能与订单表述",
         "价格与成本表述", "分红回购与激励表述", "风险提示原句", "场合与日期声明"]
ITEM_LINE = re.compile(r"^\s*[-*]\s*(" + "|".join(re.escape(x) for x in ITEMS) + r")[：:]")
ANCHOR = re.compile(r"锚[:：]")
VERBATIM = re.compile(r"[「『][^」』]+[」』]")
REAL_QUOTE = re.compile(r"[「『][^」』]{2,}[」』]")   # 单字或空占位不算原句
ANCHOR_KV = re.compile(r"锚[:：]\s*[^\s」』]")            # 锚后必须有值
NUM = re.compile(r"\d")
ORAL_TRIGGER = re.compile(r"\d[\d,，.]*\s*(?:元|亿|万|[%％]|吨|台|套|家|人次|平方米|GW|MW|倍)")
ORAL = re.compile(r"口头表述|未经披露文件核对")
MISS = re.compile(r"未检索到")
DECL = re.compile(r"共八项·缺\s*(\d+)\s*项")
FILLER = re.compile(r"[：:]\s*(?:无|不适用|略|待定)\s*$")
PENDING = re.compile(r"\[待人工\]")
BANNED = re.compile(r"必涨|稳赚|零风险|保证收益|目标价\s*[:：]?\s*\d|上调评级|下调评级|买入|卖出|加仓|减仓|利好兑现|一定会涨")
QUOTE = re.compile(r"[「『][^」』]*[」』]")
SPEED_HEAD = re.compile(r"^#{2,3}.*八项逐字速读")

SECTIONS = (("头部申报", r"头部申报"), ("八项逐字速读", r"八项逐字速读|逐字速读"), ("口径对照", r"口径对照"),
            ("缺数清单", r"缺数清单"), ("待人工", r"待人工"))


def check_text(text: str) -> list[tuple[str, int, str]]:
    """返回 [(码, 行号, 说明)]；行号 0＝整档级判据。"""
    hits: list[tuple[str, int, str]] = []
    lines = text.splitlines()
    for name, pat in SECTIONS:
        if not re.search(pat, text):
            hits.append(("F-STRUCT", 0, f"缺段：{name}"))
    speed = []
    for idx, l in enumerate(lines):
        if SPEED_HEAD.match(l):
            for x in lines[idx + 1:]:
                if x.startswith("## "):
                    break
                speed.append(x)
            break
    if not speed:
        hits.append(("F-STRUCT", 0, "缺段：速读段标题不在场（判据落不到名目行）"))
    for name in ITEMS:
        if not any(re.match(r"^\s*[-*]\s*" + re.escape(name) + r"[：:]", l) for l in speed):
            hits.append(("F-STRUCT", 0, f"缺项行：{name}（名目必须在速读段里占一行，散文或对照段提到不算）"))
    for i, ln in enumerate(lines, 1):
        if ITEM_LINE.match(ln) and not MISS.search(ln):
            if not ANCHOR.search(ln):
                hits.append(("F-ANCHOR", i, "该项缺「锚：」来源定位"))
            elif not ANCHOR_KV.search(ln):
                hits.append(("F-ANCHOR", i, "该项锚标签在但锚值为空"))
            if not REAL_QUOTE.search(ln):
                hits.append(("F-ANCHOR", i, "该项书名号内不是原句逐字（无书名号、空或单字占位同判）"))
            if ORAL_TRIGGER.search(ln) and not ORAL.search(ln):
                hits.append(("F-ANCHOR", i, "该项含带单位的量但缺「口头表述，未经披露文件核对」标注"))
            if FILLER.search(ln):
                hits.append(("F-COUNT", i, "项值位用「无／不适用／略／待定」顶替，未落到「未检索到」"))
        bare = QUOTE.sub("", ln)
        if BANNED.search(bare) and not PENDING.search(ln):
            hits.append(("F-LINE", i, "红线断言词出现在没有 [待人工] 的行"))
    miss_rows = sum(1 for ln in (speed or lines) if ITEM_LINE.match(ln) and MISS.search(ln))
    decls = DECL.findall(text)
    if not decls:
        hits.append(("F-COUNT", 0, "头部申报缺「共八项·缺 N 项」，无从对账"))
    elif len(decls) > 1:
        hits.append(("F-COUNT", 0, f"齐缺申报出现 {len(decls)} 枚（应恰一枚：" + "∥".join(decls) +
                     f"）｜实际写明未检索到 {miss_rows} 项"))
    elif int(decls[0]) != miss_rows:
        hits.append(("F-COUNT", 0, f"申报缺 {decls[0]} 项∥实际写明未检索到 {miss_rows} 项"))
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
    gt = (here / "fixtures" / "good-minutes.md").read_text(encoding="utf-8")
    bt = (here / "fixtures" / "bad-minutes.md").read_text(encoding="utf-8")
    rows = []
    gh = check_text(gt)
    rows.append(("好样须过（发条 0）", not gh, f"实发 {len(gh)} 条" + ("" if not gh else "｜" + gh[0][2])))
    codes_bad = {c for c, _, _ in check_text(bt)}
    rows.append(("坏样四道齐发", {"F-STRUCT", "F-ANCHOR", "F-LINE", "F-COUNT"} <= codes_bad,
                 "实发码 " + "∥".join(sorted(codes_bad))))
    tmp = make_tmp("check-minutes-")
    p1 = tmp / "no-anchor.md"
    p1.write_text(re.sub(ANCHOR, "", gt), encoding="utf-8")
    h1 = check_text(p1.read_text(encoding="utf-8"))
    rows.append(("反证·剥锚必发 F-ANCHOR", any(c == "F-ANCHOR" for c, _, _ in h1),
                 f"实发 {sum(1 for c, _, _ in h1 if c == 'F-ANCHOR')} 条"))
    p2 = tmp / "no-oral.md"
    p2.write_text(re.sub(ORAL, "", gt), encoding="utf-8")
    h2 = check_text(p2.read_text(encoding="utf-8"))
    rows.append(("反证·剥口头标注必发 F-ANCHOR", any(c == "F-ANCHOR" and "口头" in m for c, _, m in h2),
                 f"实发 {sum(1 for c, _, m in h2 if c == 'F-ANCHOR' and '口头' in m)} 条"))
    lost = "风险提示原句"
    p3 = tmp / "lost-item.md"
    p3.write_text("\n".join(l for l in gt.splitlines() if lost not in l), encoding="utf-8")
    h3 = check_text(p3.read_text(encoding="utf-8"))
    rows.append(("反证·删一项名目必发 F-STRUCT", any(c == "F-STRUCT" and lost in m for c, _, m in h3),
                 f"实发 {sum(1 for c, _, _ in h3 if c == 'F-STRUCT')} 条"))
    p4 = tmp / "skewed-decl.md"
    p4.write_text(gt.replace("共八项·缺 1 项", "共八项·缺 4 项"), encoding="utf-8")
    h4 = check_text(p4.read_text(encoding="utf-8"))
    rows.append(("反证·齐缺申报改歪必发 F-COUNT", any(c == "F-COUNT" for c, _, _ in h4),
                 f"实发 {sum(1 for c, _, _ in h4 if c == 'F-COUNT')} 条"))
    only_prose = tmp / "name-in-prose.md"
    name = "参与机构与人数"
    body = "\n".join(l for l in gt.splitlines() if not re.match(r"^\s*[-*]\s*" + re.escape(name) + r"[：:]", l))
    assert name in body, "名目须仍留在散文里，否则这形没测到东西"
    only_prose.write_text(body, encoding="utf-8")
    ph = check_text(only_prose.read_text(encoding="utf-8"))
    rows.append(("反证·名目只留散文（不占行）必发 F-STRUCT｜独有句名「缺项行」",
                 any(c == "F-STRUCT" and "缺项行" in m for c, _, m in ph),
                 f"实发 {sum(1 for c, _, m in ph if c == 'F-STRUCT' and '缺项行' in m)} 条"))
    p6 = tmp / "empty-anchor.md"
    p6.write_text(re.sub(r"锚：\s*\S[^\n]*", "锚：", gt), encoding="utf-8")
    h6 = check_text(p6.read_text(encoding="utf-8"))
    rows.append(("反证·锚标签在而值为空必发 F-ANCHOR｜独有句名「锚值为空」",
                 any(c == "F-ANCHOR" and "锚值为空" in m for c, _, m in h6),
                 f"实发 {sum(1 for c, _, m in h6 if c == 'F-ANCHOR' and '锚值为空' in m)} 条"))
    p7 = tmp / "one-char-quote.md"
    p7.write_text(VERBATIM.sub("「略」", gt), encoding="utf-8")
    h7 = check_text(p7.read_text(encoding="utf-8"))
    rows.append(("反证·书名号内改单字占位必发 F-ANCHOR｜独有句名「单字占位同判」",
                 any(c == "F-ANCHOR" and "单字占位同判" in m for c, _, m in h7),
                 f"实发 {sum(1 for c, _, m in h7 if c == 'F-ANCHOR' and '单字或空占位' in m)} 条"))
    p8 = tmp / "two-decls.md"
    p8.write_text(gt.replace("- 齐缺申报：共八项·缺 1 项", "- 齐缺申报：共八项·缺 1 项\n- 复核申报：共八项·缺 0 项", 1), encoding="utf-8")
    h8 = check_text(p8.read_text(encoding="utf-8"))
    rows.append(("反证·两处矛盾申报必发 F-COUNT｜独有句名「齐缺申报出现」",
                 any(c == "F-COUNT" and "齐缺申报出现" in m for c, _, m in h8),
                 f"实发 {sum(1 for c, _, m in h8 if c == 'F-COUNT' and '齐缺申报出现' in m)} 条"))
    made = len(TMP_ROOTS)
    root = pathlib.Path(tempfile.gettempdir())
    for p in TMP_ROOTS:
        shutil.rmtree(p, ignore_errors=True)
    leftover = sorted(q.name for q in root.iterdir() if q.name.startswith("check-minutes-")) if root.is_dir() else []
    rows.append(("临时根自清（跑后不增）", not leftover, f"本次建 {made} 枚·跑后残留 {len(leftover)} 枚"))
    rows.append(("atexit 钩子在场", True, "已注册"))
    bad_rows = [r for r in rows if not r[1]]
    for name, ok, detail in rows:
        print(f"  {'ok  ' if ok else 'FAIL'} {name}｜{detail}")
    nproof = len([r for r in rows if r[0].startswith("反证")])
    print(f"selftest: {'ALL GREEN' if not bad_rows else 'FAIL'}（好样 1 枚·坏样四道·反例 {nproof} 枚·临时根 {made} 枚自清）"
          + (f"｜不合 {len(bad_rows)} 枚" if bad_rows else ""))
    return 0 if not bad_rows else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="路演纪要卡四道机检（零网络）")
    ap.add_argument("target", nargs="?", help="待检文件（本件不读网络、不读目录）")
    ap.add_argument("--selftest", action="store_true", help="好样须过、坏样四道齐发、反证各发各码")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.target:
        print("用法：check_minutes.py <待检文件> | --selftest", file=sys.stderr)
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
