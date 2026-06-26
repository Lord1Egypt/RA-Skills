# Output QA for ChatGPT

Run this before trusting or shipping an answer.

## Quick QA Grid

| Check | Ask | Fail Signal |
|-------|-----|-------------|
| Goal match | Did it answer the actual brief? | Impressive output that solves a different problem |
| Source fidelity | What facts came from the provided material? | Invented details or mixed sources |
| Structure | Is the format exactly what was requested? | Missing table, wrong length, wrong audience |
| Constraint fit | Did it honor exclusions and limits? | Ignores tone, budget, deadline, or "do not" rules |
| Uncertainty | Did it label assumptions and gaps? | Confident claims with no evidence trail |

## QA Prompts

### Self-critique

```text
Review your draft against the brief.
List the top 5 weaknesses, unsupported claims, and missing edge cases before rewriting it.
```

### Evidence check

```text
For each important claim, mark it as confirmed from source material, inferred, or unknown.
If unknown, say what evidence is missing.
```

### Constraint audit

```text
Check whether the draft violates any of these constraints: [paste constraints].
Return only violations and precise fixes.
```

## Hard Rules

- Never skip QA for externally-facing content, factual summaries, or operational plans.
- If the model cannot show where a claim came from, downgrade confidence immediately.
- Prefer targeted QA prompts over "make this better."
- If the answer fails the same check twice, rebuild the packet or switch surfaces.

## Shipping Threshold

Use the output only after it clears:
- goal match,
- source fidelity,
- constraint fit,
- and at least one explicit uncertainty check.
