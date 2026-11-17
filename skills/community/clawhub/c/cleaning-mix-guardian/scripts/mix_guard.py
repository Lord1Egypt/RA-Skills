#!/usr/bin/env python3
"""Cleaning Mix Guardian — pre-mix safety checker for household cleaners.

Checks product/ingredient combinations against a curated hazard database,
decodes common products to reactive classes, sequences multi-product
cleaning safely, and prints incident first-aid cards.

Stdlib-only. This is first-aid-level information; call poison control or
emergency services for real exposures.
"""
import argparse
import sys

# Reactive ingredient classes
CLASSES = {
    "bleach": "sodium hypochlorite (NaOCl)",
    "ammonia": "ammonia / ammonium compounds",
    "acid": "mineral or organic acid (HCl, citric, vinegar, oxalic)",
    "caustic": "strong base (NaOH, KOH)",
    "peroxide": "hydrogen peroxide (H2O2)",
    "alcohol": "isopropyl / ethanol",
    "detergent": "neutral surfactants (non-reactive class)",
}

# Common products -> reactive class (conservative where formulations vary)
PRODUCTS = {
    "bleach": ("bleach", "chlorine bleach, 3-6% NaOCl"),
    "chlorine bleach": ("bleach", ""),
    "toilet cleaner": ("acid", "usually 5-10% HCl (hydrochloric)"),
    "toilet bowl cleaner": ("acid", "usually 5-10% HCl"),
    "limescale remover": ("acid", "HCl or sulfamic acid"),
    "descaler": ("acid", "citric or sulfamic acid"),
    "rust remover": ("acid", "oxalic or phosphoric; some contain HF"),
    "vinegar": ("acid", "~5% acetic acid"),
    "glass cleaner": ("ammonia", "ammonia + surfactants (some are amine-free)"),
    "window cleaner": ("ammonia", ""),
    "ammonia cleaner": ("ammonia", "5-10% ammonia solution"),
    "drain cleaner": ("caustic", "NaOH/KOH (caustic) OR H2SO4 (acid) — READ LABEL"),
    "drain unblocker": ("caustic", ""),
    "oven cleaner": ("caustic", "NaOH in foam"),
    "dishwasher tabs": ("bleach", "many contain percarbonate (peroxide source)"),
    "laundry detergent": ("detergent", "neutral; enzyme/bleach variants exist"),
    "dish soap": ("detergent", "neutral (avoid mixing with bleach anyway)"),
    "hydrogen peroxide": ("peroxide", "3% H2O2 antiseptic / cleaner"),
    "otc peroxide": ("peroxide", ""),
    "rubbing alcohol": ("alcohol", "70% isopropyl"),
    "isopropyl alcohol": ("alcohol", ""),
    "all-purpose cleaner": ("detergent", "varies — read label; many are neutral"),
    "floor cleaner": ("detergent", ""),
    "baking soda": ("base", "sodium bicarbonate — mild base, low risk"),
    "washing soda": ("base", "sodium carbonate — stronger base"),
}

