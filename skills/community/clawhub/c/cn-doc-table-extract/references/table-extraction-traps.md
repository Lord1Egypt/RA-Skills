# Table Extraction Traps and Countermeasures / 常见表格与 OCR 陷阱及应对

Symptom → root cause → what the tool does → what a human must still check.

---

## A. PDF-specific traps

### A1. Every cell is empty, but the PDF is not blank

**Cause.** The PDF has a text layer produced by a vector-to-outline converter or a
non-standard CMap. `page.extract_text()` returns empty or mojibake while the glyphs
render fine on screen.

**Tool behavior.** `extract_tables.py` counts usable cells per table. A table whose
usable-cell ratio is below 50% is emitted with `low_confidence: true` and a note
`vector_text_no_table_structure`, not as an empty success.

**Human check.** Confirm whether ruling lines exist. If the source is genuinely a
vector text layout (no ruling lines), the table structure must be reconstructed from
text coordinates, and that reconstruction should be reviewed by a person.

### A2. A table is split into many one-row fragments

**Cause.** Ruling lines are broken by scan noise, or the PDF uses clipped cell borders
so `pdfplumber` sees disconnected line segments.

**Tool behavior.** Fragmented tables are merged when their bounding boxes are
vertically adjacent (gap < 0.5 × median row height) and their column counts match.
Merged fragments are recorded in `merged_fragments` so the merge is auditable.

**Human check.** Look at whether the merged result interleaves two logical tables that
happened to share a column count.

### A3. Merged header cells shift every data column

**Cause.** A title row spans all columns (`跨列标题`), and the real header sits below
it.

**Tool behavior.** The header detector scans the first 5 rows and picks the row with
the most distinct non-empty cells that is not purely numeric. A spanning title row
scores 1 (one merged cell) and loses to a 6-column header row.

**Human check.** Verify the header-to-column mapping visually once per document type;
after that, reuse the same mapping.

### A4. A trailing 合计 row is swallowed

**Cause.** The 合计 row uses merged cells or no vertical ruling, so the table engine
excludes it from the table body.

**Tool behavior.** After the main table is found, the extractor scans the region below
the table for a row whose first cell matches `合计|小计|总计|共计|合 计|金额合计|总金额`.
Such a row is captured as a `footer_rows` entry, kept separate from detail rows, and
still reconciled against the detail sum.

**Human check.** Verify that the captured 合计 belongs to this table and not to the
next one. When a document has two consecutive tables, the 合计 of table 1 may sit
physically closer to table 2.

### A5. Numbers split across two text runs

**Cause.** In a vector PDF, `1,234.56` may be emitted as `1,234` + `.56` in separate
text objects.

**Tool behavior.** Cell text is concatenated with no separator, then re-split by the
table engine's column boundaries. When a cell value ends with a digit and the next
cell starts with `.` followed by digits, the extractor merges them and records
`rejoined_numeric_cells`.

**Human check.** Watch for values that look plausible but lost a digit — check the
digit count against the neighbouring column.

### A6. Negative amounts lost their sign

**Cause.** The minus sign is drawn as a separate glyph, or the PDF writes it in a
different font that maps to a private-use codepoint.

**Tool behavior.** Any cell whose parsed value is non-negative while the raw string
contains a `-` before the first digit, or contains `(...)`, is re-checked and a
`warning` `possible_lost_sign` is raised.

**Human check.** Confirm the sign against the 借贷方向 column: Chinese statements
sometimes express direction in a separate column rather than in the sign.

---

## B. OCR / scan traps

### B1. Full-width characters mixed with half-width

**Cause.** OCR engines return `（`, `）`, `：`, `．`, `，`, `￥` and full-width digits
`０-９` inconsistently, sometimes within one document.

**Tool behavior.** Every extracted string goes through a full-width → half-width
normalization pass before matching, while `raw` keeps the original. A cell that is
entirely full-width digits normalizes cleanly; a cell that mixes them is flagged
`info` `fullwidth_mixed`.

