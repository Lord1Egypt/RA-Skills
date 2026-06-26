# Bank Statement Analyzer — Reference Guide

## Overview
Parse any bank or credit card statement (PDF or CSV), categorize all transactions with global merchant patterns, detect subscriptions and anomalies, compute spending trends, identify tax candidates, and generate a comprehensive financial health report.

---

## Step 1 — Statement Ingestion

### For CSV files: run the parser script
```bash
python skills/doc-process/scripts/statement_parser.py --file statement.csv --output categorized.json
python skills/doc-process/scripts/report_generator.py --file categorized.json --type bank
```

### For PDF files: read manually
Extract the metadata block first:

| Field | Notes |
|---|---|
| Account holder name | |
| Bank / Institution | |
| Account type | Checking, Savings, Credit Card, Line of Credit |
| Account number | Last 4 digits only |
| Statement period | From → To date |
| Opening balance | |
| Closing balance | |
| Currency | ISO code |
| Credit limit | (credit cards only) |
| Minimum payment due | (credit cards only) |
| Payment due date | (credit cards only) |

Then extract every transaction:
- Date
- Description / Merchant name (exactly as printed)
- Debit amount (money out)
- Credit amount (money in)
- Running balance (if shown)
- Reference number (if shown)
- Foreign currency / exchange rate (if applicable)

---

## Step 2 — Transaction Categorization

Use merchant name pattern matching with the full global taxonomy. When the script is used, it applies 589+ patterns. For manual categorization:

### Tier 1 — Direct Merchant Match

| Merchant Pattern | Category | Subcategory |
|---|---|---|
| Netflix, Hulu, Disney+, HBO Max, Apple TV+, Prime Video | Entertainment | Streaming |
| Spotify, Apple Music, YouTube Music, Tidal, Deezer | Entertainment | Music |
| Amazon, AMZN, Shopify merchants | Retail & Shopping | Online Retail |
| Uber Eats, DoorDash, Grubhub, Deliveroo, Zomato, Swiggy | Food & Dining | Food Delivery |
| Starbucks, Dunkin', Tim Hortons, Costa, Pret a Manger | Food & Dining | Coffee & Cafes |
| McDonald's, Subway, KFC, Pizza Hut, Domino's | Food & Dining | Fast Food |
| Uber, Lyft, Grab, Ola, Gojek, Bolt | Travel | Rideshare |
| Airbnb, VRBO, Booking.com, Expedia, Hotels.com | Travel | Lodging |
| Delta, United, Southwest, Ryanair, Singapore Air | Travel | Flights |
| Shell, BP, Chevron, ExxonMobil, Total, Petron | Travel | Fuel |
| AWS, Google Cloud, Azure, DigitalOcean, Vercel | Technology | Cloud Services |
| GitHub, Notion, Figma, Slack, Zoom, Adobe, Canva | Technology | SaaS Tools |
| Apple, Google, Microsoft, Samsung | Technology | Hardware/Services |
| AT&T, Verizon, T-Mobile, Vodafone, Singtel, Optus | Utilities | Phone & Internet |
| PG&E, Con Edison, National Grid, SP Group | Utilities | Electricity |
| Whole Foods, Trader Joe's, Walmart, Tesco, Sainsbury's | Food & Dining | Groceries |
| CVS, Walgreens, Boots, Guardian | Health & Medical | Pharmacy |
| H&M, Zara, Uniqlo, Nike, Adidas, ASOS | Retail & Shopping | Clothing |

### Tier 2 — Description Pattern Match

| Pattern in Description | Category |
|---|---|
| SALARY, PAYROLL, DIRECT DEP, WAGES | Income > Employment |
| DIVIDEND, INTEREST, YIELD | Income > Investment |
| TRANSFER, ZELLE, VENMO, PAYPAL, WISE, REVOLUT | Transfers (neutral) |
| ATM WITHDRAWAL, CASH ADVANCE | Cash |
| REFUND, REVERSAL, CHARGEBACK, CREDIT ADJ | Refund / Credit |
| INSURANCE, PREMIUM, ASSURANCE | Health & Medical or Financial Services |
| RENT, LEASE PAYMENT, HOA | Facilities & Rent |
| MORTGAGE, LOAN PAYMENT, EMI | Financial Services > Debt Payments |
| IRS, HMRC, ATO, IRAS, CRA | Government / Tax |
| SUBSCRIPTION, RECURRING, RENEWAL | Flag for subscription detection |
| FOREIGN TRANSACTION, FX, FOREX | Travel > Foreign Transaction |

