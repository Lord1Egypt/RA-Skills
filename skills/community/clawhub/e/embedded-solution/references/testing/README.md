# Testing fixtures — embedded-solution skill

Regression test fixtures for the `embedded-solution` skill.

## What this is

7 simulated user queries, each chosen to exercise a different combination of
SKILL.md workflow paths:

| Fixture | User persona | Workflow paths exercised |
|---------|--------------|--------------------------|
| 01-industrial-iot-lora-ble | Hardware engineer | Step 5 ask → Step 6 top 3 → Step 7 if needed |
| 02-student-ble-learning | Student / hobbyist | Top 3 discipline (allows <3) |
| 03-product-manager-smart-lock | Product manager | Multi-function BOM + Step 7 out-of-catalogue |
| 04-procurement-cc2640r2f-stock | Buyer / procurement | **NOT a Top 3 question** — Step 7 marketplace tier |
| 05-founder-pet-tracker-cost | Startup founder | Cost floor + Step 7 GPS modules |
| 06-replacement-stm32wb55 | Repair engineer | Compatibility assessment template (NOT Top 3) |
| 07-advanced-matter-border-router | Senior embedded | Top 3 single-chip-vs-split + Step 7 spec lookup |
| 08-conflicting-assumptions | Distracted founder | **Conflict detection** — skill must name contradiction (USB + 5yr battery + outdoor) and ask 1 enumerated question, not silently pick |

**Note**: all fixtures are written for the **defaults-first** philosophy (2026-06-27 master change):
the skill should default to reasonable assumptions and **state them inline**, asking only
when reversible-cost is HIGH (AEC-Q100 / FDA / ATEX) or the user's request is internally
inconsistent. Earlier fixtures (01–07) were retrofitted to reflect this; their expected-output
files were updated 2026-06-27 to require `*[Assumed: ...]*` blocks and per-tier citation.

## How to run

### Manual evaluation (recommended for development)

1. Pick a fixture from `fixtures/`
2. Copy the **Input prompt** verbatim into your conversation with the skill
3. Save the response
4. Score against `evaluation-rubric.md` (5 axes × 5 pts = 25 max)
5. Document any failed checks in the fixture's "Acceptance criteria" section

### Automated regression (script template)

```bash
# Run all fixtures against the skill, capture responses
mkdir -p runs/$(date +%Y-%m-%d)
for fixture in fixtures/*.md; do
  base=$(basename "$fixture" .md)
  # Replace this with your skill invocation
  skill_run "$(extract_prompt "$fixture")" > "runs/$(date +%Y-%m-%d)/$base.response.md"
done

# Score each response
for response in runs/$(date +%Y-%m-%d)/*.response.md; do
  base=$(basename "$response" .response.md)
  echo "=== $base ===" >> "runs/$(date +%Y-%m-%d)/scores.md"
  score_response "$response" expected-outputs/$base.expected.md >> "runs/$(date +%Y-%m-%d)/scores.md"
done
```

## Expected outputs

`expected-outputs/` contains **skeleton** responses — not full answers, but the
**structural elements** that must be present (Top 3 table headers, citation
anchors, Step 5 question list). These skeletons prevent the test from being
"just match my template" — they verify the *structure* without constraining the
*prose*.

A response is structurally correct when:

1. It contains the expected sections (in any order)
2. It uses the catalogue anchors (`product_families.md#<chip>`) for cited chips
3. It marks verification status (✅/⏳/❌)
4. It explicitly says "verify against datasheet" for parameters it didn't fetch

## When to add a new fixture

Add a fixture when you encounter a new user persona or a new workflow path
that isn't yet covered. The 7 current fixtures cover:

- ✅ Step 5 ambiguity (01, 03, 05, 07)
- ✅ Step 6 with full Top 3 (01, 07)
- ✅ Step 6 with <3 (02)
- ✅ Step 6 with multi-function BOM (03, 05)
- ✅ Non-Top-3 output template (04, 06)
- ✅ Step 7 external lookup — marketplace (04)
- ✅ Step 7 external lookup — out-of-catalogue chips (03, 05)
- ✅ Step 7 external lookup — spec body (07)

Future fixtures could cover:

- Pure trigger refusal (e.g. "Rust on ESP32" — should NOT trigger)
- Multiple-application disambiguation ("smart device" — which type?)
- spec database evolution ("ST just released STM32U5 errata, what changed?")
- BOM cost recalculation ("after Q1 price drops, re-rank the candidates")
