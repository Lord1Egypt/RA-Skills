---
name: bank-statement-reconciler
description: "Bank Statement Reconciler · 银行流水对账 — Upload bank statements (CSV/Excel/PDF) + orders/invoices → AI auto-matching → Reconciliation results (matched/difference/unclaimed/unmatched). Supports Chinese banks (BOC/ICBC/CCB), Alipay/WeChat Pay, PayPal/Stripe, Amazon/Shopify/Temu. Trigger: 银行流水, 对账, 流水匹配, 银行对账, bank reconciliation, statement matching, 订单对账, 发票对账."
---

# Bank Statement Reconciler · 银行流水对账

AI-powered bank statement reconciliation — upload statements + orders → get matched,差异,未认领,未核销 results.

## AI Agent Full Flow

```python
# One-shot reconciliation
result = reconcile_bank_statements(
    statement_file="bank.csv",           # Bank statement file
    order_file="orders.csv",             # Orders/invoices file
    statement_type="auto",                # auto, boc, icbc, ccb, alipay, wechat, paypal, stripe, amazon, shopify, temu
    order_type="auto",                   # auto, invoice, order
    match_mode="smart",                  # exact, fuzzy, smart (exact + fuzzy + semantic)
    amount_tolerance=0.01,               # For fuzzy matching (CNY)
    date_range_days=3,                   # For fuzzy date matching
    tier=TierConfig(is_pro=True),        # is_pro=True for Professional/Enterprise
)

# Result contains:
# - matched: list of matched transactions
# - differences: amount mismatches
# - unclaimed: money without corresponding order
# - unmatched_orders: orders without corresponding payment
# - summary: reconciliation summary
# - excel_path: path to exported Excel (if tier supports)

# Push to Feishu (Professional/Enterprise)
push_reconciliation_to_feishu(result, chat_id="oc_xxx")
```

## Supported Statement Formats

### Chinese Banks (CSV/Excel/PDF)
| Bank | Format | Key Columns |
|------|--------|-------------|
| 中国银行 (BOC) | CSV/Excel | 交易日期, 交易金额, 对方账户, 余额, 摘要 |
| 工商银行 (ICBC) | CSV/Excel | 日期, 金额, 对方户名, 余额, 摘要 |
| 建设银行 (CCB) | CSV/Excel | 交易时间, 交易金额, 对方账户, 余额, 备注 |
| 农业银行 (ABC) | CSV/Excel | 交易日期, 金额, 对方姓名, 余额, 用途 |

### Payment Platforms
| Platform | Format | Key Columns |
|----------|--------|-------------|
| 支付宝 | CSV | 交易时间, 对方, 金额, 状态, 说明 |
| 微信支付 | CSV | 交易时间, 交易类型, 交易金额, 交易对方, 备注 |
| PayPal | CSV/JSON | Date, Amount, Item, Status, Counterparty |
| Stripe | CSV/JSON | Date, Amount, Description, Customer, Currency |

### E-commerce
| Platform | Format | Key Columns |
|----------|--------|-------------|
| 亚马逊 | CSV/Excel | Order Date, Order ID, Order Status, Item Total, Payment |
| Shopify | CSV/Excel | Created, Name, Financial Status, Total, Source |
| Temu | CSV | Date, Order ID, Amount, Status, Payment Method |

## Matching Modes

### 1. Exact Matching (date + amount)
- Same date (±0 days) + same amount (exact)
- Best for: real-time payments, bank transfers

### 2. Fuzzy Matching (date range + amount tolerance)
- Date within ±N days + amount within ±X tolerance
- Configurable via `date_range_days` and `amount_tolerance`
- Best for: delayed settlements, batch payments

### 3. Semantic Matching (counterparty name)
- Uses AI to match counterparty names with fuzzy similarity
- Handles: "阿里巴巴" ↔ "阿里云计算", "张三" ↔ "张三（个人）"
- Requires: Professional tier or higher

## Tier Capabilities

