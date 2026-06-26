---
summary:
  - Standard GL code mappings for common business expense categories
  - Includes QBO-compatible codes and IRS deductibility notes
  - Reference during GL mapping step of expense categorization
updated: 2026-03-15
---

# GL Code Mapping Reference

## Standard QBO Chart of Accounts — Expense Categories

| GL Code | Category | QBO Account Name | IRS Notes |
|---------|----------|-----------------|-----------|
| 6000 | Advertising | Advertising & Marketing | 100% deductible |
| 6010 | Marketing - Digital | Online Advertising | 100% deductible |
| 6050 | Auto - Gas | Auto & Truck Expenses | Actual method |
| 6060 | Auto - Repairs | Auto & Truck Expenses | Actual method |
| 6100 | Bank Charges | Bank Charges | 100% deductible |
| 6110 | Computer - Hardware | Computer & Technology | Section 179 eligible |
| 6120 | Computer - Software | Computer & Technology | May amortize |
| 6130 | Computer - Subscriptions | Software Subscriptions | 100% deductible |
| 6150 | Dues & Subscriptions | Dues & Subscriptions | 100% deductible |
| 6160 | Entertainment | Entertainment | 0% deductible (2018+) |
| 6170 | Equipment | Equipment Rental | 100% deductible |
| 6200 | Travel - Air | Travel Expenses | 100% deductible |
| 6205 | Travel - Hotel | Travel Expenses | 100% deductible |
| 6210 | Travel - Mileage | Travel Expenses | IRS rate × miles |
| 6215 | Travel - Rideshare | Travel Expenses | 100% deductible |
| 6220 | Travel - Parking | Travel Expenses | 100% deductible |
| 6230 | Meals - Business | Meals & Entertainment | 50% deductible |
| 6235 | Meals - Client | Meals & Entertainment | 50% deductible |
| 6240 | Office Supplies | Office Supplies | 100% deductible |
| 6250 | Postage & Shipping | Postage & Delivery | 100% deductible |
| 6260 | Professional Fees | Legal & Professional | 100% deductible |
| 6265 | Accounting | Legal & Professional | 100% deductible |
| 6270 | Insurance | Insurance Expense | 100% deductible |
| 6280 | Utilities | Utilities | 100% deductible |
| 6285 | Phone - Business | Telephone Expense | 100% deductible |
| 6290 | Internet | Telephone Expense | 100% deductible |
| 6300 | Rent | Rent or Lease | 100% deductible |
| 6310 | Repairs & Maintenance | Repairs & Maintenance | 100% deductible |
| 6320 | Taxes & Licenses | Taxes & Licenses | 100% deductible |
| 6330 | Training & Education | Training & Development | 100% deductible |
| 6340 | Contract Labor | Contract Labor | 1099 required >$600 |
| 6350 | Conference & Events | Conferences & Seminars | 100% deductible |
| 6360 | Books & Publications | Office Supplies | 100% deductible |
| 6370 | Gifts - Business | Business Gifts | $25/person/year max |
| 6380 | Home Office | Home Office Expense | Prorated |
| 6900 | Miscellaneous | Miscellaneous Expense | Requires documentation |

## Crypto/DeFi Expenses

| GL Code | Category | Notes |
|---------|----------|-------|
| 6400 | Gas Fees | Transaction costs, add to cost basis |
| 6410 | Exchange Fees | Trading fees, reduce proceeds |
| 6420 | Wallet Software | Software subscription |
| 6430 | Audit & Security | Professional fees |
| 6440 | Node Infrastructure | Computer/hosting |

## Common Vendor → Category Mapping

| Vendor Pattern | GL Code | Category |
|----------------|---------|----------|
| Delta, United, Southwest, American | 6200 | Travel - Air |
| Marriott, Hilton, Hyatt, IHG | 6205 | Travel - Hotel |
| Uber, Lyft, Taxi | 6215 | Travel - Rideshare |
| Expensify, Concur | 6130 | Software Subscriptions |
| Amazon (office supplies) | 6240 | Office Supplies |
| Amazon Web Services | 6120 | Computer - Software |
| Google Workspace, Microsoft 365 | 6130 | Software Subscriptions |
| Zoom, Slack, Notion | 6130 | Software Subscriptions |
| Staples, Office Depot | 6240 | Office Supplies |
| AT&T, Verizon, T-Mobile | 6285 | Phone - Business |
| Restaurant/café (meal keywords) | 6230 | Meals - Business |
| Doordash, Grubhub, Uber Eats | 6230 | Meals - Business |
| Starbucks, Panera | 6230 | Meals - Business |
| LinkedIn Premium | 6150 | Dues & Subscriptions |
| Continuing Ed providers | 6330 | Training & Education |
