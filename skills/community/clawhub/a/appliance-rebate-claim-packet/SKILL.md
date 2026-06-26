---
name: appliance-rebate-claim-packet
description: "Build a paperwork checklist and submission packet for appliance rebate claims, including eligibility facts, required documents, deadline checks, proof copies, and follow-up tracking. Use when the user bought or plans to buy an appliance and needs an organized claim packet without sharing full payment numbers."
---
# Appliance Rebate Claim Packet

## Purpose

Help the user assemble a complete appliance rebate claim packet for a manufacturer, retailer, utility, local government, recycling program, energy-efficiency program, or promotional rebate. Focus on paperwork readiness, deadline control, and proof tracking.

This is a prompt-only administrative checklist. It is not legal, tax, accounting, energy-audit, warranty, consumer-credit, or financial advice, and it does not guarantee rebate approval, payment timing, or eligibility.

## Use This Skill When

Use this skill when the user needs help with:

- Appliance rebates for refrigerators, freezers, washers, dryers, dishwashers, ovens, cooktops, ranges, microwaves, air conditioners, heat pumps, water heaters, or small appliances.
- Manufacturer or retailer mail-in rebates.
- Utility, municipal, state, provincial, national, or energy-efficiency program rebates.
- Trade-in, recycling, haul-away, installation, or proof-of-disposal requirements.
- A checklist before purchase, after purchase, before submission, or before a deadline.

Do not use this skill to decide tax treatment, provide legal advice, submit forms on the user's behalf, fabricate receipts, alter documents, or guarantee approval.

## Best Inputs

Ask for only what is needed. If details are missing, proceed with placeholders and a concise follow-up list.

- Appliance type, brand, model number, serial number if needed, purchase date, installation date, and retailer.
- Rebate program name, sponsor, claim URL or form title, offer code, program dates, and submission deadline.
- Purchase receipt or invoice details, with full payment card or bank numbers redacted.
- Proofs requested by the program: UPC label, EnergyGuide label, ENERGY STAR listing, invoice, order confirmation, delivery confirmation, installation certificate, contractor license, recycling receipt, haul-away proof, utility account proof, address proof, photo, or signed form.
- User contact and mailing information needed for the form, using minimal necessary details.
- Prior submission attempts, claim number, support contact, or rejection reason.

## Workflow

1. **Identify the program.** Record the rebate sponsor, program name, offer code, appliance category, purchase window, installation window, and submission deadline.
2. **Verify current rules.** Ask the user to provide the official terms or confirm the current official source. Check eligibility, model requirements, purchase location, installation requirements, household limits, account requirements, stacking rules, and required proof.
3. **Capture appliance facts.** Record model number, serial number if required, purchase date, delivery date, installation date, retailer, and address or utility account details only when needed.
4. **Redact payment data.** Remind the user to remove full card numbers, full bank numbers, security codes, unnecessary account numbers, and unrelated personal data from receipts and screenshots.
5. **Map documents to requirements.** Build a checklist that matches each program requirement to a document, photo, label, or form field.
6. **Prepare the packet.** Create a submission order, file naming plan, copies to keep, mailing or upload notes, and any signature or original-label handling notes.
7. **Run a deadline check.** Highlight purchase, installation, postmark, upload, claim correction, and follow-up dates.
8. **Plan proof of submission.** Include confirmation screenshots, email receipts, certified mail or tracking details where appropriate, and a claim log.
9. **Handle gaps.** List missing documents, who to contact, what to ask, and what evidence might satisfy the requirement.

## Output Format

Return the claim packet in this order:

1. **Rebate Snapshot**

| Field | Detail |
|---|---|
| Program sponsor | |
| Program or offer name | |
| Appliance | |
| Model number | |
| Purchase date | |
| Installation date | |
| Submission deadline | |
| Expected rebate type | |

2. **Rule and Deadline Check**

| Requirement | Current answer | Source or document | Verify before submitting? |
|---|---|---|---|
| Purchase window | | | |
| Eligible model | | | |
| Eligible retailer or installer | | | |
| Installation or recycling requirement | | | |
| Household or account limit | | | |
| Submission deadline | | | |
| Required proof list | | | |

3. **Document Checklist**

| Required item | Status | Where to find it | Redaction or handling note |
|---|---|---|---|

4. **Claim Form Field Prep**

| Field | Value to enter | Evidence source | Caution |
|---|---|---|---|

5. **Packet Assembly Order**

A numbered list of what to upload, mail, or keep, including file names and copy notes.

6. **Submission Proof Plan**

| Submission method | Proof to keep | Date/time | Follow-up date |
|---|---|---|---|

7. **Missing Items and Contact Script**

A short list of gaps plus a copy-ready message or call script for the retailer, installer, utility, manufacturer, or rebate administrator.

8. **Claim Tracking Log**

| Date | Action | Contact or confirmation number | Result | Next step |
|---|---|---|---|---|

9. **Open Questions**

A short list of missing facts that could affect eligibility or timing.

## Message Style

- Be concrete, careful, and deadline-focused.
- Separate confirmed rules from items that still need verification.
- Use plain language for forms and document names.
- Keep personal and payment data minimized.
- Avoid promising approval or payment.

## Safety Boundary

- This skill creates a paperwork checklist and claim packet only; it does not submit claims, sign forms, or contact programs on the user's behalf.
- Do not ask for full payment card numbers, bank account numbers, security codes, full tax IDs, passwords, one-time codes, or unrelated personal records.
- Remind the user to redact full payment numbers and unnecessary personal data before sharing receipts or screenshots.
- Verify program rules, deadlines, eligible models, and proof requirements against the current official program terms before submission.
- Do not fabricate receipts, UPCs, labels, installation proof, disposal proof, signatures, account status, or purchase dates.
- Do not guarantee rebate approval, processing time, payment amount, tax treatment, utility eligibility, or program funding availability.
- For tax credits, contractor rebates, government benefits, complex eligibility, or disputes over denial, recommend checking the official program administrator or qualified professional.

## Example Prompts

- "I just bought a new Energy Star refrigerator from Home Depot. Help me build a rebate claim packet for my utility company's appliance rebate program — I have the receipt and model number ready."
- "I need to submit a manufacturer mail-in rebate for my new washer and dryer. Build a document checklist and a submission proof plan so I don't miss the deadline."
- "I want to claim a state energy-efficiency rebate for my heat pump installation. Help me assemble a claim packet with the required documents, deadline calendar, and a follow-up tracking log."
