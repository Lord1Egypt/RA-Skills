# Example: Chinese Document Table Extraction & Field Validator

A complete, reproducible run. Every output below was produced by the scripts in this
package — nothing is hand-written.

---

## 1. The request

> "Extract the transaction table from this Chinese bank statement (对账单解析) and
> tell me if the numbers add up."

The source file `statement.pdf` is a one-page statement with a ruled table:

| 交易日期 | 摘要 | 借方发生额 | 贷方发生额 | 余额 | 对方户名 |
|---|---|---|---|---|---|
| 2024-01-05 | 货款汇入 | | 12,345.60 | 150,000.00 | 示例制造有限公司 |
| 2024-01-06 | 手续费 | 25.00 | | 149,975.00 | 示例制造有限公司 |
| 2024年1月8日 | 货款汇入 | | 8,000.00 | 157,975.00 | 示例贸易有限公司 |
| 2024-01-09 | 退款 | 1,000.00 | | 156,975.00 | 示例制造有限公司 |

---

## 2. Step 1 — the input contract

| # | Required input | Value | Decision |
|---|---|---|---|
| 1 | Source file | `statement.pdf` | present → PDF branch |
| 2 | Document profile | `bank_statement` | confirmed by the user |
| 3 | Field expectations | built-in `bank_statement` profile | applied |
| 4 | Output target | table + JSON | both produced |

Nothing is missing, so the skill proceeds. If the user had not named a profile, the
skill would have asked and listed the seven options rather than guessing.

---

## 3. Step 2 — extraction

```bash
python scripts/extract_tables.py --input statement.pdf --profile bank_statement --out ./out
```

Console output:

```
来源文件   : statement.pdf（pdf）
页数       : 1
文档画像   : bank_statement / 银行对账单 / 交易明细
检出表格   : 1（丢弃 0）
记录条数   : 4
合计行     : 0
丢弃重复表头: 0
```

### 3.1 Extraction table (human view)

| record_id | field (中文 / English) | value | evidence | status |
|---|---|---|---|---|
| r001 | 交易日期 / transaction date | 2024-01-05 | p1_t1 r2 c1 | ok |
| r001 | 摘要 / summary | 货款汇入 | p1_t1 r2 c2 | ok |
| r001 | 贷方发生额 / credit amount | 12345.6 | p1_t1 r2 c4 | ok |
| r001 | 余额 / balance | 150000.0 | p1_t1 r2 c5 | ok |
| r001 | 对方户名 / counterparty | 示例制造有限公司 | p1_t1 r2 c6 | ok |
| r003 | 交易日期 / transaction date | 2024-01-08 | p1_t1 r4 c1 | ok |

Note r003: the source cell reads `2024年1月8日`, the normalized value is
`2024-01-08`, and `raw` still holds `2024年1月8日`. The empty 借方发生额 cell is
`missing`, not `0` — a distinction that matters when summing columns.

### 3.2 JSON (machine view)

```json
{
  "schema_version": "1.0",
  "source": {
    "file": "statement.pdf",
    "type": "pdf",
    "pages": 1,
    "profile": "bank_statement",
    "profile_zh": "银行对账单 / 交易明细",
    "extracted_at": "2024-01-05T10:00:00Z"
  },
  "summary": {
    "tables_detected": 1,
    "tables_rejected": 0,
    "records": 4,
    "records_with_issues": 0,
    "validation_status": "not_run"
  },
  "records": [
    {
      "record_id": "r001",
      "table_id": "p1_t1",
      "row": 2,
      "fields": {
        "transaction_date": {
          "value": "2024-01-05",
          "raw": "2024-01-05",
          "evidence": { "table_id": "p1_t1", "row": 2, "col": 1, "raw": "2024-01-05", "page": 1 },
          "status": "ok"
        },
        "summary": {
          "value": "货款汇入",
          "raw": "货款汇入",
          "evidence": { "table_id": "p1_t1", "row": 2, "col": 2, "raw": "货款汇入", "page": 1 },
          "status": "ok"
        },
        "debit_amount": {
          "value": null,
          "raw": "",
          "evidence": { "table_id": "p1_t1", "row": 2, "col": 3, "raw": "", "page": 1 },
          "status": "missing"
        },
        "credit_amount": {
          "value": 12345.6,
          "raw": "12,345.60",
          "evidence": { "table_id": "p1_t1", "row": 2, "col": 4, "raw": "12,345.60", "page": 1 },
          "status": "ok"
        },
        "balance": {
          "value": 150000.0,
          "raw": "150,000.00",
          "evidence": { "table_id": "p1_t1", "row": 2, "col": 5, "raw": "150,000.00", "page": 1 },
          "status": "ok"
        },
        "counterparty": {
          "value": "示例制造有限公司",
          "raw": "示例制造有限公司",
          "evidence": { "table_id": "p1_t1", "row": 2, "col": 6, "raw": "示例制造有限公司", "page": 1 },
          "status": "ok"
        }
      },
      "issues": []
    }
  ],
  "footer_rows": [],
  "unverified_fields": [],
  "rejected_tables": [],
  "unmapped_columns": [],
  "dropped_header_rows": 0,
  "notes": []
}
```

