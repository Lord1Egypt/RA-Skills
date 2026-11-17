#!/usr/bin/env python3
"""evroadtrip.py — EV road-trip consumption model + DC charging stop solver.

Subcommands:
  consumption  physics-based Wh/km estimate (speed/temp/heat/cargo/grade)
  range        usable-kWh range at current SoC and consumption
  plan         leg-by-leg stop solver with buffers, taper, costs
  checklist    pre-departure checklist (preconditioning/adapters/apps/hotel)

Offline, stdlib only. Model, not gospel: override with the car's own
dashboard average whenever available.
"""
import argparse
import math

BASE_BY_CLASS = {"compact": 145, "sedan": 165, "suv": 195, "truck": 225}

ARRIVE_FLOOR = 10.0     # % SoC minimum at any DC stop
WINTER_EXTRA = 5.0      # added when temp < 0
TAPER_DISCOUNT = 0.75   # avg 10->80% power vs nameplate


def consumption(cls, speed, temp, heat_pump, cargo, grade):
    base = BASE_BY_CLASS.get(cls, 180)
    f = 1.0
    parts = [f"base {cls}: {base} Wh/km @110 km/h"]
    if speed:
        sf = 1 + 0.045 * (speed - 110)
        f *= max(sf, 0.75)
        parts.append(f"speed {speed}: ×{sf:.2f}")
    if temp is not None:
        dtn = max(0.0, 18 - temp)
        rate = 0.006 if heat_pump else 0.014
        tf = 1 + rate * dtn
        f *= tf
        parts.append(f"temp {temp:+.0f}°C ({'heat pump' if heat_pump else 'resistive'}): "
                     f"×{tf:.2f}")
    if cargo:
        cf = 1 + 0.02 * max(0, cargo - 150) / 100
        f *= cf
        if cargo > 150:
            parts.append(f"cargo {cargo} kg: ×{cf:.2f}")
    if grade:
        gf = 1 + 0.001 * grade
        f *= gf
        parts.append(f"net grade {grade:+.0f} m/km: ×{gf:.2f}")
    total = base * f
    print("EV CONSUMPTION ESTIMATE")
    print("═" * 62)
    for p in parts:
        print(f"  • {p}")
    print(f"→ {total:.0f} Wh/km at {speed or 110} km/h "
          f"({total / 1.609 * 1.0:.0f} Wh/mi)")
    print(f"  Reference band: {BASE_BY_CLASS['compact']} (compact, warm, calm) … "
          f"{BASE_BY_CLASS['truck'] * 1.4:.0f} (truck, freezing).")
    print("Override with the car's own trip average when it differs >10% — the "
          "dashboard beats the model.")
    return total


def plan(battery, usable, start_soc, consumption_wh, dc_kw, legs, names,
         price, temp, home_end):
    km_total = sum(legs)
    names = names or []
    floor = ARRIVE_FLOOR + (WINTER_EXTRA if (temp or 0) < 0 else 0)
    print(f"EV ROAD-TRIP STOP PLAN — {km_total} km, usable {usable:g} kWh, "
          f"start {start_soc:.0f}%")
    print(f"consumption {consumption_wh:.0f} Wh/km · DC min(vehicle {dc_kw:g} kW) "
          f"×{TAPER_DISCOUNT:.2f} taper · arrive floor {floor:.0f}%"
          + (" (winter)" if (temp or 0) < 0 else ""))
    print("═" * 78)
    print(f"{'Leg':<4}{'To':<14}{'km':>5}{'arrive':>9}{'charge':>10}"
          f"{'depart':>9}{'cost':>9}")
    soc = start_soc
    kwh_per_pct = usable / 100.0
    total_minutes = 0.0
    total_cost = 0.0
    n = len(legs)
    for i, km in enumerate(legs):
        use_kwh = km * consumption_wh / 1000.0
        arrive = soc - use_kwh / kwh_per_pct
        arrive = max(arrive, 0.0)
        is_last = (i == n - 1)
        nm = names[i] if i < len(names) else f"stop {i + 1}"
        if is_last and home_end:
            print(f"{i + 1:<4}{nm:<14}{km:>5.0f}{arrive:>8.0f}%{'— home':>10}"
                  f"{'—':>9}{'—':>9}")
            if arrive < floor:
                print(f"     ⚠ LAST LEG below floor ({arrive:.0f}% < {floor:.0f}%): "
                      "slow to −10 km/h or add a stop.")
            break
        # next leg need
        nxt = legs[i + 1] if i + 1 < n else 0
        nxt_kwh = nxt * consumption_wh / 1000.0
        need_pct = nxt_kwh / kwh_per_pct + floor
        # practical minimum: a 20-point bump ≈ a real stop; never exceed 80 unless next leg demands
        target = min(80.0, max(need_pct, arrive + 20.0))
        if target < arrive:
            target = arrive  # no charging needed
        if nxt == 0 and arrive >= floor:
            print(f"{i + 1:<4}{nm:<14}{km:>5.0f}{arrive:>8.0f}%{'— done':>10}"
                  f"{'—':>9}{'—':>9}")
            if arrive < floor:
                print(f"     ⚠ FINAL LEG below floor ({arrive:.0f}% < {floor:.0f}%): "
                      "slow to −10 km/h or add an earlier charger.")
            break
        add_kwh = (target - arrive) * kwh_per_pct
        eff_kw = dc_kw * TAPER_DISCOUNT
        minutes = add_kwh / eff_kw * 60.0
        cost = add_kwh * price
        total_minutes += minutes
        total_cost += cost
        over80 = " (past 80%: next leg demands it)" if target >= 79.9 and need_pct > 80 else ""
        print(f"{i + 1:<4}{nm:<14}{km:>5.0f}{arrive:>8.0f}%"
              f"{minutes:>7.0f} min{target:>8.0f}%  ${cost:>5.0f}{over80}")
        if arrive < floor:
            print(f"     ⚠ ARRIVAL BELOW FLOOR ({arrive:.0f}%): this plan is unsafe — "
                  "insert an earlier charger or slow down 10 km/h.")
        soc = target
    print("─" * 78)
    print(f"TOTAL: {n} legs, {total_minutes:.0f} DC minutes, "
          f"~${total_cost:.2f} DC charging")
    print("Doctrine: 10→80% zone only; meal stops cover 30–40 min; precondition the "
          "battery by making the charger the ACTIVE nav destination.")
    print("Fallback: headwind/grade eating margin → −10 km/h recovers ~12% consumption.")


