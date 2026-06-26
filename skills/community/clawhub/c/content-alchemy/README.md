# content-alchemy

`content-alchemy` is a reading-to-outcome skill for AstronClaw, ClawHub, and GitHub distribution. It does not define itself as a generic summarizer. Instead, it turns articles, web pages, PDFs, and excerpts into structured notes, durable insights, practical actions, and reusable takeaways.

Its goal is not to merely shorten content, but to convert what was read into something that can be retained, reviewed, reused, and acted on.

## Highlights

- Outcome-oriented outputs instead of plain summaries
- One workflow across text, web pages, and PDFs
- Web-first pipeline: extract article text before restructuring it
- Page-aware PDF routing: short PDFs are processed directly, long PDFs are segmented automatically
- Persistent long-PDF reading: continue, resume, jump, and checkpoint summaries
- Saved segment results and saved reading state for multi-session book workflows

## Core Positioning

`content-alchemy` is not a compression tool. It is a content transformation skill that helps users turn reading input into personal outcomes.

That means the output should feel like:

- a note worth saving
- an idea worth revisiting
- an action worth trying
- a takeaway worth reusing

## Supported Inputs

### 1. Plain text

Best for:

- article bodies
- extracted web text
- book excerpts
- long explanatory passages

### 2. Web URLs

Workflow:

1. Extract title, site, author, publication time, and readable text
2. Transform the extracted text into an outcome-oriented result

### 3. PDF files

Workflow:

1. Inspect page count and text quality
2. Choose a reading strategy
3. Extract text from the right page range
4. Transform the extracted content into reusable outcomes

For long PDFs, the skill also supports:

- segmented reading plans
- saved segment results
- checkpoint summaries
- persistent session state
- resume-from-last-session behavior

## Default Output Structure

The default result contains seven blocks:

1. Source information
2. Content theme
3. Three core ideas
4. Reconstructed structure
5. Key insights
6. Actionable next steps
7. Reusable takeaway

The reusable takeaway is the most important differentiator. It makes the result feel like a durable output rather than a disposable summary.

## Long PDF / Ebook Workflow

`content-alchemy` does not try to force long PDFs into a single context window. It routes the document by page count:

- `1-40` pages: `single_pass`
- `41-150` pages: `segmented_read`
- `151-400` pages: `long_form_read`
- `401+` pages: `book_mode`

For very long books, the intended workflow is:

1. Plan the reading strategy
2. Initialize or restore the reading state
3. Read one segment at a time
4. Save each segment result
5. Build checkpoint summaries at configured intervals
6. Resume later without losing progress

## Persistent Session State

Long-PDF reading artifacts are saved under:

```text
~/.content-alchemy/sessions
```

This includes:

- reading plans
- active state files
- segment results
- checkpoint summaries

That enables natural commands such as:

- "Where am I in this book?"
- "Resume from the last position"
- "Continue to the next segment"
- "Jump to the segment that contains page 201"

## CLI Examples

### Extract a web page

```bash
SKILL_ROOT="$HOME/.claude/skills/content-alchemy"
python3 "$SKILL_ROOT/scripts/extract_web_text.py" "https://example.com/article"
```

### Troubleshoot TLS issues

```bash
python3 "$SKILL_ROOT/scripts/extract_web_text.py" "https://example.com/article" --insecure
```

### Plan a PDF reading workflow

```bash
python3 "$SKILL_ROOT/scripts/plan_pdf_reading.py" "/path/to/file.pdf"
```

### Extract a page range from a PDF

```bash
python3 "$SKILL_ROOT/scripts/extract_pdf_text.py" "/path/to/file.pdf" --page-start 1 --page-end 5
```

### Initialize or restore a PDF session

```bash
python3 "$SKILL_ROOT/scripts/update_pdf_session_state.py" init --plan-file "<returned plan_file>" --state-file "<returned state_file>"
```

### Move to the next segment

```bash
python3 "$SKILL_ROOT/scripts/update_pdf_session_state.py" next --state-file "<returned state_file>"
```

### Show progress

```bash
python3 "$SKILL_ROOT/scripts/summarize_pdf_session.py" --state-file "<returned state_file>"
```

### Find the most recent PDF session

```bash
python3 "$SKILL_ROOT/scripts/find_recent_pdf_session.py"
```

## Dependencies

- `python3`
- system `pdftotext`
- system `pdfinfo`

Notes:

- The web extractor uses the Python standard library only
- PDF extraction relies on system PDF text tools
- OCR is not built in; scanned PDFs may still require an OCR step first

## Limits

This version does not directly handle:

- OCR for scanned PDFs
- highly dynamic websites with unstable readable text
- table-first analytical workflows
- code analysis workflows

If text extraction fails or returns sparse output, the skill should say so clearly and ask for OCR or source text instead of pretending the document was understood.

## Examples

See the `examples/` folder for sample prompts and result shapes:

- `input-article.txt`
- `input-url.txt`
- `input-pdf.txt`
- `output-note.md`
- `output-result.md`
- `output-web-result.md`
- `output-pdf-plan.md`
- `output-pdf-result.md`
- `output-pdf-checkpoint.md`

## Repository Layout

```text
content-alchemy/
├── SKILL.md
├── README.md
├── LICENSE.md
├── skill.json
├── agents/
├── scripts/
├── templates/
├── examples/
└── docs/
```

## Release Notes

This repository is the English-source version intended for GitHub and future international ClawHub packaging.

## License

This project is released under the `MIT` license for public distribution and reuse.
