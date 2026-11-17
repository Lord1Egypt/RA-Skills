#!/usr/bin/env python3
# bokatvattid.py — generisk CLI mot Boka tvättid (bokatvattid.se, Visir).
# Stdlib-only, inget byggnadsspecifikt inbakat (inga rumsalias/id:n).
# All legacy-trafik skickas som POST (credentials i request-body, aldrig i URL:en).
# Byggnad/lägenhet/PIN via flaggor, env eller ~/.config/bokatvattid/:
#   config.json: {"building": "<föreningsnamn eller v1-id>", "apartment": "<lägenhetsnr>"}
#   pin.txt: PIN på första raden
# Env-alternativ: BOKATVATTID_BUILDING, BOKATVATTID_APARTMENT, BOKATVATTID_PIN
#
# Exempel:
#   python3 bokatvattid.py buildings <föreningsnamn>
#   python3 bokatvattid.py rooms --building <föreningsnamn> --apartment <lägenhetsnr>
#   python3 bokatvattid.py slots imorgon
#   python3 bokatvattid.py free 12/10 --room "Tvätt 1"
#   python3 bokatvattid.py book 2026-10-12 19:00 --room <rums-id> --yes
#   python3 bokatvattid.py cancel 2026-10-12 --yes
#   python3 bokatvattid.py my
import argparse, datetime, json, os, re, sys, urllib.parse, urllib.request

LEGACY = "https://prod.bokatvattid.se/api/api2"
V2 = "https://api.visirsolutions.com/api/v2"
CFG_DIR = os.path.expanduser("~/.config/bokatvattid")

class BokaError(Exception):
    pass

def _get(url, params):
    url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        d = json.loads(r.read().decode("utf-8"))
    if os.environ.get("BOKA_DEBUG"):
        print(json.dumps(d, ensure_ascii=False)[:2000], file=sys.stderr)
    return d

