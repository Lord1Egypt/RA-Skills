"""
Shared utilities for doc-process scripts.
"""

import re
import unicodedata
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# CSV injection prevention
# ---------------------------------------------------------------------------

_CSV_INJECTION_PREFIXES = ('=', '+', '-', '@', '\t', '\r', '\n')


def sanitize_csv_value(value: str) -> str:
    """
    Prevent CSV formula injection and strip control characters.
    Ref: OWASP CSV Injection.
    """
    if not isinstance(value, str):
        value = str(value)
    # Strip null bytes and control characters (except tab/newline handled below)
    value = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', value)
    value = value.strip()
    if value and value[0] in _CSV_INJECTION_PREFIXES:
        value = "'" + value
    return value


# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------

def safe_output_path(requested_path: str, allowed_dir: str | None = None) -> Path:
    """
    Resolve a file path and reject path traversal and null-byte attacks.
    Raises ValueError for unsafe paths.
    """
    if '\x00' in requested_path:
        raise ValueError("Path contains null byte.")
    resolved = Path(requested_path).resolve()
    if allowed_dir is not None:
        allowed = Path(allowed_dir).resolve()
        try:
            resolved.relative_to(allowed)
        except ValueError:
            raise ValueError(
                f"Path '{requested_path}' is outside the allowed directory '{allowed_dir}'"
            )
    return resolved


# ---------------------------------------------------------------------------
# Date parsing
# ---------------------------------------------------------------------------

_DATE_FORMATS = [
    # ISO variants
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%Y%m%d",
    # With time (strip time part first)
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    # Day-first
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%d.%m.%Y",
    "%d %m %Y",
    # Month-first (US)
    "%m/%d/%Y",
    "%m-%d-%Y",
    "%m.%d.%Y",
    # Short year
    "%d/%m/%y",
    "%m/%d/%y",
    "%d.%m.%y",
    # Verbose
    "%d %b %Y",
    "%d %B %Y",
    "%b %d, %Y",
    "%B %d, %Y",
    "%b %d %Y",
    "%B %d %Y",
    # Compact verbal
    "%d-%b-%Y",
    "%d-%B-%Y",
    "%b-%d-%Y",
]


def parse_date(date_str: str) -> datetime:
    """Parse a date string in any supported format. Returns datetime or raises ValueError."""
    if not date_str or not date_str.strip():
        raise ValueError("Empty date string.")
    date_str = date_str.strip()

    # Strip trailing timezone designators like "+00:00" or " UTC"
    date_str = re.sub(r'[\s+\-]\d{2}:\d{2}$', '', date_str)
    date_str = re.sub(r'\s*[A-Z]{2,5}$', '', date_str).strip()

    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    raise ValueError(
        f"Unrecognised date format: '{date_str}'. "
        "Supported: YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY, DD.MM.YYYY, "
        "DD Mon YYYY, Mon DD YYYY, YYYYMMDD, and variants with time."
    )


def normalise_date(date_str: str) -> str:
    """Return ISO 8601 date string (YYYY-MM-DD), or raise ValueError."""
    return parse_date(date_str).strftime("%Y-%m-%d")


# ---------------------------------------------------------------------------
# Amount parsing
# ---------------------------------------------------------------------------

# Comprehensive currency symbol regex
_CURRENCY_SYMBOLS = r'[£$€¥₹₩₪₺₽฿₫₦₲₡₵₴₸₼₾₠₢₣¢₤₨＄￡￥]'


def parse_amount(amount_str) -> float:
    """
    Parse a monetary amount string to a float.

    Handles:
    - US format:        $1,234.56  →  1234.56
    - European format:  €1.234,56  →  1234.56
    - Space thousands:  1 234,56   →  1234.56
    - Parenthetical:    (42.00)    →  -42.00
    - Currency codes:   USD 12.50  →  12.50
    - Signed:           -42.00, +12.00
    - Integers:         1000       →  1000.0
    - None / empty      raises ValueError
    """
    if amount_str is None:
        raise ValueError("Amount is None.")
    if isinstance(amount_str, (int, float)):
        return round(float(amount_str), 4)

    s = str(amount_str).strip()
    if not s:
        raise ValueError(f"Could not parse amount: '{amount_str}'")

    # Parenthetical negative: (42.00) → -42.00
    negative = False
    if s.startswith('(') and s.endswith(')'):
        negative = True
        s = s[1:-1].strip()

    # Strip currency symbols
    s = re.sub(_CURRENCY_SYMBOLS, '', s).strip()

    # Strip leading/trailing ISO currency codes (USD, EUR, GBP…)
    s = re.sub(r'^[A-Za-z]{2,3}\s+', '', s).strip()
    s = re.sub(r'\s+[A-Za-z]{2,3}$', '', s).strip()

    # Handle explicit sign
    if s.startswith('-'):
        negative = True
        s = s[1:].strip()
    elif s.startswith('+'):
        s = s[1:].strip()

    if not s:
        raise ValueError(f"Could not parse amount: '{amount_str}'")

    # Remove spaces (thousands separator in some EU locales)
    s_ns = s.replace('\u00a0', '').replace(' ', '')  # also strip non-breaking space

    has_comma = ',' in s_ns
    has_dot = '.' in s_ns

    if has_comma and has_dot:
        # Whichever is rightmost is the decimal separator
        if s_ns.rfind(',') > s_ns.rfind('.'):
            # EU: 1.234,56
            s_clean = s_ns.replace('.', '').replace(',', '.')
        else:
            # US: 1,234.56
            s_clean = s_ns.replace(',', '')

    elif has_comma and not has_dot:
        parts = s_ns.split(',')
        if len(parts) == 2 and len(parts[1]) == 3 and parts[0].lstrip('-+').isdigit():
            # Likely US thousands with no decimal: 1,234
            s_clean = s_ns.replace(',', '')
        elif len(parts) > 2:
            # Multiple commas → US thousands grouping: 1,234,567
            s_clean = s_ns.replace(',', '')
        else:
            # EU decimal: 1234,56 or 1,23
            s_clean = s_ns.replace(',', '.')

    elif has_dot and not has_comma:
        parts = s_ns.split('.')
        if len(parts) > 2:
            # Multiple dots → EU thousands: 1.234.567
            s_clean = s_ns.replace('.', '')
        else:
            # Single dot → decimal separator
            s_clean = s_ns

    else:
        # No separators → plain integer
        s_clean = s_ns

    if not s_clean or s_clean in ('.', ','):
        raise ValueError(f"Could not parse amount: '{amount_str}'")

    try:
        value = float(s_clean)
        if negative:
            value = -abs(value)
        return round(value, 4)
    except ValueError:
        raise ValueError(f"Could not parse amount: '{amount_str}'")


# ---------------------------------------------------------------------------
# Currency detection
# ---------------------------------------------------------------------------

_CURRENCY_CODE_RE = re.compile(
    r'\b(USD|EUR|GBP|JPY|CAD|AUD|CHF|CNY|CNH|HKD|SGD|INR|KRW|MXN|BRL|'
    r'SEK|NOK|DKK|NZD|ZAR|AED|SAR|QAR|KWD|BHD|OMR|EGP|NGN|KES|IDR|MYR|'
    r'THB|PHP|VND|PKR|BDT|LKR|TWD|CZK|PLN|HUF|RON|BGN|HRK|RSD|TRY|RUB|'
    r'UAH|ILS|ARS|CLP|COP|PEN|UYU|PYG|BOB|GTQ|HNL|CRC|DOP|JMD|TTD|BBD)\b'
)


def detect_currency(text: str) -> str:
    """
    Detect ISO currency code from a string. Returns code or 'USD' as default.
    """
    if not text:
        return "USD"
    m = _CURRENCY_CODE_RE.search(text.upper())
    if m:
        return m.group(1)
    # Symbol fallback
    symbol_map = {
        '£': 'GBP', '€': 'EUR', '¥': 'JPY', '₹': 'INR', '₩': 'KRW',
        '₪': 'ILS', '₺': 'TRY', '₽': 'RUB', '฿': 'THB', '₫': 'VND',
        '₦': 'NGN', '₲': 'PYG', '₡': 'CRC', '₵': 'GHS', '₴': 'UAH',
        '₸': 'KZT', 'R$': 'BRL', 'S$': 'SGD', 'HK$': 'HKD', 'NT$': 'TWD',
    }
    for sym, code in symbol_map.items():
        if sym in text:
            return code
    return "USD"


# ---------------------------------------------------------------------------
# Category taxonomy
# ---------------------------------------------------------------------------

