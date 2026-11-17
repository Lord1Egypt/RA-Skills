---
name: eu-vat-precheck-en
display_name: EU VAT Return Pre-Check
description: "EU VAT return pre-check. Upload a draft return and platform statements to check six high-frequency error categories: tax rate, place of supply, OSS/IOSS, B2B/B2C, filing frequency, currency — outputs a structured risk report. Trigger words: VAT pre-check, VAT return check, EU VAT."
category: productivity
version: 0.2.0
author: snow
allowed-tools: ""
---

# EU VAT Return Pre-Check

## Red Lines
- Pre-check only, never filing. Passing the pre-check ≠ compliance.
- Never generate official filing documents.
- When information is insufficient, state "cannot determine" — do not guess.
- Do not request API keys, passwords, or network access.

## Step 1 — Information Collection
Collect in one pass: 1) filing country (DE/FR/IT/ES/UK/other EU); 2) frequency (monthly/quarterly/annual); 3) key return fields (sales, output tax, input tax, rate); 4) platform statements (per-platform sales, withheld VAT); 5) OSS/IOSS registration status; 6) customer type (B2C/B2B/unsure); 7) any intra-EU stock transfers (e.g. FBA cross-border movements). If information is incomplete, pre-check with what is available and mark the missing items.

## Step 2 — Item-by-Item Pre-Check
Check against `references/rule-table.md` and `references/deadlines.md`:
A. Rate: does the declared rate equal the country's standard rate; is cross-border B2C wrongly using a domestic rate.
B. Place of supply: the EU-wide €10,000/year threshold applies only to sellers established in a single EU member state — flag if crossed without switching; non-EU sellers are taxed at the destination country from the first sale — flag if wrongly declared under the domestic place of supply.
C. OSS/IOSS: cross-border B2C without OSS registration → high risk; IOSS applies only to imported consignments ≤ €150 — flag misuse above the threshold.
D. B2B/B2C: misclassification either way; business customers present but no VAT numbers collected → flag.
E. Frequency: complies with the country's statutory rules; deadline proximity.
F. Currency: platform settlement rate used instead of the ECB rate at the tax point; multi-currency amounts not uniformly converted.

## Step 3 — Report
Part 1 — Risk summary: 🔴 high risk / 🟡 needs attention / 🟢 no obvious high-frequency errors found (not a compliance conclusion).
Part 2 — Table: check item | finding | risk level | basis | recommended action. 🔴 = correction cost >€2,000 or possible account freeze; 🟡 = €500–2,000; 🟢 = no anomaly found (not a compliance conclusion).
Part 3 — Next steps: 1–3 prioritized actions; where supplementary filing or registration is involved, note "confirm with your tax representative."

## Step 4 — Follow-Ups
Expand only on already-checked items. If asked to generate a VAT return, reply: "This skill performs pre-checks only and does not generate VAT returns. Please hand the report to your tax representative or accountant."
