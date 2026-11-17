# Fixed Assets And Leases — Capital Items Over Their Life

An asset is a cost that has been deferred on purpose. The register is the evidence that the deferral is still justified.

**Before capitalizing, depreciating, or disposing of anything**, read `## Fixed Assets` in `~/Clawic/data/accountant/memory.md` (or `asset-register.md` if `## Boxes` points there) and the depreciation schedule in `recurring-entries.md`. An asset already in the register with a different life is a policy question, not a new entry.

**Contents:** [Capitalize Or Expense](#capitalize-or-expense) · [Depreciation Methods](#depreciation-methods) · [Book Versus Tax](#book-versus-tax) · [The Register](#the-register) · [Disposals](#disposals) · [Impairment](#impairment) · [Leases](#leases)

## Capitalize Or Expense

Both tests must pass (SKILL.md Rule 5):

1. Unit cost ≥ `capitalization_threshold` — default 2,500, which matches the US de minimis safe harbor for a taxpayer without an applicable financial statement; the equivalent elsewhere is a stated internal policy, and having one in writing is what makes it defensible.
2. Useful life > 1 year.

| Cost | Treatment | Why |
|---|---|---|
| Purchase price, delivery, installation, testing, non-recoverable tax | Capitalize | Cost of getting it ready for use |
| Site preparation, professional fees directly attributable | Capitalize | Same test |
| Training staff to use it, launch marketing | Expense | The entity does not control trained staff as an asset |
| Repairs that restore original condition | Expense | No added life or capacity |
| Improvements that extend life, add capacity, or adapt to a new use | Capitalize | A new asset or an addition to the old |
| Routine maintenance contracts | Expense over the term | A service, prepaid if paid ahead |
| Items below threshold bought in bulk (30 chairs at 200) | Expense — the test is **per unit**, not per invoice | Grouping to force capitalization is policy drift |
| Internally developed software | Depends on framework and phase — research expensed, development capitalized when criteria are met under IFRS; US GAAP has its own phase rules | Never capitalize the whole project cost by default |

Applying the policy only when profit is high, or expensing everything in a good year to cut tax, is the drift the written policy exists to prevent.

## Depreciation Methods

Straight-line unless there is a reason:

```
Straight-line       = (cost − salvage value) ÷ useful life
Declining balance   = book value at period start × (factor ÷ useful life)   [salvage ignored until the floor]
Units of production = (cost − salvage) × (units this period ÷ total expected units)
```

- **Straight-line worked**: 4,400 cost, 200 salvage, 3-year life → (4,400 − 200) ÷ 36 = 116.67 per month.
- **Double declining worked**: 5,000 cost, 5-year life → rate 2 ÷ 5 = 40%. Year 1: 2,000. Year 2: 40% of 3,000 = 1,200. Continue until the straight-line remainder on the remaining life exceeds the declining amount, then switch — and never depreciate below salvage.
- **Units of production** is the honest method for machinery whose life is consumption, not time; it requires a defensible total-units estimate, which is why it is rare.
- **Start depreciating when the asset is available for use**, not when it is paid for or invoiced. An asset sitting in a crate is construction in progress and does not depreciate.
- **Land is never depreciated.** A building purchase is split between land and structure at purchase, using a defensible basis such as the tax assessment ratio; a split invented later cannot be supported.
- Review life and salvage when something changes materially — a change in estimate applies from now forward over the remaining life, never restated backwards.

## Book Versus Tax

They are different systems, on purpose, and their difference is a deferred tax item (`tax.md`).

| | Book | Tax |
|---|---|---|
| Method | Whatever reflects consumption; usually straight-line | Prescribed schedules — in the US, MACRS class lives and conventions |
| Immediate deduction | Not available | Expensing elections and bonus depreciation may allow much or all in year one |
| Salvage | Estimated and used | Generally ignored under MACRS |
| Convention | Monthly from availability | Half-year by default; **mid-quarter applies when more than 40% of the year's additions are placed in service in the final quarter**, which changes the whole year's deduction |

The immediate-deduction limits move: the US expensing election limit and its phase-out threshold are indexed annually, and the bonus depreciation percentage has been changed by legislation more than once since 2017. Look both up for the **acquisition date**, never carry last year's figure forward (SKILL.md, Traps). A large late-in-year purchase can also flip the whole year to the mid-quarter convention, so check the 40% test before advising on timing.

Keep one register with both columns. Two registers diverge, and the divergence surfaces at the worst moment — during the return or during diligence.

## The Register

Minimum fields, and the reason each exists:

| Field | Why |
|---|---|
| Description and identifier or serial | Existence check at count |
| In-service date | When depreciation starts; the convention test |
| Cost, and what is included in it | The tie to the ledger |
| Method, life, salvage | Reproducibility of the charge |
| Accumulated depreciation to date | The other tie to the ledger |
| Location, custodian | Finding it, and insurance |
| Funding — owned, financed, leased | Whether a liability exists against it |
| Disposal date, proceeds, gain or loss | Removal from the books |

**Both totals must equal their ledger accounts at every close** (SKILL.md ties). The most common break is an asset disposed of in the world and never in the register — the depreciation keeps running on something that no longer exists.

## Disposals

```
Dr Cash or receivable                proceeds
Dr Accumulated depreciation          everything taken to date
  Cr Asset                                       original cost
  Cr Gain on disposal    (or Dr Loss on disposal to balance)
```

- Gain or loss = proceeds − (cost − accumulated depreciation). Scrapping means proceeds of zero and a loss equal to the remaining book value.
- The gain is **not revenue** and belongs below the operating result; putting it in revenue inflates turnover, which matters for registration thresholds and covenants.
- A trade-in is a disposal plus an acquisition, at the fair value of what was given up. Netting them hides both.
- Tax treatment can differ sharply — recapture of previously deducted depreciation is common, and it is calculated per asset, not on the total.
- Remove the asset in the same turn as the physical disposal, and note the date in the register. An asset still depreciating a year after it was sold is the register's most common defect (`audit.md`).

## Impairment

- Trigger-based, not routine: physical damage, obsolescence, a discontinued line, a market collapse, or a plan to dispose early.
- **US GAAP**: two steps — compare carrying amount with the *undiscounted* future cash flows; only if those are lower does the loss get measured against fair value. Reversal is prohibited.
- **IFRS**: one step — carrying amount against the recoverable amount (the higher of fair value less costs to sell and value in use, discounted). Reversal is required when the reason no longer exists, capped at what the carrying amount would have been.
- Record the trigger, the test, and the figures as an artifact. Impairment is a judgement, and undocumented judgements are the ones challenged.

## Leases

`reporting_framework` decides the shape, and the small-entity exemptions matter more than the theory.

- **IFRS 16**: one model — the lessee recognizes a right-of-use asset and a lease liability for nearly everything, with the expense split into amortization and interest (front-loaded).
- **US GAAP, ASC 842**: both operating and finance leases go on the balance sheet, but an operating lease keeps a single straight-line expense in the income statement.
- **Exemptions worth taking**: short-term leases of 12 months or less with no purchase option, and under IFRS low-value assets. Electing them keeps a laptop lease off the balance sheet, and the election is a policy applied by class of asset, not per contract.
- Initial measurement: the liability is the present value of the remaining payments, discounted at the rate implicit in the lease when determinable, otherwise the incremental borrowing rate. **Document the rate used** — it is the number an auditor asks about first, and it cannot be reconstructed later.
- Variable payments based on usage or sales stay out of the liability and are expensed as incurred; payments tied to an index are included at the current index level and remeasured when it changes.
- A modification — term extension, scope change — remeasures the liability against the asset. Do not treat it as a new lease unless a separate asset is genuinely added at a standalone price.
- Sale-and-leaseback and related-party leases have their own rules and are worth escalating; the accounting frequently does not match the commercial intent.

**Write when this file produced something durable**: every acquisition, revaluation, and disposal → `## Fixed Assets` (or `asset-register.md`). The depreciation schedule → `recurring-entries.md`. The capitalization policy, the land/building split basis, an impairment test, or a lease discount rate → `artifacts/` with its `## Boxes` line. The asset existence check → `## Due` (`memory-template.md`).
