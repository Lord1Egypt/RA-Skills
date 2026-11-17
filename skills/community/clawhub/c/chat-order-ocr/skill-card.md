## Description:

Extracts and groups chat orders from pasted LINE/Facebook messages or local OCR text, then produces reviewable JSON or CSV order lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qpooqp777](https://clawhub.ai/user/qpooqp777)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and developers use this skill to turn chat preorder messages, pasted OCR text, or locally OCRed screenshots into reviewable order rows. It supports grouping by customer, catalog alias matching, sorting, and JSON or CSV export for fulfillment checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSV exports opened in spreadsheet software may interpret crafted chat text as formulas.

Mitigation: Prefer JSON for exact records, or sanitize CSV cells before opening or sharing them in spreadsheet tools.

Risk: Screenshots used for OCR may contain unrelated personal or sensitive content.

Mitigation: Review and crop screenshots before OCR, and choose output paths deliberately.

Risk: OCR text, unmatched catalog aliases, and ambiguous rows can produce incorrect names, items, quantities, or duplicate rows.

Mitigation: Keep rows marked with confidence check and manually verify them before fulfillment or export.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qpooqp777/skills/chat-order-ocr)
- [CLI examples](references/cli_examples.md)
- [Catalog example](references/catalog.example.json)
- [Complex chat fixture](references/complex_chat_fixture.txt)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with CLI commands; generated artifacts are JSON or UTF-8 BOM CSV files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Order rows include person, item, matched_item, quantity, source, source file, match status, and confidence; OCR or unmatched rows are marked for manual review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
