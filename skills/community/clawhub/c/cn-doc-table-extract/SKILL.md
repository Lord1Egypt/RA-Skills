---
slug: cn-doc-table-extract
name: cn-doc-table-extract
version: 1.0.0
displayName: Chinese Document Table Extraction & Field Validator
description: "Extract structured tables and key fields from Chinese PDF, scanned images, Excel (xlsx) and Word (docx) documents, then validate every extracted value and flag anomalies with page/row/column traceability. Use when you need 中文PDF表格提取 (Chinese PDF table extraction), 中文发票识别 (Chinese invoice recognition), 保单信息提取 (insurance policy field extraction), 对账单解析 (bank statement parsing), 表格字段校验 (table field validation) or 中文文档结构化 (Chinese document structuring). Outputs a fixed-shape table plus a JSON record set where every field carries a source citation (page, table id, row, column) or an explicit unverified marker, plus a validation report listing missing required fields, malformed amounts, impossible dates, invalid invoice numbers, total-vs-detail sum mismatches and duplicate rows. Ships runnable scripts: scripts/extract_tables.py (PDF/XLSX/DOCX/CSV to records) and scripts/validate_fields.py (completeness, amount, date, id and reconciliation checks). Intended for developers and data teams processing Chinese documents; not a document-authoring or legal-review assistant."
summary: "从中文 PDF/扫描件/Excel/Word 中抽取结构化表格与关键字段，逐字段校验并标记异常，输出带页码行列溯源的可机读记录。"
tags:
  - 中文文档抽取
  - 表格结构化
  - 字段校验
license: MIT-0
---

# Chinese Document Table Extraction & Field Validator

This skill turns messy Chinese business documents into machine-readable records, then
audits those records so a human reviewer knows exactly what to trust.

Two halves, always in this order:

1. **Extraction** — read tables out of a PDF / scan / xlsx / docx / csv file, keeping the
   physical origin of every cell (page, table id, row index, column index).
2. **Validation** — check the extracted records against a document-type field profile
   (required fields, amount format, date format, identifier shape, totals) and mark every
   problem instead of silently repairing it.

The hard rule of this skill: **a value that cannot be pointed back to a source location is
`unverified`, and a value that is missing is reported as missing. Nothing is guessed.**

---

## When to use this skill

Use it when the request is one of these shapes:

- "Extract the transaction table from this Chinese bank statement (对账单解析)."
- "Pull invoice number, date, amount and tax amount out of these Chinese VAT invoices
  (中文发票识别)."
- "Get policy number, insured party, sum insured and payment term out of this insurance
  contract (保单信息提取)."
- "Turn this payroll or social-insurance spreadsheet into structured records and check the
  totals (工资表/社保公积金表)."
- "Extract the line-item tables from this logistics waybill, customs declaration, or bid
  attachment."
- "Pull the numeric note tables out of a Chinese financial report (财报附注)."
- "Validate these already-extracted Chinese invoice records and tell me what is broken
  (表格字段校验)."
- Any pipeline step that reads Chinese documents and needs **traceable, validated**
  output rather than free text.

Do **not** use it for:

- Drafting, polishing, translating or summarizing Chinese prose documents. There is no
  table to extract and the validation half has nothing to audit.
- Legal, tax or accounting opinions. This skill reports what a document *says*; it does
  not judge whether the document is correct, lawful or complete in a legal sense.
- Images that are photographs of physical scenes, screenshots of chat threads, or
  handwriting-only notes with no table structure.
- Documents in English or other Latin-script languages only — the field profiles and
  format rules here are built for Chinese 单据 (bills/forms) conventions.
- Anything that needs a human sign-off on authenticity (印章 verification, watermark
  checks, signature authenticity). This skill extracts pixels-to-text, not truth.

---

## Input contract

The skill must refuse to start and must state what is missing if any of these are absent.

