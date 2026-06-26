# Receipt Scanner — Reference Guide

## Overview
Extract every data point from a receipt or invoice (image, photo, PDF, or scan), categorize the expense, flag tax deductibility, detect anomalies, support multi-receipt batching, and log to an expense CSV.

---

## Step 1 — Receipt Classification

Determine the receipt type before extracting fields:

| Receipt Type | Signals | Extra Fields to Extract |
|---|---|---|
| Retail / point-of-sale | Itemized list, barcode, store branding | Line items, quantity, unit price, discounts |
| Restaurant / food | "Table", "Server", "Gratuity", "Covers" | Tip %, server name, party size |
| Fuel / gas station | "Gallons/Litres", "Grade", pump number | Fuel type (Regular/Premium/Diesel), gallons/litres, price per unit |
| Hotel / accommodation | "Room rate", "Check-in/Check-out", folio | Room nights, daily rate, taxes by type |
| Travel (flight/train) | Ticket number, route, class | Origin, destination, travel class, booking reference |
| Taxi / rideshare | Pickup, dropoff, distance | Trip distance, surge multiplier, driver name |
| Invoice (B2B) | Invoice number, PO number, net terms | Invoice date, due date, line items, tax ID |
| Pharmacy | Rx number, NDC code | Drug name, quantity, prescription vs. OTC |
| Utilities | Account number, meter reading | kWh/units, service period, account number |
| Online order | Order number, tracking number | Shipping cost, items with SKUs, return policy date |
| Mileage / expense report | "Mileage", "km", "miles" | From/to, distance, rate per mile/km, purpose |

---

## Step 2 — Extract All Fields

Read the receipt visually or from PDF text layer. Extract every visible field:

### Core Fields (all receipt types)
| Field | Notes |
|---|---|
| Merchant name | Business name exactly as printed |
| Merchant address | Full address if shown |
| Merchant phone | If shown |
| Merchant website | If shown |
| Merchant tax/VAT ID | EIN, ABN, GST number — important for B2B expense claims |
| Receipt / Invoice number | Transaction ID, receipt #, invoice # |
| Date | Transaction date (not print date, not server time zone) |
| Time | HH:MM if shown |
| Items | Line items: description, quantity, unit price, line total |
| Discounts / promotions | Coupon codes, member discounts, loyalty discounts |
| Subtotal | Pre-tax amount |
| Tax breakdown | Each tax line separately: GST, PST, HST, VAT, service tax, etc. |
| Tip / gratuity | Amount and percentage if shown |
| Service charge | Automatic service charge (common in UK/Singapore) |
| Other fees | Delivery fee, packaging fee, surcharge |
| Total | Final amount charged |
| Amount tendered | Cash given (if cash transaction) |
| Change | If cash transaction |
| Payment method | Cash, card type, digital wallet |
| Card last 4 digits | If shown |
| Authorization code | If shown |
| Loyalty points | Points earned / balance |
| Currency | ISO code and symbol |
| Exchange rate | If foreign currency transaction |

### Derived Fields
| Field | How to Derive |
|---|---|
| Effective tax rate | `tax / subtotal × 100` |
| Tip percentage | `tip / subtotal × 100` |
| Total cost per item | `line_total / quantity` |
| Local currency equivalent | `amount × exchange_rate` (if foreign) |

---

## Step 3 — Handle Special Receipt Types

### Multi-Item Receipts
Extract every line item into a structured table:

| # | Item Description | Qty | Unit Price | Discount | Line Total |
|---|---|---|---|---|---|
| 1 | Latte (Large) | 1 | $6.50 | — | $6.50 |
| 2 | Blueberry Muffin | 1 | $3.75 | $0.50 (promo) | $3.25 |

### Fuel Receipts
| Field | Value |
|---|---|
| Fuel type | Regular Unleaded / Premium / Diesel / E85 |
| Volume | 12.4 gallons / 47.2 litres |
| Price per unit | $3.89/gallon |
| Pump number | 4 |
| Odometer reading | If shown |

