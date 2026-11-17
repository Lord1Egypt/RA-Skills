#!/usr/bin/env python3
"""Weekly Danish grocery tilbudsavis scraper.

Uses the Tjek API (the backend behind etilbudsavis.dk) which powers the
digital aviser for Lidl, Rema 1000, Netto, Meny and 365 discount.

For each store:
  1. fetch catalog (avis) list, pick the weekly avis valid now (or next up)
  2. fetch all offers
  3. write data/full-<date>.json (raw dump) and data/full-<date>.txt
     (readable, ordered by supermarket then category)
  4. build the "wow" list: interest matches (prioritized) plus any other
     genuinely good deal, capped at 18 items
  5. print a spaced-out summary between markers for the notification
"""
import datetime
import json
import pathlib
import re
import sys
import urllib.request
from zoneinfo import ZoneInfo

BASE = pathlib.Path(__file__).resolve().parent
CONFIG = json.loads((BASE / "config.json").read_text(encoding="utf-8"))
KEY = CONFIG["api_key"]
API = CONFIG["api_base"]
DATA_DIR = BASE / "data"
DATA_DIR.mkdir(exist_ok=True)
TZ = ZoneInfo("Europe/Copenhagen")
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

MAX_WOW_ITEMS = 18
MAX_PER_INTEREST = 4

CATEGORY_RULES = [
    ("Kod & fjerkrae", ["okse", "kylling", "grisekod", "flaesk", "morbrad", "bof", "steak",
                       "kotelet", "bacon", "skinke", "polse", "kebab", "lam", "kalv",
                       "kalkun", "fjerkae", "palag", "cordon bleu", "schnitzel"], 45),
    ("Fisk & skaldyr", ["laks", "torsk", "sild", "rejer", "fisk", "tun", "musling",
                        "skaldyr", "makrel", "rodspaette", "orred", "havkat"], 50),
    ("Mejeri & aeg", ["maelk", "ost", "smoer", "yoghurt", "aeg", "flode", "creme fraiche",
                     "kaernemaelk", "mozzarella", "brie", "youghurt", "kvark", "fromage"], 25),
    ("Frugt & gront", ["banan", "aeble", "appelsin", "tomat", "agurk", "salat", "kartoffel",
                       "log", "gulerod", "broccoli", "blomkal", "avocado", "citron",
                       "jordbaer", "blabaer", "frugt", "gront", "peberfrugt", "svamp",
                       "spinat", "mango", "melon", "vindrue", "paere"], 12),
    ("Brod & korn", ["brod", "rundstykke", "rugbrod", "toast", "boller", "kiks", "havregryn",
                     "morgenmad", "pasta", "ris", "mel", "tortilla", "pizza", "flutes",
                     "ciabatta", "baguette"], 15),
    ("Drikkevarer", ["cola", "sodavand", "ol", "vin", "juice", "vand", "kaffe", "kakao",
                     "energidrik", "monster", "red bull", "is", "saftevand", "cider"], 8),
    ("Snacks & slik", ["chips", "slik", "chokolade", "nodder", "mandler", "kage", "is",
                       "snacks", "popcorn", "vaffel", "kugler", "vingummi"], 60),
    ("Frost", ["frost", "frossen", "dybfrost", "friture", "pizza"], 30),
    ("Husholdning", ["saebe", "vaskemiddel", "toiletpapir", "kokkenrulle", "opvask",
                     "shampoo", "tandpasta", "batteri", "skyllemiddel", "saebe"], None),
]
CATEGORY_FALLBACK = "Andet"
UNIT_LITER_RULES = ["Drikkevarer"]


