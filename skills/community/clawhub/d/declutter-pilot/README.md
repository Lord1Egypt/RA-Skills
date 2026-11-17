# Declutter Pilot

**Decluttering fails from decision fatigue, not laziness. This does the physics first and the feelings second.**

## The problem

Every cleanup attempt stalls the same way: 20 minutes in, the micro-decisions
("might need it", "was expensive", "was a gift") exhaust you, and the
half-sorted pile survives — now worse, because it's been touched and
abandoned.

Meanwhile the kept-stuff has a real price: a cluttered home typically stores
thousands of dollars of never-used items at ~$180/m³/year in space value, and
every move charges by the volume.

## What it does

| Command | What you get |
|---|---|
| `item add` | Registry with volume (liters) and decision-difficulty (1 easy … 5 heirloom) |
| `plan` | Greedy sortie order — most liters freed per unit of emotional labor, packed into 20-min sessions |
| `sortie start/done` | Runs the session: named zone, container count, exit condition, progress % |
| `bags` | Liters → trash bags / boxes / car-loads / m² reclaimed / $/yr storage freed |
| `decide` | The five decision tests + cost-of-keeping math for one hard item |
| `manifest` | Sell/donate/recycle/trash batches, donation values, disposal run checklist |

## Quick start

```bash
python3 scripts/declutter.py item add "Broken desk chair" --room office --volume 80 --difficulty 1 --decision toss
python3 scripts/declutter.py item add "University textbooks" --room office --volume 45 --difficulty 3 --decision sell --value 60
python3 scripts/declutter.py plan
python3 scripts/declutter.py sortie start
python3 scripts/declutter.py sortie done --bags 3
python3 scripts/declutter.py manifest
```

100% local, one JSON file.

## The strategy in one line

Sorties ranked by **volume ÷ difficulty** — the first bag out is 80% of the
psychological battle, so the plan makes sure it's full of easy, bulky wins,
and the sentiment box waits until momentum exists.

## Honest limits

Built for clutter, not hoarding disorder (clinical situation → professional
support; this can structure consented sessions alongside, never instead).
MIT License. © 2026 Denis Voronin
