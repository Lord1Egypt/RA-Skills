# Accounting & Finance System Research Skill

Codex skill for handling accounting/finance system "how-to" and troubleshooting questions with a clarification-first workflow, web research, analysis, and DOCX deliverables.

## What It Does

- Ask required clarifying questions before solutioning.
- Confirm deliverable format as either:
- `quick memo`
- `simple q-and-a`
- Confirm understanding before internet research.
- Research official system documentation and consultant publications.
- Produce actionable guidance with assumptions, risks, and validation checks.
- Generate `.docx` output from structured JSON.

## Skill Contents

- `SKILL.md`: Workflow and behavior rules.
- `references/`: Clarification bank, source hierarchy, schema, and example payload.
- `scripts/build_system_guidance_docx.py`: DOCX generator (`memo` or `q-and-a`).
- `agents/openai.yaml`: UI metadata for skill listing.

## Usage

1. Trigger with `$accounting-finance-system-research`.
2. Collect missing facts and confirm format with the user.
3. Research relevant official and secondary sources.
4. Build a JSON payload matching `references/report-json-schema.md`.
5. Generate document:

```bash
python scripts/build_system_guidance_docx.py \
  --input-json references/example_report_input.json \
  --output-docx system-guidance.docx \
  --format memo
```

## Dependency

```bash
python -m pip install --user python-docx
```

## License

MIT. See [LICENSE](LICENSE).
