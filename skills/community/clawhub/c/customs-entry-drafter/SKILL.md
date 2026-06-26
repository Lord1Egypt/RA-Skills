---
name: customs-entry-drafter
description: >
  Use this skill when a licensed customs broker, import compliance manager,
  or trade-compliance team needs to prepare a CBP entry summary draft for a
  commercial import shipment into the United States. Covers entry-type selection,
  document review, HTS classification confirmation, duty and fee computation,
  partner government agency (PGA) admissibility screening, and line-item entry
  summary drafting. Produces a DRAFT for licensed customs-broker review before
  any ACE/ABI transmission or CBP submission.
---

# Customs Entry Drafter

Turns shipment documents into a structured CBP entry summary draft — covering entry-type selection, document review, duty computation, and PGA checks — so a licensed customs broker can review, validate, and transmit to ACE/ABI with confidence.

## Flow

### Phase 1 — Shipment Identification

Ask the user for:
1. Importer of Record (IOR) name, address, IRS/EIN, CBP Importer Account number
2. Country of origin (and country of export if different)
3. Port of entry (CBP port code or city)
4. Transport mode (ocean / air / truck / rail)
5. Carrier SCAC / flight number / conveyance name
6. Master and house bill of lading or air waybill numbers
7. Arrival date / estimated arrival date

Ask one question block at a time. Wait for the user's answer before continuing.

### Phase 2 — Commodity and Value Review

Ask for the commercial invoice(s). Extract per-line:
- Seller and buyer names
- Commodity description (as on invoice)
- Country of manufacture
- Quantity and unit of measure
- Unit price and total invoice value
- Currency
- Incoterms (FOB / CIF / EXW / DDP)
- Any first-sale or related-party declarations

Flag:
- Related-party transactions (must document whether relationship affected price)
- Non-standard Incoterms requiring value adjustments
- Missing manufacturer / country of manufacture fields

### Phase 3 — HTS Classification Confirmation

For each line item:
1. Display the HTS number the user provides (or the user's description if no HTS yet)
2. Confirm the number is 10-digit HTSUS format
3. State the general duty rate, MPF applicability, and any applicable Section 301 / Section 232 / AD/CVD case numbers based on the provided HTS
4. Flag if the description does not appear consistent with the HTS heading

Do NOT determine HTS numbers from scratch here — use the `hs-tariff-classification` skill for that. Instruct the user to confirm classification before finalizing the entry.

### Phase 4 — Entry Type Selection

Based on shipment characteristics, recommend the appropriate CBP entry type:

| Entry Type | Use Case |
|---|---|
| Type 01 (Formal Consumption) | Dutiable merchandise ≥ $2,500 |
| Type 03 (Consumption — Quota) | Quota-subject merchandise |
| Type 06 (FTZ Admission) | Foreign Trade Zone admission |
| Type 11 (Informal — $800–$2,499) | Low-value non-restricted merchandise |
| Type 86 (Section 321 Informal) | De minimis ≤ $800, eligible shipments |
| Type 21 (Warehouse) | Bonded warehouse admission |
| Type 23 (Rewarehouse) | Transfer between bonded warehouses |
| Type 52 (TIB) | Temporary Importation under Bond |

State the recommended type with rationale. Flag if quota, antidumping/CVD, or restricted-article rules require special handling.

### Phase 5 — Duty, Fee, and Surcharge Computation

Compute per line item:
- **Entered Value**: CIF or FOB per agreed Incoterms adjustment to CBP transaction value
- **Dutiable Value**: Entered value ± statutory adjustments
- **General Duty**: Dutiable value × ad valorem rate (or specific / compound per schedule)
- **Section 301 Duty**: Flag applicable list and rate if HTS in scope
- **Section 232 Duty**: Flag if steel or aluminum
- **MPF**: 0.3464% of entered value (min $32.71, max $614.35 per entry — label as INDICATIVE; confirm current caps)
- **HMF**: 0.125% of entered value for ocean entries
- **AD/CVD Deposit**: Flag open cases with current cash deposit rate; label ESTIMATED

Label all amounts **DRAFT — ESTIMATED** and note that final liquidated duties may differ.

### Phase 6 — Partner Government Agency (PGA) Admissibility Screen

Based on HTS chapters and commodity descriptions, flag any PGA filing requirements:

- FDA (food, drug, device, cosmetics — prior notice, FSMA compliance)
- USDA APHIS (plants, plant products, meat/poultry)
- USDA FSIS (meat, poultry, eggs — FSIS establishment required)
- EPA (pesticides, vehicles, engines, refrigerants)
- CPSC (children's products, consumer goods safety)
- ATF (firearms, ammunition, explosives)
- FWS (wildlife, CITES-listed species)
- OFAC (sanctions check — flag if origin is a sanctioned country)
- DEA (controlled substances, listed chemicals)

For each flagged PGA: state the required filing, document, or permit and mark as CONFIRM WITH SPECIALIST if out of scope.

### Phase 7 — Entry Summary Draft Assembly

Produce a structured DRAFT entry summary table with:

| Field | Value |
|---|---|
| Entry Type | |
| Importer of Record | |
| Port of Entry | |
| Country of Origin | |
| Mode / Carrier | |
| MBL / HBL | |
| Arrival Date | |
| Entry Date | |

Then per-line table:

| Line | HTS | Description | COO | Qty | UOM | Entered Value | Duty Rate | Duty | AD/CVD | Sec. 301 |
|---|---|---|---|---|---|---|---|---|---|---|

Then totals block:

| Item | Amount |
|---|---|
| Total Entered Value | |
| Total Duty | |
| MPF (estimated) | |
| HMF (if ocean) | |
| AD/CVD Deposits (est.) | |
| **Total Estimated Charges** | |

Append:
- PGA flags list
- Document checklist (commercial invoice, packing list, B/L or AWB, certificate of origin if claiming FTA preference, any PGA permits)
- Open-questions / information gaps list

Close with a **Licensed Customs Broker Review Block**:
> DRAFT — NOT TRANSMITTED. This entry summary draft is for customs-broker review only. All HTS classifications, values, duty rates, and PGA admissibility determinations must be verified by a licensed customs broker or attorney before ACE/ABI transmission. Do not use as a final entry.

## Key Rules

- Never transmit an entry or represent that this draft constitutes an ABI transmission.
- Always label computed duties and fees as DRAFT — ESTIMATED.
- Never infer HTS numbers from descriptions alone — direct the user to use `hs-tariff-classification` or consult a broker.
- Flag OFAC-sanctioned country origins and require user confirmation before proceeding.
- Do not opine on whether a shipment qualifies for antidumping/CVD exclusions — state the cash deposit rate and direct to the broker or trade counsel.
- Ask one phase at a time. Do not request all information in one block.
- Mark any fee thresholds or rate values as CONFIRM CURRENT RATES with CBP.

## Output Format

- Phase-by-phase output with clear labeled sections
- Entry summary table (text-formatted for copy-paste into ACE or Excel)
- Totals block labeled DRAFT — ESTIMATED
- PGA flag list
- Document checklist
- Open-questions list
- Licensed Customs Broker Review Block as the final section

## Feedback

If the user expresses an unmet need or dissatisfaction with this skill, surface the contribution link:
> This skill can be improved. Please share your feedback at https://github.com/archlab-space/Open-Skill-Hub/issues
