# Cohabitation Untangling — Theory & Practice

## The problem in numbers

Cohabiting relationships end constantly: in the US roughly half of marriages end in divorce and cohabiting unions dissolve at *higher* rates; most adults will experience at least one live-in relationship ending. Each dissolution carries:

- **20–200 shared physical items** worth splitting (furniture, appliances, kitchen gear, tools)
- **5–20 shared or entangled accounts** (streaming, utilities, phone family plan, cloud storage, insurance, bank)
- **A lease or mortgage** with joint liability that doesn't care about feelings
- **Months of accumulated shared expenses** that were never tracked because trust made tracking unnecessary

The failure mode isn't disagreement about the big things — it's the un-tracked long tail: the subscription that renews joint for another year, the utility bill in the wrong name, the "I paid for the sofa" vs "I paid the deposit" argument that can't be resolved because nobody wrote anything down at 2 AM.

## Why fairness mechanisms matter

Two provably fair mechanisms from fair-division theory:

### 1. Alternating draft (envy-free-ish)
Both parties alternately pick items they want, highest-value first. Neither can envy the other's bundle *too much*: each pick was available when they chose. The classic problem is first-pick advantage; solved by a coin flip (seeded for reproducibility) or "I cut, you choose" on the first item.

### 2. Buyout at depreciated equity
The item goes to its principal user, who pays the other half of **current value**, not purchase price. Depreciation model used by this skill:

```
current = price × max(0.15, (1 - 0.15 × years_old))     # 15%/yr straight-line, 15% floor
```

Categories with different curves (electronics fall faster, jewelry holds) can override via `--depreciation`.

### 3. Sell-and-split
When neither wants the other's stuff or the split is too contentious: sell everything sellable (marketplace listings), split proceeds by the contribution ratio (default 50/50, `--ratio` for unequal contributions).

## Account audit — the renewal trap

The most expensive breakups are the ones that keep costing money. Shared account audit flags:

- **KEEP-MINE** — account stays with one owner; other party's profile/payment removed
- **TRANSFER** — account moves to the other party (e.g., the plan admin changes)
- **CANCEL** — service ends on a date; calendar it
- **RENAME/REPLACE** — utilities at the shared address: name change or new account at a new address
- **DISPUTE** — contested (e.g., shared console library); park it explicitly so it's visible, not forgotten

Every account with a renewal date and no decided action inside the next 90 days appears in `accounts --due 90` until resolved. That list must be empty before the process is "done".

## Expense settle-up

Shared expenses recorded with payer and sharer. Balance:

```
balance(A→B) = Σ(paid_by_A, shared) / 2 − Σ(paid_by_B, shared) / 2     # for 50/50 shares
```

Custom share ratios supported (`--share 60/40`). The settle is ONE net payment — never a series of offsetting transfers, which invites re-litigation.

## Move-out logistics

Timeline depends on lease terms; typical notice periods:
- US month-to-month: 30 days in most states
- Germany: 3 months (statutory)
- UK assured shorthold: 1 month if periodic, per break clause if fixed
- Deposit return: demand letter after move-out inspection; itemized deductions only

The `moveout` command back-computes from the move date: notice deadline, utility shutoff/transfer dates, mail forwarding start, key return event, deposit demand date.

## Legal-adjacent notes (not legal advice)

- **Property acquired during cohabitation** is generally governed by title/receipt, not by community-property presumptions (except in a handful of jurisdictions and for registered partnerships). Keep receipts; `item add --payer` records them.
- **Joint leases** bind both signers until lease end or signed release — moving out does not end liability. Landlord may pursue either party for full rent.
- **Joint bank accounts**: either owner can typically withdraw 100%; the courteous protocol is freeze-to-new-deposits, settle, then close jointly.
- For married couples, property division is statutory — this tool organizes, courts decide.

## Sensitive-data posture

Everything is stored locally in one JSON file. No network access. The data in an untangling file — who keeps the dog's vet records, who owes whom — is weaponizable in disputes; treat the file like a diary, and archive it (or delete it) when the process completes.
