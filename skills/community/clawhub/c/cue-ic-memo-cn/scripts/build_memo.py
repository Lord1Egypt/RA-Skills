#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_memo.py — 把返货转写件与用户材料落成七节投决讨论稿（零网络，幂等）。

用法：
    python3 build_memo.py --run-dir DIR --subject 600606 --subject-name 某某股份 \\
        --facts facts.jsonl [--gaps gaps.jsonl] [--materials materials.jsonl] \\
        --asof "YYYY-MM-DD HH:MM" [--billing "<服务端返回原样>"] [--quiet]

行形制（逐行 JSON，缺什么就照实落第 5 节，不猜不填）：
    facts：section(2|3|4) ＋ item ＋ source ＋ locator；二、四节另需 value／basis／date；四节需 side(bull|bear)
    gaps ：item ＋ why（这条为什么取不到／不齐／截断）
    materials：path ＋ title
退出码：0＝成文；1＝不成文（取数或形制错误，或反方两侧缺一侧）。
不成文只给可读中文行——不 traceback，也不默默少一节。
幂等：同一输入与同一 asof 日期重跑，产出逐字节一致（脚本不读墙钟）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

DATE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
DATE_HEAD = re.compile(r'^(\d{4}-\d{2}-\d{2})[ T]?\d{0,2}:?\d{0,2}:?\d{0,2}$')
ASOF = re.compile(r'^\d{4}-\d{2}-\d{2}([ T]\d{2}:\d{2}(:\d{2})?)?$')
CODE = re.compile(r'^\d{6}$')
SECTIONS = ['摘要', '事实与数字', '业务与行业要点', '风险与反方', '缺数与未决', '人工复核清单', '来源索引']
CN = ['一', '二', '三', '四', '五', '六', '七']
NEED24 = ('item', 'value', 'basis', 'date', 'source', 'locator')
NEED3 = ('item', 'source', 'locator')


def read_rows(path: Path, log, tag):
    """逐行 JSON；坏行＝取数错误（报错不成文），不静默跳过。
       合法 JSON 但不是对象（数组／字符串／数字／布尔／null）同样按取数错误出一句人话，不抛 Traceback。"""
    rows = []
    if path is None:
        return rows
    for i, ln in enumerate(path.read_text(encoding='utf-8').split('\n'), 1):
        ln = ln.strip()
        if not ln:
            continue
        try:
            obj = json.loads(ln)
        except json.JSONDecodeError:
            log(f'build_memo: --{tag} 第 {i} 行不是 JSON（取数或形制错误，不静默跳行）')
            return None
        if not isinstance(obj, dict):
            log(f'build_memo: --{tag} 第 {i} 行是 JSON {type(obj).__name__}，本件每行只收对象（一条记录＝一个对象，'
                f'取数或形制错误，不静默跳行）')
            return None
        rows.append(obj)
    return rows


def missing(obj, keys):
    return [k for k in keys if not str(obj.get(k, '')).strip()]


def num(v):
    s = str(v).replace(',', '').replace('，', '').strip()
    m = re.search(r'-?\d+(\.\d+)?', s)
    if not m:
        return None
    try:
        return Decimal(m.group(0))
    except InvalidOperation:
        return None


def cell(v):
    s = '' if v is None else str(v)
    return (s if s.strip() else '—').replace('|', '／')


