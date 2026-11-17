---
name: australia-gst-precheck
display_name: Australia GST Pre-Check
description: "Australia GST pre-check for cross-border sellers. Upload draft BAS data and platform statements to check six high-frequency error categories: rate & GST-free classification, registration threshold, low-value imported goods rules, channel/platform collection match, filing frequency, export evidence & price display — outputs a structured risk report. Trigger words: Australia GST pre-check, GST check, BAS pre-check, low-value imported goods."
category: productivity
version: 0.1.0
author: snow
allowed-tools: ""
---

# Australia GST Pre-Check

## Red Lines
- Pre-check only, never filing. Passing the pre-check ≠ compliance.
- Never generate official returns or registration documents.
- When information is insufficient, state "cannot determine" — do not guess.
- Do not request API keys, passwords, or network access.

## Step 1 — Information Collection
Collect in one pass: 1) sales channels (Amazon AU / eBay / own site); 2) Australia-connected sales for the last 12 months; 3) whether holding an ABN and GST registration; 4) product types (general goods / food / health); 5) typical order value (≤ A$1,000 vs above); 6) whether platforms collect GST on marketplace sales; 7) any goods exported out of Australia. If information is incomplete, pre-check with what is available and mark the missing items.

## Step 2 — Item-by-Item Pre-Check
Check against `references/rule-table.md` and `references/deadlines.md`:
A. Rate & classification: flat 10%; GST-free categories (basic food, health, medical, education, childcare) vs taxable — flag misclassification in mixed catalogs.
B. Registration threshold: A$75,000 GST turnover over 12 months; sales where the platform is the deemed supplier do NOT count toward the seller's own threshold — flag miscounting.
C. Low-value imported goods (LVIG): consignments ≤ A$1,000 → GST charged at checkout by the seller or the electronic distribution platform (EDP deemed supplier since 2018-07); consignments > A$1,000 → taxed at the border — flag charging GST at checkout on those (double taxation).
D. Channel match: marketplace (EDP collects) vs own website (seller collects once registered); ABN + GST registration needed for own-channel; simplified non-resident registration exists with limited input tax credits.
E. Frequency & deadlines: quarterly BAS is standard (due the 28th after quarter end; December quarter → February 28); monthly for large turnover (21st); annual only for voluntary small registrants.
F. Export & pricing: exports are GST-free but require export evidence within 60 days; consumer prices must be displayed GST-inclusive under Australian Consumer Law — flag ex-GST display.

## Step 3 — Report
Part 1 — Risk summary: 🔴 high risk / 🟡 needs attention / 🟢 no obvious high-frequency errors found (not a compliance conclusion).
Part 2 — Table: check item | finding | risk level | basis | recommended action. 🔴 = estimated correction cost >A$2,000 or ATO/ACL exposure; 🟡 = A$500–2,000; 🟢 = no anomaly found (not a compliance conclusion).
Part 3 — Next steps: 1–3 prioritized actions; where back-filing or registration is involved, note "confirm with your registered tax agent or BAS agent."

## Step 4 — Follow-Ups
Expand only on already-checked items. If asked to lodge a BAS or register, reply: "This skill performs pre-checks only and does not lodge or register. Please hand the report to your registered tax agent or BAS agent."

---
Series: cross-border tax pre-check (EU VAT: `eu-vat-precheck-en` · US: `us-sales-tax-precheck` · Japan: `japan-jct-precheck` · Australia: `australia-gst-precheck`).
