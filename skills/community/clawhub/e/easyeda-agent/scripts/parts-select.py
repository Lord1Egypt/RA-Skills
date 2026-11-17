#!/usr/bin/env python3
"""器件标准化的「比对选型」步骤 — 本地库优先,在线为显式 opt-in.

Given a free-text part need (e.g. "100nF 0402 X7R"), resolve it in two tiers:

  TIER 1 (default, OFFLINE) — search the curated standard-parts library
    (references/standard-parts.json). Deterministic, BOM-ready, already carries
    the deviceUuid needed by schematic.component.place. No network touched.

  TIER 2 (--online, explicit opt-in) — query the live JLCPCB SMT catalog and
    RANK candidates the way a manufacturable design should:
      1. JLC **basic** part (componentLibraryType=base) — avoids the
         per-extended-part assembly feeder fee, so it dominates.
      2. JLC **preferred** flag — a quality/availability signal.
      3. **In stock** (>= the build qty) — out-of-stock is heavily penalized.
      4. **Cheapest** unit price at the build qty — the tiebreaker.
    NOTE: this is the ONLY code path that talks to jlcpcb.com, and it never
    runs unless --online is passed (issue #177: no silent second network path
    besides the daemon). After picking a C-number, resolve its EasyEDA device
    identity DETERMINISTICALLY with the CLI — do not re-search by free text:

        easyeda lib by-lcsc --lcsc <C-number>

    then place via schematic.component.place { libraryUuid, uuid }, and ADD the
    part to standard-parts.json so the next design resolves offline.

    parts-select.py "<query>" [--qty N] [--n M] [--json] [--online]

Data source (--online only): JLCPCB SMT API (selectSmtComponentList) — stock +
base/extended + tiered price keyed by LCSC#. No API key; needs network (the
daemon/tool has it, the webview connector does not — so this lives tool-side).
"""
import json
import os
import re
import sys
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
STANDARD_PARTS = os.path.normpath(
    os.path.join(HERE, '..', 'references', 'standard-parts.json'))

USAGE = (
    'usage: parts-select.py "<query>" [--qty N] [--n M] [--json] [--online]\n'
    '\n'
    '  default        offline resolve against references/standard-parts.json\n'
    '  --online       ALSO query the live JLCPCB catalog (explicit opt-in;\n'
    '                 the only mode that touches the network)\n'
    '  --qty N        build quantity for stock/price ranking (default 100)\n'
    '  --n M          online page size (default 20)\n'
    '  --json         machine-readable output\n'
    '\n'
    'After an --online pick, resolve device identity deterministically with\n'
    '  easyeda lib by-lcsc --lcsc <C-number>\n'
    'and add the part to standard-parts.json for offline reuse.')


def norm(s):
    """Normalize value text so '10kohm', '10kΩ', '10k' all collapse to '10k'."""
    s = str(s or '').lower().replace('µ', 'u').replace('μ', 'u')
    s = s.replace('ω', '').replace('ohms', '').replace('ohm', '')
    return re.sub(r'\s+', ' ', s)


def _term_hits(text, qterms):
    """How many normalized query terms appear in `text` (already normalized).
    Also matches with separators collapsed, so 'usb-c' ≈ 'usb_c' ≈ 'usbc'."""
    ctext = re.sub(r'[-_.\s]+', '', text)
    return sum(1 for t in qterms
               if t in text or re.sub(r'[-_.]+', '', t) in ctext)


# Explicit resistance is a quantity, not a substring of an MPN (#202).
# Keep SI prefix case until conversion: mΩ and MΩ differ by 10^9.
_OHM_UNIT = r'(?:Ω|Ω|(?i:ohms?))'
# A symbol always activates the gate, even when attached to malformed text.
# English unit detection needs a standalone/numeric prefix so UNIOHM stays a
# brand query. ASCII boundaries allow ordinary Chinese adjacency (33Ω电阻).
_OHM_TOKEN = re.compile(
    r'[ΩΩ]|[0-9.]+\s*[A-Za-zµμ]?\s*(?i:ohms?)|'
    r'(?<![A-Za-z0-9_])(?i:ohms?)(?![A-Za-z0-9_])')
