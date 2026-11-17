# Dialogue Billing Report Specification

Write the report in chat as Markdown or plain text. Use only API fields you received or data you can fully check in the current session.

Include the query scope and sources, an amount summary with source field, basis, and currency, the smallest useful cost breakdown, checks and evidence, data-backed issues and open items, and limits. Do not fill missing amounts with zero or estimates. A price change alone does not prove an overcharge or a resource problem.

Use one label for each important amount or conclusion:

- `Direct bill API value`: returned by a bill API.
- `Checked calculation`: calculated from complete visible data; state the inputs, scope, and basis.
- `Partial data`: the scope, pages, or resource link is incomplete.
- `Cannot determine`: needed data is missing.

Do not use a fixed row or money limit. The strength of a conclusion depends on complete data and a checkable method.
