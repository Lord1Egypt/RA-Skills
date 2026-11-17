# Non-Data File Intake (intent triage)

When the user provides files that are not CSV/Excel/JSON/JSONL/TSV (PDF, PPTX, DOCX, images, plain text, books, etc.), **never enter the build pipeline directly, and never refuse service**. Follow this triage.

## Triage Decision

```
receive file (type detection failed: not a structured data file)
   ↓
check whether the context already states the intent
  ("build a database from this book's exercises" = intent A)
   ↓ intent clear → take the corresponding path directly
   ↓ intent unclear → ask once with options:
      "With this book I can:
       ① extract the content into a structured database (questions / knowledge points / formulas)
       ② just read, summarize, or explain it (no database needed)
       ③ did you mean to send a different file?
       Which one?"
```

**Principle**: file type determines capability boundaries; user intent determines the workflow. Never guess the task for the user.

## Intent A: Content Structuring → Database

Non-structured files are first "compiled" into a structured intermediate format, then fed into the standard data pipeline:

1. **Extraction** (LLM processes section by section; long documents in batches):
   - Textbooks → chapter structure + worked examples (statement/answer/difficulty) + knowledge points + formulas
   - Résumés/records → person entities (name/experience/skills)
   - Reports/papers → data tables + conclusions
   - Extraction output lands as JSONL (one entity per line, fixed fields) — this is LLM work that scripts cannot do
2. **Back to the standard pipeline**: JSONL → infer_schema.py profiling → relation discovery → checkpoints → modeling → database build
3. Ambiguities during extraction go through the same ask-checkpoint pattern ("this book has 3 question types — Practice/Exam/Mixed; how should the difficulty field be labeled?")

Extraction quality gate: after extraction, sample 10 items for human verification (with source page numbers); build the database only after user confirmation.

## Intent B: Reading Comprehension (no database)

Answer/summarize/explain directly; apart from offering "say the word if you ever want a database", this skill does not intervene. **Do not** force a database just to use the skill.

## Intent C: Wrong File

Politely confirm; start no pipeline.

## File Type × Recommended Path Quick Reference

| File type | Structuring potential | Default options offered |
|---|---|---|
| PDF textbook/book | high (hierarchy + questions + knowledge points) | question bank / knowledge-point bank / read only |
| PDF report | medium (data tables) | extract data tables into a database / summarize only |
| DOCX/PPTX | medium (table parts) | extract tables into a database / text processing only |
| Image | low (needs OCR/vision model) | describe the content / ask the user what they want |
| Plain text/Markdown | depends on content | show understanding / structure into a database |
| Code file | not data | ask the user for their purpose |