def build(subject, name, asof, facts, gaps, materials, run_extra):
    """返回 (正文, 来源行, 落账计数, 拒答原因列表)。"""
    kept2, kept3, bull, bear, routed = [], [], [], [], []
    for obj in facts:
        sec = str(obj.get('section', '')).strip()
        side = str(obj.get('side', '')).strip().lower()
        if sec == '4':
            miss = missing(obj, NEED24)
            if side not in ('bull', 'bear'):
                miss = miss + ['side(bull|bear)']
            if miss:
                routed.append((obj, '第 4 节行缺 ' + '、'.join(miss) + '，未采信'))
                continue
            if not DATE.match(str(obj['date']).strip()):
                routed.append((obj, '第 4 节行日期非 YYYY-MM-DD（' + str(obj['date']) + '），未采信'))
                continue
            (bull if side == 'bull' else bear).append(obj)
        elif sec == '2':
            miss = missing(obj, NEED24)
            if miss:
                routed.append((obj, '第 2 节行缺 ' + '、'.join(miss) + '，未采信'))
                continue
            if not DATE.match(str(obj['date']).strip()):
                routed.append((obj, '第 2 节行日期非 YYYY-MM-DD（' + str(obj['date']) + '），未采信'))
                continue
            if str(obj.get('truncated', '')).strip().lower() in ('1', 'true', 'yes', '是'):
                routed.append((obj, '返货声明正文截断，数值不完整，未采信（要引用请回官方原文）'))
                continue
            kept2.append(obj)
        elif sec == '3':
            miss = missing(obj, NEED3)
            if miss:
                routed.append((obj, '第 3 节行缺 ' + '、'.join(miss) + '，未采信'))
                continue
            kept3.append(obj)
        else:
            routed.append((obj, f'section 现值「{sec}」不在 2|3|4 之内，未采信'))

    refuse = []
    if not bull:
        refuse.append('看多依据零条（反方两侧缺一侧即不成文，不默默少一节）')
    if not bear:
        refuse.append('看空依据零条（反方两侧缺一侧即不成文，不默默少一节）')
    if not kept2 and not kept3 and not bull and not bear and not routed and not gaps:
        refuse.append('本次没有任何可落成文的行——空稿不等于「无信息」，请显式给转写件')

    gap_rows = []
    for g in gaps:
        miss = missing(g, ('item', 'why'))
        if miss:
            gap_rows.append({'item': str(g.get('item', f'缺 {miss} 的未名条目')), 'why': '转写件缺 ' + '、'.join(miss) + '（形制不合，未采信）'})
        else:
            gap_rows.append({'item': str(g['item']), 'why': str(g['why'])})
    for obj, why in routed:
        gap_rows.append({'item': str(obj.get('item') or f'（无条目名，出处 {obj.get("source", "—")}）'), 'why': why})

    # 同组同口径合计：只加本次分项，不引外部数
    groups = {}
    for obj in kept2:
        gname = str(obj.get('total_group', '')).strip()
        if not gname:
            continue
        key = (gname, str(obj.get('unit', '')).strip(), str(obj.get('basis', '')).strip())
        groups.setdefault(key, []).append(num(obj['value']))
    totals, mixed = [], []
    for (gname, unit, basis), vals in sorted(groups.items()):
        if len(vals) < 2:
            continue
        if any(v is None for v in vals):
            mixed.append((gname, '有分项不可解数，本组不合计'))
            continue
        totals.append({'group': gname, 'unit': unit, 'basis': basis, 'sum': sum(vals), 'parts': len(vals),
                       'digest': hashlib.sha256(('|'.join(str(v) for v in vals)).encode('utf-8')).hexdigest()[:12]})
    seen_basis = {}
    for obj in kept2:
        gname = str(obj.get('total_group', '')).strip()
        if not gname:
            continue
        seen_basis.setdefault(gname, set()).add((str(obj.get('unit', '')).strip(), str(obj.get('basis', '')).strip()))
    for gname, pairs in sorted(seen_basis.items()):
        if len(pairs) > 1:
            mixed.append((gname, f'本组口径／单位不齐（{len(pairs)} 种），不合计、不取平均'))

    d = []
    d.append('# 投决备忘录（草稿）')
    d.append('')
    d.append('## 头部自标')
    d.append('')
    d.append('- 本件状态：**AI 整理初稿，逐条请回官方原文核对，不构成投资建议，也不构成决议**。')
    d.append(f'- 交付形制：七节（{"/".join(SECTIONS)}）；机检跑 `check_memo.py` 并带 `--run run.json`。')
    d.append('- 能力边界：不决议只起草（人负终审、不自动发布）；不评级、不给目标价；**不含估值测算**——本件无行情与持仓数据腿，估值只作适用性声明。')
    d.append('')
    d.append(f'## {CN[0]}、{SECTIONS[0]}')
    d.append('')
    d.append(f'本稿主体为 {name}（{subject}），快照时点 {asof}。')
    d.append(f'本次落成：事实与数字 {len(kept2)} 条、业务要点 {len(kept3)} 条、看多 {len(bull)} 条、看空 {len(bear)} 条；缺数与未决 {len(gap_rows)} 条逐条列于第五节。')
    d.append('以上条数取自本次运行账 run.json，未取到的行不填、不猜、不以外部搜索顶替。')
    d.append('')
    d.append(f'## {CN[1]}、{SECTIONS[1]}')
    d.append('')
    d.append('| # | 组 | 事实／指标 | 数值 | 单位 | 口径 | 日期 | 出处锚 | 定位 |')
    d.append('|---|---|---|---|---|---|---|---|---|')
    if not kept2 and not totals:
        d.append('| 1 | — | 本次无可锚定的数值行 | 未取到 | — | 不适用 | 不适用 | 本次无可回查锚（见第五节） | 不适用 |')
    n = 0
    for obj in kept2:
        n += 1
        d.append('| {i} | {g} | {it} | {v} | {u} | {b} | {dt} | {s} | {loc} |'.format(
            i=n, g=cell(obj.get('total_group')), it=cell(obj['item']), v=cell(obj['value']),
            u=cell(obj.get('unit')), b=cell(obj['basis']), dt=cell(obj['date']),
            s=cell(obj['source']), loc=cell(obj['locator'])))
    for t in totals:
        n += 1
        d.append('| {i} | {g} | 合计 | {s} | {u} | 同口径分项逐条相加（本次返货内，不引外部数；不取平均） | {dt} | 本次返货 {p} 枚分项相加，值指纹 {dg} | 见本组各行 |'.format(
            i=n, g=cell(t['group']), s=cell(t['sum']), u=cell(t['unit']),
            dt=asof.split()[0], p=t['parts'], dg=t['digest']))
    for gname, why in mixed:
        n += 1
        d.append('| {i} | {g} | 合计 | 不适用 | — | {w} | {dt} | 本次运行账 run.json | — |'.format(
            i=n, g=cell(gname), w=cell(why), dt=asof.split()[0]))
    d.append('')
    d.append('同一事实多源时并列两源，不合并不取平均（上表每行只载一源）。')
    d.append('')
    d.append(f'## {CN[2]}、{SECTIONS[2]}')
    d.append('')
    d.append('| # | 要点（照可指到的陈述） | 出处锚 | 定位 |')
    d.append('|---|---|---|---|')
    if not kept3:
        d.append('| 1 | 本次无可指到的业务陈述；本件无行业数据腿，行业语境不在覆盖内 | 不适用 | 不适用 |')
    for i, obj in enumerate(kept3, 1):
        d.append(f'| {i} | {cell(obj["item"])} | {cell(obj["source"])} | {cell(obj["locator"])} |')
    d.append('')
    d.append(f'## {CN[3]}、{SECTIONS[3]}')
    d.append('')
    d.append(f'两方条数：看多 {len(bull)} 条、看空 {len(bear)} 条——不等就照实写不等，不强行平衡。')
    d.append('')
    for label, rows in (('看多依据', bull), ('看空依据', bear)):
        d.append(f'**{label}**')
        d.append('')
        d.append('| # | 依据 | 数值／事实 | 口径 | 日期 | 出处锚 | 定位 |')
        d.append('|---|---|---|---|---|---|---|')
        for i, obj in enumerate(rows, 1):
            d.append('| {i} | {it} | {v} {u} | {b} | {dt} | {s} | {loc} |'.format(
                i=i, it=cell(obj['item']), v=cell(obj['value']), u=cell(obj.get('unit')),
                b=cell(obj['basis']), dt=cell(obj['date']), s=cell(obj['source']), loc=cell(obj['locator'])))
        d.append('')
    d.append(f'## {CN[4]}、{SECTIONS[4]}')
    d.append('')
    d.append('| # | 事项 | 为何取不到／未决 | 状态 |')
    d.append('|---|---|---|---|')
    if not gap_rows:
        d.append('| 1 | 本次无缺数与未决申报 | 不适用（正文无「未取到」行） | — |')
    for i, g in enumerate(gap_rows, 1):
        d.append(f'| {i} | {cell(g["item"])} | {cell(g["why"])} | `[待人工]` |')
    d.append('')
    d.append('「未检索到」不等于「没有发生」：本节只记本次窗口与本次口径下取到的状态。')
    d.append('')
    d.append(f'## {CN[5]}、{SECTIONS[5]}')
    d.append('')
    d.append('| # | 事项 | 状态 |')
    d.append('|---|---|---|')
    d.append('| 1 | 评级、目标价、买卖建议与最终决议 | `[待人工]` |')
    d.append('| 2 | 估值倍数与任何估值测算（本件无行情与持仓腿，只作适用性声明） | `[待人工]` |')
    d.append('| 3 | 走势、资金面与行情类判断 | `[待人工]` |')
    d.append('| 4 | 跨期比较的口径对齐（两期同口径才可比） | `[待人工]` |')
    d.append('')
    d.append('本节是本件唯一容纳这类事项的位置：正文其余各节出现判断词即属违例。决议权在人，本件不表决、不代签、不自动发布。')
    d.append('')
    d.append(f'## {CN[6]}、{SECTIONS[6]}')
    d.append('')
    d.append('与同目录 sources.jsonl 一一对应；任一条回查不到就删该行，不补猜。')
    d.append('')
    d.append('| # | 出处 | 定位 | asof |')
    d.append('|---|---|---|---|')
    srcs, k = [], 0
    for rows, need_loc in ((kept2, True), (bull, True), (bear, True), (kept3, True)):
        for obj in rows:
            if str(obj['source']) in [s[0] for s in srcs]:
                continue
            k += 1
            srcs.append((str(obj['source']), str(obj.get('locator', '—')), str(obj.get('date') or asof.split()[0])))
    for m in materials:
        k += 1
        srcs.append((f'用户材料：{str(m.get("title") or m.get("path"))}（{m.get("path")}）', '原件在用户侧', asof.split()[0]))
    if not srcs:
        d.append('| 1 | 本次无可回查来源（正文无挂锚行） | 不适用 | 不适用 |')
    for i, (s, loc, dt) in enumerate(srcs, 1):
        d.append(f'| {i} | {cell(s)} | {cell(loc)} | {cell(dt)} |')
    d.append('')

    src_lines = [json.dumps({'n': i, 'source': s, 'locator': loc, 'date': dt, 'asof': asof},
                            ensure_ascii=False, sort_keys=True) for i, (s, loc, dt) in enumerate(srcs, 1)]
    counts = {'subject': subject, 'subject_name': name, 'asof': asof, 'asof_date': asof.split()[0],
              'fact_rows': len(kept2), 'business_rows': len(kept3), 'bull_rows': len(bull),
              'bear_rows': len(bear), 'gap_rows': len(gap_rows), 'source_rows': len(srcs),
              'material_rows': len(materials), 'routed_rows': len(routed),
              'totals': {t['group']: str(t['sum']) for t in totals},
              'totals_meta': {t['group']: {'parts': t['parts'], 'unit': t['unit'], 'basis': t['basis']} for t in totals},
              'mixed_groups': {g: w for g, w in mixed}, 'billing': run_extra.get('billing', '未回传'),
              'exit_code': 1 if refuse else 0}
    return '\n'.join(d) + '\n', src_lines, counts, refuse