**Human check.** If a *name* field contains full-width characters, do not normalize
it — a Chinese company name legitimately uses full-width punctuation.

### B2. Decimal point read as a comma, or thousands separator invented

**Cause.** The scan is low-DPI; `1,234.56` may be read as `1.234,56` or `1 234 56`.

**Tool behavior.** The amount parser accepts the Chinese/US format (comma = thousands,
dot = decimal) and the European format (dot = thousands, comma = decimal) only when
the pattern is internally consistent. `1,2,3` and `1.2.3` are always rejected. An
amount whose grouping is inconsistent with both conventions is reported as
`warning` `ambiguous_amount_format` and keeps `raw`.

**Human check.** Compare the total against the invoice's 价税合计 — a 1000× error is
usually this trap.

### B3. `0` vs `O` vs `D` vs `〇`

**Cause.** OCR confuses digit zero with the Latin letter O, with `D`, and with the
Chinese zero `〇`.

**Tool behavior.** Inside an identifier field, `O`/`D`/`o`/`Q` are normalized to `0`
only when the field's other characters are all digits and the field is declared an
identifier. For a `金额` field, `O` in a numeric position is an error, not a zero.

**Human check.** Invoice numbers are the field most affected by this trap. If the
digit count matches the expected 8 or 20 but the characters look odd, verify against
the source image.

### B4. Missing characters in a thin-stroke font

**Cause.** The `1`, `7`, `4` in the header font lose strokes, or the cell is too small
for the resolution.

**Tool behavior.** Detect via a heuristic: an identifier whose length is one short of
the expected length for its profile (19 digits where 20 are expected) raises
`warning` `identifier_length_short`.

**Human check.** Do not pad the value. Re-scan at a higher DPI.

### B5. A ruled table scanned without visible ruling

**Cause.** Some Chinese receipts and 电子发票 are printed without borders.

**Tool behavior.** Without ruling lines, no table is detected. The extractor reports
`no_table_structure` and, if the page has aligned text columns, prints the detected
text blocks with their bounding boxes so a human or a layout model can rebuild the
grid. It does not guess the grid.

**Human check.** Rebuild with a layout-aware method, then re-run the validator.

### B6. The seal (印章) overlaps the numbers

**Cause.** A red circular seal overlaps the 合计 area, and OCR reads seal strokes as
digits.

**Tool behavior.** Cells whose extracted text contains a high ratio of characters that
belong to no plausible token class are marked `low_confidence` and excluded from
automatic sums.

**Human check.** Read those cells from the image manually. A seal over an amount is a
classic place for a wrong digit.

---

## C. Spreadsheet (XLSX) traps

### C1. Merged cells hold the value only in the top-left cell

**Cause.** `openpyxl` returns `None` for the other cells of a merged range.

**Tool behavior.** `extract_tables.py` fills merged ranges from their top-left anchor
value and records `merged_filled: true` on the affected records.

**Human check.** If the merged cell was a title spanning a row, filling every column
with it creates a bogus row of the title text. The tool drops rows where more than
80% of the cells carry the same filled value.

### C2. Amounts stored as text, with a trailing space or a unit suffix

**Cause.** Numbers imported from a PDF often arrive as `"1234.56 元"` or `"1,234.56 "`.

**Tool behavior.** The amount parser strips recognized units and whitespace. If a
cell cannot be parsed at all, it is flagged rather than coerced to 0.

**Human check.** A cell that parses as 0 because it was really `—` or `-` is a
missing value, not a zero.

### C3. Multiple sheets where only one holds the statement

**Cause.** Workbooks often carry 说明 (instructions), 封面 (cover) and 汇总 (summary)
sheets before the data sheet.

**Tool behavior.** The extractor walks all sheets, records each sheet's name and
dimensions, and reports which sheets produced tables. `--sheet` restricts the run.

**Human check.** The first sheet is frequently not the data sheet. Read the sheet
list before assuming.

### C4. Date cells that are real datetimes, text, or Excel serials

