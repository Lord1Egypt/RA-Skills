# coffee-brew-lab

A dial-in instrument for manual coffee: SCA golden-ratio recipe math for six
brewing methods, a taste-defect → parameter-move diagnosis tree, and a brew
log that correlates your scores against grind/temperature/dwell/ratio to find
your actual sweet spot.

## The real-world problem

Home brewers waste bags of coffee guessing. The dial-in process has settled
science behind it (18–22% extraction, strength vs extraction as two
independent axes, one-variable-at-a-time experimentation), but almost nobody
applies it because the arithmetic and bookkeeping are tedious. Result: years
of "sometimes good, sometimes sour" coffee. This skill runs the math, tells
you exactly which single lever to move when a cup tastes wrong, and keeps
the log your palate can't.

## Quick start

```bash
cd scripts
# recipe math for any method
python3 brew_lab.py recipe --method v60 --cups 2
python3 brew_lab.py recipe --method french-press --grams 30
python3 brew_lab.py recipe --method cold-brew --liters 1
python3 brew_lab.py recipe --method aeropress --cups 1 --altitude 1800

# when a cup tastes wrong
python3 brew_lab.py diagnose bitter
python3 brew_lab.py diagnose sour
python3 brew_lab.py diagnose sour-and-bitter

# keep a log, then learn from it
python3 brew_lab.py log add --method v60 --grams 15 --water 240 --grind 4.5 \
  --temp 93 --dwell 180 --score 6 --tags bitter
python3 brew_lab.py log add --method v60 --grams 15 --water 240 --grind 5.5 \
  --temp 93 --dwell 180 --score 8 --tags balanced
python3 brew_lab.py log best
python3 brew_lab.py log analyze
```

Python 3.9+, stdlib only. Log: `brew_log.json` next to the script.

## What you get

- **recipe** — grams coffee/water at your ratio, grind size, temperature
  window (altitude-corrected — water boils ~1°C lower per 300m), dwell times,
  and a numbered method procedure including bloom/pour schedules.
- **diagnose** — maps a taste word to its axis (extraction vs strength vs
  unevenness vs staleness) and prescribes ONE move, in order of usual
  effectiveness. Bitter → coarser; sour → finer; weak-but-not-sour → ratio,
  not grind; sour-AND-bitter → channeling, stop chasing temperature.
- **log** — every brew recorded with settings + score + defect tags;
  `log analyze` runs per-variable Pearson correlation and tells you which
  lever your best cups moved, and which variable you've kept constant so
  long it's uninformative.

## The one rule

Change **one variable per cup** and log both cups. Everything else in this
skill is machinery for making that rule cheap to follow.

## License

MIT © Denis Voronin
