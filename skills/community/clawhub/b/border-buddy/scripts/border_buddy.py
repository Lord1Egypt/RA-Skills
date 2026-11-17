#!/usr/bin/env python3
"""
border-buddy — pre-trip border intelligence.

Subcommands:
  check    — entry-readiness report (visa, passport, health, customs, transit)
  schengen — 90/180 rolling-window stay calculator
  rules    — dump the raw rule snapshot for one country
  demo     — run built-in sample scenarios end-to-end

Offline rules snapshot; always verify against the named authority before travel.
"""
import argparse
import csv
import json
import sys
from datetime import date, timedelta

SNAPSHOT_AS_OF = "2026-06"

GROUPS = {
    "WESTERN": {"US", "CA", "UK", "AU", "NZ", "JP", "KR", "SG", "HK", "MY", "MX", "AE", "IL"},
    "EU_EFTA": {"AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR",
                "HU", "IS", "IE", "IT", "LV", "LI", "LT", "LU", "MT", "NL", "NO", "PL",
                "PT", "RO", "SK", "SI", "ES", "SE", "CH"},
    "SOUTH_AMERICA": {"BR", "AR", "CL", "UY", "PY", "PE", "CO", "EC", "BO"},
    "SOUTH_ASIA": {"IN", "PK", "BD", "LK", "NP"},
    "AFRICA": {"NG", "GH", "KE", "ZA", "EG", "MA"},
}

YELLOW_FEVER_ENDEMIC = {
    "NG", "GH", "CD", "CI", "ML", "BF", "SN", "LR", "SL", "GN",
    "KE", "UG", "RW", "TZ", "AO", "CM", "GA", "CG", "TD", "SD",
    "ET", "SS", "BR", "CO", "PE", "EC", "BO", "PY", "VE", "PA",
}

VF = "visa_free"
VF60 = "visa_free_60"
VF30 = "visa_free_30"
VOA = "visa_on_arrival"
ETA = "eta"
EVISA = "evisa"
REQ = "visa_required"
MIXED = "mixed"

