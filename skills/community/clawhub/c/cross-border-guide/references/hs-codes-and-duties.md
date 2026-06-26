# HS Codes, Duties & Tax Math

## 1. How HS classification actually works

The Harmonized System is global at 6 digits (chapter 2 + heading 2 + subheading 2); countries extend to 8-10 digits nationally (US HTS, EU TARIC/CN, etc.). Duty rates attach to the NATIONAL code of the DESTINATION — a US HTS lookup does not give you the EU rate.

**Classification method (simplified GRI order):**
1. Classify by what the product IS (composition/essential character), not what it is marketed as.
2. Composite goods: classify by the component giving essential character (earbuds + charging case = the earbuds).
3. Sets for retail sale: the component giving the set its character.
4. If two headings genuinely apply, the later one in numerical order wins (GRI 3(c)) — but reaching this point usually means get a ruling.

**Practical SOP:** draft a customs-grade description (material, function, how used) → find the 6-digit candidate in the origin tariff tool → verify the heading text and notes in the destination tariff database → extend to national digits → record rationale. For programs >$100k/year per market, request a binding ruling (US: CBP ruling; EU: BTI) — it is free insurance against reclassification penalties.

**High-risk categories for misclassification:** electronics accessories, textile blends (fiber percentages change headings), footwear, toys vs. collectibles, food/supplements, anything multi-function.

## 2. Customs valuation

Default basis is **transaction value**: the price actually paid by the buyer, i.e., the retail price for B2C — not your cost, not wholesale. Generally excludable if separately stated (varies by country): international shipping and insurance (in FOB-basis countries). CIF-basis countries (EU, much of Asia) include freight+insurance in the dutiable value.

- Consistency rule: invoice value = checkout receipt = payment processor record. Mismatch is the #1 audit trigger.
- Discounted sales: declare the discounted price actually paid — keep evidence of the promotion.
- Undervaluation consequences: holds, penalties (multiples of evaded duty), shipment seizure, importer-record flags that haunt every later shipment.

## 3. Duty and tax computation

```
Duty   = duty rate × customs value (CIF or FOB basis per destination)
VAT/GST = rate × (customs value + duty + freight where included)
Total landed cost = product + shipping + duty + VAT/GST + brokerage/disbursement + currency spread
```

Brokerage/disbursement: express integrators bundle clearance but charge "advancement/disbursement" fees (commonly 2-3% of duties+taxes, minimum $10-30); postal channels charge flat handling fees collected from the consignee on DDU.

## 4. De minimis — the planning lever

De minimis = value below which no duty (and sometimes no tax) is collected. Three traps:
1. **Duty and tax thresholds differ.** A market may waive duty under one threshold while taxing from zero (EU: no VAT de minimis since 2021; duty-free under €150).
2. **Channel matters.** Postal vs. courier channels can have different thresholds and remission rules (e.g., Canada's CUSMA courier remission vs. postal).
3. **They change.** Several markets have lowered or eliminated thresholds in recent years (and US de minimis policy has been in flux). Always tag thresholds "verify current" in deliverables.

**Patterns worth knowing (verify before relying):**
- EU: VAT from €0 (IOSS simplifies ≤€150); duty-free <€150.
- UK: VAT collected at checkout for consignments ≤£135 (seller/marketplace registers); duty-free <£135.
- Australia/NZ: GST on low-value imports collected at checkout above seller turnover thresholds (AU A$75k, NZ NZ$60k).
- Canada: low postal thresholds; higher courier thresholds for US/MX-origin under CUSMA.
- Japan: duty/consumption-tax relief roughly under ¥10,000 customs value with category exceptions.

**Tactical uses:** price/bundle to keep orders under the relevant threshold; split consignments only where legal (deliberate splitting to evade is not); choose DDU where most orders fall under de minimis, DDP above it.

## 5. Preferential origin (FTAs)

Free-trade agreements (CUSMA/USMCA, EU FTAs, CPTPP, RCEP…) can zero the duty IF the goods meet rules of origin AND you claim it with the right statement/certificate. Chinese-manufactured goods shipped from a US warehouse do NOT qualify as US-origin — origin is where the goods were substantially transformed, not shipped from. Only claim preference you can document; origin fraud penalties exceed duty savings by orders of magnitude.

## 6. Tax registration triggers (seller-side)

| Regime | Trigger | Effect |
|---|---|---|
| EU IOSS | Selling ≤€150 consignments to EU consumers | Collect VAT at checkout, fast clearance; one registration covers EU |
| UK VAT | Any ≤£135 B2C consignment | Register, collect at checkout |
| AU GST | >A$75k/yr AU turnover | Register, collect at checkout on ≤A$1,000 imports |
| NZ GST | >NZ$60k/yr | Same pattern |
| Marketplace deemed collector | Selling via major marketplaces | Marketplace collects — confirm in writing per market |

When the seller is below thresholds or unwilling to register, a merchant-of-record or marketplace route may beat direct selling. Surface this as a strategic option.
