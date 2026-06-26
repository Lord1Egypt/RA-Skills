#!/usr/bin/env python3
"""Generate a GaggiMate Pro profile JSON from bean parameters.

Based on Lance Hedrick's methodology:
- Pressure is a red herring — balance > 9 bar
- Ratio is the #1 extraction lever
- Coarser > finer for even extraction
- Temperature: lower than you think

Usage:
  generate-profile.py --label "Ethiopian Yirgacheffe" \
    --roast light --origin ethiopia --process washed \
    --dose 18 --ratio 2.5 --temp 90 \
    [--strategy bloom] [--style espresso] [--freshness fresh] \
    [--output profile.json]

Parameters:
  --label      Profile label (bean name)
  --roast      light, medium-light, medium, medium-dark, dark
  --origin     ethiopia, colombia, brazil, kenya, sumatra, guatemala, costarica, blend, other
  --process    washed, natural, honey, anaerobic, co-ferment, unknown
  --dose       Dose in grams (0=auto)
  --ratio      Brew ratio (0=auto based on Lance's guidelines)
  --temp       Brew temp °C (0=auto)
  --strategy   auto, flat, declining, bloom, lever, turbo, low-contact
  --style      espresso, ristretto, lungo, milk, allonge
  --freshness  fresh (<4 weeks), rested (4-8 weeks), aged (>8 weeks)
  --output     Output file (default: stdout)
"""

import argparse
import json
import sys
import uuid

# ============================================================
# Lance Hedrick's methodology encoded as selection logic
# ============================================================


def auto_select_strategy(roast: str, process: str, origin: str, freshness: str) -> str:
    """Pick strategy per Lance Hedrick's approach."""
    # Heavily processed → gentle extraction, don't push
    if process in ("anaerobic", "co-ferment"):
        return "turbo"  # Coarser, lower pressure, preserve process flavors

    # Aged coffee → fast, low pressure, accept CO2 loss
    if freshness == "aged":
        return "turbo"

    # Ultra light / Nordic → turbo (Lance's preferred for light)
    if roast == "light":
        if process == "washed":
            return "bloom"  # Bloom for washed lights — degas then extract
        return "turbo"  # Natural lights — fast, gentle

    # Medium-light → lever or bloom depending on origin
    if roast == "medium-light":
        if origin in ("ethiopia", "kenya", "costarica"):
            return "bloom"
        return "lever"

    # Medium → classic lever (natural pressure decline)
    if roast == "medium":
        return "lever"

    # Dark → declining (Lance: traditional Italian, sustained 9 bar then decline)
    if roast in ("medium-dark", "dark"):
        return "declining"

    return "lever"


def auto_select_temp(roast: str, process: str, freshness: str) -> float:
    """Temperature per Lance: lower than you think. Default 90°C baseline."""
    # Heavily processed → lower to preserve process flavors
    if process in ("anaerobic", "co-ferment"):
        if roast in ("light", "medium-light"):
            return 88
        return 86

    # Aged → lower
    if freshness == "aged":
        return 88

    temps = {
        "light": 92,  # Lance: 90-93, rarely above 94
        "medium-light": 91,  # Sweet spot
        "medium": 90,  # Lance's default baseline
        "medium-dark": 88,  # Sub-90 for darker
        "dark": 86,  # Well sub-90
    }
    return temps.get(roast, 90)


def auto_select_ratio(roast: str, process: str, style: str, freshness: str) -> float:
    """Ratio per Lance: yield is #1 extraction lever."""
    # Style overrides
    if style == "ristretto":
        return 1.5
    if style == "lungo":
        return 3.0
    if style == "allonge":
        return 3.5
    if style == "milk":
        # Slightly higher ratio for milk drinks — needs punch
        base = _base_ratio(roast, process, freshness)
        return min(base + 0.3, 3.5)

    return _base_ratio(roast, process, freshness)