# Each destination: visa_policy group -> (policy, max_stay_days_or_None, note)
RULES = {
    "PT": {
        "name": "Portugal", "authority": "sef.pt / vistos.mne.gov.pt", "schengen": True,
        "visa_policy": {
            "EU_EFTA": (VF, None, "freedom of movement"),
            "WESTERN": (VF, 90, "Schengen 90/180 window"),
            "SOUTH_AMERICA": (VF, 90, "Schengen 90/180 window"),
            "SOUTH_ASIA": (REQ, 90, "Schengen short-stay visa (type C)"),
            "AFRICA": (REQ, 90, "Schengen short-stay visa"),
        },
        "passport_validity": "schengen_3mo",
        "yellow_fever": "if_from_endemic",
        "customs": "1L spirits (>22%) or 2L <22% + 4L wine + 200 cig. Cash >= EUR 10,000 must be declared.",
        "transit": {
            "WESTERN": ("no_visa", "airside transit"),
            "SOUTH_ASIA": ("no_visa_airside", "airport transit visa if landside or changing airports"),
            "SOUTH_AMERICA": ("no_visa", "airside transit visa-free"),
        },
    },
    "FR": {
        "name": "France", "authority": "france-visas.gouv.fr", "schengen": True,
        "visa_policy": {
            "EU_EFTA": (VF, None, "freedom of movement"),
            "WESTERN": (VF, 90, "Schengen 90/180"),
            "SOUTH_AMERICA": (VF, 90, "Schengen 90/180"),
            "SOUTH_ASIA": (REQ, 90, "Schengen short-stay visa"),
            "AFRICA": (REQ, 90, "Schengen short-stay visa"),
        },
        "passport_validity": "schengen_3mo",
        "yellow_fever": "if_from_endemic",
        "customs": "1L spirits + 4L wine + 200 cig. Cash >= EUR 10,000 declare.",
        "transit": {
            "WESTERN": ("no_visa", "airside"),
            "SOUTH_ASIA": ("no_visa_airside", "ATV needed if leaving international zone"),
            "SOUTH_AMERICA": ("no_visa", "airside transit visa-free"),
        },
    },
    "DE": {
        "name": "Germany", "authority": "auswaertiges-amt.de", "schengen": True,
        "visa_policy": {
            "EU_EFTA": (VF, None, "freedom of movement"),
            "WESTERN": (VF, 90, "Schengen 90/180"),
            "SOUTH_AMERICA": (VF, 90, "Schengen 90/180"),
            "SOUTH_ASIA": (REQ, 90, "Schengen short-stay visa"),
            "AFRICA": (REQ, 90, "Schengen short-stay visa"),
        },
        "passport_validity": "schengen_3mo",
        "yellow_fever": "if_from_endemic",
        "customs": "1L spirits + 4L wine + 200 cig. Cash >= EUR 10,000 declare.",
        "transit": {
            "WESTERN": ("no_visa", "airside"),
            "SOUTH_ASIA": ("no_visa_airside", "airport transit visa for some nationalities - verify"),
            "SOUTH_AMERICA": ("no_visa", "airside transit visa-free"),
        },
    },
    "ES": {
        "name": "Spain", "authority": "exterior.gob.es", "schengen": True,
        "visa_policy": {
            "EU_EFTA": (VF, None, "freedom of movement"),
            "WESTERN": (VF, 90, "Schengen 90/180"),
            "SOUTH_AMERICA": (VF, 90, "Schengen 90/180"),
            "SOUTH_ASIA": (REQ, 90, "Schengen short-stay visa"),
            "AFRICA": (REQ, 90, "Schengen short-stay visa"),
        },
        "passport_validity": "schengen_3mo",
        "yellow_fever": "if_from_endemic",
        "customs": "1L spirits + 4L wine + 200 cig. Cash >= EUR 10,000 declare.",
        "transit": {
            "WESTERN": ("no_visa", "airside"),
            "SOUTH_ASIA": ("no_visa_airside", "verify if changing airports"),
            "SOUTH_AMERICA": ("no_visa", "airside transit visa-free"),
        },
    },
    "IT": {
        "name": "Italy", "authority": "vistoperitalia.esteri.it", "schengen": True,
        "visa_policy": {
            "EU_EFTA": (VF, None, "freedom of movement"),
            "WESTERN": (VF, 90, "Schengen 90/180"),
            "SOUTH_AMERICA": (VF, 90, "Schengen 90/180"),
            "SOUTH_ASIA": (REQ, 90, "Schengen short-stay visa"),
            "AFRICA": (REQ, 90, "Schengen short-stay visa"),
        },
        "passport_validity": "schengen_3mo",
        "yellow_fever": "if_from_endemic",
        "customs": "1L spirits + 4L wine + 200 cig. Cash >= EUR 10,000 declare.",
        "transit": {
            "WESTERN": ("no_visa", "airside"),
            "SOUTH_ASIA": ("no_visa_airside", "verify"),
            "SOUTH_AMERICA": ("no_visa", "airside transit visa-free"),
        },
    },
    "US": {
        "name": "United States", "authority": "travel.state.gov (ESTA/visas)", "schengen": False,
        "visa_policy": {
            "EU_EFTA": (ETA, 90, "ESTA required pre-departure (Visa Waiver Program)"),
            "WESTERN": (ETA, 90, "ESTA for UK/JP/KR/AU/NZ/SG; CA exempt"),
            "SOUTH_AMERICA": (ETA, 90, "CL/AR/BR/UY on VWP; others need B visa"),
            "SOUTH_ASIA": (REQ, None, "B1/B2 visa required"),
            "AFRICA": (REQ, None, "B1/B2 visa required"),
        },
        "passport_validity": "valid_for_stay",
        "yellow_fever": "not_required",
        "customs": "1L alcohol, $800 duty exemption. Cash >= $10,000 declare (FinCEN 105).",
        "transit": {
            "WESTERN": ("no_visa", "airside (VWP nationals still need ESTA)"),
            "SOUTH_ASIA": ("transit_visa_required", "C-1 transit visa or B visa; no airside-only transit"),
        },
    },
    "UK": {
        "name": "United Kingdom", "authority": "gov.uk/uk-visas-immigration", "schengen": False,
        "visa_policy": {
            "EU_EFTA": (VF, 180, "6-month standard visit; ETA required for many"),
            "WESTERN": (VF, 180, "6 months; US/CA/AU/NZ/JP/KR/SG need ETA"),
            "SOUTH_AMERICA": (VF, 180, "AR/BR/CL/PE/UY visa-free 6 months; ETA required"),
            "SOUTH_ASIA": (REQ, 180, "Standard Visitor visa"),
            "AFRICA": (REQ, 180, "Standard Visitor visa"),
        },
        "passport_validity": "valid_for_stay",
        "yellow_fever": "if_from_endemic",
        "customs": "42L beer + 4L spirits + 200 cig allowances. Cash >= GBP 10,000 declare when asked.",
        "transit": {
            "WESTERN": ("no_visa", "airside"),
            "SOUTH_ASIA": ("transit_visa_required", "Direct Airside Transit Visa (DATV) unless exempt - verify"),
        },
    },
    "JP": {
        "name": "Japan", "authority": "mofa.go.jp / japan eVISA", "schengen": False,
        "visa_policy": {
            "EU_EFTA": (VF, 90, "temporary visitor"),
            "WESTERN": (VF, 90, "temporary visitor (US/CA/UK/AU/NZ/HK/SG/KR)"),
            "SOUTH_AMERICA": (VF, 90, "AR/BR/CL/UY/PE temporary visitor"),
            "SOUTH_ASIA": (REQ, 90, "temporary visitor visa"),
            "AFRICA": (REQ, 90, "temporary visitor visa"),
        },
        "passport_validity": "valid_for_stay",
        "yellow_fever": "not_required",
        "customs": "3 bottles (760ml) alcohol + 200 cig. Cash >= JPY 1,000,000 declare.",
        "transit": {
            "WESTERN": ("no_visa", "airside"),
            "SOUTH_ASIA": ("no_visa_airside", "same-airport international transit OK"),
        },
    },
    "TH": {
        "name": "Thailand", "authority": "thaiembassy.com", "schengen": False,
        "visa_policy": {
            "EU_EFTA": (VF60, 60, "60-day exemption + 30-day extension possible"),
            "WESTERN": (VF60, 60, "60-day exemption"),
            "SOUTH_AMERICA": (VF60, 60, "60-day exemption for BR/AR"),
            "SOUTH_ASIA": (EVISA, 60, "e-Visa 60 days"),
            "AFRICA": (EVISA, 60, "e-Visa"),
        },
        "passport_validity": "six_months",
        "yellow_fever": "if_from_endemic",
        "customs": "1L alcohol duty-free. Cash >= THB 450,000 declare.",
        "transit": {
            "WESTERN": ("no_visa", "airside"),
            "SOUTH_ASIA": ("no_visa_airside", "12h same-airport airside OK"),
        },
    },
    "CN": {
        "name": "China", "authority": "bio.visa.passport.gov.cn / chineseembassy", "schengen": False,
        "visa_policy": {
            "EU_EFTA": (REQ, 30, "L visa; 30-day visa-free pilot for FR/DE/IT/NL/ES - verify current list"),
            "WESTERN": (REQ, 30, "L visa; some pilots for JP/SG - verify"),
            "SOUTH_AMERICA": (REQ, 30, "L visa"),
            "SOUTH_ASIA": (REQ, 30, "L visa"),
            "AFRICA": (REQ, 30, "L visa"),
        },
        "passport_validity": "six_months",
        "yellow_fever": "if_from_endemic",
        "customs": "1L alcohol + 400 cig (2 cartons) for stays >6 months differs. Cash > CNY 20,000 declare.",
        "transit": {
            "WESTERN": ("no_visa_airside", "24h TWOV airside; 144h landside for many nationalities"),
            "SOUTH_ASIA": ("no_visa_airside", "24h TWOV airside only"),
        },
    },
    "AE": {
        "name": "United Arab Emirates", "authority": "icp.gov.ae", "schengen": False,
        "visa_policy": {
            "EU_EFTA": (VOA, 90, "free visa on arrival, 90 days"),
            "WESTERN": (VOA, 90, "free VoA 90d (US/UK/JP/KR/SG/AU/NZ/CA)"),
            "SOUTH_AMERICA": (VOA, 90, "AR/BR/CL VoA 90d"),
            "SOUTH_ASIA": (EVISA, 60, "eVisa via airline/sponsor"),
            "AFRICA": (EVISA, 60, "eVisa (ZA VoA 90d - verify)"),
        },
        "passport_validity": "six_months",
        "yellow_fever": "if_from_endemic",
        "customs": "4L alcohol (non-Muslims; emirate rules vary). Cash >= AED 100,000 declare.",
        "transit": {
            "WESTERN": ("no_visa", "airside"),
            "SOUTH_ASIA": ("no_visa_airside", "Dubai 96h transit visa available"),
        },
    },
    "TR": {
        "name": "Türkiye", "authority": "e-visa.gov.tr", "schengen": False,
        "visa_policy": {
            "EU_EFTA": (VF, 90, "90/180-style rule"),
            "WESTERN": (VF, 90, "US/UK visa-free 90d"),
            "SOUTH_AMERICA": (VF, 90, "AR/BR visa-free"),
            "SOUTH_ASIA": (EVISA, 30, "IN conditional e-Visa (hold US/UK/Schengen visa or residence)"),
            "AFRICA": (EVISA, 30, "e-Visa"),
        },
        "passport_validity": "six_months_beyond_departure",
        "yellow_fever": "if_from_endemic",
        "customs": "1L alcohol + 200 cig. Cash threshold varies - declare above USD 5,000 equivalent to be safe.",
        "transit": {
            "WESTERN": ("no_visa", "airside"),
            "SOUTH_ASIA": ("no_visa_airside", "airside OK"),
        },
    },
    "BR": {
        "name": "Brazil", "authority": "gov.br/mre", "schengen": False,
        "visa_policy": {
            "EU_EFTA": (VF, 90, "90 days per 180, extendable"),
            "WESTERN": (EVISA, 90, "US/CA citizens: eVisa required (2025 reciprocity); UK/JP/KR visa-free"),
            "SOUTH_AMERICA": (VF, 90, "most neighbors visa-free"),
            "SOUTH_ASIA": (EVISA, 90, "eVisa for tourism"),
            "AFRICA": (EVISA, 90, "evisa.gov.br"),
        },
        "passport_validity": "valid_for_stay",
        "yellow_fever": "domestic_risk",
        "customs": "personal items up to $1,000 duty-free; limited alcohol units. Cash >= BRL equivalent of USD 10,000 declare.",
        "transit": {
            "WESTERN": ("no_visa", "airside"),
            "SOUTH_ASIA": ("no_visa_airside", "airside OK"),
        },
    },
    "IN": {
        "name": "India", "authority": "indianvisaonline.gov.in", "schengen": False,
        "visa_policy": {
            "EU_EFTA": (ETA, 60, "e-Visa (30/365-day options)"),
            "WESTERN": (ETA, 60, "US/UK/CA/AU e-Visa"),
            "SOUTH_AMERICA": (EVISA, 60, "e-Visa"),
            "SOUTH_ASIA": (REQ, None, "traditional visa (NP special arrangements)"),
            "AFRICA": (ETA, 60, "e-Visa for many"),
        },
        "passport_validity": "six_months",
        "yellow_fever": "if_from_endemic",
        "customs": "2L alcohol if staying >24h. Cash > USD 5,000 (or 10,000 combined) declare.",
        "transit": {
            "WESTERN": ("no_visa", "airside"),
            "SOUTH_ASIA": ("no_visa_airside", "airside transit OK"),
        },
    },
    "EG": {
        "name": "Egypt", "authority": "visa2egypt.gov.eg", "schengen": False,
        "visa_policy": {
            "EU_EFTA": (VOA, 30, "VoA $25 / e-Visa"),
            "WESTERN": (VOA, 30, "VoA $25 / e-Visa (US/UK/CA)"),
            "SOUTH_AMERICA": (VOA, 30, "VoA $25"),
            "SOUTH_ASIA": (EVISA, 30, "e-Visa (IN: e-Visa, no VoA)"),
            "AFRICA": (MIXED, 30, "varies; MA visa-free"),
        },
        "passport_validity": "six_months",
        "yellow_fever": "if_from_endemic",
        "customs": "1L alcohol + 200 cig. Cash > USD 10,000 declare.",
        "transit": {
            "WESTERN": ("no_visa_airside", "airside OK"),
            "SOUTH_ASIA": ("no_visa_airside", "airside OK"),
        },
    },
    "ZA": {
        "name": "South Africa", "authority": "dha.gov.za", "schengen": False,
        "visa_policy": {
            "EU_EFTA": (VF, 90, "90 days"),
            "WESTERN": (VF, 90, "US/UK/CA/AU 90d visa-free"),
            "SOUTH_AMERICA": (MIXED, 90, "BR 90d; AR/CL varies - verify"),
            "SOUTH_ASIA": (REQ, 30, "consulate visa"),
            "AFRICA": (MIXED, 90, "many SADC visa-free"),
        },
        "passport_validity": "six_months_beyond_departure",
        "yellow_fever": "if_from_endemic",
        "customs": "200 cig + 2L wine + 1L spirits. Cash > ZAR 25,000 declare.",
        "transit": {
            "WESTERN": ("no_visa", "airside"),
            "SOUTH_ASIA": ("no_visa_airside", "verify"),
        },
    },
    "AU": {
        "name": "Australia", "authority": "homeaffairs.gov.au", "schengen": False,
        "visa_policy": {
            "EU_EFTA": (ETA, 90, "eVisitor (EU, free) - 90 days per visit"),
            "WESTERN": (ETA, 90, "US/CA/JP/KR/SG: ETA; UK: eVisitor; NZ: Special Category"),
            "SOUTH_AMERICA": (ETA, 90, "AR/BR/CL/UY/PE eVisitor/ETA"),
            "SOUTH_ASIA": (REQ, 90, "Visitor 600 visa"),
            "AFRICA": (REQ, 90, "Visitor 600 visa"),
        },
        "passport_validity": "valid_for_stay",
        "yellow_fever": "if_from_endemic",
        "customs": "2.25L alcohol. Strict biosecurity - declare ALL food. Cash >= AUD 10,000 declare.",
        "transit": {
            "WESTERN": ("no_visa", "airside 8h"),
            "SOUTH_ASIA": ("transit_visa_required", "Transit 771 visa or ETA needed even airside for IN/PK - verify"),
        },
    },
    "CA": {
        "name": "Canada", "authority": "canada.ca/ircc", "schengen": False,
        "visa_policy": {
            "EU_EFTA": (ETA, 180, "eTA, 6 months per entry"),
            "WESTERN": (ETA, 180, "UK/JP/KR/AU/NZ/SG eTA; US visa-exempt"),
            "SOUTH_AMERICA": (MIXED, 180, "CL/AR/BR/UY eTA-eligible with conditions - verify"),
            "SOUTH_ASIA": (REQ, 180, "visitor visa (TRV)"),
            "AFRICA": (REQ, 180, "visitor visa (TRV)"),
        },
        "passport_validity": "valid_for_stay",
        "yellow_fever": "not_required",
        "customs": "1.5L wine or 1.14L spirits; personal exemption CAD 200-800. Cash >= CAD 10,000 declare.",
        "transit": {
            "WESTERN": ("no_visa", "airside (eTA for VWP-type nationals)"),
            "SOUTH_ASIA": ("transit_visa_required", "TRV or China Transit Program routes - verify"),
        },
    },
    "AR": {
        "name": "Argentina", "authority": "migraciones.gob.ar", "schengen": False,
        "visa_policy": {
            "EU_EFTA": (VF, 90, "90 days, extendable"),
            "WESTERN": (VF, 90, "US/CA/UK/AU visa-free"),
            "SOUTH_AMERICA": (VF, 90, "neighbors visa-free"),
            "SOUTH_ASIA": (REQ, 90, "consulate visa"),
            "AFRICA": (REQ, 90, "consulate visa"),
        },
        "passport_validity": "valid_for_stay",
        "yellow_fever": "if_from_endemic",
        "customs": "3L alcohol + 400 cig. Cash > USD 10,000 declare.",
        "transit": {
            "WESTERN": ("no_visa", "airside"),
            "SOUTH_ASIA": ("no_visa_airside", "airside OK"),
        },
    },
}


