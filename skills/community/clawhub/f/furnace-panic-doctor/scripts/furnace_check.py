#!/usr/bin/env python3
"""furnace_check.py — no-tools furnace diagnostic: questions -> verdict -> steps.

Interactive tree + symptom lookup + freeze-risk math + technician brief.
Pure stdlib. This is decision support, not a substitute for a licensed
technician on gas/fuel/oil systems.
"""
import argparse
import json
import math
import os
import sys
import time

DEFAULT_LOG = os.path.join(os.path.expanduser("~"), ".furnace_log.json")
LOG_NOTE = ("Note: incidents are logged to ~/.furnace_log.json ONLY when you "
            "pass --log or finish an interactive run; nothing is written "
            "silently. Disable entirely with --no-log.")

SAFETY_STOP = {
    "co_alarm": ("CARBON MONOXIDE ALARM",
                 "STOP. Get everyone outside NOW. Call 911 or your gas "
                 "utility's emergency line from OUTSIDE. Do not re-enter "
                 "until cleared by firefighters/utility. Do not open "
                 "windows 'to air it out' before they arrive - it makes "
                 "source diagnosis harder."),
    "sulfur_smell": ("ROTTEN-EGG / SULFUR SMELL (gas additive)",
                     "STOP. No switches, no thermostat, no phone inside if "
                     "smell is strong. Leave, call the gas utility "
                     "emergency line from outside. If smell is faint and "
                     "constant: still leave and call."),
    "fuel_oil_smell": ("FUEL OIL SMELL",
                       "STOP diagnosing. Oil leak/Spill or delayed "
                       "ignition risk. Furnace switch OFF if safely "
                       "reachable, ventilate, call oil service company "
                       "emergency line."),
    "smoke_soot": ("SMOKE OR SOOT AT REGISTERS / FURNACE",
                   "STOP. Soot means combustion problems - possible cracked "
                   "heat exchanger (CO risk). Furnace OFF at the switch. "
                   "Emergency HVAC line. Do not run it 'just a bit'."),
    "burning_electrical": ("BURNING ELECTRICAL SMELL (sharp, acrid, like "
                           "burning plastic/wiring)",
                           "Furnace switch OFF at once. Breaker OFF if the "
                           "switch is hot or smell is strong. That smell "
                           "is melting insulation - fire risk. Emergency "
                           "electrician/HVAC."),
}

SYMPTOMS = {
    "no heat": {
        "causes": [
            ("thermostat blank/dead batteries", "DIY", 30),
            ("furnace switch off (looks like light switch)", "DIY", 0),
            ("tripped breaker", "DIY", 0),
            ("clogged filter tripping high-limit", "DIY", 15),
            ("pilot out / igniter failure", "PRO if relight fails", 300),
            ("gas valve closed or failed", "PRO", 350),
            ("control board failure", "PRO", 600),
        ],
    },
    "weak heat": {
        "causes": [
            ("filter clogged (airflow starved)", "DIY", 15),
            ("registers closed/blocked", "DIY", 0),
            ("blower wheel fouled", "PRO", 250),
            ("duct leakage / wrong sizing", "PRO", 800),
            ("undersized unit or dying burner", "PRO", 900),
        ],
    },
    "short cycling": {
        "causes": [
            ("filter clogged -> overheat -> high-limit trip", "DIY", 15),
            ("registers too closed", "DIY", 0),
            ("flame sensor dirty", "PRO (clean)", 150),
            ("thermostat anticipator/mislocation", "DIY/PRO", 200),
            ("cracked heat exchanger (serious)", "PRO", 2500),
        ],
    },
    "blows cold": {
        "causes": [
            ("thermostat set to FAN ON instead of AUTO", "DIY", 0),
            ("pilot/igniter not working", "PRO", 300),
            ("gas valve not opening", "PRO", 350),
            ("limit switch stuck open", "PRO", 250),
        ],
    },
    "pilot out": {
        "causes": [
            ("draft blew it out (door slam/wind)", "DIY relight", 0),
            ("thermocouple worn", "PRO", 150),
            ("gas supply pressure issue", "PRO", 250),
        ],
    },
    "blower runs constantly": {
        "causes": [
            ("thermostat fan switch on ON", "DIY", 0),
            ("fan limit switch stuck", "PRO", 250),
            ("thermostat wire shorted", "PRO", 200),
        ],
    },
    "loud bang on ignition": {
        "causes": [
            ("delayed ignition (gas buildup then boom)", "PRO URGENT", 350),
            ("ductwork expanding (pop, harmless)", "NONE", 0),
        ],
    },
    "scraping noise": {
        "causes": [
            ("blower wheel rubbing housing / broken mount", "PRO OFF NOW", 350),
        ],
    },
    "screech squeal": {
        "causes": [
            ("blower motor bearings dry", "PRO", 300),
            ("belt worn (older units)", "PRO/brave DIY", 120),
        ],
    },
    "water around furnace": {
        "causes": [
            ("condensate drain clogged (high-eff units)", "DIY", 0),
            ("condensate pump failed", "DIY/PRO", 150),
            ("AC evaporator coil frozen/leaking", "PRO", 400),
        ],
    },
    "burning dust smell at season start": {
        "causes": [
            ("dust burning off heat exchanger", "DIY (normal first run)", 0),
        ],
    },
}

