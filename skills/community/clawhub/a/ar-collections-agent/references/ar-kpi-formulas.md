# AR KPI Formulas Reference

## Days Sales Outstanding (DSO)

**Purpose:** How many days on average to collect payment after a sale.

```
DSO = (Accounts Receivable Balance / Total Credit Sales) × Number of Days in Period
```

**Example:**
- AR Balance: $120,000
- Credit Sales (last 90 days): $360,000
- DSO = (120,000 / 360,000) × 90 = **30 days**

**Benchmarks:**
- Excellent: < 30 days
- Good: 30–45 days
- Concerning: 45–60 days
- Poor: > 60 days

---

## Best Possible DSO (BPDSO)

**Purpose:** DSO if all current (not overdue) invoices were the only AR.

```
BPDSO = (Current AR / Total Credit Sales) × Number of Days in Period
```

**Spread = DSO − BPDSO** → measures collection inefficiency from overdue accounts.

---

## Collection Effectiveness Index (CEI)

**Purpose:** % of collectible AR actually collected in a period. 100% = perfect.

```
CEI = [(Beginning AR + Credit Sales − Ending AR) / (Beginning AR + Credit Sales − Current Ending AR)] × 100
```

**Example:**
- Beginning AR: $100,000
- Credit Sales: $200,000
- Ending AR: $80,000
- Current (not overdue) Ending AR: $50,000

CEI = [(100k + 200k − 80k) / (100k + 200k − 50k)] × 100  
    = [220k / 250k] × 100  
    = **88%**

**Benchmarks:** > 80% good; > 90% excellent.

---

## AR Turnover Ratio

**Purpose:** How many times AR is collected and refreshed in a period.

```
AR Turnover = Net Credit Sales / Average Accounts Receivable
Average AR = (Beginning AR + Ending AR) / 2
```

**Higher = faster collections.**

---

## Bad Debt Percentage

**Purpose:** % of credit sales written off as uncollectible.

```
Bad Debt % = (Bad Debt Write-offs / Total Credit Sales) × 100
```

**Industry benchmarks vary widely.** For professional services: < 1% is excellent; 2–3% is acceptable.

---

## Allowance for Doubtful Accounts (ADA) — Aging Method

Apply reserve percentages to each aging bucket:

```
ADA = Σ (Bucket Balance × Reserve %)
```

Journal Entry:
```
DR  Bad Debt Expense        $X
  CR  Allowance for Doubtful Accounts   $X
```

Write-off:
```
DR  Allowance for Doubtful Accounts   $X
  CR  Accounts Receivable             $X
```

Recovery (if later paid):
```
DR  Accounts Receivable    $X
  CR  Allowance for Doubtful Accounts  $X

DR  Cash                   $X
  CR  Accounts Receivable             $X
```

---

## AR Aging Bucket Summary Table Template

| Customer | Current | 1–30 | 31–60 | 61–90 | 91–120 | 120+ | Total | Risk Score |
|----------|---------|------|-------|-------|--------|------|-------|------------|
| Acme Co  | 5,000   | 0    | 2,500 | 0     | 1,200  | 0    | 8,700 | 6.2 |
| ...      | ...     | ...  | ...   | ...   | ...    | ...  | ...   | ... |
| **Total**| **X**   | **X**| **X** | **X** | **X**  | **X**| **X** | — |

Include % of total in each bucket row.
