---
name: awl-academic-rewriter
description: "Rewrite English prose sentence by sentence into a more academic version using the bundled AWL/NAWL vocabulary list. Use when the user asks to academicize, polish, revise, or rewrite English text with academic vocabulary while preserving meaning, tense, claims, and document structure, and when two Markdown outputs are needed: a sentence-level change report and a complete revised document."
---

# AWL Academic Rewriter

## Purpose

Use the first-column AWL/NAWL headword list in `references/awl-headwords.txt` to revise English text into a more academic register. Let the model judge, sentence by sentence, which ordinary or imprecise expressions can be replaced by suitable academic vocabulary. Preserve the original meaning, tense, aspect, modality, negation, certainty level, evidence strength, and document structure unless a grammar correction requires a local change.

## Resources

- `references/awl-headwords.txt`: default vocabulary source; one first-column AWL/NAWL headword per line.
- `references/awl.csv`: full source table for selected headwords only. Columns are `Word`, `Derivatives`, and `English Definition`.
- `scripts/awl_lookup.py`: headword helper for listing, filtering, verifying first-column membership, retrieving all three CSV columns for selected headwords, and detecting headwords already present in input text. It does not score semantic replacement candidates.

Use the helper from the skill directory, for example:

```bash
python3 scripts/awl_lookup.py --all --limit 40
python3 scripts/awl_lookup.py --contains analy
python3 scripts/awl_lookup.py --word analysis --word analyze
python3 scripts/awl_lookup.py --details analysis --details factor
python3 scripts/awl_lookup.py --text-file input.txt
```

## Required Output Files

Always save two Markdown files unless the user explicitly asks for a different format:

1. Change report: if the input has a filename, use `<stem>-academic-changes.md`; otherwise use `academic-revision-changes.md`.
2. Complete revised document: if the input has a filename, use `<stem>-academic-revised.md`; otherwise use `academic-revised-document.md`.

The change report must contain a sentence-by-sentence table with these columns:

```markdown
| # | Original sentence | Revised sentence | AWL/NAWL terms used | Modification method |
|---|---|---|---|---|
```

In `Modification method`, state concrete edits, such as vocabulary substitution, grammar correction, clause restructuring, hedging, nominalization, or cohesion improvement. Keep explanations concise and do not invent reasons not visible in the text.

The complete revised document must contain only the revised text, preserving the original headings, paragraph order, list structure, citations, quoted material, numbers, and formatting as much as possible.

## Workflow

1. Read the input text from the user's message or file. If the user gives multiple files, process each file separately unless they ask for a merged output.
2. Preserve structural units first: headings, paragraphs, lists, tables, citations, code blocks, formulas, references, and quoted passages.
3. Split prose into sentences within each paragraph. Avoid splitting inside common abbreviations, decimal numbers, initials, citations, or parenthetical references.
4. Identify sentence meaning and rhetorical function before rewriting. Do not replace words merely because an academic synonym exists.
5. Use `references/awl-headwords.txt` as the candidate vocabulary set. Do not rely on automatic synonym scoring. For each sentence, let the model decide whether any source word or phrase can be replaced by a headword from the list without changing meaning.
6. After selecting candidate headwords, query `references/awl.csv` for those specific headwords and retrieve all three columns. Prefer `python3 scripts/awl_lookup.py --details <headword>` instead of loading the full CSV.
7. Use the retrieved `Derivatives` and `English Definition` to confirm semantic fit and select the correct grammatical form.
8. Rewrite each sentence according to the constraints below.
9. Reassemble the revised document in the original order and write both required Markdown files.
10. Run a final consistency pass comparing original and revised sentences for meaning, tense, factual claims, entity names, citations, and formatting.

## Headword-Based Replacement Method

For each sentence:

1. Identify the sentence's core proposition, tense, stance, and logical relations.
2. Identify ordinary, vague, conversational, or grammatically weak expressions that could be made more academic.
3. Consult `references/awl-headwords.txt` and select tentative headwords that may express the intended meaning in context.
4. Query `references/awl.csv` for each tentative headword and inspect all three columns: `Word`, `Derivatives`, and `English Definition`.
5. Confirm the definition fits the sentence meaning. Use a listed derivative when it is the best grammatical form; otherwise use an inflected form of the headword only if it remains semantically faithful.
6. Record the first-column headword in the change report even when the revised sentence uses a derivative.
7. Do not replace a word if the retrieved definition or derivative list suggests the headword would make the sentence less precise, more inflated, or semantically different.

This skill deliberately places semantic judgment on the model rather than on `scripts/awl_lookup.py`. The script is only a compact vocabulary access and verification tool.

## Rewriting Constraints

- Preserve the source meaning and factual scope. Do not add claims, evidence, citations, statistics, causal relationships, or certainty that the source does not contain.
- Preserve tense, aspect, modality, polarity, and degree. For example, do not turn "may reduce" into "reduces" or "did not find" into "found".
- Replace only vocabulary that improves academic precision, formality, or cohesion. It is acceptable for a sentence to receive no AWL/NAWL substitution if substitution would distort meaning.
- Introduce academic vocabulary only when its first-column headword appears in `references/awl-headwords.txt` and its full `references/awl.csv` row has been checked. Use a grammatical derivative or inflected form when necessary, but list the base headword in `AWL/NAWL terms used`.
- Correct grammar, punctuation, article use, agreement, and awkward syntax when needed.
- Prefer concise academic phrasing over inflated prose. Avoid overloading a sentence with multiple academic terms when one precise substitution is enough.
- Preserve technical terms, proper nouns, named methods, discipline-specific terms, citations, quoted text, numbers, units, and defined labels unless they contain clear grammar errors outside the quoted or fixed material.
- Keep paragraph structure and logical transitions stable. Add or adjust transitions only when they clarify an existing relationship.
- If the input includes non-prose elements such as code, equations, reference lists, or raw data, preserve them unchanged unless the user explicitly asks to revise them.

## Quality Checks

Before finalizing, verify that:

- Every original prose sentence has one corresponding revised sentence in the change report.
- The complete revised document contains the same substantive content and order as the original.
- Each listed AWL/NAWL term maps to a first-column headword in `references/awl-headwords.txt`.
- Each selected headword has been checked against its full `references/awl.csv` row before final use.
- Grammar fixes do not change meaning or tense.
- The revised document reads as coherent academic English without sounding artificially synonym-substituted.
