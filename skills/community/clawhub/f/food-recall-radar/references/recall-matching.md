# The Food Recall Matching Problem — Reference

## Why this is harder than it sounds

The FDA publishes enforcement reports through openFDA within days of a recall being classified. The data is public, structured, and free. The failure is entirely on the consumption side:

1. **Volume.** Thousands of food recalls per year. A human cannot read them all.
2. **Naming.** The same product appears under store brands, co-packer names, and regional brands. "Great Value Frozen Broccoli" may be recalled as "Elseason's LLC broccoli florets, distributed to Walmart."
3. **Lot specificity.** A recall almost never covers everything a brand makes — it covers specific lots, date codes, and best-by windows printed in different formats per manufacturer.
4. **Attention decay.** A recall announced Tuesday is invisible by Friday. Food stays in freezers for months.

## The openFDA food enforcement endpoint

```
https://api.openfda.gov/food/enforcement.json?search=status:"Ongoing"+AND+classification:"Class+I"&limit=1000
```

Key fields used by the script:

| Field | Meaning |
|---|---|
| `status` | `Ongoing`, `Terminated`, `Completed` — match against Ongoing |
| `classification` | `Class I` / `Class II` / `Class III` |
| `recalling_firm` | the legal entity — often NOT the brand on the package |
| `product_description` | free text: brands, sizes, lots, best-by dates |
| `reason_for_recall` | pathogen, foreign material, undeclared allergen, mislabeling |
| `report_date`, `recall_initiation_date` | when it hit |
| `code_info` | lot codes / date codes in free text |
| `url` | the actual FDA recall notice (always read before acting) |
| `distribution_pattern` | states/regions affected |

## Matching strategy

Given pantry item `(brand, product, upc?, lot?)` and recall record:

1. **Normalize**: lowercase, strip punctuation/diacritics, drop stop-words (oz, inc, ltd, llc, company, frozen is kept — it's meaningful).
2. **Brand signal**: fuzzy containment of the pantry brand in `recalling_firm + product_description` (`SequenceMatcher` ratio ≥ 0.82 on tokens).
3. **Product signal**: Jaccard-style token overlap between pantry product words and the recall's product words, minus generic words (natural, organic, fresh, original, size words).
4. **Sequence signal**: full-string `SequenceMatcher` ratio as a tie-breaker.
5. **UPC shortcut**: if pantry has a UPC and the recall text contains a 12-digit sequence equal to it → `MATCH` (near-exact).
6. **Lot extraction**: regex over `code_info + product_description` for patterns like `lot`, `code`, `best by`, `use by`, `EXP`, followed by alphanumerics/dates — surfaced as "look for:" hints.
7. **Category heuristics (audit only)**: if a recall's product words hit a pantry product strongly with NO brand hit, emit `WATCH` — the store-brand/co-packer case.

Thresholds are deliberately tuned for recall (sensitivity) over precision: you should be willing to walk to the kitchen twice a month.

## Severity classes

- **Class I** — reasonable probability that exposure will cause serious adverse health consequences or death. Listeria in ready-to-eat food, Salmonella, undeclared allergens in high-risk products, E. coli O157:H7. Act immediately.
- **Class II** — remote probability of serious consequences; temporary or medically reversible harm. Most undeclared-allergen and foreign-material recalls land here — still act if the allergen matters to your household.
- **Class III** — unlikely to cause adverse health consequences. Eating is not advisable but risk is low; return at convenience.

## Special populations

For pregnant people, adults 65+, children under 5, and the immunocompromised, Listeria guidance is an order of magnitude stricter — a frozen-vegetable recall that's "Class II, reheat to kill" for the general public is "discard" for these groups. The script's `action` line always defaults to the conservative instruction; the human notice read is where personalization happens.

## Refunds and evidence

Most recalls offer refunds with proof of purchase, and many without (photo of the product + lot). Keep the recall URL the script prints: it is the authoritative description of affected lots and is what customer service will ask about. Retailers post recall notices at the register and on shelf tags — another reason store-brand items get missed: the shelf tag is gone by your next visit.

## Limitations (honest list)

- openFDA covers US FDA-jurisdiction recalls (includes imported food sold in the US). USDA/FISIS meat-poultry recalls are a separate dataset (fsis.usda.gov) not covered by the live query; the category heuristics in `audit` partially compensate.
- Rate limits without an API key are fine for weekly household use, not for scraping.
- Fuzzy matching trades precision for recall — expect occasional `VERIFY` hits that are unrelated. That is by design.
- UPC matching depends on the UPC appearing in the recall text; many notices print brand + lot but no barcode. Absence of a UPC hit is NOT absence of a match.
