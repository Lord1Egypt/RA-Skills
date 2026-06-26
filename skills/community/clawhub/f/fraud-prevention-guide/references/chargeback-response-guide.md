# Chargeback Response Guide

Reference for card-network-specific representment procedures, evidence requirements, and timeline management.

## Card Network Response Windows

| Network | Response Deadline | Pre-Arbitration Deadline | Arbitration Deadline |
|---|---|---|---|
| Visa (Visa Resolve Online) | 30 calendar days | 30 calendar days | 10 business days |
| Mastercard (Mastercom) | 45 calendar days | 45 calendar days | 45 calendar days |
| American Express | 20 calendar days | N/A (single cycle) | N/A |
| Discover | 30 calendar days | 30 calendar days | Review-based |

## Visa Reason Codes & Evidence Requirements

### 10.4 — Fraud / Card-Absent Environment

**Required Evidence:**
- Proof that the cardholder participated in the transaction (device fingerprint, account login records)
- AVS match confirmation and CVV verification result
- IP address with geolocation data showing proximity to billing address
- Transaction history showing prior undisputed purchases from same device or account

**Compelling Evidence (improves win rate):**
- Delivery confirmation to the cardholder's verified address with signature
- Communication logs (emails, chat) between merchant and cardholder
- Photos of delivered package matching the cardholder's address
- Evidence that the cardholder used the product (login after delivery, activation records)

**Expected Win Rate:** 30-45% with full evidence package

### 13.1 — Merchandise / Services Not Received

**Required Evidence:**
- Carrier tracking number with delivery confirmation
- Proof of delivery to the address provided by the cardholder
- Shipping policy as agreed to by the cardholder at checkout

**Compelling Evidence:**
- Signed delivery receipt or delivery photo with GPS coordinates
- Subsequent communication from the cardholder acknowledging receipt
- Evidence of product usage post-delivery (account activity, product registration)
- Insurance claim records if package was lost in transit

**Expected Win Rate:** 60-75% with delivery confirmation

### 13.3 — Not as Described or Defective

**Required Evidence:**
- Product description as displayed at time of purchase (screenshot with timestamp)
- Terms and conditions accepted by cardholder including return/refund policy
- Communication logs showing any complaints and merchant response
- Evidence that product matched the description

**Compelling Evidence:**
- Quality inspection records or certifications
- Photos of actual product shipped vs. listing photos showing match
- Return shipping label offered but not used by cardholder
- Other customer reviews confirming product quality

**Expected Win Rate:** 40-55% depending on documentation quality

## Mastercard Reason Codes

### 4837 — No Cardholder Authorization

**Required Evidence:**
- Transaction receipt with cardholder name, card number (last 4), and authorization code
- AVS and CVV verification results
- 3DS authentication record if available
- Device identification data

**Expected Win Rate:** 25-40%

### 4855 — Goods or Services Not Provided

**Required Evidence:**
- Proof of delivery (tracking with carrier confirmation)
- Description of goods/services and delivery method
- Communication with cardholder regarding delivery

**Expected Win Rate:** 55-70%

## Evidence Collection Automation

### Required Data Points to Capture at Transaction Time

1. **Device data:** Browser fingerprint, OS, screen resolution, timezone, language settings
2. **Network data:** IP address, ISP, proxy/VPN detection result, geolocation
3. **Behavioral data:** Session duration, pages viewed, mouse movement patterns, form fill timing
4. **Account data:** Account age, purchase history, login method, device consistency
5. **Transaction data:** Full AVS response, CVV response, 3DS authentication result, BIN country
6. **Fulfillment data:** Carrier, tracking number, delivery confirmation, signature record, delivery photos

### Evidence Letter Template Structure

```
Re: Chargeback Case [Case Number]
Card Network: [Network]
Reason Code: [Code] — [Description]
Transaction Date: [Date]
Transaction Amount: [Amount]
ARN/Reference: [Number]

Dear Dispute Resolution Team,

We are submitting this representment to demonstrate that the transaction 
was legitimate and the chargeback is not warranted.

[SECTION 1: Transaction Legitimacy]
[Insert relevant evidence of cardholder participation]

[SECTION 2: Product/Service Delivery]
[Insert delivery confirmation and fulfillment evidence]

[SECTION 3: Customer Communication]
[Insert relevant communication logs]

[SECTION 4: Supporting Documentation]
[List all attached evidence documents]

Based on the evidence provided, we respectfully request that this 
chargeback be reversed in our favor.
```

## Chargeback Rate Management

### Visa Chargeback Monitoring Program (VCMP)

| Tier | Threshold | Consequences | Actions Required |
|---|---|---|---|
| Standard | < 0.65% and < 75 disputes | Normal processing | Ongoing monitoring |
| Early Warning | 0.65-0.89% or 75-99 disputes | Notification only | Implement remediation plan |
| Excessive | 0.9-1.79% or 100-999 disputes | Monthly fines ($50-$25K) | Mandatory fraud review |
| High Excessive | ≥ 1.8% or ≥ 1000 disputes | Higher fines, potential termination | Immediate remediation required |

### Mastercard Excessive Chargeback Program (ECP)

| Tier | Threshold | Consequences |
|---|---|---|
| Standard | < 1.0% and < 100 disputes | Normal processing |
| Excessive Chargeback Merchant | ≥ 1.0% and ≥ 100 disputes for 2+ months | Fines starting month 5 |
| High Excessive | ≥ 1.5% and ≥ 200 disputes | Immediate fines, potential termination |
