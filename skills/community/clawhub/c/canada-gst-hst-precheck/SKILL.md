---
name: canada-gst-hst-precheck
display_name: Canada GST/HST Pre-Check
description: "Canada GST/HST pre-check for cross-border sellers. Upload draft sales data and platform statements to check six high-frequency error categories: rate & province mapping, registration threshold, marketplace/DPO coverage, QST & PST separate regimes, filing frequency, currency & invoices — outputs a structured risk report. Trigger words: Canada GST HST pre-check, Canada sales tax, QST check, cross-border Canada tax."
category: productivity
version: 0.1.0
author: snow
allowed-tools: ""
---

# Canada GST/HST Pre-Check

## Red Lines
- Pre-check only, never filing. Passing the pre-check ≠ compliance.
- Never generate official returns or registration documents.
- When information is insufficient, state "cannot determine" — do not guess. Items marked "verify" in references must not be asserted without user-provided confirmation.
- Do not request API keys, passwords, or network access.

## Step 1 — Information Collection
Collect in one pass: 1) provinces sold into + rough annual sales; 2) sales channels (Amazon.ca / Walmart.ca / Shopify own site / others); 3) worldwide taxable sales over the last four calendar quarters; 4) current registrations (GST/HST, QST, provincial PST); 5) inventory in Canadian fulfillment warehouses (FBA/3PL); 6) customer type (B2C / includes B2B / unsure); 7) whether platforms collect tax on marketplace sales. If information is incomplete, pre-check with what is available and mark the missing items.

## Step 2 — Item-by-Item Pre-Check
Check against `references/rule-table.md` and `references/deadlines.md`:
A. Rate & province mapping: GST 5% vs HST by delivery province (ON 13%; NB/NL/PEI 15%; NS 14% [verify]); PST/QST charged separately where applicable — flag charging 5% GST where HST applies.
B. Registration threshold: small-supplier rule — worldwide taxable sales ≤ C$30,000 over four calendar quarters; crossing without registering → finding.
C. Marketplace/DPO coverage: since 2021-07, distribution platform operators are deemed suppliers for sales by non-registered vendors (and for fulfillment-warehouse sales); flag treating own-site sales as platform-covered once registered/over threshold.
D. QST & PST regimes: Quebec QST 9.975% is a separate registration with Revenu Québec; BC/SK/MB PST obligations for vendors and marketplace facilitators — flag assuming GST/HST registration covers these.
E. Frequency & deadlines: annual (≤C$1.5M), quarterly (≤C$6M), monthly (above); monthly/quarterly due 1 month after period end; annual due 3 months after fiscal year end (payment timing for individuals differs — flag).
F. Currency & invoices: prices and conversion in CAD at time of supply; GST/HST registration number on B2B invoices for input tax credits — flag missing numbers on B2B sales.

## Step 3 — Report
Part 1 — Risk summary: 🔴 high risk / 🟡 needs attention / 🟢 no obvious high-frequency errors found (not a compliance conclusion).
Part 2 — Table: check item | finding | risk level | basis | recommended action. 🔴 = estimated correction cost >C$2,000 or audit/registration exposure; 🟡 = C$500–2,000; 🟢 = no anomaly found (not a compliance conclusion).
Part 3 — Next steps: 1–3 prioritized actions; where back-filing or registration is involved, note "confirm with your Canadian tax advisor."

## Step 4 — Follow-Ups
Expand only on already-checked items. If asked to file returns or register, reply: "This skill performs pre-checks only and does not file or register. Please hand the report to your tax advisor."

---
Series: cross-border tax pre-check (EU `eu-vat-precheck-en` · US `us-sales-tax-precheck` · Japan `japan-jct-precheck` · Australia `australia-gst-precheck` · SEA `southeast-asia-vat-precheck` · Canada `canada-gst-hst-precheck` · Middle East `middle-east-vat-precheck` · Mexico `mexico-vat-precheck` · Korea `korea-vat-precheck`).
