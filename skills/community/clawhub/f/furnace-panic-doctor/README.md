# Furnace Panic Doctor

**The furnace dies at 2 AM in January. What you do in the next 10 minutes
decides between a $0 fix, a $350 fix, or a frozen house — and nobody
thinks clearly at 2 AM.**

## The problem

Every winter, millions of households hit "no heat" panic. The two failure
modes:

1. **Call emergency service immediately** → $150-400 premium for what was
   a dead thermostat battery, a flipped switch, or a $15 filter.
2. **Tough it out until morning** → sometimes that's a cracked heat
   exchanger or a blocked exhaust vent. That's not a comfort problem;
   that's carbon monoxide.

And even when a technician is the right call, homeowners show up to the
phone call with zero information: no symptom precision, no model number,
nothing checked. Longer diagnostics, bigger bills.

## The solution

A **10-minute, no-tools diagnostic tree**, run calmly from any phone or
laptop:

- **Safety triage first**: CO alarm, sulfur smell, soot, burning
  electrical → STOP-NOW scripts (what to shut off, whom to call, what not
  to touch)
- **The tree**: thermostat → power → fuel → ignition → airflow → one
  observed cycle, one question at a time, with word-pictures ("handle
  parallel to the pipe = OPEN")
- **Symptom table**: 25+ presentations → ranked causes with DIY/PRO flags
  and real cost bands — so you know a flame-sensor clean is $150-300 and
  a bang-on-ignition is an urgent pro call, not a curiosity
- **Freeze-risk math**: house heat-loss projection → whether emergency
  pricing is warranted, which faucets to drip, when to shut the water
  main instead of hoping
- **Technician briefing**: symptoms + what you checked + model plate
  location — printed and ready. Documented problems get fixed faster and
  billed less diagnostic time.

## Quick start

```bash
# the night it happens
python3 scripts/furnace_check.py

# jump to a symptom
python3 scripts/furnace_check.py --symptom "short cycling"

# already know some things?
python3 scripts/furnace_check.py --no-heat --filter-clean --pilot-lit

# should I pay emergency rates?
python3 scripts/furnace_check.py --freeze-risk
```

## What you get

```
SAFETY TRIAGE — answer before anything else
CARBON MONOXIDE ALARM? ... No safety stops. Continuing.
[THERMOSTAT] display alive? ... [FILTER] visibly gray? ...
  if not: Replace filter NOW (arrow toward blower)
VERDICT: Problems found: filter
  - filter: replace filter, then power-cycle switch 30s
```

## Who needs this

- Every homeowner or renter with a furnace/boiler (gas, oil, propane)
- Landlords fielding tenant panic calls at night
- First-winter homeowners who've never owned a furnace
- Anyone who wants to stop paying emergency premiums for battery swaps

## Honest scope

Decision support, not a substitute for a licensed technician. The skill
knows exactly where the DIY line is — and its most important feature is
recognizing when you've crossed into "this is dangerous, stop."

## Files

- `SKILL.md` — workflow, pitfalls, safety lines
- `scripts/furnace_check.py` — interactive tree + symptom lookup +
  freeze math + brief generator + incident log
- `references/diagnostic-tree.md` — full branch detail, cycle-timing table
- `references/symptom-table.md` — 25+ symptoms → causes → costs
- `references/manuals-and-codes.md` — model plates, blink codes, what to
  say on the phone, warranty notes

## License

MIT © Denis Voronin
