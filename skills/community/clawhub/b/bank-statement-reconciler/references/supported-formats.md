# Bank Statement Format Reference

## Chinese Banks

### 中国银行 (Bank of China - BOC)
**File types:** CSV, Excel (.xls/.xlsx)

| Column | Chinese Name | Description |
|--------|-------------|-------------|
| 交易日期 | Transaction Date | Format: YYYY-MM-DD |
| 交易金额 | Transaction Amount | Positive=income, Negative=expense |
| 对方账户 | Counterparty Account | Account number |
| 余额 | Balance | Account balance |
| 摘要 | Summary/Description | Transaction description |

### 工商银行 (ICBC)
**File types:** CSV, Excel

| Column | Chinese Name | Description |
|--------|-------------|-------------|
| 日期 | Date | YYYY-MM-DD |
| 金额 | Amount | Transaction amount |
| 对方户名 | Counterparty Name | Account holder name |
| 对方账户 | Counterparty Account | Account number |
| 余额 | Balance | Remaining balance |

### 建设银行 (CCB)
**File types:** CSV, Excel

| Column | Chinese Name | Description |
|--------|-------------|-------------|
| 交易时间 | Transaction Time | YYYY-MM-DD HH:MM:SS |
| 交易金额 | Transaction Amount | Net amount |
| 对方账户 | Counterparty | Account/Counterparty |
| 余额 | Balance | Account balance |

### 农业银行 (ABC)
**File types:** CSV, Excel

| Column | Chinese Name | Description |
|--------|-------------|-------------|
| 交易日期 | Transaction Date | YYYY-MM-DD |
| 金额 | Amount | Transaction amount |
| 对方姓名 | Counterparty Name | Person name |
| 余额 | Balance | Remaining balance |
| 用途 | Purpose | Transaction purpose |

---

## Payment Platforms

### 支付宝 (Alipay)
**File types:** CSV

| Column | Description |
|--------|-------------|
| 交易时间 | Transaction time |
| 交易对方 | Counterparty |
| 金额 | Amount |
| 状态 | Status (成功/失败) |
| 说明 | Description |

### 微信支付 (WeChat Pay)
**File types:** CSV

| Column | Description |
|--------|-------------|
| 交易时间 | Transaction time |
| 交易类型 | Transaction type |
| 交易金额 | Amount |
| 交易对方 | Counterparty |
| 备注 | Note |

### PayPal
**File types:** CSV, JSON

| Column | Description |
|--------|-------------|
| Date | Transaction date |
| Name | Counterparty name |
| Type | Transaction type |
| Status | Completed/Pending/etc |
| Amount | Transaction amount |
| Currency | Currency code |

### Stripe
**File types:** CSV, JSON

| Column | Description |
|--------|-------------|
| Created | Creation date |
| Description | Transaction description |
| Amount | Amount (in cents) |
| Currency | Currency code |
| Customer | Customer identifier |
| Status | Payment status |

---

## E-commerce Platforms

### 亚马逊 (Amazon)
**File types:** CSV, Excel

| Column | Description |
|--------|-------------|
| Order Date | Date order was placed |
| Order ID | Unique order identifier |
| Order Status | Order status |
| Item Total | Total item amount |
| Payment | Payment method |

### Shopify
**File types:** CSV, Excel

| Column | Description |
|--------|-------------|
| Created | Order creation date |
| Name | Order name (#1001) |
| Financial Status | Paid/Unpaid/Refunded |
| Fulfillment Status | Fulfilled/Unfulfilled |
| Total | Order total |

### Temu
**File types:** CSV

| Column | Description |
|--------|-------------|
| Date | Order date |
| Order ID | Order identifier |
| Amount | Order amount |
| Status | Order status |
| Payment Method | Payment used |

---

## Common Date Formats

| Format | Example |
|--------|---------|
| YYYY-MM-DD | 2024-01-15 |
| YYYY/MM/DD | 2024/01/15 |
| YYYYMMDD | 20240115 |
| YYYY年MM月DD日 | 2024年1月15日 |
| MM/DD/YYYY | 01/15/2024 |
| DD/MM/YYYY | 15/01/2024 |

## Common Amount Formats

| Format | Example |
|--------|---------|
| Plain number | 1000.00 |
| With comma | 1,000.00 |
| With currency | ¥1000.00 |
| With currency | $1000.00 |
| Negative (parentheses) | (100.00) |
| Negative (minus) | -100.00 |
