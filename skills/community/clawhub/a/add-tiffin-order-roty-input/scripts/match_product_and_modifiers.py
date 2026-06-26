import json
import os
import re
from difflib import get_close_matches

SKILL_DIR = os.path.dirname(os.path.dirname(__file__))
PRODUCT_FILE = os.path.join(SKILL_DIR, 'data', 'products_roty.json')


def load_products():
    with open(PRODUCT_FILE, 'r') as f:
        return json.load(f)


def get_all_aliases():
    products = load_products()
    aliases = []
    for p in products.values():
        for a in p.get('aliases', []):
            aliases.append(a.lower())
    return aliases


def find_product_by_intent_or_alias(text, intent_text):
    products = load_products()
    text_low = (text or '').lower()
    # special-case: explicit 'curry only' phrase -> prefer exact product name
    if 'curry only' in text_low or 'curry-only' in text_low:
        for pref, p in products.items():
            if p.get('name','').lower().startswith('curry only'):
                return pref, p
    # 1) exact alias match anywhere in text (longest-first)
    alias_map = {}
    for pref, p in products.items():
        for a in p.get('aliases', []):
            alias_map[a.lower()] = pref
    # check for alias presence
    matches = []
    for alias, pref in alias_map.items():
        if alias in text_low:
            matches.append((len(alias), alias, pref))
    if matches:
        # pick longest alias match
        matches.sort(reverse=True)
        chosen_pref = matches[0][2]
        return chosen_pref, products[chosen_pref]
    # special-case: prefer curry-only product if phrase present
    if 'curry only' in text_low or 'curry-only' in text_low:
        for pref, p in products.items():
            if 'curry' in p.get('name','').lower():
                # prefer product whose name contains 'curry'
                return pref, p
    # fallback: use intent_text (veg/non-veg)
    if not intent_text:
        return None, None
    it = intent_text.lower()
    for pref, p in products.items():
        aliases = [a.lower() for a in p.get('aliases', [])]
        if it in aliases:
            return pref, p
    # fuzzy match against aliases using intent_text
    matches = get_close_matches(it, alias_map.keys(), n=1, cutoff=0.7)
    if matches:
        return alias_map[matches[0]], products[alias_map[matches[0]]]
    return None, None


def match_modifiers(product, mod1_text, mod2_text, raw_text=''):
    # choose modifier1 option
    m1 = None
    m2 = None
    if product is None:
        return None, None
    opts1 = product.get('modification1Option', [])
    opts2 = product.get('modification2Option', [])
    # Curry-only normalization: detect patterns in raw_text or mod1_text
    pname = product.get('name','').lower()
    norm = None
    t = ((mod1_text or '') + ' ' + raw_text).lower()
    if 'curry' in pname and 'curry only' in pname:
        # normalize patterns for Curry Only
        if re.search(r"\b2\s*veg\s*1\s*non[- ]?veg\b|\b2v1nv\b", t):
            norm = '2 Veg, 1 Non Veg (+$2)'
        elif re.search(r"\b1\s*veg\s*2\s*non[- ]?veg\b|\b1v2nv\b", t):
            norm = '1 Veg, 2 Non Veg (+$4)'
        elif re.search(r"\b3\s*non[- ]?veg\b|\bthree\s*non[- ]?veg\b", t):
            norm = '3 Non Veg (+$6)'
        elif re.search(r"\b3\s*veg\b|\bthree\s*veg\b", t):
            norm = '3 Veg'
    # Non-Veg product normalization
    if 'non' in pname or 'non veg' in pname or 'non-veg' in pname:
        if re.search(r"\b6\s*rotis?\b", t):
            norm = '6 Rotis'
        elif re.search(r"\bonly\s+rice\b|\brice\s+only\b", t):
            norm = 'Only Rice (580ml)'
        elif (re.search(r"\b3\s*rotis?\b", t) and re.search(r"\brice\b", t)) or re.search(r"\b3\s*rotis?\s*\+\s*rice\b", t) or re.search(r"\b3\s*roti\s*rice\b", t):
            norm = '3 Rotis, Rice (280ml)'
    if norm:
        # find exact match in opts1
        found = False
        for o in opts1:
            if o['modificationName'].lower() == norm.lower():
                m1 = o
                found = True
                break
        if not found:
            # synthesize a modifier object when product registry lacks options
            # infer additionalCost from known patterns
            add = 0
            if '+$2' in norm or ' +$2' in norm or '(+$2)' in norm:
                add = 2
            if '+$4' in norm or '(+$4)' in norm:
                add = 4
            if '+$6' in norm or '(+$6)' in norm:
                add = 6
            m1 = {'modificationName': norm, 'additionalCost': add}
    if not m1 and mod1_text:
        names1 = [o['modificationName'].lower() for o in opts1]
        mt = mod1_text.lower()
        matches = get_close_matches(mt, names1, n=1, cutoff=0.5)
        if matches:
            idx = names1.index(matches[0])
            m1 = opts1[idx]
    if not m1 and opts1:
        m1 = opts1[0]
    # modifier2
    # modifier2 normalization for Non-Veg and general cases
    norm2 = None
    if 'non' in pname or 'non-veg' in pname or 'non veg' in pname:
        if re.search(r"both\s+curries\s*.*non[- ]?veg|all\s+non[- ]?veg", t):
            norm2 = 'Both Curries as Non-Veg (+$2)'
        elif re.search(r"extra\s+rice", t):
            norm2 = 'Extra Rice (+$2)'
        elif re.search(r"extra\s*2\s*rotis?|extra\s*2\s*rotis", t):
            norm2 = 'Extra 2 Rotis (+$2)'
    # general
    if not norm2 and mod2_text:
        names2 = [o['modificationName'].lower() for o in opts2]
        mt2 = mod2_text.lower()
        matches2 = get_close_matches(mt2, names2, n=1, cutoff=0.5)
        if matches2:
            idx2 = names2.index(matches2[0])
            m2 = opts2[idx2]
    if norm2:
        found2 = False
        for o in opts2:
            if o['modificationName'].lower() == norm2.lower():
                m2 = o
                found2 = True
                break
        if not found2:
            add2 = 0
            if '+$2' in norm2 or '(+$2)' in norm2:
                add2 = 2
            if '+$4' in norm2 or '(+$4)' in norm2:
                add2 = 4
            if '+$6' in norm2 or '(+$6)' in norm2:
                add2 = 6
            m2 = {'modificationName': norm2, 'additionalCost': add2}
    # default mod2 to Normal if present
    if not m2 and any(o['modificationName'].lower()=='normal' for o in opts2):
        m2 = next(o for o in opts2 if o['modificationName'].lower()=='normal')
    if not m2 and opts2:
        m2 = opts2[0]
    return m1, m2

if __name__ == '__main__':
    import sys
    intent = sys.argv[1] if len(sys.argv)>1 else ''
    mod1 = sys.argv[2] if len(sys.argv)>2 else ''
    mod2 = sys.argv[3] if len(sys.argv)>3 else ''
    pref, p = find_product_by_intent(intent)
    print('pref=', pref)
    print('product=', p)
    print('mods=', match_modifiers(p, mod1, mod2))

if __name__ == '__main__':
    import sys
    intent = sys.argv[1] if len(sys.argv)>1 else ''
    mod1 = sys.argv[2] if len(sys.argv)>2 else ''
    mod2 = sys.argv[3] if len(sys.argv)>3 else ''
    pref, p = find_product_by_intent(intent)
    print('pref=', pref)
    print('product=', p)
    print('mods=', match_modifiers(p, mod1, mod2))
