#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""collect_review.py — 离线采集器：读一枚本地靶件的盘面，出一份「每条都能回到一处原文」的体检报告骨架。

用法：
    python3 -B scripts/collect_review.py --target <靶件目录> [--out 报告.md] [--asof YYYY-MM-DD]
    python3 -B scripts/collect_review.py --help

它做什么：
    只读靶件的 SKILL.md／README*.md／LICENSE*，按行登记盘上现值，产出五节骨架——
    声明层（frontmatter 键的在位与缺位）、前置层（requires 那一层声明了什么）、
    面文承诺（面上写下的承诺句原样带行号摘出）、许可与出处（license 值与许可文本是否同盘在场）、
    样例真跑（**留一个待填位**：跑没跑由你决定，写「跑过」就必须同句给 cmd=… rc=整数）。
    第五节的每一行都是 `文件:行号 ｜检索日 YYYY-MM-DD`，第二节的每条发现都挂其中一个 [S#]。
它不做什么：
    不执行靶件的任何代码（连它自己的 runner 都不跑——那是决定，不是默认）；不发任何请求；不替你下装／不装的判断。
    远端面文与本地是否一致这一层，离线永远查不到：骨架把它固定写进第四节，并同句写明代价。

出口形制：
    骨架自带四件头部自标；样例真跑那一行按设计发 E-VERIFY——那是「还没跑就别写」的占位，不是待补的疏漏。
    跑完机检期望红在这一行：python3 -B scripts/check_review.py <骨架.md>

退码：0 骨架落成；1 靶件目录里没有可读的面文（没有出处不出骨架）；3 取值域故障（目录读不到、--asof 不是 YYYY-MM-DD）。
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

PKG_KEYS = ("name", "slug", "displayName", "version", "summary", "description", "license",
            "inputs", "produces", "consumes", "legs", "tags")
PROMISE_RE = re.compile(r"无需|不报错|不装|也能跑|可选|自动|开箱即用|一定能|不会|必过|不受影响|不代付")
COST_RE = re.compile(r"代价|缺|看不到|不成立|降为|残|没有出处|证据密度|不上")


def key_line(fm_lines, key):
    for no, ln in fm_lines:
        m = re.match(r"^%s:\s*(.*)$" % re.escape(key), ln)
        if m:
            return no, m.group(1).strip()
    return None, None


def nested_line(fm_lines, key):
    for no, ln in fm_lines:
        m = re.match(r"^\s+%s:\s*(.*)$" % re.escape(key), ln)
        if m:
            return no, m.group(1).strip()
    return None, None


def list_items(fm_lines, key):
    """取顶层键下面那一段列表项（缩进两格的 "- 名字"），遇到下一个顶层键即停。"""
    start = next((pos for pos, (no, ln) in enumerate(fm_lines) if re.match(r"^%s:\s*$" % re.escape(key), ln)), None)
    if start is None:
        return []
    items = []
    for no, ln in fm_lines[start + 1:]:
        if ln and not ln.startswith(" "):
            break
        m = re.match(r"\s+-\s+([A-Za-z0-9_.-]+)", ln)
        if m:
            items.append(m.group(1))
    return items


def canonical_names(root: Path):
    """词表在册名——读得到才判「在册／不在册」，读不到就明写无从对照，不猜一套名字。"""
    f = root / "scripts" / "artifact-types.yaml"
    if not f.is_file():
        return None, None
    lines = f.read_text(encoding="utf-8", errors="replace").split("\n")
    start = next((i for i, l in enumerate(lines) if l.startswith("canonical:")), None)
    if start is None:
        return None, None
    names = set()
    for ln in lines[start + 1:]:
        if ln and not ln.startswith("  "):
            break
        m = re.match(r"\s+-\s+([A-Za-z0-9_-]+)", ln)
        if m:
            names.add(m.group(1))
    return names, "scripts/artifact-types.yaml:%d" % (start + 1)


def main():
    ap = argparse.ArgumentParser(prog="collect_review.py", description=__doc__, add_help=False)
    ap.add_argument("target_pos", nargs="?", metavar="TARGET", help="靶件目录（位置参数写法）")
    ap.add_argument("--target", dest="target_kw", metavar="DIR", help="靶件目录（开关写法，二选一）")
    ap.add_argument("--out", help="骨架落盘位置；不给就走标准输出")
    ap.add_argument("--asof", help="检索日 YYYY-MM-DD（缺省＝本次运行的当天）")
    ap.add_argument("-h", "--help", action="store_true")
    a = ap.parse_args()
    if a.help or not (a.target_pos or a.target_kw):
        print(__doc__)
        return 0 if a.help else 2
    if bool(a.target_pos) == bool(a.target_kw):
        print("用法错：位置参数与开关写法二选一，只给一个（两个都给或都不给都无从判哪个是被检件）")
        return 2
    tgt = Path(a.target_pos or a.target_kw)
    if not tgt.is_dir():
        print("取值域故障：%s 不是可读目录（读不到不等于「零违例」，也不当「靶件干净」）" % tgt)
        return 3
    today = dt.date.today().isoformat()
    if a.asof:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", a.asof):
            print("取值域故障：--asof 要写成 YYYY-MM-DD，现读=%r（体检的时效凭检索日，日期形制不能凑）" % a.asof)
            return 3
        asof = a.asof
    else:
        asof = today

    faces = sorted([p for p in tgt.iterdir() if p.is_file() and p.name in
                   ("SKILL.md", "README.md", "README.zh-CN.md", "README.en.md", "SKILL.en.md")])
    if not faces:
        print("没有出处不出骨架：%s 里读不到 SKILL.md／README*.md 任一枚（退 1，不是退 3——目录是在的，只是没有面可检）" % tgt)
        return 1
    texts = {}
    for p in faces:
        try:
            texts[p.name] = p.read_text(encoding="utf-8", errors="replace").split("\n")
        except OSError as e:
            print("取值域故障：读不到 %s（%s）" % (p.name, e.strerror or "原因未取到"))
            return 3

    skill = texts.get("SKILL.md")
    fm_lines = []
    if skill:
        try:
            end = next(i for i, ln in enumerate(skill) if i > 0 and ln.strip() == "---")
        except StopIteration:
            end = None
        if end:
            fm_lines = [(i + 1, skill[i]) for i in range(1, end)]

    rel = tgt.as_posix().rstrip("/")
    rows = [("S%d" % (i + 1), name, "%s/%s:1" % (rel, name)) for i, name in enumerate(sorted(texts))]
    anchor_of = {name: sid for sid, name, _ in rows}
    sid = anchor_of.get("SKILL.md") or rows[0][0]
    vocab, vocab_loc = canonical_names(Path(__file__).resolve().parents[2])

    findings, gaps = [], []
    if not skill:
        findings.append("- 声明层：靶件目录里没有 SKILL.md 这枚面——frontmatter 整块不在盘上，现读面＝%s [%s]"
                        % ("、".join(sorted(texts)), sid))
        gaps.append("- 未取到：前置层——没有 SKILL.md 就没有 requires 那一层可比，"
                    "缺的是「声明的前置与正文要用的东西对不对得上」这一层证据（不是排版）")
        gaps.append("- 未取到：许可与出处——license 键与 LICENSE 文本都读自 SKILL.md 与包内文件，"
                    "面不在盘上时无从登记（缺的是许可声明的出处，不是本件的判定力）")
    else:
        present, missing = [], []
        for k in PKG_KEYS:
            no, val = key_line(fm_lines, k)
            if no:
                present.append("%s＝%s（SKILL.md:%d）" % (k, (val or "（值为空行）")[:48], no))
            else:
                missing.append(k)
        if present:
            findings.append("- 声明层：键在位 %d／%d 枚，逐枚带行号——%s [%s]"
                            % (len(present), len(PKG_KEYS), "；".join(present[:4]), sid))
        findings.append("- 声明层：缺位键＝%s；按本仓口径 consumes 决定图上有没有入边、produces 决定有没有下一件来取 [%s]"
                        % ("、".join(missing) if missing else "无", sid))
        if vocab:
            listed_p = list_items(fm_lines, "produces")
            listed_c = list_items(fm_lines, "consumes")
            off = [x for x in listed_p + listed_c if x not in vocab]
            findings.append("- 声明层：produces 段现值 %s｜consumes 段现值 %s｜词表对照＝%s（对照来路 %s） [%s]"
                            % ("/".join(listed_p) or "空", "/".join(listed_c) or "空",
                               "全部在册" if not off else "表外名：%s" % "、".join(off),
                               vocab_loc, sid))
        else:
            gaps.append("- 未取到：produces／consumes 是否在册——词表 scripts/artifact-types.yaml 相对本件不在场，"
                        "对照这一层缺位（缺的是「这个名字会不会成为图上的一条边」的判断依据，不是排版）")

    if skill:
        bins_no, bins_val = nested_line(fm_lines, "bins")
        env_no, env_val = nested_line(fm_lines, "envVars")
        if bins_no or env_no:
            findings.append("- 前置层：requires 那一层现读 bins＝%s（SKILL.md:%s）｜envVars 声明位＝%s [%s]"
                            % (bins_val or "未见", bins_no or "—",
                               "在场（SKILL.md:%d）" % env_no if env_no else "未见", sid))
        else:
            findings.append("- 前置层：frontmatter 没有 metadata.openclaw.requires 那一层"
                            "——正文要用的东西在声明层无从对照 [%s]" % sid)

    prom = []
    for name, lines in texts.items():
        for i, ln in enumerate(lines, 1):
            if name == "SKILL.md" and fm_lines and i <= fm_lines[-1][0]:
                continue
            if PROMISE_RE.search(ln):
                prom.append((name, i, ln.strip()[:70], bool(COST_RE.search(ln))))
    if prom:
        for name, i, s, has_cost in prom[:4]:
            findings.append("- 面文承诺：%s/%s:%d 摘原文「%s」——同句%s [%s]"
                            % (rel, name, i, s, "带代价" if has_cost else "未写代价（这一条要回面文补）",
                               anchor_of.get(name) or sid))
    else:
        gaps.append("- 未取到：面文承诺——靶件各面里没有承诺形（无需／不报错／可选／自动 一类）的句子可摘，"
                    "摘不出原句就没有可核对的承诺（缺的是被核对的那句话，不是本件的判定力）")

    if skill:
        lic_no, lic_val = key_line(fm_lines, "license")
        lic_files = [p.name for p in tgt.iterdir() if p.is_file() and p.name.upper().startswith("LICENSE")]
        src_no, src_val = key_line(fm_lines, "homepage")
        findings.append("- 许可与出处：license 现读＝%s（SKILL.md:%s）｜包内许可文本文件＝%s｜面内仓库或作者出处行＝%s [%s]"
                        % (lic_val or "未见", lic_no or "—", "、".join(lic_files) if lic_files else "不在场",
                           src_val[:40] if src_val else "未见", sid))

    runner = (tgt / "scripts" / "fixtures" / "run_fixtures.sh")
    findings.append("- 样例真跑：（待填：跑不跑是你的决定；跑过就把那条命令与它这次的退码同句写成 cmd=… rc=整数，"
                    "没跑就删掉这行、改到第四节点名）｜靶件 runner 在场＝%s [%s]"
                    % ("是（%s/scripts/fixtures/run_fixtures.sh）" % rel if runner.is_file() else "否", sid))

    gaps.insert(0, "- 未取到：远端面文与本地这一份是否一致——本件离线只读盘上那几枚文件，"
                   "这一层整块缺位（缺的是「装之前实际会拿到什么」那一层证据，不是排版；要走解析通道才看得到远端那份正文）")

    out = ["# skill 体检报告（骨架）", "",
           "本页由 AI 整理，是 **AI 整理初稿**：逐条请回原文核对，不构成上架或安装建议，判断位 [待人工]。",
           "被检对象：%s｜检索日：%s｜读取方式：本地只读（未执行靶件任何代码、未发任何请求）" % (rel, asof), "",
           "## 1、被检对象", ""]
    name_no, name_val = key_line(fm_lines, "name")
    ver_no, ver_val = key_line(fm_lines, "version")
    decl = sum(1 for x in findings if x.startswith("- 声明层"))
    out += ["| 项 | 现值 | 出处 |", "|---|---|---|",
            "| 名字与版本 | %s／%s | %s |" % (name_val or tgt.name, ver_val or "未见",
                                            "SKILL.md:%s、:%s" % (name_no or "—", ver_no or "—") if skill
                                            else "（靶件目录里没有 SKILL.md 这枚面）"),
            "| 面 | %s | %s:1 |" % ("、".join(sorted(texts)), rel),
            "| 装不装 | 本骨架不表态——判断位 [待人工] | 本件红线 |", ""]
    out += ["## 2、逐条发现", ""] + findings + ["", "## 3、五个检查面", "",
            "| 面 | 这一面查什么 | 本次是否落到第二节 |", "|---|---|---|",
            "| 声明层 | frontmatter 键在位与缺位、名字是否在词表在册 | 见 §2 前 %d 条 |" % decl,
            "| 前置层 | requires 那一层声明了什么，与正文实际要用的东西对不对得上 | 见 §2 |",
            "| 面文承诺 | 面上写下的承诺句原样摘出，同句有没有代价 | 见 §2%s |" % ("、第四节" if not prom else ""),
            "| 样例真跑 | 是不是真跑通——写「跑通」就必须带那条命令与它这次的退码 | 待填位在场＝红在这一行是设计 |",
            "| 许可与出处 | license 值、许可文本文件、出处行三件是否同盘在场 | 见 §2 |", "",
            "## 4、未取到与口径", ""] + gaps + [
            "- 口径：行号按检索日那一刻的盘上现值写，靶件被改动后行号失效；跨源不一致时两条都留、不合并",
            "- 口径：本件不发请求、不代付费；解析通道的消耗以服务端返回为准，本件不代估也不代付", ""]
    out += ["## 5、来源", ""]
    for sid, name, loc in rows:
        out.append("- [%s] %s（%s ｜检索日 %s）" % (sid, name, loc, asof))
    if vocab_loc:
        out.append("- [S%d] 本仓工件词表 canonical 段（%s ｜检索日 %s）" % (len(rows) + 1, vocab_loc, asof))
    body = "\n".join(out) + "\n"

    if a.out:
        p = Path(a.out)
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print("取值域故障：--out 的父目录建不出来（%s）" % (e.strerror or "原因未取到"))
            return 3
        try:
            p.write_text(body, encoding="utf-8")
        except OSError as e:
            print("取值域故障：写不到 %s（%s）" % (p, e.strerror or "原因未取到"))
            return 3
        print("骨架落成：%s｜面=%d 枚｜发现=%d 条｜未取到点名=%d 条｜来源行=%d 条（计数由本件现算自报）"
              % (p, len(texts), len(findings), len(gaps), len(rows) + (1 if vocab_loc else 0)))
    else:
        sys.stdout.write(body)
        print("\n---- 以上为骨架全文；未落盘（没给 --out）。计数：面=%d｜发现=%d｜未取到=%d｜来源行=%d"
              % (len(texts), len(findings), len(gaps), len(rows) + (1 if vocab_loc else 0)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