### Hotel Folios
Break down by night and by charge type:

| Date | Description | Amount |
|---|---|---|
| Mar 14 | Room rate | $189.00 |
| Mar 14 | Resort fee | $35.00 |
| Mar 14 | Room tax (12.5%) | $28.00 |
| Mar 14 | In-room dining | $48.50 |
| Mar 15 | Room rate | $189.00 |
| ... | | |

### Mileage / Reimbursement Claims
| Field | Value |
|---|---|
| Date | |
| From | |
| To | |
| Purpose | |
| Distance | miles / km |
| Reimbursement rate | e.g., $0.67/mile (IRS 2024 rate) |
| Claimable amount | distance × rate |

### Foreign Currency Receipts
| Field | Value |
|---|---|
| Amount in local currency | e.g., ¥3,200 |
| Exchange rate used | e.g., 1 USD = 149.8 JPY |
| USD equivalent | $21.36 |
| Conversion fee | e.g., 3% foreign transaction fee |
| Total USD cost | $22.00 |

### Illegible / Damaged Receipts
For any field that cannot be read:
- Mark as `[UNREADABLE — faded/torn/blurred]`
- Note overall legibility: "Receipt is 85% legible; [UNREADABLE] fields marked"
- Suggest: "For tax purposes, note the unreadable fields and attach any confirmation email/bank record"

---

## Step 4 — Categorize the Expense

Assign primary category + subcategory using both merchant name and line items:

| Category | Subcategories |
|---|---|
| Food & Dining | Restaurants, Groceries, Coffee & Cafes, Bars & Alcohol, Food Delivery, Catering |
| Travel | Flights, Hotels & Lodging, Car Rental, Taxis & Rideshare, Parking, Fuel, Public Transit, Ferry/Boat, Toll Charges |
| Office & Supplies | Stationery, Printing & Copying, Postage & Courier, Furniture, Cleaning |
| Technology | Software & SaaS, Hardware, Phone & Internet, Cloud Services, Repairs & Maintenance |
| Professional Services | Legal, Accounting & Tax, Consulting, Recruiting & Staffing, Photography |
| Marketing & Advertising | Digital Ads, Print & Media, Design & Creative, Events & Trade Shows, PR & Influencer |
| Health & Medical | Doctor & Clinic, Pharmacy, Hospital, Insurance Premium, Gym & Wellness, Mental Health |
| Entertainment | Events & Tickets, Streaming, Books & Magazines, Games, Sports |
| Utilities | Electricity, Water, Gas, Waste Management, Internet & Phone (personal) |
| Education | Courses & Training, Books (professional), Conferences, Certifications & Exams |
| Retail & Shopping | Clothing, Electronics, Home Goods, Personal Care, Gifts |
| Facilities & Rent | Office Rent, Coworking Space, Storage Unit |
| Banking & Finance | Bank Fees, ATM, Wire Transfer, Currency Exchange |
| Government & Tax | Tax Payments, Permits & Licenses, Fines |
| Other | Miscellaneous — flag for manual review |

**Categorization priority:**
1. Line items (most reliable)
2. Merchant name pattern matching
3. Merchant category code (MCC) if visible
4. Contextual cues from the conversation

---

## Step 5 — Tax Deductibility Assessment

| Category | Deductibility | Notes |
|---|---|---|
| Technology / SaaS | 100% (business) | Confirm business-exclusive use |
| Cloud Services | 100% (business) | |
| Professional Services | 100% | Legal, accounting, consulting directly for business |
| Office & Supplies | 100% | Must be business use |
| Education (business) | 100% | Maintaining/improving current job skills |
| Business Travel | 100% | Transport, lodging for work trips |
| Business Meals | 50% | Must have business purpose; keep notes on who attended |
| Home Office (portion) | Partial | Calculated % of home costs |
| Vehicle / Fuel | Partial | Business use % or standard mileage rate |
| Phone / Internet | Partial | Business use % |
| Health Insurance (self-employed) | 100% | On Schedule 1 |
| Gym / Wellness | Usually 0% | Unless documented medical necessity |
| Personal groceries | 0% | |
| Entertainment (personal) | 0% | |
| Clothing | 0% | Unless uniform/required for work |

