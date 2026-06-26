# Database Schemas - AccountantPriv

## Hapoalim DB (`output/hapoalim.db`)

### `hapoalim_transactions`
Main transactions table for Bank Hapoalim.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| account_number | TEXT | Account: 12-602-492831 (securities) or 12-640-275682 (main) |
| date | TEXT | Transaction date (YYYY-MM-DD) |
| description | TEXT | Transaction description (Hebrew) |
| charged_amount | REAL | Amount (negative for debits, positive for credits) |
| category | TEXT | Transaction category (if available) |
| reference | TEXT | Reference number |
| status | TEXT | Transaction status |

### `hapoalim_balances`
Account balances snapshot.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| account_number | TEXT | Account number |
| date | TEXT | Balance date |
| balance | REAL | Account balance |

---

## Isracard DB (`output/isracard.db`)

### `isracard_transactions`
Credit card transactions with full enrichment (34 columns).

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| card_name | TEXT | Card: מסטרקארד, גולד - מסטרקארד, AMEX BLUE |
| date | TEXT | Purchase date (YYYY-MM-DD) |
| description | TEXT | Merchant/transaction description |
| billed_amount | REAL | Amount in NIS |
| billing_month | TEXT | When it hits the bank: YYYY-MM |
| category | TEXT | Enriched category (e.g., "Entertainment", "Food") |
| sub_category | TEXT | Sub-category |
| merchant_name | TEXT | Merchant name |
| merchant_address | TEXT | Merchant address (from API) |
| merchant_phone | TEXT | Merchant phone (from API) |
| payment_method | TEXT | Payment method |
| currency | TEXT | Currency code |
| original_amount | REAL | Original amount (if foreign currency) |
| exchange_rate | REAL | Exchange rate used |

**Key concept:** `billing_month` = purchase month + 1. March purchases appear in April bank statement.

---

## Max DB (`output/max.db`)

### `max_transactions`
Max credit card transactions.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| account_number | TEXT | Card account number |
| date | TEXT | Transaction date (YYYY-MM-DD) |
| description | TEXT | Transaction description |
| charged_amount | REAL | Amount (negative for debits) |
| category | TEXT | Category (if available) |

---

## Common Query Patterns

### Find merchant across all cards
```sql
-- Isracard
SELECT card_name, date, description, billed_amount, category 
FROM isracard_transactions 
WHERE description LIKE '%נטפליקס%' OR description LIKE '%netflix%'
ORDER BY date DESC;

-- Max
SELECT account_number, date, description, charged_amount 
FROM max_transactions 
WHERE description LIKE '%נטפליקס%' OR description LIKE '%netflix%'
ORDER BY date DESC;
```

### Monthly spending by category (Isracard)
```sql
SELECT category, SUM(billed_amount) as total 
FROM isracard_transactions 
WHERE billing_month = '2026-03'
GROUP BY category 
ORDER BY total DESC;
```

### Bank debits (excluding card bills)
```sql
SELECT date, description, charged_amount 
FROM hapoalim_transactions 
WHERE charged_amount < 0 
  AND description NOT LIKE '%ישראכרט%' 
  AND description NOT LIKE '%מסטרקרד%' 
  AND description NOT LIKE '%מקס%'
ORDER BY date DESC;
```

### Card bill amounts from bank
```sql
SELECT date, description, charged_amount 
FROM hapoalim_transactions 
WHERE description LIKE '%ישראכרט%' 
   OR description LIKE '%מסטרקרד%' 
   OR description LIKE '%מקס%'
ORDER BY date DESC;
```