def _base_ratio(roast: str, process: str, freshness: str) -> float:
    """Lance's ratio rules by roast."""
    # Heavily processed → don't push
    if process in ("anaerobic", "co-ferment"):
        return 2.0

    # Aged → moderate, don't over-extract
    if freshness == "aged":
        if roast in ("light", "medium-light"):
            return 2.5
        return 2.0

    ratios = {
        "light": 2.8,  # Lance: 2.5-3.0 for light
        "medium-light": 2.5,  # Lance: 2.0-2.5
        "medium": 2.2,  # Lance: 2.0-2.5
        "medium-dark": 1.8,  # Lance: 1.8-2.0
        "dark": 1.7,  # Lance: 1.5-2.0 max
    }
    return ratios.get(roast, 2.0)


def auto_select_dose(roast: str, process: str) -> int:
    """Basket recommendation."""
    if roast in ("light", "medium-light"):
        return 20  # More surface area for harder-to-extract beans
    if process in ("anaerobic", "co-ferment"):
        return 18  # Less dose for volatile processed coffees
    return 18


def build_profile(
    label: str,
    roast: str,
    origin: str,
    process: str,
    dose: int,
    ratio: float,
    temp: float,
    strategy: str,
    style: str,
    freshness: str,
) -> dict:
    """Build a GaggiMate Pro profile dict."""
    target_weight = round(dose * ratio, 1)

    desc_parts = [
        f"{roast.title()} roast",
        origin.title() if origin != "other" else "",
        process if process != "unknown" else "",
        f"{dose}g→{target_weight}g (1:{ratio})",
        f"{strategy} profile",
    ]
    description = ", ".join([p for p in desc_parts if p])

    profile = {
        "id": str(uuid.uuid4()),
        "label": label,
        "type": "pro",
        "description": description,
        "temperature": temp,
        "phases": [],
    }

    builders = {
        "bloom": _bloom_phases,
        "declining": _declining_phases,
        "lever": _lever_phases,
        "turbo": _turbo_phases,
        "flat": _flat_phases,
        "low-contact": _low_contact_phases,
    }
    builder = builders.get(strategy, _lever_phases)
    profile["phases"] = builder(dose, target_weight, temp, roast, process)

    return profile


def _phase(
    name: str,
    phase_type: str,
    valve: int,
    duration: int,
    pump: dict,
    transition: dict | None = None,
    targets: list[dict] | None = None,
    temperature: int = 0,
) -> dict:
    """Build a phase dict."""
    p = {
        "name": name,
        "phase": phase_type,
        "valve": valve,
        "duration": duration,
        "temperature": temperature,
        "pump": pump,
    }
    p["transition"] = transition or {"type": "instant", "duration": 0, "adaptive": 1}
    if targets:
        p["targets"] = targets
    return p


# ============================================================
# Profile strategies — informed by Lance's videos
# ============================================================


def _bloom_phases(dose: int, target_weight: float, temp: float, roast: str, process: str) -> list[dict]:
    """Blooming espresso: fill → bloom (no pump) → gentle ramp → brew.
    Lance's preferred for washed light/medium-light.
    Builds 6-7 bar, extended pre-infusion to degas CO2."""
    peak_pressure = 7 if roast in ("light", "medium-light") else 8
    return [
        _phase("Fill", "preinfusion", 1, 4, {"target": "flow", "pressure": 2, "flow": 4}),
        _phase("Bloom", "preinfusion", 1, 8, {"target": "flow", "pressure": 0, "flow": 0}),
        _phase(
            "Ramp",
            "brew",
            1,
            5,
            {"target": "pressure", "pressure": peak_pressure, "flow": 4},
            transition={"type": "ease-in", "duration": 4, "adaptive": 1},
            targets=[{"type": "pressure", "operator": "gte", "value": peak_pressure - 0.5}],
        ),
        _phase(
            "Brew",
            "brew",
            1,
            35,
            {"target": "pressure", "pressure": peak_pressure, "flow": 4},
            targets=[{"type": "volumetric", "operator": "gte", "value": target_weight}],
        ),
    ]


