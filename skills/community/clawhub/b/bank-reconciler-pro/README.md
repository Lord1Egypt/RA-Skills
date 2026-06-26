# Bank Statement Reconciler

AI-powered bank statement reconciliation tool.

## Quick Start

```python
from scripts import reconcile_bank_statements, TierConfig

# Basic reconciliation
result = reconcile_bank_statements(
    statement_file="bank.csv",
    order_file="orders.csv",
)

# With Professional tier features
tier = TierConfig(token="BANK-PRO-xxxxx")
result = reconcile_bank_statements(
    statement_file="bank.csv",
    order_file="orders.csv",
    match_mode="smart",
    amount_tolerance=0.1,
    date_range_days=5,
    tier=tier,
)
```

## Features

- **Multi-format support**: CSV, Excel, PDF, JSON
- **Bank coverage**: Chinese banks (BOC, ICBC, CCB, ABC), Alipay, WeChat Pay, PayPal, Stripe, Amazon, Shopify, Temu
- **Smart matching**: Exact, fuzzy, and semantic matching modes
- **Excel export**: Professional format for finance systems
- **Feishu integration**: Interactive cards for Professional+ tiers

## Directory Structure

```
bank-statement-reconciler/
├── SKILL.md                 # Skill definition
├── README.md                # This file
├── scripts/
│   ├── __init__.py         # Main module
│   ├── parser.py           # Statement/Order parsing
│   ├── matcher.py          # Reconciliation matching
│   ├── exporter.py          # Excel export
│   ├── feishu_card.py       # Feishu card generation
│   ├── tier_config.py       # Tier configuration
│   └── test_reconciler.py  # Unit tests
└── references/
    └── supported-formats.md # Format documentation
```

## Testing

```bash
cd /home/gem/workspace/agent/skills/bank-statement-reconciler
pytest scripts/test_reconciler.py -v
```

## Tier Capabilities

| Tier | Features |
|------|----------|
| Free | 50 statements/month, text output |
| Basic | 500 statements, Excel export |
| Standard | 5,000 statements, Alipay/WeChat, Feishu cards |
| Professional | Unlimited, PayPal/Stripe, semantic matching |
| Enterprise | Custom rules, API access |

## License

Proprietary - YK Global