| # | Required input | If missing | If ambiguous |
|---|---|---|---|
| 1 | **The source file** (pdf / png / jpg / xlsx / docx / csv) or a path to it | Refuse. Ask for the file and list the supported extensions. Never fabricate a document. | If several files are given, ask which one to process first, or process each and label outputs by filename |
| 2 | **Document type profile** (bank statement / VAT invoice / insurance policy / payroll / logistics / customs / generic) | Do not guess silently. Ask the user to pick one, and offer the list below | If the type is clear from the layout or filename, use it but state the assumption in the output header |
| 3 | **Field expectations** — either a built-in profile or a custom field list | If the user says "extract everything", extract every column but mark the profile as `generic` and apply only universal checks | If a custom field list is partially named, apply it and report which named fields were not found |
| 4 | **Output target** (table only / JSON only / both) | Default to **both** and say so | — |

Optional but recommended: page or sheet range, currency assumption, whether the
document is a scan (affects OCR expectations), and the tolerance for sum
reconciliation.

### Built-in document profiles

| Profile key | 中文 | Typical fields (中文原文 → English) |
|---|---|---|
| `bank_statement` | 银行对账单 / 交易明细 | 交易日期 transaction date, 摘要 summary, 借方发生额 debit, 贷方发生额 credit, 余额 balance, 对方户名 counterparty |
| `vat_invoice` | 增值税发票 | 发票代码 invoice code, 发票号码 invoice number, 开票日期 issue date, 金额 amount, 税额 tax amount, 价税合计 total, 销方名称 seller |
| `insurance_policy` | 保单 / 保险合同 | 保单号 policy number, 投保人 policyholder, 被保人 insured, 保险标的 subject, 保额 sum insured, 缴费期 payment term, 生效日期 effective date |
| `payroll` | 工资表 / 社保公积金表 | 姓名 name, 工号 employee no, 身份证号 ID no, 应发工资 gross pay, 个人所得税 tax, 社保 personal social insurance, 公积金 housing fund, 实发工资 net pay |
| `logistics` | 运单 / 报关单 | 运单号 waybill no, 收发货人 shipper/consignee, 品名 goods, 数量 quantity, 重量 weight, 运费 freight |
| `customs` | 报关单 | 报关单号 declaration no, 商品编号 HS code, 数量 quantity, 单价 unit price, 金额 amount, 币制 currency |
| `generic` | 通用明细表 | every detected column name, header row + data rows |

### Rejection rules (hard)

- No source file → **refuse**, do not produce a "sample" answer.
- Source file present but unreadable / encrypted / corrupt → **refuse**, state the
  library error, suggest re-exporting.
- Source file present but **zero tables detected** → do not return an empty record set as
  success. Report "no table structure found", list what was inspected (pages/sheets
  scanned), and point to `references/table-extraction-traps.md` for the likely causes
  (merged cells, ruled lines, scan without ruling, text boxes).
- Missing optional libraries → scripts print the exact `pip install` command for the
  missing package and exit with a non-zero code. They never crash with a raw
  `ImportError` traceback and never silently produce an empty result.

---

## Step-by-step workflow

Each step has an explicit pass/fail criterion. Do not skip a step because "the data
looks clean" — the checks are cheap and the failure modes are silent.

### Step 1 — Identify the input and pin the profile

- If the extension is `.pdf` / `.png` / `.jpg` / `.tif` → PDF/image branch.
- If `.xlsx` / `.xlsm` → spreadsheet branch.
- If `.docx` → Word branch (only real tables; Word paragraph text is not a table).
- If `.csv` / `.tsv` → spreadsheet branch, single sheet.
- **If** the file extension contradicts the actual content (e.g. `.pdf` that is really a
  renamed `.xlsx`) → stop and report the mismatch; do not force the branch.
- **If** the profile is not stated by the user and cannot be inferred from the filename or
  the header row → ask, listing the seven profile keys above.

### Step 2 — Extract raw tables with physical coordinates

- For each page (PDF) or sheet (xlsx), collect tables with their index, bounding box or
  cell range, and the raw cell strings.
