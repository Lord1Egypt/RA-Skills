# Judge Rubric (Autoreason Lite)

Score each candidate (A, B, AB) on 1-5:

1. **Faithfulness**
   - Preserves user intent and required facts
   - No hallucinations / fabricated claims

2. **Clarity**
   - Easy to follow
   - Logical flow and structure

3. **Usefulness**
   - Directly helps user complete their objective
   - Includes actionable framing where appropriate

4. **Scope discipline**
   - Avoids unnecessary expansion
   - Keeps length near target

Then rank candidates 1st/2nd/3rd and provide one-sentence rationale.

## Tie-breakers

1. Higher Faithfulness wins
2. Then higher Usefulness
3. Then shorter output (if quality is equivalent)

## Convergence guidance

If incumbent A is still best and alternatives add mostly stylistic churn, explicitly recommend **no change**.