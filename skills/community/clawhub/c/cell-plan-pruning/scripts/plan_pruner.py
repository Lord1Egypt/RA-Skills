#!/usr/bin/env python3
"""cell-plan-pruning — audit a mobile bill against real usage; compute pruning savings.

Modes:
  --demo            built-in 4-line family bill audit
  --bill bill.json  your bill (see bill.example.json for the shape)
  --insurance AGE VALUE PREMIUM DEDUCTIBLE   one-line device-protection verdict

Stdlib only.
"""
from __future__ import annotations

import argparse
import json

# --------------------------------------------------------- usage classes
def usage_class(gb_month: float) -> str:
    if gb_month < 2:
        return "LIGHT"
    if gb_month < 5:
        return "LIGHT"
    if gb_month < 15:
        return "MEDIUM"
    return "HEAVY"


RECOMMENDED = {
    "LIGHT":  {"shape": "capped 2-5 GB plan", "mvno_all_in": 20, "postpaid_all_in": 70},
    "MEDIUM": {"shape": "10-15 GB or small unlimited", "mvno_all_in": 32, "postpaid_all_in": 80},
    "HEAVY":  {"shape": "unlimited with hotspot cap", "mvno_all_in": 48, "postpaid_all_in": 90},
}


def insurance_verdict(phone_age_mo: int, value: float, premium_mo: float,
                      deductible: float) -> dict:
    cost_18mo = premium_mo * 18 + deductible
    keep_bar = 0.40 * value
    if value < 400 or phone_age_mo > 24:
        verdict = "DROP"
        why = (f"phone age {phone_age_mo}mo / value ${value:,.0f} — premium+deductible "
               f"(${cost_18mo:,.0f} over 18mo) exceeds rational coverage")
    elif cost_18mo < keep_bar:
        verdict = "KEEP"
        why = f"18-mo cost ${cost_18mo:,.0f} < 40% of value (${keep_bar:,.0f}) — defensible"
    else:
        verdict = "DROP"
        why = f"18-mo cost ${cost_18mo:,.0f} >= 40% of value (${keep_bar:,.0f}) — self-insure"
    return {"verdict": verdict, "reason": why,
            "cost_18mo": round(cost_18mo, 2),
            "annual_premium": round(premium_mo * 12, 2)}


# --------------------------------------------------------- bill audit
ADDON_FAIR = {
    "cloud": (0, 5, "photos back up fine to free tiers; OEM gives 5-15 GB"),
    "visual voicemail": (0, 3, "free on most MVNOs/prepaid"),
    "premium voicemail": (0, 3, "same"),
    "device protection": (0, 25, "see insurance verdict per phone"),
    "insurance": (0, 25, "same"),
    "applecare": (0, 20, "drop after year 2 per breakeven"),
    "smartwatch": (10, 15, "only if actually paired"),
    "international": (0, 15, "travel eSIMs usually cheaper per trip"),
}


