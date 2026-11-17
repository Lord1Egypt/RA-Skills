
# Find money

Find the money that is leaking or owed: a charge made twice, a fee that can
be reversed, a refund that never posted, a price that crept up, a
subscription nobody uses, a trial about to bill, a paycheck that came in
short. Prove it from the records, then go get it with the person's okay
(cancel, dispute, request the refund) and leave a watch so Candor reports when
the money actually lands.

## Workflow

Work through these steps in order:

```text
- [ ] 1. Open and recover what is already being chased
- [ ] 2. Find the candidates (a named charge, or a sweep)
- [ ] 3. Test each one against the records before calling it real
- [ ] 4. Leave a watch on the outcome now, before you answer
- [ ] 5. Tell the person what you found and what it is worth
- [ ] 6. Act with their okay, then record the impact
- [ ] 7. Close it when the money lands or they drop it
```

**1. Open and recover.** `candor open` if this conversation has not opened
Candor yet. Read `watches` and due notes first:
a refund you were already chasing may have posted. Check what you have
already recorded:

```sh
candor impacts list --limit 25 --reason "Recover findings already being pursued"
```

Do not raise a finding the person already decided against; your note on the
record says so. Read their `decision_preferences` too: someone who said not
to chase small charges, or not to contact merchants for them, has answered
that already. When they tell you something like that now, save it with that
topic.

**2. Find the candidates.** For a charge they named, go straight to it:

```sh
candor transactions get TRANSACTION_ID --reason "Read the charge the person asked about"
candor transactions list --merchant MERCHANT --since START --until END --limit 100 --reason "Compare nearby charges from the same merchant"
```

For "find me money", sweep. Read the window from coverage, then every page
of it, and look for: the same merchant and amount on the same or next day,
repeated fees, charges after a known end date, large debits with no later
refund where similar debits had one, and recurring price changes.

```sh
candor coverage get --reason "Check which months the sweep can see"
candor transactions list --since START --until END --limit 100 --reason "Sweep the window for duplicates, fees, and missing credits"
candor recurring list --direction outflow --cashflow-role expense --limit 100 --reason "Read subscription-shaped bills for price changes and forgotten services"
candor changes list --domain recurring --limit 100 --reason "Read recurring price changes and series that stopped"
```

Follow every `next_actions` continuation, and keep a short ledger as pages
arrive: candidate, records, comparator, amount. See the
[sweep reference](references/sweep-and-test.md) for each pattern.

**3. Test before you claim.** A candidate is real only when the records
support it against a comparator:

- **Duplicate:** rule out split billing, a pending authorization that will
  drop, a tip adjustment, two real purchases, and a refund already posted.
- **Fee:** check earlier occurrences and the account's terms before calling
  it avoidable or reversible.
- **Missing refund or reimbursement:** know what was promised (receipt,
  cancellation email, claim, approval), by when, to which account. Match on
  payer and direction, not amount alone. Allow processing time.
- **Price increase:** `price_changed_at` and `previous_amount` on the series
  are the cue; confirm from the postings with
  `candor transactions list --recurring-item-id RECURRING_ITEM_ID --reason "Read every posting of the series"`.
  Rule out tax, usage, add-ons, proration, or a discount ending.
- **Paycheck:** compare exact deposits across prior cycles. Test a holiday
  shift, a split deposit, a new account, or a pending deposit before calling
  it missing or short. See [income checks](references/income-checks.md).

Drop what the records do not support. Missing data is not a finding.

**4. Watch it now.** As soon as a finding is real and its outcome depends on
a later posting, save a note linked with `about` to the charge, with a
`watch` and a `revisit_at` backup, in this same turn and before you ask for
anything. Do not wait for their okay: a merchant may refund on its own, and a
follow-up promised only in chat is lost.

```sh
candor notes create --file NOTE.json --reason "Watch for the Spotify refund on the duplicate charge"
```

