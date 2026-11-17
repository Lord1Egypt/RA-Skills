#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_digest.py — 公告速览产物的五道机检（零网络、只读本包外传入的文件）。

五道码（缺一即不叫过闸）：
  F-STRUCT 四段齐：头部申报／逐条要点／同类前后串／缺数与待人工，四段小标题任一段缺失即发红；
  F-ANCHOR 逐条双要素＋锚：每条要点行必须同带「[披露日]」＋书名号内的公告标题逐字＋「锚：」定位，缺任一项发红；
  F-LINE   红线断言：评级／目标价／涨跌与承诺类词只允许出现在带 [待人工] 的行里，否则发红；
  F-COUNT  计数与申报一致：头部写的「共 N 条」必须等于实际要点条数；把「未检索到」写成「无／没有」一律发红。
  FILLER   值位不许占位顶替：要点行的值位整体为空、剥掉标点与括注后只剩单字，或值位里任一处引号（«»、「」、『』、“”）内是空／单字／只剩标点，一律发红——
           没取到要写「未检索到」并进缺数清单（承诺在本面「是什么／不是什么」那张两列表的右栏），不留空、不写「略」。

用法：
  python3 -B scripts/check_digest.py <待检文件>      # 逐条发红，全过则 PASS
  python3 -B scripts/check_digest.py --selftest      # 好样须过、坏样五道齐发；五形钉阈档各钉一档；临时件跑完自清
  python3 -B scripts/check_digest.py --help
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
AT_EXIT_DONE = {"done": False}

ITEM = re.compile(r"^\s*[-*]\s*\[(\d{4}-\d{2}-\d{2}|\d{1,2}\s*月\s*\d{1,2}\s*日)\]")
TITLE = re.compile(r"[「『][^」』]+[」』]")
ANCHOR = re.compile(r"锚[:：]")
BANNED_WORDS = re.compile(r"必涨|稳赚|零风险|保证收益|目标价\s*[:：]?\s*\d|上调评级|下调评级|买入|卖出|加仓|减仓")
PENDING = re.compile(r"\[待人工\]")
COUNT = re.compile(r"共\s*(\d+)\s*条")
EMPTY_LIE = re.compile(r"(?:^|[\s：:])无公告|没有公告|无新增公告")
VALUE_SEG = re.compile(r"要点[：:]\s*(.*?)(?:\s*锚[:：]|$)")
HEAD_STRIP = re.compile(r"^\s*[-*]\s*\[[^\]]*\]\s*(?:[「『][^」』]*[」』])?\s*[—\-]*\s*")
QUOTE_SPAN = re.compile(r"[«「『“]([^»」』”]*)[»」』”]")
CORE_STRIP = re.compile(r"[\s\u3000「」『』«»“”（）()《》【】，,。.；;：:、！!？~\-—_·/％%*#]+")


def core_len(s: str) -> int:
    return len(CORE_STRIP.sub("", s))


SECTIONS = (("头部申报", r"头部申报|申报"), ("逐条要点", r"逐条要点|要点清单"),
            ("同类前后串", r"同类|前后串"), ("缺数与待人工", r"缺数|待人工"))


def check_text(text: str) -> list[tuple[str, int, str]]:
    """返回 [(码, 行号, 说明)]；行号 0＝整档级判据。"""
    hits: list[tuple[str, int, str]] = []
    lines = text.splitlines()
    for name, pat in SECTIONS:
        if not re.search(pat, text):
            hits.append(("F-STRUCT", 0, f"缺段：{name}"))
    items = 0
    for i, ln in enumerate(lines, 1):
        if ITEM.match(ln):
            items += 1
            if not TITLE.search(ln):
                hits.append(("F-ANCHOR", i, "要点行缺公告标题逐字（书名号内）"))
            if not ANCHOR.search(ln):
                hits.append(("F-ANCHOR", i, "要点行缺「锚：」来源定位"))
            if "未检索到" not in ln:
                mv = VALUE_SEG.search(ln)
                if mv:
                    seg = mv.group(1)
                else:
                    seg = HEAD_STRIP.sub("", re.split(r"锚[:：]", ln, 1)[0])
                if core_len(seg) <= 1:
                    hits.append(("FILLER", i, "值位占位：剥掉标点与括注后为空或只剩单字（没取到要写「未检索到」并进缺数清单）"))
                else:
                    for slot in QUOTE_SPAN.findall(seg):
                        if core_len(slot) <= 1:
                            hits.append(("FILLER", i, f"值位占位：引号内是空、只剩单字或只剩标点「{slot.strip() or '空'}」（关键数须逐字，不许以占位顶替）"))
                            break
        if BANNED_WORDS.search(ln) and not PENDING.search(ln):
            hits.append(("F-LINE", i, "红线断言词出现在没有 [待人工] 的行"))
    m = COUNT.search(text)
    if m and int(m.group(1)) != items:
        hits.append(("F-COUNT", 0, f"申报共 {m.group(1)} 条∥实际要点 {items} 条"))
    if not m and items:
        hits.append(("F-COUNT", 0, "头部申报缺「共 N 条」，无从对账"))
    for i, ln in enumerate(lines, 1):
        if EMPTY_LIE.search(ln):
            hits.append(("F-COUNT", i, "把「未检索到」写成「无／没有」"))
    return hits


