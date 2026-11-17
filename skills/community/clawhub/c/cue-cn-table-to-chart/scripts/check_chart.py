#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_chart.py — 校一份「图规格＋读表要点」是否合 `SKILL.md` §3 四节契约与 §5 三条硬边界。

用法：
    python3 -B scripts/check_chart.py <产物.md> [--table 表原文.md]
    python3 -B scripts/check_chart.py --selftest          跑包内夹具（好样须过、坏样须各发它该发的那一道）
    python3 -B scripts/check_chart.py --help               本说明
    校样件时给上表原文：--table scripts/fixtures/target-table.md

五道（判定全集在本脚本，本文只指路）：
    道一 形制 E-FORMAT  ：头部四件自标逐字在位；四节齐且有序；第一节四件规格（图型／横轴／纵轴／序列）齐且都不是待核位；第二节要点条数落在 3–10 这一带；第四节至少一行来源
    道二 锚   E-ANCHOR  ：每条要点行末尾带 [S#] 且该行有定位（第 N 页 或 文件:行号）；锚在第四节要有对应行；来源行必须同时带定位与解析日——解析日＝日期挂在「解析日」标签下且是日历上存在的一天；机检只核这两件，核不了那天是否真是取回当天
    道三 逐字 E-QUOTE   ：全篇任何一行里的「」都必须逐字在表里（不分行形、不分节——条目行以外的假引文同样发条）；数还要落在所报**那一行的那一格**：管道行按 | 拆列后两形之一才放行——A 整行照序（引的数与该行非空格逐格逐序相等）或 B 「列头」=「数」配对（按列头取到那一格，格里的数就得是它）；**B 的前置条件是列头格数等于该行数据格数**，列头被并（跨列表头／合并格）时格数不等，配对形在这一行整行不成立——首格也不放行，把并列列头默认对到第一格就是猜，这一行只认 A 或写进第三节；同一行既给页码又给行号时**两个定位各比各的**（只读其一会把假的那枚放过）；没给 --table 时明写不可判、不并入通过
    道四 点名 E-COVERAGE：第三节四类限度（缺格与空值／合并格与跨列表头／单位与口径／表外推与未读到）逐类在位，每类要么给定位要么写「未见到／未取到」，待核不算点名；别处报了未读到而第三节没点名的发红
    道五 断言 E-ADVICE  ：投资建议、评级与目标价、名次排序一律零命中，判的是「这一段字面里有没有投资话」这个可观察的最小事实。两张网并行：①裸断言（建议买入／目标价看至／值得投资／可投／首选／看空…）**单靠词就发条，不要求情态词在场**；②最高级／比较级形态（最高／最强／更优／优于…）与投资结论对象词（估值／基本面／前景／买入…）**同语义段同现**也发条。语义段只按结构切——标题／列表项／表格／引用块／编号项另起段，其余行含仅有缩进的普通续行并入上一段（换行与缩进都不算躲开）。**本件不设引用豁免**：书名号里的内容同样参与判定——表里真有这句只证它出现过，不为它背书；前几轮那两枚声音词表在整段上各做一次存在性判断，出处词任一枚在场就把整段洗白（段首挂表注、段尾写作者结论即静默过），那是会摆的形状，0.1.4 起退役。合法出口只有一个：第三节点名、不括原话、带定位。要留判断就同一语义段里挂 [待人工]。代价（三面同批写明）：表内含投资倾向表述时引用它就红，红的是引用行为不是造数——这是选定的保守面，不是缺陷。
退码：0 全过（不可判项在输出里明写，不改退码）；1 有发条；2 用法错；3 取值域故障（产物或表原文读不到——不读成「零违例」）。
出口形制：失败＝一行 "FAIL: <文件>（N 条）"，其下每条详行先打错误码前缀；全过＝一行 "PASS: …" 加计数行。
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import io
import re
import sys
from pathlib import Path

SECTIONS = ('图的规格', '读表要点', '图的限度与未取到', '来源与解析日')
MARKS = ('AI 整理初稿', '请回表核对', '不据图给投资建议', '判断位 [待人工]')
SPEC_KEYS = ('图型', '横轴', '纵轴', '序列')
LIMIT_KINDS = ('缺格与空值', '合并格与跨列表头', '单位与口径', '表外推与未读到')
MIN_ROWS, MAX_ROWS = 3, 10

ANCHOR_RE = re.compile(r'\[S(\d+)\]\s*$')
QUOTE_RE = re.compile(r'[「『](.+?)[」』]', re.S)
BIND_RE = re.compile(r'[「『]([^」』]{1,60})[」』]\s*[=＝]\s*[「『]([^」』]{1,60})[」』]')
CELL_ROW_RE = re.compile(r'^\s*\|(.+)\|\s*$')
PAGE_RE = re.compile(r'第\s*(\d+)\s*页')
LINE_RE = re.compile(r'([A-Za-z0-9_./-]+):(\d+)')
DATE_RE = re.compile(r'\d{4}-\d{2}-\d{2}')
PARSE_DATE_RE = re.compile(r'解析日\s*[:：]?\s*(\d{4}-\d{2}-\d{2})')
PLACE_RE = re.compile(r'\[待人工\]')
TODO_RE = re.compile(r'待填|待核|待补|（下面四件')
UNSEEN_RE = re.compile(r'未见到|未读到|未见对应|未取到')
GAPWORDS_RE = re.compile(r'未读到|未见到|没读到|截断')

ADVICE_RE = re.compile(
    r'建议买入|建议卖出|建议加仓|建议减仓|建议建仓|建议清仓|应买入|应卖出|应回避|'
    r'值得投资|不宜投资|可投|不可投|买入评级|卖出评级|目标价|评级为|予.{0,4}评级|上调评级|下调评级|'
    r'推荐买入|推荐配置|第一梯队|首选标的|跑赢行业|跑输行业|超配|低配|抄底|逃顶|止盈止损|必涨|必跌|看好后市|看空后市')
SUPER_RE = re.compile(r'最[^\n]{0,6}?(?:强|高|好|优|差|低|稳|抗跌)|更[^\n]{0,6}?(?:强|好|优|差)|优于|逊于|胜过|压过|首选|次选')
TARGET_RE = re.compile(r'估值|基本面|成长性|前景|后市|标的|投资|买入|卖出|加仓|减仓|配置|风险回报|回报')
# B 案（0.1.4）：道五**不设引用豁免**——书名号里的内容同样参与投资断言判定。
# 前几轮的「作者声音 ∥ 出处主语」两枚词表在整段上各做一次存在性判断，出处词任一枚在场就把整段豁免掉
# （段首挂表注字样、段尾写作者投资结论会静默过），且每轮都得再补同义词——那是会摆的形状。
# 现在判的是可观察的最小事实：这一段的字面里有没有投资／评级／目标话；出口只有一个——第三节点名、不括原话。
# 代价（面文三面同批写明）：表里真有投资倾向表述时，引用它就红；红的是引用行为，不是造数。

# 语义段的边界只认结构：标题／列表项／表格／引用块／编号项才另起一段（行首最多三格缩进算同一层的标记）。
# 仅有缩进的普通续行**不是**新段——「结论：」顶格、下一行两格缩进接引文，仍是一段（面文那句「换行不算躲开」靠这一枚兑现）。
UNIT_START_RE = re.compile(r'^ {0,3}(?:#|[-*+|]\s|>|\||\d+[.、]\s)')


def norm(t: str) -> str:
    return re.sub(r'\s+', '', t)


def strip_quotes(s: str) -> str:
    return QUOTE_RE.sub('', s)


def split_cells(line: str):
    m = CELL_ROW_RE.match(line)
    if m is None:
        return None
    return [c.strip() for c in m.group(1).split('|')]


def is_sep_cells(cs) -> bool:
    return bool(cs) and len(cs) >= 2 and all(c and set(c) <= set('-: ') for c in cs)


def table_model(tbl_lines):
    """行号 → 该行各格 ＋ 它所属表的列头。分隔行的上一行按 markdown 语义当列头；
    列头格数与数据行格数不等就是跨列表头，模型原样带出来，不猜哪一格对哪一列。没有分隔行的管道行不构成表，认不出列头就不判格位。"""
    model, i, n = {}, 0, len(tbl_lines)
    while i < n:
        if split_cells(tbl_lines[i]) is None:
            i += 1
            continue
        block, j = [], i
        while j < n and split_cells(tbl_lines[j]) is not None:
            block.append((j + 1, split_cells(tbl_lines[j])))
            j += 1
        sep = next((k for k, (_, cs) in enumerate(block) if is_sep_cells(cs)), None)
        if sep is not None:
            header = block[sep - 1][1] if sep >= 1 else []
            for no, cs in block[sep + 1:]:
                if not is_sep_cells(cs):
                    model[no] = {'cells': cs, 'header': header}
        i = j
    return model


def units_of(lines):
    """语义段：行首是标题／列表项／表格／引用块才开新段，其余行接到上一段——表态不因换行消失。"""
    out, cur = [], []
    for i, ln in enumerate(lines, 1):
        if not ln.strip():
            if cur:
                out.append(cur)
                cur = []
            continue
        if UNIT_START_RE.match(ln) or not cur:
            if cur:
                out.append(cur)
            cur = [(i, ln)]
        else:
            cur.append((i, ln))
    if cur:
        out.append(cur)
    return out


def page_block(lines, page):
    start = next((i for i, l in enumerate(lines) if PAGE_RE.search(l) and PAGE_RE.search(l).group(1) == str(page)), None)
    if start is None:
        return None
    end = next((i for i in range(start + 1, len(lines)) if PAGE_RE.search(lines[i])), len(lines))
    return '\n'.join(lines[start:end])


def parse_date_state(s: str):
    """返回 (ok, 现读标签, 现读日期)：日期必须在「解析日」标签下且是日历上存在的一天。"""
    ds = PARSE_DATE_RE.findall(s)
    real = []
    for x in ds:
        try:
            dt.date.fromisoformat(x)
            real.append(x)
        except ValueError:
            continue
    if ds and not real:
        return False, '解析日', ds
    if real:
        return True, '解析日', real
    bare = DATE_RE.findall(s)
    if bare:
        labels = re.findall(r'([一-龥]{2,6})\s*[:：]?\s*' + re.escape(bare[0]), s)
        return False, (labels[0] if labels else '无标签'), bare
    return False, '无', []


def scan(path: Path, tbl_lines):
    issues = []
    unverifiable = []
    seen = set()

    def add(code, lane, no, msg):
        key = (code, no, msg)
        if key in seen:
            return
        seen.add(key)
        issues.append((code, lane, no, msg))

    lines = path.read_text(encoding='utf-8', errors='replace').split('\n')
    model = table_model(tbl_lines) if tbl_lines is not None else {}
    verified = None
    if tbl_lines is not None:
        verified = set()
        ntxt = norm('\n'.join(tbl_lines))
        for i, ln in enumerate(lines, 1):
            for q in QUOTE_RE.findall(ln):
                if norm(q) in ntxt:
                    verified.add(norm(q))
                else:
                    add('E-QUOTE', '逐字回表（全篇）', i,
                        '「%s」在表原文里找不到逐字（规格：全篇书名号只有一个用途＝逐字引表里的原文，条目行内外都一样；表里没有的要么别括，要么写进第三节说未读到，不能凭印象补）' % q[:22])
    if not lines or not lines[0].startswith('# '):
        add('E-FORMAT', '标题', 1, '首行不是「# 标题」这一形（规格：产物按标题命名，首行就得是标题）')
    head_end = next((i for i, l in enumerate(lines) if l.startswith('## ')), len(lines))
    head = '\n'.join(lines[:head_end])
    for need in MARKS:
        if need not in head:
            add('E-FORMAT', '头部', 1, '头部自标缺『%s』（规格：四件逐字写在第一个「## 」之前）' % need)

    idxs = []
    for n, name in enumerate(SECTIONS, 1):
        hit = [i for i, l in enumerate(lines) if re.match(r'^##\s*%d、%s' % (n, re.escape(name)), l)]
        if not hit:
            add('E-FORMAT', '四节', 1, '缺「## %d、%s」节（规格：四节齐且按一二三四有序）' % (n, name))
        else:
            idxs.append((n, hit[0]))
    bounds = {}
    for pos in range(len(idxs)):
        n, i0 = idxs[pos]
        i1 = idxs[pos + 1][1] if pos + 1 < len(idxs) else len(lines)
        bounds[n] = (i0, i1)

    def rows_in(n):
        if n not in bounds:
            return []
        i0, i1 = bounds[n]
        return [(i + 1, lines[i].strip()) for i in range(i0 + 1, i1) if lines[i].strip().startswith(('- ', '* '))]

    def verify_row(no, s):
        """两个定位各自比：页码要在那一页找得到，行号要在那一行找得到——只读其一会把假的那枚放过。"""
        qs = QUOTE_RE.findall(s)
        if not qs or tbl_lines is None:
            return
        for pg in sorted(set(PAGE_RE.findall(s))):
            blk = page_block(tbl_lines, int(pg))
            if blk is None:
                add('E-QUOTE', '页码定位', no, '「第 %s 页」在表原文里找不到页标（规格：页码也要回得到，别只写一个看着像的数）' % pg)
            elif not any(norm(q) in norm(blk) for q in qs):
                add('E-QUOTE', '页码定位', no, '第 %s 页里没有那一格数（规格：页码与数要对得上）' % pg)
        for fname, ln_no in LINE_RE.findall(s):
            n = int(ln_no)
            if n < 1 or n > len(tbl_lines):
                add('E-QUOTE', '行号定位', no, '%s:%d 超出表原文行数（现读行数=%d）——行号与页码同时给时两个都要各自成立' % (fname, n, len(tbl_lines)))
            elif not any(norm(q) in norm(tbl_lines[n - 1]) for q in qs):
                add('E-QUOTE', '行号定位', no, '%s:%d 那一行没有这格数（现读：%s）' % (fname, n, tbl_lines[n - 1][:26]))

    def verify_cells(no, s):
        """数落在所报那一行的那一格才放行——A 整行照序，B 「列头」=「数」配对，两形之一；配了列头就得按列头取到那一格。
        全篇每一行都过这一道，不分条目行内外（非条目行想借「数在这一行」蒙过去同样发条）。"""
        if tbl_lines is None:
            return
        spans = QUOTE_RE.findall(s)
        rows_cited = []
        for _, ln_no in LINE_RE.findall(s):
            R = model.get(int(ln_no))
            if R is not None:
                rows_cited.append((int(ln_no), R))
        if not rows_cited:
            return
        binds = [(norm(h), norm(v), h, v) for h, v in BIND_RE.findall(s)]

        for hn, vn, hraw, vraw in binds:
            hit, why = None, []
            for ln_no, R in rows_cited:
                cs, hdr = R['cells'], R['header']
                nhdr = [norm(x) for x in hdr]
                if len(hdr) != len(cs):
                    why.append('第 %d 行的列头 %d 格对不上数据 %d 格＝跨列表头或合并格，本件不按列名猜那一格（把并列的列头默认对到第一格就是猜）——这一行只认整行照序，或把这一格写进第三节' % (ln_no, len(hdr), len(cs)))
                    continue
                if hn not in nhdr:
                    why.append('第 %d 行的列头里没有「%s」（现读列头=%s）' % (ln_no, hraw, '、'.join(hdr) or '该表没认到列头'))
                    continue
                k = nhdr.index(hn)
                if norm(cs[k]) == vn:
                    hit = cs[k]
                    break
                why.append('第 %d 行按「%s」取到的那一格是 %s' % (ln_no, hdr[k], cs[k] if cs[k].strip() else '空格（表里没写值）'))
            if hit is None:
                add('E-QUOTE', '格位·列头配对不成立', no,
                    '「%s」=「%s」这一对里，那一格不是这个数（%s；规格：格里是几就写几——空值「—」不等于 0，也不等于上一年的数，对不回列头就别配成一对）'
                    % (hraw, vraw, '；'.join(why)))

        if not spans:
            return
        for ln_no, R in rows_cited:
            cs, hdr = R['cells'], R['header']
            nhdr = [norm(x) for x in hdr]
            label = norm(cs[0]) if cs else ''
            data = [norm(c) for c in cs[1:] if c.strip()]
            vals = [(q, norm(q)) for q in spans if norm(q) != label and norm(q) not in nhdr and norm(q) in data]
            if not vals or [v for _, v in vals] == data:
                continue
            shown = '、'.join(c for c in cs[1:] if c.strip())
            if len(hdr) != len(cs):
                if not binds:
                    add('E-QUOTE', '格位·列头对不齐只认整行照序', no,
                        '第 %d 行的列头 %d 格对不上数据 %d 格＝跨列表头或合并格，本件不按列名猜那一格；本行括的是 %s（该行各格=%s）——这一行要么整行照序按列次序括全，要么写进第三节'
                        % (ln_no, len(hdr), len(cs), '、'.join('「%s」' % q for q, _ in vals), shown))
                continue
            if not binds:
                add('E-QUOTE', '格位·整行照序或配列头', no,
                    '第 %d 行按 | 拆列后的数=%s，本行括的是 %s——既不是整行照序，也没写一个「列头」=「数」（规格：光说数在这一行不够，得说清是哪一格；跨列表头对不回列头的就整行照序写或落第三节）'
                    % (ln_no, shown, '、'.join('「%s」' % q for q, _ in vals)))
                continue
            for q, v in vals:
                ok = any(vv == v and hh in nhdr and nhdr.index(hh) < len(cs) and norm(cs[nhdr.index(hh)]) == v
                         for hh, vv, _, _ in binds)
                if not ok:
                    add('E-QUOTE', '格位·数没配列头', no,
                        '「%s」确实在第 %d 行里，但没有一个列头配对把它指到这一格（现读列头=%s；该行各格=%s）——同一行另一格的数不能顶替你要说的那一格，跨表借列头也不算（本行只认这一行的列头）'
                        % (q, ln_no, '、'.join(hdr) or '该表没认到列头', shown))

    # 道三的另一半：逐行核格位，全篇都跑——非条目行想借「数在这一行」蒙过去也不行
    if tbl_lines is not None:
        for i, ln in enumerate(lines, 1):
            verify_cells(i, ln)
    elif any(QUOTE_RE.findall(l) for l in lines):
        unverifiable.append('全篇 %d 处书名号引文既没逐字回表、也没核格位（未给 --table 表原文，逐字回表与格位这两项无从核，故列为不可判；不可判不并入通过——道五不依赖表原文，书名号里的内容照旧参与判定）'
                            % sum(len(QUOTE_RE.findall(l)) for l in lines))

    # 第一节：规格四件
    if 1 in bounds:
        rows = rows_in(1)
        got = {}
        for no, s in rows:
            for k in SPEC_KEYS:
                m = re.match(r'^[-*]\s*%s\s*[：:]\s*(.*)$' % k, s)
                if m:
                    got[k] = (no, m.group(1).strip())
        for k in SPEC_KEYS:
            if k not in got:
                add('E-FORMAT', '规格四件', bounds[1][0] + 1, '第一节没有「%s」这一件（规格：图型／横轴／纵轴／序列四件都在，缺一件图就画不出来）' % k)
            elif TODO_RE.search(got[k][1]):
                add('E-FORMAT', '规格待核', got[k][0], '「%s」仍是待核位（规格：这一件要人选，待核不算填过——本件不代选图型）' % k)
            else:
                verify_row(got[k][0], got[k][1])

    # 第二节：要点条数与锚
    listed = {}
    if 4 in bounds:
        rows = rows_in(4)
        if not rows:
            add('E-COVERAGE', '来源', bounds[4][0] + 1, '第四节一行来源都没有（规格：产物的价值全在能回到哪一格表）')
        for no, ln in rows:
            m = re.match(r'^[-*]\s*\[S(\d+)\]', ln)
            if not m:
                add('E-ANCHOR', '来源', no, '来源行不以 [S#] 开头（规格：编号与锚一一对应）')
            else:
                listed[int(m.group(1))] = no
            ok_label, lab, shown = parse_date_state(ln)
            if not ok_label:
                add('E-ANCHOR', '来源', no, '来源行的日期没挂在「解析日」标签下或不是日历上存在的一天（现读标签=%s，现读日期=%s；规格：形制对不等于它是解析日——「合同签署日」那种标签不算，2026-13-99 也不是真实的一天；机检只核这两件，核不了那天是否真是取回当天）'
                    % (lab, '、'.join(shown) or '无'))
            if not LINE_RE.search(ln) and not PAGE_RE.search(ln) and not re.search(r'https?://|www\.', ln):
                add('E-ANCHOR', '来源', no, '来源行既无 URL 也无 文件:行号／第 N 页（规格：要回到一处表，得有个位置）')

    if 2 in bounds:
        rows = rows_in(2)
        if not MIN_ROWS <= len(rows) <= MAX_ROWS:
            plain = [lines[i].strip() for i in range(bounds[2][0] + 1, bounds[2][1])
                     if lines[i].strip() and not lines[i].strip().startswith(('- ', '* '))]
            if plain:
                add('E-FORMAT', '条数带·列表符', bounds[2][0] + 1,
                    '第二节没有以「- 」或「* 」起的要点行（现读该节有 %d 行普通文字——机检按列表符计条数，普通行不算要点；契约：每条写成一行列表项，行首必须是 - 或 *）'
                    % len(plain))
            else:
                add('E-FORMAT', '条数带', bounds[2][0] + 1, '要点 %d 条，不在 %d–%d 这一带（规格：少于 %d＝这张表没读透，多于 %d＝把整张表抄下来了）'
                    % (len(rows), MIN_ROWS, MAX_ROWS, MIN_ROWS, MAX_ROWS))
        for no, s in rows:
            m = ANCHOR_RE.search(s)
            if not m:
                add('E-ANCHOR', '锚', no, '要点行末尾没有 [S#]（规格：每条要点都要回得到一个编号）')
            elif int(m.group(1)) not in listed:
                add('E-ANCHOR', '锚', no, '锚 [S%s] 在第四节没有对应行（规格：用的每个编号都要回得到来源行）' % m.group(1))
            if not LINE_RE.search(s) and not PAGE_RE.search(s):
                add('E-ANCHOR', '定位', no, '要点行没有定位（规格：带 第 N 页 或 文件:行号，读者才翻得到那一格）')
            verify_row(no, s)

    # 第三节：四类限度点名
    if 3 in bounds:
        rows = rows_in(3)
        by_kind = {}
        for no, s in rows:
            for k in LIMIT_KINDS:
                if k in s or (k.split('与')[0] in strip_quotes(s)):
                    by_kind.setdefault(k, []).append((no, s))
        for k in LIMIT_KINDS:
            got = by_kind.get(k)
            if not got:
                add('E-COVERAGE', '四类点名', bounds[3][0] + 1, '第三节没有「%s」这一类（规格：四类逐类在位——有就给位置，没有就写未见到，不许沉默跳过）' % k)
                continue
            for no, s in got:
                if TODO_RE.search(s):
                    add('E-COVERAGE', '待核不算点名', no, '「%s」这一类仍是待核位（规格：填位置或写未见到，待核不算点名）' % k)
                elif not (LINE_RE.search(s) or PAGE_RE.search(s) or UNSEEN_RE.search(strip_quotes(s))):
                    add('E-COVERAGE', '点名形制', no, '「%s」这一类既没给位置也没写未见到（规格：两类之一，别留半句）' % k)
                verify_row(no, s)
        for i, ln in enumerate(lines, 1):
            if 3 in bounds and bounds[3][0] < i - 1 < bounds[3][1]:
                continue
            if ln.lstrip().startswith('#') or not GAPWORDS_RE.search(strip_quotes(ln)):
                continue
            if UNSEEN_RE.search(strip_quotes(ln)) and not any(UNSEEN_RE.search(l) for l in lines[bounds[3][0] + 1:bounds[3][1]]):
                add('E-COVERAGE', '缺口点名', i, '这一行报了未读到，而第三节没有任何未见到／未取到条目（规格：没读到的部分一律在第三节点名，不补常识性推断）')

    # 第五节判据：语义段制，两网并行；B 案不设引用豁免——书名号内同样判（引号里藏不进作者的话，也藏不进表里的投资话）
    for unit in units_of(lines):
        raw = '\n'.join(l for _, l in unit)
        text = raw.replace('\n', '')
        if PLACE_RE.search(text):
            continue
        m = ADVICE_RE.search(text)
        if m:
            no = next((i for i, l in unit if ADVICE_RE.search(l)), unit[0][0])
            add('E-ADVICE', '投资断言', no, '作者句子里出现投资／评级／目标价断言「%s」（规格：本件不据图给投资建议、不判评级与目标价；裸断言单靠词就发条，不要求情态词在场；**本件不设引用豁免**——书名号里的内容同样判，表里有这句只证它出现过、不为它背书；分行与缩进不算躲开（缩进续行并入上一段）；合法出口＝第三节点名、不括原话；要留判断就同一语义段里挂 [待人工]）' % m.group(0))
            continue
        s, tg = SUPER_RE.search(text), TARGET_RE.search(text)
        if s and tg:
            no = next((i for i, l in unit if SUPER_RE.search(l)), unit[0][0])
            add('E-ADVICE', '结论式名次', no, '作者句子里「%s」与「%s」同语义段同现——换了说法的投资结论同样拦（规格：不据图替读者下判断；换行不算躲开，续行并入上一段；要留就挂 [待人工]）'
                % (s.group(0), tg.group(0)))
    return issues, lines, unverifiable


codes_doc = {'E-FORMAT': '道一 形制与规格四件', 'E-ANCHOR': '道二 锚与定位与解析日标签',
             'E-QUOTE': '道三 逐字回表（全篇书名号都回表；数按列头配对或整行照序落那一格，列头格数不等于数据格数时配对形整行不成立；页码与行号各比各的）',
             'E-COVERAGE': '道四 四类限度点名',
             'E-ADVICE': '道五 投资断言零命中（语义段制；不设引用豁免，书名号内同样判）'}

FX = Path(__file__).resolve().parent / 'fixtures'
CASES = [('good-chart.md', 0, None),
         ('good-quoted-note.md', 0, None),
         ('good-merged-order.md', 0, None),
         ('good-plain-quote.md', 0, None),
         ('good-third-party.md', 0, None),
         ('bad-spec.md', 1, 'E-FORMAT'),
         ('bad-no-anchor.md', 1, 'E-ANCHOR'),
         ('bad-invented-number.md', 1, 'E-QUOTE'),
         ('bad-unbound-quote.md', 1, 'E-QUOTE'),
         ('bad-cell-misplaced.md', 1, 'E-QUOTE'),
         ('bad-no-header-pair.md', 1, 'E-QUOTE'),
         ('bad-cell-empty-zero.md', 1, 'E-QUOTE'),
         ('bad-merged-bind.md', 1, 'E-QUOTE'),
         ('bad-conclusion-crossline.md', 1, 'E-ADVICE'),
         ('bad-author-voice-verb.md', 1, 'E-ADVICE'),
         ('bad-quote-conclusion.md', 1, 'E-ADVICE'),
         ('bad-quote-source-only.md', 1, 'E-ADVICE'),
         ('bad-quote-third-party.md', 1, 'E-ADVICE'),
         ('bad-quote-bare.md', 1, 'E-ADVICE'),
         ('bad-missing-limit.md', 1, 'E-COVERAGE'),
         ('bad-advice.md', 1, 'E-ADVICE'),
         ('bad-bare-outcome.md', 1, 'E-ADVICE'),
         ('bad-superlative.md', 1, 'E-ADVICE')]
# 夹具各配自己那张表：带表注的那张证「表里真有这句」（道五的两枚声音反卡与正控都靠它），跨列表头那张证「格数不等时配对形整行不成立」
CASE_TABLE = {'good-quoted-note.md': 'target-table-noted.md', 'bad-quote-conclusion.md': 'target-table-noted.md',
              'good-plain-quote.md': 'target-table-noted.md', 'good-third-party.md': 'target-table-noted.md',
              'bad-conclusion-crossline.md': 'target-table-noted.md', 'bad-author-voice-verb.md': 'target-table-noted.md',
              'bad-quote-source-only.md': 'target-table-noted.md', 'bad-quote-third-party.md': 'target-table-noted.md',
              'bad-quote-bare.md': 'target-table-noted.md',
              'good-merged-order.md': 'target-table-merged.md', 'bad-merged-bind.md': 'target-table-merged.md'}


def run_one(path: Path, source=None, quiet=False):
    tbl_lines = None
    if source:
        p = Path(source)
        if not p.is_file():
            print('取值域故障：表原文读不到 %s（道三不因此算通过，也不算违例）' % source)
            return 3, 0, 0
        tbl_lines = p.read_text(encoding='utf-8', errors='replace').split('\n')
    issues, lines, unverifiable = scan(path, tbl_lines)
    codes = sorted({c for c, _, _, _ in issues})
    counts = {}
    for c, _, _, _ in issues:
        counts[c] = counts.get(c, 0) + 1
    if not quiet:
        for code, lane, no, msg in issues:
            print('  [%s] [%s] 第 %d 行：%s' % (code, lane, no, msg))
        for u in unverifiable:
            print('  [不可判] %s' % u)
    if issues:
        print('FAIL: %s（%d 条）' % (path.name, len(issues)))
        print('       ' + '；'.join('%s %d 条' % (c, n) for c, n in sorted(counts.items())))
        print('       码表: ' + '；'.join('%s=%s' % (c, codes_doc[c]) for c in codes))
        return 1, len(issues), len(unverifiable)
    print('PASS: %s（四节齐、规格四件人选过、要点条数在带内、锚与双定位各自成立、数逐字回表、四类限度都点名、投资与评级断言零命中）' % path.name)
    print('       扫过 %d 行，发条 0 条，不可判 %d 项；判定与阈值全集以本脚本现值为准（--help 看五道说明）'
          % (len(lines), len(unverifiable)))
    return 0, 0, len(unverifiable)


def selftest(source):
    bad = 0
    for name, want_rc, want_code in CASES:
        p = FX / name
        if not p.is_file():
            print('  取值域故障：夹具不在场 %s（不读成「零违例」）' % name)
            return 3
        tbl = CASE_TABLE.get(name)
        srcp = FX / tbl if tbl else Path(source)
        if not srcp.is_file():
            print('  取值域故障：这一枚夹具要的表原文不在场 %s（没有原文，道三与格位无从跑）' % srcp.name)
            return 3
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc, _, _ = run_one(p, str(srcp))
        detail = buf.getvalue()
        codes = sorted(set(re.findall(r'E-[A-Z]+', '\n'.join(l for l in detail.splitlines() if l.lstrip().startswith('[E-')))))
        landed = bool(detail.strip()) or rc != 0
        if rc != want_rc:
            print('  不合 %s：期望退码 %d，实发 %d（注入生效=%s）' % (name, want_rc, rc, '是' if landed else '否'))
            bad += 1
            continue
        if want_code and codes != [want_code]:
            print('  不合 %s：期望只发 %s，实发码集=%s（注入生效=%s）' % (name, want_code, '、'.join(codes) or '空', '是' if landed else '否（空注入，读数作废）'))
            bad += 1
            continue
        if want_code is None and codes:
            print('  不合 %s：好样期望全过，实发 %s' % (name, '、'.join(codes)))
            bad += 1
            continue
        print('  ok   %s（退码 %d·期望 %s·实发码 %s·表=%s·注入生效=%s）' % (
            name, rc, want_code or '全过', '、'.join(codes) or '无', tbl or '默认合成表', '是' if (rc or codes) else '不适用（好样）'))
    n_good = sum(1 for x in CASES if x[2] is None)
    n_bad = len(CASES) - n_good
    print('selftest: ' + ('ALL GREEN（好样 %d 枚·坏样 %d 枚各只发它该发的那一道 %d/%d·逐枚报注入生效与否）'
                          % (n_good, n_bad, n_bad, n_bad) if bad == 0 else '%d 条不合预期' % bad))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(prog='check_chart.py', description=__doc__, add_help=False)
    ap.add_argument('report', nargs='?', help='要校的产物')
    ap.add_argument('--table', help='表原文（本地文件；给了才逐字比数与两个定位）')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--quiet', action='store_true', help='只报末行与计数')
    ap.add_argument('-h', '--help', action='store_true')
    a = ap.parse_args()
    if a.help or (not a.report and not a.selftest):
        print(__doc__)
        return 0 if a.help else 2
    if a.selftest:
        src = a.table or str(FX / 'target-table.md')
        if not Path(src).is_file():
            print('取值域故障：自测要的表原文不在场 %s（没有原文，道三无从跑）' % src)
            return 3
        return selftest(src)
    p = Path(a.report)
    if not p.is_file():
        print('取值域故障：读不到产物文件 %s（不当「零违例」读）' % p)
        return 3
    rc, _, _ = run_one(p, a.table, quiet=a.quiet)
    return rc


if __name__ == '__main__':
    sys.exit(main())
