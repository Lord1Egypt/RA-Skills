# Feishu Document Format Report Template

## Output Format Description

The analysis report is output in Feishu document rich text format, containing the following structure. The Agent populates each section sequentially according to this template.

## Template Structure

### I. Analysis Overview

```
📊 **Analysis Topic**: [Topic name derived from L1 Persona]
👤 **Analysis Perspective**: [Role]  |  [Decision Scenario]
📅 **Analysis Period**: [Time range]

**One-Sentence Conclusion**: [One-sentence summary of core finding, including key numbers]
```

### II. Key Findings

Format for each finding:
```
### Finding [N]: [Finding Title]

**Data Evidence**:
- [Data point 1]: [Explanation]
- [Data point 2]: [Explanation]

**Confidence**: [High/Medium/Low] — [Reason for annotation]
```

Confidence standards:
- **High**: Results validated by primary and alternative methods with consistency, high data completeness
- **Medium**: Results derived from a single method, relatively complete data
- **Low**: Significant missing data, small sample size, or inconsistency with alternative method results

### III. Analysis Process

```
### Methods Used
- **Primary Method**: [Method name] — [Selection rationale]
- **Cross-Validation**: [Alternative method] — [Validation result: consistent/differences exist]

### Data Scope
- Data Source: [Source description]
- Time Window: [Start and end dates]
- Filter Conditions: [Key filters]
- Data Scale: [# records × # fields]

### Key Assumptions
1. [Assumption 1 and rationale]
2. [Assumption 2 and rationale]
```

### IV. Detailed Results

```
### [Analysis Dimension 1]

**Chart Description**: [Chart name + core information displayed]

**Statistical Results**:
- [Metric/Statistic]: [Value] ([Statistical parameters])
- [Metric/Statistic]: [Value] ([Statistical parameters])

**Interpretation**: [What the results mean for the business]
```

(Repeat above structure for each analysis dimension)

### V. Conclusions & Recommendations

```
### Conclusions

1. **[Conclusion 1 Title]**: [Conclusion text]  ⚡Confidence: [High/Medium/Low]
2. **[Conclusion 2 Title]**: [Conclusion text]  ⚡Confidence: [High/Medium/Low]

### Actionable Recommendations

| Priority | Recommendation | Expected Impact | Feasibility | Verification Method |
|----------|----------------|-----------------|-------------|----------------------|
| P0 (This week) | [Recommendation] | [Expected impact] | [Assessment] | [How to verify] |
| P1 (This month) | [Recommendation] | [Expected impact] | [Assessment] | [How to verify] |
| P2 (This quarter) | [Recommendation] | [Expected impact] | [Assessment] | [How to verify] |
```

### VI. Appendix

```
### Method Details
- [Method 1]: [Brief description and Python package dependencies]
- [Method 2]: [Brief description and Python package dependencies]

### Data Quality Notes
- Data Completeness: [Percentage/assessment]
- Known Limitations: [Data/method limitations]

### Follow-up Analysis Recommendations
- [Direction 1 for deeper analysis]
- [Direction 2 for deeper analysis]
```

## Output Considerations

- Do not include Python code or tool execution traces in the report
- Format numbers in a human-friendly way (e.g., "1.23 million" rather than "1,230,000")
- Use text to describe charts; do not actually generate images (unless requested by user)
- All comparative conclusions must specify the "comparison baseline"
- Avoid vague language (e.g., "significant" must be paired with p-value, "large" must be paired with percentage)