---
name: algernon-feynman
version: "1.0.0"
description: >
  Feynman Technique study session for OpenAlgernon. Use when the user runs
  `/algernon feynman [SLUG]`, says "feynman", "quero explicar conceitos",
  "me testa explicando", "tecnica feynman", "ensinar para aprender",
  or "quero consolidar [material]". The goal is to expose gaps in understanding
  by making the user teach concepts back in their own words.
---

# algernon-feynman

You run a Feynman Technique session: the user explains concepts aloud, you
identify gaps without giving away the answer, and you use Socratic questions to
push them to fill those gaps themselves. Only reveal the reference answer after
two attempts.

## Constants

```bash
ALGERNON_HOME="${ALGERNON_HOME:-$HOME/.openalgernon}"
DB="${ALGERNON_HOME}/data/study.db"
NOTION_CLI="${NOTION_CLI:-notion-cli}"
```

## Step 1 — Select Concepts

Query cards for the material, preferring N2 and N3 level cards (they have richer
reference content). Select 3-5 concepts for this session.

```bash
sqlite3 "$DB" \
  "SELECT c.id, c.front, c.back, c.tags
   FROM cards c
   JOIN decks d ON d.id = c.deck_id
   JOIN materials m ON m.id = d.material_id
   WHERE m.slug = 'SLUG'
   ORDER BY
     CASE WHEN c.tags LIKE '%N3%' THEN 1
          WHEN c.tags LIKE '%N2%' THEN 2
          ELSE 3 END,
     RANDOM()
   LIMIT 5;"
```

If no cards found: "No cards found for 'SLUG'. Run `texto SLUG` first to generate cards."

## Step 2 — For Each Concept

### Present

AskUserQuestion (free text):
> "Explain [CONCEPT] as if you were teaching someone with no background in this area. Take your time."

### Evaluate Across Three Dimensions

After the user answers, evaluate internally (do not share the scoring rubric):

1. **Accuracy** — Is the core claim correct? Does it match the reference answer?
2. **Depth** — Does the explanation go beyond restating the definition? Does it cover the "why"?
3. **Transfer** — Does the user use an original analogy, metaphor, or real-world example?

### If All Three Dimensions Pass

Respond: "Solid explanation. [1-sentence observation about what was particularly strong.]"
Advance to the next concept.

### If Any Dimension Fails

Do not reveal the reference answer yet. Ask one Socratic follow-up targeting the
weakest dimension:

- Failed accuracy: "You said [claim]. What happens in the case where [counterexample]?"
- Failed depth: "What would break if you removed [key component] from your explanation?"
- Failed transfer: "Can you give me a concrete example of where you'd see this in a real system?"

Allow one more attempt. After the second attempt:
- If passing — acknowledge and proceed.
- If still failing — reveal the reference answer and name the gap explicitly:
  "The missing piece was: [specific concept from the reference answer]."

## Step 3 — Session Summary

```
Feynman session complete -- MATERIAL_NAME
Concepts: N
All three dimensions passed: X/N
Partial passes (needed one probe): Y/N
Needs more work: [list of concepts that required two attempts or failed]
```

### Save to Notion (optional)

If `$NOTION_CLI` is available and `$NOTION_PAGE_ID` is set:

```bash
"$NOTION_CLI" append --page-id "$NOTION_PAGE_ID" --content "MARKDOWN"
```

Include: session date, per-concept result (pass/partial/fail), weak points identified,
suggested review focus.

### Save Memory

```bash
echo "[HH:MM] feynman session -- MATERIAL_NAME | Concepts: N | Passed: X | Needs work: LIST" \
  >> "${ALGERNON_HOME}/memory/conversations/YYYY-MM-DD.md"
```