FREEZE_ADVICE = (
    "Freeze protection while waiting: open cabinet doors under sinks on "
    "exterior walls; drip the COLD faucet furthest from the heater (thin "
    "pencil stream); keep house above 10C with one room + door closed "
    "strategy; if inside temp will pass below 7C before help arrives - "
    "shut the main water and drain the lowest faucet."
)

NO_LOG = {"disabled": False}


def ask(prompt):
    try:
        ans = input(prompt + " [y/n/skip] ").strip().lower()
    except EOFError:
        return None
    if ans in ("y", "yes"):
        return True
    if ans in ("n", "no"):
        return False
    return None


def safety_triage():
    print("=" * 64)
    print("SAFETY TRIAGE — answer before anything else")
    print("=" * 64)
    for key, (title, action) in SAFETY_STOP.items():
        hit = ask(f"{title.split('(')[0].strip()}?")
        if hit:
            print("\n" + "!" * 64)
            print(f"STOP-NOW: {title}\n{action}")
            print("!" * 64)
            return key
    print("No safety stops. Continuing.\n")
    return None


def tree_questions():
    """Returns list of (component, ok) findings; asks in order."""
    findings = []
    steps = [
        ("thermostat",
         "Thermostat: display alive? (blank = batteries/wiring)",
         "Replace batteries; if still blank, check furnace switch/breaker"),
        ("power",
         "Furnace switch ON? (wall switch near unit; looks like light switch)",
         "Flip it ON. Also check the breaker labeled FURNACE/HEATER/AIR HANDLER"),
        ("fan",
         "Set thermostat FAN to ON: does the blower run?",
         "Blower runs = power OK. If not: switch/breaker/blower-motor issue"),
        ("fuel",
         "Gas valve handle PARALLEL to the pipe? (perpendicular = closed)",
         "Open valve slowly. For oil: check tank gauge. Propane: check %"),
        ("filter",
         "Filter visibly gray/dusty? (hold up: can you see light through it?)",
         "Replace filter NOW (arrow toward blower) before anything else"),
        ("ignition",
         "Watch one cycle: does igniter glow / pilot light / burners fire?",
         "No ignition = igniter/flame sensor/gas valve - PRO territory"),
        ("burner",
         "Flame BLUE and steady across all burners?",
         "Yellow/flickering = combustion problem - PRO, mention CO risk"),
        ("blower_start",
         "Blower starts within ~60s of flame?",
         "Flame but no blower = limit/fan switch or motor capacitor - PRO"),
        ("vent",
         "Exhaust pipe outdoors clear? (snow/nest/debris)",
         "Clear it; blocked vent trips pressure switches (and is a CO risk)"),
    ]
    for comp, question, hint in steps:
        print(f"\n[{comp.upper()}] {question}")
        print(f"  if not: {hint}")
        r = ask("  OK?")
        findings.append((comp, r))
    return findings


def symptom_lookup(name):
    key = None
    for k in SYMPTOMS:
        if name.lower() in k or k in name.lower():
            key = k
            break
    return key


def print_symptom(key):
    entry = SYMPTOMS[key]
    print("=" * 64)
    print(f"SYMPTOM: {key.upper()}")
    print("=" * 64)
    print(f"{'cause':<52} {'who':<16} {'cost $':>6}")
    for cause, who, cost in entry["causes"]:
        print(f"{cause:<52} {who:<16} {cost:>6}")
    diy = [c for c, w, _ in entry["causes"] if "DIY" in w]
    if diy:
        print("\nTry the DIY items first, in order, one at a time; "
              "power-cycle the furnace switch 30s between attempts.")


def freeze_risk():
    print("\n--- FREEZE RISK MATH ---")
    try:
        inside = float(input("Inside temp now (C): "))
        outside = float(input("Outside temp now (C): "))
        hours = float(input("Hours until help arrives: "))
    except (ValueError, EOFError):
        print(FREEZE_ADVICE)
        return
    # Newton cooling: T(t) = T_out + (T_in - T_out) * exp(-t/tau)
    # tau ~16h for a typical house; wind/poor insulation -> ~8h
    tau = 16.0
    final = outside + (inside - outside) * math.exp(-hours / tau)
    first_hour_drop = (inside - outside) * (1 - math.exp(-1 / tau))
    print(f"First-hour drop ~{first_hour_drop:.1f} C; decay constant "
          f"{tau:.0f}h (windy/leaky house: halve it)")
    print(f"Projected temp in {hours:.0f}h: {final:.1f} C")
    if final <= 7:
        print("PIPE-FREEZE ZONE: " + FREEZE_ADVICE)
    elif final <= 12:
        print("Cold but safe-ish: drip the farthest cold faucet, keep one "
              "room warm, check again in 2h.")
    else:
        print("House holds: normal-hours service call is fine.")