def group_of(nationality: str) -> str:
    for g, members in GROUPS.items():
        if nationality in members:
            return g
    return "OTHER"


def parse_date(s):
    return date.fromisoformat(s)


# --- Schengen 90/180 calculator ---------------------------------------------
def presence_days(visits, start: date, end: date) -> int:
    """Count presence days in [start, end]. Entry day counts, exit day does not."""
    total = 0
    for v in visits:
        lo = max(v["entry"], start)
        hi = min(v["exit"] - timedelta(days=1), end)
        if lo <= hi:
            total += (hi - lo).days + 1
    return total


def schengen_report(visits, ref: date):
    win_start = ref - timedelta(days=179)
    used = presence_days(visits, win_start, ref)
    exits = []
    for v in visits:
        d = v["entry"] + timedelta(days=180)
        if d >= ref:
            exits.append({"date": d.isoformat(), "note": f"presence from {v['entry'].isoformat()} stops counting"})
    remaining = 90 - used
    details = {
        "window": [win_start.isoformat(), ref.isoformat()],
        "days_used": used,
        "remaining": remaining,
        "overstay": max(0, used - 90),
        "window_exit_dates": sorted(exits, key=lambda w: w["date"])[:6],
    }
    return used, remaining, details


def next_safe_entry(visits, desired_days: int, base: date, horizon_days: int = 365):
    """Earliest entry date on which a desired_days stay is legal on its final day."""
    for delta in range(0, horizon_days):
        d = base + timedelta(days=delta)
        candidate = visits + [{"entry": d, "exit": d + timedelta(days=desired_days)}]
        used, _, _ = schengen_report(candidate, d + timedelta(days=desired_days - 1))
        if used <= 90:
            return d.isoformat(), used
    return None, None