**Cause.** `openpyxl` returns `datetime` objects for real dates and strings for
everything else.

**Tool behavior.** `datetime` objects are formatted to ISO. Strings go through the
date parser. An Excel serial number that appears as a bare 5-digit integer is not
auto-converted — it is flagged `info` `possible_excel_serial` because it is
ambiguous with an ordinary amount.

### C5. Hidden rows and filtered-out rows

**Cause.** The user hid rows before exporting.

**Tool behavior.** Hidden rows are extracted but each record carries a `hidden: true`
flag.

**Human check.** Confirm whether the hidden rows are intentional (for example a
subtotal block) before including them in a reconciliation.

---

## D. Word (DOCX) traps

### D1. Paragraph lists that look like tables

**Cause.** The document uses tabs or full-width spaces for alignment, with no Word
table object.

**Tool behavior.** `python-docx` finds no tables. The extractor reports
`no_table_structure` and lists the paragraphs. It does not convert paragraphs into
a table, because alignment-based reconstruction is exactly where silent corruption
comes from.

**Human check.** If the user confirms the paragraphs are a table, convert them
deliberately and then validate.

### D2. Text boxes and floating shapes

**Cause.** Key fields (发票号码, 保单号) are often in a text box in the header.

**Tool behavior.** Text boxes are not in `document.tables`. The extractor walks the
document XML for `w:txbxContent` blocks and emits them as `text_blocks` with their
paragraph text, marked as `outside_table: true`. These can be used for field
lookups but never as row records.

**Human check.** Cross-check the header text block against the invoice body; a
mismatch usually means two different documents were merged into one file.

### D3. A table split across pages

**Cause.** A long table continues into the next section.

**Tool behavior.** Each Word table is one unit; continuation tables are separate
records sets. The extractor flags adjacent tables with identical header rows as
`continuation: true` so the validator can treat them as one logical table.

**Human check.** A repeated header row on a continuation table should not be counted
as a data row.

---

## E. Cross-document traps

### E1. The same transaction appears twice legitimately

**Cause.** A statement lists a transfer and its reversal, both with the same date
and amount.

**Tool behavior.** Duplicate detection keys on `date + amount + counterparty +
direction`. An exact key collision raises `warning` `duplicate_detail_row`, and the
report includes both row indices so a human can decide.

**Human check.** Reversal pairs are normal. Silent deletion is not; the tool never
deletes a duplicate row, it only flags it.

### E2. Totals that do not reconcile

Checklist of the usual causes, in order of likelihood:

1. A detail row continues on the next page and was not extracted → check whether the
   last row of page N and the first row of page N+1 are one logical row.
2. A 退款 (refund) row was excluded by a sign filter.
3. The 合计 includes a fee (手续费, 工商银行 typically adds 手续费) that is not a detail
   row.
4. The 合计 is for a subset (本页小计) rather than the whole document.
5. A currency conversion is embedded: the statement shows USD and the 合计 is in RMB.

The tool reports the two sides and the difference. It never edits a detail row to
make the sum work, and never substitutes a computed sum for the printed 合计.

### E3. Column headers that differ between pages of the same statement

**Cause.** Page 3 uses 借方金额 while page 5 uses 借方发生额.

**Tool behavior.** Alias matching runs per table, so both resolve to the same
canonical key. The alias table in `references/chinese-document-field-library.md` is
the single place to add a new variant.

---

## F. Quick triage

| What you see | First thing to check |
|---|---|
| Empty table set on a text PDF | A1 — vector text, no ruling |
| Empty table set on a scan | B5 — no ruling lines, rebuild grid |
| Amount 1000× too large | B2 — decimal/thousands swapped |
| One character missing in an id | B4 — thin stroke, re-scan |
| Total mismatch only on one document | E2 checklist, item 1 first |
| Header row treated as data | A3 — spanning title row above |
| Extra row of repeated labels mid-table | Statement repeats the header per page |
| A field missing entirely on a Word file | D2 — it was in a text box |
