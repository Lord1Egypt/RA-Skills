#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""digest.py — 由 watchlist.json 与本次返货转写件产出五段增量日报（零网络，幂等）。

用法：
    python3 digest.py --run-dir <目录> --events <本次返货转写件.jsonl> \
                      --asof "YYYY-MM-DD HH:MM" --window 2026-09-10~2026-10-10 \
                      [--legs-called 5] [--billing "<服务端返回原样>"] [--quiet]
    python3 digest.py --run-dir <目录> --events <同上> --check     # 只用退出码说话

退出码（可插拔位，见 SKILL.md §6）：0=窗口内无新增，10=有新增，1=取数或形制错误。
幂等：同一 --events 内容与同一 asof 日期重跑，产出逐字节一致且不重复计新增（run.json 存事件集摘要做凭据）。
指纹（新增判定唯一依据）：代码＋类型＋日期＋出处摘要，与墙钟无关。
零网络：本脚本不取任何数；events 是 agent 用工具取回后的转写件，逐行 JSON。
同源：第五段来源索引与 sources.jsonl 由同一批行写出（新增腿与存量变更腿都在内），进索引的必进件。
坏输入：某行不是合法 JSON、或是合法 JSON 但不是对象（数组／字符串／数字／布尔），都只出一句点名行号的可读出口并退 1——不抛 Traceback，也不留半件。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

DATE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
DATE_HEAD = re.compile(r'^(\d{4}-\d{2}-\d{2})[ T]?\d{0,2}:?\d{0,2}:?\d{0,2}$')
ASOF = re.compile(r'^\d{4}-\d{2}-\d{2}([ T]\d{2}:\d{2}(:\d{2})?)?$')
NEED = ('code', 'type', 'date', 'title', 'url')


def load_events(path: Path, log):
    """零条是常规路径：空转写件、或只给一行 {"_kind":"header"} 声明件都算数。
       其余任何一行缺 NEED 字段仍即报错不猜——「没检索到」要有形制，「写坏了」不算。
       合法 JSON 但不是对象（数组、字符串、数字）同样按取数错误出一句人话，不抛 Traceback。"""
    rows, header, i = [], False, 0
    for i, ln in enumerate(path.read_text(encoding='utf-8').split('\n'), 1):
        ln = ln.strip()
        if not ln:
            continue
        try:
            obj = json.loads(ln)
        except json.JSONDecodeError:
            log(f'digest: --events 第 {i} 行不是 JSON（取数或形制错误）')
            return None
        if not isinstance(obj, dict):
            log(f'digest: --events 第 {i} 行是 JSON {type(obj).__name__}，本件只收对象（每行一条事件）；'
                f'要声明零条请给 {{"_kind":"header"}} 行（取数或形制错误）')
            return None
        if obj.get('_kind') == 'header':
            header = True
            continue
        missing = [k for k in NEED if not str(obj.get(k, '')).strip()]
        if missing:
            log(f'digest: --events 第 {i} 行缺字段 {missing}（缺字段即报错，不猜；要声明零条请给 {{"_kind":"header"}} 行）')
            return None
        rows.append(obj)
    if not rows and not header:
        log('digest: 零条转写件（无数据行也未给 header 行）——按「窗口内未检索到新增」出件，退码 0')
    return rows


def fp(ev):
    src = hashlib.sha256(ev['url'].encode('utf-8')).hexdigest()[:12]
    return '|'.join([str(ev['code']), str(ev['type']), str(ev['date']), src])


def source_batch(new_rows, changed_rows, asof):
    """第五段来源索引与 sources.jsonl 的同一批行：一次组装、两处消费——进索引的那批就是写进件的那批。

    键取本次事件现值（code／name／type／date／url／asof），变更腿另带 before／now；
    索引按 URL 首现去重呈现，件按逐事件全量留痕，两处的 URL 集由本函数保证相同。"""
    batch = []
    for e in new_rows:
        batch.append({'code': e['code'], 'name': e.get('name') or str(e['code']), 'type': e['type'],
                      'date': e['date'], 'url': e['url'], 'asof': asof})
    for c in changed_rows:
        batch.append({'code': c['code'], 'name': c['name'], 'type': c['type'], 'date': c['date'],
                      'url': c['url'], 'asof': asof, 'before': c['before'], 'now': c['now']})
    return batch