- **If** a table has fewer than 2 rows or fewer than 2 columns → discard it, but record
  it in `rejected_tables` with the reason `too_small`.
- **If** a scanned PDF page yields a table with cells but with a high rate of empty or
  garbage cells (> 50% unusable) → mark that table `low_confidence` rather than
  reporting the values as clean.
- **If** `pdfplumber` / `openpyxl` / `python-docx` / `pandas` is not installed → stop
  with an install hint naming the missing package and the command to install it. Never
  continue with an empty table set.

### Step 3 — Detect the header row and build records

- Scan the first 5 rows of a table. A row is a header candidate if it has ≥ 2 non-empty
  cells and the row below it has a comparable non-empty cell count, and the candidate
  cells are not all numeric.
- **If** no row qualifies as a header → use `列1/列2/...` (Column 1, Column 2) as
  synthetic headers and set `header_detected: false` in the output, so downstream code
  knows the column names are positional.
- **If** a table contains repeated header rows mid-table (common in long statements that
  repeat headers on each page) → drop the repeated headers and count them in
  `dropped_header_rows`.
- Map every record to the original row index so citations stay correct after filtering.

### Step 4 — Normalize values without changing meaning

Normalization must be reversible and must never overwrite the raw string.

- Amounts: strip `¥ ￥ CNY RMB 人民币 元` and full-width digits, keep the original in
  `raw`. Keep negative sign, keep thousands separators out of the numeric field.
- Dates: convert `2024年1月5日`, `2024-01-05`, `2024/01/05`, `20240105`, `2024.01.05`
  to ISO `YYYY-MM-DD`. Keep the original in `raw`.
- **If** a date is ambiguous (`01/02/2024` without a year, or a Chinese date with an
  out-of-range day such as `2024年2月30日`) → keep the raw string, set
  `normalized: null`, and raise an `invalid_date` issue. Do not pick an interpretation.
- Identifiers: strip spaces and internal separators only for comparison, never for
  display.

### Step 5 — Resolve headers through the alias table

- Match each raw header cell against the alias table in
  `references/chinese-document-field-library.md` (Chinese original → English → accepted
  variants, including full-width and half-width forms and common abbreviations).
- **If** ≥ 2 candidate aliases match one header → pick the alias whose expected value
  type matches the observed column content (date-like, money-like, id-like); if still
  tied, keep the raw header and flag `ambiguous_header`.
- **If** no alias matches → keep the raw header as the field name and list it under
  `unmapped_columns` in the report. Unmapped columns are still extracted; they are never
  dropped.

### Step 6 — Attach evidence to every field

For each field value, record: source file name, page or sheet, table id, row index,
column index, and the raw cell text. If a value came from a merged cell or was inferred
from a repeated header, note it (`merged_cell: true`, `inferred: true`).

### Step 7 — Run the validator

- Run `scripts/validate_fields.py` against the extracted records using the same profile.
- **If** the validator reports `error`-level issues → do not present the output as
  finished. List the issues and the exact fields involved.
- **If** the validator reports `warning`-level issues → present the output with the
  warning count in the header.
- **If** the validator cannot run (missing library) → present the raw extraction with
  `validation_status: "not_run"` and the install command. Do not claim validation
  happened.

### Step 8 — Emit the dual output and the report

Produce the table view, the JSON view, and the issue report, using the fixed schema in
`## Output format`. Every record must be traceable and every problem must be visible.

---

## Evidence and citations

Every extracted field carries a citation. The unit of evidence is:

```
{ "file": "...", "page": 3, "table_id": "p3_t2", "row": 17, "col": 4, "raw": "￥1,234.56" }
```

Rules:

- `page` is 1-based for PDFs; `sheet` replaces `page` for spreadsheets; for Word, use
  `table_id` plus `row`.
- `raw` is the exact source cell string. It is never rewritten.
- A field with **no** resolvable location is written as `"unverified"` and is listed in
  the `unverified_fields` array of the report. This applies to values that were
  inferred, defaulted, or carried over from a template.
