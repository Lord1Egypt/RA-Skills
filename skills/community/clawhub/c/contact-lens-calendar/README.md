# Contact Lens Calendar

**The problem:** 40–60% of contact lens wearers stretch their lenses past the replacement date — the single biggest behavioral risk factor for microbial keratitis, a corneal infection that can scar vision. The failure is structural: the wear clock starts **when the foil is peeled**, not when the box was bought, and almost nobody writes that date down. The expiry printed on the carton is sterile shelf life and tells you nothing.

**What this does:** a zero-dependency Python tool that turns "I opened this pair around the 28th" into an exact maintenance calendar:

- **`due`** — replacement verdicts for every open lens: `day 24 of 30 — 6 days left, replace by 2026-10-27`, with ⚠ OVERDUE flags and days-past
- **`plan`** — what a lens opened on any date becomes across all five wear classes (daily/biweekly/monthly/quarterly/yearly)
- **`inventory`** — days of wear sitting in unopened boxes, so stock-ups are sized, not guessed
- **`cost`** — per-day and per-annualized cost per modality (settles the dailies-vs-monthlies debate with numbers, including the occasional-wearer inversion where dailies actually win)
- **`log`** — persists open events to `contacts.json`; left/right tracked separately because eyes on different open days have different due dates

Data lives in a local JSON store. No accounts, no cloud, no phone app asking for notification permissions.

## Quick start

```bash
python3 scripts/contact_lens.py log --kind monthly --opened 2026-09-28 --eye left
python3 scripts/contact_lens.py due
# [left] monthly opened 2026-09-28: day 24 of 30 — 6 day(s) left, replace by 2026-10-27
```

## Who needs this

~45 million contact lens wearers in the US alone, worldwide far more; every one of them runs an open-date clock in their head, and most run it wrong. Anyone who has ever thought "I'll get one more week out of this pair" is the target user.

## Safety boundary

This is a calendar, not a diagnostician. `references/wear-life.md` documents the red-flag symptoms (pain, photophobia, vision change, white spot on the cornea) that mean *stop and call an eye care professional same-day*, plus case hygiene — the untracked half of lens safety, since cases are biofilm reservoirs that re-inoculate "clean" lenses.

## License

MIT
