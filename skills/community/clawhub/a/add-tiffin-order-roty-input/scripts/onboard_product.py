import json
import os
import re
from match_product_and_modifiers import load_products

SKILL_DIR = os.path.dirname(os.path.dirname(__file__))
PRODUCT_FILE = os.path.join(SKILL_DIR, 'data', 'products_roty.json')
USERS_FILE = os.path.join(SKILL_DIR, 'data', 'allowed_users.json')


def is_admin(sender_id):
    try:
        d = json.load(open(USERS_FILE))
        return str(sender_id) in d.get('admins', [])
    except Exception:
        return False


def parse_product_text(text):
    # Very permissive field extraction from pasted Firestore-like text
    def find_str(key):
        # try several patterns: key: "value", key "value", key = "value"
        patterns = [r'"?%s"?\s*[:=]\s*"([^"]+)"', r'"?%s"?\s+"([^"]+)"', r'"?%s"?\s*=\s*"([^"]+)"']
        for p in patterns:
            m = re.search(p % re.escape(key), text)
            if m:
                return m.group(1)
        # try key value without quotes
        m2 = re.search(r'\b%s\b\s+([^\s\n]+)' % re.escape(key), text)
        if m2:
            return m2.group(1).strip().strip('"')
        return None
    def find_num(key):
        patterns = [r'"?%s"?\s*[:=]\s*([0-9\.]+)', r'"?%s"?\s+([0-9\.]+)', r'"?%s"?\s*=\s*([0-9\.]+)']
        for p in patterns:
            m = re.search(p % re.escape(key), text)
            if m:
                return float(m.group(1))
        return None
    productRef = find_str('productRef')
    name = find_str('name')
    vendorReference = find_str('vendorReference')
    price = find_num('price')
    # modifiers: crude extraction of modification1Option blocks
    mods1 = re.findall(r'modification1Option\"?\s*\:.*?\[(.*?)\]', text, re.S)
    modification1Option = []
    if mods1:
        block = mods1[0]
        items = re.findall(r'\{([^}]+)\}', block)
        for it in items:
            n = re.search(r'modificationName\"?\s*\:?\s*"([^"]+)"', it)
            a = re.search(r'additionalCost\"?\s*\:?\s*([0-9\.]+)', it)
            if n:
                modification1Option.append({'modificationName': n.group(1), 'additionalCost': float(a.group(1)) if a else 0})
    # similar for modification2Option
    mods2 = re.findall(r'modification2Option\"?\s*\:.*?\[(.*?)\]', text, re.S)
    modification2Option = []
    if mods2:
        block = mods2[0]
        items = re.findall(r'\{([^}]+)\}', block)
        for it in items:
            n = re.search(r'modificationName\"?\s*\:?\s*"([^"]+)"', it)
            a = re.search(r'additionalCost\"?\s*\:?\s*([0-9\.]+)', it)
            if n:
                modification2Option.append({'modificationName': n.group(1), 'additionalCost': float(a.group(1)) if a else 0})
    # aliases: look for aliases or create defaults
    aliases = re.findall(r'aliases\"?\s*\:\s*\[(.*?)\]', text, re.S)
    alias_list = []
    if aliases:
        items = re.findall(r'"([^"]+)"', aliases[0])
        alias_list = items
    return {
        'productRef': productRef,
        'name': name,
        'vendorReference': vendorReference,
        'price': price,
        'modifier1Name': find_str('modifier1Name') or 'Selection',
        'modification1Option': modification1Option,
        'modifier2Name': find_str('modifier2Name') or 'Customisations (free unless priced)',
        'modification2Option': modification2Option,
        'aliases': alias_list
    }


def upsert_product(sender_id, text, openclaw_context=False):
    # allow OpenClaw runtime to bypass admin checks
    if not openclaw_context and not is_admin(sender_id):
        return False, 'Unauthorized: sender is not admin.'
    prod = parse_product_text(text)
    missing = []
    for k in ('productRef','name','price'):
        if not prod.get(k):
            missing.append(k)
    if missing:
        return False, 'Missing fields: %s' % ', '.join(missing)
    # load existing
    data = {}
    if os.path.exists(PRODUCT_FILE):
        try:
            data = json.load(open(PRODUCT_FILE))
        except Exception:
            data = {}
    # ensure aliases
    if not prod.get('aliases'):
        # only default conservative aliases for Non Veg as requested
        if prod['name'].lower().startswith('non'):
            prod['aliases'] = ['non veg','non-veg','nonveg','nv','nonveg tiffin','non veg tiffin']
        else:
            prod['aliases'] = [prod['name'].lower()]
    data[prod['productRef']] = prod
    json.dump(data, open(PRODUCT_FILE,'w'), indent=2)
    return True, f"✅ Product saved: {prod['name']} ({prod['productRef']})"


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('Usage: onboard_product.py <sender_id> <file_with_product_text>')
        sys.exit(1)
    sid = sys.argv[1]
    txt = open(sys.argv[2]).read()
    ok, msg = upsert_product(sid, txt)
    print(ok, msg)
