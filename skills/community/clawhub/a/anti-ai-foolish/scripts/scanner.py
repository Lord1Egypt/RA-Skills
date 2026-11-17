# -*- coding: utf-8 -*-
"""scanner.py —— anti-ai-foolish 规则引擎。
用法:
  python scripts/scanner.py <文本.md/txt> [--json out.json] [--no-exempt]
加载 rules/ 全部分库 → 剥信源备注 → 应用豁免 → 逐条扫描 → 报告（按severity分层，含fix建议）。
输出 Z分（确认AI规则命中 − 确认人味规则命中）。"""
import os, re, io, json, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_DIR = os.path.join(HERE, 'rules')

def load_rules():
    rules = []
    for f in sorted(os.listdir(RULES_DIR)):
        if f.startswith('R_') and f.endswith('.json'):
            rules.extend(json.load(io.open(os.path.join(RULES_DIR, f), encoding='utf-8')))
    return rules

def strip_body(text):
    for mark in ('**信源备注**', '**处理说明**', '\n---\n'):
        i = text.find(mark)
        if i > 200:
            text = text[:i]
    return re.sub(r'^\s*#+.*$', '', text, flags=re.M).strip()

def kilo(t):
    return max(len(t) / 1000, 0.3)

def scan(text, use_exempt=True):
    body = strip_body(text)
    rules = load_rules()
    exempt_pats = [r['pattern'] for r in rules if r['category'].startswith('豁免')]
    hits, humane, info = [], [], []
    z_ai = z_hu = 0
    for r in rules:
        if r.get('mode') == 'meta':
            info.append((r['id'], r['name'], r['fix']))
            continue
        try:
            rx = re.compile(r['pattern'], re.M)
        except re.error:
            continue
        if r['mode'] == 'density':
            val = len(rx.findall(body)) / kilo(body)
            fired = val > r.get('threshold', 3)
            detail = f'{val:.1f}/千字 (阈值{r["threshold"]})'
        else:
            m = rx.search(body)
            fired = bool(m)
            detail = (m.group(0)[:24] if m else '')
        if not fired:
            continue
        if use_exempt and r.get('exempt_when') and any(re.search(p, body or '') or p in (r.get('exempt_when') or '') for p in []):
            continue
        entry = {'id': r['id'], 'name': r['name'], 'category': r['category'], 'severity': r['severity'],
                 'direction': r['direction'], 'status': r.get('status', 'untested'), 'detail': detail,
                 'fix': r.get('fix', ''), 'source': r.get('source', '')}
        if r['direction'] == '人味':
            humane.append(entry)
            if r.get('status') == 'reversed':  # 人味方向的确认态在abtest里叫 reversed
                z_hu += 1
        elif r['direction'] == 'AI':
            hits.append(entry)
            if r.get('status') == 'confirmed':
                z_ai += 1
        else:
            info.append((r['id'], r['name'], r.get('fix', '')))
    return {
        'chars': len(body),
        'z_score': z_ai - z_hu,
        'z_components': {'AI确认命中': z_ai, '人味确认命中': z_hu},
        'AI_hits_by_severity': {sev: [h for h in hits if h['severity'] == sev] for sev in ('high', 'mid', 'low')},
        'AI_hit_total': len(hits),
        'humane_hits': humane,
        'meta': info,
        'verdict': '高危（建议逐条处理high）' if any(h['severity'] == 'high' and h['status'] == 'confirmed' for h in hits)
                   else ('中危（处理high+mid）' if [h for h in hits if h['severity'] == 'high'] else '低危'),
    }

def render(rep, path):
    out = [f"# anti-ai-foolish 扫描报告 — {os.path.basename(path)}", '',
           f"正文 {rep['chars']} 字 | **Z分 = {rep['z_score']}**（AI确认{rep['z_components']['AI确认命中']} − 人味确认{rep['z_components']['人味确认命中']}；Z>0判AI侧，r=0.813）",
           f"AI向命中 {rep['AI_hit_total']} 条 | 人味命中 {len(rep['humane_hits'])} 条 | 结论：{rep['verdict']}", '']
    for sev, title in (('high', '高危（实测确认项优先处理）'), ('mid', '中危'), ('low', '低危/参考')):
        hs = rep['AI_hits_by_severity'].get(sev, [])
        if hs:
            out.append(f"## {title} ({len(hs)})")
            for h in hs[:80]:
                st = {'confirmed': '✓实测', 'reversed': '✗已反转', 'no_signal': '—无信号', 'insufficient': '□未覆盖', 'untested': '○未测'}.get(h['status'], h['status'])
                out.append(f"- **{h['id']} {h['name']}** [{st}] {h['detail']} → {h['fix'] or '见规则库'}（{h['category']}）")
            out.append('')
    hh = rep['humane_hits']
    if hh:
        out.append(f"## 人味命中 ({len(hh)}) — 保留，勿修")
        for h in hh[:40]:
            out.append(f"- {h['id']} {h['name']} {h['detail']}")
    return '\n'.join(out)

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    path = args[0]
    import os as _os
    _p = _os.path.abspath(_os.path.realpath(path))
    if not _os.path.isfile(_p) or _os.path.splitext(_p)[1].lower() not in ('.md', '.txt', '.markdown'):
        raise SystemExit('输入必须是存在的 .md/.txt 文件: %s' % _p)
    text = io.open(_p, encoding='utf-8').read()
    rep = scan(text)
    md = render(rep, path)
    print(md)
    if '--json' in sys.argv:
        out = sys.argv[sys.argv.index('--json') + 1]
        io.open(out, 'w', encoding='utf-8').write(json.dumps(rep, ensure_ascii=False, indent=1))
        print(f'\n[json → {out}]')