def make_tmp(prefix: str) -> pathlib.Path:
    d = pathlib.Path(tempfile.mkdtemp(prefix=prefix, dir=str(pathlib.Path(tempfile.gettempdir()))))
    TMP_ROOTS.append(d)
    return d


@atexit.register
def _cleanup() -> None:
    AT_EXIT_DONE["done"] = True
    for d in TMP_ROOTS:
        shutil.rmtree(d, ignore_errors=True)


def selftest() -> int:
    here = pathlib.Path(__file__).resolve().parent
    good = here / "fixtures" / "good-digest.md"
    bad = here / "fixtures" / "bad-digest.md"
    rows = []
    gt = good.read_text(encoding="utf-8")
    gh = check_text(gt)
    rows.append(("好样须过（发条 0）", not gh, f"实发 {len(gh)} 条"))
    bt = bad.read_text(encoding="utf-8")
    bh = check_text(bt)
    codes = {c for c, _, _ in bh}
    rows.append(("坏样五道齐发", {"F-STRUCT", "F-ANCHOR", "F-LINE", "F-COUNT", "FILLER"} <= codes,
                 "实发码 " + "∥".join(sorted(codes))))
    # 反证：临时件——把好样剥掉锚行，必须只发 F-ANCHOR
    tmp = make_tmp("check-digest-")
    stripped = tmp / "no-anchor.md"
    stripped.write_text(re.sub(ANCHOR, "", gt), encoding="utf-8")
    sh = check_text(stripped.read_text(encoding="utf-8"))
    rows.append(("反证·剥锚必发 F-ANCHOR", any(c == "F-ANCHOR" for c, _, _ in sh), f"实发 {len(sh)} 条"))
    # 钉阈五形（FILLER 档各钉一档）：引号内空／引号内单字／引号内只剩标点／值位整体只剩单字／值位整体留空
    nproof = 1
    pin = make_tmp("check-digest-pin-")
    SRC9 = "要点：增持 «2,100 万股»，占总股本 0.52% 锚"
    SRC11 = "«人民币 1,850 万元»"
    tiers = (
        ("钉阈·引号槽内为空必发 FILLER", gt.replace(SRC11, "«»", 1),
         "引号内是空、只剩单字或只剩标点"),
        ("钉阈·引号槽内只剩单字必发 FILLER", gt.replace(SRC11, "«略»", 1),
         "引号内是空、只剩单字或只剩标点"),
        ("钉阈·引号槽内只剩标点必发 FILLER", gt.replace(SRC11, "«——»", 1),
         "引号内是空、只剩单字或只剩标点"),
        ("钉阈·值位整体只剩单字必发 FILLER", gt.replace(SRC9, "要点：«略» 锚", 1),
         "剥掉标点与括注后为空或只剩单字"),
        ("钉阈·值位整体留空必发 FILLER", gt.replace(SRC9, "要点： 锚", 1),
         "剥掉标点与括注后为空或只剩单字"),
    )
    for n, (name, text, needle) in enumerate(tiers, 1):
        nproof += 1
        p = pin / f"pin-{n}.md"
        p.write_text(text, encoding="utf-8")
        ph = check_text(p.read_text(encoding="utf-8"))
        fired = [m for c, _, m in ph if c == "FILLER"]
        injected = text != gt
        rows.append((name, injected and bool(fired) and needle in "".join(fired),
                     f"注入{'生效' if injected else '作废'}·实发 {len(ph)} 条·FILLER 句 "
                     + ("∥".join(fired) if fired else "无")))
    made = [p.name for p in TMP_ROOTS]
    root = pathlib.Path(tempfile.gettempdir())
    for p in TMP_ROOTS:
        shutil.rmtree(p, ignore_errors=True)
    leftover = sorted(q.name for q in root.iterdir() if q.name.startswith("check-digest-")) if root.is_dir() else []
    rows.append(("临时根自清（跑后不增）", not leftover,
                 f"本次建 {len(made)} 枚·跑后残留 {len(leftover)} 枚"))
    rows.append(("atexit 钩子在场", True, "已注册"))
    bad_rows = [r for r in rows if not r[1]]
    for name, ok, detail in rows:
        print(f"  {'ok  ' if ok else 'FAIL'} {name}｜{detail}")
    print(f"selftest: {'ALL GREEN' if not bad_rows else 'FAIL'}（好样 1 枚·坏样五道·反例 {nproof} 枚·临时根 {len(TMP_ROOTS)} 枚自清）")
    return 0 if not bad_rows else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="公告速览产物五道机检（零网络）")
    ap.add_argument("target", nargs="?", help="待检文件（本件不读网络、不读目录）")
    ap.add_argument("--selftest", action="store_true", help="好样须过、坏样五道齐发、五形钉阈各钉一档、临时件自清")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.target:
        print("用法：check_digest.py <待检文件> | --selftest", file=sys.stderr)
        return 2
    p = pathlib.Path(a.target)
    if not p.is_file():
        print(f"FAIL 文件不在场：{p}", file=sys.stderr)
        return 2
    hits = check_text(p.read_text(encoding="utf-8", errors="replace"))
    for code, ln, msg in hits:
        print(f"FAIL [{code}] {p.name}" + (f":{ln}" if ln else "") + f" {msg}")
    scanned = len(p.read_text(encoding='utf-8', errors='replace').splitlines())
    print(("PASS" if not hits else "FAIL") + f"（扫过 {scanned} 行，发条 {len(hits)} 条）")
    return 0 if not hits else 1


if __name__ == "__main__":
    sys.exit(main())
