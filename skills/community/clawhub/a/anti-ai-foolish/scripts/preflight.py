# -*- coding: utf-8 -*-
"""scripts/preflight.py —— 发文前一键快筛（anti-ai-foolish）。
用法: python scripts/preflight.py <文章.md>
流程: 剥信源 → 全规则扫描 → 硬门（冒号/破折号/直引号/概念引用腔/疑问句密度）→ Z分 → 人味弹药检查 → 判定 发/改/停。"""
import os, sys, io, json, re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scanner import scan, strip_body, kilo

ALLOWED_EXT = ('.md', '.txt', '.markdown')

def _safe_read(path):
    """校验输入路径：必须存在、必须是常规文件、扩展名白名单，防路径注入。"""
    p = os.path.abspath(os.path.realpath(path))
    if not os.path.isfile(p):
        raise SystemExit('输入不是有效文件: %s' % p)
    if os.path.splitext(p)[1].lower() not in ALLOWED_EXT:
        raise SystemExit('仅支持 %s 文件: %s' % (ALLOWED_EXT, p))
    return io.open(p, encoding='utf-8').read()

def preflight(path):
    text = _safe_read(path)
    body = strip_body(text)
    rep = scan(text)
    gates = []
    colon = body.count('：')
    gates.append(('冒号=0', colon == 0, f'{colon}处'))
    dash = body.count('——')
    gates.append(('破折号=0', dash == 0, f'{dash}处'))
    dq = body.count('"')
    gates.append(('直引号=0', dq == 0, f'{dq}处'))
    concept = len(re.findall(r'[“"][^”"]{2,7}[”"]', body)) / kilo(body)
    gates.append(('概念引用腔≤3/千字', concept <= 3, f'{concept:.1f}/千字'))
    q = body.count('？') + body.count('?')
    qd = q / kilo(body)
    gates.append(('疑问句≤3/千字', qd <= 3, f'{qd:.1f}/千字'))
    sec_titles = len(re.findall(r'^#{1,6} |[一二三四五六七八九十]+、', body, re.M))
    gates.append(('无小节标题', sec_titles == 0, f'{sec_titles}处'))
    humane_hits = len(rep['humane_hits'])
    gates.append(('人味弹药≥2类', humane_hits >= 2, f'{humane_hits}类命中'))
    passed = sum(1 for _, ok, _ in gates if ok)
    verdict = '✅ 可发（朱雀切块复测后发布）' if passed == len(gates) and rep['z_score'] < 0 else \
              ('⚠️ 改后复检' if passed >= len(gates) - 2 else '❌ 停下手术')
    print(f"# Preflight — {os.path.basename(path)}")
    print(f"正文 {rep['chars']} 字 | Z分 {rep['z_score']}（AI确认{rep['z_components']['AI确认命中']} − 人味确认{rep['z_components']['人味确认命中']}）")
    for name, ok, detail in gates:
        print(f"  {'✓' if ok else '✗'} {name}: {detail}")
    print(f"门通过 {passed}/{len(gates)} → {verdict}")
    return verdict

if __name__ == '__main__':
    preflight(sys.argv[1])
