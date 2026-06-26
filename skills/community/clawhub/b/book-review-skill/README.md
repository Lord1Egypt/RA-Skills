# OpenClaw Book Review Skill

Local-only reading note expansion for OpenClaw.

This skill turns user-provided reading notes into structured reviews, brief summaries, related-concept maps, or book-to-book comparisons. It uses local templates only: no external APIs, no filesystem scanning, no note-library indexing, and no secrets.

## What It Does

- Expands a short reading insight into a useful review.
- Produces brief, detailed, related-concept, and comparison-style outputs.
- Marks the source basis as user notes, common book knowledge, or inference.
- Avoids invented page numbers, direct quotes, chapter details, and citations.
- Adds one practical application and one honest limitation or open question.

## What It Does Not Do

- It does not call any external model API.
- It does not ask for API keys or environment variables.
- It does not read Obsidian, Logseq, or local note folders.
- It does not cache reading data.
- It does not fabricate quotes or page numbers.

## Commands

```bash
/book-review <reading note>
/book-review-brief <reading note>
/book-review-related <reading note>
```

## Example

```text
/book-review 我读《原子习惯》时记下：身份认同驱动习惯，环境比意志力更重要。
```

Expected behavior:

- Source basis: user-provided notes.
- Main thesis: the note's central claim.
- Key takeaways: 3-5 grounded points.
- Application: one concrete action.
- Limits/open question: one caveat or question for further reading.

## Integrity Rules

When the user asks for quotes, page numbers, or exact chapter claims that were not provided, the skill should ask for the excerpt or clearly label the answer as a memory-based summary. It can still provide a useful thematic review, but it must not invent evidence.

## Development

```bash
npm install
npm run build
npm test
```

The bundled runtime is safe-template based. Review `src/index.ts` and `dist/index.js` if you want to audit the behavior.
