# Currency — Foreign Money Without Losing the Original

**Before converting anything**, read `home_currency` from `config.yaml` — or `currency` from `~/Clawic/profile.yaml` if the skill's own config does not set it. Every stored total is in `home_currency`; every entry also keeps what was actually paid.

**Contents:** [Three Fields, Always](#three-fields-always) · [Which Rate Is the Right Rate](#which-rate-is-the-right-rate) · [What Foreign Payment Actually Costs](#what-foreign-payment-actually-costs) · [Do Not Revalue History](#do-not-revalue-history) · [Reporting in Two Currencies](#reporting-in-two-currencies) · [Rounding](#rounding) · [Non-Money Currencies](#non-money-currencies)

## Three Fields, Always

`Amount` (what was paid, with its currency) · `Rate` (home per unit of foreign, with the date it applied) · `Home` (the converted amount, in `home_currency`).

```
Home = Amount × Rate
8,400 JPY × 0.0062 EUR/JPY = 52.08 EUR
```

Storing only `Home` destroys the entry the first time anyone needs it:

- A disputed charge cannot be matched to a statement line that shows 8,400 JPY.
- The rate cannot be checked, so an error is undetectable.
- The user cannot answer "was the ramen expensive" — the only version of the question they actually think in.
- A group settlement in the local currency has nothing to settle against.

The rate direction is fixed for the whole catalog: **home per unit of foreign**, so the conversion is always a multiplication. Storing the inverse for some currencies and not others produces entries that are wrong by a factor of thousands and look plausible.

## Which Rate Is the Right Rate

In order of authority:

1. **The rate the card actually applied**, taken from the statement. Available only after posting, and it is the true cost. At reconciliation, replace the estimate with it and mark the row settled (`reconciliation.md`).
2. **The published daily reference rate for the transaction date** (a central bank or another public reference the user names once). Correct for cash purchases and as the estimate before a card posts. Tag the row `#rate-estimated`.
3. **The rate on the receipt**, when the merchant printed one. Useful as corroboration; it is often the merchant's own rate, not the card's.
4. Never a monthly average, never a trip average, never today's rate applied to last month's purchase. Each of those moves money between periods, and in a group, between people (`sharing.md`).

Tax and accounting rules sometimes **mandate** a specific rate — an official monthly or annual rate for the reporting period. Where a business return is involved, the mandated rate governs the return while the ledger keeps the real one; verify which applies before restating anything.

For **cash** exchanged in advance, the honest rate is the effective one from the exchange itself: `local received ÷ home paid`, including the fee. The board rate was never what was paid.

## What Foreign Payment Actually Costs

Four separable costs, and users habitually attribute all of them to "the exchange rate":

| Cost | Typical shape | Control |
|---|---|---|
| Network conversion | The card network's daily rate — close to the reference rate | None; it is the fair part |
| Issuer FX fee | A percentage on top, commonly 0-3% depending on the card | Choose the card. This is why a no-FX-fee card is worth having before a trip, not after |
| Dynamic currency conversion (DCC) | The merchant's terminal or ATM offers to bill in your home currency; commonly 3-7% worse, sometimes more | **Always decline. Pay in the local currency.** Applies at ATMs too |
| ATM operator fee | Fixed per withdrawal | Withdraw larger amounts less often |

**Log fees separately**, in a `fees` category, rather than folding them into the purchase. Folded in, they are invisible; separated, they are one of the most cuttable lines in any traveller's ledger, and the annual total is usually a surprise (`categories.md`).

The DCC decision is made at the terminal in two seconds and cannot be undone afterwards. It is the highest-value single sentence this skill has for anyone travelling.

## Do Not Revalue History

An expense is fixed at its date. When rates move, past entries do **not** change — re-converting them would mean last year's dinner costs a different amount every time someone opens a report, and no comparison between two months would ever be stable.

The exceptions are **open positions**, not past spend:

- A refund due in a foreign currency: its home value moves until it lands. Record the expected amount in the foreign currency and convert only when it arrives.
- An unpaid claim or rebillable in another currency: same treatment. The difference between claim-date and payment-date value is an FX gain or loss, and it belongs in `fees`, not in the original category.
- A stranded cash balance from a trip, carried forward to the next one (`travel.md`).

## Reporting in Two Currencies

- Every total is in `home_currency`. That is what makes months comparable.
- A **trip or a period spent abroad also reports the local-currency total**, because that is the number the user experienced and can sanity-check. A home-currency-only trip summary reads as an abstraction.
- Multi-currency months state which currencies appear and what share of the total each is; a month that is 40% in another currency has a real FX sensitivity and a single number hides it.
- Never present a converted number without its rate date somewhere in the same answer when the user is likely to compare it to a receipt.

## Rounding

- Convert first, then round the **result** to two decimals. Never round the rate — a rate rounded to two decimals is worthless for anything with a small unit value, and JPY, KRW, VND and IDR are all in that class.
- Zero-decimal currencies (JPY, KRW, CLP, VND among others) are stored as integers in their own currency and to two decimals in home currency. Writing `8400.00 JPY` is not wrong, it is just noise that suggests a precision that does not exist.
- Currency codes are ISO 4217 three-letter codes in the value (`8400 JPY`), never symbols. `$` alone is ambiguous across at least a dozen currencies and the ambiguity is discovered years later.

## Non-Money Currencies

- **Points, miles and vouchers redeemed**: cost zero. Log the entry at 0 with a note of what it would have cost, so the trip's category picture stays true without inventing spend. Points *bought* for money are a real expense at the purchase price.
- **Crypto used to pay for something**: the expense is the home-currency value at the moment of payment, with the same three fields. The disposal may also be a taxable event in the user's jurisdiction — route that to their accountant (`business.md` Red Flags).
- **Barter and trades**: the expense is the fair value of what was given up, and it is a business record question rather than a personal-tracking one.

**Write on the way out.** Every foreign entry carries all three currency fields in its ledger row from the moment it is written; an estimated rate carries `#rate-estimated` and gets replaced with the settled rate at reconciliation in the same pass; FX and ATM fees get their own `fees` rows; a user's chosen reference-rate source and their `home_currency` are declarations and go to `config.yaml`; a stranded foreign cash balance carried forward is noted in the trip envelope. Formats in `memory-template.md`.
