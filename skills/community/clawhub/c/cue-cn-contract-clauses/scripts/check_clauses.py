#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_clauses.py — 校一份「合同逐条要点与需盯条款清单」是否合 `SKILL.md` §3 四节契约与 §5 红线。

用法：
    python3 -B scripts/check_clauses.py <清单.md> [--source 合同原文.md]
    python3 -B scripts/check_clauses.py --selftest        跑包内夹具（好样须过、七枚坏样须各发它该发的那一道）
    python3 -B scripts/check_clauses.py --help             本说明
    校样件时给上原文：--source scripts/fixtures/target-contract.md

五道（判定全集在本脚本，本文只指路）：
    道一 形制 E-FORMAT  ：头部四件自标逐字在位；四节齐且有序；概览只一行且 ≤80 字符，并逐件标出 标的／期限／价款（文里没有的那件要写「未见到」）；要点条数落在 4–20 这一带
    道二 锚   E-ANCHOR  ：每条要点行末尾带 [S#] 且该行有定位（第 N 页 或 文件:行号）；锚在第四节要有对应行；来源行必须同时带定位与解析日——解析日＝日期挂在「解析日」标签下且是日历上存在的一天，换成「合同签署日 2026-10-24」那种发条
    道三 逐字 E-QUOTE   ：引号里那句必须逐字在原文里；同一行既给页码又给行号时**两个定位各比各的**（只读其一会把假的那枚放过）；没给 --source 时明写不可判、不并入通过
    道四 点名 E-COVERAGE ：第三节七类需盯条款（单方变更／自动续约／排他／违约金／争议解决地／数据与保密／责任上限）逐类都要在位，每类要么给定位、要么写「未见到」；待填与待核不算点名；正文别处报了未读到而第三节没点名的发红；第四节零来源行发红
    道五 断言 E-LAW     ：作者自己写的句子里不得出现法律意见与效力断言（合法／违法／无效／可撤销／构成违约／有约束力／法院会支持／建议删除该条／风险等级 等），也不得出现**对裁判结果的表态**——裁判结果词（不被支持／获支持／被认定／被驳回／败诉／免责／获偿…）**单独出现就发条，不要求情态词在场**；写「大概率要再核」之后换行再写「最终不被支持」按同一语义段算（判的是句子不是物理行，续行并入前段）。评级排序字样同样零命中。引号里的合同原文不算作者表态，比对时先剥掉；要写判断就在同一语义段里挂 [待人工]

退码：0 全过（不可判项在输出里明写，不改退码）；1 有发条；2 用法错；3 取值域故障（清单或原文读不到——不读成「零违例」）。
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

SECTIONS = ('概览', '逐条要点', '需盯条款', '来源与解析日')
MARKS = ('AI 整理初稿', '请回原文核对', '不构成实务级法律意见或效力判断', '判断位 [待人工]')
ANCHOR_RE = re.compile(r'\[S(\d+)\]\s*$')
QUOTE_RE = re.compile(r'[「『](.+?)[」』]', re.S)
PAGE_RE = re.compile(r'第\s*(\d+)\s*页')
LINE_RE = re.compile(r'([A-Za-z0-9_./-]+):(\d+)')
DATE_RE = re.compile(r'\d{4}-\d{2}-\d{2}')
PARSE_DATE_RE = re.compile(r'解析日\s*[:：]?\s*(\d{4}-\d{2}-\d{2})')
PLACE_RE = re.compile(r'\[待人工\]')
UNSEEN_RE = re.compile(r'未见到|未读到|未见对应')
TODO_RE = re.compile(r'待填|待核|待补')
GAPWORDS_RE = re.compile(r'未读到|未见到|没读到|截断')
MIN_ROWS, MAX_ROWS = 4, 20
MAX_OVERVIEW = 80

WATCH_TYPES = (
    ('单方变更', r'单方变更|变更权|自行调整'),
    ('自动续约', r'自动续约|自动延续|自动展期|续期'),
    ('排他', r'排他|独家'),
    ('违约金', r'违约金|罚则'),
    ('争议解决地', r'争议解决|管辖'),
    ('数据与保密', r'保密|数据'),
    ('责任上限', r'责任上限|赔偿上限|责任限制'),
)

LAW_RE = re.compile(
    r'合法|违法|违规|无效|可撤销|应认定为|构成违约|具有法律约束力|有约束力|不受法律保护|受法律保护|'
    r'法院会|仲裁会|法院支持|仲裁支持|效力瑕疵|条款有效|约定有效|建议删除该条|建议修改该条|必须修改|应当删除|'
    r'风险等级|高风险条款|评级|打\s*\d+\s*分|排名|名次|排序')

# 预测式：情态／概率词 × 裁判结果词 同句同现＝对结果的预测，属于法律意见那一侧。
# 两支分开取（不是一张禁词表）：词面各自常见，只有同句同现才构成「替裁判表态」。
PROB_RE = re.compile(r'大概率|很可能|可能会|应该会|应会|将会|预计|估计|恐怕|恐难|未必|不一定|多半|迟早|终将|难以')
OUTCOME_RE = re.compile(r'不[会能]?被支持|不[会能]?获支持|不予支持|难获支持|获支持|受偿|不[会能]?成立|会?被认定|会?被撤销|会?被驳回|会?被解除|胜诉|败诉|免责|担责|追责|获偿|会?判[定给]|法院会|仲裁会')


def norm(t: str) -> str:
    return re.sub(r'\s+', '', t)


UNIT_START_RE = re.compile(r'^\\s*(#|[-*+|>]\\s?|\\|)')


def units_of(lines):
    """把正文切成「语义段」：行首是标题／列表项／表格／引用块的开新段，其余行接到前一段——
    道五判的是作者表态，表态不因排版换行而消失。返回 [ [(行号, 行内容), ...], ... ]。"""
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


def parse_date_state(s: str):
    """来源行的日期必须挂在「解析日」这个标签下——标签不在，日历上再真的一天也不是解析日。
    返回 (ok, 现读标签, 现读日期)。不可判不并入通过：有日期无标签与无日期两条分支各自报。"""
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


def page_block(lines, page):
    start = next((i for i, l in enumerate(lines) if PAGE_RE.search(l) and PAGE_RE.search(l).group(1) == str(page)), None)
    if start is None:
        return None
    end = next((i for i in range(start + 1, len(lines)) if PAGE_RE.search(lines[i])), len(lines))
    return '\n'.join(lines[start:end])


def strip_quotes(s: str) -> str:
    return QUOTE_RE.sub('', s)


def scan(path: Path, src_lines):
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
    if not lines or not lines[0].startswith('# '):
        add('E-FORMAT', '标题', 1, '首行不是「# 标题」这一形（规格：清单按标题命名，首行就得是标题）')
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

    if 1 in bounds:
        i0, i1 = bounds[1]
        body = [l.strip() for l in lines[i0 + 1:i1] if l.strip() and not l.strip().startswith(('#', '>', '-'))]
        if len(body) != 1:
            add('E-FORMAT', '概览行', i0 + 1, '概览有 %d 行（规格：只一行——概览的作用是一眼看完）' % len(body))
        else:
            if len(body[0]) > MAX_OVERVIEW:
                add('E-FORMAT', '概览长度', i0 + 1, '概览 %d 字符，超 %d 帽（规格：超了就不是概览）' % (len(body[0]), MAX_OVERVIEW))
            for lab, pat in (('标的', r'标的'), ('期限', r'期限'), ('价款', r'价款|金额')):
                if not re.search(lab, body[0]) and not UNSEEN_RE.search(body[0]):
                    add('E-FORMAT', '概览三件', i0 + 1,
                        '概览没标「%s」这一件（规格：标的／期限／价款三件都要标出，文里没有的就写未见到，不补常识）' % lab)

    listed = {}
    if 4 in bounds:
        i0, i1 = bounds[4]
        rows = [(i + 1, lines[i].strip()) for i in range(i0 + 1, i1) if lines[i].strip().startswith(('- ', '* '))]
        if not rows:
            add('E-COVERAGE', '来源', i0 + 1, '第四节一行来源都没有（规格：清单的价值全在能回到哪一处原文）')
        for no, ln in rows:
            m = re.match(r'^[-*]\s*\[S(\d+)\]', ln)
            if not m:
                add('E-ANCHOR', '来源', no, '来源行不以 [S#] 开头（规格：编号与锚一一对应）')
            else:
                listed[int(m.group(1))] = no
            ok_label, lab, shown = parse_date_state(ln)
            if not ok_label:
                add('E-ANCHOR', '来源', no, '来源行的日期没挂在「解析日」标签下或不是日历上存在的一天（现读标签=%s，现读日期=%s；规格：形制对不等于它是解析日——「合同签署日 2026-10-24」那种日期不在解析日标签下，2026-13-99 那一形也不是真实存在的一天；机检核这两件，核不了那天是否真是取回当天）'
                    % (lab, '、'.join(shown) or '无'))
            if not LINE_RE.search(ln) and not PAGE_RE.search(ln) and not re.search(r'https?://|www\.', ln):
                add('E-ANCHOR', '来源', no, '来源行既无 URL 也无 文件:行号／第 N 页（规格：要回到一处原文，得有个位置）')

    def verify_quotes(no, s, where):
        """该行每一段引文与每一个定位都各自比；两处定位都在，就两个都判。"""
        qs = QUOTE_RE.findall(s)
        if not qs:
            return
        if src_lines is None:
            unverifiable.append('道三 不可判：%s第 %d 行有引文，但未给 --source 原文（不可判不并入通过）' % (where, no))
            return
        txt = '\n'.join(src_lines)
        for q in qs:
            if norm(q) not in norm(txt):
                add('E-QUOTE', '逐字回原文', no, '引号里那句在原文里找不到逐字（规格：要么照抄那一处，要么写未见到落第三节，不能凭印象补）：%s' % q[:26])
        pages = set(PAGE_RE.findall(s))
        for pg in sorted(pages):
            blk = page_block(src_lines, int(pg))
            if blk is None:
                add('E-QUOTE', '页码定位', no, '「第 %s 页」在原文里找不到页标（规格：页码也要回得到，别只写一个看着像的数）' % pg)
            elif qs and not any(norm(q) in norm(blk) for q in qs):
                add('E-QUOTE', '页码定位', no, '第 %s 页里没有那段引文（规格：页码与引文要对得上）' % pg)
        for fname, ln_no in LINE_RE.findall(s):
            n = int(ln_no)
            if n < 1 or n > len(src_lines):
                add('E-QUOTE', '行号定位', no, '%s:%d 超出原文行数（现读行数=%d）——行号与页码同时给时两个都要各自成立' % (fname, n, len(src_lines)))
            elif qs and not any(norm(q) in norm(src_lines[n - 1]) for q in qs):
                add('E-QUOTE', '行号定位', no, '%s:%d 那一行没有这段引文（现读：%s）' % (fname, n, src_lines[n - 1][:26]))

    if 2 in bounds:
        i0, i1 = bounds[2]
        rows = [(i + 1, lines[i].strip()) for i in range(i0 + 1, i1) if lines[i].strip().startswith(('- ', '* '))]
        if not MIN_ROWS <= len(rows) <= MAX_ROWS:
            add('E-FORMAT', '条数带', i0 + 1, '要点 %d 条，不在 %d–%d 这一带（规格：少于 %d＝条款没拆完，多于 %d＝整份合同抄进来了）'
                % (len(rows), MIN_ROWS, MAX_ROWS, MIN_ROWS, MAX_ROWS))
        for no, s in rows:
            m = ANCHOR_RE.search(s)
            if not m:
                add('E-ANCHOR', '锚', no, '要点行末尾没有 [S#]（规格：每条要点都要回得到一个编号）')
            elif int(m.group(1)) not in listed:
                add('E-ANCHOR', '锚', no, '锚 [S%s] 在第四节没有对应行（规格：用的每个编号都要回得到来源行）' % m.group(1))
            if not LINE_RE.search(s) and not PAGE_RE.search(s):
                add('E-ANCHOR', '定位', no, '要点行没有定位（规格：带 第 N 页 或 文件:行号，读者才翻得到那一处）')
            verify_quotes(no, s, '要点')

    if 3 in bounds:
        i0, i1 = bounds[3]
        rows = [(i + 1, lines[i].strip()) for i in range(i0 + 1, i1) if lines[i].strip().startswith(('- ', '* '))]
        by_type = {}
        for no, s in rows:
            for name, pat in WATCH_TYPES:
                if re.search(pat, strip_quotes(s)) or name in s:
                    by_type.setdefault(name, []).append((no, s))
        for name, _pat in WATCH_TYPES:
            got = by_type.get(name)
            if not got:
                add('E-COVERAGE', '七类点名', i0 + 1, '第三节没有「%s」这一类（规格：七类逐类都在位——有就给定位，没有就写「未见到」，不许沉默跳过）' % name)
                continue
            for no, s in got:
                if TODO_RE.search(s):
                    add('E-COVERAGE', '待核不算点名', no, '「%s」这一类仍是待核位（规格：填定位或写未见到，待核不算点名）' % name)
                elif not (LINE_RE.search(s) or PAGE_RE.search(s) or UNSEEN_RE.search(strip_quotes(s))):
                    add('E-COVERAGE', '点名形制', no, '「%s」这一类既没给定位也没写未见到（规格：两类之一，别留半句）' % name)
                verify_quotes(no, s, '需盯条款')
        for i, ln in enumerate(lines, 1):
            if 3 in bounds and bounds[3][0] < i - 1 < bounds[3][1]:
                continue
            if ln.lstrip().startswith('#') or GAPWORDS_RE.search(strip_quotes(ln)) is None:
                continue
            if UNSEEN_RE.search(strip_quotes(ln)) and not any(
                    UNSEEN_RE.search(l) for l in lines[bounds[3][0] + 1:bounds[3][1]]):
                add('E-COVERAGE', '缺口点名', i, '这一行报了未读到，而第三节没有任何未见到条目（规格：未读到的部分一律在第三节点名，不补常识性推断）')

    for unit in units_of(lines):
        text = strip_quotes('\n'.join(l for _, l in unit)).replace('\n', '')
        if PLACE_RE.search(text):
            continue
        m = LAW_RE.search(text)
        if m:
            add('E-LAW', '断言', unit[0][0], '作者句子里出现「%s」（规格：本件不出实务级法律意见、不判定条款效力、不替代律师审查，也不评级排序；要写就同一语义段里挂 [待人工]）' % m.group(0))
        o = OUTCOME_RE.search(text)
        if o:
            no = next((i for i, l in unit if OUTCOME_RE.search(strip_quotes(l))), unit[0][0])
            q = PROB_RE.search(text)
            add('E-LAW', '裁判结果表态', no, '作者句子里出现对裁判结果的表态「%s」%s——这一支不靠情态词在场，也不按物理行切：写完「大概率要再核」再换行写「最终不被支持」算同一语义段（规格：本件不替法院或仲裁表态，也不预测某条会不会被支持；要留这个判断就同一语义段里挂 [待人工]）'
                % (o.group(0), '，并带情态「%s」' % q.group(0) if q else '（裸断言，无情态词也发条）'))
    return issues, lines, unverifiable


def run_one(path: Path, source=None, quiet=False):
    src_lines = None
    if source:
        p = Path(source)
        if not p.is_file():
            print('取值域故障：原文读不到 %s（道三不因此算通过，也不算违例）' % source)
            return 3, 0, 0
        src_lines = p.read_text(encoding='utf-8', errors='replace').split('\n')
    issues, lines, unverifiable = scan(path, src_lines)
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
    print('PASS: %s（四节齐、概览三件标出、要点条数在带内、锚与双定位各自成立、引文逐字回原文、七类都点名、法律与效力断言零命中）' % path.name)
    print('       扫过 %d 行，发条 0 条，不可判 %d 项；判定与阈值全集以本脚本现值为准（--help 看五道说明）'
          % (len(lines), len(unverifiable)))
    return 0, 0, len(unverifiable)


codes_doc = {'E-FORMAT': '道一 形制与条数带', 'E-ANCHOR': '道二 锚与定位',
             'E-QUOTE': '道三 引文逐字回原文（页码与行号各比各的）', 'E-COVERAGE': '道四 七类需盯条款点名',
             'E-LAW': '道五 法律意见与效力断言零命中'}

FX = Path(__file__).resolve().parent / 'fixtures'
CASES = [('good-clauses.md', 0, None),
         ('bad-format.md', 1, 'E-FORMAT'),
         ('bad-no-anchor.md', 1, 'E-ANCHOR'),
         ('bad-invented-quote.md', 1, 'E-QUOTE'),
         ('bad-missing-type.md', 1, 'E-COVERAGE'),
         ('bad-legal-verdict.md', 1, 'E-LAW'),
         ('bad-outcome-bare.md', 1, 'E-LAW'),
         ('bad-outcome-split.md', 1, 'E-LAW')]


def selftest(source):
    bad = 0
    for name, want_rc, want_code in CASES:
        p = FX / name
        if not p.is_file():
            print('  取值域故障：夹具不在场 %s（不读成「零违例」）' % name)
            return 3
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc, _, _ = run_one(p, source)
        detail = buf.getvalue()
        codes = sorted(set(re.findall(r'E-[A-Z]+', detail)))
        landed = bool(detail.strip()) or rc != 0
        if rc != want_rc:
            print('  不合 %s：期望退码 %d，实发 %d（注入生效=%s）' % (name, want_rc, rc, '是' if landed else '否'))
            bad += 1
            continue
        if want_code and codes != [want_code]:
            print('  不合 %s：期望只发 %s，实发码集=%s（注入生效=%s）' % (
                name, want_code, '、'.join(codes) or '空', '是' if landed else '否（空注入，读数作废）'))
            bad += 1
            continue
        if want_code is None and codes:
            print('  不合 %s：好样期望全过，实发 %s' % (name, '、'.join(codes)))
            bad += 1
            continue
        print('  ok   %s（退码 %d·期望 %s·实发码 %s·注入生效=%s）' % (
            name, rc, want_code or '全过', '、'.join(codes) or '无', '是' if (rc or codes) else '不适用（好样）'))
    n_good = sum(1 for x in CASES if x[2] is None)
    n_bad = len(CASES) - n_good
    print('selftest: ' + ('ALL GREEN（好样 %d 枚·坏样 %d 枚各只发它该发的那一道 %d/%d·逐枚报注入生效与否）'
                          % (n_good, n_bad, n_bad, n_bad) if bad == 0 else '%d 条不合预期' % bad))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(prog='check_clauses.py', description=__doc__, add_help=False)
    ap.add_argument('report', nargs='?', help='要校的清单')
    ap.add_argument('--source', help='合同原文（本地文件；给了才逐字比引文与两个定位）')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--quiet', action='store_true', help='只报末行与计数')
    ap.add_argument('-h', '--help', action='store_true')
    a = ap.parse_args()
    if a.help or (not a.report and not a.selftest):
        print(__doc__)
        return 0 if a.help else 2
    if a.selftest:
        src = a.source or str(FX / 'target-contract.md')
        if not Path(src).is_file():
            print('取值域故障：自测要的原文不在场 %s（没有原文，道三无从跑）' % src)
            return 3
        return selftest(src)
    p = Path(a.report)
    if not p.is_file():
        print('取值域故障：读不到清单文件 %s（不当「零违例」读）' % p)
        return 3
    rc, _, _ = run_one(p, a.source, quiet=a.quiet)
    return rc


if __name__ == '__main__':
    sys.exit(main())
