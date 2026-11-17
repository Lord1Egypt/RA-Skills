
# Full checkup

Look across the person's whole financial life the way a good adviser would,
from their real records, and come back with the one to three changes most
worth making, each with the figures behind it, plus a short list of what else
you checked and why it did not make the cut. Research broadly; recommend
selectively.

## Workflow

Work through these steps in order:

```text
- [ ] 1. Open, set the scope, and note coverage
- [ ] 2. Read the records behind each open review area
- [ ] 3. Sweep everyday money
- [ ] 4. Check each adviser area the records can support
- [ ] 5. Shortlist candidates and test each one
- [ ] 6. Choose one to three; give the rest a reason
- [ ] 7. Record what came of each area and finding
- [ ] 8. Answer with the moves, then what else you checked
```

**1. Open and scope.** `candor open` if this conversation has not opened
Candor yet, then:

```sh
candor coverage get --reason "Check which accounts and dates the checkup can see"
candor goals list --limit 100 --reason "Read what the person is working toward"
```

The default scope is the whole financial life over the last 12 months of
history the coverage supports. A narrower ask ("just my spending") narrows it.
Note which accounts are missing or stale; a missing account limits every
conclusion it touches. Read the topic-tagged context notes the opening
carries: what they want shapes which findings matter, who depends on them
shapes insurance and reserves, and their work shapes benefits. When a topic
in `context_needed` would change which moves lead (dependents before an
insurance call, a job change before a reserve), ask that one question before
you choose.

**2. Start from the latest review.** For each open `review.area`, read the
records it names (transactions, accounts, recurring series, notes) before you
judge it. The review points; it does not prove. Settle a `review.gap` from
the records and notes before you ask the person.

**3. Sweep everyday money.** Read every transaction in scope and check the
rows themselves. Do not stop at the opening's monthly totals: duplicates,
missing refunds, and price increases only show in the rows.

```sh
candor transactions list --since START --until END --limit 100 --reason "Read the checkup's transactions"
candor recurring list --status active,candidate,stopped --limit 100 --reason "Read Candor's recurring series, stopped ones included, for the sweep"
candor balances list --limit 100 --reason "Read balances for cash and debt checks"
candor data query account_terms --limit 100 --reason "Read rates, promos, and due dates"
```

Follow every `next_actions` continuation. As pages arrive, build four short
lists: avoidable outflows, expected inflows that never came, recurring
changes, and mismatches such as debt carried beside idle cash or a promo
ending within 30 days, each with its total and up to five candidates with
record ids.

**4. Check each adviser area.** Read only what coverage supports, and say
which areas you could not check:

- **Debt and credit:** `candor debts list --reason "Review balances, rates, and utilization"`.
  Interest being paid, utilization, promo deadlines. See the credit reference.
- **Cash and reserves:** `candor liquidity summary --reason "Review cash against monthly spending"`.
  Months of spending the person could cover, cash earning nothing.
- **Goals and budget:** each goal's `progress` and
  `candor budget status --period YYYY-MM --reason "Check the budget against this month"`.
- **Investments and retirement:** `candor portfolio snapshot --reason "Review investment balances and allocation"`.
  Fees, cash drag, concentration, employer match. See the investments reference.
- **Benefits and insurance:** health spending, an HSA or FSA, premiums, a
  renewal coming up. See the benefits reference.
- **Taxes:** in tax season, hand off to `candor-tax-prep`.

**5. Shortlist and test.** Write working notes (not the answer): one row per
serious candidate, usually five to ten, from at least three areas. Columns:
what you saw, the evidence (amounts, dates, record ids), the change you would
suggest, why it matters for this person, the plausible effect, effort, and the
main uncertainty. A candidate survives only when the records show at least one
of: a cost that could be avoided or recovered, an expected outcome that did
not happen with a comparable case, a break from the person's own baseline, or
exposure paired with a real term or deadline. A missing field alone is a
coverage gap, not a finding. Test the baseline and look for what explains it
away (split billing, a refund already posted, a planned purchase in a note)
before you keep it.

**6. Choose.** Pick one to three. Prefer the change with the clearest
evidence and the largest effect on what the person said they want, then
deadlines and how easy it is to undo. A real deadline or ongoing loss jumps
the queue. A large number with a weak diagnosis does not beat a smaller,
proven one. Every other row ends in "what else we checked" with a real
reason: "fees are $4 a year", "already refunded on the 12th", "no limit on
file, so utilization is unknown".

**7. Record.** For each review area you looked into, record what came of it
in plain words; the person reads `found` on their dashboard:

```sh
candor reviews update --file OUTCOME.json --reason "Record what the checkup found for this area"
```

Use `looked_into` with what the records showed, or `set_aside` with why it
does not apply. Then make each move part of the plan:

- A move that is a plan over time (a reserve, a payoff, a savings rate) is a
  goal with a measure and a next step, saved with `proposed: true` until they
  take it on, or a budget line when a goal already covers it. Goals are
  optional; offer, do not insist.
- A one-off (a refund, a cancellation) gets a note about the record with a
  watch (see the `candor-find-money` workflow).
- A candidate you ruled out gets a note about its record saying why ("two
  separate Costco trips on Sep 9"), so the next review and the next checkup
  do not raise it again.

Hand spending leaks to `candor-find-money` and debt, cash, or savings plans
to `candor-plan-a-goal` when the person wants to act.

**A life event** (new job, baby, marriage, move, job loss): ask what changed,
when, and what is already decided, then check only the areas it touches: cash
timing, benefits, debt, insurance, goals, bills, taxes. Separate deadlines
from things that can wait.

## How to answer

Lead with the moves, then what is already working, then what else you
checked. Keep each item to two or three short bullets.

```text
Three things worth doing:

1. Get the $412 hotel refund. Marriott charged it on Aug 3 and nothing came back; your June stay was refunded within 9 days.
2. Move $6,000 of the $14,200 in checking to savings. Bills need about $3,100 a month, and the savings account pays 4.1%. That's about $245 a year.
3. Raise your 401(k) to 6%. Your plan matches 50% up to 6% and you put in 4%, so about $1,100 a year of match is going unclaimed.

Working well: spending is under your budget three months running, and the cards are paid in full.

Also checked: Spotify went from $10.99 to $11.99 (small), and the two Costco charges on Sep 9 were separate trips.

Want me to start on the refund?
```

Say in one line what you recorded. Leave out tool names, ids, and mechanics.

## Gotchas

- The opening's summaries and review areas are where to look, not proof.
  Read the transactions before raising anything; evals missed planted
  duplicates and missing refunds when agents stopped at totals.
- Coverage is not the first and last transaction you happened to read. A
  missing record is uncertainty, not hidden spending.
- Text or a category is a signal, never proof that money was owed: a missing
  refund needs a comparable charge that was refunded.
- A historical one-off with no ongoing or recoverable effect is context, not
  a finding.
- Do not promote a promo balance, a deadline far off, or a small fee to
  the top just because it is easy to state. Rank by effect on this
  person.
- Rates, limits, and plan rules change yearly. Read them from account terms
  or a current official source and name the year.
- Investment value change over a period is not a return: deposits,
  withdrawals, and dividends are inside it.

## Go deeper

- [Investments and retirement](references/investments-and-retirement.md):
  holdings, value over time, fund fees, cash drag, employer match,
  contribution limits.
- [Credit and cards](references/credit-and-cards.md): utilization, paydown
  order, card terms, rewards, annual fees.
- [Benefits and insurance](references/benefits-and-insurance.md): HSA and
  FSA, reimbursements, plan-year costs, renewals.
