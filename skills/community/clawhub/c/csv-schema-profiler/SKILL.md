---
name: csv-schema-profiler
description: >
  Profile a CSV paste: headers, null-ish rates, example values, and suspected
  types. Use when exploring an unfamiliar export before writing transforms.
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":[]}}}
---

# CSV Schema Profiler

## Purpose / Overview
Give a quick structural read on tabular text so the user knows columns, messy
values, and likely types before writing code.

## When to Use
- First look at a vendor CSV
- Deciding parse options (delimiter, header row)
- Spotting ID vs numeric vs date columns

## Usage / Instructions
1. Ask for a CSV paste (header + sample rows). If huge, ask for header + ~20 rows.
2. Detect delimiter (comma/semicolon/tab) from the header line; state the guess.
3. Parse rows conservatively; note if any row has a different column count.
4. For each column report:
   - name
   - suspected type (string / int / float / bool / date / id / empty)
   - null-ish count (`""`, `NA`, `null`, `N/A`)
   - 2–3 example distinct values
5. Flag columns that look like emails, phones, or tokens — recommend redaction
   before sharing further.
6. Mention duplicate headers or unnamed columns (`Unnamed: 0`).
7. Suggest 3 cleaning steps prioritized by impact (trim, date parse, typed IDs).
8. If the user wants a pandas dtypes sketch, provide it as optional code, not
   required.
9. Do not assume encoding beyond what the paste shows; mention mojibake if seen.
10. End with a one-paragraph "schema summary" suitable for a ticket.
11. Keep answers structured with short headings so the user can skim.
12. If information is missing, ask at most two clarifying questions before guessing.
13. Prefer concrete commands or checklists the user can copy.
14. Call out assumptions explicitly when the environment is unknown.
15. Refuse to invent tool output you did not see; ask for a fresh paste instead.
16. When offering optional follow-ups, keep them clearly optional.
17. Stay within this skill's scope; suggest a different task type if the request drifts.
18. End with a brief "done when" criterion so the user knows success.


## Examples
Orders export with `order_id`, `total`, `created_at`
→ id/string, float/int, date; note empty totals; suggest parse dates.

## Requirements / Dependencies
None. Optional later code uses the user's own Python environment.

## Limitations / Caveats
Small samples mis-type rare columns. Nested CSV quoting edge cases may need a
real parser.

## Security / Permissions
Treat CSV contents as sensitive. Do not invent external uploads.

## Description

Profile a CSV paste: headers, null-ish rates, example values, and suspected types.

## License or terms

MIT

## Use case

Use when you are the operator responsible for tasks described as: Profile a CSV paste: headers, null-ish rates, example values, and suspected types.

## Risks and mitigations

## References

None readily identified for this skill.

## Ethical considerations

Illegal use of this skill is not allowed. The publisher will not be accountable for outcomes arising from unlawful use under country or international law. Prohibited examples include breaking into accounts without authorization, deploying ransomware, and trafficking in stolen personal data. Misuse against third-party systems without authorization is illegal.
