#!/usr/bin/env python3
"""Attic Insulation Payback — degree-day heat-loss model, honest savings
and payback for attic top-ups, diminishing-returns table, R-value reality
check. Stdlib only."""
import argparse

# settled/in-service R per inch (h·ft²·°F/Btu per inch)
R_PER_INCH = {
    "cellulose": 3.2,       # blown, settles ~20% over a decade
    "fiberglass": 2.9,      # blown
    "fiberglass-batt": 3.1,
    "rockwool": 3.3,
    "open-cell-foam": 3.6,
}
SETTLE = {"cellulose": 0.80, "fiberglass": 0.90, "fiberglass-batt": 0.95,
          "rockwool": 0.95, "open-cell-foam": 1.0}

# fuel energy content and units
FUELS = {
    #  name: (Btu per unit, unit name)
    "gas": (100_000, "therm"),
    "oil": (138_500, "gallon"),
    "propane": (91_500, "gallon"),
    "electric": (3_412, "kWh"),
    "heatpump": (3_412, "kWh (site)"),  # COP applied via --system-eff
}


def season_loss(area, r, hdd, eff):
    """Annual heating Btu delivered-to-attic, per R-value."""
    # Q = U*A*HDD*24 ; fuel input = Q / system efficiency
    u = 1.0 / r
    btu = u * area * hdd * 24.0
    return btu / eff


def fmt_fuel(btuh_in, fuel):
    btu_per, unit = FUELS[fuel]
    return btuh_in / btu_per, unit


def cmd_rcheck(a):
    r_in = R_PER_INCH[a.material]
    label = r_in * a.inches
    settled = label * SETTLE[a.material]
    print(f"R-CHECK — {a.inches} in of {a.material}")
    print(f"  label R-value:    R-{label:.0f}  (at {r_in}/inch, full loft)")
    print(f"  in-service R:     R-{settled:.0f}  (settlement factor "
          f"{SETTLE[a.material]:.0%} for aged {a.material})")
    if a.material == "cellulose" and a.inches >= 10:
        print("  note: pre-2010 cellulose settles harder; measure depth at")
        print("  5+ spots and use the LOW reading, not the average.")
    if settled < 30:
        print("  verdict: thin attic — top-up has real savings potential.")
    elif settled < 49:
        print("  verdict: moderate — mid-curve, savings are real but check")
        print("  the diminishing-returns table before paying for R-60.")
    else:
        print("  verdict: already deep — further R buys very little;")


