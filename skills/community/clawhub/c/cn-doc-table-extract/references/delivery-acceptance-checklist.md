# Pre-Delivery Acceptance Checklist / 交付前验收清单

Run this checklist before handing an extraction to a downstream system, a
spreadsheet, or a reviewer. Every line is a yes/no with a defined failure action.
Do not deliver with an unchecked line that is marked **BLOCKER**.

A result is deliverable only when: every BLOCKER line passes, every WARN line has
either passed or been explicitly accepted in writing by the requester, and the
report contains no `error`-level issue.

---

## 1. Source integrity

| # | Check | Pass criterion | If fail | Level |
|---|---|---|---|---|
| 1.1 | File opens | The extractor reported the file type, page/sheet count, and no read error | Stop; report the library error | BLOCKER |
| 1.2 | Whole file covered | Every page (PDF) or sheet (xlsx) appears in the extraction report | Re-run with the missing pages/sheets included | BLOCKER |
| 1.3 | Encrypted / password protected | Detected and reported explicitly, not silently skipped | Ask for a decrypted copy | BLOCKER |
| 1.4 | Table count plausible | `tables_detected + tables_rejected` equals the number of table regions the tool enumerated | Inspect the rejected list | WARN |
| 1.5 | No low-confidence table unacknowledged | Every `low_confidence: true` table has a note and a human decision | Re-scan or read manually | WARN |

## 2. Structural completeness

| # | Check | Pass criterion | If fail | Level |
|---|---|---|---|---|
| 2.1 | Header detected | `header_detected: true` for the tables you treat as data tables | Confirm the column mapping manually, then fix the alias table | BLOCKER |
| 2.2 | No synthetic headers in delivery | No `列1/列2` names in a delivered record set | Add the alias and re-extract | BLOCKER |
| 2.3 | Row count reconciled | The extracted row count matches the row count visible in the source, per table | Look for dropped rows, merged-cell drops, or a footer row counted as data | BLOCKER |
| 2.4 | Repeated headers removed | `dropped_header_rows` counts them, and none remain as data | Inspect for a header that was not recognized | WARN |
| 2.5 | Footer rows separated | 合计/小计/总计 rows are in `footer_rows`, not in detail rows | Move them in the post-processing step | BLOCKER |
| 2.6 | No continuation duplication | Continuation tables across pages are merged and the repeated header dropped | Fix per D3/E3 in the traps reference | WARN |

## 3. Field-level validation

| # | Check | Pass criterion | If fail | Level |
|---|---|---|---|---|
| 3.1 | Required fields present | Zero `required_field_missing` issues | Report which fields are missing and on which records | BLOCKER |
| 3.2 | Amounts parse | Zero `invalid_amount` issues | Fix the source or the unit; never coerce to 0 | BLOCKER |
| 3.3 | Amount signs sensible | No `unexpected_sign` on a field type that forbids negatives | Check 借贷方向 columns and reversal rows | WARN |
| 3.4 | Zero amounts legitimate | Every `amount == 0` is explained (a `-` placeholder, a waived line) | A real zero and a missing value look identical — disambiguate | WARN |
| 3.5 | Dates parse | Zero `invalid_date` issues | Fix impossible dates such as `2024年2月30日` | BLOCKER |
| 3.6 | Ambiguous dates flagged | Every `ambiguous_date` is resolved by a human or left null | Do not auto-pick an interpretation | WARN |
| 3.7 | Date ranges sane | `effective_date` ≤ `expiry_date`; statement dates inside the stated period | Check `date_range_inverted` | WARN |
| 3.8 | Identifier shapes | Invoice numbers are 8 or 20 digits; codes are 10 or 12; no letters in a numeric id | Check for an O/0 confusion and for a value pasted into the wrong column | BLOCKER |
| 3.9 | Identifier uniqueness | No duplicate primary key inside one document | Decide keep-both vs error — never silently drop | WARN |

## 4. Reconciliation