EXPENSE_CATEGORIES: dict[str, list[str]] = {
    "Food & Dining": [
        "Restaurants", "Groceries", "Coffee & Cafes", "Bars & Alcohol",
        "Food Delivery", "Fast Food", "Bubble Tea", "Bakery",
    ],
    "Travel": [
        "Flights", "Hotels & Lodging", "Car Rental", "Taxis & Rideshare",
        "Parking", "Fuel", "Public Transit", "Travel Packages",
    ],
    "Office & Supplies": [
        "Office Supplies", "Printing", "Postage & Shipping", "Furniture",
    ],
    "Technology": [
        "Software & SaaS", "Hardware", "Phone & Internet",
        "Cloud Services", "Cybersecurity",
    ],
    "Professional Services": [
        "Legal", "Accounting", "Consulting", "Recruiting", "Freelance",
    ],
    "Marketing": ["Advertising", "Design", "Events", "PR & Communications"],
    "Health & Medical": [
        "Doctor & Clinic", "Pharmacy", "Insurance",
        "Gym & Wellness", "Mental Health", "Dental & Vision",
    ],
    "Entertainment": [
        "Streaming", "Music & Audio", "Gaming", "Events & Tickets", "Books & Media",
    ],
    "Utilities": [
        "Electricity", "Water", "Gas", "Waste", "Phone & Internet",
    ],
    "Education": [
        "Online Courses", "Books", "Conferences", "Certifications",
        "Language Learning", "Tuition",
    ],
    "Retail & Shopping": [
        "Online Shopping", "Department Stores", "Clothing & Apparel",
        "Electronics", "Home & Garden", "Furniture & Home", "Personal Care",
    ],
    "Financial Services": [
        "Banking Fees", "Investment", "Insurance Premiums", "Loan Payments",
        "Cryptocurrency",
    ],
    "Other": [
        "Miscellaneous", "Payment Services", "ATM & Cash", "Uncategorized",
    ],
}

ALL_CATEGORIES: set[str] = set(EXPENSE_CATEGORIES.keys())
ALL_SUBCATEGORIES: set[str] = {
    sub for subs in EXPENSE_CATEGORIES.values() for sub in subs
}


def validate_category(category: str, subcategory: str = "") -> tuple[str, str]:
    """
    Validate category and subcategory. Case-insensitive matching.
    Returns (canonical_category, subcategory) or raises ValueError with suggestions.
    """
    # Case-insensitive category lookup
    cat_map = {c.lower(): c for c in ALL_CATEGORIES}
    matched_cat = cat_map.get(category.lower())
    if not matched_cat:
        # Suggest closest
        suggestions = [c for c in ALL_CATEGORIES if category.lower() in c.lower()]
        hint = f" Did you mean: {', '.join(suggestions)}?" if suggestions else \
               f" Valid: {', '.join(sorted(ALL_CATEGORIES))}"
        raise ValueError(f"Unknown category '{category}'.{hint}")

    if subcategory:
        valid_subs = EXPENSE_CATEGORIES[matched_cat]
        sub_map = {s.lower(): s for s in valid_subs}
        matched_sub = sub_map.get(subcategory.lower())
        if not matched_sub:
            suggestions = [s for s in valid_subs if subcategory.lower() in s.lower()]
            hint = f" Did you mean: {', '.join(suggestions)}?" if suggestions else \
                   f" Valid for '{matched_cat}': {', '.join(valid_subs)}"
            raise ValueError(f"Unknown subcategory '{subcategory}'.{hint}")
        return matched_cat, matched_sub

    return matched_cat, ""


# ---------------------------------------------------------------------------
# Global merchant patterns for auto-categorisation
# (regex pattern, category, subcategory)
# Ordered: more specific patterns before broader ones.
# ---------------------------------------------------------------------------