def cmd_payback(a):
    btu_per, unit = FUELS[a.fuel]
    loss_now = season_loss(a.area, a.r_current, a.hdd, a.system_eff)
    loss_new = season_loss(a.area, a.r_target, a.hdd, a.system_eff)
    saved_btu = loss_now - loss_new
    saved_units = saved_btu / btu_per
    saved_usd = saved_units * a.price

    print(f"ATTIC INSULATION PAYBACK — {a.area:.0f} ft², "
          f"R-{a.r_current:.0f} -> R-{a.r_target:.0f}, "
          f"{a.fuel} @ ${a.price:.2f}/{unit}")
    un, _ = fmt_fuel(loss_now, a.fuel)
    nn, _ = fmt_fuel(loss_new, a.fuel)
    print(f"  season heat loss now:   {un:,.1f} {unit}s (R-{a.r_current:.0f})")
    print(f"  season heat loss after: {nn:,.1f} {unit}s (R-{a.r_target:.0f})")
    print(f"  annual savings:         ~{saved_units:,.1f} {unit}s = "
          f"${saved_usd:,.0f}/yr")

    # calibration against winter bills
    if a.calibrate_winter_therms:
        # winter-month usage given (assumed gas therms; convert if needed)
        winter_units = a.calibrate_winter_therms
        attic_share = un / (winter_units * 5)  # ~5 winter months
        print(f"\n  CALIBRATION: model attic loss = {un:,.0f} {unit}s/yr vs")
        print(f"  meter {winter_units * 5:,.0f} {unit}s over ~5 winter months")
        if attic_share > 0.40:
            scale = 0.40 / attic_share
            print(f"  [FLAG] attic = {attic_share:.0%} of winter fuel —")
            print(f"  implausible (>40%); windows/walls/basement usually")
            print(f"  take a share. Rescaling savings by {scale:.2f} to a")
            print(f"  defensible 40% ceiling:")
            saved_units *= scale
            saved_usd *= scale
            print(f"  calibrated savings: ~{saved_units:,.1f} {unit}s = "
                  f"${saved_usd:,.0f}/yr")
        else:
            print(f"  attic = {attic_share:.0%} of winter fuel — plausible.")

    if a.quote:
        payback = a.quote / saved_usd if saved_usd > 0 else float("inf")
        print(f"\n  payback on ${a.quote:,.0f} quote: {payback:.1f} yr", end="")
        if payback <= 7:
            print("   [DO IT]")
        elif payback <= 15:
            print("   [BORDERLINE — rebate or DIY math needed]")
        else:
            print("   [NOT WORTH IT at this price]")
    else:
        payback = None

    # diminishing returns table
    print("\n  diminishing returns (savings vs staying at R-"
          f"{a.r_current:.0f}):")
    for r in (30, 38, 49, 60):
        if r <= a.r_current:
            continue
        s = (season_loss(a.area, a.r_current, a.hdd, a.system_eff)
             - season_loss(a.area, r, a.hdd, a.system_eff)) / btu_per * a.price
        print(f"    R-{r:<3} ${s:,.0f}/yr", end="")
        if a.quote:
            # pro-rated material cost by R thickness (approx linear)
            frac = (r - a.r_current) / (a.r_target - a.r_current)
            print(f"   (~${a.quote * frac:,.0f} pro-rated)", end="")
        print()

    # air-sealing doctrine
    print("\n  DOCTRINE: seal before you stack — moving air through")
    print("  fiberglass carries heat straight through; unsealed can lights,")
    print("  chases and top plates walk away with the savings. Air sealing")
    print("  is typically $200-600 DIY and often returns faster than R.")
    if payback is not None:
        if a.r_current >= 38 and payback > 7:
            print("\nVERDICT: OVERSOLD — SEAL FIRST. Your attic is already")
            print("  past the knee; spend on air sealing, not depth.")
        elif payback <= 7 and a.r_current < 30:
            print("\nVERDICT: DO IT — textbook case (thin attic, short payback).")
        elif payback <= 15:
            print("\nVERDICT: BORDERLINE — with a utility rebate (often")
            print("  30-50% up to caps) or a DIY blow machine rental this")
            print("  turns into a clear win; at full contractor price it's")
            print("  marginal. Get the R-38 price — the last R is the")
            print("  most expensive and the least valuable.")
        else:
            print("\nVERDICT: NOT WORTH IT at this price — the savings")
            print("  curve has flattened; air sealing and other measures")
            print("  beat more depth.")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--r-check", action="store_true",
                   help="verify a quoted/existing R-value from depth+material")
    p.add_argument("--inches", type=float, help="insulation depth (inches)")
    p.add_argument("--material", choices=sorted(R_PER_INCH),
                   default="cellulose")
    p.add_argument("--area", type=float, help="attic floor area (ft²)")
    p.add_argument("--r-current", type=float, help="existing R-value")
    p.add_argument("--r-target", type=float, default=60)
    p.add_argument("--fuel", choices=sorted(FUELS), default="gas")
    p.add_argument("--hdd", type=float, default=5000,
                   help="heating degree days base 65F")
    p.add_argument("--price", type=float, default=3.0,
                   help="fuel price per unit (therm/gallon/kWh)")
    p.add_argument("--system-eff", type=float, default=0.8,
                   help="furnace/COP efficiency (0-1+, COP for heatpump)")
    p.add_argument("--quote", type=float, help="contractor quote ($)")
    p.add_argument("--calibrate-winter-therms", type=float,
                   help="avg winter-month fuel units from bills")
    a = p.parse_args()
    if a.r_check:
        if not a.inches:
            p.error("--r-check requires --inches")
        cmd_rcheck(a)
    else:
        for req in ("area", "r_current"):
            if getattr(a, req.replace("-", "_")) is None:
                p.error(f"--{req} is required unless --r-check")
        cmd_payback(a)


if __name__ == "__main__":
    main()