def _turbo_phases(dose: int, target_weight: float, temp: float, roast: str, process: str) -> list[dict]:
    """Turbo shot: coarser grind, high flow, low pressure, fast extraction.
    Lance's go-to for ultra lights, processed coffees, and aged beans.
    15-20s total, 2-6 bar, maximum extraction evenness."""
    # Higher flow for light, slightly lower for processed
    flow_rate = 5.0 if process not in ("anaerobic", "co-ferment") else 4.0
    pressure_limit = 6 if roast in ("light", "medium-light") else 7
    return [
        _phase("Fill", "preinfusion", 1, 3, {"target": "flow", "pressure": 3, "flow": flow_rate}),
        _phase(
            "Turbo Brew",
            "brew",
            1,
            25,
            {"target": "flow", "pressure": pressure_limit, "flow": flow_rate},
            targets=[{"type": "volumetric", "operator": "gte", "value": target_weight}],
        ),
    ]


def _lever_phases(dose: int, target_weight: float, temp: float, roast: str, process: str) -> list[dict]:
    """Lever-style: fill → PI → fast ramp to peak → natural decline.
    Lance's preferred for medium roasts. Mimics spring lever machines.
    Natural declining pressure gives thick, syrupy body."""
    peak = 9 if roast not in ("light", "medium-light") else 8
    return [
        _phase("Fill", "preinfusion", 1, 4, {"target": "flow", "pressure": 2, "flow": 5}),
        _phase("Pre-infuse", "preinfusion", 1, 4, {"target": "flow", "pressure": 2, "flow": 2}),
        _phase(
            "Ramp",
            "brew",
            1,
            3,
            {"target": "pressure", "pressure": peak, "flow": 4},
            transition={"type": "ease-in", "duration": 2, "adaptive": 1},
            targets=[{"type": "pressure", "operator": "gte", "value": peak}],
        ),
        _phase("Hold Peak", "brew", 1, 6, {"target": "pressure", "pressure": peak, "flow": 4}),
        _phase(
            "Decline",
            "brew",
            1,
            30,
            {"target": "flow", "pressure": peak, "flow": -1},
            transition={"type": "ease-out", "duration": 8, "adaptive": 1},
            targets=[{"type": "volumetric", "operator": "gte", "value": target_weight}],
        ),
    ]


def _declining_phases(dose: int, target_weight: float, temp: float, roast: str, process: str) -> list[dict]:
    """Declining pressure: ramp to 9 bar → hold → controlled decline to 5-6 bar.
    For medium-dark and dark roasts. Traditional Italian-influenced.
    Lance: sustained 9 bar for body, then decline to reduce late-shot bitterness."""
    return [
        _phase("Fill", "preinfusion", 1, 3, {"target": "flow", "pressure": 3, "flow": 4}),
        _phase("Pre-infuse", "preinfusion", 1, 4, {"target": "pressure", "pressure": 3, "flow": 3}),
        _phase(
            "Ramp",
            "brew",
            1,
            3,
            {"target": "pressure", "pressure": 9, "flow": 4},
            transition={"type": "linear", "duration": 2, "adaptive": 1},
            targets=[{"type": "pressure", "operator": "gte", "value": 9}],
        ),
        _phase("Hold 9 bar", "brew", 1, 8, {"target": "pressure", "pressure": 9, "flow": 4}),
        _phase(
            "Decline",
            "brew",
            1,
            25,
            {"target": "pressure", "pressure": 5.5, "flow": 4},
            transition={"type": "linear", "duration": 10, "adaptive": 1},
            targets=[{"type": "volumetric", "operator": "gte", "value": target_weight}],
        ),
    ]