def render(subjects, asof, window, legs_called, legs_returned, new_rows, changed_rows, prev_date, missing_legs,
           offlist=0, sources=None):
    d = []
    d.append('# 自选清单增量日报')
    d.append('')
    d.append('## 头部自标')
    d.append('')
    d.append('- 本件状态：**AI 整理初稿，逐条请回官方原文核对，不构成投资建议**。')
    d.append('- 交付形制：五段（时点与范围／今日新增／近端变更／需人工／来源索引）；机检跑 `check_digest.py` 并带 `--run run.json`。')
    d.append('')
    d.append('## 一、时点与范围')
    d.append('')
    d.append('| 项 | 值 |')
    d.append('|---|---|')
    d.append(f'| asof 时刻 | {asof} |')
    d.append(f'| 清单规模 | {len(subjects)} 家 |')
    d.append(f'| 本次实跑域数 | {legs_called} |')
    d.append(f'| 本次返货腿数 | {legs_returned} |')
    d.append(f'| 上次快照日期 | {prev_date} |')
    d.append(f'| 检索窗口 | {window} |')
    d.append(f'| 清单外返货（未并入本清单） | {offlist} 条 |')
    d.append('')
    d.append('## 二、今日新增')
    d.append('')
    if new_rows:
        d.append('| # | 主体（代码） | 类型 | 判定句（照原文标题逐字） | 日期 | 出处锚 |')
        d.append('|---|---|---|---|---|---|')
        for i, ev in enumerate(new_rows, 1):
            d.append(f"| {i} | {ev['name']}（{ev['code']}） | {ev['type']} | 「{ev['title']}」 | {ev['date']} | {ev['url']} |")
        d.append('')
        d.append(f'零新增声明：☐ 本次检索窗口 {window} 内未检索到新增　☑ 不适用（上表有新增 {len(new_rows)} 条）')
    else:
        d.append('| # | 主体（代码） | 类型 | 判定句（照原文标题逐字） | 日期 | 出处锚 |')
        d.append('|---|---|---|---|---|---|')
        d.append('| 1 | | | | | |')
        d.append('')
        d.append(f'零新增声明：☑ 本次检索窗口 {window} 内未检索到新增　☐ 不适用（上表有新增）')
    d.append('')
    d.append('## 三、近端变更')
    d.append('')
    if changed_rows:
        d.append('| # | 主体（代码） | 项 | 前值 → 现值 | 依据锚 |')
        d.append('|---|---|---|---|---|')
        for i, ch in enumerate(changed_rows, 1):
            d.append(f"| {i} | {ch['name']}（{ch['code']}） | {ch['item']} | {ch['before']} → {ch['now']} | {ch['url']} |")
    else:
        d.append('| # | 主体（代码） | 项 | 前值 → 现值 | 依据锚 |')
        d.append('|---|---|---|---|---|')
        d.append('| 1 | 本次无可核对的存量推进变化 | — | 不适用（无前值可引，不编造） | 不适用 |')
    d.append('')
    d.append('## 四、需人工')
    d.append('')
    d.append('| # | 事项 | 状态 |')
    d.append('|---|---|---|')
    d.append('| 1 | 本清单各条事件对价格的影响、评级、目标价与买卖建议 | `[待人工]` |')
    for i, m in enumerate(missing_legs, 2):
        d.append(f'| {i} | 本腿未取到：{m}（原因以返货现值为准，不补） | `[待人工]` |')
    d.append('')
    d.append('## 五、来源索引')
    d.append('')
    d.append('与同目录 sources.jsonl 一一对应；下表逐条给出处与该条事件日期。')
    d.append('')
    d.append('| # | 出处 | 事件日 |')
    d.append('|---|---|---|')
    seen = []
    for i, rec in enumerate(sources or [], 1):
        seen.append(rec['url'])
        d.append(f"| {i} | {rec['url']} | {rec['date']} |")
    if not seen:
        d.append('| 1 | 本次无新增来源（窗口内未检索到） | 不适用 |')
    return '\n'.join(d) + '\n'


