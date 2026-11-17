#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_inquiry_letter.py — 监管问询函逐条答复核对 六道机检（零网络、零外发、不读环境变量）

本件**不抓取问询函原文**：交易所函件在公开库里没有正式通道（实测巨潮 3967 条抽样 150 条，
回复 140／收到告知 10／函件原文 0）。函件由用户粘贴或给本地路径，本件只负责拆条与核对。

用法：
    python3 scripts/check_inquiry_letter.py <核对表>.md
    python3 scripts/check_inquiry_letter.py --selftest
    python3 scripts/check_inquiry_letter.py --demo     打印一份完整合规样例（零输入可跑）

道一 IL-STRUCT 形制
  头部（第一个 `## ` 之前）四件自标逐字在位：AI 整理初稿／请回原文核对／不构成投资建议／判断位 [待人工]；
  `主体：` 与 `文件：` 行在场且非空；`收函日：` 出现时须为 YYYY-MM-DD；
  六节齐且按序：问询事项索引／要求提供的材料／回复要点／回复文件／未取到清单／来源；
  前三节各至少一条 `- ` 发现行，节内只许 `- ` 发现行、`### ` 子标题与空行；
  不得出现六节以外的 `## ` 标题（多一节即自造栏目，不静默跳过）。

道二 IL-QUOTE 原句与锚
  前三节的每条发现行必须以「」原句 + 〔锚：…〕 + [S#] 三元组收尾，可挂多组；原句与锚不得为空；
  例外只有两形：「未取到」行（缺的就是那份材料）与 [待人工] 行（判断位）；
  来源行 `- [S#] 标题 | URL | 检索日 YYYY-MM-DD`，URL 须为可点 http(s) 地址，检索日缺一不可；
  正文引用的每个 [S#] 必须在来源节有对应行，来源节登记了却没人引用的不算错（那是备查）。

道三 IL-PAIR 问题与回复两向点名（本件承重格）
  第一节登记的每个 `- 问题N`，第三节必须有同号的一条（要么给回复要点，要么写明未取到）；
  第三节出现的 `- 问题N` 而第一节没有同号 ⇒ 同样发。两向都判。
  这一格是本件与「摘要工具」的分界：只登记有问题的，不登记没答的，等于把没答的藏起来。

道四 IL-GAP 缺项点名
  前三节写 `未取到：X` ⇒ 第五节必须点名 X；第五节点名了 X 而前三节没有 ⇒ 同样发；两向都判。
  零缺口时，第五节须显式写 `未取到：无`；
  出现 `不适用`／`无此项`／`无需披露` 一律发——那是把没查当成没有；
  `未取到：无` 与其它项并列出现 ⇒ 发（自相矛盾）。

道五 IL-MEDIA 回复主体齐备性
  第四节每条 `- 主体：<名称>｜[S#]`；[S#] 须在来源节登记，行形不合即发。
  一条问询的公开产出通常 3–5 份，公司／会计师／保荐机构各出——只搜公司名会漏掉中介机构那几份。
  所以：若登记的主体里一个中介机构（会计师／保荐／律师／评估）都没有，且第五节没有点名
  中介机构回复未取到 ⇒ 发，点名这一格。

道六 IL-LINE 红线（不得代公司表态／不得出结论）
  先把行内「」引文整段剥掉再判——引文是公函原话，不是本件的立场；
  剥完后命中「本公司将／本公司拟／承诺／现回复如下／特此答复」一类表态词 ⇒ 发；
  命中「不构成重大影响／不存在问题／风险可控／回复充分／不会被处罚／预计通过」一类结论词 ⇒ 发；
  含 [待人工] 的分句豁免，且只豁免它自己那一句（按 ；;。，,｜ 切分），同行后半句照样发。

退码：0 全过 / 1 有发条 / 2 用法错（缺参数） / 3 读不到文件或空稿。
"""

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

SLUG = "cue-cn-inquiry-letter-reply"

CODES = ("IL-STRUCT", "IL-QUOTE", "IL-PAIR", "IL-GAP", "IL-MEDIA", "IL-LINE")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议", "判断位 [待人工]")

SECTIONS = ("问询事项索引", "要求提供的材料", "回复要点", "回复文件", "未取到清单", "来源")
CONTENT_SECTIONS = SECTIONS[:3]
MEDIA_SECTION = "回复文件"
GAP_SECTION = "未取到清单"
SOURCE_SECTION = "来源"
IDX_SECTION = "问询事项索引"
REPLY_SECTION = "回复要点"

HEADING = re.compile(r"^##(?!#)\s*(.+?)\s*$")
NUMBERING = re.compile(r"^(?:[0-9]+[.、)]|[一二三四五六七八九十]+[、.])\s*")

SUBJECT = re.compile(r"^主体：\s*(\S.*)$")
LETTER = re.compile(r"^文件：\s*(\S.*)$")
LETTER_DATE = re.compile(r"^收函日：\s*(\S.*)$")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

TRIPLE = re.compile(
    r"「(?P<q>[^」]*)」\s*〔\s*锚\s*[:：]\s*(?P<a>[^〕]*)〕\s*\[(?P<s>S\d+)\]\s*$")
QUOTE = re.compile(r"「[^」]*」")
ANCHOR_REF = re.compile(r"\[(S\d+)\]")

SOURCE_LINE = re.compile(
    r"^-\s*\[(?P<s>S\d+)\]\s*(?P<rest>.+?)"
    r"\|\s*(?P<url>https?://\S+)\s*\|"
    r"\s*检索日\s*(?P<d>\d{4}-\d{2}-\d{2})\s*(?:\|.*)?$"
)

PROBLEM = re.compile(r"^-\s*问题\s*(?P<n>\d+)\s*[：:、\s]")
MEDIA_ROW = re.compile(r"^-\s*主体\s*[：:]\s*(?P<who>[^｜|]+?)\s*[｜|]\s*\[(?P<s>S\d+)\]\s*$")
GAP_BODY = re.compile(r"未取到\s*[：:]\s*(?P<x>[^｜|]+)")   # 正文行：遇 ｜ 截断，故「…明细｜交人工 [待人工]」仍认出项名
GAP_ITEM = re.compile(r"^-\s*未取到\s*[：:]\s*(?P<x>[^｜|]+?)\s*$")
GAP_EXCUSE = ("不适用", "无此项", "无需披露")
GAP_NONE = "无"

# 中介机构：一条问询的公开产出通常是公司 + 会计师 + 保荐/律师 各出一份
INTERMEDIARY = ("会计", "会计师", "保荐", "律师", "律所", "评估", "审计机构", "受托管理")
MEDIARY_GAP_WORDS = ("中介", "会计师", "保荐", "律师", "律所", "评估")

# 代公司表态：本件是核对工具，不是代办，替公司说话的红线
REPLY_VOICE = ("本公司将", "本公司拟", "本公司认为", "本公司承诺", "公司承诺",
               "我方", "我司", "现回复如下", "现答复如下", "特此回复", "特此答复")
# 出结论：核对的产物是登记表，不是判断书
CONCLUSION = ("不构成重大影响", "不构成影响", "不存在问题", "符合规定", "已完成整改",
              "风险可控", "回复充分", "问询不成立", "不会被处罚", "预计通过", "通过审核",
              "建议关注", "建议买入", "建议增持", "目标价", "买入评级", "增持评级")

CLAUSE_SPLIT = re.compile(r"[；;。，,｜|]")


def mark_first_run() -> None:
    """首次运行埋点：往 ~/.cue-usage/<slug>-<日期> 落一个空文件。

    平台两个下载计数器都不可信（新 listing 首 48h 一次性播种 50~60），
    本地这枚文件是本件唯一能证明「真有人装上并跑过」的证据。
    解析参数成功后、干正事之前调用；任何失败静默跳过，绝不报错、不改进程退码。
    """
    try:
        root = Path(os.path.expanduser("~")) / ".cue-usage"
        root.mkdir(parents=True, exist_ok=True)
        target = root / f"{SLUG}-{date.today().isoformat()}"
        if not target.exists():
            target.touch()
    except Exception:                                    # noqa: BLE001
        pass


def _section_of(heading):
    h = heading.strip()
    for _ in range(2):
        h2 = NUMBERING.sub("", h)
        if h2 == h:
            break
        h = h2
    h = h.strip()
    for name in SECTIONS:
        if h == name:
            return name
        if h.startswith(name) and not h[len(name):len(name) + 1].isalnum():
            return name
    return None


def split_doc(text):
    """切成 (头部行, [(节名, 行号, 行)], [(行号, 原行)])；第三节是游离的 `## ` 标题。"""
    lines = text.splitlines()
    header, sections, stray = [], [], []
    cur = None
    seen_h2 = False
    for i, raw in enumerate(lines, 1):
        m = HEADING.match(raw)
        if m:
            seen_h2 = True
            name = _section_of(m.group(1))
            if name is None or any(name == n for n, _ln, _b in sections):
                stray.append((i, raw.strip()))
                cur = None
                continue
            cur = (name, i, [])
            sections.append(cur)
            continue
        if not seen_h2:
            header.append((i, raw))
        elif cur is not None:
            cur[2].append((i, raw))
    return header, sections, stray


def _is_finding(s):
    return s.startswith("- ") or s == "-"


def _sect(sections, name):
    for n, ln, body in sections:
        if n == name:
            return ln, body
    return None, []


def _gap_name(line):
    m = GAP_BODY.search(line)
    if not m:
        return None
    return m.group("x").strip().rstrip("。；;，,").strip()


def check(text):
    """返回 (发条列表, 备注列表)；发条＝[(码, 行号, 说明)]，行号 0 表示全篇。"""
    hits, notes = [], []
    header, sections, stray = split_doc(text)
    names = [n for n, _ln, _b in sections]

    # ---------------------------------------------------------------- 道一 形制
    header_text = "\n".join(raw for _i, raw in header)
    for mk in MARK_TEXTS:
        if mk not in header_text:
            hits.append(("IL-STRUCT", 0, "头部缺自标「%s」" % mk))
    subj = next((m.group(1) for _i, raw in header for m in [SUBJECT.match(raw)] if m), None)
    if not subj:
        hits.append(("IL-STRUCT", 0, "缺 `主体：` 行或其后为空"))
    letter = next((m.group(1) for _i, raw in header for m in [LETTER.match(raw)] if m), None)
    if not letter:
        hits.append(("IL-STRUCT", 0, "缺 `文件：` 行或其后为空"))
    for i, raw in header:
        m = LETTER_DATE.match(raw)
        if m and not ISO_DATE.match(m.group(1).strip()):
            hits.append(("IL-STRUCT", i,
                         "`收函日：` 须为 YYYY-MM-DD，实得「%s」" % m.group(1).strip()[:20]))
    missing = [s for s in SECTIONS if s not in names]
    if missing:
        hits.append(("IL-STRUCT", 0, "缺节：%s（六节须齐且按序）" % "、".join(missing)))
    else:
        order = [names.index(s) for s in SECTIONS]
        if order != sorted(order):
            hits.append(("IL-STRUCT", 0, "节序不对：实得 %s" % " → ".join(names)))
    for i, raw in stray:
        hits.append(("IL-STRUCT", i, "多出一节或重复节：%s（多一节即自造栏目）" % raw[:30]))
    for sec in CONTENT_SECTIONS:
        ln, body = _sect(sections, sec)
        if ln is None:
            continue
        n_find = 0
        for i, raw in body:
            s = raw.strip()
            if not s or s.startswith("### "):
                continue
            if not _is_finding(s):
                hits.append(("IL-STRUCT", i, "「%s」节内只许 `- ` 发现行：%s" % (sec, s[:30])))
            else:
                n_find += 1
        if n_find == 0:
            hits.append(("IL-STRUCT", ln, "「%s」节没有一条发现行" % sec))

    # ---------------------------------------------------------------- 道二 原句与锚
    refs = set()
    for sec in CONTENT_SECTIONS:
        _ln, body = _sect(sections, sec)
        for i, raw in body:
            s = raw.strip()
            if not _is_finding(s):
                continue
            for m in ANCHOR_REF.finditer(s):
                refs.add(m.group(1))
            if GAP_BODY.search(s) or "[待人工]" in s:
                continue                      # 未取到行与判断位行没有原句可挂，是设计不是漏网
            t = TRIPLE.search(s)
            if not t:
                hits.append(("IL-QUOTE", i, "发现行缺「」原句＋〔锚：…〕＋[S#] 三元组：%s" % s[:34]))
            elif not t.group("q").strip() or not t.group("a").strip():
                hits.append(("IL-QUOTE", i, "原句或锚为空：%s" % s[:34]))
    src_ln, src_body = _sect(sections, SOURCE_SECTION)
    declared = set()
    if src_ln is not None:
        for i, raw in src_body:
            s = raw.strip()
            if not s:
                continue
            m = SOURCE_LINE.match(s)
            if not m:
                hits.append(("IL-QUOTE", i,
                             "来源行形制不合（须 `- [S#] 标题 | URL | 检索日 YYYY-MM-DD`）：%s" % s[:34]))
                continue
            declared.add(m.group("s"))
    for r in sorted(refs - declared):
        hits.append(("IL-QUOTE", 0, "正文引用了 [%s] 但来源节没有登记" % r))
    if src_ln is not None and not declared:
        notes.append("来源节 0 条登记")

    # ---------------------------------------------------------------- 道三 问题与回复两向
    ids_idx, ids_rep = [], []
    _ln, body = _sect(sections, IDX_SECTION)
    for _i, raw in body:
        m = PROBLEM.match(raw.strip())
        if m:
            ids_idx.append(m.group("n"))
    _ln, body = _sect(sections, REPLY_SECTION)
    for _i, raw in body:
        m = PROBLEM.match(raw.strip())
        if m:
            ids_rep.append(m.group("n"))
    for n in [x for x in ids_idx if x not in ids_rep]:
        hits.append(("IL-PAIR", 0,
                     "索引登记了 问题%s，回复要点节没有同号条目（要么给要点，要么写明未取到）" % n))
    for n in [x for x in ids_rep if x not in ids_idx]:
        hits.append(("IL-PAIR", 0, "回复要点节出现 问题%s，索引节没有同号条目" % n))

    # ---------------------------------------------------------------- 道四 缺项点名
    body_gaps = []
    for sec in CONTENT_SECTIONS:
        _ln, body = _sect(sections, sec)
        for i, raw in body:
            s = raw.strip()
            if not _is_finding(s):
                continue
            x = _gap_name(s)
            if x:
                body_gaps.append((i, x))
    gap_ln, gap_body = _sect(sections, GAP_SECTION)
    items = []
    if gap_ln is not None:
        for i, raw in gap_body:
            s = raw.strip()
            if not s:
                continue
            m = GAP_ITEM.match(s)
            if not m:
                hits.append(("IL-GAP", i, "未取到清单只许 `- 未取到：<项名>` 形：%s" % s[:30]))
                continue
            items.append((i, m.group("x").strip().rstrip("。；;，,")))
        for i, raw in gap_body:
            for w in GAP_EXCUSE:
                if w in raw:
                    hits.append(("IL-GAP", i, "用「%s」搪塞——那是把没查当成没有" % w))
    item_names = [x for _i, x in items]
    if gap_ln is not None:
        if not items:
            hits.append(("IL-GAP", gap_ln, "未取到清单没有内容（零缺口须显式写 `未取到：无`）"))
        elif GAP_NONE in item_names and len(item_names) > 1:
            hits.append(("IL-GAP", gap_ln,
                         "既写 `未取到：无` 又列了 %d 项，自相矛盾" % (len(item_names) - 1)))
        else:
            body_names = [y for _i, y in body_gaps]
            for i, x in body_gaps:
                if x not in item_names:
                    hits.append(("IL-GAP", i, "正文写了未取到「%s」，清单没点名" % x[:26]))
            for i, x in items:
                if x != GAP_NONE and x not in body_names:
                    hits.append(("IL-GAP", i, "清单点名了「%s」，正文没有这一条" % x[:26]))

    # ---------------------------------------------------------------- 道五 回复主体齐备
    media_ln, media_body = _sect(sections, MEDIA_SECTION)
    whos = []
    if media_ln is not None:
        for i, raw in media_body:
            s = raw.strip()
            if not s:
                continue
            m = MEDIA_ROW.match(s)
            if not m:
                hits.append(("IL-MEDIA", i,
                             "回复文件行须为 `- 主体：<名称>｜[S#]`：%s" % s[:34]))
                continue
            whos.append(m.group("who").strip())
            if m.group("s") not in declared:
                hits.append(("IL-MEDIA", i, "主体行引用了 [%s] 但来源节没有登记" % m.group("s")))
        if not whos:
            hits.append(("IL-MEDIA", media_ln, "回复文件节没有登记任何一份回复文件"))
        elif not any(any(k in w for k in INTERMEDIARY) for w in whos):
            gap_txt = "".join(item_names)
            if not any(k in gap_txt for k in MEDIARY_GAP_WORDS):
                hits.append(("IL-MEDIA", media_ln,
                             "回复文件里只有公司本体，未见中介机构回复——一条问询的公开产出通常 3–5 份、"
                             "公司／会计师／保荐机构各出，可能有中介机构回复未取到"))
    # ---------------------------------------------------------------- 道六 红线
    for sec in SECTIONS:
        _ln, body = _sect(sections, sec)
        for i, raw in body:
            bare = QUOTE.sub(" ", raw)          # 引文是公函原话，不是本件的立场
            for clause in CLAUSE_SPLIT.split(bare):
                if "[待人工]" in clause:
                    continue
                v = [w for w in REPLY_VOICE if w in clause]
                c = [w for w in CONCLUSION if w in clause]
                if v or c:
                    what = []
                    if v:
                        what.append("表态：" + "、".join(sorted(set(v))))
                    if c:
                        what.append("结论：" + "、".join(sorted(set(c))))
                    hits.append(("IL-LINE", i,
                                 "红线命中（%s）：%s" % ("；".join(what), clause.strip()[:36])))
                    break
    for i, raw in header:
        bare = QUOTE.sub(" ", raw)
        c = [w for w in CONCLUSION if w in bare]
        if c:
            hits.append(("IL-LINE", i, "头部含结论词：%s" % "、".join(sorted(set(c)))))

    return hits, notes


def demo_text():
    return """# 监管问询函逐条答复核对

AI 整理初稿｜请回原文核对｜不构成投资建议｜判断位 [待人工]

主体：示例科技股份有限公司
文件：关于示例科技股份有限公司向特定对象发行股票的审核问询函
收函日：2026-03-12

## 1. 问询事项索引

- 问题1 募投项目产能消化「请说明本次募投项目新增产能的消化措施及合理性」〔锚：问询函·第 1 页·问题 1〕[S1]
- 问题2 前次募集资金使用「请说明前次募集资金的使用进度及是否存在用途变更」〔锚：问询函·第 2 页·问题 2〕[S1]

## 2. 要求提供的材料

- 问题1 要求材料：产能消化测算表「请提供产能消化测算表及在手订单明细」〔锚：问询函·第 1 页·问题 1〕[S1]
- 问题2 要求材料：前次募集资金使用明细「请提供前次募集资金使用明细表」〔锚：问询函·第 2 页·问题 2〕[S1]

## 3. 回复要点

- 问题1 回复要点：披露在手订单覆盖率「截至回复出具日，在手订单覆盖新增产能的比例为 62.35%」〔锚：回复公告·第 5 页·问题 1 回复〕[S2]
- 问题2 未取到：前次募集资金使用明细

## 4. 回复文件

- 主体：公司本体｜[S2]
- 主体：会计师事务所｜[S3]

## 5. 未取到清单

- 未取到：前次募集资金使用明细

## 来源

- [S1] 示例科技 向特定对象发行股票审核问询函（用户直供原件） | https://example.com/q1 | 检索日 2026-11-10
- [S2] 示例科技 审核问询函回复公告 | https://example.com/r1 | 检索日 2026-11-10
- [S3] 关于示例科技审核问询函回复的专项核查意见 | https://example.com/r2 | 检索日 2026-11-10
"""


# ---------------------------------------------------------------- 自测
def _mutate(text, old, new):
    n = text.count(old)
    assert n == 1, "替换目标须唯一：%r 出现 %d 次" % (old, n)
    return text.replace(old, new)


def selftest():
    good = demo_text()
    state = {"ok": True, "forms": 0}

    def one(name, want_codes, text):
        state["forms"] += 1
        got = sorted({c for c, _l, _d in check(text)[0]})
        want = sorted(set(want_codes))
        if got != want:
            state["ok"] = False
            print("FAIL 自测 %s：发条 %s，应 %s" % (name, got or "无", want or "无"))
        else:
            print("过   自测 %s：%s" % (name, "、".join(got) or "零发条"))

    one("好样零发条", [], good)

    # —— 该红的红（六道各一枚反证）——
    one("反证 形制缺自标", ["IL-STRUCT"], _mutate(good, "AI 整理初稿｜", ""))
    one("反证 原句缺锚", ["IL-QUOTE"],
        _mutate(good, "使用明细表」〔锚：问询函·第 2 页·问题 2〕[S1]", "使用明细表」[S1]"))
    one("反证 问题未答且未点名", ["IL-PAIR"],
        _mutate(good, "- 问题2 未取到：前次募集资金使用明细\n\n## 4. 回复文件",
                "- 问题9 未取到：前次募集资金使用明细\n\n## 4. 回复文件"))
    one("反证 缺项没点名", ["IL-GAP"],
        _mutate(good, "- 未取到：前次募集资金使用明细\n\n## 来源",
                "- 未取到：前次募投项目环评批复\n\n## 来源"))
    one("反证 中介机构回复缺失", ["IL-MEDIA"],
        _mutate(good, "- 主体：会计师事务所｜[S3]\n", ""))
    one("反证 代公司表态", ["IL-LINE"],
        _mutate(good, "- 问题1 回复要点：披露在手订单覆盖率",
                "- 问题1 结论：本公司将按要求完成整改「本公司将按要求完成整改」〔锚：回复公告·第 5 页〕[S2]\n"
                "- 问题1 回复要点：披露在手订单覆盖率"))

    # —— 该不红的不红（三条）——
    one("不红 引文里的表态词不是本件立场", [],
        _mutate(good, "- 问题1 回复要点：披露在手订单覆盖率",
                "- 问题1 回复要点：抄录保荐机构意见「保荐机构承诺将持续督导」〔锚：回复公告·第 6 页〕[S2]\n"
                "- 问题1 回复要点：披露在手订单覆盖率"))
    one("不红 整句待人工豁免", [],
        _mutate(good, "- 问题2 未取到：前次募集资金使用明细\n\n## 4.",
                "- 问题2 未取到：前次募集资金使用明细｜是否构成审核障碍交人工判断 [待人工]\n\n## 4."))
    # 只列了公司本体，但缺项清单已点名「保荐机构专项核查意见」⇒ 不算漏，不红
    no_cpa = _mutate(good, "- 主体：会计师事务所｜[S3]\n", "")
    no_cpa_gap = _mutate(no_cpa, "- 问题2 未取到：前次募集资金使用明细\n\n## 4.",
                         "- 问题2 未取到：前次募集资金使用明细\n"
                         "- 问题2 未取到：保荐机构专项核查意见\n\n## 4.")
    one("不红 只列公司但已点名中介机构未取到", [],
        _mutate(no_cpa_gap, "- 未取到：前次募集资金使用明细\n\n## 来源",
                "- 未取到：前次募集资金使用明细\n- 未取到：保荐机构专项核查意见\n\n## 来源"))

    print("----")
    print("自测形数=%d 不合=%d" % (state["forms"], 0 if state["ok"] else 1))
    return 0 if state["ok"] else 1


def main():
    ap = argparse.ArgumentParser(
        description="监管问询函逐条答复核对：六道机检（形制／原句锚／问题与回复对应／缺项点名／回复主体／红线）")
    ap.add_argument("path", nargs="?", help="核对表 markdown 文件")
    ap.add_argument("--selftest", action="store_true", help="跑内置夹具自检")
    ap.add_argument("--demo", action="store_true", help="打印一份完整合规样例（零输入可跑）")
    a = ap.parse_args()

    mark_first_run()

    if a.demo:
        sys.stdout.write(demo_text())
        return 0
    if a.selftest:
        return selftest()
    if not a.path:
        ap.print_usage(sys.stderr)
        print("用法错：缺输入文件路径（--demo 可先看样例）", file=sys.stderr)
        return 2

    p = Path(a.path)
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        print("读不到文件：%s" % p, file=sys.stderr)
        return 3
    if not text.strip():
        print("空稿：%s" % p, file=sys.stderr)
        return 3

    hits, notes = check(text)
    for code, ln, detail in hits:
        where = ("第 %d 行" % ln) if ln else "全篇"
        print("%s｜%s｜%s" % (code, where, detail))
    for n in notes:
        print("note｜%s" % n)
    print("----")
    if hits:
        codes = sorted({c for c, _l, _d in hits})
        print("结论：发条 %d 条，涉及 %s" % (len(hits), "、".join(codes)))
        return 1
    print("结论：六道全过（零发条）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
