# Expedia Booking Gates

Use this file before recommending any Expedia option as ready to book.

## Gate 1: Inventory freshness

- Was the price checked recently enough for the current flow?
- Is the result a public listing, a redirect candidate, or a Rapid booking-ready rate?
- If the answer is unclear, do not call it booking-safe.

## Gate 2: Cost realism

- Are taxes and mandatory fees visible?
- If a package includes flights, are baggage and seat costs still exposed elsewhere?
- Is the user comparing a like-for-like total?

## Gate 3: Flexibility and policy

- What is the cancellation deadline?
- Is the option refundable, partially refundable, or effectively locked?
- Are there property fees due later that change the decision?

## Gate 4: Trip fit

- Does the location fit the user's real plan?
- Does the package shape hide a weak flight or transfer?
- Does the car or activity timing still work with the stay?

## Gate 5: Authorization

- Is the user explicitly asking to continue toward booking?
- Are partner credentials or booking rights actually available?
- If payment or traveler identity details are needed, confirm again before execution.

## Output pattern

Return one of these:
- ready to compare further
- ready to price-check
- ready to book with explicit approval
- not safe yet, blocked by X
