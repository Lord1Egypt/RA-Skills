---
name: relativity-deposition-question-builder
description: Develop deposition question sets from Relativity-exported PDF productions using a user-provided legal theory. Use when tasks involve reviewing opponent-produced PDFs, extracting per-page document IDs from the bottom-right corner (if two numbers appear, use the smaller one), mapping document relevance to a legal theory, and drafting questions grouped by document ID with required rationale and supporting quotes.
---

# Relativity Deposition Question Builder

## Overview

Analyze one or more Relativity-exported PDF productions against a legal theory and generate deposition questions organized by document ID. Each question includes a reason for asking and a document quote that can be used if the witness denies.

## Required Behavior

- Ask for the legal theory first before producing analysis or questions.
- Ask for PDF path(s) if not already provided.
- Extract page-level document IDs from the bottom-right area of each page.
- If two numeric IDs appear in that area, choose the smaller number as the page document ID.
- Keep quotes verbatim and include source file plus page number for each quote.
- Group outputs by document ID and place each question under its document ID heading.
- Under every question, include:
  - `Reason why we ask this question`
  - `Quote from the document to use in deposition in case the opponent party denies`

## Workflow

1. Gather inputs.
   - Confirm the user's legal theory.
   - Confirm PDF source path(s).
   - Optionally gather witness name/role and priority topics.
2. Extract per-page text and document IDs.
   - Run:
     ```bash
     python scripts/extract_relativity_pages.py \
       --input <pdf-folder-or-file> \
       --recurse \
       --output <relativity_pages.json>
     ```
   - Review pages where `selected_document_id` is null and flag for manual check.
3. Build a relevance map for the legal theory.
   - For each page, classify relation to theory: `supports`, `undermines`, `neutral`.
   - Focus question drafting on `supports` pages first, then `undermines` pages for impeachment.
4. Draft deposition questions grouped by document ID.
   - Use short, concrete, single-issue questions.
   - Start with authentication/foundation, then admission and contradiction questions.
   - Use direct quotes from page text for denial follow-up.
5. Return output in required structure.
   - Follow `references/deposition_output_template.md`.
   - Keep document IDs in ascending numeric order.

## Output Rules

- Do not merge different document IDs into one section.
- Do not omit `Reason` or `Quote` sections under any question.
- If no reliable quote exists, mark:
  - `Quote from the document to use in deposition in case the opponent party denies: [No direct quote located - manual verification required]`
- Prefer quotes that are short, specific, and tied to one factual proposition.

## Resources

- Extraction tool: `scripts/extract_relativity_pages.py`
- Output template: `references/deposition_output_template.md`

## Dependencies

Install once if missing:

```bash
python -m pip install --user pdfplumber
```