# Detection is wider than parsing: an unsupported prefix (1uohm) or numeric
# expression (3e3ohm) must trigger rejection, not restore fuzzy recommendations.
_RESISTANCE = re.compile(
    r'(?<![A-Za-z0-9_.])(?P<number>\d+(?:\.\d+)?|\.\d+)\s*'
    r'(?P<prefix>[mMkK]?)\s*' + _OHM_UNIT + r'(?![A-Za-z0-9_]|[.,][0-9])')
_RESISTANCE_SHORT = re.compile(
    r'(?P<number>\d+(?:\.\d+)?|\.\d+)\s*(?P<prefix>[mMkKrR])')
_OHM_SCALE = {'': Decimal(1), 'r': Decimal(1), 'R': Decimal(1),
              'm': Decimal('0.001'), 'k': Decimal(1000),
              'K': Decimal(1000), 'M': Decimal(1000000)}


def _ohms(match):
    return Decimal(match['number']) * _OHM_SCALE[match['prefix']]


def _resistance_matches(text):
    # Unsupported fractions, decimal commas, inequalities and ranges must not
    # be reinterpreted as their numeric tail (1,000Ω -> 0Ω; 1/2Ω -> 2Ω).
    # Check after rstrip too, so adding whitespace after an operator cannot
    # bypass the boundary. Full fields are still parsed with fullmatch below.
    return [m for m in _RESISTANCE.finditer(text)
            if not text[:m.start()].rstrip().endswith(tuple('.,/+-*^<>=~≤≥±×÷−'))]


def _resistance_query(keyword):
    """Gate only explicit Ω/ohm requests; malformed/ambiguous values fail closed.

    The remaining query terms still rank footprint/category/text, after the
    quantity matches. A bare MPN or a non-resistance query keeps its old behavior.
    """
    matches = _resistance_matches(keyword)
    units = list(_OHM_TOKEN.finditer(keyword))
    if not units:
        return False, None, keyword
    values = {_ohms(m) for m in matches}
    if len(matches) != len(units) or len(values) != 1:
        return True, None, keyword
    return True, next(iter(values)), _RESISTANCE.sub(' ', keyword)


def _resistance_value(value, shorthand=False):
    """Read an entire declared resistance field, never an MPN/key/other number."""
    text = str(value or '').strip()
    match = _RESISTANCE.fullmatch(text)
    if not match and shorthand:
        # Curated res.* entries also use conventional field values like 1M/10k.
        # This rule is deliberately NOT applied to online descriptions or MPNs.
        match = _RESISTANCE_SHORT.fullmatch(text)
    return _ohms(match) if match else None


def _description_resistances(description):
    """Return all explicit quantities, or None for a malformed unit expression."""
    text = str(description or '')
    matches = _resistance_matches(text)
    if len(matches) != len(list(_OHM_TOKEN.finditer(text))):
        return None
    return {_ohms(m) for m in matches}


def _resistance_evidence(raw, ohms, source):
    return {'raw': raw, 'ohms': format(ohms.normalize(), 'f'), 'source': source}


def _local_resistance(key, part):
    if not key.startswith('res.'):
        return None
    raw = part.get('value')
    ohms = _resistance_value(raw, shorthand=True)
    description = _description_resistances(part.get('desc'))
    if ohms is None or description is None or description - {ohms}:
        return None
    return _resistance_evidence(raw, ohms, 'standard-parts.value')


def _online_resistance(candidate):
    # The category must say resistor. A matching inductor DCR/ferrite impedance
    # is not the requested component; a Resistance attribute alone is insufficient.
    category = str(candidate.get('componentTypeEn') or candidate.get('secondSortName') or '')
    if not re.search(r'\bresistors?\b|电阻', category, re.IGNORECASE):
        return None
    attrs = candidate.get('attributes') or []
    if not isinstance(attrs, list):
        return None
    declared = [a.get('attribute_value_name') for a in attrs if isinstance(a, dict)
                and str(a.get('attribute_name_en') or '').strip().lower() in ('resistance', '阻值')]
    description = _description_resistances(candidate.get('describe'))
    if description is None:
        return None
    if declared:
        values = {_resistance_value(value) for value in declared}
        if None in values or len(values) != 1 or description - values:
            return None
        return _resistance_evidence(declared[0], next(iter(values)), 'attributes.Resistance')
    # A typed resistor with one unambiguous, explicitly unit-bearing description
    # may serve as a fallback; all other fields (including MPN) remain excluded.
    if len(description) == 1:
        match = _RESISTANCE.search(str(candidate.get('describe') or ''))
        return _resistance_evidence(match.group(), next(iter(description)), 'describe')
    return None


