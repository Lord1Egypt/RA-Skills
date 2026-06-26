---
description: Calculate job profitability and track costs. Paste job data weekly for running totals and margin analysis.
disable-model-invocation: true
---

# Job Costing

Read the user's business profile for equipment list and team.

## Input format
User pastes: "[customer], [hours], [equipment used], [fuel gallons], [crew members], [price charged]"
Or provides in any format. Parse and calculate.

## Calculations

### Equipment cost per hour
(Purchase price / expected lifetime hours) + fuel cost per hour + (annual maintenance / annual hours)
If user has not provided equipment costs, ask once and remember.

### Labor cost per hour
Hourly wage + 25% burden (taxes, insurance, workers comp)

### Overhead per hour
Monthly overhead (insurance, truck, trailer, phone, software, marketing, fuel for driving, rent) / monthly billable hours

### Per job
- Total equipment cost = equipment rate x hours
- Total labor cost = labor rate x hours x crew size
- Materials (if any)
- Fuel cost = gallons x current diesel price
- Total cost = equipment + labor + materials + fuel + (overhead rate x hours)
- Profit = price charged - total cost
- Margin % = profit / price charged x 100

## Weekly report (Friday)
When user pastes multiple jobs:

| Job | Customer | Hours | Revenue | Cost | Profit | Margin |

Summary:
- Total revenue this week
- Total costs
- Total profit
- Average margin %
- Best job (highest margin)
- Worst job (lowest margin) -- diagnose why
- Month-to-date vs revenue target (if set)

## Flags
- Any job under 30% margin: flag and explain what drove costs up
- Any job under break-even: urgent flag
- Equipment cost per hour trending up: maintenance due?
