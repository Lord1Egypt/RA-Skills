import re
from datetime import datetime, timedelta, date
try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo('Australia/Melbourne')
except Exception:
    TZ = None

WEEKDAYS = {
    'monday':0,'tuesday':1,'wednesday':2,'thursday':3,'friday':4,'saturday':5,'sunday':6
}


def extract_phone(text):
    m = re.search(r"(\+?\d[\d \-()]{6,}\d)", text)
    return m.group(1).strip() if m else ""


def extract_email(text):
    m = re.search(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", text)
    return m.group(1) if m else ""


def parse_dates(text, reference=None):
    """Return list of date objects (naive) in Australia/Melbourne for tokens like 'tomorrow', 'wed to fri', '28 days'."""
    if reference is None:
        reference = datetime.now(TZ).date()
    text_low = text.lower()
    dates = []
    # tomorrow
    if 'tomorrow' in text_low:
        dates.append(reference + timedelta(days=1))
    # e.g., 'wed to fri' or 'wednesday to friday' or 'wed-fri'
    m = re.search(r"(mon|tue|wed|thu|fri|sat|sun)(?:day)?\s*[-–to]{1,3}\s*(mon|tue|wed|thu|fri|sat|sun)(?:day)?", text_low)
    if m:
        start = m.group(1); end = m.group(2)
        start_idx = WEEKDAYS[[k for k in WEEKDAYS.keys() if k.startswith(start)][0]]
        end_idx = WEEKDAYS[[k for k in WEEKDAYS.keys() if k.startswith(end)][0]]
        cur = reference
        days_ahead = (start_idx - cur.weekday() + 7) % 7
        if days_ahead == 0:
            days_ahead = 7
        start_date = cur + timedelta(days=days_ahead)
        d = start_date
        while True:
            dates.append(d)
            if d.weekday() == end_idx:
                break
            d = d + timedelta(days=1)
    # '28 days'
    m2 = re.search(r"(\d{1,3})\s+days", text_low)
    if m2:
        n = int(m2.group(1))
        for i in range(n):
            dates.append(reference + timedelta(days=i+1))
    # single weekday names
    for wd in WEEKDAYS.keys():
        if re.search(r"\b"+wd+r"\b", text_low):
            idx = WEEKDAYS[wd]
            days_ahead = (idx - reference.weekday() + 7) % 7
            if days_ahead == 0:
                days_ahead = 7
            dates.append(reference + timedelta(days=days_ahead))
    uniq = sorted(list({d for d in dates}))
    return uniq


def parse_message(text, extra_stop_aliases=None):
    # remove trigger words
    body = re.sub(r'(?i)rot[y]?\s*input', '', text)
    body = re.sub(r'(?i)\broty\b', '', body)
    # dynamic stop tokens include product aliases
    base_stop = ['veg','non veg','non-veg','tiffin','6 rotis','3 roti','rice','extra','normal','no','tomorrow','mon','tue','wed','thu','fri','sat','sun','to','-','–','28 days','days','special','request']
    extra = [a.lower() for a in (extra_stop_aliases or [])]
    stop_tokens = base_stop + extra
    addr_start = None
    m_addr_start = re.search(r"\b(\d{1,4})\b", body)
    if m_addr_start:
        addr_start = m_addr_start.start()
        substr = body[addr_start:]
        stop_pos = None
        for t in stop_tokens:
            m = re.search(r"\b"+re.escape(t)+r"\b", substr, re.I)
            if m:
                pos = m.start()
                if stop_pos is None or pos < stop_pos:
                    stop_pos = pos
        if stop_pos is not None:
            address = substr[:stop_pos].strip().strip(' ,')
        else:
            addr_end = re.search(r"[\.\;\n]", substr)
            if addr_end:
                address = substr[:addr_end.start()].strip()
            else:
                address = substr.strip()
    else:
        address = ""
    phone = extract_phone(body)
    email = extract_email(body)
    # name extraction: if a plausible human name appears BEFORE the address, use it
    name = ''
    name_m = re.search(r"name\s*[:=]\s*([A-Za-z'\-\s]+)", body, re.I)
    if name_m:
        name = name_m.group(1).strip()
    else:
        if address and addr_start:
            before = body[:addr_start].strip()
            m2 = re.search(r"([A-Za-z]+\s+[A-Za-z]+)", before)
            if m2:
                candidate = m2.group(1).strip()
                if not re.search(r"\b(?:veg|rotis?|roti|tiffin|extra|rice|no|tomorrow|days?)\b", candidate, re.I):
                    name = ' '.join([w.capitalize() for w in candidate.split()])
        if not name and address:
            street_match = re.search(r"\d+\s+([A-Za-z0-9'\.\-]+)", address)
            if street_match:
                name = street_match.group(1).strip()
    # product intent keywords
    intent = None
    if re.search(r'(?i)\bveg\b|\bveg tiffin\b', body):
        intent = 'veg'
    elif re.search(r'(?i)\bnon[- ]?veg\b|\bnonveg\b|\bchicken\b|\bmeat\b', body):
        intent = 'non-veg'
    # modifiers
    mod1 = None
    m = re.search(r"(\d+)\s*rotis?", body)
    if m:
        mod1 = m.group(1) + ' rotis'
    if not mod1:
        m2 = re.search(r"(3|2)\s*roti", body)
        if m2:
            mod1 = m2.group(1) + ' roti'
    # modifier2 candidates
    mod2 = None
    if re.search(r'(?i)extra rice', body):
        mod2 = 'Extra Rice'
    elif re.search(r'(?i)no side dish|no side', body):
        mod2 = 'No Side Dish'
    elif re.search(r'(?i)normal', body):
        mod2 = 'Normal'
    # special requests: remove address and extracted name and known tokens, then collapse whitespace
    tmp = body
    if address:
        tmp = tmp.replace(address, ' ')
    if name:
        tmp = re.sub(re.escape(name), ' ', tmp, flags=re.I)
    for token in [phone or '', email or '', 'veg', 'non-veg', 'nonveg', 'non veg', 'extra rice', 'normal', 'extra', 'no', 'tiffin', 'curry', 'both curries', 'rice', 'rotis', 'rotis?']:
        if token:
            tmp = re.sub(re.escape(token), ' ', tmp, flags=re.I)
    tmp = re.sub(r"\b(6|3|2|\d+|rotis?|roti|tomorrow|wed|fri|mon|tue|thu|sat|sun|to|and|days?)\b", ' ', tmp, flags=re.I)
    notes = ' '.join(tmp.split()).strip()
    dates = parse_dates(text)
    # Normalize address abbreviations and title-case suburb
    def normalize_address(addr):
        if not addr:
            return addr
        a = addr
        a = re.sub(r"\b(st)\b", 'Street', a, flags=re.I)
        a = ' '.join([w.capitalize() for w in a.split()])
        a = re.sub(r"(Street)\s+(Glen Waverley)", r"\1, \2", a)
        return a
    address = normalize_address(address)
    return {
        'customerName': name,
        'userAddress': address,
        'customerPhoneNumber': phone,
        'customerEmail': email,
        'intent': intent,
        'mod1': mod1,
        'mod2': mod2,
        'specialRequests': notes,
        'deliveryDates': dates
    }


if __name__ == '__main__':
    import sys
    txt = ' '.join(sys.argv[1:])
    print(parse_message(txt))
