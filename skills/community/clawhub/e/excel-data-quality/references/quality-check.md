# Quality Check — Sub-Skill

## Tool

```bash
node tools/quality_scanner.js <file_path>
```

Returns data overview + quality scan in one call.

## Key Output Fields

```jsonc
{
  "fileName": "...",
  "parseInfo": { "fileType", "sheetNames", "warnings", "mojibakeDetected" },
  "tableStats": { "totalRows", "totalColumns", "completeRowsPercentage", "totalNullPercentage", "duplicatePercentage", "memorySizeReadable" },
  "fieldStats": [{ "name", "inferredType", "nullPercentage", "uniquePercentage", "sampleValues", "detectedPatterns", "minValue", "maxValue", "meanValue", "topValues" }],
  "sampleData": [ { /* up to 10 most-complete rows */ } ],
  "dataValidity": { "canProceed": true },
  "issues": [{ "category", "severity", "title", "description", "affectedColumns", "affectedPercentage", "suggestion", "deduction" }],
  "score": { "totalScore": 72.3, "grade": "Fair", "severityCounts": {}, "breakdowns": [{ "categoryName", "weight", "rawDeduction", "scaledDeduction", "finalScore" }] }
}
```

## Scoring: 22 Modules × 6 Dimensions

Each dimension starts at 100. Raw deductions are amplified by severity (critical ×1.5, high ×1.2, low ×0.7) and category sensitivity scale, then subtracted. Total score = weighted sum.

| Dimension | Weight | Scale | Modules |
|-----------|--------|-------|---------|
| Completeness | 25% | ×2.5 | Null values, empty strings, empty rows, merged cell patterns |
| Accuracy | 23% | ×5.0 | Outliers, rare values, value uniformity |
| Consistency | 17% | ×2.0 | Mixed types, case, date format, full-width chars, number-with-unit, cross-column logic |
| Validity | 15% | ×2.5 | Format errors, special chars, range, encoding/mojibake, ID checksum |
| Uniqueness | 15% | ×3.0 | Duplicate rows, primary key, near-duplicates (fuzzy) |
| Timeliness | 5% | ×10 | Future dates, old dates |

**Grades**: >= 90 Excellent, >= 80 Good, >= 70 Fair, >= 60 Poor, < 60 Very Poor

---

## How to Present Results

Run the tool, then walk through **Step 1–6 in order**. Every step is **mandatory** — do not skip any. Do NOT dump raw JSON to the user.

---

### Step 1 — Understand the Data

**Read**: `sampleData`, `fieldStats` (all fields), `parseInfo`.
**Do NOT output anything to the user yet.** This step is internal analysis only.

You MUST complete these 4 tasks before proceeding:

1. **Detect locale/region** — examine field names, sample values, currency symbols, date formats, and text language. Determine the primary data locale (e.g., "Chinese business data", "European HR records", "Japanese logistics", "mixed EN/AR"). Keep this context for all subsequent steps.

2. **Infer business domain** — based on field names and sample values, determine what this dataset represents (e.g., e-commerce orders, employee records, IoT sensor readings, financial transactions).

