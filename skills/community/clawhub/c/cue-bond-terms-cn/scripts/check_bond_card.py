#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_bond_card.py — 债券条款卡的机检（零网络、只读本包外传入的文件）。

六道码（缺一即不叫过闸）：
  B-STRUCT 五段齐：头部申报／八项逐字速读／口径对照／缺数清单／待人工，任一节缺失即发；
           八项名目另须在「逐字速读」段内**行级在场**——每枚名目一行以「- 名目：」起头，只在散文里提到不算占行；
  B-QUOTE  每项原句与锚：项行的书名号（「」『』«»）内原句不得为空或只剩单字；「锚：」标签在而锚值为空同样发；
  B-LINE   红线断言：债项估值／估值结果／收益率测算／建议买入／建议卖出／评级上调／评级下调／目标价／必涨／稳赚／
           零风险／保证收益／代客认购／包销承诺，只允许出现在带 [待人工] 的行里，否则发；
  B-COUNT  齐缺申报恰一枚：头部「共八项·缺 N 项」只准出现一处（两处并存即发），且 N 必须等于速读段里
           「未检索到」的项行数；把「未检索到」写成「无该项／没有此项」一律发；
  B-VALUE  规模与利率项不许用推定语顶替：发行规模与期限、票面利率与付息方式两项，凡未写「未检索到」的，
           行内必须出现带单位的数字原值（亿元／万元／年／%）；「待定／询价／另行公告／以发行公告为准／
           视市场情况」这类推定语不算值，出现即发；
  B-RATING 评级符号不许裸奔：AAA／AA+／AA-／AA／A+／A- 这类评级符号出现在任何非 [待人工] 行时，
           该行必须同句带「锚：」；评级符号与出处分离＝读者无从核，发。

用法：
  python3 -B scripts/check_bond_card.py <待检文件>      # 逐条发红，全过则 PASS
  python3 -B scripts/check_bond_card.py --selftest      # 好样须过、坏样六道齐发、六形钉阈各钉一档、临时件自清
  python3 -B scripts/check_bond_card.py --help
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

ITEMS = ("发行人与债项名称", "发行规模与期限", "票面利率与付息方式", "发行价格与计息方式",
         "担保与增信安排", "赎回与回售条款", "信息披露与受托管理", "违约与交叉违约")
VALUE_ITEMS = ("发行规模与期限", "票面利率与付息方式")
ITEM = re.compile(r"^\s*[-*]\s*(" + "|".join(map(re.escape, ITEMS)) + r")[：:]")
TITLE = re.compile(r"[「『«][^」』»]+[」』»]")
ANCHOR = re.compile(r"锚[:：]")
ANCHOR_VAL = re.compile(r"锚[:：]\s*(\S.*)$")
BANNED = re.compile(r"债项估值|估值结果|收益率测算|建议买入|建议卖出|评级上调|评级下调|目标价|必涨|稳赚|零风险|保证收益|代客认购|包销承诺")
PENDING = re.compile(r"\[待人工\]")
DECL = re.compile(r"共\s*(?:八|8)\s*项\s*[·：:|｜、]\s*缺\s*(\d+)\s*项")
EMPTY_LIE = re.compile(r"(?:^|[\s：:])无(?:该项|此项)|没有(?:该项|此项)")
NUM_VAL = re.compile(r"\d[\d,\.]*\s*(?:亿元|万元|元|年|%|个月|月|日)")
VALUE_EVADE = re.compile(r"待定|询价|另行公告|以发行公告为准|视市场情况")
RATING = re.compile(r"(?<![A-Za-z0-9])(?:AAA|AA\+|AA-|AA|A\+|A-)(?![A-Za-z0-9])")
CORE_STRIP = re.compile(r"[\s\u3000「」『』«»“”（）()《》【】，,。.；;：:、！!？~\-—_·/％%*#]+")
SECTIONS = (("头部申报", r"头部申报"), ("八项逐字速读", r"逐字速读|八项速读"),
            ("口径对照", r"口径对照"), ("缺数清单", r"缺数清单"), ("待人工", r"待人工"))