# --- Visa / passport checks ---------------------------------------------------
def visa_verdict(policy_tuple, stay_days):
    if not policy_tuple:
        return "UNKNOWN - no snapshot rule for this nationality group", "UNKNOWN"
    policy, max_stay, note = policy_tuple
    label = {
        VF: "NOT REQUIRED",
        VF60: "NOT REQUIRED (60-day exemption)",
        VF30: "NOT REQUIRED (30-day exemption)",
        VOA: "VISA ON ARRIVAL",
        ETA: "ETA/eVISITOR REQUIRED",
        EVISA: "eVISA REQUIRED",
        REQ: "VISA REQUIRED",
        MIXED: "VARIES - verify",
    }.get(policy, policy.upper())
    free = label.startswith("NOT REQUIRED")
    flag = "\u26a0" if (not free and ("REQUIRED" in label or "VARIES" in label)) else "\u2713"
    if max_stay and stay_days and stay_days > max_stay:
        label += f" - \u26a0 STAY {stay_days}d EXCEEDS {max_stay}d LIMIT"
        flag = "\u26a0"
    return f"{label} ({note}) [{flag}]", label


def passport_check(rule, expiry: date, entry: date, departure: date):
    out = []
    if rule == "six_months":
        need = entry + timedelta(days=182)
        out.append((expiry >= need, f"six-month rule: expiry {expiry} must be >= {need} (entry+6mo)"))
    elif rule == "six_months_beyond_departure":
        need = departure + timedelta(days=182)
        out.append((expiry >= need, f"expiry must be >= {need} (departure+6mo)"))
    elif rule == "schengen_3mo":
        need = departure + timedelta(days=90)
        out.append((expiry >= need, f"Schengen rule: expiry >= departure+3mo = {need}; passport issued within last 10 years"))
    else:  # valid_for_stay
        out.append((expiry > departure, f"valid through stay: expiry {expiry} > departure {departure}"))
    return out


