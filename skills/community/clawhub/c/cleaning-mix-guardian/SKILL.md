---
name: cleaning-mix-guardian
description: Use before mixing ANY household cleaning products — checks combinations for dangerous reactions (bleach+ammonia→chloramine gas, bleach+acid→chlorine gas, hydrogen peroxide+vinegar→peracetic acid, two different drain cleaners→heat/pressure), explains symptoms and first aid for each gas, gives safe alternates and safe sequences (wait times between products), and a poison-center quick card by region.
version: 1.0.1
author: Denis Voronin
license: MIT
tags: [household-safety, cleaning, bleach, chlorine-gas, chloramine, poison-prevention, home]
---

# Cleaning Mix Guardian

## Overview

Mixing common household cleaners sends thousands of people to emergency
rooms every year. The chemistry is well known — bleach + ammonia releases
chloramine gas, bleach + acid releases chlorine gas — but the products
don't say "contains ammonia" on the front, and people mix them while
cleaning toilets, showers, and drains without knowing.

This skill is a **pre-mix safety checker**:

1. **Reaction lookup** — a curated database of product-ingredient
   combinations and what they produce (gas, heat, pressure), with
   severity, symptoms, and first aid.
2. **Product decoding** — maps common product names/types ("toilet bowl
   cleaner", "glass cleaner", "dishwasher tabs", "rust remover") to their
   reactive ingredient class.
3. **Safe sequencing** — when two products must be used in the same
   space, the required rinse/wait interval and ventilation.
4. **Incident card** — if a mix already happened: what gas it probably
   was, symptoms to expect, first aid, and when to call poison control.

**This is first-aid-level information, not a substitute for poison
control or emergency services.** When in doubt: call. US 1-800-222-1222,
UK 111, EU 112.

## When to Use

- "Can I mix X and Y?" for ANY two cleaners — always check first
- Deep-cleaning a bathroom: sequencing toilet cleaner, bleach, limescale
  remover safely
- Drain unblocking: choosing ONE drain cleaner, never a second different
  one after the first
- Someone already mixed something / smells sharp/gassy: incident mode
- Building a shopping list: which products can coexist in one cupboard

**Don't use for:** industrial chemicals, pool chemistry dosing (different
concentrations — see pool-chemistry skills), pesticide mixing. Never use
it to *design* a mix — it exists to prevent them.

## Quick Start

```bash
# Can I mix bleach and ammonia-based glass cleaner?
python3 scripts/mix_guard.py check --a bleach --b "glass cleaner"

# Check by ingredient class
python3 scripts/mix_guard.py check --a bleach --b acid

# What's actually in common products (reactive classes)
python3 scripts/mix_guard.py products

# Safe order to use several products in one bathroom
python3 scripts/mix_guard.py sequence --items "toilet cleaner,bleach,limescale remover"

# Something already happened
python3 scripts/mix_guard.py incident --a bleach --b "drain cleaner"
```

## The Chemistry That Hurts People

| Mix | Releases | Severity |
|---|---|---|
| Bleach (NaOCl) + ammonia | Chloramine gas (NH₂Cl) | CRITICAL |
| Bleach + acid (HCl, vinegar, citric) | Chlorine gas (Cl₂) | CRITICAL |
| Hydrogen peroxide + vinegar | Peracetic acid | HIGH |
| Bleach + hydrogen peroxide | Oxygen gas + heat | HIGH (pressure in closed containers) |
| Bleach + alcohol (isopropyl) | Chloroform-like compounds (in practice, chlorinated ethers/aldehydes) | HIGH |
| Two different drain cleaners (acid + caustic) | Heat, boiling spray, pressure | CRITICAL |
| Caustic (NaOH) + acid (HCl) | Violent heat, spattering | HIGH |
| Bleach + "rust remover" (oxalic/hydrofluoric types) | Chlorine gas + HF risk | CRITICAL |

Symptoms progress: throat irritation → coughing → chest tightness →
difficulty breathing. Chlorine is heavier than air and pools low — pets
and children are affected first.

### Why "I'll just rinse it down" fails

Chlorine/chloramine release starts the moment the products contact —
in the toilet bowl, on the scrub brush, in the sponge. By the time you
smell it (pool smell = chloramines; sharp green smell = chlorine), the
exposure has happened. Prevention is the only reliable control.

## Common Pitfalls

1. **"Bleach + dish soap is fine."** Usually true for plain detergent —
   but many dish soaps and almost all glass cleaners contain ammonia
   derivatives. Check the label for "ammonia", "quats" plus acid, or
   amines.
2. **Toilet-bowl cleaner then bleach.** Bowl cleaners are usually ~9 %
   HCl. Bleach after an acid bowl cleaner without a FULL rinse + flush =
   chlorine gas in your face. This is the single most common injury path.
3. **"The drain is still clogged, I'll add a different cleaner."** NEVER
   add a different chemistry to a drain that still contains the first —
   acid-after-caustic boils out of the drain. Mechanical clearing (plunger,
   drain snake) has no chemistry.
4. **Mixing in a closed spray bottle "to make it stronger."** Closed
   containers turn gas release into pressure explosions. Also: never put
   bleach into anything that had another product in it.
5. **Vinegar as a "safe natural" cleaner.** Vinegar is a real acid: it
   etches stone, corrodes grout and rubber seals, and it reacts with
   bleach and hydrogen peroxide. Natural ≠ inert.

## Verification Checklist

- [ ] check prints CRITICAL/HIGH verdict with gas name, symptoms, first aid
- [ ] products lists the reactive class of every catalog entry
- [ ] sequence outputs an order with wait/rinse steps between risky pairs
- [ ] incident mode prints the poison-control card and evacuation advice
- [ ] unknown product names produce a "treat as incompatible" warning

## Examples

```
$ python3 scripts/mix_guard.py check --a bleach --b "glass cleaner"
✗ DO NOT MIX — CRITICAL
  Bleach (sodium hypochlorite) + ammonia-based glass cleaner
  → CHLORAMINE GAS (NH2Cl)
  Symptoms: throat/eye irritation, coughing, chest pain, breathing
  difficulty. Low-lying gas — affects pets and children first.
  First aid: leave the room NOW, ventilate from outside if possible,
  fresh air 30+ min, seek medical care if breathing is affected.
  Poison control (US): 1-800-222-1222
```

Data compiled from poison-control guidance (US AAPCC, UK NHS) and
standard inorganic chemistry of hypochlorite reactions. When exposure has
already happened: fresh air first, poison control second, 112/911 if
breathing is impaired.
