---
name: csv-profiler
description: Profile and analyze CSV or other tabular data — column types, summary statistics, missing values, and anomalies. Use when the user needs to understand, clean, or sanity-check a dataset.
---

# CSV Profiler

Turn a raw CSV (or TSV, or an existing DataFrame) into a clear profile of what the data actually contains.

## Workflow

1. **Load and detect.** Read the file; detect delimiter, encoding, and header. Report row and column counts.

2. **Classify columns.** For each column, assign a type: numeric, datetime, categorical, boolean, or free text.

3. **Summarize.** For each column report:
   - Numeric: min, max, mean, median, missing count, distinct count.
   - Categorical: top values with counts, distinct count, missing count.
   - Datetime: min/max range and count of unparseable values.

4. **Flag anomalies.** Call out:
   - Missing or empty values, and all-null columns.
   - Mixed types within a single column.
   - Duplicate rows and near-duplicate keys.
   - Outliers beyond roughly 1.5×IQR.

5. **Recommend.** Suggest concrete cleaning steps (drop, fill, cast, dedupe) and note which columns look usable as identifiers or join keys.