def main() -> int:
    ap = argparse.ArgumentParser(description='落成七节投决讨论稿草稿（零网络，幂等）')
    ap.add_argument('--run-dir', required=True)
    ap.add_argument('--subject', required=True, help='6 位 sec_code（主键；名称多候选不代选，先定码）')
    ap.add_argument('--subject-name', dest='name', help='主体名（缺省用代码顶）')
    ap.add_argument('--facts', help='返货转写件（逐行 JSON）')
    ap.add_argument('--gaps', help='缺数清单（逐行 JSON：item＋why）')
    ap.add_argument('--materials', help='用户材料清单（逐行 JSON：path＋title）')
    ap.add_argument('--asof', required=True, help='本次快照时点 YYYY-MM-DD[ HH:MM]')
    ap.add_argument('--billing', default='未回传', help='计费按服务端返回逐笔照录，不折算')
    ap.add_argument('--quiet', action='store_true')
    args = ap.parse_args()

    def log(msg):
        if not args.quiet:
            print(msg, file=sys.stderr)

    if not CODE.match(args.subject):
        log(f'build_memo: --subject 现值「{args.subject}」不是 6 位代码——主键不猜，先解析出 sec_code（多候选列给用户点）')
        return 1
    if not ASOF.match(args.asof):
        log('build_memo: --asof 必须是 YYYY-MM-DD 或 YYYY-MM-DD HH:MM（时点缺一即不成文）')
        return 1
    day = DATE_HEAD.match(args.asof).group(1)
    run_dir = Path(args.run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

    loaded = {}
    for tag in ('facts', 'gaps', 'materials'):
        val = getattr(args, tag)
        if not val:
            loaded[tag] = []
            continue
        p = Path(val)
        if not p.is_file():
            log(f'build_memo: 读不到 --{tag} 指定的文件 {p}')
            return 1
        rows = read_rows(p, log, tag)
        if rows is None:
            return 1
        loaded[tag] = rows

    md, src_lines, counts, refuse = build(args.subject, args.name or args.subject, args.asof,
                                          loaded['facts'], loaded['gaps'], loaded['materials'],
                                          {'billing': args.billing})
    if refuse:
        for r in refuse:
            log(f'build_memo: 不成文——{r}')
        log('build_memo: 反方两侧缺一侧时本件拒绝成文（不是默默少一节，也不是出一半再补）；补齐那一侧的带锚依据后重跑')
        return 1
    out = run_dir / f'memo-{args.subject}-{day}.md'
    out.write_text(md, encoding='utf-8')
    (run_dir / 'sources.jsonl').write_text(''.join(x + '\n' for x in src_lines), encoding='utf-8')
    counts['memo'] = out.name
    (run_dir / 'run.json').write_text(json.dumps(counts, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    if not args.quiet:
        print(f'build_memo: {out.name} 落成｜事实 {counts["fact_rows"]} 条／业务 {counts["business_rows"]} 条／'
              f'看多 {counts["bull_rows"]} 条／看空 {counts["bear_rows"]} 条｜缺数与未决 {counts["gap_rows"]} 条'
              f'（含路由 {counts["routed_rows"]} 条）｜来源 {counts["source_rows"]} 枚｜退码 0')
    return 0


if __name__ == '__main__':
    sys.exit(main())