def brief(findings, symptom, extra=""):
    print("\n" + "=" * 64)
    print("TECHNICIAN BRIEFING — hand the phone/tech this")
    print("=" * 64)
    print(f"Date: {time.strftime('%Y-%m-%d %H:%M')}")
    print(f"Symptom: {symptom or '(interactive tree)'}")
    if findings:
        print("Checked:")
        for comp, ok in findings:
            state = "OK" if ok else ("NOT OK <-" if ok is False else "skipped")
            print(f"  - {comp}: {state}")
    if extra:
        print(extra)
    print("Model/serial plate: inside burner compartment door or side panel "
          "(photo before calling).")
    print("Timeline: when did it start? Any noises/smells? Recent filter "
          "change or work on the system?")


def log_event(symptom, verdict):
    if NO_LOG.get("disabled"):
        return
    try:
        data = []
        if os.path.exists(DEFAULT_LOG):
            with open(DEFAULT_LOG) as f:
                data = json.load(f)
        data.append({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
                     "symptom": symptom, "verdict": verdict})
        with open(DEFAULT_LOG, "w") as f:
            json.dump(data, f, indent=2)
        print(f"\nincident logged -> {DEFAULT_LOG} (use --no-log to disable)")
    except OSError:
        pass


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--symptom", default=None)
    ap.add_argument("--no-heat", action="store_true")
    ap.add_argument("--filter-clean", action="store_true")
    ap.add_argument("--pilot-lit", action="store_true")
    ap.add_argument("--brief", action="store_true")
    ap.add_argument("--freeze-risk", action="store_true")
    ap.add_argument("--skip-safety", action="store_true")
    ap.add_argument("--log", default=None, help="verdict string to log")
    ap.add_argument("--no-log", action="store_true",
                    help="never write the incident log file")
    args = ap.parse_args()
    NO_LOG["disabled"] = args.no_log

    if args.log:
        log_event(args.symptom or "unspecified", args.log)
        return 0

    if not args.skip_safety:
        stop = safety_triage()
        if stop:
            log_event("safety-stop", stop)
            return 1

    if args.freeze_risk:
        freeze_risk()
        return 0

    if args.symptom:
        key = symptom_lookup(args.symptom)
        if not key:
            print(f"[!] unknown symptom '{args.symptom}'. Known:")
            for k in SYMPTOMS:
                print("  -", k)
            return 2
        print_symptom(key)
        if args.brief:
            brief(None, key)
        return 0

    # non-interactive quick flags
    if args.no_heat:
        print("Quick path: no-heat with filter-clean and pilot-lit flags")
        if args.filter_clean and args.pilot_lit:
            print("Filter OK + pilot OK + no heat => likely igniter, flame "
                  "sensor, gas valve, or control board. PRO-CALL. "
                  "Estimated: $150-600.")
            if args.brief:
                brief([("filter", True), ("pilot", True)], "no heat")
            return 0

    print("Running interactive tree. Answer y/n; Enter = skip/unknown.\n")
    findings = tree_questions()
    bad = [c for c, ok in findings if ok is False]
    skipped = [c for c, ok in findings if ok is None]
    print("\n" + "=" * 64)
    print("VERDICT")
    print("=" * 64)
    if not bad:
        if skipped:
            print("No failures found but you skipped: " + ", ".join(skipped))
            print("Re-check those first; skipped items hide common causes.")
        else:
            print("All basics pass. Symptom persists => PRO-CALL with "
                  "detailed brief (rare causes: control board, limit "
                  "switch, duct issues).")
    else:
        print("Problems found: " + ", ".join(bad))
        for comp in bad:
            hint = {"thermostat": "thermostat batteries/wiring",
                    "power": "furnace switch + breaker",
                    "fan": "blower motor or its capacitor (PRO)",
                    "fuel": "gas valve / fuel supply",
                    "filter": "replace filter, then power-cycle switch 30s",
                    "ignition": "igniter/flame sensor (PRO usually)",
                    "burner": "combustion issue - PRO, flag CO concern",
                    "blower_start": "limit/fan switch or capacitor (PRO)",
                    "vent": "clear vent; if icy/snowed, also check intake"}
            print(f"  - {comp}: {hint.get(comp, 'see symptom table')}")
    if args.brief:
        brief(findings, None)
    log_event("interactive", "found: " + (", ".join(bad) if bad else "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
