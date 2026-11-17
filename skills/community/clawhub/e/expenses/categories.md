# Categories — A Taxonomy That Survives a Year

The category system lives in `## Categories` and `## Vendor Rules` in `~/Clawic/data/expenses/memory.md`, or in `~/Clawic/data/expenses/categories.md` once `## Boxes` says it moved. **Read it before assigning any category** — the value of a taxonomy is entirely in its consistency, and an agent that re-decides each time destroys it faster than a user ever could.

**Contents:** [Derive, Do Not Design](#derive-do-not-design) · [The Three Axes](#the-three-axes) · [The Decision Test](#the-decision-test) · [A Starting Skeleton](#a-starting-skeleton) · [Splits That Earn Their Place](#splits-that-earn-their-place) · [Vendor Rules](#vendor-rules) · [Changing the Taxonomy](#changing-the-taxonomy) · [Overlays: Deductible, Fixed, Private](#overlays-deductible-fixed-private)

## Derive, Do Not Design

A category system designed before there are entries is a guess about someone's life, and it is wrong in the specific way that matters: it has categories with nothing in them and lacks the one that turns out to hold a fifth of the spend.

Two weeks of flat logging first — vendor and amount, category `other` or the obvious word. Then read the list and let the categories fall out of what is actually there. This costs nothing: recategorizing 60 entries with vendor rules is a single pass, while un-designing a system a user has emotionally committed to is not.

## The Three Axes

The single most common taxonomy failure is collapsing three independent questions into one field:

| Axis | Field | Question it answers | Cardinality |
|---|---|---|---|
| What was bought | `Category` | Where does the money go? | 8-15, stable for years |
| Why / what it belongs to | `Tags` | This trip, this project, this client, this claim | Unbounded, mostly short-lived |
| How it was paid | `Method` | Which account, which statement | One per account |

`japan-2026` is a tag, not a category — it dies in three weeks and would ruin every year-over-year comparison it touched. `groceries` is a category. `amex` is a method. Anything that will not exist in two years is a tag.

## The Decision Test

A category deserves to exist when **its own number could change a behavior**. Not "is it interesting" — interesting is what tags are for.

- `food` at 620 → could change a behavior only if it separates the part that is discretionary. So `groceries` and `eating-out` earn their split.
- `coffee` at 38 → a real number that changes nothing, unless the user has said coffee is the thing they are watching. Then it earns the split, for them.
- `bank fees` at 190/year → changes a behavior immediately (switch account). Earns it.
- `home` split into `furniture`, `decor`, `tools` → three numbers, no decision. One category, tags if needed.

**Ceiling: 8-15 categories.** A list that does not fit in the user's head gets applied inconsistently, and inconsistency is worse than coarseness — a coarse total is true, an inconsistent one is not.

**The `other` test**: `other` above ~5% of monthly spend means the taxonomy is missing something real. Read what is in `other` and the missing category is usually obvious. Below 5%, leave it alone; forcing every stray purchase into a named home is the other way to break a taxonomy.

## A Starting Skeleton

Not a default to impose — a checklist for the derivation pass, so nothing structural gets missed.

`housing` (rent/mortgage, community fees) · `utilities` (power, water, internet, phone) · `groceries` · `eating-out` · `transport` (fuel, transit, taxis, parking) · `health` · `shopping` · `entertainment` · `subscriptions` · `travel` · `fees` · `gifts` · `other`

Business overlay when the user has one: `work-travel` · `work-tools` · `work-services` · `work-marketing`, or the tax authority's own headings if the user files against them — matching the filing categories saves a full reclassification every year.

## Splits That Earn Their Place

The handful of divisions that reliably produce decisions, in the order they usually pay off:

1. **`groceries` vs `eating-out`.** The largest genuinely controllable gap in most personal ledgers, and the one people misestimate most.
2. **Fixed vs variable** — not a split, an attribute (below). A budget cut is only actionable against the variable half.
3. **`fees` out of everything else.** FX, ATM, overdraft, late payment, annual card fees. Small per line, embarrassing per year, entirely removable.
4. **`subscriptions` out of `entertainment` and `work-tools`.** Recurring spend behaves differently from decisions; the inventory belongs in the shared `~/Clawic/data/finances/subscriptions.md` and the ledger keeps the cash.
5. **`transport` split into commute vs discretionary** only when the user is deciding about a car.
6. **Per-person categories in a household** — resist. That is the beneficiaries field (`sharing.md`), not a category.

## Vendor Rules

A vendor rule is the whole reason a taxonomy stays consistent. Written once, applied forever, stored in `## Vendor Rules`.

- **Match order**: exact vendor string → substring → amount band → ask once, then write the rule. Never ask twice about the same vendor.
- **Ambiguous multi-category vendors** — a general marketplace, a supermarket that sells electronics, a fuel station that sells food. Two workable rules: an amount band (`> 60 → shopping, else groceries`) or a default plus a correction habit. Pick the amount band; it is right more often than a coin flip and it never asks.
- **A rule change is retroactive** for the current month only, by default. Older months are only rewritten by the full recategorization procedure below.
- Rules are written from the vendor string **as it appears on the statement**, not as the user says it, because that is the string the import will present (`reconciliation.md`).

## Changing the Taxonomy

Renaming, merging or splitting a category applies **across the whole history in the same turn, or it does not happen** (SKILL.md Rule 7). A taxonomy change applied "from now on" silently invalidates every comparison that crosses the boundary, and nothing will ever flag it again.

Procedure:

1. Count the affected ledger months. If the rewrite is more than the session can carry, do not start it — say so and propose the smaller change.
2. Rewrite every affected `ledger/<YYYY-MM>.md` row.
3. Update `## Categories`, and any `## Vendor Rules` that referenced the old name.
4. Recompute `Top categories` for every affected row in `## Monthly Totals`.
5. Note the change and its date in `## How They Work` — the next comparison that looks strange has its explanation.

**Merging** keeps the survivor's name and never invents a third. **Splitting** an existing category retroactively requires a rule that can classify old rows (vendor, amount, tag); if no such rule exists, the split starts from today and every report crossing the boundary says so.

## Overlays: Deductible, Fixed, Private

Three attributes, each a column or a tag, none of them a category:

- **Fixed / variable.** Housing, utilities and subscriptions are fixed; groceries and eating-out are variable. Only the variable half responds to a decision this month, which is why "cut 10%" against a total is meaningless advice.
- **Deductible.** A business overlay on the same categories, mapped to the filing headings once and kept in that map. Deductibility is a property of the purpose, not the category — the same restaurant row is deductible or not depending on who was at the table (`business.md`).
- **Private.** Categories listed in `private_categories` are excluded from any shared, exported or household report and fold into `other` there (`reports.md`). The ledger keeps them intact; only the reporting layer hides them.

**Write on the way out.** A new category, a rename, a merge or a vendor decision goes into `## Categories` / `## Vendor Rules` in `memory.md` — or `categories.md` if it has been split out — in the same turn, together with every ledger row the change touched. A recategorization pass also refreshes `Top categories` in `## Monthly Totals`. Formats in `memory-template.md`.