def audit_bill(bill: dict) -> dict:
    lines = bill["lines"]
    verdicts = []
    tax = bill.get("tax_rate", 0.18)
    prem_sum = sum(l["premium"] for l in lines)
    ins_sum = sum(l["insurance"]["premium_mo"] for l in lines if l.get("insurance"))
    addon_sum = sum(a.get("amount", 0) for a in bill.get("addons", []))
    # all-in monthly total: recurring charges + tax
    total_now = bill.get("monthly_total") or round((prem_sum + ins_sum + addon_sum) * (1 + tax), 2)

    # 1) per-line: usage class vs what's paid
    bucket_savings = 0.0
    for l in lines:
        uc = usage_class(l["gb_month"])
        rec = RECOMMENDED[uc]
        line_all_in = l["premium"] * (1 + bill.get("tax_rate", 0.18))
        if line_all_in > rec["mvno_all_in"] * 1.15:
            action = "SWITCH (MVNO)"
            save = (line_all_in - rec["mvno_all_in"]) * 12
        elif line_all_in > rec["postpaid_all_in"]:
            action = "DOWNGRADE tier"
            save = (line_all_in - rec["postpaid_all_in"]) * 12
        else:
            action, save = "KEEP", 0.0
        bucket_savings += save
        verdicts.append({
            "line": l["name"], "usage": f"{l['gb_month']} GB/mo ({uc})",
            "pays_all_in": round(line_all_in, 2),
            "recommended": rec["shape"],
            "action": action,
            "annual_saving": round(save, 2),
        })

    # 2) insurance per phone (taxed like everything else)
    ins_savings = 0.0
    for l in lines:
        ins = l.get("insurance")
        if not ins:
            continue
        v = insurance_verdict(ins.get("age_mo", 30), ins.get("value", 300),
                              ins["premium_mo"], ins.get("deductible", 150))
        save = ins["premium_mo"] * (1 + tax) * 12 if v["verdict"] == "DROP" else 0.0
        verdicts.append({"line": f"{l['name']} insurance", "usage": "-",
                         "pays_all_in": round(ins["premium_mo"] * (1 + tax), 2),
                         "recommended": v["verdict"], "action": v["verdict"],
                         "annual_saving": round(save, 2),
                         "why": v["reason"]})
        ins_savings += save

    # 3) add-ons (taxed)
    addon_savings = 0.0
    for a in bill.get("addons", []):
        nm = a["name"].lower()
        for kw, (lo, hi, why) in ADDON_FAIR.items():
            if kw in nm:
                if a["amount"] > hi:
                    save = a["amount"] * (1 + tax) * 12
                    verdicts.append({"line": a["name"], "usage": "-",
                                     "pays_all_in": round(a["amount"] * (1 + tax), 2),
                                     "recommended": f"${lo}-{hi}/mo fair",
                                     "action": "DROP add-on", "why": why,
                                     "annual_saving": round(save, 2)})
                    addon_savings += save
                else:
                    verdicts.append({"line": a["name"], "usage": "-",
                                     "pays_all_in": round(a["amount"] * (1 + tax), 2),
                                     "recommended": "fair",
                                     "action": "KEEP", "annual_saving": 0.0, "why": why})
                break

    # bucket-size sanity: sum actual vs sum of what's bought
    actual_gb = sum(l["gb_month"] for l in lines)
    return {
        "current_monthly": round(total_now, 2),
        "current_annual": round(total_now * 12, 2),
        "total_usage_gb": round(actual_gb, 1),
        "n_lines": len(lines),
        "verdicts": verdicts,
        "annual_savings": {
            "plan_tier_or_mvno": round(bucket_savings, 2),
            "insurance_drops": round(ins_savings, 2),
            "addons": round(addon_savings, 2),
            "TOTAL": round(bucket_savings + ins_savings + addon_savings, 2),
        },
    }


DEMO_BILL = {
    "tax_rate": 0.18,
    "lines": [
        {"name": "adult-1", "gb_month": 11, "premium": 62,
         "insurance": {"age_mo": 30, "value": 320, "premium_mo": 17, "deductible": 200}},
        {"name": "adult-2", "gb_month": 8, "premium": 62,
         "insurance": {"age_mo": 10, "value": 900, "premium_mo": 17, "deductible": 200}},
        {"name": "teen", "gb_month": 26, "premium": 62},
        {"name": "grandma", "gb_month": 1.5, "premium": 42},
    ],
    "addons": [
        {"name": "cloud storage 200GB", "amount": 10},
        {"name": "premium visual voicemail", "amount": 5},
    ],
}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--demo", action="store_true")
    p.add_argument("--bill", help="bill JSON (see bill.example.json)")
    p.add_argument("--insurance", nargs=4, metavar=("AGE_MO", "VALUE", "PREM_MO", "DEDUCT"),
                   help="device protection verdict: e.g. 30 320 17 200")
    args = p.parse_args()

    if args.demo or args.bill:
        bill = DEMO_BILL
        if args.bill:
            with open(args.bill) as f:
                bill = json.load(f)
        r = audit_bill(bill)
        print(f"CURRENT: ${r['current_monthly']:.0f}/mo  (${r['current_annual']:,.0f}/yr) "
              f"| {r['n_lines']} lines | {r['total_usage_gb']} GB/mo combined\n")
        print(f"{'ITEM':<26}{'PAYS':>8}  {'ACTION':<18}{'SAVES/yr':>10}")
        print("-" * 70)
        for v in r["verdicts"]:
            pay = v["pays_all_in"]
            pay_s = f"${pay:.0f}" if isinstance(pay, (int, float)) else str(pay)
            print(f"{v['line']:<26}{pay_s:>8}  {v['action']:<18}"
                  f"${v['annual_saving']:>9,.0f}")
            if "usage" in v and v["usage"] != "-":
                print(f"    usage {v['usage']} -> recommended: {v.get('recommended','')}")
            if v.get("why"):
                print(f"    why: {v['why']}")
        print("-" * 70)
        for k, v in r["annual_savings"].items():
            print(f"{k:<26}${v:>10,.0f}")
        return

    if args.insurance:
        age, val, prem, ded = map(float, args.insurance)
        print(json.dumps(insurance_verdict(int(age), val, prem, ded), indent=2))
        return

    p.print_help()


if __name__ == "__main__":
    main()
