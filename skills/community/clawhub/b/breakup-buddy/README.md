# Breakup Buddy — Cohabitation Untangler

**Two lives untangled, itemized, settled, and closed.**

When a live-in relationship ends, the emotional work gets all the attention —
but the *logistical* work is what ruins the next three months: who keeps the
sofa bought together, the Netflix account still joint, the car insurance that
auto-renews in two weeks, the gas bill in the wrong name at an address nobody
lives at anymore.

This is a structured untangling system, 100% local (one JSON file):

- **Shared catalog** — every shared item with price, purchase date, payer,
  principal user, sentimental flag
- **Three fair-split engines** — alternating draft (seeded coin flip for first
  pick), buyout at *depreciated* equity (15%/yr straight-line, 15% floor —
  not list price), or sell-and-split with custom ratios
- **Sentimental quarantine** — flagged items are excluded from automation;
  they resolve only by explicit agreement
- **Account audit with the renewal trap closed** — every shared account gets
  KEEP-MINE / TRANSFER / CANCEL / RENAME / DISPUTE; `account list --due 90`
  flags anything renewing inside 90 days with no decision until the list is
  empty
- **One-payment settle-up** — shared expenses recorded with payer and share
  ratio (50/50, 60/40...) collapse to a single net payment: "B pays A $385 —
  one payment, then this chapter is closed"
- **Dated move-out plan** — notice deadline back-computed from move date,
  utilities shutoff/transfer, meter photos, key return with receipt, mail
  forwarding, deposit demand letter timeline
- **Status report** — bundle equity per party, pending account actions, net
  settle, and a blocker count that must reach zero

## Quick start

```bash
python3 scripts/untangle.py item add "Sofa" --price 1200 --date 2024-03-15 \
    --payer both --user A --sentimental no
python3 scripts/untangle.py split draft --seed 42
python3 scripts/untangle.py account add "Netflix" --type subscription \
    --renews 2026-11-01 --owner both --action-flag transfer
python3 scripts/untangle.py expense add "October rent" 950 --payer A --shared-with B
python3 scripts/untangle.py expense settle
python3 scripts/untangle.py moveout --move-date 2026-11-15 --notice-days 30
python3 scripts/untangle.py report
```

## Who it's for

Anyone ending a cohabiting relationship — romantic or roommate. Roughly half
of marriages end in divorce and cohabiting unions dissolve at higher rates;
each one carries 20–200 shared items and 5–20 entangled accounts. Fair
division mechanics (draft, buyout, sell-and-split) come from fair-division
theory; the renewal-trap audit exists because the most expensive breakups are
the ones that keep costing money silently.

Informational organizer, not legal advice. Treat `untangle.json` like a
diary — archive or delete when the process completes.

MIT © 2026 Denis Voronin
