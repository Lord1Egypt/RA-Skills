---
name: data-classification
description: 用于数据分类、数据分级、数据分类分级任务。用户要求对单一数据字段名、字段列表、数据库表 SQL/DDL 文件进行数据分类、数据分级或数据分类分级时使用；支持普通数据分类分级、GB/T 43697-2024 通用数据分类分级、金融数据分类分级、JR/T 0197-2020 金融数据安全级别，以及“通用数据标签 + 金融数据标签”的金融双标签体系。
---

# Data Classification

## Purpose

Classify user-provided field names or SQL DDL into:

1. **普通/通用数据分类分级**: GB/T 43697-2024 style category + level (`一般数据 / 重要数据 / 核心数据`).
2. **金融数据双标签体系**: general label + JR/T 0197-2020 financial label (`一级/二级/三级/四级子类` + `最低安全级别1-5`).

This skill produces **classification suggestions**, not final regulatory determinations. Mark uncertain items for business-owner review.

## Quick workflow

1. Identify input type:
   - Single field name: classify directly.
   - SQL/DDL file: extract table names, column names, types, and comments.
2. Run the helper when useful:
   ```bash
   python3 skills/data-classification/scripts/classify_data.py --field "customer_id" --mode finance
   python3 skills/data-classification/scripts/classify_data.py --sql path/to/schema.sql --mode finance --format markdown
   ```
3. Review financial rows against JR/T 0197-2020 Appendix A before falling back to heuristics:
   - `references/jrt0197-appendix-a-full.csv` is the machine-readable full Appendix A table.
   - `references/jrt0197-appendix-a-compact.md` is the human-readable compact Appendix A table.
   - `references/financial-dual-label.md` contains dual-label workflow and fallback heuristics.
   - `references/general-rules.md` contains GB/T 43697-2024 logic.
4. Return a field-level result that covers **every input field**. Do not replace the full field list with a summary.
5. Choose output delivery by field count internally, but do not explain this threshold policy to the user:
   - **≤20 fields**: output the complete field-level table inline in chat; do not create/attach files unless the user explicitly asks for an export/file.
   - **>20 fields**: save the complete field-level result as a CSV file, attach it with a `MEDIA:` line using the CSV file's absolute filesystem path, show the first 20 classified fields inline, and include a coverage statement in the message. Do not inline rows after the first 20. Never provide only a plain local path as the download method. Do not write the coverage statement into the CSV file itself.
6. Run a coverage check before finalizing: compare parsed/input field count with classified output row count. If any field is missing, fix the output or explicitly mark the field as `[blocked: 未解析/缺少字段信息]`.
7. Ask for business context only if the field name/comment is too ambiguous.

## Output requirements

For a **single field**, include:

- 字段名
- 通用分类：行业领域、描述对象/数据主体、内容类别
- 通用分级：一般/重要/核心 + 理由
- 置信度与需确认点
- 金融标签（仅金融场景输出）：推荐的一级/二级/三级/四级子类 + 最低安全级别
- 候选金融标签（仅金融场景输出）：当字段可落入多个 JR/T 分类时，一并列出候选项并说明推荐依据
- 双标签结果（仅金融场景输出）：`通用标签 + 金融标签`

For a **SQL file/table**, classify **all parsed columns from all tables**. Choose the delivery format internally and do not tell the user the threshold/routing rule.

- **≤20 fields**: the complete field-level table inline. Do **not** create/attach files unless the user explicitly asks for an export/file.
- **>20 fields**: create a complete CSV result file. Return a concise completion note, attach the CSV with `MEDIA:<absolute-csv-path>` on its own line so the UI can render a downloadable link, include the first 20 field-level rows inline, and include the coverage statement in the message. Do not inline rows after the first 20. Do not rely on a bare local path as the user's download link. Do not include the coverage statement as a row in the CSV file.

Do not provide only a subset such as “core fields”, “sample rows”, or “summary table” unless the user explicitly asks for a summary.

The following output columns are **mandatory for every field and must be non-empty in all scenarios**:

1. 字段名
2. 通用分类
3. 通用分级
4. 置信度

For **financial data/scenarios only**, also include these mandatory non-empty columns:

5. 推荐金融分类标签
6. JR/T最低级别
7. 候选金融标签

For financial fields, match against `references/jrt0197-appendix-a-full.csv` or `references/jrt0197-appendix-a-compact.md` first. Use `financial-dual-label.md` heuristics only when Appendix A has no clear match or when field/table context creates multiple reasonable candidates.

For **non-financial data**, do **not** output `推荐金融分类标签`、`JR/T最低级别`、`候选金融标签`.

Recommended non-financial table shape:

| 表名 | 字段名 | 类型/注释 | 通用分类 | 通用分级 | 置信度 | 依据/备注 |
|---|---|---|---|---|---:|---|

Recommended financial table shape:

| 表名 | 字段名 | 类型/注释 | 通用分类 | 通用分级 | 推荐金融分类标签 | JR/T最低级别 | 候选金融标签 | 双标签 | 置信度 | 依据/备注 |
|---|---|---|---|---|---|---:|---|---|---:|---|

After the table, include a coverage line:

`覆盖校验：输入/解析字段 N 个，已分类 N 个，遗漏 0 个。`

If output is saved to a file, still include the coverage line in the message and an attachment. For CSV outputs, include `MEDIA:<absolute-csv-path>` on its own line so the user can click/download directly; use the absolute path returned by the file-writing step, not a relative workspace path. File output is allowed for >20 fields as CSV, or whenever the user explicitly requests a file/export. Do not write the coverage line into the CSV file. Do not explain that files are chosen because of the field-count threshold unless the user asks why.

## Classification principles

- Coverage is mandatory: every user-provided field/parsed SQL column must receive a classification row.
- Use **就高从严**: if multiple rules match, choose the stricter level as the recommendation, list reasonable candidate labels, and explain why.
- Treat field names alone as weak evidence; comments and table names improve confidence.
- Do not infer `核心数据` from a field name alone unless the field clearly describes large-scale national/security/critical-infrastructure data. Usually mark as `需人工确认`.
- `重要数据` usually requires scale, coverage, precision, or public/national impact context. For isolated personal or organization fields, default to `一般数据` unless a law/industry rule says otherwise.
- For financial data, Appendix A match takes precedence over broad keyword heuristics. JR/T 0197 level is the **minimum security level**; business context may raise it.
- For personal financial information, authentication credentials, biometric identifiers, account/payment/transaction data, and credit data should be handled conservatively.

## Helper script notes

`classify_data.py` is deterministic and heuristic. It is designed for first-pass tagging:

- Inputs: `--field`, `--fields`, or `--sql`.
- Modes: `general`, `finance`.
- Formats: `markdown`, `json`, `csv`.
- It parses common `CREATE TABLE` DDL and column comments.
- Low confidence means the assistant should inspect context and possibly ask one focused follow-up.

## References

- `references/general-rules.md`: compact GB/T 43697-2024 classification/grading rules.
- `references/financial-dual-label.md`: financial dual-label workflow and fallback heuristics.
- `references/jrt0197-appendix-a-compact.md`: compact human-readable JR/T 0197-2020 Appendix A typical data grading table.
- `references/jrt0197-appendix-a-full.csv`: full machine-readable JR/T 0197-2020 Appendix A typical data grading table.
