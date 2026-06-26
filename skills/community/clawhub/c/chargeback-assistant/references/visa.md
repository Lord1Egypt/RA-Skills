# Visa Dispute Reference

> Source: Visa Core Rules and Visa Product and Service Rules
> Visa dispute process: Cardholder → Issuing Bank → Visa Network → Acquiring Bank → Merchant

---

## Filing deadline
**120 days** from the transaction date, OR 120 days from the expected delivery date for INR disputes, OR 120 days from when you became aware of the problem — whichever is latest. Maximum 540 days from the original transaction date in any case.

This is one of the longer windows. Do not delay — acquirers can request extensions that eat into this.

---

## Visa Reason Codes by Dispute Type

### Unauthorized transactions
| Code | Name | Use when |
|---|---|---|
| **10.1** | EMV Liability Shift — Counterfeit Fraud | Card was chip-enabled, merchant processed mag stripe only |
| **10.2** | EMV Liability Shift — Lost/Stolen Fraud | Card was chip-enabled, merchant processed without chip |
| **10.3** | Other Fraud — Card Present | In-person fraudulent transaction (non-EMV) |
| **10.4** | Other Fraud — Card Absent | Online/phone transaction cardholder did not authorize |
| **10.5** | Visa Fraud Monitoring Program | Used by Visa internally; not filed by cardholder |

**Most common for consumers:** 10.4 (unauthorized card-not-present transaction — e.g., someone used your card number online)

---

### Processing errors
| Code | Name | Use when |
|---|---|---|
| **12.1** | Late Presentment | Merchant submitted transaction more than 30 days after processing |
| **12.2** | Incorrect Transaction Code | Transaction coded incorrectly (e.g., credit processed as debit) |
| **12.3** | Incorrect Currency | Charged in different currency than agreed |
| **12.4** | Incorrect Account Number | Transaction posted to wrong account |
| **12.5** | Incorrect Amount | Amount charged differs from what you authorized |
| **12.6** | Duplicate Processing | Same transaction processed more than once |
| **12.7** | Invalid Data | Missing or invalid transaction data |

**Most common for consumers:** 12.5 (overcharge), 12.6 (duplicate charge)

---

### Consumer disputes
| Code | Name | Use when |
|---|---|---|
| **13.1** | Merchandise / Services Not Received | Paid, goods or services never delivered |
| **13.2** | Cancelled Recurring | Merchant continued charging after documented cancellation |
| **13.3** | Not as Described or Defective Merchandise | Item received but materially different from description |
| **13.4** | Counterfeit Merchandise | Item received is counterfeit |
| **13.5** | Misrepresentation | Merchant materially misrepresented the transaction |
| **13.6** | Credit Not Processed | Merchant promised refund, never issued it |
| **13.7** | Cancelled Merchandise / Services | Merchant cancelled, cardholder not refunded |
| **13.8** | Original Credit Transaction Not Accepted | N/A for most consumers |
| **13.9** | Non-Receipt of Cash or Load Transaction Value | ATM dispensed incorrect amount |

**Most common for consumers:** 13.1 (INR), 13.2 (subscription), 13.3 (SNAD), 13.6 (credit not processed)

---

## Evidence requirements by reason code

### 10.4 — Unauthorized card-not-present
Required:
- Cardholder's statement that they did not make the transaction
- Confirmation the card was in cardholder's possession at time of transaction
- Any fraud alerts received from the bank
Optional but helpful:
- Evidence of other unauthorized charges in same timeframe
- Police report if identity theft involved

### 13.1 — Merchandise / Services Not Received
Required:
- Proof that goods/services were not received
- Evidence that the expected delivery date has passed
- Documentation of attempt to resolve with merchant
- Tracking information showing non-delivery (or absence of tracking)
Optional but helpful:
- Merchant's terms showing delivery promise
- Shipping carrier confirmation of non-delivery

### 13.2 — Cancelled Recurring
Required:
- Evidence of cancellation (email, screenshot, confirmation number)
- Date cancellation was communicated to merchant
- Evidence that charges continued after cancellation date
Optional but helpful:
- Merchant's own cancellation policy
- All charges posted after cancellation date

### 13.3 — Not as Described or Defective
Required:
- Original item description / listing (screenshot or saved copy)
- Photos of item received showing discrepancy
- Evidence of attempt to return or resolve (merchant response or lack thereof)
Optional but helpful:
- Expert opinion for high-value items
- Shipping records showing return attempt

### 13.6 — Credit Not Processed
Required:
- Written documentation of merchant's refund promise (email, chat log)
- Proof of returned item if applicable (tracking showing delivery to merchant)
- Evidence that credit never appeared on statement (bank statement screenshot)

---

## Visa dispute timeline (what happens after you file)

| Stage | Timeframe | What's happening |
|---|---|---|
| Provisional credit | 5–10 business days | Your bank typically credits the amount while investigating |
| Chargeback filed | Within 30 days of your filing | Your bank submits the dispute to Visa |
| Merchant response | Up to 30 days | Merchant can accept or provide rebuttal evidence |
| Pre-arbitration | If merchant disputes | Your bank reviews merchant response |
| Arbitration | If unresolved | Visa makes final binding decision; $500 fee to losing party |
| Resolution | 45–90 days total typical | Provisional credit becomes permanent or is reversed |

---

## Visa-specific tips

- **Pre-dispute requirement:** Visa requires you to attempt resolution with the merchant first for most consumer dispute codes (13.x). Document this attempt — date, method (email/phone), and merchant's response.
- **Unauthorized charges (10.x):** No merchant contact required — go straight to your bank.
- **For subscription disputes (13.2):** Visa requires that the cancellation was communicated to the merchant per their stated cancellation process. If you cancelled through the wrong channel, this weakens your case.
- **Amount:** No minimum dispute amount. No maximum.
- **Provisional credit:** Most Visa-issuing banks provide provisional credit within a few business days of filing. If yours doesn't, ask for it explicitly — you're entitled to it during the investigation.