MERCHANT_PATTERNS: list[tuple[str, str, str]] = [

    # ── STREAMING ─────────────────────────────────────────────────────────────
    (r"netflix", "Entertainment", "Streaming"),
    (r"hulu", "Entertainment", "Streaming"),
    (r"disney\+|disneyplus", "Entertainment", "Streaming"),
    (r"apple\s*tv\+?(?!\s*store)", "Entertainment", "Streaming"),
    (r"paramount\+|paramountplus|cbs\s*all\s*access", "Entertainment", "Streaming"),
    (r"peacock\s*(?:tv|premium)?", "Entertainment", "Streaming"),
    (r"hbo\s*max|\bmax\s*(?:streaming|subscription)", "Entertainment", "Streaming"),
    (r"discovery\+|discoveryplus", "Entertainment", "Streaming"),
    (r"amazon\s*prime\s*video|prime\s*video", "Entertainment", "Streaming"),
    (r"crunchyroll|funimation", "Entertainment", "Streaming"),
    (r"mubi|criterion\s*channel|shudder|britbox|acorn\s*tv", "Entertainment", "Streaming"),
    (r"youtube\s*premium", "Entertainment", "Streaming"),
    (r"espn\+|espnplus", "Entertainment", "Streaming"),
    (r"sling\s*tv|fubotv?|philo\s*tv|directv\s*stream", "Entertainment", "Streaming"),
    (r"tubi\s*tv|pluto\s*tv|plex\s*(?:pass|tv)?", "Entertainment", "Streaming"),
    (r"viu\b|iflix|catchplay|bilibili|iqiyi|youku|mango\s*tv", "Entertainment", "Streaming"),   # Asia
    (r"wavve|tving|watcha|laftel|seezn|kakao\s*tv", "Entertainment", "Streaming"),              # Korea
    (r"hotstar|jio\s*cinema|zee5|voot|sony\s*liv|eros\s*now|alt\s*balaji", "Entertainment", "Streaming"),  # India
    (r"vidio|mola\s*tv|genflix", "Entertainment", "Streaming"),                                  # Indonesia
    (r"iptv|stan\b|binge\b|foxtel\s*(?:now|go)?", "Entertainment", "Streaming"),                # Australia

    # ── MUSIC ─────────────────────────────────────────────────────────────────
    (r"spotify", "Entertainment", "Streaming"),
    (r"apple\s*music", "Entertainment", "Music & Audio"),
    (r"tidal\b", "Entertainment", "Music & Audio"),
    (r"amazon\s*music", "Entertainment", "Music & Audio"),
    (r"youtube\s*music", "Entertainment", "Music & Audio"),
    (r"deezer", "Entertainment", "Music & Audio"),
    (r"soundcloud", "Entertainment", "Music & Audio"),
    (r"pandora", "Entertainment", "Music & Audio"),
    (r"qobuz|napster|iheartradio|bandcamp", "Entertainment", "Music & Audio"),

    # ── GAMING ────────────────────────────────────────────────────────────────
    (r"xbox\s*(?:game\s*pass|live|gold)|microsoft\s*gaming", "Entertainment", "Gaming"),
    (r"playstation|psn\b|ps\s*(?:now|plus|store)", "Entertainment", "Gaming"),
    (r"nintendo(?:\s*eshop)?", "Entertainment", "Gaming"),
    (r"steam(?:\s*games|\s*purchase)?", "Entertainment", "Gaming"),
    (r"epic\s*games", "Entertainment", "Gaming"),
    (r"ea\s*(?:play|origin)|\borigin\.com", "Entertainment", "Gaming"),
    (r"battle\.net|blizzard\s*entertainment", "Entertainment", "Gaming"),
    (r"ubisoft|uplay\b", "Entertainment", "Gaming"),
    (r"discord\s*nitro", "Entertainment", "Gaming"),
    (r"roblox|minecraft|valorant|fortnite|genshin", "Entertainment", "Gaming"),

    # ── EVENTS & TICKETS ──────────────────────────────────────────────────────
    (r"ticketmaster|ticketek|sistic|axs\.com|eventbrite|stubhub|viagogo|dice\.fm", "Entertainment", "Events & Tickets"),
    (r"amc\s*theatre|regal\s*cinema|cinemark|imax\b|cineplex|odeon|cineworld|vue\s*cinema", "Entertainment", "Events & Tickets"),
    (r"golden\s*village|cathay\s*cineplexes|shaw\s*theatres|gsc\s*cinemas|tgv\s*cinemas", "Entertainment", "Events & Tickets"),  # SEA

    # ── FOOD DELIVERY ─────────────────────────────────────────────────────────
    (r"uber\s*eats", "Food & Dining", "Food Delivery"),
    (r"doordash", "Food & Dining", "Food Delivery"),
    (r"grubhub", "Food & Dining", "Food Delivery"),
    (r"postmates", "Food & Dining", "Food Delivery"),
    (r"instacart", "Food & Dining", "Food Delivery"),
    (r"swiggy", "Food & Dining", "Food Delivery"),
    (r"zomato", "Food & Dining", "Food Delivery"),
    (r"deliveroo", "Food & Dining", "Food Delivery"),
    (r"foodpanda|food\s*panda", "Food & Dining", "Food Delivery"),
    (r"grabfood|grab\s*food", "Food & Dining", "Food Delivery"),
    (r"rappi", "Food & Dining", "Food Delivery"),
    (r"ifood\b", "Food & Dining", "Food Delivery"),
    (r"pedidosya|pedidos\s*ya", "Food & Dining", "Food Delivery"),
    (r"wolt\b", "Food & Dining", "Food Delivery"),
    (r"glovo", "Food & Dining", "Food Delivery"),
    (r"just\s*eat|justeat|menulog|skip\s*the\s*dishes|skipthedishes", "Food & Dining", "Food Delivery"),
    (r"talabat", "Food & Dining", "Food Delivery"),
    (r"noon\s*food|careem\s*food|hungerstation", "Food & Dining", "Food Delivery"),
    (r"meituan|ele\.me|baidu\s*waimai", "Food & Dining", "Food Delivery"),
    (r"baemin|yogiyo|coupang\s*eats", "Food & Dining", "Food Delivery"),
    (r"demaecan", "Food & Dining", "Food Delivery"),

    # ── COFFEE & CAFES ────────────────────────────────────────────────────────
    (r"starbucks", "Food & Dining", "Coffee & Cafes"),
    (r"dunkin(?:\s*donuts)?", "Food & Dining", "Coffee & Cafes"),
    (r"tim\s*hortons", "Food & Dining", "Coffee & Cafes"),
    (r"peet'?s\s*coffee", "Food & Dining", "Coffee & Cafes"),
    (r"blue\s*bottle\s*coffee", "Food & Dining", "Coffee & Cafes"),
    (r"costa\s*coffee", "Food & Dining", "Coffee & Cafes"),
    (r"caffe\s*nero", "Food & Dining", "Coffee & Cafes"),
    (r"second\s*cup", "Food & Dining", "Coffee & Cafes"),
    (r"gloria\s*jean'?s", "Food & Dining", "Coffee & Cafes"),
    (r"the\s*coffee\s*bean", "Food & Dining", "Coffee & Cafes"),
    (r"caribou\s*coffee", "Food & Dining", "Coffee & Cafes"),
    (r"mccafe|mc\s*cafe", "Food & Dining", "Coffee & Cafes"),
    (r"nespresso|nescafe|lavazza|segafredo|illy\s*caffe", "Food & Dining", "Coffee & Cafes"),
    (r"hollys\s*coffee|ediya|coffee\s*bene|twosome\s*place|paik'?s\s*coffee", "Food & Dining", "Coffee & Cafes"),  # Korea
    (r"doutor|komeda|st\s*marc\s*cafe|tully'?s", "Food & Dining", "Coffee & Cafes"),            # Japan
    (r"old\s*town\s*white\s*coffee|zus\s*coffee|tealive", "Food & Dining", "Coffee & Cafes"),   # Malaysia
    (r"ya\s*kun|toast\s*box|killiney\s*kopitiam", "Food & Dining", "Coffee & Cafes"),           # Singapore
    (r"kopi\s*kenangan|fore\s*coffee|janji\s*jiwa", "Food & Dining", "Coffee & Cafes"),         # Indonesia

    # ── BUBBLE TEA ────────────────────────────────────────────────────────────
    (r"gong\s*cha|kung\s*fu\s*tea|tiger\s*sugar|koi\s*the|xing\s*fu\s*tang|moge\s*tee", "Food & Dining", "Bubble Tea"),
    (r"chatime|coco\s*(?:fresh|boba)?|share\s*tea|the\s*alley|r&b\s*tea|presotea|tp\s*tea", "Food & Dining", "Bubble Tea"),
    (r"tpumkin|boba\s*guys|kung\s*tea|tiger\s*milk\s*tea|happy\s*lemon", "Food & Dining", "Bubble Tea"),

    # ── FAST FOOD ─────────────────────────────────────────────────────────────
    (r"mcdonald'?s|mcdonalds|mcd\b|golden\s*arches", "Food & Dining", "Fast Food"),
    (r"burger\s*king", "Food & Dining", "Fast Food"),
    (r"wendy'?s", "Food & Dining", "Fast Food"),
    (r"kfc|kentucky\s*fried\s*chicken", "Food & Dining", "Fast Food"),
    (r"subway(?!\s*(?:train|metro|station|transit|rail))", "Food & Dining", "Fast Food"),
    (r"pizza\s*hut", "Food & Dining", "Fast Food"),
    (r"domino'?s(?:\s*pizza)?", "Food & Dining", "Fast Food"),
    (r"taco\s*bell", "Food & Dining", "Fast Food"),
    (r"chick-?fil-?a", "Food & Dining", "Fast Food"),
    (r"five\s*guys", "Food & Dining", "Fast Food"),
    (r"shake\s*shack", "Food & Dining", "Fast Food"),
    (r"in-?n-?out\s*burger", "Food & Dining", "Fast Food"),
    (r"popeyes\s*(?:louisiana)?", "Food & Dining", "Fast Food"),
    (r"chipot?le", "Food & Dining", "Fast Food"),
    (r"panda\s*express", "Food & Dining", "Fast Food"),
    (r"wingstop|wing\s*stop|buffalo\s*wild\s*wings|bww\b", "Food & Dining", "Fast Food"),
    (r"sonic\s*drive-?in", "Food & Dining", "Fast Food"),
    (r"jack\s*in\s*the\s*box", "Food & Dining", "Fast Food"),
    (r"carl'?s\s*jr|hardee'?s|whataburger", "Food & Dining", "Fast Food"),
    (r"papa\s*john'?s|little\s*caesars", "Food & Dining", "Fast Food"),
    (r"nando'?s|wagamama|itsu\b|leon\b|pret\s*a\s*manger|pret\b", "Food & Dining", "Fast Food"),  # UK
    (r"greggs\b", "Food & Dining", "Bakery"),
    (r"krispy\s*kreme|cinnabon|auntie\s*anne'?s", "Food & Dining", "Bakery"),
    (r"jollibee", "Food & Dining", "Fast Food"),                                                  # Philippines
    (r"mos\s*burger|lotteria|yoshinoya|sukiya|matsuya|gyudon|pepper\s*lunch", "Food & Dining", "Fast Food"),  # Japan/Korea
    (r"grill'?d|hungry\s*jack'?s|red\s*rooster|oporto", "Food & Dining", "Fast Food"),           # Australia

    # ── GROCERIES ─────────────────────────────────────────────────────────────
    # US / Canada
    (r"walmart(?!\s*(?:pharmacy|vision|auto|money|credit))", "Food & Dining", "Groceries"),
    (r"costco", "Food & Dining", "Groceries"),
    (r"sam'?s\s*club", "Food & Dining", "Groceries"),
    (r"kroger", "Food & Dining", "Groceries"),
    (r"whole\s*foods", "Food & Dining", "Groceries"),
    (r"trader\s*joe'?s", "Food & Dining", "Groceries"),
    (r"safeway", "Food & Dining", "Groceries"),
    (r"albertsons", "Food & Dining", "Groceries"),
    (r"publix", "Food & Dining", "Groceries"),
    (r"h-?e-?b\b", "Food & Dining", "Groceries"),
    (r"meijer", "Food & Dining", "Groceries"),
    (r"wegmans", "Food & Dining", "Groceries"),
    (r"harris\s*teeter", "Food & Dining", "Groceries"),
    (r"stop\s*&\s*shop", "Food & Dining", "Groceries"),
    (r"shoprite", "Food & Dining", "Groceries"),
    (r"aldi(?!\s*(?:cafe|coffee))", "Food & Dining", "Groceries"),
    (r"food\s*lion|sprouts\s*farmers|fresh\s*market|market\s*basket", "Food & Dining", "Groceries"),
    (r"winco\s*foods|grocery\s*outlet|save-?a-?lot", "Food & Dining", "Groceries"),
    (r"winn-?dixie|jewel-?osco|randalls|tom\s*thumb|vons|ralphs|pavilions|king\s*soopers", "Food & Dining", "Groceries"),
    (r"loblaws|sobeys|maxi\b|provigo|iga\s*canada|metro\s*(?:inc|grocery|épicerie)", "Food & Dining", "Groceries"),
    # UK / Ireland
    (r"tesco(?!\s*(?:bank|mobile))", "Food & Dining", "Groceries"),
    (r"sainsbury'?s", "Food & Dining", "Groceries"),
    (r"asda", "Food & Dining", "Groceries"),
    (r"waitrose(?!\s*(?:uae|me|middle\s*east))", "Food & Dining", "Groceries"),
    (r"m&s\s*food|marks\s*&\s*spencer\s*food", "Food & Dining", "Groceries"),
    (r"lidl", "Food & Dining", "Groceries"),
    (r"iceland\s*foods", "Food & Dining", "Groceries"),
    (r"co-?op\s*(?:food|group)?", "Food & Dining", "Groceries"),
    (r"morrisons", "Food & Dining", "Groceries"),
    (r"dunnes\s*stores", "Food & Dining", "Groceries"),
    # France
    (r"carrefour(?!\s*(?:sa\s*?|uae|egypt|kenya|maroc))", "Food & Dining", "Groceries"),
    (r"e\.\s*leclerc|leclerc\b", "Food & Dining", "Groceries"),
    (r"intermarche|intermarché", "Food & Dining", "Groceries"),
    (r"auchan", "Food & Dining", "Groceries"),
    (r"monoprix|franprix|naturalia|biocoop|systeme\s*u|système\s*u", "Food & Dining", "Groceries"),
    # Germany / Austria / Switzerland
    (r"rewe\b", "Food & Dining", "Groceries"),
    (r"edeka", "Food & Dining", "Groceries"),
    (r"netto\s*marken-?discount", "Food & Dining", "Groceries"),
    (r"penny\s*markt", "Food & Dining", "Groceries"),
    (r"billa(?!\s*(?:creek))", "Food & Dining", "Groceries"),
    (r"migros", "Food & Dining", "Groceries"),
    (r"coop\s*(?:schweiz|suisse|supermarkt)?", "Food & Dining", "Groceries"),
    # Spain / Italy / Netherlands / Nordics
    (r"mercadona", "Food & Dining", "Groceries"),
    (r"dia\s*(?:supermarket)?", "Food & Dining", "Groceries"),
    (r"eroski|consum\b|plusfresc", "Food & Dining", "Groceries"),
    (r"esselunga|conad|eurospin\b", "Food & Dining", "Groceries"),
    (r"albert\s*heijn|jumbo\s*(?:supermarkt)?|plus\s*supermarkt", "Food & Dining", "Groceries"),
    (r"ica\s*(?:maxi|kvantum|nara|supermarket)?|willys|hemkop", "Food & Dining", "Groceries"),
    (r"rema\s*1000|kiwi\s*(?:minipris)?|bunnpris|joker\s*(?:butikk)?", "Food & Dining", "Groceries"),
    (r"k-?market|k-?ruoka|prisma\b|s-?market|sale\b|alepa\b", "Food & Dining", "Groceries"),
    # Asia-Pacific
    (r"fairprice|ntuc\s*fairprice|cold\s*storage|sheng\s*siong|prime\s*supermarket", "Food & Dining", "Groceries"),  # SG
    (r"aeon(?!\s*(?:insurance|credit|bank|mall\s*(?!food)))", "Food & Dining", "Groceries"),
    (r"ito\s*yokado|daiei|york\s*mart|seiyu\b|tokyustore", "Food & Dining", "Groceries"),
    (r"parknshop|wellcome\s*(?:supermarket)?|citysuper|fusion\s*superstore", "Food & Dining", "Groceries"),
    (r"99\s*ranch|h\s*mart|mitsuwa|nijiya|marukai|t&t\s*supermarket", "Food & Dining", "Groceries"),
    (r"big\s*c|lotus'?s|tops\s*(?:market|supermarket)|villa\s*market", "Food & Dining", "Groceries"),
    (r"giant\s*(?:hypermarket|supermarket|superstore)|jaya\s*grocer|village\s*grocer|mydin", "Food & Dining", "Groceries"),
    (r"transmart|hypermart|superindo|lotte\s*mart|ranch\s*market|grand\s*lucky", "Food & Dining", "Groceries"),
    (r"sm\s*supermarket|puregold|robinsons\s*supermarket|rustan'?s", "Food & Dining", "Groceries"),
    (r"woolworths(?!\s*(?:financial|sa|south\s*africa))", "Food & Dining", "Groceries"),
    (r"coles(?!\s*(?:group|myer))", "Food & Dining", "Groceries"),
    (r"pak'?n'?save|new\s*world\s*(?:nz)?|countdown\s*(?:nz)?|four\s*square", "Food & Dining", "Groceries"),
    # Middle East
    (r"lulu\s*(?:hypermarket|express)?", "Food & Dining", "Groceries"),
    (r"spinneys", "Food & Dining", "Groceries"),
    (r"waitrose\s*(?:uae|me)", "Food & Dining", "Groceries"),
    (r"al\s*maya|union\s*coop|nesto\s*hypermarket", "Food & Dining", "Groceries"),
    (r"carrefour\s*(?:uae|sa|egypt|maroc|kenya)", "Food & Dining", "Groceries"),
    # South Africa
    (r"checkers(?!\s*(?:auto|hardware))", "Food & Dining", "Groceries"),
    (r"pick\s*n\s*pay|shoprite\s*(?:holdings|supermarket)?", "Food & Dining", "Groceries"),
    (r"woolworths\s*(?:sa|south\s*africa|food)", "Food & Dining", "Groceries"),
    (r"spar\s*(?:south\s*africa)?", "Food & Dining", "Groceries"),

    # ── RESTAURANTS ──────────────────────────────────────────────────────────
    (r"applebee'?s|chili'?s|ihop|denny'?s|olive\s*garden|red\s*lobster", "Food & Dining", "Restaurants"),
    (r"tgi\s*friday'?s|outback\s*steakhouse|texas\s*roadhouse|cheesecake\s*factory", "Food & Dining", "Restaurants"),
    (r"cracker\s*barrel|bob\s*evans|waffle\s*house|first\s*watch", "Food & Dining", "Restaurants"),
    (r"benihana|p\.?\s*f\.?\s*chang'?s|melting\s*pot|bonefish\s*grill", "Food & Dining", "Restaurants"),

    # ── AIRLINES ──────────────────────────────────────────────────────────────
    # Americas
    (r"delta\s*(?:air\s*lines|airlines)?", "Travel", "Flights"),
    (r"united\s*(?:airlines|air)?", "Travel", "Flights"),
    (r"american\s*(?:airlines|air)?", "Travel", "Flights"),
    (r"southwest\s*(?:airlines|air)?", "Travel", "Flights"),
    (r"jetblue\s*(?:airways)?", "Travel", "Flights"),
    (r"alaska\s*(?:airlines|air)?", "Travel", "Flights"),
    (r"spirit\s*(?:airlines)?", "Travel", "Flights"),
    (r"frontier\s*(?:airlines)?", "Travel", "Flights"),
    (r"hawaiian\s*(?:airlines)?", "Travel", "Flights"),
    (r"sun\s*country|breeze\s*airways|avelo\s*airlines", "Travel", "Flights"),
    (r"air\s*canada", "Travel", "Flights"),
    (r"westjet", "Travel", "Flights"),
    (r"porter\s*airlines", "Travel", "Flights"),
    (r"aeromexico", "Travel", "Flights"),
    (r"latam\s*(?:airlines)?", "Travel", "Flights"),
    (r"avianca", "Travel", "Flights"),
    (r"gol\s*(?:linhas|airlines)?|azul\s*(?:linhas|airlines)?", "Travel", "Flights"),
    (r"copa\s*(?:airlines)?", "Travel", "Flights"),
    # Europe
    (r"british\s*airways", "Travel", "Flights"),
    (r"lufthansa", "Travel", "Flights"),
    (r"air\s*france", "Travel", "Flights"),
    (r"klm\b", "Travel", "Flights"),
    (r"iberia\s*(?:airlines)?", "Travel", "Flights"),
    (r"swiss\s*(?:international\s*air|air\s*lines)?", "Travel", "Flights"),
    (r"austrian\s*(?:airlines)?", "Travel", "Flights"),
    (r"sas\b|scandinavian\s*airlines", "Travel", "Flights"),
    (r"finnair", "Travel", "Flights"),
    (r"norwegian\s*(?:air)?", "Travel", "Flights"),
    (r"wizz\s*air|wizzair", "Travel", "Flights"),
    (r"ryanair", "Travel", "Flights"),
    (r"easyjet", "Travel", "Flights"),
    (r"vueling|transavia|volotea", "Travel", "Flights"),
    (r"brussels\s*airlines", "Travel", "Flights"),
    (r"lot\s*(?:polish\s*airlines)?", "Travel", "Flights"),
    (r"tap\s*(?:air\s*portugal)?", "Travel", "Flights"),
    (r"alitalia|ita\s*airways", "Travel", "Flights"),
    # Middle East & Africa
    (r"emirates\s*(?:airlines)?", "Travel", "Flights"),
    (r"etihad\s*(?:airways)?", "Travel", "Flights"),
    (r"qatar\s*airways", "Travel", "Flights"),
    (r"turkish\s*(?:airlines|air)?", "Travel", "Flights"),
    (r"flydubai", "Travel", "Flights"),
    (r"air\s*arabia", "Travel", "Flights"),
    (r"ethiopian\s*(?:airlines)?", "Travel", "Flights"),
    (r"kenya\s*airways", "Travel", "Flights"),
    (r"south\s*african\s*airways", "Travel", "Flights"),
    (r"royal\s*air\s*maroc", "Travel", "Flights"),
    (r"egyptair", "Travel", "Flights"),
    # Asia-Pacific
    (r"singapore\s*airlines|silkair", "Travel", "Flights"),
    (r"cathay\s*pacific|hk\s*express|hong\s*kong\s*express", "Travel", "Flights"),
    (r"japan\s*airlines|jal\b", "Travel", "Flights"),
    (r"ana\b|all\s*nippon\s*airways", "Travel", "Flights"),
    (r"korean\s*air", "Travel", "Flights"),
    (r"asiana\s*(?:airlines)?", "Travel", "Flights"),
    (r"thai\s*(?:airways|airasia)", "Travel", "Flights"),
    (r"garuda\s*(?:indonesia)?", "Travel", "Flights"),
    (r"malaysia\s*airlines|malindo\s*air|batik\s*air", "Travel", "Flights"),
    (r"vietnam\s*airlines", "Travel", "Flights"),
    (r"(?:air)?asia|airasia", "Travel", "Flights"),
    (r"lion\s*air|wings\s*air", "Travel", "Flights"),
    (r"indigo\s*(?:airlines)?|6e\b", "Travel", "Flights"),
    (r"air\s*india", "Travel", "Flights"),
    (r"spicejet|vistara|go\s*(?:first|air|airlines)", "Travel", "Flights"),
    (r"qantas\s*(?:airways)?", "Travel", "Flights"),
    (r"jetstar\s*(?:airways)?", "Travel", "Flights"),
    (r"virgin\s*australia", "Travel", "Flights"),
    (r"air\s*new\s*zealand", "Travel", "Flights"),
    (r"cebu\s*pacific|philippine\s*airlines", "Travel", "Flights"),

    # ── HOTELS & LODGING ──────────────────────────────────────────────────────
    (r"marriott", "Travel", "Hotels & Lodging"),
    (r"hilton(?!\s*(?:honors\s*credit|garden\s*inn\s*credit))", "Travel", "Hotels & Lodging"),
    (r"hyatt", "Travel", "Hotels & Lodging"),
    (r"sheraton|westin|w\s*hotels|st\.\s*regis|ritz-?carlton|le\s*meridien|autograph\s*collection", "Travel", "Hotels & Lodging"),
    (r"intercontinental|crowne\s*plaza|holiday\s*inn|staybridge|indigo\s*hotel|kimpton\s*hotel", "Travel", "Hotels & Lodging"),
    (r"best\s*western", "Travel", "Hotels & Lodging"),
    (r"radisson(?!\s*(?:blu\s*rewards\s*credit))", "Travel", "Hotels & Lodging"),
    (r"wyndham|ramada|days\s*inn|super\s*8|la\s*quinta|microtel|travelodge|howard\s*johnson", "Travel", "Hotels & Lodging"),
    (r"choice\s*hotels|comfort\s*inn|quality\s*inn|sleep\s*inn|econo\s*lodge", "Travel", "Hotels & Lodging"),
    (r"motel\s*6|red\s*roof\s*inn|extended\s*stay|woodspring\s*suites", "Travel", "Hotels & Lodging"),
    (r"four\s*seasons", "Travel", "Hotels & Lodging"),
    (r"mandarin\s*oriental", "Travel", "Hotels & Lodging"),
    (r"sofitel|novotel|ibis(?!\s*(?:paint|styles\s*paint))|mercure|pullman|mgallery", "Travel", "Hotels & Lodging"),
    (r"accorhotels|accor\s*(?:live|hotels)", "Travel", "Hotels & Lodging"),
    (r"airbnb", "Travel", "Hotels & Lodging"),
    (r"vrbo", "Travel", "Hotels & Lodging"),
    (r"booking\.com", "Travel", "Hotels & Lodging"),
    (r"expedia(?!\s*(?:cruise|group\s*media))", "Travel", "Hotels & Lodging"),
    (r"hotels\.com", "Travel", "Hotels & Lodging"),
    (r"sonder\b|vacasa\b|blueground|furnished\s*finder", "Travel", "Hotels & Lodging"),

    # ── RIDESHARE & TAXI ──────────────────────────────────────────────────────
    (r"uber(?!\s*(?:eats|one))", "Travel", "Taxis & Rideshare"),
    (r"lyft", "Travel", "Taxis & Rideshare"),
    (r"grab(?!\s*(?:food|mart|express|financial|pay))", "Travel", "Taxis & Rideshare"),
    (r"ola\s*(?:cabs|money)?", "Travel", "Taxis & Rideshare"),
    (r"bolt(?!\s*(?:ev|electric|scooter|energy))", "Travel", "Taxis & Rideshare"),
    (r"gett\b|taxify", "Travel", "Taxis & Rideshare"),
    (r"cabify", "Travel", "Taxis & Rideshare"),
    (r"99\s*taxis|indriver", "Travel", "Taxis & Rideshare"),
    (r"didi(?!\s*(?:food|chuxing\s*invest))", "Travel", "Taxis & Rideshare"),
    (r"yandex\s*(?:taxi|go)\b", "Travel", "Taxis & Rideshare"),
    (r"gojek|gocar", "Travel", "Taxis & Rideshare"),

    # ── CAR RENTAL ────────────────────────────────────────────────────────────
    (r"hertz\b", "Travel", "Car Rental"),
    (r"avis\s*(?:car|rent|budget)?", "Travel", "Car Rental"),
    (r"budget\s*(?:car|rent\s*a\s*car)", "Travel", "Car Rental"),
    (r"enterprise\s*(?:rent|car|holdings)?", "Travel", "Car Rental"),
    (r"national\s*car\s*rental", "Travel", "Car Rental"),
    (r"alamo(?!\s*(?:drafthouse))", "Travel", "Car Rental"),
    (r"thrifty\s*(?:car)?", "Travel", "Car Rental"),
    (r"dollar\s*car\s*rental", "Travel", "Car Rental"),
    (r"sixt\s*(?:rent\s*a\s*car)?", "Travel", "Car Rental"),
    (r"europcar", "Travel", "Car Rental"),
    (r"zipcar", "Travel", "Car Rental"),
    (r"turo\b", "Travel", "Car Rental"),
    (r"getaround", "Travel", "Car Rental"),

    # ── FUEL / GAS ────────────────────────────────────────────────────────────
    (r"shell(?!\s*(?:gift|rewards|credit))", "Travel", "Fuel"),
    (r"bp\b|british\s*petroleum", "Travel", "Fuel"),
    (r"chevron(?!\s*(?:bank|card|credit))", "Travel", "Fuel"),
    (r"exxon(?:mobil)?", "Travel", "Fuel"),
    (r"texaco", "Travel", "Fuel"),
    (r"arco\b", "Travel", "Fuel"),
    (r"sunoco", "Travel", "Fuel"),
    (r"marathon\s*(?:petro|gas|fuel)?", "Travel", "Fuel"),
    (r"murphy\s*(?:usa|express)?", "Travel", "Fuel"),
    (r"casey'?s\s*(?:general\s*store)?", "Travel", "Fuel"),
    (r"circle\s*k(?!\s*convenience\s*non)", "Travel", "Fuel"),
    (r"pilot\s*(?:flying\s*j|travel\s*centers)?", "Travel", "Fuel"),
    (r"love'?s\s*(?:travel\s*stops)?", "Travel", "Fuel"),
    (r"speedway(?!\s*(?:motorsports|nascar|casino))", "Travel", "Fuel"),
    (r"wawa(?!\s*(?:inc|foundation|music))", "Travel", "Fuel"),
    (r"sheetz", "Travel", "Fuel"),
    (r"quiktrip|kwik\s*trip|racetrac|maverik|cenex|kum\s*&\s*go|thorntons", "Travel", "Fuel"),
    (r"total\s*(?:energies)?|elf\b|esso\b", "Travel", "Fuel"),
    (r"repsol", "Travel", "Fuel"),
    (r"petrobras|ipiranga|br\s*distribuidora", "Travel", "Fuel"),
    (r"pemex", "Travel", "Fuel"),
    (r"sinopec|petrochina|cnpc", "Travel", "Fuel"),
    (r"enoc\b|adnoc\b|emarat\b", "Travel", "Fuel"),
    (r"petron\b|caltex(?!\s*credit)", "Travel", "Fuel"),
    (r"pertamina", "Travel", "Fuel"),
    (r"ampol|bp\s*australia", "Travel", "Fuel"),

    # ── PUBLIC TRANSIT ────────────────────────────────────────────────────────
    (r"mta\b|nyc\s*transit|new\s*york\s*transit", "Travel", "Public Transit"),
    (r"bart\b", "Travel", "Public Transit"),
    (r"cta\b|chicago\s*transit", "Travel", "Public Transit"),
    (r"wmata\b|washington\s*metro", "Travel", "Public Transit"),
    (r"septa\b", "Travel", "Public Transit"),
    (r"clipper\s*card|orca\s*card|charlie\s*card|smartrip\s*card", "Travel", "Public Transit"),
    (r"tfl\b|transport\s*for\s*london|oyster\s*card", "Travel", "Public Transit"),
    (r"translink\b|stm\b|oc\s*transpo\b|presto\s*card", "Travel", "Public Transit"),
    (r"suica|pasmo|toica|manaca|nimoca|hayakaken", "Travel", "Public Transit"),
    (r"t-?money\b|cashbee\b", "Travel", "Public Transit"),
    (r"octopus\s*card", "Travel", "Public Transit"),
    (r"ez-?link|nets\s*flashpay", "Travel", "Public Transit"),
    (r"opal\s*card", "Travel", "Public Transit"),

    # ── CLOUD & INFRASTRUCTURE ────────────────────────────────────────────────
    (r"amazon\s*web\s*services|aws\b", "Technology", "Cloud Services"),
    (r"google\s*cloud|gcp\b", "Technology", "Cloud Services"),
    (r"microsoft\s*azure|azure\b", "Technology", "Cloud Services"),
    (r"digitalocean", "Technology", "Cloud Services"),
    (r"cloudflare", "Technology", "Cloud Services"),
    (r"linode\b|akamai\s*cloud", "Technology", "Cloud Services"),
    (r"vultr\b", "Technology", "Cloud Services"),
    (r"hetzner", "Technology", "Cloud Services"),
    (r"ovhcloud|ovh\b", "Technology", "Cloud Services"),
    (r"rackspace", "Technology", "Cloud Services"),
    (r"ibm\s*cloud", "Technology", "Cloud Services"),
    (r"oracle\s*cloud", "Technology", "Cloud Services"),
    (r"alibaba\s*cloud|aliyun", "Technology", "Cloud Services"),
    (r"tencent\s*cloud|huawei\s*cloud", "Technology", "Cloud Services"),

    # ── SOFTWARE & SaaS ───────────────────────────────────────────────────────
    (r"github", "Technology", "Software & SaaS"),
    (r"gitlab", "Technology", "Software & SaaS"),
    (r"atlassian|jira\b|confluence\b|bitbucket|trello\b", "Technology", "Software & SaaS"),
    (r"notion\b", "Technology", "Software & SaaS"),
    (r"figma\b", "Technology", "Software & SaaS"),
    (r"slack(?!\s*(?:apparel|store))", "Technology", "Software & SaaS"),
    (r"zoom(?!\s*(?:car|dental|whitening|tan))", "Technology", "Software & SaaS"),
    (r"webex", "Technology", "Software & SaaS"),
    (r"microsoft\s*365|office\s*365|microsoft\s*office", "Technology", "Software & SaaS"),
    (r"google\s*workspace|g\s*suite|google\s*one\b|google\s*drive", "Technology", "Software & SaaS"),
    (r"adobe\s*(?:creative\s*cloud|acrobat|lightroom|photoshop|illustrator|premiere|after\s*effects|substance)", "Technology", "Software & SaaS"),
    (r"dropbox(?!\s*(?:sign|paper\s*sub))", "Technology", "Software & SaaS"),
    (r"box\.com|box\s*inc", "Technology", "Software & SaaS"),
    (r"canva\b", "Technology", "Software & SaaS"),
    (r"sketch\s*(?:app)?", "Technology", "Software & SaaS"),
    (r"invision|zeplin|framer\b", "Technology", "Software & SaaS"),
    (r"linear\.app|linear\s*(?:issues)?", "Technology", "Software & SaaS"),
    (r"asana\b", "Technology", "Software & SaaS"),
    (r"monday\.com", "Technology", "Software & SaaS"),
    (r"clickup", "Technology", "Software & SaaS"),
    (r"basecamp", "Technology", "Software & SaaS"),
    (r"airtable", "Technology", "Software & SaaS"),
    (r"hubspot", "Technology", "Software & SaaS"),
    (r"salesforce", "Technology", "Software & SaaS"),
    (r"pipedrive", "Technology", "Software & SaaS"),
    (r"intercom\b", "Technology", "Software & SaaS"),
    (r"zendesk", "Technology", "Software & SaaS"),
    (r"freshdesk|freshworks", "Technology", "Software & SaaS"),
    (r"mailchimp", "Technology", "Software & SaaS"),
    (r"klaviyo|activecampaign|convertkit|sendgrid|mailgun|brevo|sendinblue", "Technology", "Software & SaaS"),
    (r"twilio\b", "Technology", "Software & SaaS"),
    (r"datadog", "Technology", "Software & SaaS"),
    (r"new\s*relic", "Technology", "Software & SaaS"),
    (r"sentry\.io|sentry\s*subscription", "Technology", "Software & SaaS"),
    (r"pagerduty", "Technology", "Software & SaaS"),
    (r"circleci|travis\s*ci", "Technology", "Software & SaaS"),
    (r"vercel\b", "Technology", "Software & SaaS"),
    (r"netlify\b", "Technology", "Software & SaaS"),
    (r"heroku\b", "Technology", "Software & SaaS"),
    (r"supabase|planetscale|neon\s*database|railway\.app|render\.com|fly\.io", "Technology", "Software & SaaS"),
    (r"jetbrains|intellij|pycharm|webstorm|goland|clion|datagrip|rider\b", "Technology", "Software & SaaS"),
    (r"quickbooks|xero\b|freshbooks|wave\s*accounting|sage\s*(?:50|intacct|accounting)", "Technology", "Software & SaaS"),
    (r"shopify\b", "Technology", "Software & SaaS"),
    (r"squarespace|wix\.com|webflow\b|wordpress\.com", "Technology", "Software & SaaS"),
    (r"loom\.com", "Technology", "Software & SaaS"),
    (r"calendly", "Technology", "Software & SaaS"),
    (r"typeform|surveymonkey|hotjar\b", "Technology", "Software & SaaS"),

    # ── CYBERSECURITY ─────────────────────────────────────────────────────────
    (r"1password|lastpass|bitwarden|dashlane|keeper\s*security", "Technology", "Cybersecurity"),
    (r"nordvpn|expressvpn|protonvpn|surfshark|private\s*internet\s*access|mullvad", "Technology", "Cybersecurity"),
    (r"norton\s*(?:360|antivirus|lifelock)?|mcafee|bitdefender|malwarebytes|crowdstrike|eset\b", "Technology", "Cybersecurity"),

    # ── TELECOM / PHONE / INTERNET ────────────────────────────────────────────
    # US
    (r"at&t(?!\s*(?:retirement|pension|savings\s*plan))", "Utilities", "Phone & Internet"),
    (r"verizon(?!\s*(?:pension|retirement|media))", "Utilities", "Phone & Internet"),
    (r"t-?mobile", "Utilities", "Phone & Internet"),
    (r"comcast|xfinity", "Utilities", "Phone & Internet"),
    (r"charter\s*communications|spectrum\b", "Utilities", "Phone & Internet"),
    (r"cox\s*communications", "Utilities", "Phone & Internet"),
    (r"dish\s*network|directv\s*(?!stream)", "Utilities", "Phone & Internet"),
    (r"centurylink|lumen\s*technologies|frontier\s*communications|windstream", "Utilities", "Phone & Internet"),
    (r"boost\s*mobile|cricket\s*wireless|metropcs|tracfone|mint\s*mobile|visible\s*wireless", "Utilities", "Phone & Internet"),
    # Canada
    (r"rogers(?!\s*(?:arena|centre))", "Utilities", "Phone & Internet"),
    (r"bell\s*(?:canada|mobility|fibe|mts)?", "Utilities", "Phone & Internet"),
    (r"telus(?!\s*garden)", "Utilities", "Phone & Internet"),
    (r"shaw\s*(?:communications)?|freedom\s*mobile|videotron|eastlink|sasktel", "Utilities", "Phone & Internet"),
    # UK
    (r"vodafone(?!\s*(?:idea|india))", "Utilities", "Phone & Internet"),
    (r"o2\s*(?:uk)?", "Utilities", "Phone & Internet"),
    (r"bt\s*(?:group|broadband|mobile)?", "Utilities", "Phone & Internet"),
    (r"sky\s*(?:uk|broadband|tv|mobile|q)?", "Utilities", "Phone & Internet"),
    (r"three\s*(?:uk)?|3\s*uk\b", "Utilities", "Phone & Internet"),
    (r"ee\b|everything\s*everywhere", "Utilities", "Phone & Internet"),
    (r"virgin\s*media", "Utilities", "Phone & Internet"),
    (r"talktalk|plusnet", "Utilities", "Phone & Internet"),
    # Europe
    (r"deutsche\s*telekom|t-?online|telekom\s*deutschland", "Utilities", "Phone & Internet"),
    (r"orange(?!\s*(?:julius|theory\s*fitness|county|bank|theory))", "Utilities", "Phone & Internet"),
    (r"sfr\b|bouygues\s*telecom|free\s*mobile|free\s*telecom", "Utilities", "Phone & Internet"),
    (r"swisscom", "Utilities", "Phone & Internet"),
    (r"salt\s*mobile|sunrise\s*uw", "Utilities", "Phone & Internet"),
    (r"proximus\b|telenet\s*belgium", "Utilities", "Phone & Internet"),
    (r"telefonica|movistar|yoigo|masmovil", "Utilities", "Phone & Internet"),
    (r"tim\s*(?:brasil|telecom\s*italia)", "Utilities", "Phone & Internet"),
    (r"telenor", "Utilities", "Phone & Internet"),
    (r"telia(?!\s*(?:company\s*arena|arena))", "Utilities", "Phone & Internet"),
    # Asia
    (r"singtel", "Utilities", "Phone & Internet"),
    (r"starhub", "Utilities", "Phone & Internet"),
    (r"m1\s*(?:limited|singapore)?", "Utilities", "Phone & Internet"),
    (r"telstra\b", "Utilities", "Phone & Internet"),
    (r"optus\b", "Utilities", "Phone & Internet"),
    (r"tpg\s*telecom|aussie\s*broadband", "Utilities", "Phone & Internet"),
    (r"airtel(?!\s*(?:africa\s*nigeria|money))", "Utilities", "Phone & Internet"),
    (r"jio\b|reliance\s*jio", "Utilities", "Phone & Internet"),
    (r"bsnl\b|vi\b|vodafone\s*idea", "Utilities", "Phone & Internet"),
    (r"globe\s*telecom|smart\s*communications|dito\s*telecom", "Utilities", "Phone & Internet"),
    (r"ntt\s*docomo|softbank(?!\s*(?:vision\s*fund|robotics))|kddi\b", "Utilities", "Phone & Internet"),
    (r"sk\s*telecom|kt\s*(?:corporation)?|lg\s*uplus", "Utilities", "Phone & Internet"),
    (r"china\s*mobile|china\s*unicom|china\s*telecom", "Utilities", "Phone & Internet"),
    (r"celcom|maxis\b|digi\s*telecom|u\s*mobile", "Utilities", "Phone & Internet"),
    (r"du\b\s*(?:telecom)?|etisalat\b|e&\b", "Utilities", "Phone & Internet"),
    (r"stc\b|mobily\b|zain\s*(?:ksa|saudi|group)?|ooredoo", "Utilities", "Phone & Internet"),
    (r"mtn\s*(?:group|nigeria|ghana|south\s*africa|uganda)?", "Utilities", "Phone & Internet"),
    (r"safaricom", "Utilities", "Phone & Internet"),

    # ── RETAIL & SHOPPING ─────────────────────────────────────────────────────
    # MUST come after specific Amazon sub-services above
    (r"amazon(?!\s*(?:web\s*services|music|prime\s*video|pay|flex|fresh|go\b))", "Retail & Shopping", "Online Shopping"),
    (r"ebay", "Retail & Shopping", "Online Shopping"),
    (r"etsy\b", "Retail & Shopping", "Online Shopping"),
    (r"aliexpress", "Retail & Shopping", "Online Shopping"),
    (r"alibaba(?!\s*cloud)", "Retail & Shopping", "Online Shopping"),
    (r"taobao|tmall|jd\.com|jingdong|pinduoduo", "Retail & Shopping", "Online Shopping"),
    (r"shopee", "Retail & Shopping", "Online Shopping"),
    (r"lazada", "Retail & Shopping", "Online Shopping"),
    (r"tokopedia|bukalapak", "Retail & Shopping", "Online Shopping"),
    (r"shein\b|temu\b|wish\.com", "Retail & Shopping", "Online Shopping"),
    # Department stores
    (r"target(?!\s*(?:optical|pharmacy|clinic))", "Retail & Shopping", "Department Stores"),
    (r"nordstrom(?!\s*rack\s*credit)", "Retail & Shopping", "Department Stores"),
    (r"bloomingdale'?s", "Retail & Shopping", "Department Stores"),
    (r"neiman\s*marcus|saks\s*fifth\s*avenue", "Retail & Shopping", "Department Stores"),
    (r"macy'?s", "Retail & Shopping", "Department Stores"),
    (r"j\.?\s*c\.?\s*penney|jcpenney", "Retail & Shopping", "Department Stores"),
    (r"kohl'?s", "Retail & Shopping", "Department Stores"),
    (r"burlington\s*(?:coat\s*factory)?", "Retail & Shopping", "Department Stores"),
    (r"tj\s*maxx|t\.?j\.?\s*maxx", "Retail & Shopping", "Department Stores"),
    (r"marshalls", "Retail & Shopping", "Department Stores"),
    (r"ross\s*(?:stores|dress\s*for\s*less)?", "Retail & Shopping", "Department Stores"),
    (r"john\s*lewis", "Retail & Shopping", "Department Stores"),
    (r"selfridges|harrods|harvey\s*nichols|house\s*of\s*fraser", "Retail & Shopping", "Department Stores"),
    (r"el\s*corte\s*ingles", "Retail & Shopping", "Department Stores"),
    (r"galeries\s*lafayette|printemps\b|bon\s*marche", "Retail & Shopping", "Department Stores"),
    (r"galeria\s*kaufhof|karstadt", "Retail & Shopping", "Department Stores"),
    (r"isetan|takashimaya|sogo\b|parco\b|tokyu\s*(?:dept|hands)", "Retail & Shopping", "Department Stores"),
    (r"david\s*jones|myer\b", "Retail & Shopping", "Department Stores"),
    (r"sm\s*(?:department\s*store|supermalls)|robinsons\s*(?:dept|malls)", "Retail & Shopping", "Department Stores"),
    # Clothing
    (r"h&m\b|h\s*and\s*m\b|hennes\s*&\s*mauritz", "Retail & Shopping", "Clothing & Apparel"),
    (r"zara(?!\s*larsson)", "Retail & Shopping", "Clothing & Apparel"),
    (r"uniqlo", "Retail & Shopping", "Clothing & Apparel"),
    (r"gap(?!\s*(?:insurance|year))", "Retail & Shopping", "Clothing & Apparel"),
    (r"mango(?!\s*(?:language|smoothie|juice))", "Retail & Shopping", "Clothing & Apparel"),
    (r"pull\s*&\s*bear|bershka|massimo\s*dutti|stradivarius", "Retail & Shopping", "Clothing & Apparel"),
    (r"primark|penneys\s*ireland", "Retail & Shopping", "Clothing & Apparel"),
    (r"asos\b", "Retail & Shopping", "Clothing & Apparel"),
    (r"boohoo|prettylittlething|plt\b|missguided|nasty\s*gal", "Retail & Shopping", "Clothing & Apparel"),
    (r"levi'?s|wrangler\b|lee\s*jeans", "Retail & Shopping", "Clothing & Apparel"),
    (r"nike\b", "Retail & Shopping", "Clothing & Apparel"),
    (r"adidas", "Retail & Shopping", "Clothing & Apparel"),
    (r"puma\b", "Retail & Shopping", "Clothing & Apparel"),
    (r"under\s*armour", "Retail & Shopping", "Clothing & Apparel"),
    (r"lululemon", "Retail & Shopping", "Clothing & Apparel"),
    (r"patagonia|the\s*north\s*face|columbia\s*sportswear|arc'?teryx", "Retail & Shopping", "Clothing & Apparel"),
    # Electronics
    (r"best\s*buy", "Retail & Shopping", "Electronics"),
    (r"b&h\s*photo|adorama", "Retail & Shopping", "Electronics"),
    (r"micro\s*center|newegg", "Retail & Shopping", "Electronics"),
    (r"apple\s*(?:store|retail|com)(?!\s*(?:tv\+|music|pay|card|fitness|one|arcade|news))", "Retail & Shopping", "Electronics"),
    (r"currys|curry'?s\s*pc\s*world|pcworld", "Retail & Shopping", "Electronics"),
    (r"mediamarkt|saturn\s*(?:electro)?", "Retail & Shopping", "Electronics"),
    (r"fnac\b", "Retail & Shopping", "Electronics"),
    (r"darty\b", "Retail & Shopping", "Electronics"),
    (r"harvey\s*norman", "Retail & Shopping", "Electronics"),
    (r"jb\s*hi-?fi", "Retail & Shopping", "Electronics"),
    # Home improvement
    (r"home\s*depot", "Retail & Shopping", "Home & Garden"),
    (r"lowe'?s(?!\s*foods)", "Retail & Shopping", "Home & Garden"),
    (r"b&q\b", "Retail & Shopping", "Home & Garden"),
    (r"bunnings\s*(?:warehouse)?", "Retail & Shopping", "Home & Garden"),
    (r"bauhaus\b", "Retail & Shopping", "Home & Garden"),
    (r"ikea", "Retail & Shopping", "Furniture & Home"),
    (r"wayfair", "Retail & Shopping", "Furniture & Home"),
    (r"pottery\s*barn|williams-?sonoma", "Retail & Shopping", "Furniture & Home"),
    (r"crate\s*&\s*barrel|west\s*elm|restoration\s*hardware", "Retail & Shopping", "Furniture & Home"),

    # ── PHARMACY & HEALTH ─────────────────────────────────────────────────────
    (r"cvs(?!\s*(?:energy|corporate|pharmacy\s*credit))", "Health & Medical", "Pharmacy"),
    (r"walgreens", "Health & Medical", "Pharmacy"),
    (r"rite\s*aid", "Health & Medical", "Pharmacy"),
    (r"boots\s*(?:uk|pharmacy)?", "Health & Medical", "Pharmacy"),
    (r"superdrug", "Health & Medical", "Pharmacy"),
    (r"dm\s*(?:drogerie)?", "Health & Medical", "Pharmacy"),
    (r"rossmann", "Health & Medical", "Pharmacy"),
    (r"mueller|müller\s*drogerie", "Health & Medical", "Pharmacy"),
    (r"kruidvat", "Health & Medical", "Pharmacy"),
    (r"apotek(?:\s*hjärtat)?|apoteket|lloydsapotek", "Health & Medical", "Pharmacy"),
    (r"chemist\s*warehouse", "Health & Medical", "Pharmacy"),
    (r"priceline\s*pharmacy|terry\s*white", "Health & Medical", "Pharmacy"),
    (r"guardian\s*pharmacy", "Health & Medical", "Pharmacy"),
    (r"watsons(?!\s*hotel)", "Health & Medical", "Pharmacy"),
    (r"mannings\b", "Health & Medical", "Pharmacy"),
    (r"mercury\s*drug", "Health & Medical", "Pharmacy"),
    # Gym & Fitness
    (r"planet\s*fitness", "Health & Medical", "Gym & Wellness"),
    (r"equinox(?!\s*(?:payments|capital))", "Health & Medical", "Gym & Wellness"),
    (r"24\s*hour\s*fitness", "Health & Medical", "Gym & Wellness"),
    (r"anytime\s*fitness", "Health & Medical", "Gym & Wellness"),
    (r"la\s*fitness", "Health & Medical", "Gym & Wellness"),
    (r"ymca|ywca", "Health & Medical", "Gym & Wellness"),
    (r"orangetheory\s*fitness", "Health & Medical", "Gym & Wellness"),
    (r"f45\s*training|barry'?s\s*bootcamp|soulcycle|soul\s*cycle", "Health & Medical", "Gym & Wellness"),
    (r"peloton", "Health & Medical", "Gym & Wellness"),
    (r"classpass|mindbody", "Health & Medical", "Gym & Wellness"),
    (r"fitness\s*first|virgin\s*active|pure\s*gym|snap\s*fitness", "Health & Medical", "Gym & Wellness"),
    (r"goodlife\s*(?:fitness|health\s*clubs)", "Health & Medical", "Gym & Wellness"),
    # Healthcare
    (r"teladoc|mdlive|doctor\s*on\s*demand|sesame\s*care|zocdoc|one\s*medical", "Health & Medical", "Doctor & Clinic"),
    (r"labcorp|quest\s*diagnostics", "Health & Medical", "Doctor & Clinic"),
    (r"cigna|aetna|humana|anthem\b|bluecross|blue\s*cross|bcbs\b|kaiser\s*permanente", "Health & Medical", "Insurance"),
    (r"unitedhealthcare|uhc\b|oscar\s*health|united\s*health", "Health & Medical", "Insurance"),

    # ── FINANCIAL SERVICES ────────────────────────────────────────────────────
    (r"paypal", "Other", "Payment Services"),
    (r"stripe(?!\s*security)", "Other", "Payment Services"),
    (r"square(?!\s*(?:enix|mile|meal|trade))", "Other", "Payment Services"),
    (r"venmo", "Other", "Payment Services"),
    (r"zelle\b", "Other", "Payment Services"),
    (r"cash\s*app", "Other", "Payment Services"),
    (r"wise\b(?!\s*(?:owl|crack|man|acre|word|town|use))|transferwise", "Other", "Payment Services"),
    (r"revolut\b", "Other", "Payment Services"),
    (r"n26\b", "Other", "Payment Services"),
    (r"monzo\b", "Other", "Payment Services"),
    (r"starling\s*bank", "Other", "Payment Services"),
    (r"chime(?!\s*communications)", "Other", "Payment Services"),
    (r"remitly|worldremit|western\s*union|moneygram", "Other", "Payment Services"),
    (r"paynow|paylah|grabpay", "Other", "Payment Services"),
    (r"wechat\s*pay|alipay|unionpay", "Other", "Payment Services"),
    (r"paytm|phonepe|bhim\b|gpay\b", "Other", "Payment Services"),
    (r"ovo\b|gopay|dana\b|linkaja|qris", "Other", "Payment Services"),
    (r"gcash|maya(?!\s*(?:bay|riviera|angelou))|paymaya", "Other", "Payment Services"),
    (r"m-?pesa|m-?shwari|tigo\s*pesa", "Other", "Payment Services"),
    (r"flutterwave|paystack", "Other", "Payment Services"),
    (r"coinbase|binance|kraken\s*exchange|gemini\s*exchange|crypto\.com", "Financial Services", "Cryptocurrency"),
    (r"robinhood|webull|etrade|e\*trade|td\s*ameritrade|charles\s*schwab|fidelity|vanguard\b", "Financial Services", "Investment"),
    (r"betterment|wealthfront|acorns\b|stash\b|sofi\s*invest", "Financial Services", "Investment"),

    # ── EDUCATION ─────────────────────────────────────────────────────────────
    (r"coursera", "Education", "Online Courses"),
    (r"udemy", "Education", "Online Courses"),
    (r"udacity", "Education", "Online Courses"),
    (r"linkedin\s*learning|lynda\.com", "Education", "Online Courses"),
    (r"skillshare", "Education", "Online Courses"),
    (r"pluralsight", "Education", "Online Courses"),
    (r"masterclass", "Education", "Online Courses"),
    (r"brilliant\.org", "Education", "Online Courses"),
    (r"duolingo", "Education", "Language Learning"),
    (r"babbel|rosetta\s*stone", "Education", "Language Learning"),
    (r"o'reilly\s*(?:media|learning)?", "Education", "Books"),

    # ── PROFESSIONAL SERVICES ─────────────────────────────────────────────────
    (r"legalzoom|rocket\s*lawyer|docusign|hellosign|pandadoc", "Professional Services", "Legal"),
    (r"upwork|fiverr|toptal|freelancer\.com|99designs", "Professional Services", "Freelance"),

    # ── OFFICE & SHIPPING ─────────────────────────────────────────────────────
    (r"staples(?!\s*(?:center|arena))", "Office & Supplies", "Office Supplies"),
    (r"office\s*depot|officemax|office\s*max", "Office & Supplies", "Office Supplies"),
    (r"ryman(?!\s*auditorium)|viking\s*direct", "Office & Supplies", "Office Supplies"),
    (r"uline\b|quill\.com", "Office & Supplies", "Office Supplies"),
    (r"fedex(?!\s*field)", "Office & Supplies", "Postage & Shipping"),
    (r"ups\s*(?:store)?(?!\s*arena)", "Office & Supplies", "Postage & Shipping"),
    (r"usps\b|royal\s*mail|australia\s*post|canada\s*post|new\s*zealand\s*post", "Office & Supplies", "Postage & Shipping"),
    (r"dhl(?!\s*fashion)", "Office & Supplies", "Postage & Shipping"),
    (r"ninja\s*van|lalamove|j&t\s*express|pos\s*malaysia|singpost|thailand\s*post", "Office & Supplies", "Postage & Shipping"),
]


def auto_categorise(merchant: str) -> tuple[str, str]:
    """
    Auto-categorise a merchant/description by pattern matching.
    Returns (category, subcategory). Falls back to ('Other', 'Uncategorized').
    """
    if not merchant:
        return "Other", "Miscellaneous"

    # Normalise: lowercase, collapse whitespace, strip non-ASCII diacritics
    merchant_lower = merchant.lower().strip()
    try:
        merchant_ascii = unicodedata.normalize('NFKD', merchant_lower)
        merchant_ascii = merchant_ascii.encode('ascii', 'ignore').decode('ascii')
    except Exception:
        merchant_ascii = merchant_lower

    for pattern, category, subcategory in MERCHANT_PATTERNS:
        if re.search(pattern, merchant_lower) or re.search(pattern, merchant_ascii):
            return category, subcategory

    return "Other", "Miscellaneous"
