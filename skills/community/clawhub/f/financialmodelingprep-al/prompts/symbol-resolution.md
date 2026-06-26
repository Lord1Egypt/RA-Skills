# Prompt: Symbol Resolution

## Purpose
Reliably turn a company name (or ambiguous text) into the **correct, confirmed ticker** before any data is pulled. Prevents the classic failure of querying the wrong company.

## Reusable template

```
Resolve the company "{{company}}" to its FMP ticker before pulling any data.

1. Call /search-name?query={{company}} (or fmp_search).
2. From the results, identify candidates: symbol, name, exchange, currency.
3. Choose the PRIMARY listing on the expected exchange/currency. If there are
   multiple plausible matches (e.g. ADR vs local listing, same name on different
   exchanges), either ask me to confirm OR state which you picked and why.
4. Confirm the choice with /profile?symbol=<TICKER> — verify companyName,
   exchange, and currency match "{{company}}".
5. Report the resolved symbol explicitly, e.g.:
   "Resolved '{{company}}' -> <TICKER> on <exchange>, <currency>."
Do NOT pull quotes/statements until the symbol is confirmed. Never guess a ticker.
```

## Variables
- `{{company}}` — the company name or ambiguous text the user provided.

## Example
Input: `{{company}} = "Apple"`
- `/search-name?query=Apple` → candidates include `AAPL` (NASDAQ, USD) and unrelated names.
- Pick `AAPL`; confirm via `/profile?symbol=AAPL` → "Apple Inc.", NASDAQ, USD.
- Output: "Resolved 'Apple' → AAPL on NASDAQ, USD."

## Bad
> User: "Get Apple's revenue."
> Agent immediately calls `/income-statement?symbol=APPL` (typo) → empty array, or
> calls `/income-statement?symbol=AAPL` without confirming and happens to pull a
> different cross-listed entity. No confirmation, no profile check.

## Good
> User: "Get Apple's revenue."
> Agent: searches "Apple" → AAPL; confirms via profile (Apple Inc., NASDAQ, USD);
> states "Resolved 'Apple' → AAPL (NASDAQ, USD)"; only then pulls the income
> statement. If the name were ambiguous (e.g. "Delta"), it would ask which one.
