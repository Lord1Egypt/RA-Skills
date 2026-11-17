---
name: "discussion-diagnosis-aggregator"
description: "Aggregate 6 single-skill diagnosis outputs into one Discussion report (scoring, severity, top-3). Output: chat reply in conversation language."
---

# Discussion Diagnosis Aggregator

## Role

This skill does **not** run the 6 single-skill diagnoses itself. It assumes their outputs (structured text or JSON) are available, and performs:

1. **Merge** — combine 6 skill outputs into a unified report
2. **Deduplicate** — collapse multi-skill issues that point to the same sentence (e.g., a verb-tense problem flagged by both Grammar and Vocabulary should appear once)
3. **Severity-tag** — classify each issue as critical / major / minor
4. **Prioritise** — produce top-3 fix list (severity × frequency × position in text)
5. **Anchor with examples** — for each high-severity issue, point to a positive example in `references/examples/`
6. **Score** — compute overall score (weighted) + per-dimension score + narrative-coherence meta-score
7. **Render** — output a single Markdown report **directly in the chat** as the assistant's reply; see **Output Mode** below for the chat-first, language-adaptive delivery rules

## Output Mode (chat-first, language-adaptive)

This skill's final report must be delivered **inside the assistant's chat reply**, not as a file artifact. Concrete rules:

- **Channel**: assistant message body (Markdown rendered in the conversation)
- **No `write` / `edit` for the report itself** — do NOT create `*_diagnosis.md` / `*_discussion_report.md` style files for the final report
- **Language policy** — match the **conversation language** at the moment of diagnosis:
  - User wrote in Chinese (中文对话) → report in Chinese (中文报告)
  - User wrote in English → report in English
  - Mixed / ambiguous → follow the dominant language in the user's most recent turn
  - Section headers, severity tags, bullet labels are translated consistently with the chosen report language
- **Internal scaffolding is fine on disk** — intermediate artifacts (PDF text dumps via `pymupdf`/`pdfplumber`, `_extract_*.py` scripts, scratch text) may still be written to disk for processing; only the **final report** is chat-bound
- **Opt-in file fallback** — if the user explicitly asks "save the report to a file" / "生成报告文件" / "export the diagnosis", fall back to writing a `.md` file AND still match the conversation language
- **Self-containment** — the report inside the chat must be complete and readable without opening any external file (no "see attached" stubs)

## Required inputs (from the 6 single skills)

Each single skill is expected to emit a structured block including:
- `dimension` (one of: structure / cohesion / grammar / vocabulary / logic / conventions)
- `score` (0–20 or 0–100, depending on the skill's rubric)
- `issues` (list of `{sentence_ref, severity, description, fix_suggestion, example_ref, cross_dimension_refs?}`)

## Aggregator output structure

```markdown
# Discussion Diagnostic Report

## Overall score: X / 100
(Weighted: structure 20% / cohesion 20% / grammar 10% / vocabulary 10% / logic 20% / conventions 20%)

## Per-dimension scores
- Structure: X / 20
- Cohesion (incl. narrative thread): X / 20
- Grammar: X / 20
- Vocabulary: X / 20
- Logic: X / 20
- Conventions: X / 20

## Narrative-coherence meta-score
(From Cohesion Level 2 — global thread + take-home persistence)
Score: X / 10 — [strong / adequate / weak]

## Severity-tagged issue list
### Critical (must fix)
1. [sent X] — [brief description] — flagged by: [dimensions]
2. ...

### Major (should fix)
1. ...

### Minor (nice to fix)
1. ...

## Top-3 priority fixes
1. **[Critical] [Sentence X]** — issue: ...; fix: ...; positive example: `references/examples/good_XX.md`
2. ...
3. ...

## Cross-dimension deduplication notes
- Issue Y was flagged by both Grammar and Vocabulary; consolidated here.
- Issue Z was flagged by both Conventions and Cohesion; consolidated here.

## Strengths (also surfaced)
- ...
```

## Severity rubric

| Severity | Definition |
|---|---|
| **Critical** | Undermines the take-home message; makes a claim that is not warranted by the data; missing a required move (contribution statement, limitations) |
| **Major** | Significantly weakens a specific move; misuses a modal verb / hedge in a load-bearing claim; breaks a citation chain |
| **Minor** | Stylistic; small register issues; non-load-bearing word choice |

## References (to be filled in Phase 3)
- `references/output-template.md` — full Markdown template
- `references/severity-rubric.md` — full severity criteria
- `references/cross-dimension-map.md` — which issues are expected to be flagged by multiple skills (and how to consolidate)
- `references/examples/` — annotated good/bad Discussion examples
