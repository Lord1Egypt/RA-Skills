# Chinese Document Table Extraction & Field Validator

> Extract structured tables and key fields from Chinese PDF / scans / Excel / Word, then
> validate every value and flag anomalies — with page, row and column traceability for each field.

**中文简介**：从中文 PDF、扫描件、Excel、Word 中批量抽取结构化表格与关键字段，逐字段校验金额、日期、编号格式、合计勾稽与重复行，输出带页码/表号/行列溯源的可机读记录。面向需要处理中文文档的开发者与数据团队（跨境电商与外贸财务、SaaS 进中国、数据迁移、文档 AI 产品），不是面向中文文书工作者的写作助手。

---

## What it solves / 解决什么

Chinese business documents are table-heavy and field-heavy, and the field names do not
translate one-to-one. A bank statement says 借方发生额, an invoice says 价税合计, a
policy says 缴费期 — and none of them is self-explanatory to a system that was built
against English forms.

This skill does two things, in this order:

1. **Extract** — pull tables out of PDF / xlsx / docx / csv, mapping each Chinese
   header to a canonical English field key while keeping the original string and the
   physical location (page, table id, row, column) of every cell.
2. **Validate** — check the result against a document-type profile (required fields,
   amount format, date format, identifier shape, totals reconciliation, duplicate rows)
   and mark every problem instead of silently repairing it.

The governing rule: **a value that cannot be pointed back to a source location is
`unverified`; a value that is missing is reported as missing. Nothing is invented.**

---

## When to use / 何时使用

Use it for:

- Bank statements / 对账单解析 — transaction tables into structured records
- VAT invoices / 中文发票识别 — 发票代码、发票号码、开票日期、金额、税额、价税合计、销方
- Insurance policies / 保单信息提取 — 保单号、投保人、被保人、保额、缴费期、生效日期
- Payroll and social insurance tables / 工资表、社保公积金表
- Logistics waybills, customs declarations, bid attachments / 运单、报关单、招投标明细
- Numeric note tables in Chinese financial reports / 财报附注
- Any pipeline that needs **validated, traceable** output from Chinese documents

Do not use it for drafting or polishing Chinese prose, for legal or tax opinions, for
authenticity checks (印章、签名), or for documents with no table structure.

---

## Install / 安装

```bash
# Claude Code / Codex CLI / Cursor — install from the skills registry
npx skills add Tingyun01/tingyun-skills

# or point your agent at this directory's SKILL.md directly
```

Runtime dependencies (only needed for the formats you actually process):

```bash
pip install pdfplumber openpyxl python-docx pandas
```

`scripts/validate_fields.py` and `scripts/field_library.py` run on the Python standard
library alone — if a dependency is missing, the script prints the exact `pip install`
command and exits with a non-zero code instead of crashing.

---

## Trigger phrases / 触发词

| Language | Trigger |
|---|---|
| 中文 | 中文PDF表格提取、中文发票识别、保单信息提取、对账单解析、表格字段校验、中文文档结构化 |
| English | extract tables from Chinese PDF, Chinese invoice OCR, parse bank statement, validate extracted fields, Chinese document data pipeline |

---

## Usage / 用法

```bash
# 1) extract tables + fields with evidence coordinates
python scripts/extract_tables.py --input statement.pdf --profile bank_statement --out ./out

# 2) validate the extraction and produce a report
python scripts/validate_fields.py --input ./out/records.json --profile bank_statement --report ./out/report.md

# machine-readable result
python scripts/validate_fields.py --input ./out/records.json --profile vat_invoice --json ./out/validation.json

# built-in self-tests
python scripts/extract_tables.py --selftest
python scripts/validate_fields.py --selftest
```

### Document profiles / 文档画像

`bank_statement` (银行对账单) · `vat_invoice` (增值税发票) · `insurance_policy`
(保单) · `payroll` (工资表) · `logistics` (物流运单) · `customs` (报关单) ·
`generic` (通用明细表)

```bash
python scripts/extract_tables.py --list-profiles
```

### Output / 输出

- `out/records.json` — records with `value`, `raw`, and `evidence` (page / table id /
  row / column) per field, plus footer rows, rejected tables and unmapped columns
- `out/records.csv` — flat view for quick human review
- `out/report.md` — validation report: issue table by level and rule, unverified fields,
  extraction notes, and the pre-delivery reminders

---

## What you get / 产出

| Item | Detail |
|---|---|
| Extraction table | Human-readable field table with evidence column |
| JSON record set | Fixed schema, `schema_version` 1.0, one object per record |
| Validation report | error / warning / info issues, each with a rule id and a fix hint |
| Reconciliation | Detail-row sums vs printed 合计, plus 价税合计 = 金额 + 税额 and 数量 × 单价 = 金额 |
| Refusal list | When inputs are insufficient, the skill returns what is missing instead of data |

---

## Package contents / 包内文件

```
SKILL.md                                    main skill file (English body, bilingual field terms)
README.md                                   this file
EXAMPLE.md                                  one complete, reproducible input → output run
meta.json                                   package metadata
references/
  chinese-document-field-library.md         Chinese ⇄ English field library and format rules
  table-extraction-traps.md                 PDF/OCR/XLSX/DOCX traps and countermeasures
  delivery-acceptance-checklist.md          pre-delivery acceptance checklist
scripts/
  extract_tables.py                         PDF/XLSX/DOCX/CSV → records JSON + CSV
  validate_fields.py                        records → validation report (text + JSON)
  field_library.py                          shared aliases, amount/date parsers, profiles
```

---

## Notes / 说明

- Outputs are decision support and require human review; no accuracy or completeness
  guarantee is made or implied.
- Not legal, tax or accounting advice, and not a document authenticity check.
- The methodology, field library, rules and scripts in this package are original work
  compiled for this skill.