### Unknown Merchants
If a merchant cannot be categorized: assign "Other — Review Needed" and add to anomalies list.

---

## Step 3 — Spending Summary

Compute and present:

### Account Health Metrics
| Metric | Value | Interpretation |
|---|---|---|
| Total income (credits) | $X | All money in |
| Total spending (debits) | $X | All money out |
| Net change | $X | Income minus spending |
| Savings rate | X% | Net / Income × 100 |
| Avg daily spend | $X | Total debits / days in period |
| Avg transaction size | $X | Total debits / count of debit transactions |
| Largest single expense | $X (merchant, date) | |
| Most frequent merchant | Merchant (N transactions) | |
| Days with no spending | N days | |

**Savings rate benchmarks:**
- <10%: Below recommended — consider reviewing discretionary spend
- 10–20%: Moderate savings
- 20–30%: Good
- >30%: Excellent

### Spending by Category
| Category | Transactions | Total | % of Spend | vs. Last Month |
|---|---|---|---|---|

### Monthly Trend Table
| Month | Income | Spending | Net | Savings Rate |
|---|---|---|---|---|

---

## Step 4 — Subscription Detection

Identify every recurring charge:

**Detection criteria:**
1. Same merchant, same amount (±5%), recurring within consistent interval
2. Description contains "subscription", "recurring", "membership", "renewal", "annual"
3. Known subscription services (Netflix, Spotify, SaaS tools, gym, etc.)

**For each subscription found:**
| Service | Category | Amount | Frequency | Annual Cost | Last Charged | Status |
|---|---|---|---|---|---|---|
| Netflix | Entertainment | $15.99 | Monthly | $191.88 | 2024-03-01 | Active |

**Subscription health analysis:**
- Total monthly subscription spend
- Total annual subscription cost
- % of total spend that is subscriptions
- Flag subscriptions charged but unused based on merchant type (e.g., fitness apps alongside infrequent gym visits)
- Alert: subscriptions whose price has increased vs. prior period

---

## Step 5 — Anomaly Detection

Run all 7 anomaly checks:

| Check | Rule | Severity |
|---|---|---|
| **Large charge** | Amount > 3× category average or > $1,000 on unknown merchant | High |
| **Duplicate charge** | Same merchant + same amount within 7 days | High |
| **Micro/test charge** | Amount < $2.00 from an unknown or suspicious merchant | Medium (could be card testing fraud) |
| **Round number large** | Amount ≥ $500 and exact round number (no cents) from unknown merchant | Medium |
| **Same-day cluster** | 3+ transactions to same merchant on same day | Medium |
| **Foreign transaction** | Non-ASCII merchant name or explicit FX conversion | Low (informational) |
| **Orphan refund** | Credit/refund from a merchant with no corresponding debit in last 90 days | Medium |
| **Velocity spike** | Daily spending > 3× average daily spend | Medium |
| **Unusual hour** | Transaction timestamped between midnight and 5 AM local time (if time available) | Low |

For each anomaly:
| Date | Merchant | Amount | Issue | Recommended Action |
|---|---|---|---|---|

---

## Step 6 — Budget & Financial Health Analysis

If asked or if the statement spans 2+ months, add:

### Category Budget Check
Compare spending to common recommended budget percentages (50/30/20 rule):
| Category | Spent | % of Income | Recommended % | Status |
|---|---|---|---|---|
| Housing (rent/mortgage) | $X | X% | ≤30% | Over / Under |
| Food & Dining | $X | X% | ≤10–15% | Over / Under |
| Transport | $X | X% | ≤10–15% | Over / Under |
| Entertainment | $X | X% | ≤5–10% | Over / Under |
| Savings | $X | X% | ≥20% | Over / Under |

### Debt Payments
List all loan/credit payments detected:
| Creditor | Amount | Type | Est. APR (if inferable) |
|---|---|---|---|

### Cash Flow Projection
If 2+ months available: extrapolate next month's expected spend by category based on trend.

---

## Step 7 — Tax Deduction Candidates

| Date | Merchant | Category | Amount | Tax Note |
|---|---|---|---|---|
| 2024-03-05 | Adobe Creative | Technology | $54.99 | 100% deductible if business use |
| 2024-03-08 | United Airlines | Travel | $620.00 | 100% deductible if work travel |
| 2024-03-12 | Nobu Restaurant | Food & Dining | $180.00 | 50% deductible — note business purpose |

