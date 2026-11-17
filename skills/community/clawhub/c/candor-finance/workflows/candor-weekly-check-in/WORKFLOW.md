
# Check-in

On its own schedule, Candor
reviews the household's records and every note you and the person have kept,
and raises up to five areas worth talking through (a problem, an
opportunity, or a question) and up to three gaps that keep its picture wrong. A check-in turns that, plus what changed since last time, into
a short conversation: what moved, what you found in each area, and what needs
their answer. Every area you look into gets an outcome recorded, so the next
review builds on it.

## Workflow

```text
- [ ] 1. Open and read what changed since last time
- [ ] 2. Report goal moves, answered watches, and due notes
- [ ] 3. Look into each review area in the records
- [ ] 4. Record what came of each area, and check it saved
- [ ] 5. Settle the gaps from records and notes before asking
- [ ] 6. Acknowledge the opening
- [ ] 7. Send the check-in
```

**1. What changed.** `candor open` if this conversation has not opened
Candor yet. Read `new_since_checkpoint` first and
follow every continuation it lists before you say anything about it. For the
new transactions, check what matters: a large or unusual charge, a deposit
that was expected or missing, a category that reads wrong, a transfer
mistaken for spending. A transaction that matched no rule is fine if its
category reads right. Keep routine activity out of the reply.

For "how did this month compare?" use Candor's comparison rather than your
own sums:

```sh
candor changes list --reason "Compare this month's spending and income with last month"
```

**2. Goals, watches, notes.** Say how each measured goal moved
(`goal.moved`), which watches answered (`seen`, `missed`, `held`, `broken`,
`crossed`), and which notes came due. Tell the person what each watch found.
Resolve its note only when the outcome is settled, such as the refund posting;
after `missed` or `broken`, update the note and its `revisit_at` instead. A
goal step that came due gets done or rescheduled.

Keep the plan current with what you find. A goal that fell behind, money a
finding frees or costs each month, or a bill that changed ends in a saved
change to the plan: a new pace or date on the goal (with the person's say
on which), a budget line, or the goal's next step. Say it in one line.

**3. Look into each area.** Each `review.area` names a topic, why it matters
for this household, what is not known, and the records behind it. It states
no figures on purpose. Read those records before you raise it:

```sh
candor transactions get TRANSACTION_ID --reason "Read a record the review area points at"
candor recurring get RECURRING_ITEM_ID --reason "Read the series the review area points at"
```

Use the workflow that owns the topic when it needs depth: a spending leak to
`candor-find-money`, a slipping goal to `candor-plan-a-goal`, wrong
categories to `candor-sort-transactions`. If the area does not hold up in the
records, say so; that is an outcome too.

**4. Record each outcome.** For every area you looked into, send the area id
from the opening, `outcome` (`looked_into` or `set_aside`), and `found`: what
the records or the person showed, or why it does not apply. The person reads
`found` on their dashboard, so write it in their words, with no ids or
jargon.

```sh
candor reviews update --file OUTCOME.json --reason "Record what came of the review area"
```

```json
{
  "area": "AREA_ID",
  "outcome": "looked_into",
  "found": "Your phone bill went from $65 to $85 in October. It is a price increase, not a one-off."
}
```

Check the write response; if it failed, fix and retry before you tell the
person anything was recorded. When
there is a follow-up, also leave a note about the record (`about`), with a
watch when the records will show the answer.

**5. Gaps.** Each `review.gap` says what to settle, which area it changes,
and how the answer is recorded (a rule, a note on a record, an account
added: from the person's statements, or connected when they choose to). Settle it from the records and notes first. Ask the person only
what is left, in one plain question, and save the answer the way the gap
says. When nothing else needs their answer this time, one question from
`context_needed` is a good use of the slot.

**6. Acknowledge.** Run `open.acknowledge` when the opening offers it, after
you have processed everything above.

**7. Send the check-in.** See below. A scheduled check-in with nothing worth
saying stays silent unless the person asked for a report every time.

Earlier reviews and what came of them: `candor reviews list --reason "Read earlier reviews"`.

## How to answer

What changed first, then each area in a line or two with what you found,
then the one thing that needs their answer.

```text
Since last Sunday: your paycheck landed ($3,140), and the emergency fund passed $4,000, two weeks ahead of pace.

- Your phone bill went from $65 to $85 in October. It's a price increase, not a one-off. Want me to look for a cheaper plan or call them?
- The $214 Amazon return from September hasn't been refunded yet. I'm watching for it and will tell you when it posts.
- The review asked whether your partner's card belongs in the budget. I left that open for you.

Should your partner's card count toward the household budget?
```

## Gotchas

- Do not list the review's areas back. Evals failed when agents named the
  areas without opening their records, and when one told the person an area
  was resolved after the write had failed.
- Record an outcome for every area you looked into, including one that did
  not hold up. An area without an outcome comes back in the next review.
- Read `new_since_checkpoint` before saying "nothing new". Evals failed when
  a return visit missed a $684 payment that had landed in between.
- `found` is for the person: "Your phone bill went up $20 in October", not
  "recurring item r4 price_changed_at".
- Areas state no figures. The figures come from the records you read.
- A note or answer that settles an area is how the next review learns it;
  an area you set aside stays out of later reviews.

## Go deeper

- [Scheduled check-ins](references/scheduled-check-ins.md): the person asks
  for a recurring or later check, and how each host runs one.
