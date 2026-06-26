# Data Quality Checks

Run these checks on every dataset before analysis. Report findings before results. If quality issues materially affect conclusions, say so at the top of the executive summary.

## 1. Completeness

### Missing values
- Count missing/null/empty values per column
- Calculate completeness rate per column: (non-null rows / total rows) x 100
- Flag columns below 90% completeness
- Distinguish between: truly missing, intentionally blank (e.g., optional fields), and encoded as zero/placeholder

### Row completeness
- Calculate per-row completeness: (non-null fields / total fields) x 100
- Flag rows with <50% completeness for potential exclusion
- Report: "X of Y rows are fully complete; Z rows have significant gaps"

### Date coverage
- Identify the date range in the data
- Check for gaps (missing days, weeks, months in a time series)
- Report: "Data covers [start] to [end] with [N] gaps in coverage"

## 2. Consistency

### Date formats
- Check for mixed date formats (MM/DD/YYYY vs. DD/MM/YYYY vs. YYYY-MM-DD)
- Attempt auto-detection; if ambiguous (e.g., 03/04/2025), ask the user
- Normalize to ISO 8601 (YYYY-MM-DD) for analysis

### Categorical values
- Check for variant spellings, casing differences, trailing spaces
- Examples: "Active" vs. "active" vs. "ACTIVE" vs. " Active"
- Report unique values per categorical column and flag likely duplicates
- Normalize after confirming with user if ambiguous

### Unit consistency
- Check for mixed units in the same column (e.g., $ and EUR, kg and lbs)
- Check for mixed scales (e.g., some values in thousands, others in actuals)
- Flag and ask before normalizing

### Naming consistency
- Check column headers for typos, inconsistent naming conventions
- Report any columns that appear to contain the same data under different names

## 3. Validity

### Range checks
- Numeric columns: flag values outside expected ranges
  - Negative values where only positive expected (e.g., revenue, counts)
  - Zero values where zero is unusual (e.g., price, quantity)
  - Values orders of magnitude above/below the column median
- Date columns: flag future dates (if unexpected), dates before a reasonable start
- Percentage columns: flag values >100% or <0% (unless explicitly allowed)

### Type validation
- Check that numeric columns contain only numbers (no text mixed in)
- Check that date columns parse correctly
- Flag columns where >5% of values fail type validation

### Business rule validation
- Revenue = Quantity x Price (if all three columns exist)
- End date >= Start date
- Running totals match sum of components
- Report any violations found

## 4. Uniqueness

### Duplicate detection
- Check for exact duplicate rows
- Check for near-duplicates (same key fields, different minor fields)
- Report: "Found X exact duplicates and Y potential near-duplicates"

### Key column analysis
- Identify likely primary key columns (high cardinality, no nulls)
- Check uniqueness of suspected key columns
- Flag if a supposed unique identifier has duplicates

## 5. Timeliness

### Data freshness
- Note the most recent date in the dataset
- If more than 30 days old, add a staleness warning
- If more than 90 days old, flag as historical baseline only

### Update frequency
- Infer the expected update frequency from the data (daily, weekly, monthly)
- Check if the most recent period is complete or partial
- Flag partial periods: "March 2025 data appears incomplete — only 15 of expected ~30 days present"

## 6. Outlier Detection

### Statistical outliers
- For numeric columns: flag values beyond 3 standard deviations from the mean
- For skewed distributions: use IQR method (below Q1 - 1.5*IQR or above Q3 + 1.5*IQR)
- Report outliers but do not auto-exclude — ask the user if they represent real events or errors

### Domain-based outliers
- Revenue: single transaction >10x the median transaction value
- Dates: entries on weekends/holidays if the business is weekday-only
- Counts: zero-activity periods in otherwise active time series
- Growth rates: single-period spikes >3x the typical rate

## 7. Privacy / PII Scan

Run this check before any analysis. PII detection takes priority over all other quality checks.

### Column-level PII detection
- **Email addresses:** columns matching `*@*.*` patterns
- **Phone numbers:** columns matching common phone formats (XXX-XXX-XXXX, (XXX) XXX-XXXX, +X XXXXXXXXXX)
- **SSN / government IDs:** columns matching XXX-XX-XXXX or similar national ID patterns
- **Physical addresses:** columns with street number + street name patterns, or labeled "address"
- **Dates of birth:** columns labeled "DOB", "birth", "birthday" or containing dates clearly in a birth-year range
- **Names combined with other PII:** a "Name" column alone is low risk, but Name + any of the above = PII dataset

### When PII is detected
1. Flag immediately and prominently — before any data quality or analysis output
2. List which columns contain PII and what type
3. Exclude all PII columns from analysis entirely
4. Do not reproduce, quote, or reference specific PII values anywhere in the output
5. Proceed with analysis on remaining non-PII columns only
6. Recommend: "Remove PII columns before sharing data for analysis"

### Decision rule
- **Any PII column detected** → exclude from analysis, flag at top of report, proceed with non-PII columns
- **All columns are PII** → cannot analyze; ask user to provide non-PII data

## Reporting Format

Present data quality findings in this structure:

```
## Data Quality Summary

**Dataset:** [name/description]
**Rows:** [count] | **Columns:** [count] | **Date range:** [start] to [end]
**Overall quality:** [Good / Moderate / Poor]

### Issues Found
- [Issue 1]: [description and impact on analysis]
- [Issue 2]: [description and impact on analysis]

### Actions Taken
- [Normalization or cleaning step 1]
- [Normalization or cleaning step 2]

### Caveats for Analysis
- [How remaining issues affect conclusions]
```

## Decision Rules

- **Completeness <80%** on a key analysis column → warn the user, proceed with caveats
- **Completeness <50%** on a key analysis column → recommend the user fix the data first
- **Duplicate rate >5%** → deduplicate before analysis, report what was removed
- **Mixed types >10%** in a column → column may need to be split or cleaned before use
- **Date gaps >20%** of expected periods → time-series trend analysis unreliable, use point-in-time comparisons instead