- A value that appears in the document but sits outside any detected table (for example a
  价税合计 printed in the invoice footer) is cited to the page, and flagged
  `outside_table: true` with a note that it is a layout-level value, not a row value.
- Downstream consumers must be able to select any single field and open the source
  region that produced it. If that is not possible for a field, the field is
  `unverified` — there is no third option.
- Cross-document claims (for example "the invoice total matches the statement entry")
  must cite **both** sources with their ids.

---

## Validation gate and refusal paths

The gate runs before the result is presented as usable. It has three outcomes:
**PASS**, **PASS WITH WARNINGS**, **BLOCKED**.

### Gate rules

| # | Check | Fail condition | Result |
|---|---|---|---|
| G1 | Required fields present | Any profile-required field missing or empty on any record | BLOCKED |
| G2 | Amount parseable | A money field cannot be parsed to a number | BLOCKED |
| G3 | Amount sign/zero | Negative where the document type forbids it (e.g. 保费 must be > 0), or a total of exactly 0 across non-empty rows | WARNING |
| G4 | Date valid & in range | Unparseable date, or a date outside the document's stated period, or a future date in a historical statement | WARNING |
| G5 | Identifier shape | 发票号码 length not in the accepted set for the document type; duplicate identifier within one document | WARNING |
| G6 | Totals reconcile | 合计/小计/总计 row differs from the sum of the detail rows by more than the stated tolerance | WARNING |
| G7 | Duplicate detail rows | Two detail rows identical on the key columns | WARNING |
| G8 | Traceability | Any field without a source location | WARNING + `unverified` marker |

### Refusal paths — the skill must refuse, not improvise

1. **Insufficient information** → return a *requirements list*, not data. The list names
   exactly what is needed: which document is missing, which profile to apply, which
   fields to extract, which pages to scan. A refusal looks like this:

   ```
   CANNOT EXTRACT — missing inputs
   1. Source file: not provided. Accepted: .pdf .png .jpg .tif .xlsx .xlsm .docx .csv
   2. Document profile: not specified. Choose one of: bank_statement, vat_invoice,
      insurance_policy, payroll, logistics, customs, generic
   3. Scope: whole document or specific pages/sheets
   ```

2. **Unreadable or empty source** → report the error and stop. Do not return an empty
   record set as if it were a successful extraction.

3. **Numbers that do not add up** → report the mismatch with both sides and the
   difference. Never adjust a detail row to force a match, and never re-derive a printed
   合计 from the details and present it as the document's 合计.

4. **Guessing prohibited** → if a field cannot be read, it stays missing and is listed as
   missing. Filling in an 税额 from a rate applied to 金额, or inventing an invoice number
   that is cut off in a scan, is forbidden: the field is reported as missing with a note
   `not_readable_from_source`.

5. **Low-confidence OCR region** → if a table's cells are mostly unusable, return the
   table as `low_confidence` with the readable fragments and request a better scan
   (higher DPI, deskew, crop) rather than presenting plausible-looking values.

6. **Out-of-scope request** (legal opinion, authenticity verification, drafting) →
   state the boundary in one line and offer the closest in-scope action.

---

## Output format

Three blocks, always in this order. Field names are fixed so they can be parsed.

### 1. Extraction table (human view)

| record_id | field (中文 / English) | value | evidence | status |
|---|---|---|---|---|
| r001 | 发票号码 / invoice number | 25377000000123456789 | p1_t1 r2 c3 | ok |
| r001 | 开票日期 / issue date | 2024-01-05 | p1_t1 r2 c4 | ok |
| r001 | 销方名称 / seller | 示例制造有限公司 | p1_t1 r1 c1 | ok |

### 2. JSON (machine view)

