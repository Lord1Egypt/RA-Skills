# Mode: analyze -- Full Competitor Analysis

Perform a comprehensive analysis of a competitor.

## Usage

```
/comp analyze <company-name>
```

## Process

### 1. Input
- Company name (normalized)
- Read industry context from `modes/_industry-context.md` based on configured industry

### 2. Research Phase
- [ ] **TODO: TavilySearch Integration**
  ```javascript
  // Target: comprehensive research on company
  tavilyResults = await TavilySearch({
    query: `${company} competitive analysis product pricing market`,
    maxResults: 10
  })
  ```
- WebSearch fallback for:
  - Company news and press
  - Product announcements
  - Pricing information
  - Customer reviews
  - Market reports

### 3. SWOT Analysis
Generate four-quadrant SWOT using industry-specific questions from `_industry-context.md`:
- **Strengths:** Product advantages, market position, brand (industry-specific)
- **Weaknesses:** Product gaps, limitations, customer complaints (industry-specific)
- **Opportunities:** Market trends, expansion potential, partnerships (industry-specific)
- **Threats:** Competitive pressure, market shifts, new entrants (industry-specific)

Apply the configured industry's scoring weights from `config/industry-profiles.yml`.

### 4. Scoring Phase
Score each dimension 1-5 using industry-adjusted weights from `config/industry-profiles.yml`:

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Product Maturity | X | [Reason] |
| Pricing | X | [Reason] |
| Market Presence | X | [Reason] |
| Feature Coverage | X | [Reason] |
| Brand Strength | X | [Reason] |
| Growth Trajectory | X | [Reason] |

**Global Score:** Weighted average using industry-specific weights

### 5. Confidence Assessment
- **High (4-5):** Multiple current sources, verified data
- **Medium (2-3):** Some data gaps, older sources
- **Low (1):** Limited data, significant assumptions

### 6. Output

#### Markdown Report
```markdown
# Competitor Analysis: [Company]

**Date:** YYYY-MM-DD
**Archetype:** [Detected]
**Overall Score:** X.X/5
**Confidence:** [Level]

## Executive Summary
[2-3 sentence overview]

## Scoring Matrix
[6-dimension table with scores and justifications]

## SWOT Analysis
[Four-quadrant analysis]

## Key Findings
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

## Sources
- [Source 1]
- [Source 2]

**Source:** [URL]
```

#### HTML Report (optional)
- [ ] **TODO: Playwright Integration**
  ```javascript
  // Generate HTML report
  await Playwright.screenshot({ /* report snapshot */ })
  ```

### 7. Save Results
- Save markdown to `reports/{num}-{company-slug}-{date}.md`
- Update `data/profiles/{company-slug}/profile.md`
- Save SWOT to `data/swot-analysis/{company-slug}.md`
- Add entry to `data/competitors.md` if new

## Example

```
/comp analyze Anthropic
/comp analyze "OpenAI"
```

## Output Files

- Report: `reports/{###}-{company-slug}-{YYYY-MM-DD}.md`
- Profile: `data/profiles/{company-slug}/profile.md`
- SWOT: `data/swot-analysis/{company-slug}.md`

## TODO Checklist

- [ ] Implement TavilySearch for deep research
- [ ] Implement Playwright for HTML report generation
- [ ] Add confidence scoring
- [ ] Add trend analysis (vs last analysis)
