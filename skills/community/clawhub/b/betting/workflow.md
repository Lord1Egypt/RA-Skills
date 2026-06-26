# Clean Ticket Protocol

Use this protocol whenever the user asks whether a bet is good, how much to stake, or whether to wait for a better number.

If legality, age, jurisdiction, or operator compliance is unclear, stop at general information and do not move into actionable sizing.

## 1. Define the ticket exactly

Capture:
- sport and event
- market type
- line and odds
- book or exchange
- stake size or unit plan
- settlement rule if it matters

If any of these are missing, say what is still unknown before giving a view.

## 2. Convert the price

Turn odds into:
- implied probability
- break-even price
- payout profile

Use `sizing.md` for the formulas. Narratives come after the price math.

## 3. Check market integrity

Run `market-checks.md` to confirm:
- same market and same line across books
- overtime, player, and void rules
- limit or liquidity realism
- whether the quote is still actionable

## 4. Reject weak tickets fast

Run `red-flags.md`.

Instant pass if:
- the edge depends on missing information
- the market is obviously stale or suspended
- the user is forcing a parlay to rescue bad single-leg prices

## 5. Return a decision memo

Use `ticket-template.md` and end with one label:
- positive edge
- reduce size
- wait
- pass

Good output includes fair price, book price, estimated edge, maximum analytical size, and kill conditions.
