#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_fit.py — 校一份「简历 × JD 双向核对」是否合 `SKILL.md` §3 四节契约与 §5 红线。

用法：
    python3 -B scripts/check_fit.py <报告.md> [--jd JD.md] [--resume 简历.md]
    python3 -B scripts/check_fit.py --selftest              跑包内夹具（好样须过、七枚坏样须各发它该发的那一道）
    python3 -B scripts/check_fit.py --help                   本说明
    校样件时给上两枚原文：--jd scripts/fixtures/target-jd.md --resume scripts/fixtures/target-resume.md

五道（判定全集在本脚本，本文只指路）：
    道一 形制 E-FORMAT   ：头部四件自标逐字在位；四节齐且有序；一句话结论只一行且 ≤80 字符，且这一行要有两件结构在场——**报到哪几条**（计数＋条）与**未读到／缺口点名**；逐条对齐行数落在 3–15 这一带
    道一附 结论位归属    ：第一节若引原话，同一行必须写明那是谁的话（简历自述／JD 原文一类），否则发 E-RANK——被引者的话只能当证据，搬进「结论」这一格就成了报告自己的名次
    道二 锚   E-ANCHOR   ：每条对齐行必须同时有要求锚与证据锚，且两个编号在第四节都有对应行；来源行必须带 定位（文件:行号 或 URL）＋解析日
    道三 逐字 E-QUOTE    ：要求引号里那句必须逐字在 JD 原文里，证据引号里那句必须逐字在简历原文里——只给一侧时另一侧明写不可判，不并入通过
    道四 缺口 E-COVERAGE ：第三节两栏（JD 有要求而简历无证据／简历有内容而 JD 不关心）都要在位；第二节判为无证据的要求必须在第三节点名；第四节零来源行发红
    道五 断言 E-RANK     ：推荐录用／建议录用／优先录用／排名／排序／打分／淘汰 一类人评断言零命中；**换了说法的名次也拦**——最高级／比较级形态（最适合／更匹配／优于…）与面向用户结论的对象词（本岗位／候选人／申请者／录用…）同句同现即发条，逐字挂了锚照样发红；同行挂 [待人工] 才放行（本件只交付能回到原文的事实；引号里的原话先剥掉，那是被引者说的）

