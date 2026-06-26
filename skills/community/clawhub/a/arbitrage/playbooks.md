# Arbitrage Playbooks

Use the playbook that matches the market structure. If none match cleanly, fall back to `workflow.md` and classify conservatively.

## 1. Sportsbook Surebet

Best for opposite outcomes across books or a book versus exchange.

### Required checks
- exact event, market, and line match
- decimal odds after commission
- max stake or max payout by venue
- void and palpable error rules

### Output focus
- surebet test
- stake split
- max realistic size
- one-leg-fill failure plan

## 2. Prediction Market Basket

Best for mutually exclusive outcomes whose total cost is below the guaranteed payout.

### Required checks
- outcome partition is complete
- outcomes cannot overlap
- resolution source and cutoff are identical
- redemption and withdrawal costs are included

### Output focus
- basket cost
- guaranteed payout
- net basket edge
- remaining ambiguity, if any

## 3. Cross-Exchange Spot Arbitrage

Best for the same asset trading at different prices across venues.

### Required checks
- transferable asset or pre-funded inventory
- order book depth, not just last price
- fees, withdrawal costs, FX, and transfer latency
- whether the edge survives realistic fill size

### Output focus
- locked versus inventory-dependent classification
- size limited by depth and transfers
- venue that constrains the trade

## 4. Basis or Carry Trade

Best for spot versus perp or future.

### Required checks
- exact contract specs
- funding, borrow, and carry
- liquidation mechanics
- expiry and roll plan

### Output focus
- annualized net edge
- carry assumptions
- hard lock versus synthetic edge classification

## 5. Retail or Pricing Mismatch

Best for the same good or service priced differently across channels.

### Required checks
- identical SKU or deliverable
- shipping, tax, returns, and fraud reserve
- payment hold and cash conversion cycle
- inventory availability

### Output focus
- unit economics
- operational bottleneck
- whether the edge scales or disappears after friction

## Default Recommendation Ladder

Use one of these endings:
- Proceed: economics and settlement both hold
- Verify one item: only one missing fact stands between watchlist and action
- Watchlist: real angle exists but not enough lock quality yet
- Reject: edge is fake, too small, or too operationally fragile
