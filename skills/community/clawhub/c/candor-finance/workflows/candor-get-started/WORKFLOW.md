
# Get started

The first conversation decides whether Candor is useful. Leave the person
with a short, true picture of their money from their own records, one or two
things worth a closer look that you checked yourself, and what they want from
their money saved in their words. Setup itself takes one line.

## Workflow

```text
- [ ] 1. Confirm Candor is connected and the first records have landed
- [ ] 2. Read what they already told Candor
- [ ] 3. Give the first look from first_pass
- [ ] 4. Check what is worth raising in the records
- [ ] 5. Learn what they want and what shapes it, and save it
- [ ] 6. Hand off to the workflow that fits
- [ ] 7. Acknowledge the opening
```

**1. Confirm the connection.** Use the opening this conversation already
has (the front door opens first, and that first opening carries
`first_pass`); run `candor open` only if there is none. If it returns an account
step instead of records, pass through the exact link it gives and say in one
sentence what to do there (see Access below). If the first sync is still
filling in, say so, do the parts that do not need history, and open again
when it finishes. If the person asked something specific during setup, do
that task first and fold the setup confirmation into the answer.

**A free start with no accounts yet** (the opening's `coverage.missing`): the
first look starts with building the picture. Ask which accounts they have,
starting with the one most of their money moves through, and bring the
records in with `candor-add-records` (its migration reference for a move):

- A CSV or another finance app's export (Monarch, Copilot, YNAB, Mint,
  Quicken), of any size, comes in as an upload: create one and give them its
  link to drop the file into Candor on the device that has it. A CSV already
  attached in the chat goes through the link too. Files they already dropped
  show in the opening as `uploads.waiting`. When they are not sure how to
  download one, give them `https://candor.money/how-to-export-your-transactions`.
- A PDF statement or a screenshot already in the chat is read there and
  imported inline.
- With no file to hand, start lighter: ask what each account holds or owes,
  roughly, and add the accounts by hand with those balances. That gives a
  first picture of what they have and owe. Candor's first review needs
  transactions, so it waits until a statement or export comes in; say so.

Sort what landed with no category, then give the first look from the
records. Candor works from records kept by hand the same way it works from a
bank's. Connected banks (US institutions, on the Personal plan, set up on the
web) keep every account and transaction current on their own; records kept
by hand suit trying Candor first. Every opening names the page where a bank
connection starts (`financial_position.coverage.accounts_url`), for when the
person wants that.

**2. Read what they already told Candor.** During signup the person chose a
starting point and may have answered up to seven household questions (work,
dependents, upcoming changes, age, housing, workplace retirement plan, health
coverage). Those are their own context notes and arrive in the opening's
`agent_context`. Do not ask them again. Process `untagged_notes` too: tag a
note with the matching `context_needed` topic only when it is the person's
own statement.

```sh
candor notes update --file NOTE.json --reason "Tag what the person said with its topic"
```

**3. Give the first look.** If this is not the workspace's first opening,
`first_pass` is absent: build the same picture from
`candor budget context --reason "Read monthly income and spending for a first look"`,
`candor debts list --reason "Read what is owed for a first look"`, and
`candor recurring list --limit 100 --reason "Read what repeats for a first look"`.
The first opening carries `first_pass`: monthly
income, spending, debt payments, and net; each account with its balance and
debt terms; and the recurring series. Turn it into three or four plain lines
the person would care about: what comes in, what goes out, what they owe, and
what repeats. Say which months and accounts it covers. Where your host draws
Candor's panels in the chat, show the same picture with
`candor visual overview --reason "Show the first look"`, and read the
panel's text before you talk about it. If the opening offers to keep the
first look as a report, save it once it lands and link it; the person opens
it from their Reports tab and it stays current.

**4. Check what is worth raising.** Summaries point; records prove. Read the
review's areas if the first review has landed, then look in the
transactions themselves:

```sh
candor transactions list --since START --until END --limit 100 --reason "Read the first months of transactions for anything worth raising"
candor recurring list --limit 100 --reason "Check repeating charges for price changes and overdue bills"
```