退码：0 全过（不可判的项在输出里明写，不改退码）；1 有发条；2 用法错；3 取值域故障（报告读不到，或原文给了路径却读不到——不读成「零违例」）。
出口形制：失败＝一行 "FAIL: <文件>（N 条）"，其下每条详行先打错误码前缀；全过＝一行 "PASS: …" 加计数行。
"""

from __future__ import annotations

import argparse
import contextlib
import io
import re
import sys
from pathlib import Path

SECTIONS = ('一句话结论', '逐条对齐', '缺口与未取到', '来源')
MARKS = ('AI 整理初稿', '请回原文核对', '不构成录用或排序建议', '判断位 [待人工]')
ANCHOR_RE = re.compile(r'\[S(\d+)\]')
QUOTE_RE = re.compile(r'[「『](.+?)[」』]', re.S)
LOC_RE = re.compile(r'[A-Za-z0-9_./-]+:\d+|https?://\S+|www\.\S+')
DATE_RE = re.compile(r'\d{4}-\d{2}-\d{2}')
PLACE_RE = re.compile(r'\[待人工\]')
RANK_RE = re.compile(r'推荐录用|建议录用|优先录用|应当录用|不建议录用|直接淘汰|淘汰|排名第一|第二名|排序|名次|打分|评分最高|更合适的人选|不合适该淘汰')

# 结构式判据（不扩禁词表）：最高级／比较级形态 × 面向用户结论的对象词 同句同现＝本报告在替人排先后。
# 两支分开取，词面各自常见，只有同句同现才构成结论；引号里的原话先剥掉——那是被引者说的，不是本报告下的判断。
SUPER_RE = re.compile(r'最[^\n]{0,6}?(?:适合|合适|匹配|契合|符合|贴近|接近|优|佳|强)|最[一二三]名|第一名|首选|次选|更[^\n]{0,6}?(?:适合|合适|匹配|契合|符合|优|强|佳)|优于|胜过|高过|压过')
CONCL_RE = re.compile(r'本岗位|该岗位|这个岗位|此岗位|岗位|候选人|申请者|应聘者|应聘|录用|入职|进人|招人|综上|因此|所以|建议|推荐|结论|取舍')
NOEVID_RE = re.compile(r'无证据|没有证据|未见证据|未取到')

# 第一节「结论」位的结构判据（不靠扩名次词表）：要说清匹配到哪几条＋未读到哪些；引号必须带归属。
COUNT_RE = re.compile(r'(?<![\d])(?:\d+|[一二三四五六七八九十两]+)\s*条')
GAPWORD_FIT_RE = re.compile(r'未取到|未读到|无证据|没有证据|部分证据|缺口|未见|只有部分')
ATTRIB_RE = re.compile(r'自述|原话|原文|写的|写道|说过|简历|JD|岗位说明|对方|本人')
MIN_ROWS, MAX_ROWS = 3, 15
MAX_CONCLUSION = 80


def norm(t: str) -> str:
    return re.sub(r'\s+', '', t)


def load(path):
    if path is None:
        return None
    p = Path(path)
    if not p.is_file():
        return False
    return norm(p.read_text(encoding='utf-8', errors='replace'))


def scan(path: Path, jd_text, resume_text):
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
        body = [l.strip() for l in lines[i0 + 1:i1] if l.strip() and not l.strip().startswith(('#', '>'))]
        concl = body[0] if len(body) == 1 else ''
        if len(body) != 1:
            add('E-FORMAT', '结论行', i0 + 1, '一句话结论有 %d 行（规格：只一行——多出来的那句就不叫一句话）' % len(body))
        elif len(body[0]) > MAX_CONCLUSION:
            add('E-FORMAT', '结论长度', i0 + 1, '一句话结论 %d 字符，超 %d 帽（规格：结论要短到能被一眼读完）'
                % (len(body[0]), MAX_CONCLUSION))
        elif concl:
            if not COUNT_RE.search(concl):
                add('E-FORMAT', '结论结构', i0 + 1, '一句话结论没报到哪一条（现读=%s；规格：这一格要说清「几条有逐字证据、几条没有」——不计数就不是核对结果，是一句感想）'
                    % concl[:26])
            if not GAPWORD_FIT_RE.search(concl):
                add('E-FORMAT', '结论结构', i0 + 1, '一句话结论没点名缺口（现读=%s；规格：要说清未取到／无证据／只有部分证据的是哪几条，缺这一半就把缺口藏进了语气里）'
                    % concl[:26])
            for q in QUOTE_RE.findall(concl):
                if not ATTRIB_RE.search(concl):
                    add('E-RANK', '结论位带引号无归属', i0 + 1, '第一节引了原话「%s」却没写这是谁的话（规格：被引者的话只能当证据、不能当本报告的结论——要么写明「简历自述／JD 原文」，要么把这句放回第二节挂锚；这条与引号内容无关，判的是「结论」这一格的框架）'
                        % q[:18])
                    break

    listed = {}
    if 4 in bounds:
        i0, i1 = bounds[4]
        rows = [(i + 1, lines[i].strip()) for i in range(i0 + 1, i1) if lines[i].strip().startswith(('- ', '* '))]
        if not rows:
            add('E-COVERAGE', '来源', i0 + 1, '第四节一行来源都没有（规格：核对报告的价值全在能回到哪一处原文）')
        for no, ln in rows:
            m = re.match(r'^[-*]\s*\[S(\d+)\]', ln)
            if not m:
                add('E-ANCHOR', '来源', no, '来源行不以 [S#] 开头（规格：编号与锚一一对应）')
            else:
                listed[int(m.group(1))] = no
            if not DATE_RE.search(ln):
                add('E-ANCHOR', '来源', no, '来源行缺解析日 YYYY-MM-DD（规格：两侧文档都在改，这一行要说清正文是哪一天取回的；机检只核它成形、是日历上存在的一天，核不了那天是否真是取回当天——取回时刻由人登记并对得上）')
            if not LOC_RE.search(ln):
                add('E-ANCHOR', '来源', no, '来源行既无 URL 也无 文件:行号 定位（规格：要回到一处原文，得有个位置）')

    row_count = 0
    named_gaps = []
    if 2 in bounds:
        i0, i1 = bounds[2]
        rows = [(i + 1, lines[i].strip()) for i in range(i0 + 1, i1) if lines[i].strip().startswith(('- ', '* '))]
        row_count = len(rows)
        if not MIN_ROWS <= row_count <= MAX_ROWS:
            add('E-FORMAT', '条数带', i0 + 1, '逐条对齐 %d 行，不在 %d–%d 这一带（规格：少于 %d＝没逐条对完，多于 %d＝把整份 JD 抄进来了）'
                % (row_count, MIN_ROWS, MAX_ROWS, MIN_ROWS, MAX_ROWS))
        for no, s in rows:
            ids = [int(x) for x in ANCHOR_RE.findall(s)]
            quotes = QUOTE_RE.findall(s)
            if len(ids) < 2:
                add('E-ANCHOR', '双锚', no, '对齐行只有 %d 枚锚（规格：要求一枚、证据一枚，两枚都要在第四节有对应行）' % len(ids))
            for i in ids:
                if i not in listed:
                    add('E-ANCHOR', '锚', no, '锚 [S%d] 在第四节没有对应行（规格：用的每个编号都要回得到来源行）' % i)
            if len(quotes) < 2:
                add('E-QUOTE', '引用形制', no, '对齐行的引号不足两段（规格：要求与证据各用「」括出逐字那一段）')
            else:
                req, ev = quotes[0], quotes[1]
                if jd_text is None:
                    unverifiable.append('道三 不可判：第 %d 行的要求那句没比——未给 --jd 原文' % no)
                elif norm(req) not in jd_text:
                    add('E-QUOTE', '要求逐字', no, '要求引号里那句在 JD 原文里找不到逐字（规格：要求要照抄 JD，不要转述后自称原文）')
                if resume_text is None:
                    unverifiable.append('道三 不可判：第 %d 行的证据那句没比——未给 --resume 原文' % no)
                elif norm(ev) not in resume_text:
                    add('E-QUOTE', '证据逐字', no, '证据引号里那句在简历原文里找不到逐字（规格：证据要么照抄简历原话，要么写成未取到落第三节，不能造）')
            if NOEVID_RE.search(s):
                qm = QUOTE_RE.findall(s)
                if qm:
                    named_gaps.append((no, norm(qm[0])))
                else:
                    named_gaps.append((no, norm(s)[:24]))

    if 3 in bounds:
        i0, i1 = bounds[3]
        sec3 = '\n'.join(lines[i0 + 1:i1])
        norm3 = norm(sec3)
        if not re.search(r'JD.*?(无证据|未取到|缺)|简历.*?JD.*?不关心', sec3):
            add('E-COVERAGE', '两栏', i0 + 1, '第三节没分两栏（规格：JD 有要求而简历无证据的、简历有内容而 JD 不关心的，两栏都要点名；一栏没有也要明写没有）')
        for no, key in named_gaps:
            if key and key[:16] not in norm3:
                add('E-COVERAGE', '缺口点名', no, '第二节判为无证据的那条要求没在第三节点名（规格：判缺就必须在缺口那一栏留名，不留名等于悄悄丢一条）')
    for i, ln in enumerate(lines, 1):
        if PLACE_RE.search(ln):
            continue
        m = RANK_RE.search(ln)
        if m:
            add('E-RANK', '人评断言', i, '命中「%s」（规格：本件只做要求与证据的双向核对，不排序、不打分、不说录不录；要写就同行挂 [待人工]）' % m.group(0))
            continue
        authorial = QUOTE_RE.sub('', ln)
        sm, cm = SUPER_RE.search(authorial), CONCL_RE.search(authorial)
        if sm and cm:
            add('E-RANK', '描述式名次', i, '作者句子里「%s」与「%s」同句——这是换了说法的名次，挂 [S#] 也不放行（规格：本件不替用户排先后；要留这个判断就同行挂 [待人工]）' % (sm.group(0), cm.group(0)))
    return issues, lines, unverifiable


def run_one(path: Path, jd=None, resume=None, quiet=False):
    jd_text, resume_text = load(jd), load(resume)
    for label, val in (('JD 原文', jd), ('简历原文', resume)):
        if val is not None and val is False:
            print('取值域故障：%s 读不到 %s（这一道不因此算通过，也不算违例）' % (label, val if val else ''))
            return 3, 0, 0
    issues, lines, unverifiable = scan(path, jd_text if jd_text not in (None, False) else None,
                                       resume_text if resume_text not in (None, False) else None)
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
    print('PASS: %s（四节齐、双锚回得到来源、要求与证据都逐字在原文里、两栏缺口都点名、人评断言零命中）' % path.name)
    print('       扫过 %d 行，发条 0 条，不可判 %d 项；判定与阈值全集以本脚本现值为准（--help 看五道说明）'
          % (len(lines), len(unverifiable)))
    return 0, 0, len(unverifiable)


codes_doc = {'E-FORMAT': '道一 形制与条数带', 'E-ANCHOR': '道二 双锚与来源定位',
             'E-QUOTE': '道三 要求与证据逐字回两侧原文', 'E-COVERAGE': '道四 两栏缺口点名',
             'E-RANK': '道五 录用与排序断言零命中'}

FX = Path(__file__).resolve().parent / 'fixtures'
CASES = [('good-fit.md', 0, None),
         ('bad-format.md', 1, 'E-FORMAT'),
         ('bad-no-anchor.md', 1, 'E-ANCHOR'),
         ('bad-invented-evidence.md', 1, 'E-QUOTE'),
         ('bad-missing-gap.md', 1, 'E-COVERAGE'),
         ('bad-hire-verdict.md', 1, 'E-RANK'),
         ('bad-concl-structure.md', 1, 'E-FORMAT'),
         ('bad-concl-quote.md', 1, 'E-RANK')]


def selftest(jd, resume):
    bad = 0
    for name, want_rc, want_code in CASES:
        p = FX / name
        if not p.is_file():
            print('  取值域故障：夹具不在场 %s（不读成「零违例」）' % name)
            return 3
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc, _, _ = run_one(p, jd, resume)
        detail = buf.getvalue()
        codes = sorted(set(re.findall(r'E-[A-Z]+', detail)))
        injected = detail.strip() != '' or rc != 0
        if rc != want_rc:
            print('  不合 %s：期望退码 %d，实发 %d（注入生效=是）' % (name, want_rc, rc))
            bad += 1
            continue
        if want_code and codes != [want_code]:
            print('  不合 %s：期望只发 %s，实发码集=%s（注入生效=%s）' % (
                name, want_code, '、'.join(codes) or '空', '是' if injected else '否（空注入，读数作废）'))
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
    ap = argparse.ArgumentParser(prog='check_fit.py', description=__doc__, add_help=False)
    ap.add_argument('report', nargs='?', help='要校的核对报告')
    ap.add_argument('--jd', help='JD 原文（本地文件；给了才能判要求那句逐字）')
    ap.add_argument('--resume', help='简历原文（本地文件；给了才能判证据那句逐字）')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--quiet', action='store_true', help='只报末行与计数')
    ap.add_argument('-h', '--help', action='store_true')
    a = ap.parse_args()
    if a.help or (not a.report and not a.selftest):
        print(__doc__)
        return 0 if a.help else 2
    if a.selftest:
        jd = a.jd or str(FX / 'target-jd.md')
        resume = a.resume or str(FX / 'target-resume.md')
        if not (Path(jd).is_file() and Path(resume).is_file()):
            print('取值域故障：自测要的两枚原文不在场（%s／%s）' % (jd, resume))
            return 3
        return selftest(jd, resume)
    p = Path(a.report)
    if not p.is_file():
        print('取值域故障：读不到报告文件 %s（不当「零违例」读）' % p)
        return 3
    rc, _, _ = run_one(p, a.jd, a.resume, quiet=a.quiet)
    return rc


if __name__ == '__main__':
    sys.exit(main())
