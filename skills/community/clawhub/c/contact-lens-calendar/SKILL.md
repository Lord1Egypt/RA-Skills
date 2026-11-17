---
name: contact-lens-calendar
description: Use when tracking open contact lenses, deciding replacement dates, planning a lens stock-up, or comparing daily vs monthly lens cost — computes exact do-not-exceed replacement dates from the day the foil was peeled, flags overdue lenses, counts days of wear left in unopened boxes, and prices each wear modality per day and per year.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [contact-lenses, vision, health-tracking, replacement-schedule, eye-care, supplies]
---

# Contact Lens Calendar

The most common contact lens error is not the fit — it's the calendar.
Study after study (CDC, contact lens hygiene surveys) finds 40–60% of lens
wearers stretch their lenses past the replacement date, which is the single
biggest behavioral risk factor for microbial keratitis. The reason is
structural: **the wear clock starts when the foil is peeled, not when the
box was bought**, and almost nobody writes that date down. The carton's
expiry date is sterile shelf life and tells you nothing about wear.

This skill turns the one date you actually know — "I opened this pair
around the 28th" — into a maintenance calendar with no ambiguity:
exact replace-by dates per lens class, overdue flags, a stockpile
countdown, and honest per-day cost math for the dailies-vs-monthlies
debate.

## When to Use

- "When do I replace my lenses?" — any lens type, from the open date
- Tracking multiple open lenses at once (left/right on different
  schedules, or transitioning between pairs)
- Planning a stock-up: how many months of wear is in the drawer?
- Deciding between daily, biweekly, and monthly modalities with real
  cost-per-day math instead of sticker shock
- After a lens-related red eye: reconstructing whether the lens in use
  was overdue (useful history for the optometrist)

**Don't use for:** medical advice about eye pain, redness, or vision
changes — those are same-day optometrist/ER questions. This is a
calendar, not a diagnostician.

## How It Works

1. **Wear life by class** — daily = 1 day, biweekly = 14, monthly = 30,
   quarterly = 90, yearly = 365. These are the FDA-cleared wear periods
   for disposable lens classes; they are NOT extended by "I only wore
   them a few hours" — the clock runs from opening.
2. **Replace-by = open date + life − 1** — day 1 is the day you open it.
   A monthly opened Sept 28 is due Oct 27, not Oct 28.
3. **Overdue is overdue** — there is no grace period. The script flags
   any lens past its window with days-overdue so the habit stays honest.
4. **Inventory math** — unopened boxes × lenses per box ÷ 2 eyes × wear
   days = days of supply on hand.
5. **Cost truth** — per-lens price ÷ wear days = cost per day. Dailies
   lose their scary reputation once annualized against solution costs
   for monthlies.

## Commands

```bash
# What a lens opened today becomes, per class
python3 scripts/contact_lens.py plan --opened 2026-10-10

# Track lenses (persists to contacts.json)
python3 scripts/contact_lens.py log --kind monthly --opened 2026-09-28 --eye left
python3 scripts/contact_lens.py log --kind biweekly --opened 2026-10-05 --eye right

# Verdicts as of any date (default: today)
python3 scripts/contact_lens.py due --on 2026-10-21

# Stockpile: days of wear in unopened boxes
python3 scripts/contact_lens.py log --kind monthly --boxes 3 --lenses-per-box 6 --opened 2026-10-21
python3 scripts/contact_lens.py inventory

# Dailies vs monthlies, annualized
python3 scripts/contact_lens.py cost
```

## Reference Table — Wear Life by Lens Class

| Class | Wear life | Replace-by for lens opened Oct 10 |
|---|---|---|
| Daily | 1 day | same day |
| Biweekly | 14 days | Oct 23 |
| Monthly | 30 days | Nov 8 |
| Quarterly | 90 days | Jan 7 |
| Yearly (conventional) | 365 days | Oct 9 next year |

## Common Pitfalls

1. **Trusting the carton expiry.** That's sterile shelf life of an
   UNOPENED lens. Once opened, the carton date is irrelevant.
2. **"I don't wear them every day, so the monthly lasts longer."** For
   most lens materials the clock runs from opening regardless of daily
   use (check your brand's IFU; some daily-disposable-only brands market
   "day of use" counting — the script assumes calendar-day counting,
   the safe default).
3. **Replacing both eyes on different days.** If you open left and right
   on different days, their due dates differ — track them separately
   (`--eye left/right`) or you'll silently stretch one.
4. **Ignoring the case.** Cases need replacement every 1–3 months —
   lens calendar apps never track this; put it on the same cadence as
   your monthly pair.
5. **Solution topping-off.** Not a calendar issue but the #1 companion
   sin: recharge solution in the case instead of replacing it and the
   disinfection cycle is compromised even with fresh lenses.

## Verification Checklist

- [ ] Every open lens is logged with kind + open date + eye
- [ ] `due` shows no OVERDUE lines (or the lens is in the trash)
- [ ] Replace-by dates set as phone reminders 1 day early
- [ ] Inventory checked before reordering (avoid duplicate stock-ups)
- [ ] Case replacement tied to a monthly lens change

## References

- `references/wear-life.md` — wear classes, CDC hygiene findings, why
  the clock starts at opening, red-flag symptoms that bypass this tool.
