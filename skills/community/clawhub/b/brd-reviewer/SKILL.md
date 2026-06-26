---
name: brd-reviewer
description: Review Business Requirements Documents in `.docx` format by reading the existing BRD, extracting paragraph-level context, drafting clarification questions for unclear statements, and producing a final Word document that combines comments and tracked changes. Use when the user wants a BRD reviewed, challenged for ambiguity, or redlined with proposed wording improvements while preserving Word-native review features.
---

# BRD Reviewer

## Overview
Review a BRD paragraph by paragraph, capture clarification questions for ambiguous or incomplete requirements, and generate a single `.docx` with Word comments plus tracked revisions.

Prefer the bundled pipeline so the final deliverable is a Word-native review artifact instead of chat-only notes.

## Workflow
1. Confirm the source BRD `.docx` path.
2. Initialize the paragraph review JSON:
   ```bash
   python scripts/brd_review_pipeline.py init-review \
     --input <brd.docx> \
     --output <brd.review.json>
   ```
3. Read the BRD and fill the review JSON.
   - For every `paragraphs[]` item, keep `paragraph_index`, `style_id`, `heading_path`, and `source_text` unchanged.
   - Set `needs_comment` to `true` when the paragraph is unclear, incomplete, internally inconsistent, or missing acceptance criteria, data definitions, ownership, dependencies, assumptions, or edge cases.
   - Write `comment_question` as a concise reviewer question suitable for a Word comment.
   - Set `needs_revision` to `true` when the paragraph should be rewritten for precision, completeness, grammar, or testability.
   - Write `proposed_replacement` as full replacement language, not fragments.
   - Use `issue_tags` to make the reason explicit. Prefer tags such as `ambiguity`, `scope`, `actor`, `data`, `workflow`, `exception`, `dependency`, `acceptance-criteria`, `nonfunctional`, `term-definition`, or `conflict`.
4. Materialize the final reviewed DOCX in the same folder as the source BRD:
   ```bash
   python scripts/brd_review_pipeline.py materialize \
     --input <brd.docx> \
     --review-json <brd.review.json> \
     --output <brd.reviewed.docx> \
     --author "Codex BRD Reviewer"
   ```
5. Verify output quality.
   - Confirm the reviewed file exists beside the source BRD.
   - Confirm Word comments appear on paragraphs with `needs_comment=true`.
   - Confirm tracked changes are visible for paragraphs with `needs_revision=true`.
   - If the BRD relies heavily on tables or special layout, use the `$doc` skill workflow to render and visually inspect the result before delivery.

## Review standard
- Question every paragraph that leaves implementation choices unresolved.
- Favor reviewer comments for missing information and tracked changes for proposed wording.
- Rewrite requirements into concrete, testable statements.
- Flag undefined actors, systems, interfaces, calculations, timing, permissions, and exception handling.
- Do not silently invent business rules. If the BRD lacks a critical detail, ask for it in the comment instead of guessing.
- Keep comments short and specific enough to be actionable in a comment balloon.
- Keep proposed replacements professional and directly usable in the document.

## Output contract
- Always produce:
  - `<name>.review.json`
  - `<name>.reviewed.docx`
- Place both outputs in the same folder as the source BRD unless the user explicitly requests another path.
- Treat chat analysis as supplemental only. The `.docx` is the primary deliverable.

## Resources
- Paragraph review schema: `references/review-json-schema.md`
- Main tool: `scripts/brd_review_pipeline.py`

## Dependencies
Install once if missing:
```bash
python -m pip install python-docx lxml
```