Always append: _"Confirm deductibility with your tax advisor. Rules vary by jurisdiction, business structure, and circumstance."_

---

## Step 6 — Anomaly Detection

Flag these issues on the receipt itself (before logging):

| Anomaly | Detection Rule |
|---|---|
| Arithmetic error | Recalculate: `sum(line items) + tax + tip` ≠ total |
| Tax rate unusual | Effective tax rate outside expected range for merchant location |
| Tip exceeds 30% | Flag as "unusually high — confirm" |
| Duplicate receipt | If logging to CSV, check if same merchant + date + amount already exists |
| Future date | Receipt date is after today |
| Year discrepancy | Receipt shows year that seems wrong (e.g., "2019" on a recent photo) |
| Currency mismatch | Merchant in one country, currency in another without FX line |
| Negative line item | Discount or return — note and include in subtotal |

---

## Step 7 — Output Format

```
## Receipt Scan

### Summary
| Field | Value |
|---|---|
| Merchant | Starbucks — 123 Main St, San Francisco, CA 94105 |
| Phone | (415) 555-0192 |
| Date | 2024-03-15 |
| Time | 09:42 AM |
| Receipt # | 00847 |
| Currency | USD |

### Line Items
| # | Item | Qty | Unit | Discount | Total |
|---|---|---|---|---|---|
| 1 | Venti Caramel Latte | 1 | $6.50 | — | $6.50 |
| 2 | Blueberry Muffin | 1 | $3.75 | — | $3.75 |

### Totals
| | Amount |
|---|---|
| Subtotal | $10.25 |
| Tax (8.5% SF sales tax) | $0.87 |
| Tip | $2.00 |
| **Total** | **$13.12** |
| Payment | Visa ••••4521 |
| Auth Code | 847321 |

### Categorization
- **Primary**: Food & Dining
- **Subcategory**: Coffee & Cafes

### Tax Deductibility
- **Deductibility**: Likely 50% deductible as a business meal if client or team was present
- **To claim**: Record who attended and the business purpose
- _Confirm with your tax advisor_

### Anomaly Checks
- Arithmetic: $10.25 + $0.87 + $2.00 = $13.12 ✓
- Tax rate: 8.5% — consistent with San Francisco sales tax ✓
- Tip: 19.5% — within normal range ✓
```

---

## Step 8 — Expense Logging

Use the expense logger script:
```bash
python skills/doc-process/scripts/expense_logger.py add \
  --date "2024-03-15" \
  --merchant "Starbucks" \
  --category "Food & Dining" \
  --subcategory "Coffee & Cafes" \
  --amount 13.12 \
  --tax 0.87 \
  --currency USD \
  --payment "Visa ••••4521" \
  --receipt-no "00847" \
  --file expenses.csv
```

If the user has not specified a file, use `expenses.csv` in the current directory. Create it if it doesn't exist.

### Batch Processing
If the user provides multiple receipts at once:
1. Process each receipt individually
2. Present a batch summary table at the end:

| # | Merchant | Date | Total | Category |
|---|---|---|---|---|
| 1 | Starbucks | 2024-03-15 | $13.12 | Food & Dining |
| 2 | Shell Gas | 2024-03-15 | $82.40 | Travel > Fuel |
| 3 | Marriott | 2024-03-14 | $224.00 | Travel > Hotels |
| **Batch Total** | | | **$319.52** | |

3. Ask: "Log all 3 to expenses.csv?"

---

## Step 9 — Follow Up

Offer:
- "Should I log this to your expense file (expenses.csv)?"
- "Want me to scan another receipt or process a batch?"
- "Would you like a summary of all logged expenses by category?"
- "Want me to flag this as a reimbursable business expense and generate a claim?"
- "Should I check if this matches your bank statement?"
