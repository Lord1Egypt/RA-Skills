#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""商誉减值风险台账·五道机检（零网络、纯标准库）。

    python3 -B scripts/check_goodwill.py <台账.md>
    python3 -B scripts/check_goodwill.py --selftest        # 好样必过、坏样各发其码

退码：0＝全过；1＝有发红；3＝取值域故障（文件不存在／不像台账）

五道：GW-STRUCT 形制｜GW-QUOTE 原句与锚｜GW-LINE 红线｜GW-GAP 未取到与不得自算｜GW-BOUND 边界
本件卖的是「这枚数字回得到那一句」，所以 GW-GAP 第三条判逐字在场，不判数值相等。
"""
import re
import sys
from pathlib import Path

SECTIONS = ('一', '二', '三', '四', '五', '六', '七', '八')
SEC_TITLE = {
    '一': '头部申报', '二': '商誉余额', '三': '业绩承诺完成度', '四': '减值测试关键假设',
    '五': '计提与未计提', '六': '未取到清单', '七': '来源', '八': '待人工',
}

# 四类数据行的行首与必备要素（形制判据）
ROW_KINDS = {
    '余额': ('标的', '期末余额', '期初余额', '口径'),
    '承诺': ('标的', '承诺期', '承诺数', '实现数', '完成率', '口径'),
    '假设': ('标的', '预测期', '折现率', '增长率'),
    '计提': ('标的', '本次计提金额', '计提比例', '累计计提', '账面余额'),
}
ROW_SEC = {'余额': '二', '承诺': '三', '假设': '四', '计提': '五'}

MISSING_WORD = '未取到'
QUOTE = re.compile(r'「([^」]*)」')
ANCHOR = re.compile(r'锚[：:]\s*(\S[^\n]*)')
SREF = re.compile(r'\[S(\d+)\]')
SRC_LINE = re.compile(r'^\s*[-*]\s*\[S(\d+)\]\s*(.+)$', re.M)
URL = re.compile(r'https?://\S+')
DATECN = re.compile(r'\d{4}-\d{2}-\d{2}')
HEAD_CNT = re.compile(r'共\s*(\d+)\s*项[·・\s]*未取到\s*(\d+)\s*项')
HEAD_CALIBER = re.compile(r'^[-*]?\s*减值口径[：:]')

# 带单位的金额／百分比（GW-GAP 第三条要逐字回到本行原句）
AMOUNT = re.compile(r'\d[\d,]*(?:\.\d+)?\s*(?:万元|亿元|元)')
PCT = re.compile(r'\d[\d,]*(?:\.\d+)?\s*%')


def tok_in_quote(tok, quote_txt):
    """金额／百分比是否以**完整词元**出现在原句里（不是裸子串命中）。

    裸 `tok in quote_txt` 会把 `200.00 万元` 认成在场——它只是 `1,200.00 万元` 的后缀。
    边界规则：命中处前一位不得是数字或小数点；前一位是半角逗号且再往前还是数字／逗号时，
    那是千分位，同样不算边界（`200.00 万元` 对 `1,200.00 万元` ⇒ 不在场）。
    后一位不得是数字或小数点，否则本次命中只是更长数字的前缀。
    """
    for m in re.finditer(re.escape(tok), quote_txt):
        start, end = m.start(), m.end()
        if start > 0:
            prev = quote_txt[start - 1]
            if prev.isdigit() or prev == '.':
                continue
            if prev == ',':
                back = start - 2
                if back >= 0 and (quote_txt[back].isdigit()
                                  or quote_txt[back] == ','):
                    continue              # 千分位逗号：本次命中从数字中间开始
        if end < len(quote_txt):
            nxt = quote_txt[end]
            if nxt.isdigit() or nxt == '.':
                continue
        return True
    return False


# 红线（GW-LINE）：一律零命中。分组是为了报错时说清犯了哪条。
REDLINE = [
    ('会不会减值', re.compile(r'(会|可能|将要?|必然|大概率)\s*减值|减值压力(大|较大)|存在减值风险|商誉高估|有减值风险')),
    ('计提是否充分', re.compile(r'计提(充分|不足|不够|不充分)|减值(充分|不足|不充分)|该计提未计提')),
    ('评级与目标价', re.compile(r'(买入|增持|减持|卖出)\s*评级|目标价|评级为')),
    ('股价预测', re.compile(r'(利好|利空|拖累|推升|拉高)\s*股价|股价(将|会|有望)|预计涨|预计跌')),
    ('收益承诺', re.compile(r'(保证|承诺)(收益|回报)|稳赚|保本')),
    ('代办', re.compile(r'代为?(出具|申报|回复|会计处理|核算)|替你(算|申报)')),
]
# 免责话只管自己那一分句：同一行后半的断言照发。按分号／句号／逗号切段。
CLAUSE_SPLIT = re.compile(r'[；;。，,\n]')
DISCLAIM = ('不构成', '不提供', '不判断', '不预测', '不评价', '不含', '不做', '不给出', '不判', '不评')

# GW-GAP 第二条：替披露下结论的写法
SUBSTITUTE = re.compile(r'无减值|不存在减值|不适用|无需计提|不计提')

# GW-BOUND：别的件的活
BOUND_RULE = [
    ('cn-restructuring-tracker', re.compile(r'重组|对价|交易作价|支付方式|标的资产作价')),
    ('cn-earnings-note', re.compile(r'财报点评|业绩点评|营业收入|归母净利润|毛利率')),
]
BOUND_ROW = {'交易对价', '支付方式', '标的资产作价', '营业收入', '归母净利润'}


def split_sections(text):
    """按 `## N. …` 或 `## 一、…` 取节。返回 {key: [lines]}，
    key 优先取中文章号（一二三…），没有则按序号 1..8 映射。"""
    out = {}
    cur = None
    order = []
    for ln in text.splitlines():
        m = re.match(r'^#{1,4}\s*(?:(\d+)[.、]\s*|([一二三四五六七八])[、.]\s*)', ln)
        if m:
            num, cn = m.group(1), m.group(2)
            if cn:
                cur = cn
            elif num and 1 <= int(num) <= 8:
                cur = SECTIONS[int(num) - 1]
            else:
                cur = None
            if cur:
                out.setdefault(cur, [])
                order.append(cur)
            continue
        if ln.startswith('#') and not ln.startswith('##'):
            cur = None  # 一级标题切段
            continue
        if cur:
            out[cur].append(ln)
    return out


def find_caliber_line(text):
    for ln in text.splitlines():
        if HEAD_CALIBER.match(ln.strip()):
            return ln.strip()
    return None


def clause_of(line, word):
    """免责话所在的**那一个分句**里，红线词不算（只管自己那一分句）。"""
    segs = CLAUSE_SPLIT.split(line)
    return [s for s in segs if not any(d in s for d in DISCLAIM)]


def check(text):
    f = []          # (code, lineno, msg)
    lines = text.splitlines()
    secs = split_sections(text)

    # ---------- GW-STRUCT 道一 形制 ----------
    for s in SECTIONS:
        if s not in secs:
            f.append(('GW-STRUCT', 0, '缺第八节之一：第%s节（%s）不在场' % (s, SEC_TITLE[s])))
    cal = find_caliber_line(text)
    if cal is None:
        f.append(('GW-STRUCT', 0, '头部缺 `减值口径：` 行（本件与重组/财报点评的分界，机检按它判边界）'))

    # 头部「共 N 项·未取到 M 项」全文恰一处
    cnt_hits = [(i + 1, m) for i, ln in enumerate(lines) for m in [HEAD_CNT.search(ln)] if m]
    if not cnt_hits:
        f.append(('GW-STRUCT', 0, '头部缺 `共 N 项·未取到 M 项` 申报行'))
    elif len(cnt_hits) > 1:
        f.append(('GW-STRUCT', cnt_hits[1][0],
                  '`共 N 项·未取到 M 项` 出现 %d 处（全文只准一处）：行 %s'
                  % (len(cnt_hits), ','.join(str(c[0]) for c in cnt_hits))))

    # 四类数据行：行级在场 + 各节至少一行 + 要素齐
    rows = []       # (kind, lineno, body, section)
    for i, ln in enumerate(lines, 1):
        for kind in ROW_KINDS:
            if re.match(r'^\s*[-*]\s*%s[：:]' % kind, ln):
                sec = None
                for s, body in secs.items():
                    if ln in body:
                        sec = s
                        break
                rows.append((kind, i, ln.strip(), sec))
                break
    for kind, sec in ROW_SEC.items():
        got = [r for r in rows if r[0] == kind]
        if not got:
            f.append(('GW-STRUCT', 0, '缺 `- %s：` 行级形制（散文里提到不算一行）' % kind))
        elif not any(r[3] == sec for r in got):
            f.append(('GW-STRUCT', 0, '`- %s：` 行没有落在第%s节（%s）'
                      % (kind, sec, SEC_TITLE[sec])))

    for kind, i, body, sec in rows:
        if MISSING_WORD in body:
            continue                       # 未取到形，要素豁免，由 GW-GAP 对账
        for field in ROW_KINDS[kind]:
            if not re.search(r'%s[：:]' % re.escape(field), body):
                f.append(('GW-STRUCT', i, '%s行要素缺 `%s：`' % (kind, field)))

    # ---------- GW-QUOTE 道二 原句与锚 ----------
    for kind, i, body, sec in rows:
        if MISSING_WORD in body:
            continue
        q = QUOTE.search(body)
        if not q:
            f.append(('GW-QUOTE', i, '%s行缺「」原句' % kind))
        elif len(q.group(1).strip()) < 2:
            f.append(('GW-QUOTE', i, '%s行原句过短（＜2 字），不是逐字抄录' % kind))
        a = ANCHOR.search(body)
        if not a or not a.group(1).strip():
            f.append(('GW-QUOTE', i, '%s行 `锚：` 缺位或为空' % kind))
        if not SREF.search(body):
            f.append(('GW-QUOTE', i, '%s行行末缺 `[S#]`' % kind))

    src = {}
    for s in SRC_LINE.finditer(text):
        src.setdefault(s.group(1), []).append(s.group(2))
    used = set()
    for kind, i, body, sec in rows:
        for s in SREF.finditer(body):
            used.add(s.group(1))
            if s.group(1) not in src:
                f.append(('GW-QUOTE', i, '正文引用 [S%s] 在第七节无对应行' % s.group(1)))
    for sid, bodies in sorted(src.items(), key=lambda x: int(x[0])):
        if len(bodies) > 1:
            f.append(('GW-QUOTE', 0, '第七节 [S%s] 出现 %d 次（编号须唯一）' % (sid, len(bodies))))
        b = bodies[0]
        if not URL.search(b):
            f.append(('GW-QUOTE', 0, '第七节 [S%s] 缺 URL' % sid))
        if not DATECN.search(b):
            f.append(('GW-QUOTE', 0, '第七节 [S%s] 缺 `YYYY-MM-DD` 检索日' % sid))

    # ---------- GW-LINE 道三 红线 ----------
    for i, ln in enumerate(lines, 1):
        if not ln.strip() or SRC_LINE.match(ln):
            continue
        for label, pat in REDLINE:
            for seg in clause_of(ln, label):
                m = pat.search(seg)
                if m:
                    f.append(('GW-LINE', i, '红线「%s」命中：%s' % (label, m.group(0)[:24])))
                    break

    # ---------- GW-GAP 道四 未取到与不得自算 ----------
    # ① 两向对账：N＝四节数据行总数，M＝写未取到的行数
    data_rows = [r for r in rows if r[0] in ROW_SEC]
    miss_rows = [r for r in data_rows if MISSING_WORD in r[2]]
    if cnt_hits:
        m0 = cnt_hits[0][1]
        n_decl, m_decl = int(m0.group(1)), int(m0.group(2))
        if n_decl != len(data_rows):
            f.append(('GW-GAP', cnt_hits[0][0],
                      '申报 N=%d ≠ 四节数据行实到 %d（多报是虚报、少报是漏报，两向都发）'
                      % (n_decl, len(data_rows))))
        if m_decl != len(miss_rows):
            f.append(('GW-GAP', cnt_hits[0][0],
                      '申报 M=%d ≠ 正文写未取到的行数 %d' % (m_decl, len(miss_rows))))
    # 第六节逐条点名 vs 正文未取到行：两向
    sec6 = '\n'.join(secs.get('六', []))
    for kind, i, body, sec in miss_rows:
        key = re.search(r'%s[：:]\s*(.*)$' % kind, body)
        tail = (key.group(1) if key else '').replace(MISSING_WORD, '').strip()
        tail = re.sub(r'（[^）]*）', '', tail).strip()
        if tail and tail not in sec6:
            f.append(('GW-GAP', i, '%s行未取到的项「%s」未在第六节点名' % (kind, tail[:20])))
    # ② 替披露下结论
    for i, ln in enumerate(lines, 1):
        if MISSING_WORD in ln:
            continue
        for seg in clause_of(ln, ''):
            m = SUBSTITUTE.search(seg)
            if m:
                f.append(('GW-GAP', i, '替披露下结论「%s」（未披露只能写未取到）' % m.group(0)))
                break
    # ③ 金额与百分比必须逐字在本行原句里——本件最要紧的一格
    for kind, i, body, sec in rows:
        if MISSING_WORD in body:
            continue
        q = QUOTE.search(body)
        if not q:
            continue                        # 无原句已由 GW-QUOTE 发，此处不重复
        quote_txt = q.group(1)
        for m in list(AMOUNT.finditer(body)) + list(PCT.finditer(body)):
            tok = m.group(0)
            if tok_in_quote(tok, quote_txt):
                continue
            # 允许原句里同一数的另一种写法？不允许：本件判逐字在场。
            f.append(('GW-GAP', i, '%s行 `%s` 不在本行原句里（卡面自算或换算）' % (kind, tok)))

    # ---------- GW-BOUND 道五 边界 ----------
    if cal is not None:
        body_cal = cal.split('：', 1)[-1].split(':', 1)[-1]
        if not body_cal.strip().startswith('商誉科目'):
            f.append(('GW-BOUND', 0, '`减值口径：` 须以「商誉科目」起头（现值：%s）' % body_cal.strip()[:30]))
        for target, pat in BOUND_RULE:
            if pat.search(body_cal):
                f.append(('GW-BOUND', 0,
                          '`减值口径：` 写成了本件域外口径（命中「%s」）——该走 %s'
                          % (pat.search(body_cal).group(0), target)))
    for i, ln in enumerate(lines, 1):
        m = re.match(r'^\s*[-*]\s*([^：:]{2,12})[：:]', ln)
        if m and m.group(1).strip() in BOUND_ROW:
            target = 'cn-restructuring-tracker' if m.group(1).strip() in (
                '交易对价', '支付方式', '标的资产作价') else 'cn-earnings-note'
            f.append(('GW-BOUND', i, '出现域外项行 `- %s：`——该走 %s' % (m.group(1).strip(), target)))

    return f, secs, rows, data_rows, miss_rows, src


def report(f, rows, data_rows, miss_rows, src):
    for code, ln, msg in f:
        where = '行 %d' % ln if ln else '全局'
        print('FAIL %s｜%s｜%s' % (code, where, msg))
    codes = {}
    for code, _, _ in f:
        codes[code] = codes.get(code, 0) + 1
    print('----')
    print('数据行 %d｜未取到 %d｜来源 %d 条｜发红 %d' % (len(data_rows), len(miss_rows), len(src), len(f)))
    print('按道：' + ('｜'.join('%s=%d' % (k, codes[k]) for k in sorted(codes)) if codes else '无'))
    return 1 if f else 0


def selftest(root):
    fix = root / 'scripts' / 'fixtures'
    good = fix / 'good-goodwill-ledger.md'
    if not good.is_file():
        print('取值域故障：好样不在 %s' % good)
        return 3
    bad_files = sorted(fix.glob('bad-*.md'))
    rc_all = 0
    # 好样必过
    t = good.read_text(encoding='utf-8')
    f, secs, rows, dr, mr, src = check(t)
    ok = (len(f) == 0)
    print('%s 好样 %s｜数据行 %d 未取到 %d 来源 %d' %
          ('ok  ' if ok else 'FAIL', good.name, len(dr), len(mr), len(src)))
    if not ok:
        report(f, rows, dr, mr, src)
        rc_all = 1
    # 注入档（金额词元边界）：把好样的「本次计提金额」改成 200.00 万元，原句一字不动。
    # 裸子串会把「200.00 万元」认成在「1,200.00 万元」里在场——字符在场 ≠ 金额词元在场。
    needle = '本次计提金额：1,200.00 万元｜'
    if needle not in t:
        raise RuntimeError('夹具注入点对不上：%r' % needle)
    f_sub = check(t.replace(needle, '本次计提金额：200.00 万元｜', 1))[0]
    codes_sub = set(c for c, _, _ in f_sub)
    if codes_sub == {'GW-GAP'} and len(f_sub) == 1:
        print('ok   注入档 金额后缀子串（200.00 万元 / 原句 1,200.00 万元）只发 GW-GAP（共 %d 条）'
              % len(f_sub))
    else:
        print('FAIL 注入档 金额后缀子串：期望只发 {GW-GAP}，实发 %s' % (sorted(codes_sub) or '无'))
        rc_all = 1
    # 词元边界单测：后缀与千分位前缀都不得算在场，整词必须算在场。
    boundary = [
        ('200.00 万元', '1,200.00 万元', False),
        ('1,200.00 万元', '11,300.00 万元', False),
        ('1,200.00 万元', '11,300.00 万元、1,200.00 万元', True),
        ('1,200.00 万元', '1,200.00 万元', True),
    ]
    boundary_bad = 0
    for tok, quote, want in boundary:
        got = tok_in_quote(tok, quote)
        if got != want:
            print('FAIL 词元边界：`%s` 对 `%s` 期望 %s 实得 %s' % (tok, quote, want, got))
            boundary_bad += 1
    if boundary_bad:
        rc_all = 1
    print('词元边界单测 %d 条：%s'
          % (len(boundary), '全过' if not boundary_bad else '不合 %d 条' % boundary_bad))
    # 坏样各发其码
    expect = {
        'bad-1-struct.md': 'GW-STRUCT',
        'bad-2-quote.md': 'GW-QUOTE',
        'bad-3-line.md': 'GW-LINE',
        'bad-4-gap-count.md': 'GW-GAP',
        'bad-5-self-calc.md': 'GW-GAP',
        'bad-6-bound.md': 'GW-BOUND',
    }
    seen = set()
    for bf in bad_files:
        t = bf.read_text(encoding='utf-8')
        f, secs, rows, dr, mr, src = check(t)
        codes = set(c for c, _, _ in f)
        want = expect.get(bf.name)
        if want and want in codes:
            print('ok   %s 发出 %s（共 %d 条）' % (bf.name, want, len(f)))
            seen.add(bf.name)
        else:
            print('FAIL %s 未发出期望码 %s（实发：%s）' % (bf.name, want, sorted(codes) or '无'))
            rc_all = 1
    for name in expect:
        if name not in seen:
            print('FAIL 坏样缺件：%s' % name)
            rc_all = 1
    print('----')
    print('自检：好样 %s｜坏样 %d/%d 各发其码' %
          ('过' if rc_all == 0 else '未过', len(seen), len(expect)))
    return rc_all


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 3
    if argv[1] == '--selftest':
        return selftest(Path(__file__).resolve().parent.parent)
    p = Path(argv[1])
    if not p.is_file():
        print('取值域故障：文件不存在 %s（不读成不合格）' % p)
        return 3
    text = p.read_text(encoding='utf-8', errors='ignore')
    if '商誉' not in text:
        print('取值域故障：%s 里没有「商誉」字样，不像本件台账（不读成不合格）' % p)
        return 3
    f, secs, rows, dr, mr, src = check(text)
    return report(f, rows, dr, mr, src)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
