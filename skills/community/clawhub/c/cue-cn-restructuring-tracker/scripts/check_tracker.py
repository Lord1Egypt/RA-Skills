#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_tracker.py — 校一份「并购重组跨期进度跟踪稿」是否合 `SKILL.md` §3 七节契约与 §5 红线。

用法：
    python3 check_tracker.py <跟踪稿.md>      校一份跟踪稿（纯标准库、零网络、不发任何请求）
    python3 check_tracker.py --selftest       跑包内夹具：好样必须过，五枚坏样必须各发它该发的那一道
    python3 check_tracker.py --help           本说明

出口形制（与套件姊妹件同族）：
    失败 = 一行 "FAIL: <文件>（N 条）"，其下每条详行先打错误码前缀（五枚 E-* 之一），道名后是行号与该道规格；
           末行 "码表:" 只列本次真正用到的码与含义。
    全过 = 一行 "PASS: <文件>（…）"，并印「扫过 N 行」与五道计数——计数说看到多少，不说猜多少。

五道是什么（判定全集在本脚本，本文只指路，不复述细节）：
    道一 形制：头部四件自标逐字在位＋「跟踪口径：」行在场且值可认＋七节齐且按一至七有序
                ＋一句话结论非空非占位＋三个内容节（交易概况／进度时间轴／每步变化）各至少一行
                ＋时间轴每行「日期｜节点｜事实 [S#]」三格齐、日期 YYYY-MM-DD、节点在册、
                  日期非降序、终止若出现须是最后一行
    道二 锚：时间轴与每步变化每行行末带 [S#]，且该编号在第七节有对应行；第七节每行必须同时带 URL 与
              YYYY-MM-DD 检索日；**每步变化每行至少两枚不同号的锚**——变化是两处之间的差，只指一处不构成差
    道三 红线：评级／目标价／买卖动作／涨跌承诺／过会获批概率／估值评价 一律零命中，要写只能同行挂 [待人工]；
              改数词（约／左右／大概）不得替数字打底
    道四 未取到与计数：正文写了「未取到／未检索到」的，第六节必须逐条点名它；第六节列了而正文没有这条表述的同样发
    道五 边界：跟踪口径写成「单份／条款／速读」，或时间轴不足两行＝这是条款速读的活，
              点名改走 ma-restructuring-terms-cn（八项逐字卡），不是只报形制错

退码：0 全过；1 有发条（详行逐条给码、道名、行号与规格）；2 用法错；3 取值域故障（文件读不到，不读成「零违例」）。
"""

from __future__ import annotations

import argparse
import atexit
import re
import shutil
import sys
import tempfile
from pathlib import Path

TMP_ROOTS = []


@atexit.register
def _cleanup_tmp() -> None:
    for d in TMP_ROOTS:
        shutil.rmtree(d, ignore_errors=True)


def _probe_copy(text: str) -> Path:
    d = Path(tempfile.mkdtemp(prefix='check-restructuring-tracker-', dir=tempfile.gettempdir()))
    TMP_ROOTS.append(d)
    f = d / 'probe.md'
    f.write_text(text, encoding='utf-8')
    return f


SECTIONS = ('一句话结论', '交易概况', '进度时间轴', '每步变化', '未决事项', '未取到与口径', '来源')
CN_NUM = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七'}
ALWAYS_CONTENT = (2, 3, 4)          # 交易概况／进度时间轴／每步变化：各至少一行
MARKS = ('AI 整理初稿', '请回原文核对', '不构成投资建议', '判断位 [待人工]')
URL_RE = re.compile(r'https?://|www\.[A-Za-z0-9.-]+')
DATE_RE = re.compile(r'\d{4}-\d{2}-\d{2}')
ANCHOR_RE = re.compile(r'\[S(\d+)\]\s*$')
ANY_ANCHOR_RE = re.compile(r'\[S(\d+)\]')
PLACEHOLDER_RE = re.compile(r'^\s*(（[^）]*）)?[—\-–]\s*$|待定|待填|TBD|<[^>]*>$')
SCOPE_RE = re.compile(r'^跟踪口径[：:]\s*(.+?)\s*$')

# 节点册：六个进度节点＋一个终态。**终止不是进度节点**，它是这笔交易死掉的那一格——
# 一枚记不下「终止」的时间轴不是跟踪器，所以它必须在册；但它出现即须是最后一行（见道一）。
NODES = ('停牌', '预案', '草案', '问询', '过会', '核准', '实施', '终止')
TERMINAL_NODES = ('实施', '终止')
TL_RE = re.compile(r'^[-*]\s*(\d{4}-\d{2}-\d{2})\s*[｜|]\s*([^｜|\n]+?)\s*[｜|]\s*(.+)$')

# 红线词族：只收「推荐动作」与「涨跌承诺」的确形。
# **裸「减持」不收**——锁定期与减持限制是重组文件里的事实条款（「控股股东承诺 36 个月内不减持」），
# 收进来会把正当登记判红；要禁的是「建议减持」这种推荐语。裸「评级」同样不收：
# 「主体信用评级 AA+」是事实陈述，收进来会假红；只收「投资评级／券商评级／评级为／上调评级」这类评价形。
BANNED = re.compile(r'买入|卖出|建仓|清仓|加仓|减仓|目标价|止盈|止损|必涨|必跌|稳赚|无风险'
                    r'|强烈推荐|建议买入|建议卖出|建议增持|建议减持|翻倍|跑赢大盘'
                    r'|严重低估|严重高估|值得买入|可以买入'
                    r'|必能过会|过会无虞|大概率过会|必获核准')
RATING_VALUE = r'(?:买入|增持|推荐|强烈推荐|优于大市|跑赢行业|中性|持有|观望|减持|卖出|回避)'
RATING_FORM = re.compile(r'(?:投资评级|券商评级|机构评级|股票评级)[^。；\n]{0,6}?' + RATING_VALUE
                         + r'|评级(?:为|：|:)\s*' + RATING_VALUE
                         + r'|(?:上调|下调|维持)[^。；\n]{0,4}评级')
# 主题×语气两支：评价词后接「性·度·论」时那是被说明的对象、不是本件下的评价断言
# （「说明定价的合理性」「估值充分性说明待补充」都不发红）——这一份排除同时喂两支，不留双份真值。
EVAL_WORD = r'(?:合理|公允|偏低|偏高|充分|审慎)'
EVAL_EXCL = r'(?![性度论])'
TOPIC_EVAL = re.compile(r'(?:估值|评估值|定价|作价|对价)[^。；\n]{0,6}?' + EVAL_WORD + EVAL_EXCL)
PROB_TOPIC = re.compile(r'(?:过会|获批|核准|注册生效|通过)[^。；\n]{0,6}?(?:概率|可能性)[^。；\n]{0,4}?(?:大|高|很小|极低)')
HEDGE = re.compile(r'约\s*[\d０-９]|左右|大概|大约')
CODES = {'E-FORMAT': '道一 形制', 'E-ANCHOR': '道二 锚', 'E-BANWORD': '道三 红线',
         'E-COVERAGE': '道四 未取到与计数', 'E-SCOPE': '道五 边界'}


def scan(path: Path):
    issues = []
    seen = set()

    def add(code, lane, line_no, msg):
        key = (code, line_no, msg)
        if key not in seen:
            seen.add(key)
            issues.append((code, lane, line_no, msg))

    lines = path.read_text(encoding='utf-8', errors='replace').split('\n')
    first_h2 = next((i for i, ln in enumerate(lines) if ln.startswith('## ')), len(lines))
    head = '\n'.join(lines[:first_h2])

    # ---- 道一 头部自标 ----
    for need in MARKS:
        if need not in head:
            add('E-FORMAT', '头部', 1, f"头部自标缺『{need}』（规格：四件逐字齐，写在第一个「## 」之前）")

    # ---- 道一／道五 跟踪口径 ----
    st = None
    for i in range(first_h2):
        m = SCOPE_RE.match(lines[i].strip())
        if m:
            st = (i, m.group(1))
            break
    if st is None:
        add('E-FORMAT', '跟踪口径', 1,
            '头部缺「跟踪口径：」行（规格：本件只做跨期跟踪，这一格是它与条款速读的分界，必须自报）')
    else:
        i, v = st
        if any(k in v for k in ('单份', '条款', '速读')):
            add('E-SCOPE', '边界', i + 1,
                f'跟踪口径写的是「{v}」——单份重组文件的条款速读走 ma-restructuring-terms-cn（八项逐字卡），'
                '本件的时间轴框架不适用；要么改走那一件，要么把同一笔交易的多份公告凑齐再跑')
        elif '跨期' not in v:
            add('E-FORMAT', '跟踪口径', i + 1,
                f'跟踪口径「{v}」认不出（规格：以「跨期」起头，如「跨期（同一笔交易的多份公告按时间轴串起来）」）')

    # ---- 道一 七节齐且有序 ----
    idxs = []
    for n, name in enumerate(SECTIONS, 1):
        hit = [i for i, ln in enumerate(lines) if re.match(rf'^##\s*{CN_NUM[n]}、{re.escape(name)}\s*$', ln)]
        if not hit:
            add('E-FORMAT', '七节', 1, f"缺「## {CN_NUM[n]}、{name}」段（规格：七节齐且按一至七有序）")
        else:
            idxs.append((n, hit[0]))
    if len(idxs) > 1 and [n for n, _ in idxs] != sorted(n for n, _ in idxs):
        add('E-FORMAT', '七节', idxs[0][1] + 1, '七节次序与契约不一致（规格：一至七有序）')
    bounds = {}
    for pos, (n, i0) in enumerate(idxs):
        i1 = idxs[pos + 1][1] if pos + 1 < len(idxs) else len(lines)
        bounds[n] = (i0, i1)

    # ---- 道一 结论非空非占位 ----
    if 1 in bounds:
        i0, i1 = bounds[1]
        # 带真实行号走：过滤掉空行与标题行后，列表下标 ≠ 文件行号，用 index 定位会错位。
        body = [(i, lines[i]) for i in range(i0 + 1, i1)
                if lines[i].strip() and not lines[i].startswith('#')]
        if not body:
            add('E-FORMAT', '结论', i0 + 1, '一句话结论留空（规格：至少一行实句，不留占位）')
        else:
            bad = next(((i, ln) for i, ln in body if PLACEHOLDER_RE.search(ln)), None)
            if bad is not None:
                add('E-FORMAT', '结论', bad[0] + 1,
                    '一句话结论仍是占位（规格：写成可核的实句；判断走 [待人工]，不靠占位）')

    # ---- 道一 时间轴形制（日期／节点／次序／终态） ----
    tl_rows = []          # [(行号, 日期, 节点, 行文本)]
    if 3 in bounds:
        i0, i1 = bounds[3]
        for i in range(i0 + 1, i1):
            ln = lines[i]
            if not ln.strip().startswith(('-', '*')):
                continue
            m = TL_RE.match(ln.strip())
            if not m:
                add('E-FORMAT', '时间轴', i + 1,
                    '时间轴行不是「日期｜节点｜事实」三格（规格：`- YYYY-MM-DD｜节点｜一句话事实 [S#]`）')
                continue
            d, node, rest = m.group(1), m.group(2).strip(), m.group(3)
            if node not in NODES:
                add('E-FORMAT', '时间轴', i + 1,
                    f'节点「{node}」不在册（在册＝{"／".join(NODES)}；'
                    '「终止」是终态不是进度节点，出现即须是最后一行）')
            tl_rows.append((i + 1, d, node, rest))
        dates = [d for _, d, _, _ in tl_rows]
        for k in range(1, len(dates)):
            if dates[k] < dates[k - 1]:
                add('E-FORMAT', '时间轴', tl_rows[k][0],
                    f'日期倒序：{dates[k]} 排在 {dates[k - 1]} 之后（规格：时间轴按日期非降序——'
                    '倒序的时间轴不是时间轴）')
        for k, (no, _d, node, _r) in enumerate(tl_rows):
            if node == '终止' and k != len(tl_rows) - 1:
                add('E-FORMAT', '时间轴', no,
                    '「终止」不是最后一行（规格：终止是终态，出现即须是最后一行——'
                    '终止之后还有节点，说明这一行不是终止，或者时间轴混进了另一笔交易）')
        if len(tl_rows) < 2:
            add('E-SCOPE', '边界', (bounds[3][0] + 1) if 3 in bounds else 1,
                f'时间轴只有 {len(tl_rows)} 行——只有一份公告＝条款速读的活，不是跨期跟踪；'
                '改走 ma-restructuring-terms-cn（八项逐字卡），或把同一笔交易的多份公告凑齐再跑')

    # ---- 道一 内容节各至少一行（未决事项在终态下可空） ----
    last_node = tl_rows[-1][2] if tl_rows else None
    for n in ALWAYS_CONTENT:
        if n not in bounds:
            continue
        i0, i1 = bounds[n]
        rows = [ln for ln in lines[i0 + 1:i1] if ln.strip() and not ln.startswith('#')]
        if not rows:
            add('E-FORMAT', '内容节', i0 + 1,
                f'「{SECTIONS[n - 1]}」整节为空（规格：三个内容节各至少一行——'
                '没有时间轴的跟踪稿不是跟踪稿）')
    if 5 in bounds and last_node not in TERMINAL_NODES:
        i0, i1 = bounds[5]
        rows = [ln for ln in lines[i0 + 1:i1] if ln.strip() and not ln.startswith('#')]
        if not rows:
            add('E-FORMAT', '内容节', i0 + 1,
                f'「未决事项」整节为空，而时间轴最后一格是「{last_node}」——'
                '交易还没走到实施或终止，就一定有未决事项；空节等于把卡点藏起来'
                '（走到实施或终止后本格可空，那是设计）')

    # ---- 道二 锚 ----
    anchors_used, listed = [], set()
    for n in (3, 4):
        if n not in bounds:
            continue
        i0, i1 = bounds[n]
        for i in range(i0 + 1, i1):
            ln = lines[i]
            if not ln.strip().startswith(('-', '*')):
                continue
            m = ANCHOR_RE.search(ln.strip())
            if not m:
                add('E-ANCHOR', '锚', i + 1,
                    '行末没有 [S#] 锚（规格：时间轴与每步变化每行行末带一个锚；没有锚就不要写进这两节）')
            else:
                anchors_used.append((int(m.group(1)), i + 1))
            if n == 4:
                nums = sorted({int(x) for x in ANY_ANCHOR_RE.findall(ln)})
                if len(nums) < 2:
                    add('E-ANCHOR', '变化锚', i + 1,
                        f'每步变化这一行只有 {len(nums)} 枚不同号的锚（规格：至少两枚——'
                        '变化是两处之间的差，只指一处不构成差；前后两值各挂它自己那一处公告）')
                if '→' not in ln:
                    add('E-FORMAT', '变化形', i + 1,
                        '每步变化这一行没有「→」（规格：`- 变化项：前值 → 后值 [S#][S#]`——'
                        '变化要写成前后两值，不写成一句叙述）')
            if HEDGE.search(ln):
                add('E-BANWORD', '改数', i + 1,
                    f"命中改数词「{HEDGE.search(ln).group(0)}」（规格：数值要么照公告写，要么落第六节写未取到，"
                    '不用约／左右打底）')

    if 7 in bounds:
        i0, i1 = bounds[7]
        # 带真实行号走：来源行可能逐字重复（同一份公告挂两次），用 .index(ln) 会全部指到第一行。
        rows = [(i, lines[i]) for i in range(i0 + 1, i1) if lines[i].strip().startswith(('-', '*'))]
        if not rows:
            add('E-COVERAGE', '来源', i0 + 1, '第七节一行来源都没有（规格：逐条挂源的价值就在这一节，空节等于没有出处）')
        for k, (i, ln) in enumerate(rows, 1):
            no = i + 1
            m = re.match(r'^[-*]\s*\[S(\d+)\]', ln.strip())
            if not m:
                add('E-ANCHOR', '来源', no, f'来源第 {k} 行不以 [S#] 开头（规格：编号与正文锚一一对应）')
            else:
                listed.add(int(m.group(1)))
            if not URL_RE.search(ln):
                add('E-ANCHOR', '来源', no,
                    f'来源 [S{m.group(1) if m else k}] 缺 URL（规格：逐条可回查——域名或链接原样写进同一行）')
            if not DATE_RE.search(ln):
                add('E-ANCHOR', '来源', no,
                    f'来源 [S{m.group(1) if m else k}] 缺检索日 YYYY-MM-DD（规格：跨期跟踪的时效以检索日为凭）')
    for num, ln_no in anchors_used:
        if num not in listed:
            add('E-ANCHOR', '锚', ln_no, f'锚 [S{num}] 在第七节没有对应行（规格：正文用的每个编号都要能回到来源行）')

    # ---- 道三 红线 ----
    for i, ln in enumerate(lines, 1):
        if '[待人工]' in ln:
            continue
        for pat, label in ((BANNED, '判断词'), (RATING_FORM, '评级形'), (TOPIC_EVAL, '估值评价'), (PROB_TOPIC, '过会概率')):
            m = pat.search(ln)
            if m:
                add('E-BANWORD', label, i,
                    f"命中「{m.group(0)}」（规格：评级／目标价／买卖动作／涨跌承诺／过会获批概率／估值评价"
                    '本件不产出；要写就同行挂 [待人工]，或改中性陈述）')

    # ---- 道四 未取到两向点名 ----
    MISS_WORD = re.compile(r"未取到|未检索到|没取到|没检索到")
    STOP_TOK = {"它", "这", "该", "其", "本节", "来源", "渠道", "本条", "该项", "本次"}
    # 名目「同指」判：先剥括号注与标点，再按核心名词短语判——字面全等算同指；一方含另一方且短的一方 ≥4 字算同指；
    # 否则取汉字集合的 Jaccard ≥ SAME_REF_MIN 算同指。阈值写在这里、由自测的三形钉死，不按文体特例放宽。
    SAME_REF_MIN = 0.6
    PUNCT_STRIP = re.compile(r"[^一-龥A-Za-z0-9]")

    def core(tok):
        return PUNCT_STRIP.sub("", re.sub(r"[（(][^）)]*[）)]", "", tok))

    def same_ref(a, b):
        ca, cb = core(a), core(b)
        if not ca or not cb:
            return False
        if ca == cb:
            return True
        if (ca in cb or cb in ca) and min(len(ca), len(cb)) >= 4:
            return True
        sa, sb = set(ca), set(cb)
        return len(sa & sb) / len(sa | sb) >= SAME_REF_MIN

    def refs(tok, pool):
        return any(same_ref(tok, other) for other in pool)

    def miss_tokens(seg_lines):
        out = []
        for off, ln in seg_lines:
            if ln.strip().startswith("#") or not MISS_WORD.search(ln):
                continue
            # 后置形只认「未取到：X」与「未取到X」两种——**逗号不算分隔符**：
            # 「分品类收入未取到，本期无定期报告」里逗号后面是原因从句，不是名目；
            # 把逗号当分隔符会把整句原因抓成名目，于是好样被判「第六节多列一项」。
            for m in re.finditer(r"(?:未取到|未检索到|没取到|没检索到)[：:\s]*([^\s，。；、：:｜\[\]（）()「」【】\n]{3,24})", ln):
                tok = m.group(1)
                if tok not in STOP_TOK:
                    out.append((tok, off))
            for m in re.finditer(r"([^\s，。；、：:｜\[\]（）()「」【】\n]{3,24}?)(?:未取到|未检索到|没取到|没检索到)", ln):
                tok = m.group(1)
                if tok not in STOP_TOK:
                    out.append((tok, off))
        return out

    body_seg = [(i, lines[i]) for n, (a, b) in bounds.items() if n != 6 for i in range(a + 1, b)]
    sec6_seg = [(i, lines[i]) for i in range(bounds[6][0] + 1, bounds[6][1])] if 6 in bounds else []
    body_toks = [tok for tok, _ in miss_tokens(body_seg)]
    sec6_toks = [tok for tok, _ in miss_tokens(sec6_seg)]
    for tok, no in miss_tokens(body_seg):
        if not refs(tok, sec6_toks):
            add("E-COVERAGE", "未取到点名", no + 1,
                f"第六节的点名缺一项：正文写了「{tok}」未取到，第六节没有同指的名目"
                "（规格：没列就是没说——逐条点名按名目同指对，不认整节出现过一个「未取到」）")
    for tok, no in miss_tokens(sec6_seg):
        if not refs(tok, body_toks):
            add("E-COVERAGE", "未取到点名", no + 1,
                f"第六节多列一项：「{tok}」在第六节点名为未取到，正文没有同指的这条表述"
                "（规格：反向同判——多列与少列都不许）")
    return issues, lines


def run_one(path: Path, quiet=False):
    issues, lines = scan(path)
    codes = sorted({c for c, _, _, _ in issues})
    if not quiet:
        for code, lane, no, msg in issues:
            print(f"  [{code}] [{lane}] 第 {no} 行：{msg}")
    counts = {}
    for code, _, _, _ in issues:
        counts[code] = counts.get(code, 0) + 1
    if issues:
        print(f'FAIL: {path.name}（{len(issues)} 条）')
        print('       ' + '；'.join(f'{CODES[c]} {n} 条' for c, n in sorted(counts.items())))
        print('       码表: ' + '；'.join(f'{c}={CODES[c]}' for c in codes))
        return 1, len(issues), counts
    print('PASS: ' + path.name + '（七节齐、自标在位、跟踪口径为跨期、时间轴按日期非降序且节点在册、'
          '每步变化带前后两值与两处锚、来源行齐 URL 与检索日、判断词零命中、未取到逐条点名）')
    print(f'       扫过 {len(lines)} 行，发条 0 条；判定与阈值全集以本脚本现值为准（--help 看五道说明）')
    return 0, 0, {}


def selftest():
    fx = Path(__file__).resolve().parent / 'fixtures'
    cases = [('good-tracker.md', 0, None),
             ('bad-no-anchor.md', 1, 'E-ANCHOR'),
             ('bad-missing-section.md', 1, 'E-FORMAT'),
             ('bad-rating-word.md', 1, 'E-BANWORD'),
             ('bad-gap-unlisted.md', 1, 'E-COVERAGE'),
             ('bad-single-doc.md', 1, 'E-SCOPE')]
    bad = 0
    gt = (fx / 'good-tracker.md').read_text(encoding='utf-8')
    body_gap_line = '- 标的公司2025年度审计净利润未取到，公告只披露承诺数与评估值 [S3]'
    sec6_line = '- 未取到：标的公司2025年度审计净利润（公告只披露承诺数与评估值）'
    assert gt.count(body_gap_line) == 1 and gt.count(sec6_line) == 1, '夹具形制变了，反证档要跟着改'
    probes = []
    # 阈值三形钉死：字面全等与同指异词都算点到，真无关才算多列
    p0a = gt.replace(sec6_line, '- 未取到：标的公司2025年度审计净利润（公告只披露承诺数）')
    probes.append(('钉阈·字面全等（两侧都写「标的公司2025年度审计净利润」）不得报多列', p0a, '第六节多列一项', False))
    p0b = gt.replace(sec6_line, '- 未取到：标的公司2025年度审计净利润数据（公告只披露承诺数）')
    probes.append(('钉阈·同指异词（正文「…净利润」∥第六节「…净利润数据」）不得报多列', p0b, '第六节多列一项', False))
    p0c = gt.replace(sec6_line, '- 未取到：标的公司员工安置方案')
    probes.append(('钉阈·真无关（第六节只列「标的公司员工安置方案」）必须报多列', p0c, '第六节多列一项', True))
    p1 = gt.replace(body_gap_line, body_gap_line + '\n- 标的公司土地权属证明未取到 [S3]')
    probes.append(('反证·正文多写一条未取到而第六节不列｜独有句「第六节的点名缺一项」', p1, '第六节的点名缺一项', True))
    p2 = gt.replace(sec6_line, sec6_line + '；标的公司员工安置方案未取到')
    probes.append(('反证·第六节多列一条而正文无｜独有句「第六节多列一项」', p2, '第六节多列一项', True))
    p3 = gt.replace('\n' + body_gap_line, '').replace(
        sec6_line, '- 口径：审计净利润取公告披露口径，未做审计调整')
    probes.append(('反证·两处都无这一项时本支不发｜独有句反向断言', p3, '第六节的点名缺一项', False))
    probes.append(('反证·两处都有时本支不发（好样原样）', gt, '第六节多列一项', False))
    # 边界收窄两向钉死：信用评级是事实陈述不误红，投资评级是评价形必红
    p4 = gt.replace('- 交易对方：标的公司全体股东共 5 名，其中 2 名为上市公司关联方 [S2]',
                    '- 交易对方：标的公司全体股东共 5 名，其中 2 名为上市公司关联方 [S2]\n'
                    '- 上市公司主体信用评级为 AA+，评级机构为某评级公司 [S2]')
    probes.append(('钉阈·「主体信用评级 AA+」是事实陈述，不得判红', p4, '评级形', False))
    p5 = gt.replace('- 交易对方：标的公司全体股东共 5 名，其中 2 名为上市公司关联方 [S2]',
                    '- 交易对方：标的公司全体股东共 5 名，其中 2 名为上市公司关联方 [S2]\n'
                    '- 券商投资评级为增持 [S2]')
    probes.append(('钉阈·「券商投资评级为增持」是评价形，必须判红', p5, '评级形', True))
    # 时间轴两条结构判据各钉一形
    p6 = gt.replace('- 2026-07-03｜实施｜标的资产完成过户，新增股份尚未上市 [S8]',
                    '- 2026-07-03｜实施｜标的资产完成过户，新增股份尚未上市 [S8]\n'
                    '- 2026-08-01｜终止｜交易终止 [S8]')
    probes.append(('钉阈·「终止」在最后一行不判红', p6, '不是最后一行', False))
    p7 = gt.replace('- 2026-07-03｜实施｜标的资产完成过户，新增股份尚未上市 [S8]',
                    '- 2026-07-03｜终止｜交易终止 [S8]\n'
                    '- 2026-08-01｜实施｜标的资产完成过户 [S8]')
    probes.append(('钉阈·「终止」不在最后一行必须判红', p7, '不是最后一行', True))
    p8 = gt.replace('- 2026-02-27｜问询｜回复首轮问询并披露修订后的报告书 [S5]',
                    '- 2026-02-27｜问询｜回复首轮问询并披露修订后的报告书 [S5]\n'
                    '- 2026-01-20｜问询｜补充披露问询回复 [S5]')
    probes.append(('钉阈·日期倒序必须判红', p8, '日期倒序', True))
    p9 = gt.replace('- 交易对价：8.6 亿元 → 9.2 亿元（草案相对预案上调 0.6 亿元） [S2][S3]',
                    '- 交易对价：8.6 亿元 → 9.2 亿元（草案相对预案上调 0.6 亿元） [S3]')
    probes.append(('钉阈·变化行只挂一枚锚必须判红', p9, '只有 1 枚不同号的锚', True))
    for name, txt, needle, want in probes:
        assert txt != gt or not want, '注入自证：反证档必须真改过文本（除好样档）'
        pf = _probe_copy(txt)
        iss_p, _ls_p = scan(pf)
        detail_p = "\n".join(f'[{c}] [{lane}] 第 {no} 行：{msg}' for c, lane, no, msg in iss_p)
        rc_p = 1 if iss_p else 0
        hit = needle in detail_p
        okp = (hit if want else not hit)
        print(f"  {'ok  ' if okp else 'FAIL'} {name}｜实发{'含' if hit else '不含'}独有句、退码 {rc_p}")
        if not okp:
            bad += 1
    n_probes = len(probes)   # 现算：下面两档行号探针不在 probes 列表里，写死会少报

    # 行号两档：判据报的行号必须是文件里真的那一行，不是过滤后列表的下标。
    # 这两档钉的是「空行错位」与「逐字重复行」——两种都会让 index() 指错行，而错行号比不报更难查。
    def line_of(txt, needle):
        for i, ln in enumerate(txt.split('\n'), 1):
            if needle in ln:
                return i
        return -1

    concl = '公司发行股份购买某精密制造 100% 股权，2026-07-03 完成标的资产过户，新增股份尚未上市；对价与锁定期在草案阶段各改过一次。'
    p10 = gt.replace(concl, '\n（待填：本件不代你下结论）')
    want_no = line_of(p10, '（待填：本件不代你下结论）')
    iss_p, _ = scan(_probe_copy(p10))
    got = [no for c, lane, no, msg in iss_p if '结论仍是占位' in msg]
    okp = got == [want_no]
    print(f"  {'ok  ' if okp else 'FAIL'} 钉阈·结论占位报的行号＝真行号（空行在前，期望 {want_no}，实发 {got}）")
    if not okp:
        bad += 1
    n_probes += 1

    src1 = '- [S1] 关于筹划重大资产重组的停牌公告 https://www.cninfo.com.cn/new/disclosure/detail?annoId=1001 检索日 2026-07-05'
    bad_src = '- [S1] 关于筹划重大资产重组的停牌公告 检索日 2026-07-05'   # 缺 URL
    p11 = gt.replace(src1, bad_src + '\n' + bad_src)
    want_nos = [i for i, ln in enumerate(p11.split('\n'), 1) if ln == bad_src]
    iss_p, _ = scan(_probe_copy(p11))
    got = sorted(no for c, lane, no, msg in iss_p if '缺 URL' in msg)
    okp = got == want_nos
    print(f"  {'ok  ' if okp else 'FAIL'} 钉阈·逐字重复的来源行各报自己的行号（期望 {want_nos}，实发 {got}）")
    if not okp:
        bad += 1
    n_probes += 1

    root = Path(tempfile.gettempdir())
    for d in TMP_ROOTS:
        shutil.rmtree(d, ignore_errors=True)
    leftover = sorted(q.name for q in root.iterdir() if q.name.startswith('check-restructuring-tracker-')) if root.is_dir() else []
    print(f"  {'ok  ' if not leftover else 'FAIL'} 临时根自清（跑后不增）｜本次建 {len(TMP_ROOTS)} 枚·跑后残留 {len(leftover)} 枚")
    if leftover:
        bad += 1
    for name, want_rc, want_code in cases:
        p = fx / name
        if not p.is_file():
            print(f'  selftest 取值域故障：夹具不在场 {name}')
            return 3
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc, n, counts = run_one(p, quiet=True)
        detail = buf.getvalue()
        if rc != want_rc:
            print(f'  不合 {name}：期望退码 {want_rc}，实发 {rc}')
            bad += 1
            continue
        if want_code and want_code not in detail:
            print(f'  不合 {name}：期望发码 {want_code}，实发详行不含它')
            bad += 1
            continue
        if want_code is None and rc == 0:
            print(f'  ok   {name}（退码 {rc}·发条 {n}）')
        elif want_code:
            print(f'  ok   {name}（退码 {rc}·发条 {n}·实发 {want_code}）')
    print('selftest: ' + ('ALL GREEN（好样 1 枚·坏样五道 5/5·钉阈与反证 %d 档）' % n_probes if bad == 0
                          else f'{bad} 条不合期望'))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(prog='check_tracker.py', add_help=False,
                                 description='校一份并购重组跨期进度跟踪稿（五道，见 --help 正文）')
    ap.add_argument('target', nargs='?')
    ap.add_argument('--selftest', action='store_true', help='跑包内夹具（好样须过、五枚坏样须各发红）')
    ap.add_argument('--quiet', action='store_true', help='只报末行')
    ap.add_argument('-h', '--help', action='store_true', help='本说明')
    a = ap.parse_args()
    if a.help or (not a.target and not a.selftest):
        print(__doc__)
        return 0 if a.help else 2
    if a.selftest:
        return selftest()
    p = Path(a.target)
    if not p.is_file():
        print(f'取值域故障：读不到跟踪稿文件 {p}（不当「零违例」读）')
        return 3
    rc, _, _ = run_one(p, quiet=a.quiet)
    return rc


if __name__ == '__main__':
    sys.exit(main())
