# canning-safety-ranger

**Botulism-gate screening for home canning.** Classifies foods acid/borderline/low-acid,
enforces the right method (water-bath + acid vs pressure), corrects process times and
pressures for altitude, screens recipes against the seven classic violations, and
triages suspect jars into eat/refrigerate/discard verdicts.

## The real-world problem

Home canning is surging (garden boom, food prices, homestead culture) and it's the one
kitchen activity where an error is lethal rather than unpleasant. *Clostridium botulinum*
spores survive boiling water, multiply in airless low-acid jars, and produce one of the
most toxic substances known. The poison is **odorless and invisible** — you cannot smell,
see, or taste it.

The deadly mistakes are all seductive folklore:
- "Grandma water-bathed green beans for 40 years" (survivorship bias)
- "Tomatoes are acidic, right?" (modern varieties sit at pH 4.6+, the exact cutoff)
- "I'm at 6,000 ft, recipe says 10 min" (boiling point drops ~1°F per 500 ft)
- Pinterest salsa with improvised veggie ratios (onions/peppers raise pH)
- Pumpkin butter, pesto, cake-in-a-jar (no safe home process exists)

## What it does

| Capability | Detail |
|---|---|
| Food classification | acid / borderline (tomatoes) / low-acid / NEVER — with the pH logic stated |
| Method enforcement | water-bath + acidification vs pressure-can, by class |
| Altitude engine | USDA water-bath time ladder (+5 min/1,000 ft); dial & weighted pressure ladders |
| Recipe screen | the 7 violations: low-acid in water bath, unacidified tomatoes, untested mixed recipes, thickeners, open-kettle, paraffin, dairy |
| Jar triage | bulging/unsealed/mold/fizz/smell → EAT / REPROCESS / DISCARD with reasoning + discard protocol |
| Tomato acid math | bottled lemon juice / citric acid per jar size, in-jar before filling |

## Quick start

```bash
python3 scripts/canning_ranger.py --demo
python3 scripts/canning_ranger.py --screen --food "green beans" --method water-bath --altitude 5000
python3 scripts/canning_ranger.py --screen --food "tomato sauce" --method water-bath
python3 scripts/canning_ranger.py --time pints water-bath 35 5000
python3 scripts/canning_ranger.py --pressure quarts 11 6500 weighted
python3 scripts/canning_ranger.py --jar bulging-lid low-acid
```

Stdlib only.

## Example

```
$ --screen --food "green beans" --method water-bath --altitude 5000
verdict:      UNSAFE-AS-PLANNED
violations:   RULE 1: low-acid food + water-bath = botulism risk
corrections:  Pressure-can only (dial 13 psi at 5,000 ft...)
              Altitude 5,000 ft: dial 13 psi or weighted 15 lb
```

Grandma's book says 30 minutes in boiling water at 5,000 ft — the screen flags it,
names the violated rule, and gives the corrected process: pints 20 min at 13 psi.

## Why it matters

Roughly 1 in 5 US botulism cases trace to home-canned food, and nearly all follow one
of the seven violations this skill screens. Canning is otherwise cheap, rewarding food
preservation — this makes the safety layer explicit instead of inherited folklore.
