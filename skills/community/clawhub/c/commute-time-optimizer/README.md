# Commute Time Optimizer

**What your commute really costs — in hours of your life, dollars, and waking days per decade — and how to shrink it with better housing, mode, and hybrid-schedule choices.**

The average US worker spends ~230 hours a year commuting — six work-weeks — yet "10 extra minutes each way" sounds trivial when you sign a lease. It isn't: it's 83 hours/year and ~52 waking days per decade. This tool prices every option (car, transit, bike, walk, WFH) in time AND money, so housing and job-tradeoff decisions finally compare apples to apples.

## The real-world problem

- **Housing decisions systematically misprice commute time** because it's paid in small daily installments. People agonize over $100/month rent and sleepwalk into +40 minutes/day.
- **Hybrid workers pick office days by habit** (Mon/Wed/Fri), not by traffic. Mid-week congestion peaks Tue–Thu, and Friday's PM peak is the lightest — the optimizer makes the penalty visible.
- **"Is moving closer worth it?" has no intuitive answer** until you annualize time at your wage + vehicle cost + rent gap over your realistic tenure. This computes the exact breakeven rent.
- **Mode comparisons ignore reliability and full vehicle cost.** AAA/IRS-style per-mile numbers ($0.47/mi loaded, $0.24 marginal) and transit pass-switch logic are built in.

## What it does

```bash
# What my current commute costs
python3 scripts/commute_opt.py cost --offpeak 25 --distance 15 --mode car --rate 35

# Car vs transit vs bike vs walk vs WFH for my route
python3 scripts/commute_opt.py compare --offpeak 25 --distance 8

# Which 3 office days minimize traffic?
python3 scripts/commute_opt.py hybrid --offpeak 30 --mode car --office-days 3

# Apartment vs house-with-longer-commute, 5-year horizon
python3 scripts/commute_opt.py decide \
  --option "Apt A,offpeak=25,distance=12,mode=car,extra_rent=0" \
  --option "House B,offpeak=42,distance=26,mode=car,extra_rent=-450" \
  --rate 40 --years 5
```

Every command accepts `--json` for piping into other tools.

## How it works

Weekday rush multipliers (Mon 1.28 … Fri 1.22, editable) scale your observed off-peak time; costs use AAA/IRS-style vehicle per-mile rates, transit fare with automatic monthly-pass switching, and time valued at your after-tax hourly rate. The hybrid optimizer brute-ranks all C(5,N) weekday subsets. Full assumptions, sources, and a sanity table: `references/commute-model.md`.

## Who needs this

- **Renters/buyers comparing homes** across neighborhoods with different commutes
- **Job switchers** weighing pay raise vs. longer commute
- **Hybrid/remote workers** choosing office days and renegotiating them with data
- **Anyone pricing a return-to-office mandate** — what 3 days/week in traffic actually costs per year

## Install

Python 3.8+ standard library only.

```bash
python3 scripts/commute_opt.py params     # see/edit all assumptions
python3 scripts/test_commute_opt.py       # verify the build
```

## License

MIT © Denis Voronin