def yellow_fever_check(mode, coming_from):
    if mode == "not_required":
        return "not required"
    if mode == "domestic_risk":
        return "recommended (domestic risk areas); certificate REQUIRED if arriving from endemic country"
    if coming_from and coming_from in YELLOW_FEVER_ENDEMIC:
        return f"REQUIRED - arriving from endemic country {coming_from}"
    return "not required (not arriving from an endemic country)"


def load_visits(path):
    if path.endswith(".json"):
        data = json.loads(open(path).read())
        return [{"entry": parse_date(v["entry"]), "exit": parse_date(v["exit"]),
                 "country": v.get("country", "")} for v in data]
    rows = list(csv.DictReader(open(path)))
    return [{"entry": parse_date(r["entry"]), "exit": parse_date(r["exit"]),
             "country": r.get("country", "")} for r in rows]


# --- Subcommands ---------------------------------------------------------------
def cmd_check(args):
    nat = args.nationality.upper()
    dest = args.destination.upper()
    entry = parse_date(args.entry_date) if args.entry_date else date.today()
    dep = entry + timedelta(days=args.stay_days or 0)
    group = group_of(nat)
    rule = RULES.get(dest)
    if not rule:
        print(f"No snapshot for {dest}. Verify with the destination's foreign ministry.")
        return 1
    lines = []
    add = lines.append
    add(f"ENTRY READINESS - {rule['name']} ({dest}) for {nat} nationals [group: {group}]")
    add(f"  snapshot as_of {SNAPSHOT_AS_OF} - always verify before booking")
    add("")
    pol = rule["visa_policy"].get(group)
    visa_line, verdict = visa_verdict(pol, args.stay_days)
    add(f"  Visa:         {visa_line}")
    if rule.get("schengen") and group != "EU_EFTA":
        add("                \u2514 shared 90/180 Schengen pool - budget across ALL Schengen states")
    if args.passport_expiry:
        for ok, msg in passport_check(rule["passport_validity"],
                                      parse_date(args.passport_expiry), entry, dep):
            sym = "\u2713" if ok else "\u2717 FAIL"
            add(f"  Passport:     {sym} - {msg}")
    else:
        add(f"  Passport:     (no expiry given - rule: {rule['passport_validity']})")
    if args.transit:
        for tp in args.transit:
            tp = tp.upper()
            trule = RULES.get(tp, {}).get("transit", {}).get(group)
            if trule:
                tv, tnote = trule
                add(f"  Transit {tp}:   {tv.replace('_', ' ').upper()} ({tnote})")
            else:
                add(f"  Transit {tp}:   no snapshot - verify; most same-airport airside transits are visa-free")
    yf = yellow_fever_check(rule.get("yellow_fever"),
                            args.coming_from.upper() if args.coming_from else None)
    add(f"  Yellow fever: {yf}")
    add(f"  Customs:      {rule.get('customs', 'n/a')}")
    add(f"  Purpose note: answers assume {args.purpose}; work/study changes visa class")
    add(f"  VERIFY WITH:  {rule['authority']}")
    print("\n".join(lines))
    return 0


