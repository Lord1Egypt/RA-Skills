# Optimizing Skill Descriptions

The description is the sole mechanism for skill triggering. Under-specified → doesn't trigger; over-broad → false triggers.

## How Triggering Works

Agents load name + description for all skills at startup (Tier 1). User task matches description → full SKILL.md read. Simple requests may not need a skill; complex domain tasks are where descriptions make the difference.

## Writing Effective Descriptions

- **Use imperative phrasing**: "Use this skill when..." not "This skill does..."
- **Focus on user intent**: describe what the user wants to achieve, not skill internals
- **Err on the side of pushy**: explicitly list applicable contexts, including when the user doesn't name the domain
- **Keep concise**: a few sentences to a short paragraph, ≤1024 chars

## Trigger Eval Queries

~20 queries: 8-10 should-trigger + 8-10 should-not-trigger.

### Should-trigger

Vary across: phrasing, explicitness, detail, complexity. Most valuable are queries where the skill helps but the connection isn't obvious.

### Should-not-trigger

Most valuable negatives are near-misses: share keywords but need something different. Example for CSV skill: "update Excel budget formulas" (shares spreadsheet concept but needs Excel editing) or "write Python script to upload CSV to database" (involves CSV but task is ETL).

## Testing

Run each query 3 times, compute trigger rate. Should-trigger passes if rate ≥0.5; should-not passes if <0.5.

## Avoiding Overfitting

60% train (guide improvements) + 40% validation (check generalization). Keep both sets proportionally mixed.

## Optimization Loop

1. Evaluate on both train + validation
2. Identify train failures only; keep validation blind
3. Revise: too narrow → broaden; too broad → add specificity
4. Avoid adding specific keywords from failed queries (overfitting); find the general category
5. If stuck, try structurally different descriptions rather than incremental tweaks
6. Repeat until train passes or no improvement
7. Select the iteration with highest validation pass rate (not necessarily the last)

~5 iterations usually suffice. No improvement → issue may be with queries, not description. Validate generalization with 5-10 fresh queries.

## Example

```yaml
# Before
description: Process CSV files.

# After
description: >
  Analyze CSV and tabular data — compute summary statistics,
  add derived columns, generate charts, and clean messy data.
  Use when the user has a CSV, TSV, or Excel file and wants to
  explore, transform, or visualize the data, even if they don't
  explicitly mention "CSV" or "analysis."
```