def _post(url, params):
    # Form-encoded POST: credentials stay in the request body, never in a URL
    # (query strings end up in server/proxy access logs; bodies normally do not).
    body = urllib.parse.urlencode(params).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST",
                                 headers={"Accept": "application/json",
                                          "Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=20) as r:
        d = json.loads(r.read().decode("utf-8"))
    if os.environ.get("BOKA_DEBUG"):
        print(json.dumps(d, ensure_ascii=False)[:2000], file=sys.stderr)
    return d

def api(token, uid, method, **kw):
    p = {"method": method, "token": token, "userid": uid, "lang": "1"}
    p.update({k: ("" if v is None else str(v)) for k, v in kw.items()})
    d = _post(LEGACY, p)
    if d.get("error") not in (0, "0"):
        raise BokaError("%s misslyckades: error=%s %s" % (method, d.get("error"), d.get("message", "")))
    return d

def _cfg():
    try:
        return json.load(open(os.path.join(CFG_DIR, "config.json")))
    except Exception:
        return {}

def _find_lists(o, key):
    out = []
    def walk(x):
        if isinstance(x, list):
            if x and all(isinstance(i, dict) for i in x) and key in x[0]: out.extend(i for i in x if key in i); return
            for i in x: walk(i)
        elif isinstance(x, dict):
            for v in x.values(): walk(v)
    walk(o)
    return out

def read_pin(a):
    if a.pin: return a.pin
    if os.environ.get("BOKATVATTID_PIN"): return os.environ["BOKATVATTID_PIN"].strip()
    kf = os.path.join(CFG_DIR, "pin.txt")
    if os.path.exists(kf):
        pin = open(kf).readline().strip()
        if pin: return pin
    sys.exit("PIN saknas. Ange --pin, sätt BOKATVATTID_PIN eller skriv den i %s" % kf)

def building_arg(a):
    q = a.building or os.environ.get("BOKATVATTID_BUILDING") or _cfg().get("building")
    if not q: sys.exit("Byggnad saknas. Ange --building (söknamn eller v1-id), env BOKATVATTID_BUILDING eller config.json")
    return q

def apartment_arg(a):
    q = a.apartment or os.environ.get("BOKATVATTID_APARTMENT") or _cfg().get("apartment")
    if not q: sys.exit("Lägenhet saknas. Ange --apartment, env BOKATVATTID_APARTMENT eller config.json")
    return q

def search_buildings(q):
    d = _get(V2 + "/public/buildings/search", {"q": q})
    hits = _find_lists(d, "id")
    seen, out = set(), []
    for h in hits:
        name = h.get("name") or h.get("building_name") or h.get("BuildingName") or "?"
        bid = str(h.get("id"))
        if (bid, name) not in seen:
            seen.add((bid, name)); out.append({"id": bid, "name": name, "city": h.get("city", "")})
    return out

def lookup_building(bid):
    d = _get(V2 + "/public/buildings/lookup", {"building_id": bid})
    body = d.get("data") or d.get("body") or {}
    if not isinstance(body, dict): body = {}
    return {"backend_mode": body.get("backend_mode"), "v1_building_id": str(body.get("v1_building_id") or "")}

def resolve_building(q):
    q = q.strip()
    if re.fullmatch(r"\d+", q): return q
    hits = search_buildings(q)
    if not hits: sys.exit("Ingen byggnad matchade '%s'." % q)
    if len(hits) > 1:
        for h in hits: print("%-6s %s %s" % (h["id"], h["name"], h["city"]))
        sys.exit("Flera träffar — kör igen med --building <id eller säkrare sökord>.")
    info = lookup_building(hits[0]["id"])
    if info["backend_mode"] != "v1" or not info["v1_building_id"]:
        sys.exit("Byggnaden '%s' kör inte v1-läge (mode=%s) — stöds inte ännu." % (hits[0]["name"], info["backend_mode"]))
    print("Byggnad: %s (v1-id %s)" % (hits[0]["name"], info["v1_building_id"]), file=sys.stderr)
    return info["v1_building_id"]

def login(pin, building, apartment):
    d = _post(LEGACY, {"method": "checkLogin2", "buildingid": building, "pincode": pin,
                       "apartmentnumber": apartment, "lang": "1"})
    if d.get("error") not in (0, "0"):
        raise BokaError("Inloggning misslyckades: %s (fel PIN/lägenhet?)" % d.get("message", ""))
    b = d["body"]
    return b["Token"], str(b["ApartmentID"])

def _norm(s):
    s = (s or "").lower().replace("å", "a").replace("ä", "a").replace("ö", "o")
    return re.sub(r"[^a-z0-9]", "", s)

def rooms(token, uid, building):
    d = api(token, uid, "getLaundryRoomList", buildingid=building, v="3")
    out = _find_lists(d.get("body"), "LaundryRoomID")
    return [r for r in out if r.get("LaundryRoomID") and r.get("IsActive", 1)]

def pick_room(rs, q):
    if not q:
        for r in rs:
            if r.get("IsDefault"): return r
        return rs[0]
    qn = _norm(q)
    for r in rs:  # exakt id eller exakt namn
        if q == str(r["LaundryRoomID"]) or qn == _norm(r.get("LaundryRoomName")): return r
    toks = [_norm(t) for t in q.split() if t.strip()]
    cand = [r for r in rs if all(t in _norm(r.get("LaundryRoomName")) for t in toks)]
    if len(cand) == 1: return cand[0]
    if len(cand) > 1:
        sys.exit("Tvetydigt rum '%s' — menar du: %s?" % (q, " / ".join("%s (%s)" % (r["LaundryRoomName"], r["LaundryRoomID"]) for r in cand)))
    sys.exit("Hittade inte rum '%s'. Kör 'rooms' för listan." % q)

def parse_date(s):
    t = datetime.date.today()
    s = (s or "").strip().lower()
    if s in ("", "idag", "today"): return t
    if s in ("imorgon", "tomorrow"): return t + datetime.timedelta(days=1)
    m = re.fullmatch(r"\+(\d+)", s)
    if m: return t + datetime.timedelta(days=int(m.group(1)))
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d/%m-%Y", "%d-%m-%Y", "%d/%m", "%d-%m", "%d.%m"):
        try:
            d = datetime.datetime.strptime(s, fmt).date()
            if fmt in ("%d/%m", "%d-%m", "%d.%m") and d < t:
                d = d.replace(year=d.year + 1)
            return d
        except ValueError:
            pass
    sys.exit("Ogiltigt datum '%s' (ex: 2026-10-12, 12/10, imorgon, +3)" % s)

def slots(token, uid, room_id, d):
    b = api(token, uid, "getLaundryRoomSlots", laundryid=room_id,
            day=d.day, month=d.month, year=d.year)["body"]
    cal = b.get("calendar")
    if not isinstance(cal, list):
        cal = _find_lists(b, "isBook")
    return cal

def fmt_slot(s):
    tag = "DIN " if s.get("isOwner") else ("ledig" if not s.get("isBook") and not s.get("isDisable") else "bokad")
    return "  %-14s %s" % (s["name"].replace(" - ", "–"), tag)

def confirm(msg, assume_yes):
    if assume_yes: return True
    if not sys.stdin.isatty():
        sys.exit("Icke-interaktivt läge: kräver --yes för %s" % msg)
    return input("%s [j/N]: " % msg).strip().lower() in ("j", "y", "ja", "yes")

def main():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--pin", help="PIN (annars env BOKATVATTID_PIN eller ~/.config/bokatvattid/pin.txt)")
    common.add_argument("--building", help="söknamn eller v1-id (annars env/config)")
    common.add_argument("--apartment", help="lägenhetsnummer (annars env/config)")
    common.add_argument("--room", help="rums-id eller (del av) rumsnamn — default är byggnadens standardrum")
    common.add_argument("--yes", "-y", action="store_true", help="hoppa över bekräftelse")
    ap = argparse.ArgumentParser(description="Boka tvättid (generisk)", parents=[common])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("buildings", help="sök byggnad"); p.add_argument("query")
    for name, help_ in (("login", "testa inloggning"), ("rooms", "lista rum"), ("my", "mina bokningar")):
        sub.add_parser(name, parents=[common], help=help_)
    for name, help_ in (("slots", "visa tider"), ("free", "visa bara lediga"), ("cancel", "avboka dina tider ett datum")):
        p = sub.add_parser(name, parents=[common], help=help_); p.add_argument("date", nargs="?")
    p = sub.add_parser("book", parents=[common], help="boka"); p.add_argument("date"); p.add_argument("time", help="t.ex. 19:00 eller 19:00,21:00")
    a = ap.parse_args()

    if a.cmd == "buildings":
        hits = search_buildings(a.query)
        if not hits: print("Ingen träff."); return
        for h in hits:
            info = lookup_building(h["id"])
            v1 = info["v1_building_id"] or ("—" if info["backend_mode"] != "v1" else "?")
            print("%-6s %-30s %-12s v1-id: %s" % (h["id"], h["name"], h["city"], v1))
        return

    building = resolve_building(building_arg(a))
    token, uid = login(read_pin(a), building, apartment_arg(a))
    rs = rooms(token, uid, building)

    if a.cmd == "login":
        print("Inloggning OK (userid=%s, %d aktiva rum)" % (uid, len(rs)))
    elif a.cmd == "rooms":
        for r in sorted(rs, key=lambda r: r["LaundryRoomID"]):
            mark = " (standard)" if r.get("IsDefault") else ""
            print("%-5s %s%s" % (r["LaundryRoomID"], r.get("LaundryRoomName", "?"), mark))
    elif a.cmd in ("slots", "free"):
        r = pick_room(rs, a.room); d = parse_date(a.date)
        print("%s — %s" % (r["LaundryRoomName"], d.strftime("%a %d/%m")))
        for s in sorted(slots(token, uid, r["LaundryRoomID"], d), key=lambda x: x["name"]):
            if a.cmd == "free" and (s.get("isBook") or s.get("isDisable") or s.get("isOwner")): continue
            print(fmt_slot(s))
    elif a.cmd == "book":
        r = pick_room(rs, a.room); d = parse_date(a.date)
        cal = slots(token, uid, r["LaundryRoomID"], d)
        ids = []
        for w in (w.strip() for w in a.time.split(",") if w.strip()):
            hh = w.split("-")[0].split(":")[0]
            m = [s for s in cal if s["name"].startswith(hh + ":")]
            if not m: sys.exit("Ingen tid börjar %s:00 den dagen." % hh)
            s = m[0]
            if s.get("isBook") or s.get("isDisable"): sys.exit("%s är inte bokbar." % s["name"])
            ids.append((s["id"], s["name"]))
        label = ", ".join(n for _, n in ids)
        if not confirm("Boka %s %s i %s?" % (d.strftime("%a %d/%m"), label, r["LaundryRoomName"]), a.yes):
            print("Avbröts."); return
        res = api(token, uid, "Booking3", laundryid=r["LaundryRoomID"],
                  timeslot=",".join(str(i) for i, _ in ids), day=d.day, month=d.month, year=d.year,
                  rebook=0, devicemodel="BokaTvattidV2 Web", firmware="web", appid=0,
                  curday="", devicetoken="")
        print("Bokat! BookingID %s — %s %s, %s" % (res.get("body"), d.strftime("%a %d/%m"), label, r["LaundryRoomName"]))
    elif a.cmd == "cancel":
        d = parse_date(a.date)
        targets = [(r, [s for s in slots(token, uid, r["LaundryRoomID"], d) if s.get("isOwner")]) for r in rs]
        targets = [(r, own) for r, own in targets if own]
        if not targets: print("Inga egna bokningar %s." % d.strftime("%a %d/%m")); return
        for r, own in targets:
            print("%s: %s" % (r["LaundryRoomName"], ", ".join(s["name"] for s in own)))
        if not confirm("Avboka dessa?", a.yes): print("Avbröts."); return
        for r, _ in targets:
            api(token, uid, "Booking3", laundryid=r["LaundryRoomID"], timeslot="",
                day=d.day, month=d.month, year=d.year, rebook=1,
                devicemodel="BokaTvattidV2 Web", firmware="web", appid=0, curday="", devicetoken="")
        print("Avbokat.")
    elif a.cmd == "my":
        d = api(token, uid, "getMyBooking", start=0, limit=50).get("body", {})
        data = d.get("data", d) if isinstance(d, dict) else d
        if not data: print("Inga bokningar."); return
        for b in data:
            print(json.dumps(b, ensure_ascii=False))

if __name__ == "__main__":
    try:
        main()
    except BokaError as e:
        sys.exit("FEL: %s" % e)