def cmd_schengen(args):
    visits = load_visits(args.visits)
    ref = parse_date(args.on) if args.on else date.today()
    used, remaining, details = schengen_report(visits, ref)
    print(f"SCHENGEN 90/180 - as of {ref}")
    print(f"  window:       {details['window'][0]} -> {details['window'][1]}")
    print(f"  days used:    {used} / 90")
    print(f"  remaining:    {remaining}")
    if details["overstay"]:
        print(f"  \u26a0 OVERSTAY by {details['overstay']} day(s) as of {ref}")
    if args.plan_days:
        base = max(ref, date.today())
        d, u = next_safe_entry(visits, args.plan_days, base)
        if d:
            print(f"  next safe entry for a {args.plan_days}-day stay: {d} (uses {u}/90 on final day)")
        else:
            print(f"  no safe entry found within horizon for a {args.plan_days}-day stay")
    if details["window_exit_dates"]:
        print("  days leaving the window soonest:")
        for w in details["window_exit_dates"]:
            print(f"    {w['date']}  {w['note']}")
    return 0


def cmd_rules(args):
    dest = args.destination.upper()
    rule = RULES.get(dest)
    if not rule:
        print(f"No snapshot entry for {dest}.")
        return 1
    print(json.dumps(rule, indent=2))
    return 0