def api_get(path: str):
    req = urllib.request.Request(
        API + path,
        headers={
            "User-Agent": UA,
            "Authorization": "Bearer " + KEY,
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def parse_dt(s: str) -> datetime.datetime:
    s = s.replace("+0000", "+00:00").replace("Z", "+00:00")
    return datetime.datetime.fromisoformat(s)


def pick_catalog(catalogs: list, now: datetime.datetime):
    week = []
    for c in catalogs:
        try:
            rf = parse_dt(c["run_from"])
            rt = parse_dt(c["run_till"])
        except Exception:
            continue
        days = (rt - rf).days
        if 4 <= days <= 10:
            week.append((c, rf, rt))
    if not week:
        return None, None, None
    valid = [w for w in week if w[1] <= now <= w[2]]
    if valid:
        return max(valid, key=lambda w: w[0].get("offer_count", 0) or 0)
    upcoming = [w for w in week if w[1] > now]
    if upcoming:
        return min(upcoming, key=lambda w: w[1])
    return max(week, key=lambda w: w[1])


def parse_dk_num(s: str):
    s = s.strip().replace("kr", "").replace("kr.", "").strip()
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
        return float(s)
    return float(s)


def fmt_price(p) -> str:
    if p is None:
        return ""
    if isinstance(p, float) and p != int(p):
        return f"{p:,.2f} kr".replace(",", " ").replace(".", ",")
    return f"{int(p)} kr"


def fmt_dk(v: float, suffix: str = "") -> str:
    s = f"{v:,.2f}".replace(",", " ").replace(".", ",")
    return f"{s} {suffix}".strip()


def normalize(s: str) -> str:
    return s.lower().replace("æ", "ae").replace("ø", "oe").replace("å", "aa")


KG_RE = re.compile(r"([0-9][0-9.,]*)\s*(?:kr\.?)?\s*(?:pr\.?\s*kg|kg[- ]pris)", re.I)
L_RE = re.compile(r"([0-9][0-9.,]*)\s*(?:kr\.?)?\s*(?:pr\.?\s*l(?:iter)?|literpris)", re.I)
STK_RE = re.compile(r"([0-9][0-9.,]*)\s*(?:kr\.?)?\s*(?:pr\.?\s*stk|stk\.?[- ]pris)", re.I)


def offer_metrics(o: dict) -> dict:
    desc = o.get("description") or ""
    pricing = o.get("pricing") or {}
    price = pricing.get("price")
    pre = pricing.get("pre_price")
    q = o.get("quantity") or {}
    unit = ((q.get("unit") or {}).get("symbol") or "").lower()
    size_from = (q.get("size") or {}).get("from")
    size_to = (q.get("size") or {}).get("to")
    pieces = (q.get("pieces") or {}).get("from")

    per_kg = per_l = per_piece = None
    size_text = ""
    weight_g = None

    if unit in ("g", "kg") and size_from:
        if unit == "g":
            weight_g = size_from
            size_text = f"{size_from}-{size_to} g" if size_to and size_to != size_from else f"{size_from} g"
        else:
            weight_g = size_from * 1000
            size_text = f"{size_from} kg"
    elif unit in ("ml", "l", "cl") and size_from:
        if unit == "ml":
            size_text = f"{size_from} ml"
        elif unit == "cl":
            size_text = f"{size_from} cl"
        else:
            size_text = f"{size_from} l"
    elif unit == "pcs" and pieces:
        size_text = f"{pieces} stk"

    if price is not None:
        if weight_g:
            per_kg = price / (weight_g / 1000.0)
        if unit in ("ml", "l", "cl") and size_from:
            ml = size_from * (1 if unit == "ml" else 10 if unit == "cl" else 1000)
            per_l = price / (ml / 1000.0)
        if unit == "pcs" and pieces:
            per_piece = price / pieces

    m = KG_RE.search(desc)
    if m:
        try:
            per_kg = parse_dk_num(m.group(1))
        except ValueError:
            pass
    m = L_RE.search(desc)
    if m:
        try:
            per_l = parse_dk_num(m.group(1))
        except ValueError:
            pass
    m = STK_RE.search(desc)
    if m:
        try:
            per_piece = parse_dk_num(m.group(1))
        except ValueError:
            pass

    discount_pct = None
    if price is not None and pre:
        discount_pct = round((pre - price) / pre * 100)

    return {
        "size_text": size_text,
        "per_kg": per_kg,
        "per_l": per_l,
        "per_piece": per_piece,
        "discount_pct": discount_pct,
    }


def classify(text: str) -> str:
    n = normalize(text)
    for name, kws, _bar in CATEGORY_RULES:
        if any(kw in n for kw in kws):
            return name
    return CATEGORY_FALLBACK


def interest_wow(metrics: dict, interest: dict) -> bool:
    cfg = interest.get("wow", {})
    min_disc = cfg.get("min_discount_pct")
    if min_disc and metrics["discount_pct"] is not None and metrics["discount_pct"] >= min_disc:
        return True
    if cfg.get("max_price_per_kg") and metrics["per_kg"] is not None and metrics["per_kg"] <= cfg["max_price_per_kg"]:
        return True
    if cfg.get("max_price_per_l") and metrics["per_l"] is not None and metrics["per_l"] <= cfg["max_price_per_l"]:
        return True
    if cfg.get("max_price_per_piece") and metrics["per_piece"] is not None and metrics["per_piece"] <= cfg["max_price_per_piece"]:
        return True
    return False


def general_strength(metrics: dict, category: str):
    if metrics["discount_pct"] is not None and metrics["discount_pct"] >= 40:
        return metrics["discount_pct"] * 2
    bar = None
    for name, _kws, b in CATEGORY_RULES:
        if name == category:
            bar = b
            break
    if bar is None:
        return None
    if category in UNIT_LITER_RULES:
        v = metrics["per_l"]
        unit = "per_l"
    else:
        v = metrics["per_kg"]
        unit = "per_kg"
    if v is None or v <= 0:
        return None
    if unit == "per_l" and metrics["per_l"] is not None and metrics["per_l"] <= bar:
        return 100 - (metrics["per_l"] / bar * 80)
    if unit == "per_kg" and metrics["per_kg"] is not None and metrics["per_kg"] <= bar:
        return 100 - (metrics["per_kg"] / bar * 80)
    return None


def fmt_per_unit(metrics: dict) -> str:
    if metrics["per_kg"] is not None:
        return fmt_dk(metrics["per_kg"], "kr/kg")
    if metrics["per_l"] is not None:
        return fmt_dk(metrics["per_l"], "kr/l")
    if metrics["per_piece"] is not None:
        return fmt_dk(metrics["per_piece"], "kr/stk")
    return ""


def fmt_item(rec: dict, metrics: dict) -> str:
    parts = [fmt_price(rec["price"])]
    if metrics["size_text"]:
        parts.append(metrics["size_text"])
    u = fmt_per_unit(metrics)
    if u:
        parts.append(u)
    if rec.get("pre_price"):
        parts.append(f"for {fmt_price(rec['pre_price'])}")
    if metrics["discount_pct"]:
        parts.append(f"spar {metrics['discount_pct']}%")
    return " / ".join(parts)


def main() -> int:
    now = datetime.datetime.now(datetime.timezone.utc)
    now_local = now.astimezone(TZ)
    today = now_local.date()

    results = []
    interest_hits = {}
    general_candidates = []
    period_start, period_end = None, None
    errors = []

    for store in CONFIG["stores"]:
        try:
            catalogs = api_get(f"/v2/catalogs?dealer_id={store['id']}")
            cat, rf, rt = pick_catalog(catalogs, now)
            if cat is None:
                errors.append(f"{store['name']}: ingen ugentlig avis fundet")
                continue
            offers = []
            offset = 0
            while True:
                page = api_get(f"/v2/offers?catalog_id={cat['id']}&limit=100&offset={offset}")
                if not page:
                    break
                offers.extend(o for o in page if o.get("catalog_id") == cat["id"])
                if len(page) < 100:
                    break
                offset += 100
            cat_info = {
                "id": cat["id"],
                "label": cat.get("label"),
                "run_from": cat.get("run_from"),
                "run_till": cat.get("run_till"),
                "page_count": cat.get("page_count"),
                "offer_count": cat.get("offer_count"),
            }
            if period_start is None or rf < period_start:
                period_start = rf
            if period_end is None or rt > period_end:
                period_end = rt
            results.append({
                "store": store["name"],
                "avis_url": store["avis_url"],
                "catalog": cat_info,
                "offers": offers,
            })
            for o in offers:
                rec = {
                    "store": store["name"],
                    "heading": o.get("heading"),
                    "description": o.get("description"),
                    "price": o.get("pricing", {}).get("price"),
                    "pre_price": o.get("pricing", {}).get("pre_price"),
                    "page": o.get("catalog_page"),
                }
                metrics = offer_metrics(o)
                text = (o.get("heading") or "") + " " + (o.get("description") or "")
                hay = normalize(text)
                category = classify(text)

                matched_interest = None
                for interest in CONFIG["interests"]:
                    if not any(kw in hay for kw in interest["keywords"]):
                        continue
                    if any(ex in hay for ex in interest.get("exclude", [])):
                        continue
                    matched_interest = interest
                    break
                if matched_interest is not None and interest_wow(metrics, matched_interest):
                    interest_hits.setdefault(matched_interest["category"], []).append(
                        (store["name"], rec, metrics, category))
                else:
                    strength = general_strength(metrics, category)
                    if strength is not None:
                        general_candidates.append(
                            (strength, store["name"], rec, metrics, category))
        except Exception as e:
            errors.append(f"{store['name']}: {e}")

    date_str = today.isoformat()
    (DATA_DIR / f"full-{date_str}.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")

    flines = []
    if period_start and period_end:
        ps = period_start.astimezone(TZ).strftime("%a %d. %b")
        pe = period_end.astimezone(TZ).strftime("%a %d. %b")
        flines.append(f"TILBUD i butikkerne ({ps} til {pe})")
    else:
        flines.append("TILBUD i butikkerne")
    flines.append("")
    for r in results:
        flines.append(f"=== {r['store'].upper()} ({len(r['offers'])} tilbud) ===")
        by_cat = {}
        for o in r["offers"]:
            text = (o.get("heading") or "") + " " + (o.get("description") or "")
            cat = classify(text)
            by_cat.setdefault(cat, []).append(o)
        for cat in sorted(by_cat):
            flines.append(f"")
            flines.append(f"  {cat}")
            for o in sorted(by_cat[cat], key=lambda x: (x.get("pricing") or {}).get("price") or 0):
                rec = {"store": r["store"], "heading": o.get("heading"),
                       "description": o.get("description"),
                       "price": (o.get("pricing") or {}).get("price"),
                       "pre_price": (o.get("pricing") or {}).get("pre_price"),
                       "page": o.get("catalog_page")}
                flines.append(f"    - {rec['heading']}: {fmt_item(rec, offer_metrics(o))}")
        flines.append("")
    (DATA_DIR / f"full-{date_str}.txt").write_text("\n".join(flines), encoding="utf-8")

    selected = []
    used = set()

    def add(store, rec, metrics, category, interest_cat):
        key = (store, rec["heading"])
        if key in used:
            return
        used.add(key)
        selected.append((store, rec, metrics, category, interest_cat))

    for interest in CONFIG["interests"]:
        cat = interest["category"]
        hits = interest_hits.get(cat, [])
        hits_sorted = sorted(hits, key=lambda h: (
            -(h[2]["discount_pct"] or 0),
            h[2]["per_kg"] if h[2]["per_kg"] is not None else 1e9,
        ))
        for store_name, rec, metrics, category in hits_sorted[:MAX_PER_INTEREST]:
            add(store_name, rec, metrics, category, cat)
        if len(selected) >= MAX_WOW_ITEMS:
            break

    general_candidates.sort(key=lambda x: -x[0])
    for strength, store_name, rec, metrics, category in general_candidates:
        if len(selected) >= MAX_WOW_ITEMS:
            break
        add(store_name, rec, metrics, category, None)

    lines = []
    if period_start and period_end:
        ps = period_start.astimezone(TZ).strftime("%a %d. %b")
        pe = period_end.astimezone(TZ).strftime("%a %d. %b")
        lines.append(f"Ugens bedste tilbud ({ps} til {pe})")
    else:
        lines.append("Ugens bedste tilbud")
    lines.append("")

    shown_cats = set()
    for interest in CONFIG["interests"]:
        cat = interest["category"]
        if cat in shown_cats:
            continue
        shown_cats.add(cat)
        cat_items = [x for x in selected if x[4] == cat]
        lines.append(f"{interest['emoji']} {cat}")
        if not cat_items:
            lines.append("")
            lines.append("   Ingen wow-tilbud denne uge")
            lines.append("")
            continue
        for store_name, rec, metrics, category, _ic in cat_items:
            lines.append("")
            lines.append(f"   • {store_name}: {rec['heading']}")
            lines.append(f"      {fmt_item(rec, metrics)}")
        lines.append("")

    general_items = [x for x in selected if x[4] is None]
    if general_items:
        lines.append("🔥 Andre gode tilbud")
        for store_name, rec, metrics, category, _ic in general_items:
            lines.append("")
            lines.append(f"   • {store_name}: {rec['heading']}")
            lines.append(f"      {fmt_item(rec, metrics)}")
        lines.append("")

    if errors:
        lines.append("Fejl")
        for e in errors:
            lines.append(f"   {e}")
        lines.append("")

    summary = "\n".join(lines)
    (DATA_DIR / f"summary-{date_str}.txt").write_text(summary, encoding="utf-8")

    print("---BEGIN SUMMARY---")
    print(summary)
    print("---END SUMMARY---")

    cutoff = now - datetime.timedelta(days=90)
    for f in DATA_DIR.glob("full-*.json"):
        try:
            fd = datetime.date.fromisoformat(f.stem.split("-", 1)[1])
            if datetime.datetime(fd.year, fd.month, fd.day, tzinfo=datetime.timezone.utc) < cutoff:
                f.unlink()
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