The last record (r004) is the one worth looking at twice: its 借方发生额 is
`1,000.00` and its 贷方发生额 is empty. The balance chain is
150,000.00 → 149,975.00 → 157,975.00 → 156,975.00, which is consistent with a
refund of 1,000.00 on the last row.

---

## 4. Step 3 — validation

```bash
python scripts/validate_fields.py --input ./out/records.json --profile bank_statement
```

Report (full output):

```
# 字段校验报告 / Field Validation Report

- 来源文件 / source file : statement.pdf
- 文件类型 / source type : pdf
- 文档画像 / profile    : bank_statement / 银行对账单 / 交易明细
- 校验结论 / status     : pass
- 容差 / tolerance      : 0.01

## 概览 / Summary

| 记录数 records | error | warning | info | unverified |
|---|---|---|---|---|
| 4 | 0 | 0 | 0 | 0 |

## 问题明细 / Issues

无问题检出。

## 不可溯源字段 / Unverified fields

所有字段均可溯源。
```

`validation_status: pass`. No 合计 row exists on this page, so no reconciliation was
attempted — the tool reports "no total row" rather than inventing one.

---

## 5. A second run, where the rules fire

The same pipeline on a statement that contains real problems. Source
`statement_problem.csv`:

```
record_id,交易日期,摘要,借方发生额,贷方发生额,余额,对方户名,流水号
r001,2024-01-05,货款汇入,,"12,345.60","150,000.00",示例制造有限公司,TX20240105001
r002,2024-01-06,手续费,"25.00",,"149,975.00",示例制造有限公司,TX20240106002
r003,2024-01-08,货款汇入,,"8,000.00","157,975.00",示例贸易有限公司,TX20240108003
r004,2024-01-08,货款汇入,,"8,000.00","157,975.00",示例贸易有限公司,TX20240108003
r005,01/02/2024,退款,"15.00",,"149,960.00",示例制造有限公司,TX20240108004
r006,2024-01-09,货款汇入,,"1,000.00","160,960.00",示例制造有限公司,TX20240108005
合计,,,"40.00","29,345.60",,,
```

```bash
python scripts/validate_fields.py --input statement_problem.csv --profile bank_statement
```

Result:

```
结论：pass_with_warnings

  [warning] ambiguous_date        r005  日期存在日/月顺序歧义，未自动判读：01/02/2024
  [warning] duplicate_identifier  r004  同一单据内 流水号 / transaction no 重复：TX20240108003（首次出现在 r003）
  [info   ] total_matched              合计 40.0 与 借方发生额 / debit amount 明细求和一致（2 行）
  [info   ] total_matched              合计 29345.6 与 贷方发生额 / credit amount 明细求和一致（4 行）
  [warning] duplicate_detail_row  r004  明细行重复：与 r003 完全一致
```

What the skill did **not** do, and why:

- It did not pick `01/02/2024` as January 2 or February 1. The raw string is kept,
  the normalized value stays `null`, and the record is flagged `ambiguous_date`.
- It did not delete r004 even though it duplicates r003. Both rows are reported with
  their row numbers so a human decides whether it is a double posting or a genuine
  repeated 流水号.
- It did not adjust any amount to make the 合计 line up. Both columns reconciled
  exactly here; in the case where they do not, the report prints the two sides and
  the difference (see `total_mismatch` in the rules list).

---

## 6. The refusal path

When the input is insufficient, the skill returns a requirements list — never data.

```
CANNOT EXTRACT — missing inputs
1. Source file: not provided. Accepted: .pdf .png .jpg .tif .xlsx .xlsm .docx .csv
2. Document profile: not specified. Choose one of: bank_statement, vat_invoice,
   insurance_policy, payroll, logistics, customs, generic
3. Scope: whole document or specific pages/sheets
```

Another refusal case: a source file with no table structure at all. The skill
reports `no_table_structure`, lists the pages and sheets it inspected, and points to
`references/table-extraction-traps.md` (sections A1 and B5 cover the two usual
causes). It does not return an empty record set dressed up as a successful run.

---

## 7. Delivery acceptance block

```
Extraction acceptance
source_file        : statement.pdf (pdf, 1 page)
profile            : bank_statement  [confirmed by user]
tables_detected    : 1   tables_rejected: 0   records: 4
coverage           : all pages/sheets covered
validation_status  : pass
issues_error       : 0   issues_warning: 0   issues_info: 0
unverified_fields  : 0 (list or "none")
reconciliation     : not applicable (no 合计 row on this page)
low_confidence     : none
privacy            : PII masked yes/no — no personal data in this statement
reviewer           : <name>   date: <YYYY-MM-DD>
outstanding        : none
```

---

## 8. Reproducing this example

The scripts ship with self-tests, so the pipeline can be checked without any input
file:

```bash
python scripts/extract_tables.py --selftest    # -> SELFTEST: PASS
python scripts/validate_fields.py --selftest   # -> SELFTEST: PASS
```

The self-test data is synthetic. The source values in this document (示例制造有限公司,
25377000000123456789 and similar) are placeholders that exist only to demonstrate the
field mapping and the validation rules; they are not real company identifiers and
carry no meaning.

---

## 9. Where to go next

- Field names, aliases and the exact format rules: `references/chinese-document-field-library.md`
- Why an extraction came out wrong: `references/table-extraction-traps.md`
- Before shipping to a downstream system: `references/delivery-acceptance-checklist.md`