CHECKLIST_ITEMS = [
    ("Battery preconditioning",
     "Make each DC charger the ACTIVE in-car nav destination 20–30 min before "
     "arrival — this is what warms the pack for fast charging. Non-navigated "
     "arrival at 0°C = half-rate charging."),
    ("Adapter + plugs",
     "Know your port (CCS1/CCS2/NACS) and carry approved adapters; check the "
     "car's Tesla/NACS access list — some cap speed via adapter."),
    ("Network accounts",
     "One app per network, installed AND topped-up with payment BEFORE the trip "
     "(NA: Tesla, EA, EVgo, ChargePoint, Shell; EU: check roaming). Card readers "
     "fail at the worst hours."),
    ("Charger health",
     "Check last-24–48 h status per stop in PlugShare/app; prefer corridors with "
     "2+ networks for redundancy."),
    ("Route margins",
     "Floors: ≥10% arrival (+5% winter), 15–20% at the last stop of the day."),
    ("Cables",
     "Type-2/portable 2–5 kW fallback cable + adapters for hotel/emergency "
     "trickle; extension rated for EV use."),
    ("Hotel L2",
     "Confirm destination charger in photos/reviews; arrive <20% only with "
     "confirmed overnight charging."),
    ("Cold-weather kit",
     "Seat heaters over cabin air (−1–2 kW); snow/ice on the car = aero penalty "
     "that shows up as range loss."),
    ("Tow coverage",
     "Roadside plan EV tow-to-charger coverage confirmed."),
]


def checklist(destination_country, winter):
    print("EV ROAD-TRIP PRE-DEPARTURE CHECKLIST"
          + (" (winter edition)" if winter else ""))
    print("═" * 62)
    for i, (title, body) in enumerate(CHECKLIST_ITEMS, 1):
        if winter or title not in ("Cold-weather kit",):
            print(f"[{i}] {title}\n     {body}")
    if destination_country and destination_country.lower() in ("eu", "europe", "de", "fr"):
        print("\nEU note: many AC public posts are type-2 cable-LOCKED — carry your "
              "own type-2 cable; some DC still need the operator's RFID/app.")
    print("\nNight-before: charge to 100% at home on L2 (cheap), depart warm and full.")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("consumption")
    p.add_argument("--car-class", default="suv", choices=list(BASE_BY_CLASS))
    p.add_argument("--speed", type=float, default=115, help="km/h")
    p.add_argument("--temp", type=float, default=None, help="°C")
    p.add_argument("--heat-pump", default="yes", choices=["yes", "no"])
    p.add_argument("--cargo", type=float, default=0, help="kg of load")
    p.add_argument("--grade", type=float, default=0, help="net m per km (+uphill)")

    p = sub.add_parser("range")
    p.add_argument("--usable", type=float, required=True, help="kWh")
    p.add_argument("--soc", type=float, default=100)
    p.add_argument("--consumption", type=float, required=True, help="Wh/km")

    p = sub.add_parser("plan")
    p.add_argument("--battery", type=float, required=True, help="nominal kWh (info only)")
    p.add_argument("--usable", type=float, required=True, help="usable kWh")
    p.add_argument("--start-soc", type=float, required=True)
    p.add_argument("--consumption", type=float, required=True, help="Wh/km")
    p.add_argument("--dc-kw", type=float, required=True,
                   help="min(vehicle max, station max) kW")
    p.add_argument("--legs", required=True,
                   help="comma-separated km between stops, last = destination")
    p.add_argument("--names", default="", help="comma-separated stop names")
    p.add_argument("--price", type=float, default=0.45, help="$/kWh DC")
    p.add_argument("--temp", type=float, default=None)
    p.add_argument("--home-end", action="store_true",
                   help="last leg ends at home L2 (night charge)")

    p = sub.add_parser("checklist")
    p.add_argument("--destination-country", default="")
    p.add_argument("--winter", action="store_true")

    a = ap.parse_args()
    if a.cmd == "consumption":
        consumption(a.car_class, a.speed, a.temp, a.heat_pump == "yes", a.cargo, a.grade)
    elif a.cmd == "range":
        kwh = a.usable * a.soc / 100.0
        print(f"RANGE: {kwh:.1f} kWh / {a.consumption:.0f} Wh/km = "
              f"{kwh / a.consumption * 1000:.0f} km "
              f"({kwh / a.consumption * 1000 / 1.609:.0f} mi) at {a.soc:.0f}%")
    elif a.cmd == "plan":
        legs = [float(x) for x in a.legs.split(",") if x.strip()]
        names = [x.strip() for x in a.names.split(",") if x.strip()] if a.names else []
        plan(a.battery, a.usable, a.start_soc, a.consumption, a.dc_kw, legs,
             names, a.price, a.temp, a.home_end)
    elif a.cmd == "checklist":
        checklist(a.destination_country, a.winter)


if __name__ == "__main__":
    main()
