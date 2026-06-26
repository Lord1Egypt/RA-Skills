---
name: content-alchemy
slug: content-alchemy
version: "1.0.0"
description: "Turn articles, web pages, PDFs, and excerpts into structured notes, key insights, practical actions, and reusable takeaways."
changelog: "English-source release for GitHub and international ClawHub publishing."
metadata: {"clawdbot":{"emoji":"🧪","os":["linux","darwin","win32"],"requires":{"bins":["python3","pdftotext","pdfinfo"]}}}
---

# Content Alchemy

## Skill Purpose

Use this skill to transform reading input into reusable personal outcomes rather than plain summaries.

Supported input types:

- article text
- web URLs
- extracted web text
- PDF files
- book excerpts
- long explanatory passages

Expected output shape:

- structured notes
- key insights
- actionable next steps
- reusable takeaway

## When To Use

Prefer this skill when the user wants something like:

- "Turn this article into something I can keep"
- "Extract the useful takeaways from this page"
- "Turn this PDF into notes and actions"
- "Help me continue reading this long PDF"
- "Summarize this content, but make it more useful than a plain summary"

## Differentiation Rules

Always follow these rules:

1. Do not treat the task as plain summarization.
2. Reconstruct value, structure, and usefulness instead of merely compressing content.
3. The output should feel like a saved personal artifact, not model paraphrase.
4. Every result should improve at least one of these:
   - easier to revisit
   - easier to retain
   - easier to act on
   - easier to reuse
5. If the result still reads like a generic summary, restructure it again.

## Scope and Limits

This release supports three routes:

- `plain_text`
- `web_url`
- `pdf_file`

This release does not directly handle:

- OCR for scanned PDFs
- code analysis workflows
- pure table-first analysis
- fragmented, image-first inputs with little readable text

If text extraction fails or text quality is too low, say so clearly and recommend OCR or source text.

## Script Rules

When running bundled scripts:

- always use `python3`
- prefer absolute paths from the installed skill directory
- do not assume the current working directory is the skill directory

Recommended setup:

```bash
SKILL_ROOT="$HOME/.claude/skills/content-alchemy"
```

Content transformation is performed directly by the model.

- There is no `process_content_alchemy.py` script.
- Do not invent a hidden processing script.
- If you need a fixed output structure, use:
  - `templates/result_template.md`
  - `templates/checkpoint_template.md`

## Input Route A: plain_text

Use this route for:

- article bodies
- extracted web content
- excerpts
- long explanatory text

Process directly in-model using the outcome-oriented structure.

## Input Route B: web_url

When the input is a URL:

1. Run `extract_web_text.py`
2. Extract title, site, author, publication time, and body text
3. Check whether the extraction is strong enough to support transformation
4. If not, explain the limit and ask for source text

Command:

```bash
python3 "$SKILL_ROOT/scripts/extract_web_text.py" "https://example.com/article"
```

Troubleshooting only:

```bash
python3 "$SKILL_ROOT/scripts/extract_web_text.py" "https://example.com/article" --insecure
```

## Input Route C: pdf_file

When the input is a PDF:

1. Run `plan_pdf_reading.py`
2. Determine the strategy from page count and text quality
3. Use `extract_pdf_text.py` for the appropriate page range
4. For longer PDFs, initialize or restore state and proceed segment by segment

Plan command:

```bash
python3 "$SKILL_ROOT/scripts/plan_pdf_reading.py" "/path/to/file.pdf"
```

The planning result returns:

- `session_root`
- `plan_file`
- `state_file`
- `commands`
- `segment_results_dir`
- `checkpoint_results_dir`

Prefer the exact returned paths and commands instead of guessing filenames.

Extract a page range:

```bash
python3 "$SKILL_ROOT/scripts/extract_pdf_text.py" "/path/to/file.pdf" --page-start 1 --page-end 5
```

Initialize or restore state:

```bash
python3 "$SKILL_ROOT/scripts/update_pdf_session_state.py" init --plan-file "<returned plan_file>" --state-file "<returned state_file>"
```

Force reset only when the user explicitly wants to restart:

```bash
python3 "$SKILL_ROOT/scripts/update_pdf_session_state.py" init --plan-file "<returned plan_file>" --state-file "<returned state_file>" --force-reset
```

Move to the next segment:

```bash
python3 "$SKILL_ROOT/scripts/update_pdf_session_state.py" next --state-file "<returned state_file>"
```

Save the current segment result:

```bash
python3 "$SKILL_ROOT/scripts/record_pdf_segment_result.py" --state-file "<returned state_file>" --content-file "/path/to/segment-result.md"
```

Build the next checkpoint package:

```bash
python3 "$SKILL_ROOT/scripts/build_pdf_checkpoint.py" --state-file "<returned state_file>"
```

Save a checkpoint summary:

```bash
python3 "$SKILL_ROOT/scripts/record_pdf_checkpoint.py" --state-file "<returned state_file>" --content-file "/path/to/checkpoint-summary.md"
```

Show session progress:

```bash
python3 "$SKILL_ROOT/scripts/summarize_pdf_session.py" --state-file "<returned state_file>"
```

Find the most recent saved PDF session:

```bash
python3 "$SKILL_ROOT/scripts/find_recent_pdf_session.py"
```

## PDF Routing Rules

Default routing by page count:

- `1-40` pages -> `single_pass`
- `41-150` pages -> `segmented_read`
- `151-400` pages -> `long_form_read`
- `401+` pages -> `book_mode`

If multi-window sampling still reports `low_text_pdf = true`, treat the PDF as likely scanned, image-based, or low-quality text.

## Session State Rules

For `segmented_read`, `long_form_read`, and `book_mode`:

1. Initialize state before the first reading step.
2. Read state before continuing.
3. Update state before previous / next / jump actions.
4. Do not rely on chat memory alone in a new session.
5. If state is missing, re-plan or re-initialize instead of pretending progress exists.
6. Prefer returned commands from the planning result whenever available.
7. Restore saved progress by default unless the user explicitly asks to restart.
8. Save every completed segment result immediately.
9. Build checkpoint source material before writing a checkpoint summary.

## Existing Session Behavior

If `plan_pdf_reading.py` returns an `existing_session`:

1. "Continue next segment" should restore state and then move forward.
2. "Resume from last position" should restore state and read the current segment without advancing.
3. "Where am I?" or "reading status" should call `summarize_pdf_session.py`.
4. Only use `--force-reset` when the user explicitly wants to restart from the beginning.

In status summaries, distinguish clearly between:

- total completed segments
- contiguous completion from the beginning
- the earliest incomplete checkpoint window

## Output Structure

Default segment results should use this shape:

1. Source information
2. Content theme
3. Three core ideas
4. Reconstructed structure
5. Key insights
6. Actionable next steps
7. Reusable takeaway

For checkpoints:

1. stage range
2. stage theme
3. core findings
4. reconstructed structure
5. key insights
6. follow-up actions or reading guidance
7. reusable checkpoint takeaway

## Writing Rules

- The model writes the transformation directly.
- Write result content to a temporary markdown file first.
- Then call the correct record script to save it into the official session structure.
- Do not manually write final `segment-XXX.md` or `checkpoint-XXX.md` files unless the record script is intentionally bypassed for debugging.
