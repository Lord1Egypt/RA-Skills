
# Plan a goal

Take what the person wants, even half worked out, and leave them with a plan
Candor keeps current: each goal saved in their words with the measure that
reads its progress from their records, a pace, a next step, and a budget that
pays for it. Tell them straight whether it works, and if not yet, what would
have to change.

## Workflow

Work through these steps in order:

```text
- [ ] 1. Open and recover saved goals, budget, and what they said before
- [ ] 2. Hear the goal and save it in their words right away
- [ ] 3. Read what the records say about capacity
- [ ] 4. Work out what it takes and give the verdict
- [ ] 5. Break it into goals with measures, paces, and next steps
- [ ] 6. Make the budget pay for it
- [ ] 7. Tag the money a tagged measure reads
- [ ] 8. Say what you saved and how you will keep them on it
```

**1. Open and recover.** `candor open` if this conversation has not opened
Candor yet, then the saved plan:

```sh
candor goals list --limit 100 --reason "Recover saved goals before planning"
```

The opening carries the context notes tagged `objectives_and_time_horizons`
and the other topics; when it says they are truncated, follow its
continuation. Read each goal's `progress` (required contribution, projected completion,
what moved since last time). On a return visit, say what changed first:
payments that landed, a goal that moved, a step that came due.

**2. Hear the goal, save it now.** Ask what they want and why, and the
questions they would not think to ask: by when, what it is for, what they
will not give up, what is flexible. Ask one or two at a time. Save the goal as
soon as they describe it, even with no figures: `goal_key` (a durable slug you
reuse), `kind`, `name` in their words, `why` in their words, and `note` with
what they said. Numbers come later with `goals update`. A goal that lives
only in the conversation is lost.

Their answers outlive this goal, so save them by topic too, not only in the
goal's `note`: what they will not give up
(`constraints_and_protected_resources`), who it is for
(`people_and_responsibilities`), how they trade speed against safety
(`decision_preferences`), how they cover bills meanwhile (`operating_plan`).
The budget, Candor's review, and later plans read those. Skip what
`agent_context` already answers.

**3. Read capacity from the records.** Use Candor's figures; do not rebuild
them:

```sh
candor budget context --reason "Read monthly income, spending, and saved budget for the plan"
candor debts list --reason "Read debts, rates, and minimums the plan must carry"
candor recurring list --limit 100 --reason "Read committed bills and income for the plan"
candor liquidity summary --reason "Read cash the plan could start from"
```

Follow every `next_actions` continuation before you sum anything. Read
coverage: if income or an account is missing, say what the plan cannot see.

**4. Work out what it takes, then the verdict.** Required pace = what is left
over the time left. Compare it with what the records show is free each month
after spending and debt payments. `candor goals preview --file GOAL.json --reason "Check the draft goal's figures"`
computes a draft's required contribution and projected date without saving.
Give the verdict plainly:

- **Works:** say the pace and when they get there.
- **Not yet:** say by how much, and what would change it, with figures: a
  later date, a smaller target, a cut in a category they told you they care
  less about, a debt paid off first, income they expect.

Show the current course and one alternative when the choice is real. For
debt payoff, cash and reserves, or "can I afford it" questions, read the
matching reference below first.

**5. Break it into goals.** One ambition with several figures is several
goals, each with its own measure and `parent_goal_id` naming the goal it
serves. Pick the measure that tells whether they are getting there:

| What they want | Measure |
| --- | --- |
| Save in an account kept for it | `accounts` |
| Part of an account (an amount or percent) | `account_share` |
| Pay down cards or loans | `debt` |
| A cushion in everyday accounts, in months of spending | `cover` |
| Live within an amount, spend less | `spending` (a ceiling) |
| A side business paying for itself, a property's net, what a habit costs | `tagged` (see step 7) |
| Something the records cannot show | `recorded` |

Set `priority` only as they ranked it. Give each goal a `next_step` with a
date and a `check` (a payee transaction to watch, the goal's own `figure`, an
`ask`, or a `review`). Save a piece you suggested that they did not name, such
as a cushion, with `proposed: true`; set it false when they take it on.

A debt payoff goal once it has figures (ids come from `accounts.list`; amounts
are exact Money text):

```sh
candor goals create --file GOAL.json --reason "Save the goal the person described"
```

