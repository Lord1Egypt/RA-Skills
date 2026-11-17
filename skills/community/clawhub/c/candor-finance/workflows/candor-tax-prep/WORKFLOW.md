
# Tax prep

Turn a tax year of records into a packet a preparer can work from: the
records that might matter grouped and tagged, what each group totals where the
grouping holds, the gaps and missing receipts, and the questions the preparer
will ask. Candor organizes the facts; the preparer decides the tax treatment.

## Workflow

Work through these steps in order:

```text
- [ ] 1. Open and set the year, accounts, and what the packet is for
- [ ] 2. Check coverage for the year
- [ ] 3. Gather candidate records by group
- [ ] 4. Test each group and settle what the person knows
- [ ] 5. Tag and correct so the groups hold
- [ ] 6. Write the packet and the open questions
- [ ] 7. Point them to the export
```

**1. Set the scope.** `candor open` if this conversation has not opened
Candor yet, then agree on the tax year, whose accounts, and what it is for: a
preparer, tax software, or estimated payments. Start from `agent_context`:
work, a side business, and dependents may already be there. Ask only what
applies and is not yet known (a rental, donations, medical costs, education,
a home office, childcare) instead of sweeping for everything. Save what they
tell you as a note tagged `current_financial_situation`, and dependents or
people they support as `people_and_responsibilities`.

**2. Check coverage.**

```sh
candor coverage get --reason "Check which accounts and months of the tax year Candor can see"
```

List months or accounts missing from the year. The first and last
transaction you see are not the coverage boundary.

**3. Gather candidates by group.** Read the year and the existing
organization:

```sh
candor transactions list --since YEAR-01-01 --until YEAR-12-31 --limit 100 --reason "Read the tax year's transactions"
candor rules list --limit 100 --reason "Read rules already shaping the year's records"
candor corrections list --limit 100 --reason "Read corrections already made to the year's records"
```

Follow every continuation. Group candidates by what the person said applies:
business income and costs, charitable gifts, medical, education, estimated
tax payments, childcare. A candidate is a record worth reviewing, not a
deduction. Keep exact date, amount, merchant, account, and category.

**4. Test and settle.** For each group, test refunds and reimbursements,
transfers and card payments, duplicates and reversals, mixed personal and
business use, and transactions that cross the year line. Ask the person only
what the records cannot show: the business purpose, the split on a mixed
purchase, whether a payment was a gift. Save each answer as a note on the
record (`about`), in their words.

**5. Tag and correct.** Make the groups hold with the smallest change:

```sh
candor corrections create TRANSACTION_ID --category CATEGORY --reason "Apply the category the person confirmed"
candor transactions split set --file SPLIT.json --reason "Split the mixed purchase as the person described"
```

For a repeated pattern, preview a draft rule first, then save it:

```sh
candor rules preview --match-merchant-contains "UPWORK" --add-tag tax-business-income --reason "Check which records the business income tag would cover"
candor rules create --file RULE.json --reason "Tag the person's business income for the tax packet"
```

Rules apply to past and new records as soon as they are saved, in the
background: total a tagged group only once `candor rules get RULE_ID --reason "Check the tag has applied"`
reports `applied`. Undo one
application with `candor rules revert APPLICATION_ID --reason "Undo the rule on this transaction"`, or stop the rule with
`candor rules disable RULE_ID --reason "Turn off the rule"`. Read back a corrected record with
`candor transactions get TRANSACTION_ID --reason "Read the transaction in question"` before you rely on it.

**6. Write the packet.** See [the packet](references/packet.md) for the
format. Save the open questions and missing receipts as a note tagged
`current_financial_situation`, so the next conversation picks them up.

**7. Point them to the export.** The person downloads their records from
Export in Candor Settings at `https://app.candor.money/settings`. You do not
generate, open, send, or upload that file; they decide who gets it.

## How to answer

Lead with what the year shows and what is missing, then the groups as short
bullets, then the questions, then one line on what you saved.

```text
Your 2025 records cover all of checking and the Chase card, but not the Amex before June.

- Etsy shop income: $14,320 across 212 deposits (tagged).
- Shop costs: $3,180 in supplies and $1,140 in Etsy fees (tagged). 9 Amazon orders mix shop and household items.
- Donations: $1,250 to 4 charities; receipts needed for the $500 gift.

Questions for your preparer: the Amex months, the 9 mixed Amazon orders, and whether the home studio counts.

I saved the tags and a note with these questions. You can download everything from Export in Candor Settings.

Want to go through the 9 mixed orders now?
```

## Gotchas

- Never call a record a deduction or estimate tax owed. Say "candidate" or
  "to review", and leave treatment to the preparer.
- Merchant name and category do not establish tax treatment. A purchase at
  an office supply store can be personal.
- Do not invent a business purpose, a split, or a receipt. Ask, or list it as
  a question.
- Check tax rules (limits, what counts) on irs.gov or the state's tax site
  when you mention them, with the year. Rules change every year.
- Prefer a single correction or split over a rule until the pattern is clear;
  a broad rule can retag records the person did not mean.
- Totals only where the grouping holds. A total that mixes personal and
  business purchases misleads the preparer.

## Go deeper

- [The packet](references/packet.md): sections, groups, and the questions
  preparers usually ask.