def cmd_demo(args):
    print("=== DEMO 1: BR -> PT with DE transit, 42 days ===")
    a = argparse.Namespace(nationality="BR", destination="PT", transit=["DE"],
                           stay_days=42, purpose="tourism", passport_expiry="2027-03-01",
                           entry_date="2026-09-01", coming_from=None)
    cmd_check(a)
    print()
    print("=== DEMO 2: IN -> FR, 10 days, passport tight ===")
    a = argparse.Namespace(nationality="IN", destination="FR", transit=[],
                           stay_days=10, purpose="tourism",
                           passport_expiry="2026-11-30", entry_date="2026-05-10",
                           coming_from=None)
    cmd_check(a)
    print()
    print("=== DEMO 3: Schengen overstay scenario ===")
    visits = [
        {"entry": "2026-01-10", "exit": "2026-04-09", "country": "PT"},
        {"entry": "2026-06-01", "exit": "2026-06-20", "country": "ES"},
    ]
    import tempfile, os
    tf = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(visits, tf)
    tf.close()
    cmd_schengen(argparse.Namespace(visits=tf.name, on="2026-06-20", plan_days=None))
    os.unlink(tf.name)
    print()
    print("=== DEMO 4: recovery plan after heavy usage ===")
    visits2 = [{"entry": "2026-01-10", "exit": "2026-04-09", "country": "PT"}]
    tf2 = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(visits2, tf2)
    tf2.close()
    cmd_schengen(argparse.Namespace(visits=tf2.name, on="2026-08-18", plan_days=20))
    os.unlink(tf2.name)
    return 0


