#!/usr/bin/env python3
"""near_town.py - the free camps on record near a town. Read-only, Python 3.8+, standard library only.

  near_town.py "Sisters" --state OR [--limit 5] [--radius 25] [--json]

It reads the same two addresses the Field Guide's aa.py "town" command reads:
  https://davelalande.com/towns.json     (the town's point)
  https://davelalande.com/api/near       (camps near that point, nearest first)
and keeps only the camps whose cost verdict is "free". Distances are straight-line miles.
A null or missing field is UNRECORDED; nothing is estimated. If no free camp is on record
inside the radius, it widens once to 50 miles and gives the nearest free camp, with its miles.
Exit code 0 = answered, 2 = town not found (ask for the state), 1 = could not read.
Makes no account and sends no personal data.
"""
import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://davelalande.com"
UA = "aa-skill/1 (+https://davelalande.com/skill/) near-town/1.0.0"
CREDIT = "Camp records: American Adventurer (davelalande.com)"
OSM = "Where a record's source names OpenStreetMap, also credit: (c) OpenStreetMap contributors (ODbL)."
WIDE = 50
PACE = 0.5
_last = [0.0]


class NotFound(Exception):
    pass


class CouldNotRead(Exception):
    pass


def get(path, params=None):
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    err = None
    for attempt in range(2):
        wait = PACE - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return url, json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err = "HTTP %s from %s" % (e.code, url)
            if e.code in (429, 500, 502, 503, 504) and attempt == 0:
                time.sleep(3)
                continue
            break
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            err = "could not read %s (%s)" % (url, e)
            if attempt == 0:
                time.sleep(3)
                continue
            break
    raise CouldNotRead("%s. Could not read; that is not the same as none." % err)


def record_date(data):
    pub = data.get("publisher") if isinstance(data, dict) else None
    if isinstance(pub, dict):
        cite = pub.get("cite", "")
        if "data built " in cite:
            return cite.split("data built ", 1)[1].split()[0]
    for k in ("updated", "generated", "data_built_at"):
        if isinstance(data, dict) and data.get(k):
            return data[k]
    return None


def find_town(name, state):
    url, data = get("/towns.json")
    want = name.strip().lower()
    hits = [t for t in data["towns"] if t[2].lower() == want and (not state or t[3].upper() == state.upper())]
    if not hits:
        raise NotFound("town not found: no town named %r%s in the town list. Ask the person for the state."
                       % (name, " in " + state.upper() if state else ""))
    hits.sort(key=lambda t: -(t[4] or 0))
    others = sorted({t[3] for t in hits[1:] if t[3] != hits[0][3]})
    return hits[0], others


def stay_of(slug):
    """The record's own stay-limit number, read from the camp record. None = unrecorded; "?" = could not read."""
    try:
        url, d = get("/api/camps/" + urllib.parse.quote(slug))
    except CouldNotRead:
        return "?"
    return ((d.get("camp") or {}).get("rules") or {}).get("stay_limit_days")


def trim(c):
    stay = stay_of(c["slug"]) if c.get("slug") else None
    if stay == "?":
        stay_text, stay = "could not read the record", None
    else:
        stay_text = ("%s days" % stay) if stay is not None else "unrecorded"
    return {
        "name": c.get("name"),
        "slug": c.get("slug"),
        "state": c.get("state"),
        "miles": c.get("miles"),
        "cost": c.get("cost"),
        "cost_evidence": c.get("cost_evidence"),
        "land_manager": c.get("land_manager") or None,
        "camp_type": c.get("camp_type"),
        "water": c.get("water"),
        "site_details": c.get("site_details") or None,
        "stay_limit_days": stay,
        "stay_limit": stay_text,
        "record_url": c.get("url"),
    }


def free_near(lat, lon, radius):
    url, data = get("/api/near", {"lat": lat, "lon": lon, "radius": radius, "limit": 100})
    free = [c for c in data.get("camps", []) if c.get("cost") == "free"]
    return url, data, free


def answer(name, state, radius, limit):
    (lat, lon, tname, tstate, _), others = find_town(name, state)
    url, data, free = free_near(lat, lon, radius)
    out = {
        "request_url": url,
        "source": "American Adventurer records (davelalande.com); the record's own source is named inside",
        "record_date": record_date(data),
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "credit": CREDIT,
        "osm_note": OSM,
        "distance_unit": "straight-line miles",
        "unrecorded_rule": "A null or missing field is UNRECORDED. Do not estimate it.",
        "town": {"name": tname, "state": tstate, "lat": lat, "lon": lon, "source": "davelalande.com/towns.json"},
        "town_also_in_states": others,
        "town_page": None,
        "radius_miles": float(radius),
        "free_count": len(free),
        "free_count_is_minimum": len(data.get("camps", [])) >= 100,
        "free_count_note": ("counted among the nearest 100 camps the API returned (any cost), so a busy area may hold more"
                            if len(data.get("camps", [])) >= 100 else "counted among all camps the API returned inside the radius"),
        "camps": [trim(c) for c in free[:limit]],
        "zero_result": None,
    }
    if not free:
        url2, data2, free2 = free_near(lat, lon, WIDE)
        out["zero_result"] = {
            "said": "No free camps on record within %g miles of %s, %s." % (radius, tname, tstate),
            "widened_radius_miles": WIDE,
            "request_url": url2,
            "nearest_free_camp": trim(free2[0]) if free2 else None,
        }
    return out


def line(c):
    bits = [c["name"], "%s mi" % c["miles"] if c["miles"] is not None else "miles unrecorded",
            c["land_manager"] or "manager unrecorded"]
    if c["water"]:
        bits.append("water: %s" % (c["water"] if isinstance(c["water"], str) else json.dumps(c["water"])))
    bits.append("stay limit: %s" % c["stay_limit"])
    return ", ".join(bits) + ". " + (c["record_url"] or "record link unrecorded")


def text(o):
    t = o["town"]
    out = []
    if o["free_count"]:
        out.append("%s%d free camps are on record within %g miles of %s, %s. The %d nearest:"
                   % ("At least " if o["free_count_is_minimum"] else "", o["free_count"], o["radius_miles"], t["name"], t["state"], len(o["camps"])))
        out += ["%d. %s" % (i, line(c)) for i, c in enumerate(o["camps"], 1)]
        out.append("Each is free on its record's evidence. Miles are straight-line, not drive miles.")
    else:
        z = o["zero_result"]
        out.append(z["said"])
        c = z["nearest_free_camp"]
        out.append(("Nearest free camp on record (within %d miles): " % WIDE + line(c)) if c
                   else "None within %d miles either." % WIDE)
    out.append("Record date: %s. Source: %s" % (o["record_date"] or "unrecorded", o["source"]))
    out.append(o["credit"])
    return "\n".join(out)


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description="Free camps on record near a town (read-only).")
    p.add_argument("town")
    p.add_argument("--state", help="two-letter state, e.g. OR")
    p.add_argument("--limit", type=int, default=5)
    p.add_argument("--radius", type=float, default=25)
    p.add_argument("--json", action="store_true", help="print the JSON envelope instead of plain text")
    a = p.parse_args(argv)
    try:
        o = answer(a.town, a.state, a.radius, max(1, a.limit))
    except NotFound as e:
        print("ERROR: " + str(e), file=sys.stderr)
        sys.exit(2)
    except CouldNotRead as e:
        print("ERROR: " + str(e), file=sys.stderr)
        sys.exit(1)
    print(json.dumps(o, indent=2, ensure_ascii=False) if a.json else text(o))


if __name__ == "__main__":
    main()
