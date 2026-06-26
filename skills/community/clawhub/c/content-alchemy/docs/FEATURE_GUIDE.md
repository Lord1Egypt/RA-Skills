# Content Alchemy Feature Guide

## Product Definition

`content-alchemy` is designed to transform reading input into saved outcomes rather than simple summaries.

The standard result includes:

- source information
- content theme
- three core ideas
- reconstructed structure
- key insights
- actionable next steps
- reusable takeaway

## Feature 1: Outcome-Oriented Text Transformation

Works well for:

- article bodies
- excerpts
- long-form explanations
- already extracted webpage text

Use it when the goal is not just understanding, but retention and reuse.

## Feature 2: Web URL Input

Workflow:

1. fetch the page
2. extract readable article text
3. transform the readable text into a usable result

Useful for:

- saved reading links
- long-form blog posts
- research articles with readable HTML

## Feature 3: PDF Input

PDF processing has two layers:

### A. Standard PDF reading

For:

- reports
- whitepapers
- essays
- papers

Capabilities:

- extract text and metadata
- transform selected pages or the whole document
- support page-range-based reading

### B. Long PDF / ebook reading

For:

- very long reports
- books
- reading over multiple sessions

Capabilities:

- build a reading plan
- segment the document safely
- save segment results
- save checkpoint summaries
- restore progress across sessions

## Feature 4: Page-Aware Routing

Default routing:

- `1-40` pages: `single_pass`
- `41-150` pages: `segmented_read`
- `151-400` pages: `long_form_read`
- `401+` pages: `book_mode`

This gives the skill a stable path even for 500-1000 page PDFs.

## Feature 5: Persistent Session State

Long-document state is saved under:

```text
~/.content-alchemy/sessions
```

Saved artifacts include:

- reading plans
- state files
- segment outputs
- checkpoint summaries

This enables commands like:

- where did I stop?
- resume from last position
- continue to the next segment
- jump to the segment that contains page 201

## Feature 6: Checkpoint Summaries

For segmented reading, the skill can build a checkpoint package from saved segment results and then generate a higher-level stage summary.

That means long-document reading is not just chunk splitting. It becomes a cumulative understanding workflow.

## Known Limits

This release does not directly handle:

- OCR
- scanned-PDF restoration
- fully dynamic webpage rendering
- pure table-first analytical workflows

If readable text quality is poor, the skill should say so directly and recommend OCR or source text.
