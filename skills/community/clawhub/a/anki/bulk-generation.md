# Bulk Generation — Source Material Into An Importable Deck

The job the agent is asked for most: "make cards from this". Volume is the danger, not the difficulty — every card generated is a lifetime cost the user pays (SKILL.md rule 8), so the pipeline is a filter first and a formatter second.

## The Pipeline

1. **Scope**: ask nothing yet — read the material and state what you found ("14 pages, ~35 testable facts, mostly definitions and 6 numeric thresholds"). Users correct a proposal far more precisely than they answer a question.
2. **Budget**: pick the target count BEFORE writing (see Intake Budget). Report it with its review cost.
3. **Extract atoms**: one fact per line, no formatting yet. Facts that need the surrounding paragraph to be meaningful are not yet atoms — reword or drop them.
4. **Filter**: apply the keep/cut rules below. This is where most of the value is; expect to cut 30-60% of a first extraction.
5. **Format**: choose per fact, respecting `note_type` from config — Basic Q&A is the default; Cloze when the sentence has to stay intact; Image Occlusion for a labelled diagram, map or UI; `{{type:Back}}` for spelling and exact syntax; reversed only where production is genuinely needed.
6. **Dedupe**: against the user's existing deck if they supply an export or a term list; otherwise, at minimum, against the batch itself.
7. **Tag**: reuse the user's scheme, never invent a parallel one.
8. **Emit** in `card_format`, in chunks of `batch_size`, with the field header stated.
9. **Hand off** the import settings that make the file land correctly — separator, field mapping, note type, tag column, and whether HTML is allowed.

## Intake Budget

Card count is chosen from the study budget, not from the length of the source.

- Steady-state cost of a batch: `+N/reviews_per_card_lifetime` new cards per day for the days it takes to introduce them, then `N × reviews_per_card` extra reviews spread over their lifetime (SKILL.md Workload Math).
- Practical targets, stated as budgets rather than measurements: a 45-minute lecture yields **20-40 keepers**; a dense textbook page yields **5-15**; a research paper yields **3-10** (the claims, the method's constraint, the numbers you would quote). Producing three times that means recognition noise is being carded.
- If the user asks for "everything", give the budgeted set plus the list of what was cut and why. The cut list is what earns trust — and they can reclaim any line from it.

## Keep / Cut

| Keep | Cut |
|---|---|
| A fact you would be embarrassed to look up | Anything derivable in seconds from a fact you already carded |
| Numbers, thresholds, doses, dates, limits | Numbers you would always look up before acting on |
| Vocabulary, names, mappings, exceptions | Narrative, motivation, "why this chapter matters" |
| A distinction between two things you will confuse | Definitions circular with a term already carded |
| The one constraint that makes a method fail | Whole procedures — those need practice, not cards (SKILL.md, When Anki Is The Wrong Tool) |
| The counterexample that bounds a rule | Anything you do not yet understand — flag it for study instead |

## Extraction Patterns By Source

| Source | Where the cards actually are |
|---|---|
| Lecture slides | Bullet headings become questions; the last slide's summary is the deck skeleton; images with labels → Image Occlusion |
| Textbook chapter | Bolded terms, boxed thresholds, end-of-chapter questions (they are pre-written cards); skip the prose bridging them |
| Research paper | Claim + the number attached to it, the method's one constraint, the definition the field uses differently |
| Lecture transcript / video notes | Whatever the speaker repeated or wrote down; verbal filler carries no testable content |
| Code documentation | Signatures, defaults, error → cause pairs |
| Vocabulary list | Frequency-ordered; add example sentence and part of speech before importing |
| Personal notes | The questions the notes were written to answer — often already in the margins |
| Handwritten / scanned PDF | Extract text first and show the user the extraction; OCR errors become permanent card errors |

## Dedupe Before Import

Duplicates are cheap to prevent and expensive to find later.

- Anki's duplicate detection is **first-field, exact-text** — a rephrased duplicate is invisible to it (Browse → Notes → Find Duplicates catches only the exact ones).
- Semantic duplicates to catch while writing: the same fact asked forward and backward as two Basic notes; a cloze and a Q&A over one sentence; a subset card ("name one X") living beside the full set.
- Practical check with an existing collection: ask for a text export of the deck's first fields, and match on the keyword of each new question rather than on the whole string.
- Resolution: exact → keep the older note (it has the review history); semantic → keep the better-worded one and delete the other; subset → keep the more complete one only if the subset card is not a distinct discrimination.

## Output Format

```
#separator:tab
#html:true
#notetype:Basic
#tags column:3
What enzyme converts angiotensin I to angiotensin II?	ACE (angiotensin-converting enzyme)	physiology::cardio
```

- The `#` header lines are read by Anki on import and remove every manual mapping step — always emit them.
- Cloze batches use `#notetype:Cloze` and the cloze text in field 1; `#deck:` can preselect the destination deck.
- Tabs inside a field break the row: strip or replace them. Multi-line answers need `#html:true` and `<br>` — a raw newline ends the record.
- Semicolons and commas as separators break on any European decimal number or list; tab is the default for a reason.
- Never emit a partially-formed batch. An import is one action; a half-written file becomes 40 broken notes to clean up.

## Quality Pass Before Handing Over

Run SKILL.md Output Gates on the batch, then these three that only apply at volume:

- **Uniformity check**: same question stem repeated across 20 cards means one template, not 20 facts — vary the phrasing or the deck becomes pattern-matching.
- **Order check**: cards derived from a single paragraph will be introduced together and leak context to each other; shuffle the emitted order, or set the deck's new-card gather order to `random notes`.
- **Sample read-back**: read three random cards as if seen in two years with no memory of the source. Any that fail get context (SKILL.md rule 2) before delivery.