# Hazard pairs: (class_a, class_b) -> hazard dict
# class "base" (weak carbonates) treated separately from caustic.
HAZARDS = {
    frozenset(("bleach", "ammonia")): {
        "gas": "CHLORAMINE GAS (NH2Cl)",
        "sev": "CRITICAL",
        "symptoms": "throat/eye irritation, coughing, chest pain, "
                    "breathing difficulty; delayed pulmonary symptoms possible",
        "first_aid": "leave the area immediately; ventilate from outside; "
                     "fresh air 30+ min; medical care if breathing affected",
    },
    frozenset(("bleach", "acid")): {
        "gas": "CHLORINE GAS (Cl2)",
        "sev": "CRITICAL",
        "symptoms": "sharp odor, burning eyes/throat, coughing, chest "
                    "tightness; heavier than air — pools low (pets/kids first)",
        "first_aid": "evacuate NOW; open windows from outside if possible; "
                     "fresh air; urgent care if any breathing difficulty",
    },
    frozenset(("peroxide", "acid")): {
        "gas": "PERACETIC ACID vapor",
        "sev": "HIGH",
        "symptoms": "pungent vinegar-like odor, respiratory and eye "
                    "irritation, skin burns at concentration",
        "first_aid": "ventilate; flush skin/eyes 15 min with water; "
                     "medical care if irritation persists",
    },
    frozenset(("bleach", "peroxide")): {
        "gas": "OXYGEN gas + heat",
        "sev": "HIGH",
        "symptoms": "rapid gas release; in closed containers: pressure "
                    "rupture and spraying",
        "first_aid": "do NOT cap the container; ventilate; flush contact "
                     "areas with water",
    },
    frozenset(("bleach", "alcohol")): {
        "gas": "chlorinated compounds (chloroform-like at concentration)",
        "sev": "HIGH",
        "symptoms": "dizziness, nausea, irritation with significant "
                    "exposure in poor ventilation",
        "first_aid": "ventilate; fresh air; medical care if symptomatic",
    },
    frozenset(("caustic", "acid")): {
        "gas": "VIOLENT HEAT + spattering (neutralization)",
        "sev": "CRITICAL",
        "symptoms": "boiling/splashing of corrosive liquid; chemical burns "
                    "to skin/eyes on contact",
        "first_aid": "stay clear; if splashed: flush 15+ min, remove "
                     "clothing, emergency care for eye/large-area burns",
    },
    frozenset(("bleach", "caustic")): {
        "gas": "reduced hypochlorite activity; heat in concentration",
        "sev": "MODERATE",
        "symptoms": "mostly product degradation; splashing risk",
        "first_aid": "flush contact areas with water",
    },
    frozenset(("ammonia", "acid")): {
        "gas": "ammonium salts + heat (irritating fumes at heat)",
        "sev": "MODERATE",
        "symptoms": "irritating fumes, splattering",
        "first_aid": "ventilate; flush contacts with water",
    },
}

POISON_CARD = """
POISON CONTROL — save this before you need it
  US:    1-800-222-1222 (poisoncontrol.org)
  UK:    111 (NHS) / 999 in emergency
  EU:    112
If breathing is impaired: call emergency services FIRST.
"""

SAFE_WAIT = ("rinse the surface completely with water, flush drains with "
             "plenty of water, wait 15-30 min with ventilation before "
             "applying the other product")


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(2)


def resolve(name):
    n = name.strip().lower()
    if n in CLASSES:
        return n, CLASSES[n], name
    if n in PRODUCTS:
        cls, note = PRODUCTS[n]
        return cls, CLASSES.get(cls, cls) + (f" — {note}" if note else ""), name
    return None, None, name


def hazard_for(a, b):
    return HAZARDS.get(frozenset((a, b)))


def print_hazard(hz, label_a, label_b):
    print("✗ DO NOT MIX —", hz["sev"])
    print(f"  {label_a} + {label_b}")
    print(f"  → {hz['gas']}")
    print(f"  Symptoms: {hz['symptoms']}")
    print(f"  First aid: {hz['first_aid']}")
    print(POISON_CARD)


# ---------------------------------------------------------------- commands
def cmd_check(args):
    cls_a, chem_a, raw_a = resolve(args.a)
    cls_b, chem_b, raw_b = resolve(args.b)
    if cls_a is None or cls_b is None:
        unknown = raw_a if cls_a is None else raw_b
        print(f"⚠ Unknown product {unknown!r}. Treat as INCOMPATIBLE with")
        print("  everything: read the label for bleach/ammonia/acid")
        print("  declarations before mixing with anything.")
        return
    raws = {args.a.lower(), args.b.lower()}
    if any("drain" in r for r in raws):
        print("⚠ DRAIN CLEANER WARNING: some drain cleaners are CAUSTIC")
        print("  (NaOH) and some are STRONG ACID (H2SO4). They behave")
        print("  completely differently with bleach. Read the label.")
        print("  NEVER add a second chemistry to a drain that still contains")
        print("  product — acid-after-caustic can boil out of the drain.")
        print()
    hz = hazard_for(cls_a, cls_b)
    if hz:
        print_hazard(hz, args.a, args.b)
        if hz["sev"] in ("CRITICAL", "HIGH"):
            print("SAFE ALTERNATIVES: use ONE product per surface, or")
            print("  detergent-only cleaning between the two.")
        return
    if cls_a == cls_b:
        print(f"✓ Same class ({cls_a}) — mixing adds nothing; just use one.")
        return
    # special notes
    notes = {
        ("bleach", "detergent"): "plain detergent is generally OK with bleach "
            "BUT many soaps contain amines — check the label",
        ("base", "acid"): "baking soda + vinegar: harmless fizzing; cleans "
            "nothing after they neutralize each other",
    }
    note = notes.get((cls_a, cls_b)) or notes.get((cls_b, cls_a))
    print(f"✓ No known critical reaction between {cls_a} and {cls_b}.")
    if note:
        print(f"  Note: {note}.")
    print("  Still: never mix in a closed container; ventilate; label anything")
    print("  you decant.")


