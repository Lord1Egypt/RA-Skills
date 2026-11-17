# Time-of-Use Rates Playbook

## What TOU is
Your utility prices electricity by time of day, mirroring wholesale costs:
solar flood midday, demand peaks in the evening, the grid idles overnight.
Typical US residential TOU structure:

| Window | Name | Typical price |
|---|---|---|
| 23:00-07:00 (or 00:00-06:00) | off-peak / super off-peak | $0.09-0.15/kWh |
| 07:00-15:00 | mid-peak (varies) | $0.15-0.25/kWh |
| 15:00/16:00-21:00/22:00 | on-peak | $0.25-0.55/kWh |

Spreads of 2-3× between off-peak and peak are common. An EV averaging
300 kWh/month of home charging saves $25-50/month by charging only in the
off-peak window — $300-600/year for a 15-minute enrollment call.

## Enrollment checklist
1. Find your utility's rate plan page; search "[utility] time of use EV rate".
2. Compare: your CURRENT flat rate vs the TOU off-peak rate AND on-peak
   rate. TOU only wins if your whole-house load (not just the car) fits the
   windows — running AC 15:00-21:00 on a $0.40 peak rate can eat the car's
   savings. Rules of thumb:
   - If you charge overnight and keep AC/evening use normal, TOU wins for
     anyone driving 600+ miles/month electric.
   - If someone is home all day running AC on peak, model the whole house
     first (compare your hourly usage from the utility's usage tool).
3. Some utilities require/separately meter the EV (a second meter or a
   submetering device on the EVSE circuit — then house stays flat-rate and
   the car gets the cheap rate; often the best of both).
4. Ask for the "EV rate" specifically — some utilities hide it behind a
   separate enrollment from generic TOU.

## Whole-house discipline after enrolling
TOU punishes laziness as much as it rewards overnight charging:
- Dishwasher/clothes dryer/oven: schedule or run before 15:00 or after 21:00.
- The compare tool only models the car; do a mental pass on the house:
  moving 200 kWh/month of laundry/dishwashing from peak to off-peak saves
  another $20-40/month in peaky markets.

## When flat-rate beats TOU
- You drive little (<300 mi/month electric) — savings can't cover the plan
  difference if the flat rate is unusually good.
- Your household CANNOT move evening usage (medical equipment, work-from-
  home cooling loads in a hot climate on a brutal peak rate).
- The TOU plan carries a higher fixed monthly charge than flat — do the
  arithmetic: savings must exceed the fee delta.

## Scheduling the car (the practice)
1. In the car (or EVSE app), set: off-peak window = utility window,
   target = 80% daily / departure time + buffer 30 min.
2. The car starts/stops itself — you never think about it again.
3. Re-check twice a year: utilities occasionally shift window boundaries,
   and season flips (summer/winter schedules differ for some utilities).
4. After a big-charge night (road trip recovery), re-run the `tou` planner —
   recovery fills don't always fit one window.

## Public charging reality check
- Level 2 public ( destination chargers): $0.20-0.35/kWh — comparable to
  an expensive flat-rate home; fine for topping up.
- DC fast: $0.40-0.60/kWh + sometimes per-minute fees. At 3.4 mi/kWh that's
  $0.13-0.18/mile — MORE than a 30-mpg car at $4.10 gas ($0.137/mile).
- The `--public-pct` flag in `compare` exists so the honest number includes
  the road-trip and apartment-street-parking reality.

## Reading your bill after 2 months
1. Pull the utility's hourly usage chart.
2. Confirm the charging block sits inside the off-peak window (a mis-set
   car schedule is the #1 "TOU didn't save me anything" cause).
3. Confirm peak usage dropped (or that you accept the peak price knowingly).
4. Compute actual $/mile: bill EV line-item ÷ miles driven. Under $0.05/mi
   means the setup is working; over $0.10 means something's off-plan.
