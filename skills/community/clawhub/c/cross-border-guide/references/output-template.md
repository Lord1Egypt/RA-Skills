# Cross-Border Guide — Output Templates

Two formats: Market-Entry Plan (program scope) and Customs Troubleshooting Report (single shipment/incident). Never omit Assumptions or the broker-verification note.

---

## Format A — Market-Entry Plan

### 1. Executive Summary
- Markets covered, product, AOV, monthly volume
- Go/no-go gating items (compliance registrations, restricted-goods issues)
- Recommended Incoterm and carrier per market, one line each
- Landed cost headline: [market]: $X.XX per order all-in

### 2. Product & Classification
| Item | Value |
|---|---|
| Product description (customs-grade) | |
| HS code (6-digit) + destination extensions | |
| Classification rationale | |
| Ambiguity / binding ruling recommendation | |

### 3. Landed Cost Table (at actual AOV)
| Market | De minimis (duty / tax) | Duty rate & amount | VAT/GST | Brokerage/fees | Shipping | Total landed cost | % of AOV |
|---|---|---|---|---|---|---|---|

State valuation basis used per market (CIF/FOB) and the channel (courier vs. postal).

### 4. Tax & Incoterm Setup
- Per market: DDP or DDU/DAP, and why
- Registrations needed: IOSS / UK VAT / AU GST / other, with thresholds and who collects (seller vs. marketplace)
- Checkout behavior: what the customer sees and pays

### 5. Carrier Plan
| Lane | Carrier/class | Transit | Cost/order | DDP support | Tracking | Why |
|---|---|---|---|---|---|---|

Include restricted-goods confirmation per carrier.

### 6. Compliance Gates (non-customs)
Numbered list of regulatory requirements that block launch (Responsible Person, product notifications, labeling, battery certs), each with effort estimate and owner.

### 7. Documentation Pack Spec
Commercial invoice fields and consistency rules, packing list, certificates required, data-quality rules (description ↔ HS ↔ value alignment).

### 8. Returns Policy per Market
Refund-without-return threshold, local return hub (if any), return-to-sender economics.

### 9. Assumptions & Verification List
Numbered. Every rate, threshold, and classification that should be confirmed with a licensed customs broker or official tariff source before scaling.

---

## Format B — Customs Troubleshooting Report

### 1. Situation
Shipment details, destination, carrier/channel, declared values, days held, carrier/customs status message.

### 2. Root Cause Analysis
Ranked causes with evidence. Distinguish: documentation defects, valuation issues, classification issues, restricted/regulated goods, consignee non-response, random inspection.

### 3. Immediate Actions (today)
Numbered, each with owner and exact artifact to produce (e.g., corrected invoice with transaction value, UN3481 statement, broker authorization letter).

### 4. Expected Resolution Path
Timeline expectations, escalation contacts, abandonment/return decision point with costs.

### 5. Prevent Recurrence
Policy changes (valuation, carrier, Incoterm, documentation), each with cost/benefit one-liner.

### 6. Assumptions & Verification List
As in Format A.

---

### Formatting rules
- Currency in the seller's currency, converted rates dated.
- Every duty/tax figure shows its basis and source type (tariff schedule, calculator estimate, broker quote).
- Mark estimates "(est.)". Regulatory thresholds get a "verify current" tag — they change.
- Executive summary ≤120 words.
