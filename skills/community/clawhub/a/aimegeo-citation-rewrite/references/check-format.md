# Check-plan format

`check_rewrite.py` compares an original Markdown file, a revised file, and a JSON plan. The plan has `schema_version: 1`, `editable_sections`, `sources`, `questions`, and `numeric_claims`.

- `editable_sections`: exact existing H2 heading lines authorized for edits. The script checks that other content and heading order remain stable.
- `sources`: source IDs and user-provided/retrieved excerpts for this revision. The script does not retrieve or authenticate them.
- `questions`: requested prompts and the expected heading/answer block locations. This is a structural presence check only.
- `numeric_claims`: newly added numeric sentences linked to a source ID and excerpt. The script checks textual association, not whether the excerpt proves the claim.

Exit code 0 means the implemented checks passed; 1 means a content/scope check failed; 2 means malformed input or invocation. Human review remains responsible for authorization, factual support, and the quality of the prose.