| # | Check | Pass criterion | If fail | Level |
|---|---|---|---|---|
| 4.1 | 价税合计 additive | `amount + tax_amount ≈ total_amount` within tolerance | Report the three values and the difference; do not repair the row | BLOCKER |
| 4.2 | Tax rate consistent | `amount × tax_rate ≈ tax_amount` within tolerance | Report the mismatch; do not back-solve a rate | WARN |
| 4.3 | Detail sum vs 合计 | The sum of detail rows matches the printed 合计 within tolerance | Report both sides and the difference; walk the E2 checklist | WARN |
| 4.4 | Subtotals additive | 本页小计 rows add up to the grand total when both exist | Check for a row that continues on the next page | WARN |
| 4.5 | Payroll arithmetic | `gross − deductions ≈ net` | Report the mismatch; check whether a component is missing | WARN |
| 4.6 | Currency assumed and stated | Every amount field's currency is stated (default RMB) | State the assumption in the report header | WARN |
| 4.7 | Unit conversions recorded | 万元 (10k yuan) conversions are recorded in `notes` with the multiplier | Unrecorded conversions silently corrupt totals | BLOCKER |

## 5. Traceability

| # | Check | Pass criterion | If fail | Level |
|---|---|---|---|---|
| 5.1 | Every field has evidence | No field is missing `evidence` | Mark it `unverified` and list it | BLOCKER |
| 5.2 | Evidence coordinates resolve | Spot-check 10 random fields: open the source at the cited page/row/column and confirm the value | Fix the coordinate mapping | BLOCKER |
| 5.3 | `raw` is untouched | `raw` equals the source cell string byte-for-byte after only whitespace trimming | Fix the normalizer | BLOCKER |
| 5.4 | Unverified list is short | `unverified_fields` is empty, or every entry has a stated reason | Any unexplained unverified field blocks delivery | WARN |
| 5.5 | Outside-table values marked | Layout-level values (invoice footer totals) carry `outside_table: true` | Add the flag | WARN |
| 5.6 | Cross-document claims cite both sides | Every reconciliation between two documents cites both ids | Fix the citation | WARN |

## 6. Privacy and delivery hygiene

| # | Check | Pass criterion | If fail | Level |
|---|---|---|---|---|
| 6.1 | PII masked in the human view | 身份证号 masked to the last 4 characters | Re-generate the view | BLOCKER |
| 6.2 | Raw PII not in the chat | The conversation holds only masked values unless the user explicitly asked for raw | Remove | BLOCKER |
| 6.3 | Document type noted | The profile used is stated in the output header | Add it | WARN |
| 6.4 | Profile assumption stated | Any inferred profile is labelled as an assumption | Add the note | WARN |
| 6.5 | Validation status stated | `pass` / `pass_with_warnings` / `blocked` / `not_run` appears in the header | Add it | BLOCKER |
| 6.6 | No overclaiming | The delivery text makes no completeness or accuracy promise | Rewrite the wording | BLOCKER |
| 6.7 | Tool version recorded | The extractor and validator versions appear in the report | Add them | WARN |
| 6.8 | Temp files cleaned | Intermediate files (renders, page images) removed or listed | Clean up | WARN |

## 7. Sign-off block

Copy this into the delivery message and fill every line. A delivery without a
completed block is not a delivery.

```
Extraction acceptance
source_file        : <file name> (<type>, <pages/sheets> pages/sheets)
profile            : <profile key>  [confirmed by user | assumed - stated above]
tables_detected    : <n>   tables_rejected: <n>   records: <n>
coverage           : <all pages/sheets covered | pages X-Y only>
validation_status  : <pass | pass_with_warnings | blocked | not_run>
issues_error       : <n>   issues_warning: <n>   issues_info: <n>
unverified_fields  : <n> (list or "none")
reconciliation     : <total check result: matched / mismatch by X / not applicable>
low_confidence     : <list or "none">
privacy            : <PII masked yes/no>
reviewer           : <name>   date: <YYYY-MM-DD>
outstanding        : <what a human must still check, or "none">
```

---

## 8. Known-good sample

`EXAMPLE.md` in this package shows a complete run against a synthetic invoice
statement: the input, the extraction table, the JSON record set, the validator
output with two triggered rules, and the acceptance block. Use it as the reference
shape for a delivery.
