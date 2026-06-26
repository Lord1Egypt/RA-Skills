# Purchase Paths

Use this file when the user wants a recommended route rather than a raw winner.

## Core Output Idea

Do not output only a winner.

Output a path:
- where to buy
- which seller type to prefer
- why this route wins
- what tradeoff it accepts

## Recommended Output Modes

### Best Overall Route

Use when the user wants one default answer.

Structure:
- `Default route`
- `Why this route wins`
- `What you give up`

### Multi-Route Decision

Use when the user has mixed priorities.

Structure:
- `Lowest-price route`
- `Safest route`
- `Best-value route`

### Wait / Skip Route

Use when current offers are all weak.

Structure:
- `Why not buy now`
- `What better trigger to wait for`
- `What platform or seller to watch`

## Route Templates

### Lowest-Price Route

Use when:
- the savings gap is meaningful
- the product is easy to verify
- the user is willing to accept some friction

### Safest Route

Use when:
- the item is high-value
- returns or warranty matter
- authenticity certainty matters
- the user wants the most reliable experience

### Best-Value Route

Use when:
- lowest price is too risky
- safest route costs slightly more but not excessively
- the goal is the best risk-adjusted purchase path

### Apparel / Outlet Route

Use when:
- VIPSHOP or similar channels are relevant
- branded discount inventory is part of the comparison
- size, season, and return constraints matter more than electronics-style authenticity logic

## Good Final Language

Prefer:
- "默认最优路径是..."
- "如果你主要看最低价，走这条，但默认不建议"
- "这条路径贵一点，但买的是更稳的履约和售后"
- "这条路最省钱，但便宜主要便宜在风险"

Avoid:
- "看需求"
- "都可以"
- "各有优劣"
