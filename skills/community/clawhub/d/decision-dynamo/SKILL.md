---
name: decision-dynamo
description: Run a weighted decision matrix to score and rank 2-4 options across 5 configurable criteria. Use when a user needs help choosing between options, comparing tradeoffs, or making a structured decision. Triggers on phrases like "help me decide", "which option is better", "decision matrix", "weigh my options", or "I can't choose between".
---

# Decision Dynamo

Run a weighted matrix analysis to score and rank options objectively.

## Workflow

1. **Gather options** — Identify 2–4 named choices to compare.
2. **Set weights** — Ask the user to rate how important each of the 5 criteria is (1–10).
3. **Score options** — For each option, rate it 1–10 on each criterion.
4. **Run the matrix** — Execute `scripts/decision_matrix.py` (interactive or JSON mode).
5. **Present results** — Share the ranked output and briefly explain the winner.

## Running the Script

**Interactive mode** (guided prompts):
```bash
python3 scripts/decision_matrix.py
```

**JSON mode** (pre-built input):
```bash
python3 scripts/decision_matrix.py input.json
```

See `references/criteria.md` for the JSON schema, criteria definitions, scoring scale, and inversion logic for negative criteria.

## The Five Criteria

| Criterion         | Type     |
|-------------------|----------|
| Skill/Leverage Gain | Positive |
| Goal Alignment    | Positive |
| Mental/Emotional Drag | Negative (inverted) |
| Financial Cost    | Negative (inverted) |
| Time and Effort   | Negative (inverted) |

Negative criteria use `(11 - score) * weight` so that *less drag = higher score*.

## Agent Guidance

- If the user hasn't defined weights, suggest defaults (all equal at 5) and ask if they want to adjust.
- If scoring feels subjective, help the user by asking "on a scale of 1–10, how much does this option [criterion]?"
- After presenting results, offer to re-run with adjusted weights to test sensitivity.
- Always show the winner clearly and explain *why* it scored highest in plain language.
