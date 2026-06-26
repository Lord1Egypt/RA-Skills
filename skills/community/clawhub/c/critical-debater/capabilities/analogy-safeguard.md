# Capability: Analogy Safeguard

## Purpose

Validate historical analogies used in debate arguments. Ensure they meet quality standards and are properly caveated.

## Inputs

| Parameter | Required | Default | Description |
|---|---|---|---|
| workspace_dir | Yes | - | Path to debate workspace |
| round | Yes | - | Current round number |
| side | No | both | "pro", "con", or "both" |

## Validation Rules

### Structural Requirements

Every historical analogy MUST include:

1. **>= 2 similarities**: At least two concrete parallels between historical event and current topic
2. **>= 1 structural difference**: At least one acknowledged difference that limits the analogy
3. **< ~15% content share**: Historical analogies should not dominate the argument
4. **weight = "advisory"**: Analogies are explanation layer ONLY, never proof

### Quality Assessment

Use LLM to evaluate each analogy on:

| Dimension | Grades |
|---|---|
| Relevance | strong_parallel / moderate_parallel / weak_parallel |
| Honesty | honest / partially_honest / misleading |

**Relevance criteria:**
- `strong_parallel`: Multiple structural similarities, differences are minor or acknowledged
- `moderate_parallel`: Some similarities, but significant unaddressed differences
- `weak_parallel`: Superficial similarity only, more differences than parallels

**Honesty criteria:**
- `honest`: Differences and caveats clearly stated, analogy not overstated
- `partially_honest`: Some differences acknowledged but key ones omitted
- `misleading`: Differences suppressed, analogy presented as stronger than warranted

### Failure Modes to Check

1. **Cherry-picking**: Only citing aspects of historical event that support the argument
2. **False equivalence**: Claiming situations are identical when structural differences are significant
3. **Anachronism**: Applying modern concepts to historical contexts where they don't apply
4. **Survivorship bias**: Only citing historical examples that support the desired conclusion

## Execution Steps

1. Read debate turns for the specified round and side
2. Extract all `historical_wisdom` sections
3. For each analogy reference:
   a. Verify >= 2 similarities are cited
   b. Verify >= 1 difference is acknowledged (key_differences field)
   c. Verify applicability_caveat is non-trivial
   d. Grade relevance and honesty
   e. Check for failure modes
4. Return assessment for inclusion in JudgeRuling's `historical_wisdom_assessment`

## Output Format

```json
[
  {
    "side": "pro | con",
    "historical_event": "...",
    "relevance_grade": "strong_parallel | moderate_parallel | weak_parallel",
    "honesty_grade": "honest | partially_honest | misleading",
    "note": "Assessment details..."
  }
]
```

## Completion Marker

Output `DONE:analogy_safeguard` when complete.
