---
name: cap-table
description: Cap table management and modeling for startups. Tracks equity分配, option pools, investor ownership, and dilution scenarios. Essential for fundraising.
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: [python3]
    always: false
---

# Cap Table Manager

Comprehensive cap table modeling tool for startup founders and investors.

## Features

### Ownership Tracking
- Founders, employees, investors ownership %
- Option pool allocation
- Vesting schedules
- Transfer restrictions

### Modeling Scenarios
- New funding round dilution
- Option pool shuffle (increase)
- M&A acquisition scenarios
- Liquidation preferences

### Reports
- Ownership breakdown by stakeholder
- Dilution impact by round
- Option pool utilization
- 409A valuation support

## Usage

```bash
python3 captable.py --action summary
python3 captable.py --action dilute --round SeriesA --new_investors 2 --investment 5000000
python3 captable.py --action pool --increase 10
```

## Example Cap Table

| Stakeholder | Shares | Ownership |
|-------------|--------|-----------|
| Founders | 4,000,000 | 40% |
| Employee Pool | 1,000,000 | 10% |
| Seed Investors | 2,500,000 | 25% |
| Series A | 2,500,000 | 25% |

## liquidation preference Examples

- 1x non-participating
- 1x participating
- 2x liquidation preference + participation

---

*Built by Beta*
