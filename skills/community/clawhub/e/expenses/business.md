# Business Expenses — Deductibility, Apportionment and Rebilling

**Before deciding whether anything is deductible**, read `config.yaml` for `tax_year_start` and `platform.jurisdiction`, and any apportionment basis the `## Boxes` index lists in `artifacts/` — a basis that was derived once and written down is the difference between a defensible claim and an argument.

Every rule here is jurisdiction-shaped. This file gives the tests and the mechanics; the numbers, percentages and thresholds must be confirmed for the user's country and year before being stated as fact. Anything in the Red Flags table below suspends that and routes to a professional.

**Contents:** [The Test](#the-test) · [The Evidence Chain](#the-evidence-chain) · [Mixed Use and Apportionment](#mixed-use-and-apportionment) · [Home Office](#home-office) · [Capital vs Expense](#capital-vs-expense) · [Meals, Entertainment and Gifts](#meals-entertainment-and-gifts) · [VAT and Input Tax](#vat-and-input-tax) · [Personal Card, Company Money](#personal-card-company-money) · [Rebilling a Client](#rebilling-a-client) · [Red Flags](#red-flags)

## The Test

Two famous phrasings of one question. The US test is **ordinary and necessary** for the trade or business; the UK test is **wholly and exclusively** for the purposes of the trade. They differ in a way that matters — the UK formulation is stricter about dual purpose — but the practical question an agent should ask is the same:

> Would this cost exist if the business did not?

- Clearly yes → deductible, subject to the category rules below.
- Clearly no → personal, and forcing it through is the failure that gets an entire return examined rather than one line.
- Both → it is a mixed-use cost, and mixed-use costs are apportioned with a stated basis, not estimated with a round percentage.

The single most-challenged pattern is the round number with no basis behind it: "50% of the phone", "£10 a week for use of home". Some jurisdictions publish flat rates that are safe precisely because they are official — use the official flat rate or a real basis, never a self-invented percentage.

## The Evidence Chain

Three links, and any claim missing one is weak:

| Link | Source | Fails when |
|---|---|---|
| The money moved | Bank or card statement | Cash with no receipt |
| What it was for | The ledger row's **purpose** field, written at payment | Reconstructed at filing time |
| What was bought, from whom | Receipt or tax invoice (`receipts.md`) | Card slip only, in a VAT jurisdiction |

Amounts are the link nobody loses and nobody challenges. **Purpose** is the link that is both easy to lose and the one actually examined. That asymmetry is the whole reason SKILL.md Rule 8 exists.

## Mixed Use and Apportionment

Store the **basis**, not the percentage. The percentage is an output; the basis is the answer to the question that gets asked.

| Cost | Defensible basis |
|---|---|
| Home office | Floor area used exclusively for work ÷ total floor area, sometimes × time if the room is shared use |
| Vehicle | Business kilometres ÷ total kilometres, from a log or odometer readings |
| Phone and internet | A representative usage period — an itemized month, or a documented split of hours |
| A trip | Business days ÷ total days (`reimbursement.md`) |
| A laptop used for both | Time-based estimate, documented once, revisited only when the pattern changes |

Write the basis to `artifacts/` the first time it is derived — the floor plan measurement, the four-week usage log, the odometer readings — with the date and when it should be revisited. Deriving it costs an afternoon; nobody should pay that twice, and re-deriving it differently next year is itself a red flag.

Revisit on a **change of circumstances** (moved house, changed car, changed working pattern), not annually for its own sake. A basis that shifts every year without a cause looks like a number being tuned.

## Home Office

Two routes almost everywhere:

- **Simplified / flat rate** — a published amount per month or per hour worked from home. Smaller, and effectively unchallengeable. Correct for most people.
- **Actual costs apportioned** — rent or mortgage interest, power, heating, internet, council/property charges × the area basis. Larger, and requires the measurements plus the bills for the whole period.

The exclusivity trap: some jurisdictions require the space to be used **exclusively** for business, and a room used for work by day and as a spare bedroom fails that test outright. Others allow time-and-space apportionment. Verify which regime applies before choosing the route.

Owner-occupiers claiming mortgage interest or a share of the property should check the capital-gains consequence of claiming exclusive business use of part of a home. This is a route-to-professional item, not an agent decision.

## Capital vs Expense

An item with a useful life beyond the current year is generally **capitalized and depreciated**, not expensed in full — unless it falls under a de minimis or immediate-expensing rule, which most jurisdictions now have in some form.

- Do not quote a threshold from memory. Say that a de minimis threshold exists and needs checking for the year and jurisdiction.
- **Repair vs improvement** is the same distinction wearing different clothes: restoring an asset to working order is an expense, improving it beyond its previous state is capital.
- Splitting one purchase into parts to slip under a threshold is a recognized avoidance pattern and is treated as such.
- In the ledger, capitalized items get a `#capital` tag and stay out of the deductible expense totals; the depreciation schedule is the accountant's, not this skill's.

## Meals, Entertainment and Gifts

The most-changed rules in the whole subject, and the ones most often quoted from a stale memory.

- **Client entertainment** is fully non-deductible in some jurisdictions, partially deductible in others; the treatment has changed repeatedly in the last decade in several countries.
- **Business meals** are commonly deductible at a reduced percentage, and that percentage has moved more than once. Never state a figure without checking the current year.
- **Staff events** often have their own separate allowance with a per-head annual cap.
- **Gifts** typically have a low per-recipient annual cap and frequently require the business name to be on the item.
- **Subsistence while travelling** on business is usually treated more favourably than a local meal.

What the agent should do rather than guess: record the row with the attendees and purpose so **any** treatment can be applied later, tag it `#entertainment` or `#meals`, and say plainly that the rate needs confirming for the year. A correctly documented meal can always be classified; an undocumented one cannot.

## VAT and Input Tax

- Input tax is recoverable only with a **valid tax invoice** carrying the supplier's registration number and the tax broken out — a card slip is not one at any amount (`receipts.md`).
- **Simplified invoices** are permitted below a local ceiling and still carry the supplier's tax number.
- Some categories are **blocked from recovery** regardless of documentation — commonly business entertainment and, in several countries, passenger cars and fuel for private use.
- **Cross-border services** frequently trigger a reverse charge: the buyer accounts for the tax. A foreign invoice with no tax on it is usually not a tax-free purchase, it is a reverse-charge one.
- **Mixed-use purchases** recover input tax on the business proportion only, using the same stored basis.
- Store amounts **gross and net with the tax broken out** in the ledger row for anything business — retro-fitting the tax split across a year is a project.

## Personal Card, Company Money

A company expense paid on a personal card is **not a company expense at the moment of payment**. It is a claim against the company: an employee reimbursement, or in a one-person company a director's loan / owner's draw entry.

- Book it in `claims/<year>.md` like any other claim (`reimbursement.md`), even where the user is the company.
- Recording it directly as a company cost with no reimbursement trail is what turns into an unexplained loan account balance a year later.
- The reverse — a personal purchase on the company card — is a debt to the company and must be repaid or treated as pay. It is a routine finding and a routine correction, provided it is recorded.

## Rebilling a Client

Two treatments with different tax consequences, and the choice is not cosmetic:

| Treatment | What it is | Consequence |
|---|---|---|
| **Disbursement / pass-through** | A cost incurred **as agent** for the client, in the client's name, passed on at exactly cost | Usually outside the supplier's own taxable turnover; the client gets the original invoice's tax |
| **Recharge** | A cost the business incurred **for itself** while serving the client, then billed on — with or without markup | Part of the business's own supply: its own tax rate applies to the whole rebilled amount, including a travel cost that was originally zero-rated |

The condition for a genuine disbursement is narrow — incurred in the client's name and passed on unaltered — and most "expenses billed to the client" are recharges. Assume recharge unless the arrangement clearly meets the disbursement conditions, and verify the local criteria before treating anything as a pass-through.

Mechanically: the cost keeps its ledger row tagged `#billable` with the client's name as a pointer to `~/Clawic/data/contacts/contacts.md`, and it stays a cost. The rebill is revenue, and it becomes an invoice line (`invoice` skill). Netting the two inside the expense ledger loses both numbers.

## Red Flags

Anything observable in this table suspends the guidance above and routes to a qualified accountant or tax adviser in the user's jurisdiction.

| Signal | Suspicion | Action |
|---|---|---|
| A letter, notice or enquiry from a tax authority | An examination is open; informal reconstruction can make it worse | Stop; route to a professional before producing or altering any record |
| A deduction being claimed retroactively across multiple prior years | Amended returns and interest exposure | Professional; do not amend from this skill |
| Business use of a home the user owns, at a material percentage | Capital gains consequence on sale | Professional before claiming the exclusive-use route |
| A cost being reclassified specifically to fall under a threshold | Avoidance pattern, recognized as such | Refuse the reclassification; document the real facts |
| Payments to a family member on the payroll | Reasonableness and evidence-of-work tests | Professional; ensure the work and the rate are documented |
| Crossing a registration threshold (VAT/GST, payroll, quarterly filing) | Late registration penalties | Professional; the date of crossing matters, not the date noticed |
| Cash-heavy revenue or expenses with sparse records | Reconstruction risk and presumption of unreported income | Professional; fix capture first (`capture.md`) |
| Cross-border activity — foreign clients, foreign employees, foreign subsidiaries | Reverse charge, permanent establishment, withholding | Professional; do not apply domestic rules abroad |

**Write on the way out.** A deductibility decision and its reasoning go into the ledger row's purpose field with the `#billable`, `#capital`, `#meals` or `#entertainment` tag as applicable; an apportionment basis that took work to derive goes to `artifacts/` with its measurement, its date and its revisit condition, plus its `## Boxes` line in the same turn; a confirmed jurisdiction rule the user supplies is a declaration and goes to `config.yaml` under `platform`; a rebillable cost keeps the client's name as a pointer to `~/Clawic/data/contacts/contacts.md`, never a duplicated client record. Formats in `memory-template.md`.