| Feature | Free | Basic | Standard | Professional | Enterprise |
|---------|------|-------|----------|-------------|-----------|
| Monthly statements | 50 | 500 | 5,000 | Unlimited | Unlimited |
| Bank accounts | 1 | 3 | Unlimited | Unlimited | Unlimited |
| Output format | Text | Excel | Excel | Excel + JSON | Excel + JSON + API |
| Alipay/WeChat | ✗ | ✗ | ✓ | ✓ | ✓ |
| PayPal/Stripe | ✗ | ✗ | ✗ | ✓ | ✓ |
| Semantic matching | ✗ | ✗ | ✗ | ✓ | ✓ |
| Custom rules | ✗ | ✗ | ✗ | ✗ | ✓ |
| Feishu card | ✗ | ✗ | ✓ | ✓ | ✓ |
| Token prefix | BANK-FREE | BANK-BSC | BANK-STD | BANK-PRO | BANK-ENT |

## Difference Handling

Each discrepancy can be marked as:
- `已处理` (Processed) - manually resolved
- `待追款` (Pending collection) - amount owed
- `坏账` (Bad debt) - unrecoverable

## Excel Export Format

Exported Excel (`reconciliation_YYYYMMDD_HHMMSS.xlsx`) contains:
- **Sheet: 匹配结果** - Matched transactions
- **Sheet: 差异** - Amount differences
- **Sheet: 未认领** - Money without order (unclaimed)
- **Sheet: 未核销** - Order without payment (unmatched)
- **Sheet: 汇总** - Summary statistics

## Feishu Card Output

Professional/Enterprise tiers support Feishu interactive cards:

```json
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": {"tag": "plain_text", "content": "对账结果"},
      "template": "blue"
    },
    "elements": [
      {"tag": "div", "text": {"tag": "lark_md", "content": "**匹配率**: 95.2%"}},
      {"tag": "div", "text": {"tag": "lark_md", "content": "**已匹配**: 238 笔"}},
      {"tag": "div", "text": {"tag": "lark_md", "content": "**差异**: 8 笔 (¥12,345.00)"}},
      {"tag": "div", "text": {"tag": "lark_md", "content": "**未认领**: 3 笔 (¥5,600.00)"}},
      {"tag": "div", "text": {"tag": "lark_md", "content": "**未核销**: 12 笔 (¥45,000.00)"}}
    ]
  }
}
```

## Usage Examples

### Basic Reconciliation
```
User: 对账这个月的银行流水和订单
Agent: 
1. Upload bank statement CSV + order CSV
2. Call reconcile_bank_statements(...)
3. Return structured results
4. (Standard+) Push to Feishu
```

### Specific Bank
```
User: 对账中国银行的流水和发票
Agent:
1. statement_type="boc"
2. order_type="invoice"
3. Run reconciliation
4. Export Excel + Feishu card
```

### Fuzzy Match with Tolerance
```
User: 对账时金额容差0.1元，日期范围3天
Agent:
1. amount_tolerance=0.1
2. date_range_days=3
3. match_mode="fuzzy"
4. Return results
```

## Pricing & Token Validation

| Tier | Token Prefix | Plan ID |
|------|-------------|----------|
| Free | BANK-FREE | TBD (yk global backend) |
| Basic | BANK-BSC | TBD |
| Standard | BANK-STD | TBD |
| Professional | BANK-PRO | TBD |
| Enterprise | BANK-ENT | TBD |

Token validation checks token prefix against tier.

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `UNSUPPORTED_FORMAT` | File format not supported | Convert to CSV/Excel |
| `COLUMN_NOT_FOUND` | Required column missing | Check statement format |
| `AMOUNT_MISMATCH` | Amount parsing failed | Verify currency/decimal |
| `DATE_PARSE_ERROR` | Date format not recognized | Specify date format manually |
| `TIER_LIMIT_EXCEEDED` | Statement count exceeds tier | Upgrade or split files |
