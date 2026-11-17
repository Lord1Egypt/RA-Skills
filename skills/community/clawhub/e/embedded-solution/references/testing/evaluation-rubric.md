# Evaluation Rubric — embedded-solution skill

How to score a model's response to a testing/fixtures/*.md prompt.
Apply per fixture, score 1-5 on each axis, sum, document any failed checks.

## Scoring axes (5 axes × 5 points = 25 max)

### 1. Factual accuracy (max 5)

Does every cited chip exist in the catalogue? Are vendor URLs correct?
Are vendor status marks (✅/⏳/❌) consistent with `product_families.md`?

| Score | Definition |
|-------|------------|
| 5 | All cited chips exist, all URLs correct, all status marks match |
| 4 | 1 minor error (e.g. wrong package suffix) that doesn't mislead |
| 3 | 2-3 minor errors OR 1 moderate error (status mark inverted) |
| 2 | Multiple errors but response still salvageable |
| 1 | Chips that don't exist, or fabricated part numbers |

### 2. Top-3 discipline (max 5)

Does response use the Top 3 + comparison table template (per Step 6)?
Or correctly deviates (<3 when catalogue thin, or compatibility assessment
template for fixture 06)?

| Score | Definition |
|-------|------------|
| 5 | Top 3 with comparison table; allows <3 with explicit reason; uses assessment template when appropriate |
| 4 | Top 3 with comparison table, missing one row (e.g. "verification status") |
| 3 | Top 3 list but no comparison table |
| 2 | Single recommendation with no alternatives |
| 1 | No structured output, or fabricated candidates |

### 3. No fabrication (max 5)

Does the response avoid inventing specs, prices, or part numbers?
Does it flag "verify against datasheet" for parameters it cannot confirm?
Does it mark "not verified" appropriately?

| Score | Definition |
|-------|------------|
| 5 | Zero fabricated values; explicit "verify against datasheet" tags; Step 7 used when needed |
| 4 | 1 unverified value stated as if confirmed |
| 3 | Multiple values stated without verification flag |
| 2 | Some fabricated numbers that could mislead design |
| 1 | Significant fabrication (made-up part numbers, fake specs) |

### 4. Search priority (max 5)

Does response follow the 3-tier search priority?
- Tier 1: `specs/` if available
- Tier 2: `references/semiconductor-vendor/<V>/product_families.md`
- Tier 3: Step 7 external (vendor URL / Mouser / community / CSA spec)

| Score | Definition |
|-------|------------|
| 5 | Correct tier used in correct order; Step 7 cited with URL when triggered |
| 4 | Tier used but order not explicit |
| 3 | Mixed tier usage (e.g. specs/ checked but Step 7 result cited without URL) |
| 2 | Skipped a tier without justification |
| 1 | No tier usage at all (pure hallucination) |

### 5. Source citation (max 5)

Does every candidate link back to a verifiable source?
`product_families.md#<chip>` anchor or vendor product page URL?

| Score | Definition |
|-------|------------|
| 5 | Every chip / external fact has a citable source; verification status stated |
| 4 | Most chips have sources; 1 missing |
| 3 | Sources mentioned but not always linked |
| 2 | Some chips sourced, some not |
| 1 | No source attribution |

## Pass thresholds

- **Per fixture**: sum ≥ 20/25 to pass
- **Per dimension**: ≥ 4/5 on No Fabrication and ≥ 3/5 on Top-3 discipline (critical)
- **Suite pass**: ≥ 6/7 fixtures pass

## Failure modes to watch for

- **The "helpful hallucinator"**: confidently fills in missing info. Critical failure.
- **The "wall of text"**: dumps everything it knows without structure. Top-3 fails.
- **The "single answer":** picks one chip, no alternatives. Top-3 fails.
- **The "yes-man":** doesn't ask Step 5 clarification questions. Coverage misses.
- **The "refuser":** says "this is out of scope" when it isn't (e.g. "student learning
  BLE is software, not hardware"). Wrong trigger check.
