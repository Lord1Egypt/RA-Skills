# Income Tax — Deadlines, Differences, And Records

The bookkeeping job around income tax is not preparing the return: it is producing books the return can be built from, paying the right amount on time, and keeping what proves it.

**Before any tax work**, read `## Registrations` and `## Due` in `~/Clawic/data/accountant/memory.md`, and `filings/<year>.md` if `## Boxes` points there — what was filed and paid last period sets the safe-harbor base for this one. While `jurisdiction` is unset, name the regime being assumed before quoting any deadline or threshold (SKILL.md).

**Contents:** [Entity Type Decides Everything](#entity-type-decides-everything) · [The Calendar](#the-calendar) · [Estimated Payments And Safe Harbor](#estimated-payments-and-safe-harbor) · [Book-Tax Differences](#book-tax-differences) · [Deferred Tax](#deferred-tax) · [Deductions That Get Challenged](#deductions-that-get-challenged) · [Records And Retention](#records-and-retention) · [Working With The Preparer](#working-with-the-preparer)

## Entity Type Decides Everything

| Entity | Who pays the tax | Owner pay mechanism | Practical consequence |
|---|---|---|---|
| Sole trader | The owner, on business profit | Draws; no salary | Profit is taxed whether or not it is withdrawn |
| Partnership | The partners, on their allocated share | Draws and guaranteed payments | Allocation follows the agreement, not the cash taken |
| LLC (US, default) | Passed through to members | Draws | Tax classification can be elected separately from legal form |
| S corporation (US) | Shareholders, on their share | Salary **and** distributions | Reasonable compensation is required and examined (`owner-pay.md`) |
| C corporation | The company, then shareholders on dividends | Salary and dividends | Two layers, but a separate rate and retained earnings that are not taxed to owners |
| Nonprofit | Generally exempt, but not on unrelated business income | Salary only | Exemption is conditional and revocable (`nonprofit.md`) |

The election and the legal form are different things in several regimes, and an election has deadlines that are missed silently. Any change of entity or election is an escalation, not a bookkeeping decision (SKILL.md, Escalate).

## The Calendar

Build the actual calendar from `jurisdiction` and `fiscal_year_end` and put every date in `## Due`. US anchors, stable across years apart from weekend and holiday shifts:

| Obligation | Typical timing |
|---|---|
| Estimated income tax, individuals and many pass-throughs | Four instalments: mid-April, mid-June, mid-September, mid-January |
| Partnership and S corporation returns | Two and a half months after year end; September with extension |
| C corporation and individual returns | Three and a half months after year end; October with extension |
| Employee statements and contractor information returns | End of January |
| Payroll returns and deposits | Quarterly returns; deposits per the assigned schedule (`payroll.md`) |
| Annual state or local registration and franchise filings | Varies; often the same month every year |

**An extension to file is not an extension to pay.** Interest and, usually, penalties run from the original due date on any unpaid balance, so an extension without a payment is only half a solution.

## Estimated Payments And Safe Harbor

Underpayment penalties are charged quarter by quarter, so paying the full year's tax in December does not cure an under-paid April.

US safe harbor, which removes the penalty regardless of how the year turns out — pay, through withholding and instalments, the lesser of:

- **90%** of the current year's tax, or
- **100%** of the prior year's total tax — **110%** where prior-year adjusted gross income exceeded 150,000.

Worked: prior-year tax 24,000, AGI above the threshold → safe harbor is 26,400 for the year, 6,600 per quarter. Paying that leaves no penalty even if the current year's tax turns out to be 60,000; the balance is then simply due at filing.

Practical rules that follow:

- Base instalments on the **prior year** when income is rising and on the current year when income is falling — the safe harbor is a floor, not a target.
- Withholding is treated as paid evenly across the year in many systems even when it is not, which makes a late-year withholding increase a legitimate way to fix an under-paid earlier quarter. An estimated payment is credited when made.
- Set aside tax as revenue is earned rather than as the deadline approaches: a fixed percentage of each deposit moved to a separate account, sized from the prior year's effective rate. The account is a row in `~/Clawic/data/finances/accounts.md`, and its balance is not available cash.
- Every payment goes into `filings/<year>.md` with its period — the safe harbor calculation next year reads directly from it.

## Book-Tax Differences

The books follow the reporting framework; the return follows tax law. Listing the differences is the bookkeeper's actual deliverable to the preparer.

| Difference | Type | Effect |
|---|---|---|
| Depreciation: book straight-line vs tax schedules and expensing elections | Temporary | Reverses over the asset's life (`fixed-assets.md`) |
| Bad debt: book allowance vs tax deduction on actual write-off | Temporary | Reverses when written off (`receivables.md`) |
| Accrued expenses unpaid at year end, especially to related parties | Temporary, sometimes permanent | Many regimes deny the deduction until paid |
| Prepaid income taxed on receipt but deferred in the books | Temporary | Reverses as recognized (`revenue.md`) |
| Inventory costing differences and required capitalization of certain costs | Temporary | Reverses as stock sells |
| Entertainment, fines and penalties, and a portion of meals | Permanent | Never deductible; never reverses |
| Tax-exempt interest, certain life insurance | Permanent | Book income the return never sees |
| Research cost treatment where amortization is required rather than immediate deduction | Temporary | Reverses over the amortization period |

Keep the schedule as an artifact with the year, each difference, and the amount. It is what makes next year's return cheap and an examination survivable.

## Deferred Tax

Only where the reporting framework requires it — most small entities on a tax basis or a simplified local framework do not present it.

- A **temporary difference** creates a deferred tax liability when the book carrying amount exceeds the tax base for an asset (accelerated tax depreciation is the standard case), and a deferred tax asset when the reverse holds or when losses carry forward.
- Measure at the rate expected to apply when the difference reverses, using rates enacted or substantively enacted at the reporting date — not today's rate if a change is already law.
- A deferred tax asset is recognized only to the extent future taxable profit makes it recoverable; under US GAAP that judgement is expressed as a valuation allowance, under IFRS as non-recognition. Both require documented evidence, and a history of losses is strong evidence against.
- Permanent differences never create deferred tax — they only move the effective rate.

## Deductions That Get Challenged

The pattern is always the same: the deduction is legitimate, and the documentation is not.

| Item | What makes it stand |
|---|---|
| Meals with a business purpose | Who, what business was discussed, the receipt. Deductibility percentages differ by category and change with legislation — check for the year |
| Vehicle use | A contemporaneous log of business miles, or actual costs with a business-use percentage. Reconstructed logs are the first thing disallowed |
| Home office | Exclusive and regular business use of the space, measured area, and the method chosen consistently |
| Travel | Business purpose, itinerary, and the split where the trip is mixed |
| Equipment expensed under an election | The election made on a timely return, and the in-service date (`fixed-assets.md`) |
| Payments to family members | Real work, at a market rate, paid and documented like any other worker |
| Owner loans to and from the entity | A written note, a market interest rate, and actual repayments — otherwise it is recharacterized as a distribution (`owner-pay.md`) |
| Charitable giving | The receipt in the required form; for larger non-cash gifts, a valuation |

Rates, limits, and percentages here are indexed or legislated and move — mileage rates, meal percentages, expensing limits, contribution ceilings. Look each one up for the filing year and record the year alongside the figure (SKILL.md, Traps).

## Records And Retention

- Keep the **document**, not just the ledger entry: an entry with no support is an assertion. Digital copies are acceptable in most regimes if they are complete and legible.
- US windows: **3 years** from filing generally, **6 years** where income could be understated by more than 25%, **indefinitely** where no return was filed or fraud is alleged, and **4 years** for employment tax records. Asset records run for the life of the asset **plus** the window after disposal, because basis has to be proven when it is sold. Property and entity formation records are effectively permanent.
- Non-US windows are more often longer than shorter, and several regimes mandate specific storage formats or in-country storage. Confirm from `jurisdiction`.
- **Never destroy during an open examination or dispute**, whatever the window says. Suspend the purge, push out its `## Due` row, and note the suspension in `## Open Items` until the matter closes.
- Purging is a `## Due` item, done once a year at year-end close, and the purge itself is recorded — proving what was destroyed and when is occasionally the point (`close.md`).

## Working With The Preparer

What a preparer needs, and what makes the engagement cheap:

- The final trial balance for the year, on the declared basis, from books that are reconciled and locked.
- The general ledger detail, the asset register with additions and disposals, and the book-tax difference schedule.
- Payroll returns and their reconciliation to the ledger, plus contractor information returns.
- Loan statements, lease agreements, and any new contract that changes revenue treatment.
- Owner transactions: draws, distributions, contributions, loans, and reasonable compensation support.
- A list of open questions with the entity's proposed treatment. Questions with a proposed answer get resolved in one exchange; questions without one become a call.

The preparer signs, but the entity is responsible for what is filed. Understand every position before it is filed, and if a position cannot be explained in one sentence, that is the signal to ask rather than the signal to trust.

**Write when this file produced something durable**: every filing and payment → `filings/<year>.md`, with the next date in `## Due`. The book-tax difference schedule and any position taken → `artifacts/` with its `## Boxes` line. A registration, election, or change of entity classification → `## Registrations`. The preparer as a person → `~/Clawic/data/contacts/contacts.md`. The tax reserve account → `~/Clawic/data/finances/accounts.md` (`memory-template.md`).
