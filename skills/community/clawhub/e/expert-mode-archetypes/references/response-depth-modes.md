# Response Depth Modes v0.9.0

Expert Mode supports explicit response-depth modes. Use them to control both context loading and output length.

## Modes

| Mode | Trigger phrases | Context budget | Output style |
|---|---|---|---|
| Quick Expert Mode | quick expert mode, quick expert take, quick expert review | roster or one dossier header; usually Level 0-1 retrieval | short, decisive, usually 3-7 bullets or 100-250 words |
| Standard Expert Mode | activating expert mode, expert mode | one lead dossier or small panel; Level 1-3 retrieval | balanced, practical, usually 300-700 words |
| Deep Expert Mode | deep expert mode, full expert mode, deep expert analysis | small panel or broad summary; Level 3-4 retrieval | longer analysis with tradeoffs, risks, examples, next steps; usually 900-2000 words |
| Custom Length | in about N tokens/words, max N tokens, N bullet points, one paragraph, detailed report | match requested depth; do not load more context than needed | follow the user's requested length/shape |

## Quick Expert Mode

Use when the user wants speed or asks for a quick take.

Behaviour:

1. Select at most 1-3 archetypes.
2. Avoid creating many new dossiers unless required.
3. Load roster or one relevant dossier/header.
4. Answer with recommendation first.
5. Include only key rationale and next action.

Default output:

```markdown
Quick expert take:
- Recommendation: <answer>
- Why: <1-2 reasons>
- Watchout: <main risk>
- Next step: <action>
```

## Standard Expert Mode

Use for normal “activating expert mode”.

Behaviour:

1. Select 3-5 archetypes for ordinary work.
2. Load the smallest useful context, usually one lead dossier or 2-3 dossier panel.
3. Provide recommendation, rationale, tradeoffs, risks, and next steps.

## Deep Expert Mode

Use when the user wants thorough analysis.

Behaviour:

1. Select 5-10 archetypes if warranted by scope.
2. Load up to a small panel fully and summarize others.
3. Include assumptions, expert perspectives, consensus, disagreements, risks, evidence, and next-step plan.
4. Still avoid theatrical roleplay unless requested.

Default structure:

```markdown
Deep expert analysis

## Recommendation

## Expert lenses used

## Reasoning and tradeoffs

## Risks / failure modes

## Options

## Next steps

## What would change the recommendation
```

## Custom response length specifier

If the user requests a specific length, obey it over the default mode length when possible.

Recognize:

- “in about 200 tokens”
- “under 500 words”
- “give me 10 bullets”
- “one paragraph”
- “short answer”
- “long report”
- “detailed, around 1500 tokens”

Rules:

1. Treat token/word counts as approximate unless exactness is explicitly required.
2. Prefer respecting the requested length over showing every expert detail.
3. If requested length is too short for the risk level, give the concise answer plus a warning that more review may be needed.
4. If the user asks for a long answer but the task is simple, do not pad; say the concise answer is sufficient and offer deeper expansion.
5. If the user asks for exact token counts, aim close but do not claim exact unless you can measure.

## Priority order

When instructions conflict, use this order:

1. Safety and honesty boundaries.
2. User's explicit length/format request.
3. Quick/standard/deep mode.
4. Expert Mode default style.
5. Dossier voice cues.

## Length self-check

Before answering, ask:

- Did the user request quick, standard, deep, or custom length?
- Did I load too much context for the requested mode?
- Is the answer too long for the client's current need?
- Did I sacrifice necessary safety detail to be brief?
