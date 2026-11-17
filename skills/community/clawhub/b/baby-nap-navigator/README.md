# Baby Nap Navigator

**Skill:** `baby-nap-navigator` · v1.0.0 · MIT · [ClawHub](https://clawhub.com) `@voronindenis5/baby-nap-navigator`

## The real-world problem

Every new parent hits the same wall. The baby woke at 6:50. When is the next nap? Guess late and you get the cortisol second-wind — a wired, screaming infant who *cannot* fall asleep despite being exhausted. Guess early and you're rocking a wide-awake baby for 40 minutes. Multiply by 4–6 naps a day for the first year and this single timing question dominates the household's mood, the parents' sleep, and every caregiver handoff.

The answer exists — **wake windows**, the age-banded awake-time ranges pediatric sleep practice has used for decades — but parents meet it as folklore scattered across forum posts and conflicting app subscriptions, not as a computable schedule they own.

## What it does

A 3AM-usable timing instrument, offline, stdlib-only Python, state in a JSON file you keep:

- **`now`** — last wake-up + baby's age → the current window ("08:50–09:35, ideal 09:12") plus the drowsy cues to watch for
- **`projections`** — the rest of the day simulated: every nap start/length, the bedtime window, and an ⚠ OVERTIRED RISK flag with the "pull bedtime earlier, not later" correction when a day runs long
- **`drift`** — linear regression on nap start times; detects the slow morning-nap creep that signals a 3→2 or 2→1 transition weeks before the meltdown phase
- **`report`** — 7-day summary for pediatrician visits and caregiver handoffs
- Every printed plan ends with the AAP safe-sleep footer

## Who needs this

- **New and expecting parents** (~130M births/year worldwide) for whom nap timing is a daily, high-stakes guessing game
- **Grandparents and nannies** covering shifts — a printed projection replaces the 20-minute verbal briefing
- **Daycare-transition planners** checking whether the facility's 12:30 nap fits the child's current pattern
- Anyone who wants the data instead of the folklore — no cloud, no account, no subscription

## Example

```bash
python3 scripts/nap_navigator.py log --age-weeks 22 --wake 06:50
python3 scripts/nap_navigator.py projections
# nap 1: 09:12-10:19 (window 08:50-09:35)
# nap 2: 12:41-13:48
# nap 3: 16:10-17:17
# BEDTIME 19:30  <- OVERTIRED RISK: pull previous nap shorter / bedtime earlier
```

## Scope & safety

A timing instrument, not a sleep-training method and not medical advice. It never recommends crying-it-out, and it prints an explicit red-flag list (snoring, breathing pauses, pain wakes) that routes straight to a pediatrician.

## License

MIT © Denis Voronin
