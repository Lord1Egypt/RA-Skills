---
name: catalog-sku-matcher-india
description: Match and normalize product listings across Indian ecommerce catalogs with variant-aware rules, confidence scoring, false-match prevention, and review queues for ambiguous pairs.
metadata: {"openclaw":{"emoji":"🧩","homepage":"https://clawhub.ai/Michael-laffin/price-tracker"}}
---

# Catalog SKU Matcher India

## Purpose

Build reliable cross-store product matching for Indian catalogs so price comparison is accurate.

## Disclaimer

This skill provides matching and normalization guidance only. It does not guarantee perfect match accuracy for all catalogs or seller data quality.

Use at your own risk. The skill author/publisher/developer is not liable for direct or indirect loss, incorrect match decisions, trading losses, or other damages arising from use or misuse of this guidance.

## Matching strategy

Use a layered approach:

1. **Hard identifiers**
   - model number / GTIN / MPN / ISBN where available

2. **Variant normalization**
   - brand
   - model family
   - storage/RAM
   - color
   - size/pack quantity
   - condition (new/refurbished/used)

3. **Soft similarity**
   - token similarity on cleaned title
   - key-attribute overlap
   - seller metadata sanity checks

4. **Confidence score**
   - `high`: auto-match
   - `medium`: human review queue
   - `low`: reject

## False-match guardrails

- Never match different storage/RAM variants as same SKU.
- Never match bundles/accessories to standalone products.
- Never ignore refurbished/used condition differences.
- Require manual review when two or more variant fields are missing.

## Output format

When matching listings, return:

1. canonical SKU candidate
2. matched listings with confidence level
3. rejected candidates with reason codes
4. manual review queue entries

## Setup

Read [setup.md](setup.md) and define normalization dictionaries first.

## Validation

Run [validation-checklist.md](validation-checklist.md) on labeled test sets before production.

## References

- Rules and reason codes: [matching-rules.md](matching-rules.md)
- Confidence scoring: [scoring-guide.md](scoring-guide.md)
- Edge-case examples: [examples.md](examples.md)