**Deductible categories and rules:**
| Category | Deductibility |
|---|---|
| Technology / SaaS | 100% business use |
| Professional Services | 100% |
| Office & Supplies | 100% |
| Education (professional) | 100% |
| Business Travel (transport, lodging) | 100% |
| Business Meals | 50% |
| Financial Services (business fees) | May be deductible |
| Health Insurance (self-employed) | 100% on Schedule 1 |

_Disclaimer: Confirm with your accountant. Rules vary by jurisdiction and business structure._

---

## Step 8 — Output Format

```
## Bank Statement Analysis

### Account Summary
| Field | Value |
|---|---|
| Institution | Chase Bank |
| Account | Checking ••••7823 |
| Period | Feb 1 – Feb 28, 2024 |
| Opening Balance | $4,250.00 |
| Closing Balance | $3,180.45 |
| Total Credits (Income) | $5,200.00 |
| Total Debits (Spending) | $6,269.55 |
| Net Change | -$1,069.55 |
| Savings Rate | -20.6% (spending exceeded income) |
| Avg Daily Spend | $223.91 |
| Largest Expense | $620.00 — United Airlines (Feb 22) |

---

### Monthly Trend
| Month | Credits | Debits | Net | Savings Rate |
|---|---|---|---|---|
| Jan 2024 | $5,200.00 | $4,880.00 | +$320.00 | 6.2% |
| Feb 2024 | $5,200.00 | $6,269.55 | -$1,069.55 | -20.6% |

---

### Spending by Category
| Category | Transactions | Total | % of Spend |
|---|---|---|---|
| Travel | 6 | $1,240.00 | 19.8% |
| Retail & Shopping | 9 | $834.20 | 13.3% |
| Food & Dining | 18 | $423.80 | 6.8% |
| Technology > SaaS | 8 | $187.50 | 3.0% |
| Utilities | 3 | $210.00 | 3.4% |
| Entertainment | 5 | $89.97 | 1.4% |
| Other — Review Needed | 4 | $310.00 | 4.9% |
| **TOTAL** | **53** | **$3,295.47** | 100% |

---

### Subscriptions Detected (6) — $142.97/month • $1,715.64/year
| Service | Frequency | Per Charge | Annual Cost | Last Charged |
|---|---|---|---|---|
| Adobe Creative Cloud | Monthly | $54.99 | $659.88 | Feb 1 |
| Gym Membership | Monthly | $49.00 | $588.00 | Feb 5 |
| Netflix | Monthly | $15.99 | $191.88 | Feb 1 |
| Spotify | Monthly | $10.99 | $131.88 | Feb 3 |
| Notion | Monthly | $8.00 | $96.00 | Feb 6 |
| GitHub Pro | Monthly | $4.00 | $48.00 | Feb 1 |

---

### Anomalies (3)
| Date | Merchant | Amount | Issue | Action |
|---|---|---|---|---|
| Feb 14 | AMZN Mktp | $389.00 | 4× larger than typical Amazon spend | Verify this purchase |
| Feb 19 | TRX*98234 | $75.00 | Unrecognized merchant; could not categorize | Identify or dispute if unrecognized |
| Feb 22 | Starbucks | $45.50 | Possible duplicate — same amount on Feb 20 | Check if this was charged twice |

---

### Tax Deduction Candidates
| Date | Merchant | Category | Amount | Note |
|---|---|---|---|---|
| Feb 1 | Adobe Creative Cloud | Software | $54.99 | 100% if business use |
| Feb 1 | GitHub Pro | Software | $4.00 | 100% if business use |
| Feb 6 | Notion | Software | $8.00 | 100% if business use |
| Feb 22 | United Airlines | Travel | $620.00 | 100% if work travel |
| Feb 25 | Business Lunch — Nobu | Meals | $180.00 | 50% deductible |

**Estimated deductible total: $866.99**

_Confirm with your accountant._
```

---

## Step 9 — Multi-Statement Comparison

If the user provides 2+ months of statements:
- Build a month-over-month comparison table for each category
- Highlight categories with >20% change
- Compute rolling average and flag months >1 standard deviation from the mean
- Show income stability (is income consistent or variable?)

---

## Step 10 — Follow Up

Offer:
- "Want me to export the full categorized transaction list as CSV?"
- "Should I compare with last month's statement if you share it?"
- "Want a report formatted for your accountant (tax deductions + subscriptions summary)?"
- "Should I investigate any of the flagged anomalies further?"
- "Want a 3-month spending trend analysis?"
- "Should I set up a budget comparison against the 50/30/20 rule?"
