---
name: generate-import-template-data
description: Generate import-ready data from user-provided Excel or CSV import templates based on the customer's described business scenario. Use when Codex receives an uploaded template, workbook, or CSV and the user asks to generate, fill, mock, fabricate, prepare, or output corresponding template data, sample rows, initialization data, test data, or import content. This skill must be used whenever the user uploads a template and requests corresponding template data generation.
---

# Generate Import Template Data

Generate data that can be pasted into or saved as the user's import template while preserving the template's actual column names, order, sheet choice, and business meaning.

## Workflow

1. Inspect the uploaded template before generating any data.
   For `.xlsx`, `.xlsm`, `.csv`, or `.tsv`, run `scripts/inspect_template.py` to identify candidate sheets, header rows, and sample structure.
2. Identify the true import target.
   Prefer the sheet that contains business headers over instruction sheets such as `填表说明`, `字段说明`, `模板说明`, `数据字典`, or `示例`.
3. Extract the scenario requirements from the user request.
   Capture the business entity, row count, edge cases, required statuses, date ranges, amounts, codes, and whether the user wants realistic data, extreme test data, or minimum valid data.
4. Map the scenario to columns conservatively.
   Use explicit template names and nearby notes. If a field meaning is ambiguous, state the assumption instead of fabricating hidden business logic.
5. Generate import-ready rows.
   Keep the exact column order. Do not add extra columns. Respect apparent code formats, identifier lengths, enum-like values, and date formats already shown by the template.
6. Validate before returning.
   Re-check that every generated row aligns with the header set, obvious formatting expectations, and any instruction-sheet constraints visible in the workbook.

## Generation Rules

- Preserve the original header text exactly.
- Preserve the target sheet name when returning workbook-oriented results.
- Prefer realistic data that matches the user's described customer scene instead of generic placeholders.
- If the template includes examples, mimic their format but do not duplicate values blindly.
- If the workbook contains instruction sheets, read them before generating data.
- If the user requests "template data" without row count, default to 10 rows unless the template clearly implies a smaller fixed sample.
- If the request is for a single scenario, keep all rows internally consistent with that scenario.
- If the request is for testing coverage, include a balanced set of normal rows plus a small number of boundary rows only when the user asked for them.
- Do not invent mandatory codes, dictionaries, or foreign keys when the template suggests an external source is required. In that case, either ask for the missing mapping or clearly label the assumption.

## Output Style

- Prefer returning a Markdown table only for very small outputs.
- Prefer fenced `csv` blocks for tabular data the user can copy directly.
- When working with a spreadsheet file in the workspace, write the generated rows into a new output file instead of overwriting the original template unless the user asked for in-place filling.
- Briefly state the chosen sheet, detected headers, row count, and any assumptions that materially affect import success.

## Template Inspection

Run:

```powershell
python scripts/inspect_template.py --input <template-file>
```

Optional flags:

- `--sheet <name>` to inspect one Excel sheet
- `--json` to print compact machine-readable output

Use the script output to confirm:

- candidate import sheet
- detected header row
- exact header names
- sample rows or preview cells

## Ambiguity Handling

- If the scenario is missing, ask only for the minimum business details needed to generate rows that are not meaningless.
- If multiple sheets look importable, say which one you chose and why.
- If a field cannot be inferred safely, keep the assumption explicit in the final answer.
- If the template appears to require strict validation rules, read [references/generation-guidelines.md](references/generation-guidelines.md) and tighten the output accordingly.

## References

- Read [references/generation-guidelines.md](references/generation-guidelines.md) for scenario-to-field mapping guidance and common output checks.
- Run `scripts/inspect_template.py` before generating data from a new template structure.
