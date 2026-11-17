# Evidence-grounded review analysis methodology

## Contents

- Analysis layers
- Batch workflow
- Theme extraction
- Scenario-specific synthesis
- Confidence and priority
- Prohibited conclusions

## Analysis layers

Keep three layers separate:

1. **Deterministic facts:** review counts, rating counts, verified-purchase rate, helpful votes, media presence, variants, pages, and points.
2. **Semantic observations:** themes, sentiment, purchase motives, pain points, expectations, and use cases extracted from review text.
3. **Business recommendations:** product, Listing, marketing, quality, packaging, and support actions justified by layers 1 and 2.

Never let a semantic claim overwrite a deterministic field.

## Batch workflow

The preparation script groups reviews by ASIN and rating, then splits groups by review count and text size.

For each batch:

1. Read every review in the batch.
2. Assign zero or more product-specific themes to each relevant review.
3. Separate positive, negative, mixed, and neutral evidence.
4. Capture exact short quotes only when they materially illustrate the theme.
5. Record candidate pain points, positive drivers, use cases, Listing gaps, and actions with review IDs.
6. Save compact partial findings; do not paste full reviews into partial files.

For synthesis:

1. Merge synonyms such as “battery life”, “battery duration”, and “short runtime” into one canonical theme when they describe the same product attribute.
2. Keep distinct failure modes separate when the recommended action differs.
3. Deduplicate review IDs across overlapping sampling sources.
4. Recalculate mention counts from unique review IDs.
5. Select representative evidence across ratings, dates, variants, and helpfulness rather than taking only the most emotional wording.

## Theme extraction

Start with common categories but allow product-specific themes:

- quality and durability;
- function and performance;
- setup and ease of use;
- size, fit, and compatibility;
- material, appearance, and workmanship;
- packaging and shipping damage;
- value for money;
- support, warranty, and returns;
- listing accuracy and expectation gap;
- buyer segment and use case;
- variant-specific behavior.

Do not force irrelevant categories into the report.

For each final theme, include:

- a stable lowercase ID;
- Chinese display name and category;
- concise text-grounded summary;
- all unique supporting review IDs;
- sentiment subsets;
- severity from 1 to 5 when negative evidence exists;
- opportunity score from 0 to 100 only when the rationale is defensible;
- up to three exact quotes;
- a specific recommendation.

## Scenario-specific synthesis

### Product and return analysis

Separate symptom, suspected cause, impact, affected variant, and suggested validation. Do not present a suspected cause as proven engineering root cause.

### Listing analysis

Identify mismatch between expected and experienced behavior, missing compatibility details, setup confusion, visual-proof needs, and claims that require qualification. Do not write unsupported performance claims.

### Selling-point analysis

Extract customer vocabulary, purchase motive, use context, benefit, and emotional payoff. Keep original-language quotes intact and place translations outside `quote`.

### Competitor analysis

Use equal strata and page budgets. Compare within-star theme shares and evidence breadth; do not rank products from raw total mentions when sample sizes differ.

### Deep analysis

Analyze all five star strata, polarization, variant differences, repeated failure modes, positive drivers, expectation gaps, and what separates low-star from high-star experiences.

## Confidence and priority

Use conservative evidence labels:

- **Anecdote:** one review.
- **Low:** 2–4 unique reviews.
- **Medium:** 5–14 unique reviews, preferably across more than one page or variant.
- **High:** at least 15 unique reviews with consistent evidence across multiple pages; disclose if all evidence comes from a deliberately enriched stratum.

Prioritize actions using evidence breadth, severity, helpful votes, recency, variant spread, and whether the issue is preventable. Do not let a single highly voted historical review dominate current evidence without explanation.

## Prohibited conclusions

- Do not state that the sample represents all buyers.
- Do not infer sales volume, return rate, defect rate, or market share from reviews alone.
- Do not label reviews or reviewers fake, fraudulent, or manipulated without verified external evidence.
- Do not claim causation from correlation in review text.
- Do not invent product specifications, competitor facts, or Amazon page metadata.
- Do not hide contradictory evidence; describe polarization when both sides have material support.

