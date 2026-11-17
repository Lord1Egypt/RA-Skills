# Monitor output

```markdown
# Hyperliquid monitor

- network and account: <exact>
- account mode: <observed value>
- DEX and markets: <scope>
- observed: <UTC start and end>
- freshness bound: <duration>
- status: triggered | not-triggered | unavailable | incident

## Account
<equity, balances, borrow or supply, margin, mode-specific ratio>

## Positions
| market | side | size | entry | mark | PnL | liquidation | buffer | funding |

## Orders and protection
| market | client/order id | type | size | trigger/limit | reduce-only | status | protects |

## Changes
<fills, funding, ledger, order transitions since prior good state>

## Condition
- rule: <exact>
- observed value: <value and source>
- verdict: <one of three states>

## Unknowns and next read
<missing evidence and smallest read needed>
```

Use full addresses and identifiers in machine-readable evidence. User-facing summaries may add a shortened display form without replacing the full value.