Follow every continuation. Look for a duplicate charge, a fee, a refund or
reimbursement that never arrived, a bill that went up, a promo rate ending,
or a review area the records confirm. For a full pass, run the sweep in the
`candor-full-checkup` workflow. Raise at most two things, each with the
amount, the date, and what it is compared against. Keep the rest for a later
conversation; a first look that lists everything buries what matters. A finding that waits on a
later posting gets a note with a watch (see `candor-find-money`). Raising
nothing is fine when nothing stands out.

**5. Learn what they want, and what shapes it.** Start with one natural
question, built from their starting point if they chose one: "What do you
want your money to do in the next year or two? Paying off the cards, a home,
working less, or just knowing where it goes are all good answers." Do not
make goals a gate: someone who only wants to see where the money goes gets
that. Save what they say right away, in their words:

- a note tagged `objectives_and_time_horizons` with what they want and why;
- the goal itself, with `candor-plan-a-goal`, even before it has numbers.

```sh
candor notes create --file NOTE.json --reason "Keep what the person wants from their money"
```

```json
{
  "body_markdown": "Wants both cards paid off before the baby comes in May: \"I don't want to start that with debt.\"",
  "context_topics": ["objectives_and_time_horizons"]
}
```

Then work through `context_needed`, one question per reply, picking the
topics their answer and the first look made matter: a payoff goal raises how
they trade speed against cash on hand (`decision_preferences`); a dated goal
raises how they cover bills and reserves meanwhile (`operating_plan`); kids
or parents raise `people_and_responsibilities`; "but not the vacation fund"
is `constraints_and_protected_resources`. Two or three topics is plenty for a
first conversation. Save each answer with its topic as it comes; the rest
wait for later conversations, where the review's gaps and the other
workflows pick them up.

If they say they want lighter help, record it:

```sh
candor preferences update --file PREFERENCES.json --reason "The person asked for just the essentials"
```

**6. Hand off.** A goal goes to `candor-plan-a-goal`; "where does it go" to
`candor-budget`; wrong categories to `candor-sort-transactions`; a finding to
`candor-find-money`. If they want regular check-ins and your host can run
them, set one up with `candor-weekly-check-in`.

**7. Acknowledge.** When the opening offers `open.acknowledge`, run it after
the first look is done. On a free start that opened empty, acknowledge once
you have asked for the records; when they land, open again for the first
look, since the first opening after a workspace's first records carries
`first_pass` however few there are.

## How to answer

One line of setup, then the picture, then what you checked, then one
question. Put any offer ("I can ask Spotify for the refund") before the
question, and end on that one question. Under a screen.

```text
Candor is connected to your checking, savings, and two cards, with records back to June.

- About $6,200 comes in each month and $5,700 goes out, so roughly $500 is left.
- You owe $9,800 across the two cards. The Citi card charges 26%.
- Rent, car insurance, and 9 subscriptions repeat every month, about $2,900 together.

One thing worth a look: Spotify charged you twice on September 3 ($11.99 each). I'll watch for the refund if you ask for one.

What do you want your money to do in the next year or two?
```

## Access

- No Candor tools in this session: send them to
  `https://candor.money/START.md`.
- The opening returns an account step (no account yet, or a business
  workspace's access lapsed): pass
  through the exact `safe_url` or `recovery_url` and say what to do there.
  Banks, plans, and payment are handled only on `https://app.candor.money`.
- No bank connected: you keep their records with `candor-add-records`, and
  Candor works from them, amounts stored as entered with no conversion. Connecting US banks on the Personal plan, on the web, keeps
  every account and transaction current with no statements to send; mention
  it once, when it fits.

## Gotchas

- Do not stop at `first_pass` or the review's titles. Evals failed when the
  first look repeated the summaries and missed a duplicate, a price increase,
  and a missing reimbursement that were plainly in the transactions.
- A sync that is still filling looks like a month with no spending. Check
  coverage before you call anything low.
- Do not send a "you're all set" message and stop. The first reply carries
  the first look.
- Do not recite the household answers back as a list; use them.
- Do not run the topics as a questionnaire. Ask one question per reply, each
  tied to what they just said or what the records showed.
- Do not promise a fixed number of findings, and do not invent one to fill
  the slot.
- Do not ask which review to run. Pick from what the records show.

## Go deeper

- [First look in detail](references/first-look.md): reading `first_pass`,
  partial coverage, empty or balances-only workspaces, and the household
  answers each adviser area depends on.
