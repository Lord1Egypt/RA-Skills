# Academic Composer — Skill Specification

## Purpose

Academic writing assistant for **research and learning purposes**: search academic sources, build evidence-based outlines, expand into fully cited essays (APA / MLA / Chicago), and improve writing style with local quantitative analysis.

> **Academic Integrity Notice:** This skill is intended for personal research drafts, study aids, and learning how to construct academic arguments with proper citations. It is **NOT** intended for submitting AI-generated content as one's own original work, bypassing academic integrity policies, or any form of plagiarism. Users are solely responsible for ensuring their use complies with their institution's academic honesty requirements.

## When to Use

- User wants to **write an academic essay or research paper**
- User needs help with **citations, references, or bibliography**
- User wants to **find academic sources** for a topic
- User needs to **convert an outline into a full essay**
- User mentions **academic writing**, **essay draft**, **cite sources**

## Four-Phase Workflow

### Phase 0 — Source Collection

Build a curated Source List before writing. The essay is structured around evidence, not the other way around.

**Option A — Academic search:**
1. Run: `python skill/scripts/scholar.py --query "TOPIC KEYWORDS" --limit 10 --year-min YEAR --json`
2. Present the returned papers as a numbered list
3. User selects which papers to include

**Option B — User-provided sources:**
1. User pastes titles, DOIs, URLs, or BibTeX entries
2. Parse into structured records

**Combined:** Search first, then merge user-provided sources. Confirm Source List before proceeding.

### Phase 1 — Outline Generation

1. Collect from the user: topic, essay type, word count, citation style, requirements
2. Generate a structured outline with source mapping per paragraph
3. Present outline, wait for user approval, revise if requested

### Phase 2 — Essay Expansion

1. Expand the approved outline into a complete essay
2. Insert in-text citations at every evidence point per chosen style
3. Append a complete Reference List (APA), Works Cited (MLA), or Bibliography (Chicago)
4. Present draft to user for review

### Phase 3 — Writing Style Improvement (optional)

Runs entirely locally. No data leaves the machine.

1. Save essay to a temp file, then run: `python skill/scripts/pipeline.py --file /tmp/essay.txt --measure-only --json`
   (Essay is passed via file path, not CLI argument, to avoid process-listing exposure.)
2. If style score > 15: rewrite flagged passages to improve naturalness
3. Citation protection: All citations are immutable during rewriting
4. Repeat until style score <= 15 or max passes reached

## Rules

1. Sources first: Build the Source List before generating the outline
2. User approval required on outline before expanding
3. Citation integrity: Never fabricate, alter, or remove citations
4. Citation protection: Citations are immutable during rewriting
5. Plain text output in the essay body
6. No hallucination: Only use sources from the confirmed Source List
7. Local scripts: `pipeline.py`, `measure.py`, and `scholar.py` do not transmit essay content externally. However, essay generation and rewriting are performed by the orchestrating LLM, which may use a remote model provider depending on the agent's configuration
8. Ethics: Always include academic integrity disclaimer in the final output

## Supporting Files

| File | Purpose |
|------|---------|
| `skill/scripts/scholar.py` | Semantic Scholar API source search |
| `skill/scripts/pipeline.py` | Local writing style analysis |
| `skill/scripts/measure.py` | Bundled quantitative scorer |
| `skill/references/essay_templates.md` | Essay type templates with source mapping |
| `skill/references/citation_formats.md` | APA / MLA / Chicago formatting rules |
| `SECURITY.md` | Data flow, permissions, academic integrity |
