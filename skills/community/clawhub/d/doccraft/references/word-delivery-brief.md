# Word Delivery Brief

Use this reference when the task is not just "write some text" but "deliver a complete Word document".

## Purpose

The delivery brief is the contract for Word output. It separates:

- what the user must specify before drafting can start
- what the user must confirm before the final `.docx` can be delivered

Without this split, teams either block too early on formatting trivia or ship incomplete Word files that still need structural decisions.

## User must specify before drafting

These items determine whether content generation can begin safely:

- `document_title`: the working or final document title
- `source_authority`: which files or folders are the factual basis
- `target_structure`: required outline, template, or existing target document
- `document_purpose`: what the document is meant to accomplish
- `audience`: who will read or review it
- `output_mode`: new document, rewrite from sources, or edit existing `.docx`

If any of these are missing, use the smallest safe assumption and record it as a working note.

## User must confirm before final Word delivery

These items determine whether the final `.docx` is complete and deliverable:

- `completeness_scope`: cover, table of contents, appendices, glossary, figure list, table list, attachments
- `review_mode`: clean copy, tracked changes, or comments
- `format_authority`: template, explicit spec, accepted sample, or default profile
- `file_naming_and_version`: output filename, version label, date label, or package naming rule
- `cleanup_rule`: whether source markers, TODOs, evidence notes, or traceability hints must be removed

Do not treat these as optional if the file is an external or formal deliverable.

## Safe defaults

Use these defaults when the task is still in drafting mode and the user has not confirmed the final package yet:

- `completeness_scope`: body-only draft
- `review_mode`: clean copy for drafting, no tracked changes yet
- `format_authority`: default profile from [word-format-profile.md](word-format-profile.md)
- `cleanup_rule`: keep working notes outside the final body

These defaults allow text work to continue, but they do not authorize final Word delivery.

## Confirmation timing

Ask for confirmation:

- before generating the final `.docx`
- before editing a third-party `.docx` in a way that affects review mode
- whenever the output must satisfy an institutional submission format

Do not ask too early:

- if the task is still gathering sources
- if the current output is only Markdown or text
- if the user already supplied a template and a target document shape

## Minimal delivery-brief payload

Use a short structured note or file with these fields:

- `document_title`
- `source_authority`
- `target_structure`
- `document_purpose`
- `audience`
- `output_mode`
- `delivery_stage`
- `completeness_scope`
- `review_mode`
- `format_authority`
- `file_naming_and_version`
- `cleanup_rule`
- `open_questions`

## Practical rule

Do not ask the user broad questions like "What else do you want in the Word file?"

Instead, present the resolved delivery brief with defaults filled in and ask the user to confirm only the unresolved or high-risk items.

## Tooling

Use [scripts/init_delivery_brief.py](../scripts/init_delivery_brief.py) to generate a first-pass delivery brief.