def cmd_products(args):
    print(f"{'Product':<22}{'Reactive class':<15}Notes")
    print("-" * 72)
    for name, (cls, note) in sorted(PRODUCTS.items()):
        print(f"{name:<22}{cls:<14}{note}")
    print()
    print("Formulations vary by brand and country — ALWAYS read the label.")
    print("When a product lists bleach/ammonia/acid anywhere, use its class.")


def cmd_sequence(args):
    items = [i.strip() for i in args.items.split(",") if i.strip()]
    resolved = []
    problems = []
    for it in items:
        cls, chem, raw = resolve(it)
        resolved.append((it, cls))
        if cls is None:
            problems.append(f"unknown product {it!r} — treat as incompatible")
    print("Safe-use sequence (one product at a time):")
    ok_pairs = []
    for i, (name_a, cls_a) in enumerate(resolved):
        for (name_b, cls_b) in resolved[i+1:]:
            if cls_a and cls_b and hazard_for(cls_a, cls_b):
                ok_pairs.append((name_a, name_b, hazard_for(cls_a, cls_b)))
    order_notes = []
    if ok_pairs:
        print(f"⚠ {len(ok_pairs)} dangerous pair(s) in this set:")
        for a, b, hz in ok_pairs:
            print(f"  ✗ {a} + {b} → {hz['gas']} ({hz['sev']})")
        print()
        print("Sequence rule: use ONE, then " + SAFE_WAIT + ",")
        print("then the next. Between bleach and acid: FULL water rinse,")
        print("flush toilets twice, 30 min ventilation minimum.")
    else:
        print("✓ No critical pairs detected — any order works.")
    for p in problems:
        print(f"⚠ {p}")
    print()
    print("Universal rules: ventilate; never mix in closed containers;")
    print("never add a second chemistry to a drain with product in it;")
    print("store acids and bleach in separate cupboards.")


def cmd_incident(args):
    cls_a, _, _ = resolve(args.a)
    cls_b, _, _ = resolve(args.b)
    print("=== INCIDENT MODE — act now ===")
    print("1. LEAVE THE ROOM. Do not lean over the mixture.")
    print("2. From outside: open windows/doors to the space if possible.")
    print("3. Fresh air; do not return for 30+ min or until odor is gone.")
    print("4. If ANYONE has breathing difficulty, coughing that doesn't")
    print("   stop, chest pain, or burning eyes that persist:")
    print("   call emergency services (911/112/999) IMMEDIATELY.")
    print()
    if cls_a and cls_b:
        hz = hazard_for(cls_a, cls_b)
        if hz:
            print(f"Probable release: {hz['gas']} ({hz['sev']})")
            print(f"Expected: {hz['symptoms']}")
        else:
            print("No critical reaction on record for this pair —")
            print("ventilation and observation still apply.")
    else:
        print("Pair not in database — assume irritant gas, ventilate.")
    print()
    print(POISON_CARD)
    print("Pets: remove them too (gases pool low). If a pet shows")
    print("drooling, coughing, lethargy — vet promptly.")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="First-aid information only — call poison control/emergency "
               "services for real exposures.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("check", help="can these two be mixed?")
    p.add_argument("--a", required=True)
    p.add_argument("--b", required=True)
    p.set_defaults(fn=cmd_check)

    p = sub.add_parser("products", help="product → reactive class table")
    p.set_defaults(fn=cmd_products)

    p = sub.add_parser("sequence", help="safe order for several products")
    p.add_argument("--items", required=True,
                   help="comma-separated product list")
    p.set_defaults(fn=cmd_sequence)

    p = sub.add_parser("incident", help="a mix already happened")
    p.add_argument("--a", required=True)
    p.add_argument("--b", required=True)
    p.set_defaults(fn=cmd_incident)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
