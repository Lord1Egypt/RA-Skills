# Venue and Settlement Checks

Use this checklist before calling any opportunity locked.

## Core Venue Questions

For every venue involved, answer:
- What product is being traded?
- What are the fees and hidden charges?
- How fast can collateral or inventory move?
- Are there max size, max payout, or withdrawal limits?
- Are there region, KYC, or account restrictions?
- Can the venue void or repricing events under special conditions?

## Settlement Audit

| Check | Why It Matters |
|-------|----------------|
| Resolution language | Similar market names can settle differently |
| Expiry or cutoff time | A hedge can fail if one leg closes earlier |
| Collateral currency | FX can create non-obvious risk |
| Void rules | One side can be canceled while the other stands |
| Payout timing | Capital can be trapped longer than expected |
| Counterparty quality | Default or withdrawal risk can erase edge |

## Product-Specific Notes

### Sportsbooks and betting exchanges
- Check max bet, account limits, and palpable error rules
- Confirm whether voids apply symmetrically
- Treat promo terms separately from hard price edge

### Prediction markets
- Read full resolution criteria
- Check whether outcome baskets are truly complete and mutually exclusive
- Confirm fees on exit, redemption, and withdrawal

### Crypto spot, perp, and futures
- Check taker and maker fees, funding, borrow, and liquidation mechanics
- Treat bridge and withdrawal time as risk, not logistics
- Verify whether hedge requires pre-funded inventory

### Retail, resale, and physical goods
- Include shipping, handling, returns, fraud, breakage, and payment processor reserves
- Verify inventory is real and deliverable
- Treat time-to-cash as part of economics

## Red Flag Matrix

| Red Flag | Consequence | Response |
|----------|-------------|----------|
| Withdrawal disabled or slow | Hedge cannot complete on time | Reject or heavily discount |
| One venue has lower reliability | Payout risk dominates price edge | Cap size or reject |
| Rule mismatch | No true hedge exists | Reject |
| Size caps hidden until checkout | Capacity overstated | Re-size or reject |
| Fees depend on tier or token holdings | Net edge uncertain | Model worst-case fees |
| Region lock or KYC delay | Execution path breaks | Reject for that user |

## Minimum Output

Always state:
- which venue is the weakest link
- whether the trade depends on transfer
- what single check would most likely kill the trade
