# Mode: report -- Report Generation

Generate professional reports from competitor data.

## Usage

```
/comp report
/comp report <company-name>
/comp report --filter <company1>,<company2>
/comp report --date <start-date>:<end-date>
/comp report html
```

## Report Types

### 1. Executive Summary
- High-level overview of competitive landscape
- Top threats and opportunities
- Recommended actions

### 2. Competitive Landscape
- Full analysis of all tracked competitors
- Market positioning map
- Feature comparison matrix

### 3. Company Deep Dive
- Detailed analysis of single competitor
- Full SWOT
- Historical tracking

### 4. Trend Report
- Score changes over time
- Market movement analysis
- Emerging threats

### 5. Custom Report
- Filter by company, date, archetype
- Select specific sections

## Process

### 1. Aggregate Data
- Read from `data/competitors.md`
- Load profiles from `data/profiles/`
- Load SWOT from `data/swot-analysis/`
- Load pricing from `data/pricing-snapshots/`
- Load reports from `reports/`

### 2. Generate Content

#### Sections
1. **Header:** Report type, date range, companies included
2. **Executive Summary:** 3-5 key findings
3. **Competitive Matrix:** All companies with scores
4. **Detailed Analysis:** By company or section
5. **Trend Analysis:** Changes since last report
6. **Recommendations:** Action items

### 3. Output Formats

#### Markdown
```markdown
# Competitive Report: [Type]

**Generated:** YYYY-MM-DD
**Period:** [Date Range]
**Companies:** [N]

## Executive Summary
[3-5 key findings]

## Competitive Matrix

| Company | Score | Archetype | Trend |
|---------|-------|-----------|-------|
| ... | ... | ... | ... |

## [Section Name]
[Content]

## Recommendations

1. [Action 1]
2. [Action 2]
```

#### HTML (TODO)
- [ ] **TODO: Playwright Integration**
  ```javascript
  await Playwright.renderHTML({
    template: 'templates/report.html',
    data: reportData
  })
  ```

#### PDF (TODO)
- [ ] **TODO: PDF Generation**
  ```bash
  node generate-pdf.mjs --report reports/{name}.md
  ```

## Templates

### Report Template Location
- `templates/report.html` - HTML template for PDF generation
- `templates/report.css` - Styling

### Customization
Edit templates to customize:
- Header/footer
- Branding
- Color scheme
- Sections included

## Filters

### By Company
```
/comp report Anthropic
/comp report --filter Anthropic,OpenAI
```

### By Date Range
```
/comp report --date 2026-01-01:2026-03-31
```

### By Archetype
```
/comp report --archetype "Direct Competitor"
```

### By Score Range
```
/comp report --score "4.0:"
```

## Output Files

- Report: `reports/{type}-{YYYY-MM-DD}.md`
- HTML: `output/{type}-{YYYY-MM-DD}.html`
- PDF: `output/{type}-{YYYY-MM-DD}.pdf`

## Example

```
/comp report
/comp report Anthropic
/comp report --filter "Direct Competitor" --date 2026-01-01:
/comp report --type executive
```

## TODO Checklist

- [ ] Implement report template system
- [ ] Add HTML report generation with Playwright
- [ ] Add PDF export
- [ ] Implement date range filtering
- [ ] Add trend analysis section
- [ ] Implement custom report builder
