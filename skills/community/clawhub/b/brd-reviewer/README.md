# BRD Reviewer Skill

`brd-reviewer` is a Codex skill for reviewing Business Requirements Documents in Word format. It extracts paragraph-level review units from an existing BRD, lets Codex draft clarification questions for unclear points, and materializes a final `.docx` with Word comments and tracked changes in the same file.

## Repository layout

- `brd-reviewer/`: Installable skill folder.
- `brd-reviewer/scripts/brd_review_pipeline.py`: Paragraph extraction and DOCX materialization pipeline.
- `brd-reviewer/references/review-json-schema.md`: Review JSON field guide.

## Typical workflow

1. Run `init-review` on the source BRD `.docx`.
2. Fill the generated JSON with paragraph-level questions and proposed wording.
3. Run `materialize` to generate `<name>.reviewed.docx`.
4. Install `brd-reviewer/` into `$CODEX_HOME/skills` to use it locally.

## License

MIT. See [LICENSE](./LICENSE).
