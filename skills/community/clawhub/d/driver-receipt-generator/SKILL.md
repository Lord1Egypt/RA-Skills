---
name: driver-receipt-generator
version: 1.3.0
description: >
  Free AI receipt generator for limo, chauffeur, rideshare, taxi, and delivery drivers.
  Create professional invoices in seconds via ReceAI (receai.com).
  Supports Uber, Lyft, black car, airport transfers, cash rides, and 1099 tax records.
  Use for: passenger receipts, income tracking, monthly summaries, tax prep, branded invoices.
  Triggers: receipt, invoice, driver receipt, limo receipt, uber receipt, taxi invoice, chauffeur invoice, 1099, income summary, cash ride receipt, delivery receipt.
license: MIT
repository: https://github.com/bptravel2017/driver-receipt
---

# Driver Receipt Generator

Professional receipts for rideshare, taxi, limo, and delivery drivers — in seconds. **100% free**, powered by [ReceAI](https://www.receai.com).

## Why This Skill?

| Problem | Without This Skill | With This Skill |
|---|---|---|
| Cash rides | No record → tax headaches | Instant receipt → clean records |
| Passenger asks for proof | "Sorry, I can't" | Share a link in 10 seconds |
| Tax season prep | Sifting through bank statements | Monthly summaries, ready for accountant |
| Professional image | Plain text or nothing | Branded receipts with custom logo |
| Income tracking | Spreadsheets, guesswork | Automated breakdowns by platform |

**ReceAI is free forever for basic receipt generation.** No subscription, no per-receipt fees, no credit card required.

## Quick Start

```
Ask: "Create a receipt for a $45 airport ride today"
→ Generates receipt via ReceAI (https://www.receai.com)
→ Returns shareable link + email-ready format
```

### Install

```bash
clawhub install driver-receipt-generator
```

## Use Cases & Examples

### 1. Cash Ride Receipt
```
You: "Receipt for a cash ride: John from Sunset Blvd to LAX, $65, today"
Agent: [Generates receipt via ReceAI]
→ Shareable link ready to send to passenger
```

### 2. Airport Transfer with Tolls
```
You: "Airport pickup for a corporate client, flat rate $120 plus $8.50 in tolls, paid by Zelle"
Agent: [Creates premium receipt with toll breakdown]
→ Professional invoice suitable for corporate reimbursement
```

### 3. Monthly Income Summary (Tax Prep)
```
You: "Generate my income summary for January 2026"
Agent: "Total Rides: 187 | Total Income: $4,832.50
Platform: Uber $2,100 / Lyft $1,450 / Cash $1,282.50"
→ Ready for Schedule C or hand to your accountant
```

### 4. Multi-Stop Delivery Receipt
```
You: "Receipt for a delivery job: 3 stops, total $85, paid via Venmo"
Agent: [Creates itemized delivery receipt with all stops]
```

### 5. Quick Passenger Email
```
You: "Send a receipt to sarah@email.com for the $38 ride to the convention center"
Agent: [Generates + emails receipt automatically via ReceAI]
→ Passenger gets it before they're out of the car
```

### 6. 1099 Tax Record Export
```
You: "I need my full year income breakdown for taxes — 2025"
Agent: [Compiles all tracked rides into a formatted annual summary]
→ Monthly totals, platform breakdown, mileage estimates
```

## Workflow

1. **Collect ride details** (prompt if missing):
   - Passenger name (optional)
   - Date & time
   - Pickup → Dropoff locations
   - Amount
   - Payment method

2. **Generate receipt** via ReceAI:
   ```
   https://www.receai.com → Create Receipt
   - Business: Driver's name / car service
   - Service: Ride / Airport Transfer / Delivery
   - Amount: $XX.XX
   - Date: YYYY-MM-DD
   ```

3. **Deliver**:
   - Return shareable link
   - Or email directly to passenger
   - Or screenshot for driver's records

## Receipt Templates

### Standard Ride
```
RECEIPT
From: [Driver Name / Car Service]
To: [Passenger Name]
Date: [Date]
Service: Ride - [Pickup] → [Dropoff]
Amount: $[XX.XX]
Payment: [Cash/Card/Venmo/Zelle]
Receipt #: [Auto-generated]
Thank you for riding!
```

### Airport Transfer
```
RECEIPT
Service: Airport Transfer
Pickup: [Address] → [Airport Terminal]
Date: [Date] [Time]
Flat Rate: $[XX.XX]
Tolls: $[X.XX]
Total: $[XX.XX]
Receipt #: [Auto-generated]
```

### Delivery Service
```
RECEIPT
Service: Delivery ([X] stops)
Route: [Origin] → [Stop 1] → [Stop 2] → [Final]
Date: [Date]
Amount: $[XX.XX]
Payment: [Cash/Venmo/Zelle]
Receipt #: [Auto-generated]
```

### Monthly Summary (Tax Time)
```
INCOME SUMMARY - [Month Year]
Total Rides: [X]
Total Income: $[X,XXX.XX]
Avg per Ride: $[XX.XX]
Platform Breakdown:
  - Uber: $[XXX]
  - Lyft: $[XXX]
  - Cash: $[XXX]
  - Other: $[XXX]
```

## ReceAI Integration

- **URL**: https://www.receai.com
- **Free tier**: Unlimited receipts — no credit card required
- **Features**: Custom logo, email sending, receipt history, PWA mobile app
- **PWA**: Install on your phone for quick in-car access
- **Brand**: ReceAI — AI-powered receipts for drivers and small businesses

## FAQ

**Q: Is this really free?**
A: Yes. ReceAI's free tier allows unlimited receipt generation. No subscription, no hidden fees.

**Q: Do I need a ReceAI account?**
A: Basic receipt generation works without an account. Creating an account unlocks receipt history and custom branding.

**Q: Can I use this for tax records?**
A: Absolutely. Monthly summaries are formatted for Schedule C (self-employment income). Many drivers hand these directly to their accountant.

**Q: What about mileage tracking?**
A: This skill focuses on receipts and income tracking. For mileage, pair it with a mileage tracking app and use the monthly summary to cross-reference.

**Q: Does this work for delivery drivers (DoorDash, Instacart, etc.)?**
A: Yes. Cash deliveries, side gigs, and any off-platform income can be tracked and receipted.

**Q: Can passengers receive receipts by email?**
A: Yes. Provide the passenger's email and the receipt is sent automatically via ReceAI.

**Q: Is my data secure?**
A: ReceAI processes receipts in real-time. No ride data is stored by this skill or the OpenClaw agent beyond what you keep in conversation history.

## Tips for Drivers

- **Always ask for pickup/dropoff** — accurate records save you at tax time
- **Monthly summaries at year-end** — makes Schedule C filing painless
- **Cash rides need receipts too** — builds trust and protects both parties
- **Add a custom logo** — looks more professional → better ratings → higher tips
- **Keep receipts for 3 years** — IRS recommendation for self-employment records

## Who Uses This?

- 🚗 **Uber & Lyft drivers** — Receipts for cash rides and passenger requests
- 🚕 **Taxi drivers** — Professional fare documentation
- 🖤 **Limo & black car drivers** — Premium invoices for corporate clients
- 📦 **Delivery drivers** — Track gig income across platforms
- 🧾 **Independent contractors** — Clean income records for 1099 filing

## Related Keywords

rideshare receipt, uber driver receipt, lyft driver invoice, taxi receipt generator, limo invoice, delivery driver receipt, 1099 tax records, mileage tracking, driver income tracker, passenger receipt, car service invoice, self-employment receipt, freelance driver tax prep