# ── TIER 1: offline standard-parts.json ─────────────────────────────────────

def local_select(keyword):
    """Rank curated standard parts by query-term relevance (offline)."""
    try:
        with open(STANDARD_PARTS, encoding='utf-8') as f:
            parts = json.load(f).get('parts', {})
    except (OSError, json.JSONDecodeError) as e:
        print(f'warn: cannot read {STANDARD_PARTS}: {e}', file=sys.stderr)
        return []
    resistance_query, requested_ohms, remaining = _resistance_query(keyword)
    if resistance_query and requested_ohms is None:
        return []
    qterms = [t for t in norm(remaining).split() if t]
    ranked = []
    for key, p in parts.items():
        resistance = _local_resistance(key, p)
        if resistance_query and (not resistance or Decimal(resistance['ohms']) != requested_ohms):
            continue
        # Identity fields (key/value/mpn/lcsc) weigh double vs. prose fields —
        # a desc that merely *mentions* "100nF" (e.g. an RC-filter note on a
        # resistor) must not tie with the actual 100nF cap.
        ident = norm(f"{key.replace('.', ' ').replace('_', ' ')} {p.get('value', '')} "
                     f"{p.get('mpn', '')} {p.get('lcsc', '')}")
        prose = norm(f"{p.get('desc', '')} {p.get('footprint', '')} "
                     f"{p.get('manufacturer', '')}")
        rel = 2 * _term_hits(ident, qterms) + _term_hits(prose, qterms) + int(resistance_query)
        if rel == 0:
            continue
        ranked.append({
            'source': 'standard-parts', 'key': key,
            'lcsc': p.get('lcsc'), 'mpn': p.get('mpn'),
            'brand': p.get('manufacturer'), 'desc': p.get('desc'),
            'deviceUuid': p.get('deviceUuid'),
            'relevance': rel, 'base': bool(p.get('basic')),
            **({'resistance': resistance} if resistance else {}),
        })
    maxrel = max((r['relevance'] for r in ranked), default=0)
    ranked = [r for r in ranked if r['relevance'] >= maxrel]
    ranked.sort(key=lambda r: (r['relevance'], r['base']), reverse=True)
    return ranked


# ── TIER 2: live JLCPCB catalog (opt-in via --online) ───────────────────────

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      'Chrome/136 Safari/537.36')
JLC_URL = ('https://jlcpcb.com/api/overseas-pcb-order/v1/'
           'shoppingCart/smtGood/selectSmtComponentList')


def jlc_search(keyword, n=20, library_type=None):
    import urllib.request  # imported here: offline default never loads the network stack
    payload = {'keyword': keyword, 'currentPage': 1, 'pageSize': n}
    if library_type:
        payload['componentLibraryType'] = library_type   # 'base' filters to JLC basic parts
    req = urllib.request.Request(
        JLC_URL, data=json.dumps(payload).encode(),
        headers={'Content-Type': 'application/json', 'User-Agent': UA})
    r = json.load(urllib.request.urlopen(req, timeout=15))
    return (r.get('data') or {}).get('componentPageInfo', {}).get('list', []) or []


