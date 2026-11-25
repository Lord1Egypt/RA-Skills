#!/usr/bin/env python3
"""Funeral quote comparator and FTC Funeral Rule defender.

Input: JSON with funeral home quotes (line items) + cemetery options.
Output:
  1. Per-home itemized comparison vs national median bands
  2. Padding flags (embalming on cremation, hidden basic fee, vault-as-law, package delta)
  3. Path trade-off table: direct cremation / cremation+viewing / burial / green burial
  4. Negotiation script + rights card (FTC 16 CFR 453 citations)

stdlib only.
"""
import argparse
import json
import sys

MEDIANS = {  # NFDA-style medians; keys are line-item ids
    "basic_services": (2300, (1500, 2700)),
    "direct_cremation": (2500, (1000, 3000)),   # excl. basic fee at some shops
    "immediate_burial": (3300, (2000, 4000)),
    "viewing_service": (5200, (3500, 7000)),
    "embalming": (775, (500, 1000)),
    "other_prep": (300, (150, 500)),
    "casket_steel18": (2500, (900, 2500)),
    "burial_vault": (1825, (1000, 3500)),
    "rental_casket": (1000, (800, 1200)),
    "cremation_container": (150, (0, 200)),
    "hearse": (350, (250, 500)),
    "death_certificate": (15, (6, 30)),
    "obituary": (300, (150, 600)),
}

NAMES = {
    "basic_services": "non-declinable basic services fee",
    "direct_cremation": "direct cremation (w/ container)",
    "immediate_burial": "immediate burial (no viewing)",
    "viewing_service": "viewing + ceremony",
    "embalming": "embalming",
    "other_prep": "other prep (dress/cosmetic)",
    "casket_steel18": "casket 18ga steel",
    "burial_vault": "burial vault",
    "rental_casket": "rental casket (view+cremate)",
    "cremation_container": "alt. cremation container",
    "hearse": "hearse (local)",
    "death_certificate": "death certificate (each)",
    "obituary": "obituary placement",
}


def flag(item, price, ctx):
    """Padding detectors."""
    out = []
    if item == "embalming" and price > 0 and ctx.get("plan") in ("direct_cremation", "immediate_burial"):
        out.append("EMBALMING NOT REQUIRED for this plan (no viewing): REFUSE this line "
                   "(FTC 453.4(f); refrigeration is lawful)")
    if item == "burial_vault" and price > 0 and ctx.get("vault_claimed_law"):
        out.append("VAULT IS NOT LAW — cemetery contract maybe; ask which cemetery rule "
                   "in writing + whether grave liner (cheaper) passes")
    if item == "basic_services" and price > MEDIANS["basic_services"][1][1]:
        out.append(f"basic fee ${price} above fair band ${MEDIANS['basic_services'][1][1]} "
                   "— ask what it covers, negotiate hours-based items instead")
    if item == "casket_steel18" and price > 2000:
        out.append("casket > $2,000: identical-gauge retail (Costco/Amazon) $900-1,500; "
                   "they cannot charge an outside-casket fee (453.4(b)(2))")
    if item == "cremation_container" and price > 200:
        out.append("container >$200: many shops loan free; ask for the LEAST expensive option")
    lo, hi = MEDIANS.get(item, (0, (0, 0)))[1]
    if price > hi:
        out.append(f"above fair band (${lo}-{hi})")
    return out


def cmd_compare(args):
    data = json.load(open(args.quotes))
    homes = data["homes"]
    ctx = data.get("context", {})

    print("=" * 78)
    for h in homes:
        name, items = h["name"], h["items"]
        flags = 0
        print(f"\nHOME: {name}")
        total = 0
        for item, price in items.items():
            if item not in MEDIANS:
                print(f"  {item:<34} ${price:>7,}   (not in band table)")
                total += price
                continue
            med, (lo, hi) = MEDIANS[item]
            mark = "ok" if lo <= price <= hi else ("HIGH" if price > hi else "low")
            print(f"  {NAMES[item]:<34} ${price:>7,}   median ${med:,} [{mark}]")
            total += price
            for f in flag(item, price, ctx):
                print(f"      ⚠ {f}")
                flags += 1
        if h.get("package_price"):
            print(f"  {'TOTAL (quoted package)':<34} ${h['package_price']:>7,}")
            print(f"  {'TOTAL (sum of listed items)':<34} ${total:>7,}")
            if h["package_price"] > total:
                print(f"      ⚠ package costs ${h['package_price']-total:,} MORE than its own "
                      "items à la carte — demand the GPL and re-price (453.4(d))")
                flags += 1
        else:
            print(f"  {'TOTAL (items)':<34} ${total:>7,}")
        print(f"  flags: {flags}")
    if ctx.get("plan") == "direct_cremation":
        print("\n" + "=" * 78)
        print("PATH COMPARISON (cremation family):")
        for h in homes:
            items = dict(h["items"])
            direct = items.get("direct_cremation", 0) + items.get("basic_services", 0) \
                + items.get("cremation_container", 0)
            print(f"  {h['name']:<14} direct cremation all-in ≈ ${direct:>7,}")
            viewing = direct + items.get("viewing_staff_add", 475) + items.get("rental_casket", 1000)
            print(f"  {'':<14} + viewing/rental casket ≈ ${viewing:>7,}  "
                  "(rental casket, NOT purchase)")
    if ctx.get("plan") == "burial":
        cem = data.get("cemetery", {})
        plot = cem.get("plot", 2500); open_ = cem.get("opening", 1200)
        vault = cem.get("vault", 1400); marker = cem.get("marker", 2000)
        ctotal = plot + open_ + vault + marker
        print("\n" + "=" * 78)
        print(f"CEMETERY (the other half): plot ${plot:,} + open/close ${open_:,} + "
              f"vault ${vault:,} + marker ${marker:,} = ${ctotal:,}")
        print("  ⚠ Price the cemetery separately from the funeral home — it's often 50% "
              "of burial cost and never on the GPL")
        green = cem.get("green_option")
        if green:
            print(f"  Green/natural burial option nearby: ~${green:,} all-in "
                  "(no vault, shroud/plain wood)")
    print("\n" + "=" * 78)
    print("RIGHTS CARD (read aloud, FTC Funeral Rule 16 CFR 453):")
    print("  - 'I'd like the General Price List, itemized' — required, phone quotes too")
    print("  - 'I'm declining embalming' — not required by law except narrow state cases")
    print("  - 'I'm providing my own casket/urn' — no refusal, no fee, no presence required")
    print("  - 'No packages; charge only items I select' (453.4(d))")
    print("  - 'Cash advances (certificates, obituary) at cost, itemized' (453.4(e))")
    print("  - Complaints: FTC ReportFraud.ftc.gov + your state funeral board")
    print("\nGet 3 GPLs before signing anything. Cross out declined items and initial.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("quotes", help="path to quotes JSON")
    args = ap.parse_args()
    cmd_compare(args)


if __name__ == "__main__":
    main()