```json
{
  "body_markdown": "Spotify charged $11.99 twice on Oct 3, four minutes apart; every other month has one charge. Expect an $11.99 refund to the same card. If none by Oct 20, dispute it with the card.",
  "about": { "resource": "transactions", "id": "TRANSACTION_ID" },
  "watch": { "payee": "SPOTIFY", "expect": "deposit" },
  "revisit_at": "2026-10-20"
}
```

The `watch` for other findings:

- A cancelled subscription or trial: `{"payee": "HULU", "expect": "no_charge"}`.
- A paycheck: `{"payee": "ACME PAYROLL", "expect": "deposit"}`.

Set `revisit_at` to when the money should have posted, processing time
included.

**5. Tell them what it is worth.** The amount, the dates, the comparator, and
a yearly figure only when the cadence is real. Say Candor is already watching.
Then the move: "Want me to cancel it?" or "Want me to ask Comcast for the $35
back?"

**6. Act with their okay, then record it.** Canceling, disputing, requesting
a refund, or emailing a merchant is outside Candor and needs their okay for
that action. Once you have it, do it with your own tools: sign in through the
browser they use, send the email, fill in the dispute form. If you do not have
the tools, give them the exact message or call script, the account and charge
details, and what to ask for. Never ask for their passwords in chat. See
[getting it back](references/getting-it-back.md). Then record what it is
worth:

```sh
candor impacts create --file IMPACT.json --reason "Record the duplicate charge being disputed"
candor impacts record --file EVENT.json --reason "The dispute was filed"
```

Use the [impact reference](references/impacts.md) for the event types and
value rules.

**7. Close it.** When the watch reports the deposit, or a cancelled charge
stays away past the next billing date, tell the person, record the value with
`impacts record` (`value_recorded`, `realized`), and resolve the note. When
the saving repeats (a cancelled $15 a month, a lower bill), offer to point it
at what they are working toward: a higher pace on a goal, or a budget line.
Save it if they agree; a goal they name goes to `candor-plan-a-goal`. If they
decide not to pursue it, note the decision, close the impact
(`closed_without_value`), and resolve the follow-up so it is not raised again.

## How to answer

Lead with what you found and what it is worth, then the evidence in one or
two bullets, then the move, then one question.

```text
Spotify charged you twice on October 3: $11.99 and $11.99, four minutes apart. Only one month of service.

- Your other months each have one $11.99 charge.
- Nothing has come back since.

Candor is watching for the refund. I can ask Spotify for the $11.99 back through their help page, or you can dispute it with your card.

Want me to request it?
```

After acting: "Requested. Candor is watching for an $11.99 deposit from
Spotify, and if it has not posted by October 20 it comes back up the next time
we talk."

## Gotchas

- Same amount and same day is a candidate, not a duplicate. Read both
  transactions; split billing and authorizations look the same at first.
- A promise, a submitted request, or an "approved" status is not money
  received. Realized means a posted deposit or an authoritative final status.
- Leave the watch before you answer. Recovery work usually ends unfinished,
  and evals failed most when the follow-up was only promised in chat.
- When the evidence settles it (split billing, a fee the terms allow), say
  so and close it. A watch on a settled finding is noise.
- Overdue is not pending. If the expected date passed, set the next
  `revisit_at` from what could still change the answer (the dispute window,
  the next statement), not the date you just checked.
- A small authorization at signup identifies the trial; it is not the price.
- A net deposit does not show gross pay, taxes, or hours. Do not blame a
  smaller paycheck on any of them without evidence.
- A watch counts only transactions that arrive after it is set. Read what
  already posted first.

## Go deeper

- [Sweep and test](references/sweep-and-test.md): the patterns to look for
  across a window and how to rule each one in or out.
- [Getting it back](references/getting-it-back.md): canceling, disputing,
  refund requests, trials, and what to put in a message or call script.
- [Income checks](references/income-checks.md): a paycheck that is late,
  short, missing, or irregular.
- [Impacts](references/impacts.md): recording what a finding is worth and
  what actually came back.
