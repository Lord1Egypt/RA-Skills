# Analysis and Report Template

This template handles the final analysis of extracted data and generates comprehensive reports.

## Process

### Step 1: Data Cleaning and Normalization

**Deduplication**:
- Remove exact duplicates
- Remove near-duplicates (90%+ similarity)
- Keep the most complete/authoritative version

**Normalization**:
- Dates: Convert to ISO 8601 format (YYYY-MM-DD)
- Currencies: Convert to numbers, store currency separately
- Numbers: Remove commas, formatting
- Text: Trim whitespace, normalize line breaks
- URLs: Ensure well-formed, remove tracking parameters

**Standardization**:
- Units: Convert to standard units (USD, km, kg, etc.)
- Categories: Map to standard taxonomy
- Ratings: Convert to common scale (0-5 or 0-10)
- Locations: Standardize country/city names

### Step 2: Statistical Analysis

**Descriptive Statistics**:
```javascript
{
  "count": total_number_of_items,
  "min": minimum_value,
  "max": maximum_value,
  "mean": average_value,
  "median": middle_value,
  "mode": most_common_value,
  "stddev": standard_deviation,
  "quartiles": {
    "q1": 25th_percentile,
    "q2": 50th_percentile,
    "q3": 75th_percentile
  }
}
```

**Distribution Analysis**:
- Identify clusters and patterns
- Detect outliers (values > 2 std deviations from mean)
- Analyze frequency distributions
- Visualize with histograms (if applicable)

**Trend Analysis**:
- Compare across time periods
- Identify growth/decline patterns
- Calculate rates of change
- Detect seasonality

### Step 3: Comparative Analysis

**Cross-Source Comparison**:
- Compare data from different sources
- Identify agreements and discrepancies
- Validate findings across sources
- Calculate inter-source reliability

**Benchmarking**:
- Compare against industry averages
- Identify above/below average performers
- Calculate percentiles and rankings
- Highlight leaders and laggards

**Correlation Analysis**:
- Find relationships between variables
- Calculate correlation coefficients
- Identify causal factors (where appropriate)
- Spot unexpected correlations

### Step 4: Insight Generation

**Key Findings**:
1. **Most Important**: What are the top 3-5 most significant insights?
2. **Surprising**: What's unexpected or counterintuitive?
3. **Actionable**: What can the user do with this information?
4. **Trends**: What patterns or changes are emerging?
5. **Outliers**: What stands out from the norm?

**Data-Backed Insights**:
Every insight should include:
- The finding (what)
- The evidence (data)
- The significance (so what)
- The implication (now what)

### Step 5: Report Generation

Choose the appropriate format based on `output_format`:

#### Markdown Format

Clean, readable markdown with:
- Clear headings hierarchy
- Bullet points for lists
- Tables for structured data
- Code blocks for JSON/data
- Links to sources

#### JSON Format

Structured JSON with:
- Metadata (query, timestamp, method)
- Summary statistics
- Raw and processed data
- Sources and provenance
- Validation information

#### Report Format

Comprehensive document with:
- Executive summary (1-2 pages)
- Detailed findings (5-10 pages)
- Methodology section (1 page)
- Data visualizations (tables, charts)
- Recommendations section (1-2 pages)
- Appendices (raw data, sources)

## Report Structure

### Executive Summary

**Purpose**: Give key insights in 2-3 minutes

**Content**:
- Brief overview of research scope
- Top 3-5 key findings
- Most important recommendations
- Confidence level in findings

**Length**: 2-3 paragraphs

### Key Findings

**Purpose**: Detail the main discoveries

**Structure**:
```markdown
## Finding 1: [Descriptive Title]

**Summary**: One-sentence summary

**Details**: Elaborate on the finding with supporting data

**Evidence**:
- Data point 1
- Data point 2
- Data point 3

**Impact**: Why this matters

**Source**: [Source URL](https://example.com)
```

### Detailed Analysis

**Purpose**: Provide in-depth exploration

**Content**:
- Statistical breakdown
- Comparisons and benchmarks
- Trends over time
- Subgroup analyses
- Correlations and relationships

### Methodology

**Purpose**: Document research process

**Content**:
- Sources searched
- Number of URLs analyzed
- Tools and methods used
- Data quality assessment
- Limitations and caveats

### Recommendations

**Purpose**: Actionable next steps

**Format**:
```markdown
## Recommendation 1: [Action Title]

**Priority**: High/Medium/Low

**Action**: What to do

**Rationale**: Why to do it

**Expected Impact**: What outcome to expect

**Effort**: How difficult (Easy/Medium/Hard)
```

### Sources

**Purpose**: Provide traceability

**Format**: Numbered list with URLs and titles

## Data Visualization

### Tables

For structured data:

```markdown
| Product | Price | Rating | Reviews |
|---------|-------|--------|---------|
| Item 1  | $29.99| 4.5    | 1,234   |
| Item 2  | $49.99| 4.7    | 567     |
```

### Statistics

For numerical data:

```markdown
## Price Analysis

- **Count**: 45 products
- **Range**: $15.00 - $299.99
- **Average**: $87.50
- **Median**: $79.99
- **Std Dev**: $45.30

**Distribution**:
- Under $50: 12 products (27%)
- $50-$100: 20 products (44%)
- $100-$150: 8 products (18%)
- Over $150: 5 products (11%)
```

### Rankings

For comparative data:

```markdown
## Top 5 by Rating

1. **Product A** - 4.9/5 (2,345 reviews)
2. **Product B** - 4.8/5 (1,234 reviews)
3. **Product C** - 4.7/5 (987 reviews)
4. **Product D** - 4.6/5 (765 reviews)
5. **Product E** - 4.5/5 (654 reviews)
```

## Quality Assurance

### Data Quality Checks

- [ ] All data points have sources
- [ ] Statistics are calculated correctly
- [ ] Findings are supported by data
- [ ] No contradictions in the report
- [ ] All URLs are accessible
- [ ] Spelling and grammar checked
- [ ] Formatting is consistent

### Validation

- Cross-check findings with raw data
- Verify statistical calculations
- Ensure logical consistency
- Check for bias or misinterpretation

## Output Examples

### Quick Research Output

```markdown
# Quick Research: iPhone 15 Price

**Date**: 2024-01-22
**Sources**: Google, Amazon, Best Buy
**URLs Analyzed**: 5

## Summary

Found 5 retailers selling iPhone 15 Pro Max 256GB.
Price range: $999 - $1,099
Best deal: Walmart at $999 (save $100)

## Prices

1. Walmart: $999 ✓ Best Price
2. Amazon: $1,049
3. Best Buy: $1,069
4. Target: $1,079
5. Apple: $1,099

## Recommendation

Buy from Walmart to save $100 compared to Apple.
```

### Comprehensive Report Output

See the main template for full report structure.

## Best Practices

1. **Start with Summary**: Most users only read the executive summary
2. **Use Visuals**: Tables, lists, and formatting improve readability
3. **Be Specific**: Use exact numbers, not vague descriptions
4. **Provide Context**: Explain why findings matter
5. **Cite Sources**: Every data point should have a source
6. **Be Honest**: Admit limitations and uncertainties
7. **Make it Actionable**: Tie findings to recommendations
8. **Keep it Concise**: Respect the user's time
