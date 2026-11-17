# Estate Settlement Navigator

**Ten organizations each want an ORIGINAL certified death certificate —
and the family ordered three. Meanwhile the $255 lump sum, the widow's
benefit at 60, and the group-life claim all have claim windows nobody in
grief is tracking.**

The death of a family member starts an administrative cascade that runs
for a year on zero sleep. The order you notify organizations in decides
whether money gets clawed back; the credit bureaus decide whether the
deceased's identity gets used for loans for the next decade; the
retirement-account decision (spousal rollover vs inherited IRA) is
irreversible. This skill is the checklist executor brain for the worst
week: certificate math, the notification cascade with the WHY for every
slot, survivor-benefit screening with the claim-small-first switch
strategy, a dated settlement timeline through the final tax returns, and
the notification letters banks require.

## What it does

- **`certificates`** — count organizations → certified-copy order size +
  cost; the reorder-is-expensive math that says order high at the funeral
  home.
- **`cascade`** — ordered US/UK notification plan: SSA before banks
  (clawback), bureaus before collectors, employer windows first; UK gets
  Tell Us Once + the 3-month Bereavement Support Payment trap.
- **`benefits`** — SSA survivor screen from ages (widow(er) 60/50 gates,
  75%-of-PIA child benefits, family maximum), $255 two-year window, and
  the take-the-smaller-check-first switch strategy between two records.
- **`timeline`** — dated milestones from date of death through probate
  decision, titles, estate 1041, the final 1040, and estate-tax-only-
  above-$14M reality.
- **`letter`** — generates close/claim/transfer letters with the
  authority statement and enclosure list institutions act on.

## Quick start

```bash
python3 scripts/estate_admin.py certificates --orgs 14
python3 scripts/estate_admin.py cascade --country us
python3 scripts/estate_admin.py benefits --spouse-age 61 --kids-under16 1
python3 scripts/estate_admin.py timeline --date 2026-10-14
python3 scripts/estate_admin.py letter --type claim --to "Acme Life" \
    --deceased "John M. Doe" --dod 2026-10-14 --requester "Mary Doe, beneficiary"
```

Stdlib only, offline, no accounts. General administrative information,
not legal or tax advice — for contested estates or big ones, bring an
estate attorney and a CPA.

MIT © Denis Voronin