def _flat_phases(dose: int, target_weight: float, temp: float, roast: str, process: str) -> list[dict]:
    """Classic flat 9 bar. Simple, predictable.
    Good starting point when unsure."""
    return [
        _phase("Fill", "preinfusion", 1, 3, {"target": "flow", "pressure": 3, "flow": 5}),
        _phase("Pre-infuse", "preinfusion", 1, 5, {"target": "pressure", "pressure": 3, "flow": 3}),
        _phase(
            "Ramp",
            "brew",
            1,
            3,
            {"target": "pressure", "pressure": 9, "flow": 0},
            transition={"type": "linear", "duration": 2, "adaptive": 1},
            targets=[{"type": "pressure", "operator": "gte", "value": 9}],
        ),
        _phase(
            "Brew 9 bar",
            "brew",
            1,
            35,
            {"target": "pressure", "pressure": 9, "flow": 4},
            targets=[{"type": "volumetric", "operator": "gte", "value": target_weight}],
        ),
    ]


def _low_contact_phases(dose: int, target_weight: float, temp: float, roast: str, process: str) -> list[dict]:
    """Low contact / allongé: very fast, very low pressure.
    For ultra light geisha-type coffees.
    Lance: 1:3.5 ratio, ~20s, 1-3 bar, "like drinking hot juice"."""
    return [
        _phase("Fill", "preinfusion", 1, 3, {"target": "flow", "pressure": 2, "flow": 6}),
        _phase(
            "Low Contact Brew",
            "brew",
            1,
            30,
            {"target": "flow", "pressure": 4, "flow": 5},
            targets=[{"type": "volumetric", "operator": "gte", "value": target_weight}],
        ),
    ]


def main():
    parser = argparse.ArgumentParser(description="Generate GaggiMate Pro profile (Lance Hedrick methodology)")
    parser.add_argument("--label", required=True)
    parser.add_argument("--roast", required=True, choices=["light", "medium-light", "medium", "medium-dark", "dark"])
    parser.add_argument("--origin", default="other")
    parser.add_argument(
        "--process", default="washed", choices=["washed", "natural", "honey", "anaerobic", "co-ferment", "unknown"]
    )
    parser.add_argument("--dose", type=int, default=0)
    parser.add_argument("--ratio", type=float, default=0)
    parser.add_argument("--temp", type=float, default=0)
    parser.add_argument(
        "--strategy", default="auto", choices=["auto", "flat", "declining", "bloom", "lever", "turbo", "low-contact"]
    )
    parser.add_argument("--style", default="espresso", choices=["espresso", "ristretto", "lungo", "milk", "allonge"])
    parser.add_argument("--freshness", default="fresh", choices=["fresh", "rested", "aged"])
    parser.add_argument("--output", default="-")

    args = parser.parse_args()

    # Auto-fill defaults using Lance's methodology
    if args.dose == 0:
        args.dose = auto_select_dose(args.roast, args.process)
    if args.ratio == 0:
        args.ratio = auto_select_ratio(args.roast, args.process, args.style, args.freshness)
    if args.temp == 0:
        args.temp = auto_select_temp(args.roast, args.process, args.freshness)
    if args.strategy == "auto":
        args.strategy = auto_select_strategy(args.roast, args.process, args.origin, args.freshness)

    # Style-driven overrides
    if args.style == "allonge" and args.strategy == "auto":
        args.strategy = "low-contact"

    profile = build_profile(
        label=args.label,
        roast=args.roast,
        origin=args.origin,
        process=args.process,
        dose=args.dose,
        ratio=args.ratio,
        temp=args.temp,
        strategy=args.strategy,
        style=args.style,
        freshness=args.freshness,
    )

    output = json.dumps(profile, indent=2)

    if args.output == "-":
        print(output)
    else:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Profile saved to {args.output}", file=sys.stderr)
        print(f"  Label: {profile['label']}", file=sys.stderr)
        print(f"  Strategy: {args.strategy} | Style: {args.style}", file=sys.stderr)
        print(f"  Temp: {args.temp}°C | Dose: {args.dose}g | Ratio: 1:{args.ratio}", file=sys.stderr)
        print(f"  Target: {round(args.dose * args.ratio, 1)}g out", file=sys.stderr)
        print(f"  Freshness: {args.freshness}", file=sys.stderr)
        print(f"  Phases: {len(profile['phases'])}", file=sys.stderr)


if __name__ == "__main__":
    main()