```json
{
  "schema_version": "1.0",
  "source": {
    "file": "example_invoice.pdf",
    "type": "pdf",
    "pages": 2,
    "profile": "vat_invoice",
    "extracted_at": "2024-01-05T10:00:00Z"
  },
  "summary": {
    "tables_detected": 3,
    "tables_rejected": 1,
    "records": 42,
    "records_with_issues": 3,
    "validation_status": "pass_with_warnings"
  },
  "records": [
    {
      "record_id": "r001",
      "fields": {
        "invoice_number": {
          "value": "25377000000123456789",
          "raw": "25377000000123456789",
          "evidence": { "page": 1, "table_id": "p1_t1", "row": 2, "col": 3 },
          "status": "ok"
        }
      },
      "issues": []
    }
  ],
  "unverified_fields": [],
  "rejected_tables": [
    { "table_id": "p2_t1", "reason": "too_small", "detail": "1 row x 1 col" }
  ]
}
```

### 3. Validation report (issue list)

| issue_id | level | rule | record_id | field | raw | message | fix_hint |
|---|---|---|---|---|---|---|---|
| i001 | error | required_field_missing | r002 | 税额 / tax amount | — | required field missing | rescan page 1 at higher DPI |
| i002 | warning | total_mismatch | — | 合计 / total | 合计 12,000.00 | sum of 41 detail rows = 11,900.00, diff 100.00 | check the excluded row r017 |

Levels: `error` (blocks delivery), `warning` (deliver with flag), `info` (note only).

---

## Common failure modes

Detailed symptoms, root causes and remedies for every failure below live in
`references/table-extraction-traps.md`. Quick index:

| Symptom | Likely cause | Reference section |
|---|---|---|
| Table detected but every cell empty | Text-layer PDF with glyph positioning, or scan without ruling lines | Vector text vs scan |
| Header row picked up as a data row | Multi-row headers with merged title cells | Header detection |
| Amount column off by 100× | OCR read `￥1,234.00` as `1234.00` with a lost decimal separator, or a full-width `．` | Full-width and separator traps |
| Two identical transaction rows | Genuine duplicate postings in the source, or double-counting after page-merge | Duplicate rows |
| 合计 does not match the details | A detail row sits on the next page, or a refunded row is excluded | Totals reconciliation |
| 发票号码 rejected as invalid | 全电发票 numbers are 20 digits, older 纸质发票 codes are 8 or 12 | Invoice numbering |
| Date shifted by one day | `2024年1月5日` vs `2024-01-05` vs `20240105` handled inconsistently | Date normalization |
| Total row swallowed by the extractor | The 合计 row uses merged cells | Merged cells |
| DOCX text extracted but no tables | The document is a paragraph list, not a Word table | Word specifics |

### Reference files

- `references/chinese-document-field-library.md` — the field library: Chinese original
  name, English name, accepted alias variants, expected value type, and per-profile
  required-field sets. This is the canonical mapping used by Step 5.
- `references/table-extraction-traps.md` — PDF/OCR/XLSX/DOCX traps with symptom →
  cause → remedy, plus the reconciliation and duplicate-row decision rules.
- `references/delivery-acceptance-checklist.md` — the pre-delivery checklist to run
  before handing an extraction to a downstream system.

### Scripts

- `scripts/extract_tables.py` — PDF / XLSX / DOCX / CSV → records JSON + CSV.
  `--help` for usage. Missing dependencies are reported as an actionable install
  message, not a traceback.
- `scripts/validate_fields.py` — records JSON/CSV → validation report (text and JSON).
  `--help` for usage. `--selftest` runs a built-in sample to confirm the rules fire.

Example:

```bash
python scripts/extract_tables.py --input statement.pdf --profile bank_statement --out ./out
python scripts/validate_fields.py --input ./out/records.json --profile bank_statement --report ./out/report.md
```

---

## Copyright and boundaries

Methodology, field library, rules and scripts in this package are original work compiled
for this skill. No third-party textbook, course material or vendor documentation is
reproduced here. No guarantee of accuracy, completeness or fitness for a specific
purpose is made or implied — outputs are decision support and require human review.
This skill does not provide legal, tax or accounting advice, and does not verify document
authenticity, seals or signatures.
