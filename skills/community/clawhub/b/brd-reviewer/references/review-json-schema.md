# Review JSON Schema

Use this file only when populating the intermediate review JSON.

## Top-level fields
- `source_docx`: Source BRD path.
- `prepared_at_utc`: Timestamp from the initializer.
- `reviewer`: Optional reviewer name.
- `overall_notes`: Optional high-level review notes.
- `paragraphs`: Ordered list of paragraph review units.

## `paragraphs[]` fields
- `paragraph_index`: Zero-based index in `word/document.xml`. Do not change.
- `style_id`: Word paragraph style identifier. Do not change.
- `heading_path`: Closest heading hierarchy used for context. Do not change.
- `source_text`: Visible paragraph text. Do not change.
- `issue_tags`: Array of short reason tags.
- `needs_comment`: `true` when the paragraph needs a Word comment.
- `comment_question`: The exact clarification question for the comment balloon.
- `needs_revision`: `true` when the paragraph should receive tracked replacement text.
- `proposed_replacement`: Full replacement paragraph text used for the tracked change.

## Authoring rules
- If `needs_comment` is `true`, `comment_question` must be non-empty.
- If `needs_revision` is `true`, `proposed_replacement` must be non-empty.
- A paragraph may have both a comment and a revision.
- Leave `needs_comment` and `needs_revision` as `false` when no action is needed.
- Keep `issue_tags` short and machine-friendly.
