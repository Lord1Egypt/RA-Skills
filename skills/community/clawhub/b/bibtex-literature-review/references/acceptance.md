# Acceptance Criteria

Use this file before delivering a generated DOCX.

## Structural Checks

Run:

```bash
python scripts/validate_docx_crossrefs.py output.docx --forbid-hyperlinks --require-ref --require-superscript --require-auto-numbered-bib
```

Required pass conditions:

- At least one `REF _RefBibNNN` field exists.
- No `HYPERLINK` field or `w:hyperlink` points to `_RefBibNNN`.
- REF field cached result runs are superscript.
- Every `_RefBibNNN` bookmark lives in a paragraph with `w:numPr`.
- Bibliography bookmark count equals expected bibliography count when `--expect-bib-count` is passed.

## Skill Package Hygiene

Before considering the skill package itself ready, check:

- No `__pycache__`, `.DS_Store`, temporary JSON, temporary DOCX, rendered PNG/PDF, or scratch files remain in the skill directory.
- `SKILL.md` frontmatter contains only `name` and `description`.
- The folder name matches the skill name.
- Scripts use explicit input/output paths and do not depend on user-specific absolute paths.

Run the isolated regression check with a real BibTeX fixture:

```bash
python scripts/self_check.py --bib /path/to/original-fixture.bib
```

The self-check creates a temporary workspace, builds candidates JSON, generates a review DOCX, validates strict REF/autonumbering requirements, inspects DOCX XML, and then removes the temporary workspace unless `--keep-temp` is used.

## XML Spot Checks

```bash
rm -rf /tmp/docx_check && mkdir -p /tmp/docx_check
unzip -q output.docx -d /tmp/docx_check
rg 'REF _RefBib[0-9]+' /tmp/docx_check/word/document.xml
rg '<w:hyperlink' /tmp/docx_check/word/document.xml
rg '<w:numPr>' /tmp/docx_check/word/document.xml
rg '<w:bookmarkStart[^>]*w:name="_RefBib' /tmp/docx_check/word/document.xml
```

## Visual Checks

Code-level OOXML validation is required. Visual validation is strongly recommended when the environment can render DOCX pages.

Render the DOCX and inspect page PNGs when a renderer is available:

- title and body text are visible.
- citations appear in the body and are superscript.
- single citations show `[1]`, not blank, `{ REF ... }`, or `[[1]]`.
- ranges and groups show correctly, such as `[3-5]` and `[10,11]`.
- reference list numbering is visible and aligned.
- no page has text overlap, clipping, or large accidental blank gaps.

If the active AI environment supports multimodal image inspection, inspect the PNG pages directly before delivery. If PNG rendering or multimodal inspection is unavailable, state that only structural code validation was completed.

## Manual Word Checks When Needed

If the user is specifically verifying Word field codes:

- Open Word.
- Toggle field codes with `Option+F9` on macOS or `Alt+F9` on Windows.
- Confirm fields are `REF`, not `HYPERLINK`.
- Confirm clicking a body citation jumps to the relevant bibliography entry.

If field results differ after opening in Word, run "Update Field" and re-check. The robust hidden-anchor pattern should remain stable.