```json
{
  "goal_key": "cards-paid-off",
  "kind": "debt_reduction",
  "name": "Pay off the cards",
  "why": "So we start with the baby debt free",
  "measure": { "kind": "debt", "account_ids": ["CHASE_CARD_ACCOUNT_ID", "CITI_CARD_ACCOUNT_ID"] },
  "target_amount": "USD 9800.00",
  "target_date": "2027-05-01",
  "contribution_amount": "USD 640.00",
  "contribution_cadence": "monthly",
  "next_step": { "date": "2026-11-05", "check": { "kind": "transaction", "payee": "CHASE", "expect": "charge" } }
}
```

A piece of a larger ambition adds `parent_goal_id`; one you suggested adds
`proposed: true`. Later changes send `goal_id` (the `goal_key` works as its
value) and only what changed:
`candor goals update --file GOAL_UPDATE.json --reason "Add the target and pace they settled on"`.

If the write returns `goal_not_tracked`, `goal_plan_short`, or
`goal_plan_missing`, fix what it names (usually a missing measure or a pace
below what the date needs) or tell the person why not.

**6. Make the budget pay for it.** A goal with a monthly pace needs room in
the budget. With no budget, save a starting one from their records with a line
for the goal (the `candor-budget` workflow builds it). With a budget, add or
change only the lines involved:

```sh
candor budget update --file BUDGET_UPDATE.json --reason "Make room for the goal's monthly pace"
```

Nudge toward a budget that supports each goal; never force one on someone who
does not want a budget.

**7. Tag what a tagged measure reads.** Before saving a `tagged` goal, tag
the transactions it counts with a rule, and check the draft first:

```sh
candor rules preview --match-merchant-contains "ETSY" --add-tag shop --reason "Check which transactions the shop tag would cover"
candor rules create --file RULE.json --reason "Tag the shop's income and costs for its goal"
```

The tag reaches past records in the background; quote the goal's progress
once `candor rules get RULE_ID --reason "Check the shop tag has applied"` reports `applied`.

**8. Keep them on it.** Save a note tagged `objectives_and_time_horizons`
with what they want and why, if it is not already kept, and the other topic
notes from step 2. Candor's review
raises a goal that slips; each goal's next step comes back on its
date. Offer a recurring check-in only if they want one.

## How to answer

Lead with the verdict in one or two sentences, then the plan as short
bullets, then one line on what you saved, then one question.

```text
Paying off both cards by next June doesn't work yet. It takes $640 a month, and right now about $410 is free after bills, so it is $230 short.

- Pay the Chase card first: it charges 27% and is the smaller balance.
- Dining out has run $380 a month. Cutting it to $150 closes the gap.
- Or keep dining as is and the cards are clear by October instead.

I saved "Pay off the cards" with both cards as its measure, $640 a month, and a check on the Chase payment on the 5th. Your budget now has a $640 debt line.

Which do you want: June with less dining out, or October as things are?
```

Pass through the goals panel when they want to see it:
`candor visual goals --reason "Show the person their goals"`.

## Gotchas

- Save on the first visit. Evals failed most often when the ambition stayed
  only in the conversation. A goal with no figures yet is still a goal.
- Do not save your own idea as theirs. A cushion, a sub-goal, or an account
  they did not name is `proposed: true`.
- Do not invent targets or dates. Use what they said or what the records
  show; leave the rest out until they say.
- Do not decide their priorities. Rank goals only as they did; you can
  recommend an order and say why.
- Goal progress fields already carry the pace math (`required_contribution`,
  `projected_completion_date`). Quote them instead of recalculating.
- An account can hold only one goal outright. Use `account_share` or `cover`
  when money is shared.
- A balance is not spare cash. Subtract near-term bills, saved budget lines,
  and other goals before calling money available.
- Rates, promo deadlines, and benefit rules change. Read them from account
  terms or a current official source, never from memory.

## Go deeper

- [Debt payoff and promo rates](references/debt-and-promos.md): payoff order,
  promo deadlines, missing card or loan terms.
- [Cash, reserves, and spare money](references/cash-and-reserves.md):
  emergency funds, idle cash, interest rates, what to do with extra money.
- [Cash flow ahead](references/cash-flow-ahead.md): "can I afford it", runway,
  making it to payday, a planned big expense.
- [Goal recipes](references/goal-recipes.md): revising a goal, recording
  progress by hand, archiving, and goal history.
