# Sharing — Splitting Costs and Settling Without an Argument

Group state lives in `## Shared Balances` in `~/Clawic/data/expenses/memory.md`, one `### <group>` block per group, or in `~/Clawic/data/expenses/groups/<group>.md` once `## Boxes` says a group moved out. **Read the group's block before splitting anything** — the split rule and the current balances are both in it, and a split done without the rule is a split that gets relitigated.

**Contents:** [Two Facts Per Expense](#two-facts-per-expense) · [Split Methods](#split-methods) · [Rounding](#rounding) · [The Balance Invariant](#the-balance-invariant) · [Settling: Net First, Then Minimize](#settling-net-first-then-minimize) · [Households and Couples](#households-and-couples) · [Group Trips](#group-trips) · [Membership Changes](#membership-changes) · [When Someone Does Not Pay](#when-someone-does-not-pay) · [Non-Money Contributions](#non-money-contributions)

## Two Facts Per Expense

Who paid the money out, and who the money was spent on. A tracker that stores one field for both can produce a household total and nothing else — and the household total is never the question anyone asks. The question is always "what do I owe".

The ledger row keeps the **full amount** and lists the beneficiaries. The user's own share is derived, never stored as a second row: two rows for one expense is how a group total ends up double-counted.

## Split Methods

| Method | Formula | Use when |
|---|---|---|
| Equal | `total ÷ n` | Default (`default_split`), and correct for most one-off shared purchases |
| Shares / weights | `total × wᵢ ÷ Σw` | Rent by room, a couple counted as two, a child counted as a half |
| Exact amounts | Stated per person | Itemized restaurant bills where one person had the wine |
| Percentage | `total × pᵢ`, `Σp = 1` | Standing arrangements someone already negotiated |
| By income | `total × incomeᵢ ÷ Σincome` | Standing rule where incomes differ materially — see below |
| By consumption | `total × unitsᵢ ÷ Σunits` | Utilities by occupancy-days, fuel by kilometres |
| Payer only | Beneficiary = payer | Someone's personal purchase inside a shared shop; the escape hatch that keeps the group honest |

**Rent by room size** is the one worth doing properly, because it is the largest recurring number in most shared flats: split the **common area equally** and the **private area proportionally**, rather than pro-rating the whole rent by bedroom square metres. A 1,200 flat with 40 m² common and private rooms of 16/12/8 m²: common 400 each, private `800 × 16/36 = 355.56`, `800 × 12/36 = 266.67`, `800 × 8/36 = 177.78`. Fix the numbers at move-in and write them into the group rule; renegotiating them mid-tenancy is a different conversation from tracking money.

**By income** starts mattering when the highest and lowest incomes differ by more than roughly a factor of two; below that the fairness gain is smaller than the friction of maintaining income data that people do not enjoy sharing. If it is used, it is a standing rule written into the group block once, not a per-expense negotiation — and incomes are stored as **weights**, not as amounts, so the block does not become a salary disclosure.

## Rounding

Shares that do not sum to the total are how balances drift to numbers nobody can explain.

- Compute shares to two decimals, then give the **remainder cents to the payer**. `10.00 ÷ 3 → 3.34 / 3.33 / 3.33`, payer takes the 3.34.
- Verify the sum equals the total exactly before writing. This check costs one line and prevents the class of bug where a group of five never reaches zero.
- Do not round to whole units unless the user asked for it — that request is a declaration and gets written to `config.yaml` as `split_policy.settlement_rounding: whole` (default `none`, two decimals); rounding 4.60 to 5 across a hundred entries is a real transfer of money.

## The Balance Invariant

After every shared entry and every settlement: **the net balances of the group sum to zero.** Positive means owed, negative means owes, and the block says so in a `Meaning` column because half of all users read the sign backwards.

If the sum is not zero, one split is wrong. Find it before adding another entry — the error compounds and the group loses trust in the whole ledger, not just the row. The usual causes: a beneficiary list that omitted the payer, a rounding remainder that went nowhere, or an expense entered twice by two people.

## Settling: Net First, Then Minimize

Settling per expense means one transfer per expense. Nobody does that, so balances silently accumulate instead. Settle on `settle_cadence` and do it in two steps.

**Step 1 — net.** Collapse everything to one number per person.

**Step 2 — minimize.** Any group of n people can be settled in **at most n−1 transfers**. Greedy pairing gets there: repeatedly match the largest debtor with the largest creditor and transfer the smaller of the two magnitudes.

Worked example — A +120, B +30, C −60, D −90 (sums to zero):

1. Largest debtor D (−90) with largest creditor A (+120): **D → A 90**. A now +30.
2. Largest debtor C (−60) with largest creditor A (+30): **C → A 30**. A settled.
3. C (−30) with B (+30): **C → B 30**. All zero.

Three transfers for four people. The round-robin alternative — everyone paying everyone what they owe them per expense — is up to `n × (n−1)` transfers, which is why group trips end with someone still owed money in March.

Write the settlement into the group block with its date and the transfers. If the group wants a record, produce a settlement statement in `artifacts/` — period, entry count, total, the transfers, and the confirmation that balances are zero afterwards. That artifact is what a disputed settlement gets resolved with.

**Fronting.** When one person pays for everything, their balance grows and so does their risk. If a single person's positive balance exceeds roughly one settlement period's worth of group spend, say so once and suggest rotating who fronts. This is a mechanical observation, not a judgement about anyone.

## Households and Couples

Three models, each with a specific failure mode:

| Model | How it works | Fails when |
|---|---|---|
| Everything shared | One pot, no per-person tracking | Incomes or spending habits diverge; there is no way to discuss it without discussing everything |
| Proportional | Shared costs split by income weights | The weights go stale after a raise or a job change and nobody updates them |
| Yours / mine / ours | Fixed contribution to a shared pot, the rest independent | **"Ours" was never defined.** Is a joint holiday ours? A haircut before a joint event? |

Yours/mine/ours is the most robust of the three and the most commonly broken, always for the same reason. Write the list of what counts as shared into the group rule at the start — categories, not examples — and every ambiguous purchase gets decided once against the list instead of negotiated live.

Household utilities where one person travels: split by **occupancy-days**, `total × daysᵢ ÷ Σdays`. It takes one number per person per month and removes the most frequent recurring flat argument.

## Group Trips

- **One payer per category** — one person books accommodation, one handles transport, one covers group meals. This flattens the ledger and makes the settlement small, and it distributes the fronting.
- **Settle once, at the end**, not nightly. Nightly settling is n transfers a day for a week.
- **Multi-currency**: convert **each entry at its own rate date** (`currency.md`). A single trip-average rate silently moves money between whoever paid early and whoever paid late — the person who paid on the strong day subsidizes the rest.
- **Different itineraries**: beneficiaries are the people who were actually there. The three who skipped the boat trip are not beneficiaries of it, and the group block must reflect that or the settlement is wrong in a way everyone can feel.
- Post-trip, produce the summary in the trip's envelope file and the settlement in `artifacts/` (`travel.md`).

## Membership Changes

Someone joining or leaving mid-period invalidates every open split unless the balances are frozen first.

1. Settle or at minimum **snapshot** the current balances with a dated line in the group block.
2. Change the membership, with the effective date.
3. New entries use the new membership. Old entries are never re-split.

A person who leaves keeps their `contacts.md` row — they may still owe money, and deleting the person deletes the only record of who the balance belongs to. Only their line in the group block goes, with its date.

## When Someone Does Not Pay

The tool here is a factual statement, never advocacy: the period, the entries they benefited from, the amounts with currencies, the net, the transfer requested. Produce it as an `artifacts/` settlement statement so the numbers exist outside a chat.

If the balance is written off, book it: a negative row against the debtor's balance and a matching entry in the user's own ledger under a `bad-debt` or `gifts` category. An "informally forgiven" balance that stays in the block poisons every future settlement of that group.

## Non-Money Contributions

Driving, hosting, cooking, lending equipment. These are the single largest source of unspoken group resentment, and they are outside a money ledger by default.

Two valid treatments, and the failure is choosing neither: **price it** (fuel and tolls at a stated rate become a real entry; the host's flat is worth a stated nightly amount) or **exclude it explicitly** in the group rule ("driving and hosting are not tracked"). Write which one the group chose. A group that has not decided will discover it has two opinions at settlement time.

**Write on the way out.** Every shared entry updates the ledger row's beneficiaries **and** the `### <group>` block in the same turn, with the invariant checked; a first-time participant gets their row in `~/Clawic/data/contacts/contacts.md`; a settlement writes its dated line in the group block, resets the balances, updates `## Due` for the next one under `settle_cadence`, and puts any statement produced in `artifacts/` with its `## Boxes` line; a standing split rule the user states is a declaration and goes to `config.yaml` under `split_policy`. Formats in `memory-template.md`.