3. **Build a field mapping** — for EVERY field in `fieldStats`, determine:
   - A human-readable **display name** (translated to the user's language)
   - A one-line **business meaning**
   - The `inferredType` from the tool output

4. **Draft a dataset summary** — 1–2 sentences: what the data represents, its granularity (one row = one what?), and approximate time range (if any date field exists).

---

### Step 2 — Present Data Overview

**Read**: `tableStats`, the field mapping from Step 1.
**Output to user**: the dataset summary, a metrics table, and a column details table.

You MUST produce exactly this structure (adapt values):

> **sales.xlsx** — E-commerce order data, 5,000 orders from 2023-01 to 2024-06.
>
> | Metric | Value |
> |--------|-------|
> | Rows | 5,000 |
> | Columns | 12 |
> | Complete rows | 84.0% |
> | Null cells | 1.33% |
> | Duplicates | 1.0% |
> | File size | 1.2 MB |
>
> | Column | Display Name | Type | Nulls | Unique | Key Stats |
> |--------|-------------|------|-------|--------|-----------|
> | order_id | Order ID | string | 0% | 100% | uuid pattern |
> | amount | Amount | float | 2.1% | 85% | Range: 0.50 – 9,999.00 |
> | created_at | Created At | date | 0% | 95% | 2023-01 to 2024-06 |

Rules:
- Show ALL columns, not just a selection.
- Use the display names from Step 1.
- For numeric columns, show range (min–max) or mean in "Key Stats".
- For categorical columns with `topValues`, show top 2–3 values.
- For columns with `detectedPatterns`, note the pattern (e.g., "email", "uuid", "id_card_cn").

---

### Step 3 — Present Quality Score

**Read**: `score.totalScore`, `score.grade`, `score.severityCounts`, `score.breakdowns`.
**Output to user**: score headline + 6-dimension breakdown table.

You MUST produce exactly this structure:

> **Data Quality Score: 72.3 / 100** (Fair ⚠️)
> 15 issues found: 1 critical, 3 high, 5 medium, 4 low, 2 info
>
> | Dimension | Score | Dimension | Score |
> |-----------|-------|-----------|-------|
> | Completeness | 65.0 | Validity | 78.0 |
> | Accuracy | 82.0 | Uniqueness | 85.0 |
> | Consistency | 90.5 | Timeliness | 95.0 |

Rules:
- Use the emoji: >= 90 ✅, >= 80 🟢, >= 70 ⚠️, >= 60 🟠, < 60 🔴.
- Show severity counts on the same line as the headline.

---

### Step 4 — Narrate Issues & Insights

**Read**: `issues` array (all of them), the business domain and locale from Step 1.
**Output to user**: a narrative analysis grouped by dimension.

You MUST follow these rules:
1. **Do NOT list issues one by one.** Group related issues into paragraphs by dimension (Completeness, Consistency, etc.). Only create a paragraph for dimensions that have issues.
2. **For each group, explain the business impact** — connect the issue to the specific business domain. Example: "The `age` field is 85% empty — for a customer segmentation dataset, this makes age-based analysis impossible."
3. **For every critical or high severity issue, provide a specific actionable recommendation.** Not generic advice like "fix this" — state exactly what to do. Example: "Forward-fill the `region` column (merged cell pattern detected) rather than using mean imputation."
4. **For medium/low issues, summarize briefly** — one sentence per group is enough.
5. **Mention the `suggestion` field from issues as supporting context**, but rephrase it in business terms rather than quoting it verbatim.

---

### Step 5 — Semantic Deep Analysis

**Read**: `sampleData`, `fieldStats.topValues`, `issues`, and the locale from Step 1.
**Output to user**: additional findings that the programmatic scan cannot detect.

You MUST check ALL of the following. For each, either report findings or explicitly state "not detected":

1. **Synonym detection** — Scan `topValues` of every categorical column. Identify value groups that represent the same concept across languages or abbreviations.
   - Examples: "M"/"Male"/"男"/"masculin"/"ذكر", "Y"/"Yes"/"是"/"Oui"/"نعم", "CN"/"China"/"中国".
   - Output: list each synonym group found as `[value1, value2, ...] → suggested canonical value`.

2. **Multi-value cells** — Scan `sampleData` for cells containing commas, semicolons, pipes, slashes, or newlines that suggest multiple values packed in one cell.
   - Output: list affected columns and example values.

3. **Business key duplicates** — Based on the field semantics from Step 1, identify the most likely composite business key (e.g., `[customer_id, order_date]` or `[employee_id, department]`). State whether the dataset has entity-level duplicates using this key, even if no single-column PK violation was found.
   - Output: state the inferred business key and whether duplicates exist.

4. **Cross-column relationships** — Identify logical relationships between columns (date ranges, parent-child, calculated totals). Explain any violations found by the `cross_column_logic` issues in business terms. Also note relationships the tool did NOT check but that appear relevant.
   - Output: list each relationship and its status (valid / violated / unchecked).

5. **Locale-specific issues** — Based on the locale detected in Step 1, check for region-specific problems:
   - CJK: full-width/half-width mixing, encoding, era-based dates
   - European: DD/MM vs MM/DD ambiguity, decimal comma vs dot (1.234,56), GDPR-sensitive fields
   - Middle Eastern: RTL text mixing, Arabic numeral variants (٠١٢ vs 012), Hijri dates
   - Multi-region: mixed languages in same column, inconsistent formats
   - Output: list any locale-specific findings, or state "no locale-specific issues detected".

6. **Data fitness assessment** — Based on ALL findings (Steps 4 + 5), produce this table:

> | Use Case | Fitness | Key Blockers |
> |----------|---------|-------------|
> | BI Reporting | ⚠️ Fair | date inconsistency, 2 fields need cleaning |
> | ML Training | ❌ Poor | 85% null in key feature |
> | Aggregation | ✅ Good | core numerics clean |

   Fitness levels: ✅ Good, ⚠️ Fair, ❌ Poor. Include at least 3 common use cases.

---

### Step 6 — Recommendation & Next Steps

**Read**: `score.totalScore`, `dataValidity.canProceed`, your analysis from Steps 4–5, the issues list.
**Output to user**: a closing statement + a numbered follow-up menu.

Rules:
- IF `dataValidity.canProceed` is false → **warn first**: "⚠️ This file has structural issues that prevent reliable analysis: [reason]. Results above may be incomplete."
- THEN give the score-based recommendation:
  - Score >= 90 → "Data quality is excellent. Ready for analysis."
  - Score 70–89 → "A few issues to address. Recommend cleaning before critical use."
  - Score < 70 → "Significant issues detected. Strongly recommend cleaning before use."

**THEN output the follow-up menu.** You MUST:

1. **Build 1–3 exploration suggestions** based on the actual findings from Steps 4–5. Pick the most valuable from:
   - A dimension with critical/high issues → "Deep-dive into [dimension] issues"
   - Synonym groups found → "Review synonym/duplicate value consolidation"
   - Cross-column violations → "Explore cross-column logic issues"
   - Fitness blockers → "Analyze blockers for [use case]"
   - High-null columns → "Investigate missing data in [column(s)]"
   - Use concrete column/dimension names — not generic text.

2. **Output this menu structure** (adapt the exploration items to the actual data):

> | # | Next |
> |:---:|------|
> | **1** | Chart — visualize this data |
> | **2** | Advanced Chart — dashboards, Gantt, PPT (ChartGen) |
> | **3** | *[exploration suggestion 1, e.g., "Deep-dive: Completeness — 3 fields with >50% nulls"]* |
> | **4** | *[exploration suggestion 2, e.g., "Review synonym groups in `status` and `region`"]* |
> | **5** | *[exploration suggestion 3, if applicable]* |
> | **0** | Done |
>
> Reply 0–N, or describe what you need.

Rules for routing:
- IF user replies `1` → follow `references/chart.md`.
- IF user replies `2` → follow `references/advanced-chart.md`.
- IF user replies an exploration number (3/4/5) → provide the detailed analysis for that topic using the data already available from the scan results and your semantic analysis. Do NOT re-run the tool.
- IF user replies `0` → end.
