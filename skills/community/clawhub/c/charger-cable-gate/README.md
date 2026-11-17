# Charger & Cable Gate — USB-C PD Compatibility

**Why is the laptop charging slowly? The weakest of charger × cable × device caps everything — silently.**

You plugged a 100W brick into your performance laptop and it's still
losing battery. The culprit chain: PD negotiation (5/9/15/20/28/36/48V
steps), the cable's current cap (3A = 60W wall without an e-marker),
charge-only cables that can't negotiate at all, and proprietary
protocols (VOOC/SCP) that ignore standard PD. This tool checks the
whole triple and names the bottleneck with an actionable verdict.

## What it does

- **check** — device × charger × cable verdict: negotiated watts,
  device needs, and one of OK / CAPPED / SLOW / NO-CHARGE plus the
  specific warning (3A cable wall, charge-only trap, proprietary
  protocol miss, EPR cable requirement)
- **table** — the full rule ladder: PD voltage steps, cable classes,
  device and charger archetype catalogs
- **watt** — decode any wattage into V×A operating points + device
  class meaning ("65W = ultrabook single-port standard")

## The problem in numbers

- A 3A cable caps a 100W setup to **60W** — the #1 hidden cause of
  "slow charging" complaints
- Charge-only cables negotiate nothing: **5V forever**
- Proprietary-fast phones (VOOC/SCP) deliver ~27W on standard PD
  regardless of the brick's 65W+ rating
- EPR 140-240W requires BOTH a PD 3.1 charger and a 50V-rated cable

## Quick start

```bash
python3 scripts/pd_compatibility_checker.py check \
    --device phone-flagship --charger 65w-pd --cable 3a-charge-only
```

```
Negotiated power : 0 W
VERDICT          : NO-CHARGE
WARNING: charge-only cable: no data lines -> PD negotiation IMPOSSIBLE...
```

```bash
python3 scripts/pd_compatibility_checker.py check \
    --device laptop-performance --charger 100w-pd --cable 3a-standard
# -> CAPPED at 60W of 100W: buy an e-marked 5A cable
```

## Install

No dependencies. Python 3.8+.

## License

MIT © Denis Voronin
