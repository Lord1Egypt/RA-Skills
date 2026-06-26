# Word Assembly Plan

Use this reference after the content is drafted and before generating or handing off the final `.docx`.

## Purpose

The assembly plan turns the delivery brief and format profile into an executable Word job.

It answers three questions:

1. Is the job ready for a draft Word file or a final Word deliverable?
2. Which package components must be included?
3. Which blockers or unresolved confirmations still prevent final delivery?

## Inputs

Use these two inputs together:

- delivery brief from [word-delivery-brief.md](word-delivery-brief.md)
- format profile from [word-format-profile.md](word-format-profile.md)

Do not assemble a final Word file from format rules alone.

## Readiness gates

### Minimum for Word draft assembly

These fields must be resolved:

- `source_authority`
- `target_structure`
- `document_purpose`
- `audience`
- `output_mode`

If these are missing, the task is not ready even for a reliable draft `.docx`.

### Minimum for final Word delivery

These must also be resolved:

- `delivery_stage` set to final
- `completeness_scope`
- `review_mode`
- `format_authority`
- `file_naming_and_version`
- any format confirmation blocker

If any of these remain open, stop at internal draft output.

## Package components

Derive package components from `completeness_scope`.

Common components:

- `body`
- `cover`
- `table-of-contents`
- `appendices`
- `glossary`
- `figure-list`
- `table-list`
- `attachments-manifest`

### Default derivation

- If `completeness_scope` is `body-only draft`, include `body` only.
- If `completeness_scope` says `full-deliverable`, include at least `body`, `cover`, and `table-of-contents`.
- Add appendices, glossary, lists, or attachments only when the brief or template requires them.

## Review artifact mode

Map `review_mode` into the actual output behavior:

- `clean-copy`: deliver a clean Word document
- `tracked-changes`: preserve reviewable edits in the final file
- `comments`: keep comments for review rather than silent edits

For third-party or formal documents, default to `tracked-changes` or `comments` unless the user explicitly asks for a clean copy.

## Cleanup rule

Before final delivery, decide whether to remove:

- evidence notes
- source markers
- TODO markers
- working comments
- traceability hints

Do not assume these can stay in the final file unless the user explicitly wants an internal review artifact.

## Practical rule

Final Word generation is not the same as text export. It is a controlled packaging step with entry criteria.

If the package is not ready, emit blockers instead of forcing a half-specified `.docx`.

## Tooling

Use [scripts/resolve_word_job.py](../scripts/resolve_word_job.py) to generate a first-pass readiness report and assembly plan.

Use [scripts/generate_docx_from_markdown.cjs](../scripts/generate_docx_from_markdown.cjs) to turn resolved Markdown, the delivery brief, and the format profile into an actual `.docx` file.