def main():
    p = argparse.ArgumentParser(description="border-buddy: pre-trip border intelligence")
    sub = p.add_subparsers(dest="cmd")
    c = sub.add_parser("check", help="entry-readiness report")
    c.add_argument("--nationality", required=True, help="passport country ISO code, e.g. BR")
    c.add_argument("--destination", required=True, help="destination ISO code, e.g. PT")
    c.add_argument("--transit", nargs="*", default=[], help="transit ISO codes")
    c.add_argument("--stay-days", type=int)
    c.add_argument("--purpose", default="tourism")
    c.add_argument("--passport-expiry", help="YYYY-MM-DD")
    c.add_argument("--entry-date", help="YYYY-MM-DD")
    c.add_argument("--coming-from", help="country you depart from (yellow fever)")
    s = sub.add_parser("schengen", help="90/180 rolling-window calculator")
    s.add_argument("--visits", required=True, help="visits JSON/CSV file")
    s.add_argument("--on", help="reference date YYYY-MM-DD (default today)")
    s.add_argument("--plan-days", type=int, help="find next safe entry for this stay length")
    r = sub.add_parser("rules", help="dump raw snapshot for a destination")
    r.add_argument("--destination", required=True)
    sub.add_parser("demo", help="run built-in sample scenarios")
    args = p.parse_args()
    if args.cmd == "check":
        return cmd_check(args)
    if args.cmd == "schengen":
        return cmd_schengen(args)
    if args.cmd == "rules":
        return cmd_rules(args)
    if args.cmd == "demo":
        return cmd_demo(args)
    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
