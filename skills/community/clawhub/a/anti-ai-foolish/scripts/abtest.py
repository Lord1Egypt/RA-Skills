# -*- coding: utf-8 -*-
"""scripts/abtest.py —— 全量规则在52片段朱雀语料上的A/B验证，回写 status 到规则库。
判定：confirmed（CI不含0且|d|≥0.10）/ reversed（人味方向过CI）/ no_signal / insufficient（触发<5）。
meta与豁免规则不参与。结果存 validation/results/abtest_results.json 并更新 rules/*.json。"""
import os, re, io, json, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scanner import load_rules, kilo

corpus = [c for c in json.load(io.open(os.path.join(HERE, 'validation', 'corpus', 'zhuque_corpus.json'), encoding='utf-8')) if c['text'] and len(c['text']) > 200]
N = len(corpus); aigc = [c['aigc'] for c in corpus]; texts = [c['text'] for c in corpus]

def stats(fired):
    n1 = sum(fired); n0 = N - n1
    if n1 == 0 or n0 == 0: return None
    m1 = sum(a for a, f in zip(aigc, fired) if f) / n1
    m0 = sum(a for a, f in zip(aigc, fired) if not f) / n0
    v1 = sum((a - m1) ** 2 for a, f in zip(aigc, fired) if f) / n1
    v0 = sum((a - m0) ** 2 for a, f in zip(aigc, fired) if not f) / n0
    se = (v1 / n1 + v0 / n0) ** .5
    diff = m1 - m0; lo, hi = diff - 1.96 * se, diff + 1.96 * se
    sd = (sum((a - sum(aigc) / N) ** 2 for a in aigc) / N) ** .5
    r = (m1 - m0) * ((n1 / N) * (1 - n1 / N)) ** .5 / sd if sd else 0
    return n1, m1, m0, diff, lo, hi, r

rules = load_rules()
results = {}
for r in rules:
    if r.get('mode') == 'meta' or r['category'].startswith('豁免'):
        continue
    try:
        rx = re.compile(r['pattern'], re.M)
    except re.error:
        results[r['id']] = {'status': 'regex_error'}
        continue
    if r['mode'] == 'density':
        fired = [len(rx.findall(t)) / kilo(t) > r.get('threshold', 3) for t in texts]
    else:
        fired = [bool(rx.search(t)) for t in texts]
    st = stats(fired)
    if st is None:
        results[r['id']] = {'status': 'insufficient', 'n': 0}
        continue
    n1, m1, m0, diff, lo, hi, corr = st
    if n1 < 5:
        status = 'insufficient'
    elif diff > 0.10 and lo > 0:
        status = 'confirmed'
    elif diff < -0.10 and hi < 0:
        status = 'reversed'  # 人味方向
    elif abs(diff) >= 0.15:
        status = 'directional'
    else:
        status = 'no_signal'
    results[r['id']] = {'status': status, 'n': n1, 'm1': round(m1, 3), 'm0': round(m0, 3),
                        'diff': round(diff, 3), 'ci': [round(lo, 3), round(hi, 3)], 'r': round(corr, 2)}

# 回写规则库
import glob
for f in glob.glob(os.path.join(HERE, 'rules', 'R_*.json')):
    rs = json.load(io.open(f, encoding='utf-8'))
    changed = False
    for r in rs:
        if r['id'] in results:
            res = results[r['id']]
            if res['status'] == 'regex_error':
                continue
            r['status'] = res['status']
            r['evidence'] = f"AB(n={res['n']}, diff={res.get('diff')}, CI{res.get('ci')}, r={res.get('r')})"
            changed = True
    if changed:
        io.open(f, 'w', encoding='utf-8').write(json.dumps(rs, ensure_ascii=False, indent=1))

from collections import Counter
cnt = Counter(v['status'] for v in results.values())
io.open(os.path.join(HERE, 'validation', 'results', 'abtest_results.json'), 'w', encoding='utf-8').write(json.dumps(results, ensure_ascii=False, indent=1))
print(f'验证规则 {len(results)} 条 | 片段 {N}')
print(dict(cnt))
print('\n== confirmed（AI信号）TOP15 ==')
for rid, v in sorted(results.items(), key=lambda kv: -kv[1].get('diff', 0))[:15]:
    if v['status'] == 'confirmed':
        print(f"  {rid:<16} n={v['n']:>2} diff={v['diff']:+.3f} CI{v['ci']} r={v['r']:+.2f}")
print('\n== reversed（人味信号）TOP15 ==')
for rid, v in sorted(results.items(), key=lambda kv: kv[1].get('diff', 0))[:15]:
    if v['status'] == 'reversed':
        print(f"  {rid:<16} n={v['n']:>2} diff={v['diff']:+.3f} CI{v['ci']} r={v['r']:+.2f}")
