# Mode: compare -- Competitor Comparison

Compare two competitors side-by-side.

## Usage

```
/comp compare <company1> vs <company2>
/comp compare <company1> and <company2>
```

## Process

### 1. Input
- Two company names
- Normalize both names

### 2. Load Data
- Read existing profiles from `data/profiles/`
- If missing, run abbreviated research
- Load most recent scores

### 3. Side-by-Side Analysis

#### Feature Matrix

| Feature | [Company 1] | [Company 2] |
|---------|-------------|-------------|
| Feature A | ✓/✗/Partial | ✓/✗/Partial |
| Feature B | ✓/✗/Partial | ✓/✗/Partial |
| ... | ... | ... |

#### Scoring Comparison

| Dimension | [Company 1] | [Company 2] | Delta |
|-----------|-------------|-------------|-------|
| Product Maturity | X | X | ±X |
| Pricing | X | X | ±X |
| Market Presence | X | X | ±X |
| Feature Coverage | X | X | ±X |
| Brand Strength | X | X | ±X |
| Growth Trajectory | X | X | ±X |
| **Overall** | **X** | **X** | **±X** |

#### SWOT Comparison

| | [Company 1] | [Company 2] |
|--|-------------|-------------|
| **Strengths** | S1, S2 | S1, S2 |
| **Weaknesses** | W1, W2 | W1, W2 |
| **Opportunities** | O1, O2 | O1, O2 |
| **Threats** | T1, T2 | T1, T2 |

### 4. Output

```markdown
# Competitive Comparison: [Company 1] vs [Company 2]

**Date:** YYYY-MM-DD

## Feature Matrix

[Matrix table]

## Scoring Comparison

[Comparison table with delta]

## SWOT Comparison

[SWOT table]

## Key Differentiators

### [Company 1] Advantages
- [Advantage 1]
- [Advantage 2]

### [Company 2] Advantages
- [Advantage 1]
- [Advantage 2]

## Winner Assessment

**Overall Winner:** [Company 1/2/Tie]
**By:** [Score differential]

**Recommendation:** [Based on user's competitive stance]
```

## Example

```
/comp compare Anthropic vs OpenAI
/comp compare Salesforce vs HubSpot
```

## Output Files

- Report: `reports/{###}-compare-{company1}-{company2}-{date}.md`

## Use Cases

- **Vendor selection:** Which competitor to partner with?
- **Competitive positioning:** Where do we stand?
- **Feature gap analysis:** What do we lack vs competition?
- **Pricing strategy:** How should we price relative to market?