def relevance(c, qterms):
    """How many normalized query terms appear in the candidate's value text."""
    text = norm(f"{c.get('componentModelEn', '')} {c.get('describe', '')} "
                f"{c.get('componentSpecificationEn', '')} {c.get('componentTypeEn', '')}")
    return _term_hits(text, qterms)


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
    resistance_query, requested_ohms, remaining = _resistance_query(keyword)
    if resistance_query and requested_ohms is None:
        return []
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
    qterms = [t for t in norm(remaining).split() if t]
    ranked = []
    for c in cands:
        resistance = _online_resistance(c)
        if resistance_query and (not resistance or Decimal(resistance['ohms']) != requested_ohms):
            continue
        stock = c.get('stockCount') or 0
        unit = float(unit_price_at(c.get('componentPrices'), qty) or 9.99)
        ranked.append({
            'source': 'jlcpcb.com',
            'lcsc': c.get('componentCode'),
            'mpn': c.get('componentModelEn'),
            'brand': c.get('componentBrandEn'),
            'desc': c.get('describe') or c.get('componentSpecificationEn'),
            'relevance': relevance(c, qterms) + int(resistance_query),
            'base': c.get('componentLibraryType') == 'base',
            'preferred': bool(c.get('preferredComponentFlag')),
            'stock': stock, 'in_stock': stock >= qty, 'unit': unit,
            **({'resistance': resistance} if resistance else {}),
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


# ── output ──────────────────────────────────────────────────────────────────

def print_local(ranked, query):
    print(f'query="{query}"  source=standard-parts.json (offline)  candidates={len(ranked)}\n')
    print(f"{'#':>2} {'LCSC':>12} {'type':<7} {'key':<24}  MPN / desc")
    for i, r in enumerate(ranked[:10], 1):
        tag = 'BASIC' if r['base'] else 'ext'
        print(f"{i:>2} {str(r['lcsc']):>12} {tag:<7} {str(r['key'])[:24]:<24}  "
              f"{str(r['mpn'])[:20]:<20} {str(r['desc'])[:40]}")
    best = ranked[0]
    print(f"\n✅ 推荐: {best['lcsc']} ({best['mpn']}) — 标准件库 `{best['key']}`, "
          f"deviceUuid={best['deviceUuid']}")
    if best.get('resistance'):
        r = best['resistance']
        print(f"   阻值原文: {r['raw']} = {r['ohms']} Ω; 来源: {r['source']}")
    print("   直接用于 schematic.component.place;需复核身份时: "
          f"easyeda lib by-lcsc --lcsc {best['lcsc']}")


def print_online(ranked, query, qty):
    print(f'query="{query}"  source=jlcpcb.com (--online)  qty={qty}  candidates={len(ranked)}\n')
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
        if best.get('resistance'):
            r = best['resistance']
            print(f"   阻值原文: {r['raw']} = {r['ohms']} Ω; 来源: {r['source']}")
        print(f"   下一步(确定性解析设备身份): easyeda lib by-lcsc --lcsc {best['lcsc']}")
        print("   选定后请把该件补进 references/standard-parts.json,下次即可离线命中")


def main():
    av = sys.argv[1:]
    if '--help' in av or '-h' in av:
        print(USAGE)
        return 0
    args = [a for a in av if not a.startswith('--')]
    if not args:
        print(USAGE, file=sys.stderr)
        return 2
    qty = int(av[av.index('--qty') + 1]) if '--qty' in av else 100
    n = int(av[av.index('--n') + 1]) if '--n' in av else 20
    online = '--online' in av
    query = args[0]
    resistance_query, _, _ = _resistance_query(query)

    local = local_select(query)
    if not online:
        if '--json' in av:
            print(json.dumps(local, ensure_ascii=False, indent=1))
            return int(resistance_query and not local)
        if local:
            print_local(local, query)
        else:
            print(f'query="{query}"  source=standard-parts.json (offline)  candidates=0\n')
            if resistance_query:
                print('显式阻值未找到经来源证实的电阻候选；不作模糊推荐。')
                return 1
            print('本地标准件库无匹配。两条路(不自动联网):')
            print('  1. 加 --online 显式启用 jlcpcb.com 在线目录比对(库存/价格/basic)')
            print('  2. 已知 C 号时直接: easyeda lib by-lcsc --lcsc <C-number>;'
                  ' 或 easyeda lib search --query "…"')
        return 0

    ranked = select(query, qty, n)
    if '--json' in av:
        # same flat-list shape as the pre-#177 script (plus a 'source' field)
        print(json.dumps(ranked, ensure_ascii=False, indent=1))
        return int(resistance_query and not ranked)
    if local:
        print_local(local, query)
        print('\n── 在线比对 (--online) ──\n')
    print_online(ranked, query, qty)
    if resistance_query and not ranked:
        print('显式阻值未找到经来源证实的在线电阻候选；不作模糊推荐。')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