SPEED_HEAD = re.compile(r"^#{1,4}.*(?:逐字速读|八项速读)")
ANY_HEAD = re.compile(r"^#{1,4}\s")


def core_len(s: str) -> int:
    return len(CORE_STRIP.sub("", s))


def speed_zone(lines: list[str]) -> range:
    start = None
    for i, ln in enumerate(lines):
        if SPEED_HEAD.match(ln):
            start = i + 1
            break
    if start is None:
        return range(0, len(lines))
    end = len(lines)
    for j in range(start, len(lines)):
        if ANY_HEAD.match(lines[j]):
            end = j
            break
    return range(start, end)


def check_text(text: str) -> list[tuple[str, int, str]]:
    """返回 [(码, 行号, 说明)]；行号 0＝整档级判据。"""
    hits: list[tuple[str, int, str]] = []
    lines = text.splitlines()
    for name, pat in SECTIONS:
        if not re.search(pat, text):
            hits.append(("B-STRUCT", 0, f"缺段：{name}"))
    zone = speed_zone(lines)
    seen = {}
    for i in zone:
        ln = lines[i]
        m = ITEM.match(ln)
        if not m:
            continue
        name = m.group(1)
        seen.setdefault(name, i + 1)
        if "未检索到" not in ln:
            if not TITLE.search(ln):
                hits.append(("B-QUOTE", i + 1, f"缺项原句：{name} 那一行没有书名号内的原文"))
            elif any(core_len(q) <= 1 for q in re.findall(r"[「『«]([^」』»]*)[」』»]", ln)):
                hits.append(("B-QUOTE", i + 1, f"原句占位：{name} 那一行的书名号内为空或只剩单字"))
            mv = ANCHOR_VAL.search(ln)
            if not mv or core_len(mv.group(1)) == 0:
                hits.append(("B-QUOTE", i + 1, f"锚值为空：{name} 那一行的「锚：」后面没有来源定位"))
            if name in VALUE_ITEMS:
                if not NUM_VAL.search(ln):
                    hits.append(("B-VALUE", i + 1, f"规模或利率项无数字原值：{name} 那一行既没写「未检索到」也没有带单位的数字"))
                elif VALUE_EVADE.search(ln):
                    hits.append(("B-VALUE", i + 1, f"规模或利率项以推定语顶替：{name} 那一行出现「待定／询价／另行公告／以发行公告为准／视市场情况」，推定语不算值"))
    for name in ITEMS:
        if name not in seen:
            hits.append(("B-STRUCT", 0, f"缺项行：{name} 在逐字速读段里没有以「- 名目：」起头的行"))
    pending_items = sum(1 for i in zone if ITEM.match(lines[i]) and "未检索到" in lines[i])
    decls = DECL.findall(text)
    if len(decls) > 1:
        hits.append(("B-COUNT", 0, f"齐缺申报出现 {len(decls)} 处：只准一枚，两处并存即口径不唯一"))
    elif len(decls) == 1 and int(decls[0]) != pending_items:
        hits.append(("B-COUNT", 0, f"齐缺申报与清单不对账：申报缺 {decls[0]} 项∥速读段实有 {pending_items} 行「未检索到」"))
    elif not decls:
        hits.append(("B-COUNT", 0, "头部缺「共八项·缺 N 项」申报，无从对账"))
    for i, ln in enumerate(lines, 1):
        if BANNED.search(ln) and not PENDING.search(ln):
            hits.append(("B-LINE", i, "红线断言词出现在没有 [待人工] 的行"))
        if EMPTY_LIE.search(ln):
            hits.append(("B-COUNT", i, "把「未检索到」写成「无／没有」"))
        if RATING.search(ln) and not PENDING.search(ln) and not ANCHOR.search(ln):
            hits.append(("B-RATING", i, "评级符号裸奔：这一行出现评级符号却没有同句「锚：」定位（也没有落在 [待人工] 行）"))
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
    good = here / "fixtures" / "good-bond-card.md"
    bad = here / "fixtures" / "bad-bond-card.md"
    rows = []
    gt = good.read_text(encoding="utf-8")
    gh = check_text(gt)
    rows.append(("好样须过（发条 0）", not gh, f"实发 {len(gh)} 条"))
    bt = bad.read_text(encoding="utf-8")
    bh = check_text(bt)
    codes = {c for c, _, _ in bh}
    rows.append(("坏样六道齐发", {"B-STRUCT", "B-QUOTE", "B-LINE", "B-COUNT", "B-VALUE", "B-RATING"} <= codes,
                 "实发码 " + "∥".join(sorted(codes))))
    tmp = make_tmp("check-bond-")
    stripped = tmp / "no-anchor.md"
    stripped.write_text(re.sub(r"锚[:：][^\n]*", "锚：", gt), encoding="utf-8")
    sh = check_text(stripped.read_text(encoding="utf-8"))
    rows.append(("反证·剥锚必发 B-QUOTE", any(c == "B-QUOTE" for c, _, _ in sh), f"实发 {len(sh)} 条"))
    nproof = 1
    pin = make_tmp("check-bond-pin-")
    tiers = (
        ("钉阈·名目只剩散文必发 B-STRUCT",
         gt.replace("- 违约与交叉违约：", "违约与交叉违约条款在原文另有说明，", 1),
         "缺项行：违约与交叉违约"),
        ("钉阈·书名号内单字必发 B-QUOTE",
         gt.replace("「本期债券发行规模为人民币 10 亿元，期限 5 年」", "「十」", 1),
         "原句占位"),
        ("钉阈·齐缺申报改数必发 B-COUNT",
         gt.replace("共八项·缺 1 项", "共八项·缺 0 项", 1),
         "齐缺申报与清单不对账"),
        ("钉阈·利率项写成待定必发 B-VALUE",
         gt.replace("票面利率与付息方式：", "票面利率与付息方式：待定 ", 1).replace("「票面利率 3.20%，按年付息」", "«利率»", 1),
         "规模或利率项无数字原值"),
        ("钉阈·评级符号裸奔必发 B-RATING",
         gt.replace("｜附件腿：未发起", "｜附件腿：未发起（主体评级 AAA）", 1),
         "评级符号裸奔"),
        ("钉阈·红线词落在非待人工行必发 B-LINE",
         gt.replace("｜附件腿：未发起", "｜附件腿：未发起｜建议买入", 1),
         "红线断言词出现在没有 [待人工] 的行"),
    )
    for n, (name, text, needle) in enumerate(tiers, 1):
        nproof += 1
        p = pin / f"pin-{n}.md"
        p.write_text(text, encoding="utf-8")
        ph = check_text(p.read_text(encoding="utf-8"))
        fired = [m for c, _, m in ph if needle in m]
        injected = text != gt
        rows.append((name, injected and bool(fired),
                     f"注入{'生效' if injected else '作废'}·实发 {len(ph)} 条·命中句 "
                     + ("∥".join(fired) if fired else "无")))
    made = [p.name for p in TMP_ROOTS]
    root = pathlib.Path(tempfile.gettempdir())
    for p in TMP_ROOTS:
        shutil.rmtree(p, ignore_errors=True)
    leftover = sorted(q.name for q in root.iterdir() if q.name.startswith("check-bond-")) if root.is_dir() else []
    rows.append(("临时根自清（跑后不增）", not leftover,
                 f"本次建 {len(made)} 枚·跑后残留 {len(leftover)} 枚"))
    bad_rows = [r for r in rows if not r[1]]
    for name, ok, detail in rows:
        print(f"  {'ok  ' if ok else 'FAIL'} {name}｜{detail}")
    print(f"selftest: {'ALL GREEN' if not bad_rows else 'FAIL'}（好样 1 枚·坏样六道·反例 {nproof} 枚·临时根 {len(TMP_ROOTS)} 枚自清）")
    return 0 if not bad_rows else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="债券条款卡六道机检（零网络）")
    ap.add_argument("target", nargs="?", help="待检文件（本件不读网络、不读目录）")
    ap.add_argument("--selftest", action="store_true", help="好样须过、坏样六道齐发、六形钉阈各钉一档、临时件自清")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.target:
        print("用法：check_bond_card.py <待检文件> | --selftest", file=sys.stderr)
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