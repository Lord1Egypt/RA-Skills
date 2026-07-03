#!/usr/bin/env python3
"""立创/JLC mall comparison part selection (器件标准化的"比对选型"步骤).

Given a free-text part need (e.g. "100nF 0402 X7R"), query the JLCPCB SMT parts
catalog (live), then RANK candidates the way a manufacturable design should:

  1. JLC **basic** part (componentLibraryType=base) — avoids the per-extended-part
     assembly feeder fee, so it dominates.
  2. JLC **preferred** flag — a quality/availability signal.
  3. **In stock** (>= the build qty) — out-of-stock is heavily penalized.
  4. **Cheapest** unit price at the build qty — the tiebreaker.

Prints the comparison table + the recommended LCSC C-number, which then feeds
schematic.component.place (map C# → EasyEDA device via lib_Device.search) and
tools/standard-parts.json, making standardization DATA-DRIVEN instead of arbitrary.

    parts-select.py "100nF 0402 X7R" [--qty 100] [--n 20] [--json]

Data source: JLCPCB SMT API (selectSmtComponentList) — gives stock + base/extended
+ tiered price keyed by LCSC#. No API key; needs network (the daemon/tool has it,
the webview connector does not — so this lives tool-side, not in the connector).
"""
import json
import re
import sys
import urllib.request


def norm(s):
    """Normalize value text so '10kohm', '10kΩ', '10k' all collapse to '10k'."""
    s = str(s or '').lower().replace('µ', 'u').replace('μ', 'u')
    s = s.replace('ω', '').replace('ohms', '').replace('ohm', '')
    return re.sub(r'\s+', ' ', s)


def relevance(c, qterms):
    """How many normalized query terms appear in the candidate's value text."""
    text = norm(f"{c.get('componentModelEn', '')} {c.get('describe', '')} "
                f"{c.get('componentSpecificationEn', '')} {c.get('componentTypeEn', '')}")
    return sum(1 for t in qterms if t in text)

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      'Chrome/136 Safari/537.36')
JLC_URL = ('https://jlcpcb.com/api/overseas-pcb-order/v1/'
           'shoppingCart/smtGood/selectSmtComponentList')


def jlc_search(keyword, n=20, library_type=None):
    payload = {'keyword': keyword, 'currentPage': 1, 'pageSize': n}
    if library_type:
        payload['componentLibraryType'] = library_type   # 'base' filters to JLC basic parts
    req = urllib.request.Request(
        JLC_URL, data=json.dumps(payload).encode(),
        headers={'Content-Type': 'application/json', 'User-Agent': UA})
    r = json.load(urllib.request.urlopen(req, timeout=15))
    return (r.get('data') or {}).get('componentPageInfo', {}).get('list', []) or []


def unit_price_at(prices, qty):
    """Unit price for the tier covering `qty` (fallback: first/last tier)."""
    if not prices:
        return None
    for p in prices:
        lo = p.get('startNumber', 1) or 1
        hi = p.get('endNumber') or 10 ** 12
        if lo <= qty <= hi:
            return p.get('productPrice')
    return prices[0].get('productPrice')


def select(keyword, qty=100, n=20):
    # JLC's default search returns only extended parts in the top page; the few
    # BASIC parts must be requested explicitly. The base library per category is
    # small (~tens), but the wanted basic (e.g. the 10k C25744) can rank below other
    # basic 0402 parts, so fetch a generous page. Merge both, dedup by C#.
    seen, cands = set(), []
    for c in jlc_search(keyword, 50, library_type='base') + jlc_search(keyword, n):
        code = c.get('componentCode')
        if code and code not in seen:
            seen.add(code)
            cands.append(c)
    qterms = [t for t in norm(keyword).split() if t]
    ranked = []
    for c in cands:
        stock = c.get('stockCount') or 0
        unit = float(unit_price_at(c.get('componentPrices'), qty) or 9.99)
        ranked.append({
            'lcsc': c.get('componentCode'),
            'mpn': c.get('componentModelEn'),
            'brand': c.get('componentBrandEn'),
            'desc': c.get('describe') or c.get('componentSpecificationEn'),
            'relevance': relevance(c, qterms),
            'base': c.get('componentLibraryType') == 'base',
            'preferred': bool(c.get('preferredComponentFlag')),
            'stock': stock, 'in_stock': stock >= qty, 'unit': unit,
        })
    # Spec match FIRST (drop candidates whose value doesn't match — a cheap basic
    # 220pF must not win a 10k query); THEN buildable (stock >= qty, so the pick can
    # actually be ordered); THEN basic (no feeder fee); preferred; cheapest. A basic
    # part with too little stock thus yields to an in-stock part — buildability wins.
    maxrel = max((r['relevance'] for r in ranked), default=0)
    if maxrel:
        ranked = [r for r in ranked if r['relevance'] >= maxrel]
    ranked.sort(key=lambda r: (r['relevance'], r['in_stock'], r['base'],
                               r['preferred'], -r['unit']), reverse=True)
    return ranked


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print('usage: parts-select.py "<query>" [--qty N] [--n M] [--json]', file=sys.stderr)
        return 2
    av = sys.argv[1:]
    qty = int(av[av.index('--qty') + 1]) if '--qty' in av else 100
    n = int(av[av.index('--n') + 1]) if '--n' in av else 20
    ranked = select(args[0], qty, n)
    if '--json' in av:
        print(json.dumps(ranked, ensure_ascii=False, indent=1))
        return 0
    print(f'query="{args[0]}"  qty={qty}  candidates={len(ranked)}\n')
    print(f"{'#':>2} {'LCSC':>10} {'type':<7} {'stock':>9} {'unit@'+str(qty):>9}  MPN / desc")
    for i, r in enumerate(ranked[:10], 1):
        tag = 'BASIC' if r['base'] else 'ext'
        low = '' if r['in_stock'] else '!'      # ! = stock < build qty
        print(f"{i:>2} {str(r['lcsc']):>10} {tag:<7} {r['stock']:>8}{low:1} {str(r['unit']):>9}  "
              f"{str(r['mpn'])[:20]:<20} {str(r['desc'])[:34]}")
    best = ranked[0] if ranked else None
    if best:
        warn = '' if best['in_stock'] else (
            f"  ⚠ 库存 {best['stock']} < {qty},可能不够;表中带库存的可作替代")
        print(f"\n✅ 推荐: {best['lcsc']} ({best['mpn']}) — "
              f"{'BASIC' if best['base'] else 'extended'}, 库存 {best['stock']}, "
              f"单价@{qty} {best['unit']}{warn}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