def main() -> int:
    ap = argparse.ArgumentParser(description='生成五段增量日报（零网络，幂等，退出码 0/10/1）')
    ap.add_argument('--run-dir', required=True)
    ap.add_argument('--events', required=True, help='本次返货转写件（jsonl）')
    ap.add_argument('--asof', help='本次运行的快照时刻 YYYY-MM-DD[ HH:MM]')
    ap.add_argument('--window', help='检索窗口，如 2026-09-10~2026-10-10')
    ap.add_argument('--legs-called', type=int, default=0, help='本次实跑域数（取自返货回显）')
    ap.add_argument('--billing', default='未回传', help='计费按服务端返回逐笔照录，不折算')
    ap.add_argument('--check', action='store_true', help='只用退出码说话：0 无新增／10 有新增／1 错')
    ap.add_argument('--quiet', action='store_true')
    args = ap.parse_args()

    def log(msg):
        if not (args.check or args.quiet):
            print(msg, file=sys.stderr)

    run_dir = Path(args.run_dir)
    wl = run_dir / 'watchlist.json'
    if not wl.is_file():
        log(f'digest: 缺 {wl}——先跑 init_watchlist.py 落清单')
        return 1
    subjects = json.loads(wl.read_text(encoding='utf-8')).get('subjects') or []
    if not subjects:
        log('digest: watchlist.json 的 subjects 为空（缺字段即报错，不猜）')
        return 1
    ev_path = Path(args.events)
    if not ev_path.is_file():
        log(f'digest: 读不到 --events 指定的文件 {ev_path}')
        return 1
    events = load_events(ev_path, log)
    if events is None:
        return 1
    if not args.check:
        if not args.asof or not ASOF.match(args.asof):
            log('digest: --asof 必须是 YYYY-MM-DD 或 YYYY-MM-DD HH:MM（时点缺一无效）')
            return 1
        if not args.window or args.window.count('~') != 1 or not all(DATE.match(x) for x in args.window.split('~')):
            log('digest: --window 必须给起止两个日期（形如 2026-09-10~2026-10-10）')
            return 1
    else:
        if not args.asof or not ASOF.match(args.asof):
            return 1
    day = (DATE_HEAD.match(args.asof).group(1) if args.asof and DATE_HEAD.match(args.asof) else '')
    names = {s['code']: s.get('name') or s['code'] for s in subjects}
    rows = [e for e in events if e.get('code') in names]
    off = [e for e in events if e.get('code') not in names]
    skipped = sorted({str(e.get('code', '?')) for e in off})
    if skipped and not args.check:
        log(f'digest: 清单外返货 {len(off)} 条（代码 {("、".join(skipped))}）不并入，已计入 run.json 与第一段')
    for e in rows:
        e.setdefault('name', names[e['code']])
    new_rows = [e for e in rows if e.get('kind', 'new') == 'new']
    window_new = len(new_rows)          # 窗口存量：未经快照差集过滤，重放判据的对照面
    changed_rows = []
    for e in (r for r in rows if r.get('kind') == 'changed'):
        if 'before' in e and 'now' in e:
            changed_rows.append({**e, 'name': names[e['code']], 'item': e.get('item') or e.get('type')})
    legs_returned = len({e.get('leg', e['type']) for e in rows})
    missing_legs = []
    if args.legs_called and legs_returned < args.legs_called:
        missing_legs = [f'实跑 {args.legs_called} 域、返货只覆盖 {legs_returned} 域']

    prev_f = run_dir / 'snapshot.prev.json'
    snap = json.loads(prev_f.read_text(encoding='utf-8')) if prev_f.is_file() else {'fingerprints': [], 'asof_date': '无（首次运行）'}
    digest_all = hashlib.sha256('\n'.join(sorted(fp(e) for e in new_rows)).encode('utf-8')).hexdigest()
    run_f = run_dir / 'run.json'
    stored = json.loads(run_f.read_text(encoding='utf-8')) if run_f.is_file() else {}
    same_day_replay = (snap.get('asof_date') == day and stored.get('events_digest') == digest_all
                       and stored.get('asof_date') == day)
    keep = set(snap.get('fingerprints', []))
    first_seen = [e for e in new_rows if fp(e) not in keep]
    if args.check:
        # 三态只看快照差集：已报过的指纹不算新增；同日重放按 run.json 记账值说话
        if same_day_replay:
            return 10 if stored.get('new_count') else 0
        return 10 if first_seen else 0
    day_fps = stored.get('new_fps')
    if same_day_replay and day_fps is None and not args.check:
        log('digest: 当日 run.json 里没有「new_fps」记账集（旧版留下的 run.json）——重放无从复用当日增量子集。'
            '不写件，以免把窗口存量当新增重播；请按当日原始输入重跑一次即补记账，或删 run.json 与 snapshot.prev.json 后从头跑')
        return 1
    if not same_day_replay:
        new_rows = first_seen
        prev_date = snap.get('asof_date', '无（首次运行）')
    else:
        # 重放态：呈现与记账都取当日已记的那一子集，不重新判定，也不退回窗口存量
        keep_day = set(day_fps)
        new_rows = [e for e in new_rows if fp(e) in keep_day]
        prev_date = stored.get('prev_date', snap.get('asof_date'))
        legs_returned = stored.get('legs_returned', legs_returned)
        missing_legs = stored.get('missing_legs', missing_legs)

    sources = source_batch(new_rows, changed_rows, args.asof)
    md = render(subjects, args.asof, args.window, args.legs_called, legs_returned, new_rows, changed_rows,
                prev_date, missing_legs, len(off), sources=sources)
    out = run_dir / f'digest-{day}.md'
    out.write_text(md, encoding='utf-8')
    src = run_dir / 'sources.jsonl'
    src.write_text(''.join(json.dumps(rec, ensure_ascii=False, sort_keys=True) + '\n' for rec in sources),
                   encoding='utf-8')
    run = {'asof': args.asof, 'asof_date': day, 'window': args.window, 'subjects': len(subjects),
           'legs_called': args.legs_called, 'legs_returned': legs_returned, 'new_count': len(new_rows),
           'changed_count': len(changed_rows), 'offlist_skipped': len(off), 'events_digest': digest_all,
           'new_fps': sorted(fp(e) for e in new_rows), 'window_new_rows': window_new,
           'prev_date': prev_date,
           'missing_legs': missing_legs, 'billing': args.billing,
           'exit_code': 10 if new_rows else 0, 'idempotent_replay': same_day_replay}
    run_f.write_text(json.dumps(run, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    if not same_day_replay:
        keep = set(snap.get('fingerprints', [])) | {fp(e) for e in new_rows}
        prev_f.write_text(json.dumps({'asof_date': day, 'fingerprints': sorted(keep)}, ensure_ascii=False,
                                     indent=2, sort_keys=True) + '\n', encoding='utf-8')
    if not args.quiet:
        print(f'digest: {out.name} 新增 {len(new_rows)} 条／存量变更 {len(changed_rows)} 条（窗口存量 {window_new} 条）；'
              f'实跑域 {args.legs_called}／返货腿 {legs_returned}；同日重跑={same_day_replay}；退码 {run["exit_code"]}')
    return run['exit_code']


if __name__ == '__main__':
    sys.exit(main())
