# Sweep and test

Use when the person asks you to find money rather than naming a charge.

## Set the window

```sh
candor coverage get --reason "Check which accounts and months the sweep can see"
```

Sweep the months coverage supports, usually the last 3 to 12. The first and
last transaction you see are not the coverage boundary. Name the accounts and
months you could not see in the answer.

## Read every page

```sh
candor transactions list --since START --until END --limit 100 --reason "Read the sweep window"
```

Follow each `next_actions` continuation and keep only counts and the few
candidates you need next as pages arrive (if you can run code, save the
pages and analyze them there). A page total covers that page only.

## Patterns and comparators

| Pattern | Looks like | Comparator that makes it real |
| --- | --- | --- |
| Duplicate | Same merchant, same amount, same or next day | The merchant's other periods show one charge; no refund followed |
| Repeat fee | Overdraft, late, foreign, ATM, maintenance fees | Earlier occurrences, and the account terms that set the fee |
| Missing credit | A large or unusual debit with no later inflow | A similar past debit that did get a refund or reimbursement |
| Charge after cancel | A recurring payee posting after a known end date | The cancellation date from a confirmation or a note |
| Price increase | A series with `price_changed_at` set | The postings before and after, at the same cadence |
| Forgotten service | A subscription-shaped series the person does not mention | Ask; do not decide it is unwanted |
| Trial converting | A small authorization, then a first full charge | The trial terms from the signup confirmation |

Subscription-shaped means `direction` outflow with `cashflow_role` expense.
Transfers, debt payments, and refunds are not subscriptions however regular
they look. Text and category are signals, never proof.

## Testing one candidate

```sh
candor transactions get TRANSACTION_ID --reason "Read the exact candidate"
candor transactions list --merchant MERCHANT --since START --until END --limit 100 --reason "Compare the merchant's other charges"
candor recurring get RECURRING_ITEM_ID --reason "Read the series behind a recurring candidate"
candor transactions list --recurring-item-id RECURRING_ITEM_ID --reason "Read every posting of the series"
```

For each candidate, compare posted versus pending, date, amount, currency,
account, description, and any refund or reversal. Classify it as supported,
explained (say why), or not enough evidence. Keep only supported ones for
the person.

A series keeps only its newest postings (`last_paid_at`, `last_amount`); the
series read above returns every posting under each name the bank used. Check
amounts against `price_levels`: another plan from the same payee can appear.

## Ranking

Lead with money already lost and recoverable, then ongoing costs (a yearly
figure only when the cadence is real), then deadlines like a trial ending.
Three solid findings beat ten maybes.
