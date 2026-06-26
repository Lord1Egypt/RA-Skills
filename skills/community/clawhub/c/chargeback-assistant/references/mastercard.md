# Mastercard Dispute Reference

> Source: Mastercard Chargeback Guide and Transaction Processing Rules
> Mastercard dispute process: Cardholder → Issuing Bank → Mastercard Network → Acquiring Bank → Merchant

---

## Filing deadline
**120 days** from the transaction date or from the date you became aware of the problem.
For recurring billing disputes: 120 days from when the unauthorized charge posted.
For merchandise not received: 120 days from the promised delivery date.

Do not wait — the 120-day clock starts from the event, not from when you decide to act.

---

## Mastercard Reason Codes by Dispute Type

Mastercard uses a two-tier system: **Dispute Category** → **Reason Code**

### Fraud disputes
| Code | Name | Use when |
|---|---|---|
| **4837** | No Cardholder Authorization | Cardholder did not authorize the transaction |
| **4849** | Questionable Merchant Activity | Merchant engaged in fraud against cardholder |
| **4863** | Cardholder Does Not Recognize | Cardholder doesn't recognize the transaction |
| **4870** | Chip Liability Shift | Counterfeit card used at non-chip terminal |
| **4871** | Chip/PIN Liability Shift | Lost/stolen card used without PIN verification |

**Most common for consumers:** 4837 (unauthorized — card not present fraud)

---

### Authorization disputes
| Code | Name | Use when |
|---|---|---|
| **4808** | Authorization-Related Chargeback | Transaction processed without proper authorization |
| **4812** | Account Number Not on File | Card number not valid |

---

### Point of interaction errors
| Code | Name | Use when |
|---|---|---|
| **4831** | Transaction Amount Differs | Charged more than authorized amount |
| **4834** | Duplicate Processing | Same transaction charged twice |
| **4842** | Late Presentment | Transaction submitted past allowed timeframe |
| **4846** | Correct Transaction Currency | Charged in wrong currency |

**Most common for consumers:** 4831 (overcharge), 4834 (duplicate)

---

### Cardholder disputes
| Code | Name | Use when |
|---|---|---|
| **4853** | Cardholder Dispute | Broad category — goods/services not as described, not received, or cancelled recurring |
| **4854** | Cardholder Dispute — Not Elsewhere Classified | Disputes not covered by other codes |
| **4855** | Non-Receipt of Merchandise | Item never delivered |
| **4859** | Addendum, No-Show, or ATM Dispute | Services not rendered, hotel no-show, ATM error |
| **4860** | Credit Not Processed | Merchant promised refund, never delivered |

**Most common for consumers:** 4853 (general disputes, SNAD, cancelled recurring), 4855 (INR), 4860 (credit not processed)

---

## Evidence requirements by reason code

### 4837 — No Cardholder Authorization
Required:
- Signed statement from cardholder declaring they did not authorize the transaction
- Confirmation that cardholder's card was in their possession
Optional:
- Any fraud notification received from bank
- Evidence of account compromise (password change notification, etc.)

### 4853 — Cardholder Dispute (SNAD / Cancelled Recurring)
**For SNAD (not as described):**
- Original product listing / description
- Photos or documentation of what was actually received
- Evidence of attempt to return to merchant with merchant's response

**For cancelled recurring:**
- Written evidence of cancellation (email, chat transcript, confirmation page screenshot)
- Date cancellation was communicated to the merchant
- Bank statement showing charges continued after cancellation date

### 4855 — Non-Receipt of Merchandise
Required:
- Proof that goods were not received
- Expected delivery date has passed
- Evidence of attempt to resolve with merchant (email, chat, phone note)
Optional:
- Tracking showing non-shipment or failed delivery
- Merchant's shipping policy

### 4860 — Credit Not Processed
Required:
- Merchant's written promise of credit (email, chat log, return acceptance)
- Proof item was returned if applicable (tracking showing merchant receipt)
- Statement showing credit never appeared

---

## Mastercard dispute timeline

| Stage | Timeframe | What's happening |
|---|---|---|
| Filing | Day 0 | You submit dispute to your bank |
| Chargeback issued | 5–30 days | Your bank files with Mastercard |
| Merchant rebuttal | 45 days | Merchant may provide counter-evidence |
| Second chargeback | If needed | Your bank reviews and may re-file |
| Arbitration | If unresolved | Mastercard decides; $250–$500 fee to loser |
| Resolution | 45–90 days typical | Provisional credit becomes permanent or reversed |

---

## Mastercard-specific tips

- **ADC (Arbitration-Dispute-Chargeback) process:** Mastercard has moved most consumer disputes into a streamlined process. Your bank handles most of the technical classification.
- **4853 is broad by design:** When in doubt, your bank will likely file under 4853. Make sure your evidence is clear about which sub-type applies (SNAD vs. cancelled recurring vs. general non-performance).
- **Merchant contact requirement:** Required for most 4853 disputes. Your bank will ask for documentation. For 4837 (unauthorized), skip merchant contact — go straight to your bank.
- **Provisional credit:** Most Mastercard-issuing banks provide provisional credit within 5 business days. If denied, escalate to a supervisor and cite Reg E (for debit) or your cardholder agreement (for credit).
- **No minimum amount.** File regardless of the dollar amount — it's your right.
