# Property

A property's value is an estimate or appraisal with a date and a source, not
cash and not a sale price. Estimated rent is not income received.

## Find or add the property

```sh
candor properties list --limit 25 --reason "Check whether this property is already tracked"
candor properties get PROPERTY_ID --limit 100 --reason "Read the property and its value history"
```

Match on the full address, including the unit, before creating anything.
Use the canonical property id for every later change; a provider's id is not
it.

## Preview and apply

```sh
candor properties preview --file PROPERTY.json --reason "Preview the property the person described"
candor properties apply PREVIEW_ID --reason "Track the reviewed property"
```

Send the complete intended property input (include `property_id` for an
existing one). Check the preview's address, amounts, date, ownership share,
and `effect` before applying that exact preview. A changed input needs a
fresh preview; never create a second property as a workaround.

- A current manual value switches the property to manual tracking and stops
  automatic estimates.
- An older appraisal has `effect: history_only`: it extends history and
  changes nothing current.
- In manual mode, omit `monthly_rent` to keep the current estimate, or send
  `monthly_rent: null` to clear it. Zero means a real zero.
- Rent estimates say whether they are for the whole property or one unit.
  Per-unit estimates are not multiplied by a guessed unit count.

## Ownership and the mortgage

- Value is whole-property; the owned value applies the recorded ownership
  share once.
- Link the loan account once. Set `mortgage_balance_scope: full_account` only
  when the whole recorded loan balance belongs in this property's equity.
  Ownership share does not establish who owes the debt; when that is unclear,
  leave equity unknown rather than inventing a split. One loan links to one
  property.
- A property confirmed paid off needs no loan link; a recorded zero balance
  is also fine.

## Check the result

Re-read the property and `candor net-worth summary --reason "Check the property's effect on net worth"`.
History-only changes must not move current net worth. Value changes are not
investment returns or income.

## Estimates and refresh

Automatic estimates use a US provider about every 30 days. Ordinary reads
never contact it; a preview may. On `property_rate_limited` or
`property_provider_budget_exhausted`, wait `retry_after_seconds` before
another estimate; saved estimates and manual tracking keep working. A failed
refresh keeps the last estimate: report its original date.

## Undo or stop tracking

- `candor properties revert PREVIEW_ID --reason "Undo the latest property change"`
  reverses the latest import unless newer evidence arrived; then submit a
  correction instead.
- `candor properties archive PROPERTY_ID --reason "Stop tracking the sold property"`
  stops tracking and keeps history. It does not record a sale or pay off the
  loan.
