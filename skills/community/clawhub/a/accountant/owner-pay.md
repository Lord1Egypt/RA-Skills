# Owner Pay And Equity — Taking Money Out Correctly

How an owner is paid is decided by `entity_type`, not by preference, and getting it wrong is expensive in a way that compounds quietly across years.

**Before advising on or recording owner pay**, read `entity_type` in `~/Clawic/data/accountant/config.yaml` and `## Books` in `~/Clawic/data/accountant/memory.md` for the election actually in force, and `artifacts/` for an existing reasonable-compensation determination. Changing the salary/distribution split without revisiting that determination is what makes it indefensible.

## What Is Available By Entity

| Entity | Mechanism | Payroll taxes | Accounting |
|---|---|---|---|
| Sole trader | Draw only | Owner pays self-employment tax on business profit | Dr Owner draws (contra-equity) / Cr Bank |
| Partnership | Draws plus guaranteed payments for services | Generally self-employment tax on the allocated share | Draws to each partner's capital account; guaranteed payments are an expense of the partnership |
| LLC taxed as a pass-through | Draw only | Self-employment tax on the member's share | Member draws, per member |
| S corporation | **Salary and** distributions | Payroll tax on the salary; distributions carry none | Salary through payroll; distributions to a distributions account |
| C corporation | Salary and dividends | Payroll tax on the salary; dividends taxed at the shareholder level | Salary through payroll; dividends reduce retained earnings |
| Nonprofit | Salary only | Normal payroll | No distributions exist; excess benefit is a sanctionable event (`nonprofit.md`) |

Two consequences that surprise people constantly:

- A sole trader or partner **is taxed on profit, not on draws**. Taking nothing out does not reduce the tax bill; taking everything out does not increase it.
- A sole trader cannot be an employee of their own business. Running themselves through payroll creates a payroll registration, returns, and withholding for a person who is not an employee.

## Draws Are Not Expenses

```
Owner takes money:               Dr Owner draws (contra-equity)  / Cr Bank
Owner puts money in:             Dr Bank                          / Cr Owner capital
Owner pays a business cost personally, to be repaid:
                                 Dr Expense                       / Cr Due to owner (liability)
Business card pays a personal cost:
                                 Dr Owner draws                   / Cr Card
At year end (pass-throughs):     Draws and capital close into the owner's capital or retained earnings
```

Coding a draw to expense overstates costs, understates equity, produces a wrong return, and — for a limited-liability entity — weakens the argument that the entity is separate at all (SKILL.md Rule 6). Mixed personal and business spending on one account is the single most common finding in a small-business examination.

## Reasonable Compensation (S Corporations)

The structural point: distributions avoid payroll tax, salary does not, so there is a permanent incentive to under-pay salary. Tax authorities examine exactly this, and the correction is back payroll tax plus interest and penalties on the reclassified amount.

- **There is no statutory percentage.** The widely repeated 60/40 salary-to-distribution split is a practitioner rule of thumb with no legal basis; relying on it as if it were a rule is what makes a position weak. Practitioners use it as a sanity check, never as the determination.
- The determination is built from **what the role would cost to replace**: duties actually performed, hours, experience, comparable local pay for the same scope, what the business could pay, what non-shareholder staff earn, and the amount of profit attributable to capital and other people rather than to the owner's work.
- Distributions materially exceeding a modest salary in a business whose profit comes from the owner's own labor is the classic examined fact pattern.
- **Document the determination the year it is made**: the comparables with their sources and retrieval dates, the hours, the calculation, and the conclusion → `artifacts/reasonable-comp-<year>.md`. Reconstructing it during an examination convinces nobody.
- Review annually and whenever the role, the hours, or revenue changes materially.

## Loans To And From The Owner

- A loan needs the substance of a loan: a **written note**, a stated market interest rate, a repayment schedule, and actual repayments. Without them, tax authorities recharacterize it — money out becomes a distribution or salary, money in becomes a capital contribution.
- Interest on a below-market loan can be imputed in both directions, creating income the parties never received.
- A due-to-owner balance that only grows is not a loan; a due-from-owner balance that only grows is a distribution nobody labelled. Both belong in `## Open Items` with a plan.
- Loans between related entities carry the same requirements plus transfer-pricing exposure where a border is involved (`currency.md`).

## Partner And Member Capital Accounts

- One capital account **per partner**, each tracking contributions, allocated profit or loss, and draws. A partnership with a single combined equity figure cannot settle a departure, a buy-in, or a dispute.
- Allocation follows the **agreement**, not the cash taken. A partner who took less than their allocated share still pays tax on the full allocation, and their capital account records the difference.
- Guaranteed payments for services are an expense of the partnership and income to the partner regardless of profit — economically like a salary, mechanically not one.
- Tax basis and book capital are different figures and diverge over time. Where they need to be reported separately, that is the preparer's calculation, built from the ledger's history — which is another reason capital accounts are never reconstructed later.

## Distributions, Dividends, And Legality

- **Distributions come out of accumulated profit**, and most jurisdictions prohibit distributing beyond it. A distribution from a company with no retained earnings can be unlawful and personally repayable by the recipients or the directors.
- Check before distributing: retained earnings after the current period, solvency after the payment, and any covenant restricting distributions.
- Distributions must respect ownership proportions where the law requires it — for S corporations, disproportionate distributions can threaten the election itself.
- Dividends are declared and become a liability on the declaration date, paid later: Dr Retained earnings / Cr Dividends payable, then Dr Dividends payable / Cr Bank.
- Distributions **never** run through the income statement, and a distribution recorded as an expense misstates profit and the return in the same stroke.

## Owner Benefits And Fringe Items

- Health coverage, vehicles, phones, home office, and travel provided to owners follow rules that differ by entity type — several regimes require adding some owner benefits to reportable wages, and a few disallow the deduction entirely.
- A benefit that is not on the payroll record where it should be is undeclared compensation, which is worse than a disallowed deduction.
- Retirement contributions for owners are frequently the largest legitimate deduction available and have their own limits, deadlines, and sometimes a requirement to cover employees on comparable terms. Contribution deadlines are often later than the filing deadline — a `## Due` row, because the opportunity expires silently.

## Buying Out Or Adding An Owner

An ownership change is an escalation, not a bookkeeping entry (SKILL.md, Escalate). The reasons are structural rather than clerical: valuation, whether the transaction happens at the entity or between owners, allocation of the year's profit around the change date, basis consequences, and the survival of any election. Record the facts and the date; let a tax professional decide the treatment before anything posts.

**Write when this file produced something durable**: the reasonable-compensation determination with its comparables → `artifacts/reasonable-comp-<year>.md` with its `## Boxes` line. The salary/distribution split and its review date → `## Due`. Loans to or from the owner, with the note reference → `## Open Items` until documented. A new partner, member, or ownership change → `## Books` and an escalation. Retirement contribution deadlines → `## Due` (`memory-template.md`).
