#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_outline.py — 零通道骨架：把一份材料清单排成「客户集中度与依赖风险台账」的待填骨架。

用法：
    python3 make_outline.py --sources 材料.jsonl --out 我的骨架.md [--subject 公司名] [--window 2026-11-09]
    python3 make_outline.py --help

材料行必需三键：title / url / asof（检索日 YYYY-MM-DD）；id 可省，缺省按行序给 S1、S2…
非法 JSON 行、缺键行、日期不是 YYYY-MM-DD 的行一律**未采信并逐行点名**，不静默跳行。
一条可用行都没有时退 1——空清单不出骨架，那是没有出处，不是待填。

**代价同句写清**：缺的正是公告检索与原文解析那一层，所以骨架只会有形状、不会有权衡后的集中度事实——
第二节留一行合计待填位、第三节留一行单客户待填位、第四节留一行依赖事实待填位，第五节逐条点名，
集中度一句话留占位。骨架过不了机检是设计，不是待补的疏漏。

退码：0 出骨架；1 一条可用材料行都没有；2 用法错；3 取值域故障（清单读不到）。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
# 骨架里待填位的期间名。写成「待填期间」而不是「2024年度」，
# 是因为期间必须来自披露原文——骨架没有原文，就不能替它编一个期间。
SEED_PERIOD = '待填期间'


def load_sources(path: Path):
    ok, rejected = [], []
    for no, raw in enumerate(path.read_text(encoding='utf-8', errors='replace').split('\n'), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as e:
            rejected.append((no, f'非法 JSON（{e.msg}）'))
            continue
        if not isinstance(row, dict):
            rejected.append((no, '不是对象行'))
            continue
        miss = [k for k in ('title', 'url', 'asof') if not str(row.get(k) or '').strip()]
        if miss:
            rejected.append((no, '缺键 ' + '／'.join(miss)))
            continue
        if not DATE_RE.match(str(row['asof']).strip()):
            rejected.append((no, f"asof 不是 YYYY-MM-DD（现值「{row['asof']}」）"))
            continue
        ok.append(row)
    return ok, rejected


def build(rows, subject, window):
    out = []
    out.append('AI 整理初稿｜请回原文核对｜不构成投资建议｜判断位 [待人工]')
    out.append('集中度口径：客户依赖（收入来自哪些客户、占比多少、跨期怎么变；不判客户质量、不判风险大小）')
    out.append('')
    out.append('## 一、集中度一句话')
    out.append('')
    # 这一行不能带「未取到」三个字：道四会把正文里的「未取到」抽成名目，
    # 于是骨架凭空多出一条「点名缺一项」。骨架的缺口由第五节逐条点名，不靠这句话自述。
    out.append(f'（待填）{subject}的客户集中度——骨架只排了材料清单，占比与期间待补。')
    out.append('')
    out.append('## 二、分期集中度')
    out.append('')
    out.append(f'- 期间：{SEED_PERIOD}｜前五大客户合计：未取到 [S1]')
    out.append('')
    out.append('## 三、单客户明细')
    out.append('')
    # 字段名写「单客户占比」而不是「客户」：道四的同指判据里「一方含另一方」那一支要求短的一方 ≥4 字，
    # 2 字的「客户」与第五节的「单客户占比明细」够不着，会凭空多出一条「点名缺一项」。
    out.append(f'- 期间：{SEED_PERIOD}｜单客户占比：未取到 [S1]')
    out.append('')
    out.append('## 四、关联与依赖事实')
    out.append('')
    out.append('- 未取到：关联关系与重大合同（骨架未取到披露原文，只排了材料清单）')
    out.append('')
    out.append('## 五、未取到与口径')
    out.append('')
    # 名目必须与正文里那几行「未取到」同指：正文写的是「前五大客户合计：未取到」与「客户：未取到」，
    # 第五节就点名这两件事。写成「分期集中度／单客户明细」会与正文对不上，道四按反向同判发红。
    out.append('- 未取到：前五大客户合计（骨架未取到披露原文，只排了材料清单）')
    out.append('- 未取到：单客户占比明细（骨架未取到披露原文，只排了材料清单）')
    out.append('- 未取到：关联关系与重大合同（骨架未取到披露原文，只排了材料清单）')
    out.append(f'- 口径：检索窗口 {window}；材料清单 {len(rows)} 条可用行，逐条见第六节')
    out.append('')
    out.append('## 六、来源')
    out.append('')
    for k, row in enumerate(rows, 1):
        sid = str(row.get('id') or f'S{k}').strip()
        out.append(f"- [{sid}] {str(row['title']).strip()}（{str(row['url']).strip()} ｜检索日 {str(row['asof']).strip()}）")
    out.append('')
    return '\n'.join(out)


def main():
    ap = argparse.ArgumentParser(prog='make_outline.py', add_help=False,
                                 description='零通道骨架：把材料清单排成客户集中度台账的待填骨架')
    ap.add_argument('--sources', required=False)
    ap.add_argument('--out', required=False)
    ap.add_argument('--subject', default='本公司')
    ap.add_argument('--window', default='')
    ap.add_argument('-h', '--help', action='store_true')
    a = ap.parse_args()
    if a.help or not a.sources or not a.out:
        print(__doc__)
        return 0 if a.help else 2
    src = Path(a.sources)
    if not src.is_file():
        print(f'取值域故障：读不到材料清单 {src}（不当「零条可用」读）')
        return 3
    rows, rejected = load_sources(src)
    for no, why in rejected:
        print(f'  未采信 第 {no} 行：{why}')
    if not rows:
        print(f'FAIL: {src.name} 一条可用材料行都没有（未采信 {len(rejected)} 行）——空清单不出骨架，那是没有出处，不是待填')
        return 1
    text = build(rows, a.subject, a.window or '未填')
    Path(a.out).write_text(text, encoding='utf-8')
    print(f'PASS: 骨架已出 {a.out}（可用 {len(rows)} 条·未采信 {len(rejected)} 条）')
    print('       代价：缺公告检索与原文解析那一层，骨架只有形状、没有集中度事实；三节各留一行待填位')
    print('       骨架过不了机检是设计，不是待补的疏漏——别把它当台账交付')
    return 0


if __name__ == '__main__':
    sys.exit(main())
