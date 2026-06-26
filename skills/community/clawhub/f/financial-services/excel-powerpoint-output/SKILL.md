---
name: financial-services-excel-powerpoint-output
description: >
  Use when generating Excel workbooks or PowerPoint decks for financial deliverables. Enforces consistent professional formatting for financial models, comps tables, pitch decks, and analytical reports. Applied after analysis is complete.
metadata:
  openclaw:
    emoji: "📐"
---

# Excel & PowerPoint Output

金融 Excel 工作簿和 PowerPoint Deck 的标准化格式规范。

**Announce at start:** "I'm using the excel-powerpoint-output skill to format the deliverable."

## Core Principle

格式一致性和专业性是金融交付物的基本要求。好的格式让审阅者快速找到关键信息，差的格式掩盖好的分析。

## Excel Formatting Standards

### Number Format

```
Type                | Format              | Example
--------------------|---------------------|----------
Revenue, large      | $#,##0.0"M"        | $4,218.5M
Revenue, small      | $#,##0.0"K"        | $421.8K
Percentages         | 0.00%              | 24.35%
Percentages (bps)   | 0 bps              | 235 bps
Multiples           | 0.00x              | 12.55x
Ratios              | 0.00               | 1.15
Share price         | $#,##0.00          | $142.55
Shares              | #,##0.0"M"         | 1,245.3M
Negative values     | (#,##0) or (0.0%)  | (125.5) or (2.3%)
N/A or N/M          | "N/A" or "N/M"     | text
```

### Color Coding

```
Element                  | Color (Light Mode) | Color (Dark Mode)
-------------------------|-------------------|------------------
Header row background    | #1F2937 (gray-800)| #F9FAFB (gray-50)
Header row text          | #FFFFFF (white)    | #111827 (gray-900)
Subheader background     | #E5E7EB (gray-200)| #374151 (gray-700)
Positive values          | #059669 (green-600)| #34D399 (green-400)
Negative values          | #DC2626 (red-600)  | #F87171 (red-400)
Covenant breach          | #FEE2E2 bg + red text|#7F1D1D bg + #FCA5A5
Covenant near-miss       | #FEF3C7 bg + amber  |#78350F bg + #FCD34D
Input cells              | #DBEAFE bg (blue)  | #1E3A5F bg
Calculated cells         | No background       | No background
Borders                  | #D1D5DB (gray-300) | #4B5563 (gray-600)
```

### Layout Rules

**General:**
- Freeze panes: freeze header row AND first column (company names)
- Column widths: auto-fit, minimum 10 characters
- Row heights: 15pt standard, 20pt for header rows
- Font: Calibri 10pt body, 11pt headers, 9pt footnotes
- Alignment: numbers right-aligned, text left-aligned, headers center-aligned

**Financial Model Tab:**
```
Column A: Row labels (left-aligned, bold for section headers)
Column B+: Periods (FY2023, FY2024, etc.)
Last column: CAGR or YoY change

Section headers: bold, light gray background
Subtotals: top border (thin line)
Grand totals: top and bottom border (double line)
Input assumptions: blue font or blue background
Calculated values: black font, no special background
```

**Comps Table Tab:**
```
Column A: Company name
Column B: Ticker
Column C+: Financial metrics and multiples
Last rows: Median, Mean, Min, Max, Target position

Sort order: by EV/EBITDA descending (or as specified)
Highlight: Target company row in light blue background
Outliers: gray italic with footnote explaining exclusion
```

**Sources Tab:**
```
Column A: Source abbreviation
Column B: Full source name
Column C: Data type
Column D: Retrieval date
Column E: Access method (API, manual, file)
Column F: Notes
```

### Tab Naming Convention

```
Tab Name            | Content
--------------------|----------------------------------------
Summary             | Key metrics overview
Income Statement    | P&L historical + projected
Balance Sheet       | BS historical + projected
Cash Flow           | CF historical + projected
Comps               | Comparable company analysis
DCF                 | Discounted cash flow model
Precedent Txns      | Precedent transactions
WACC                | WACC calculation details
Sensitivity         | Sensitivity tables
Sources             | Data sources and retrieval dates
```

## PowerPoint Formatting Standards

### Slide Layout

**Title Slide:**
```
[Company Logo if applicable]

[Title: Deliverable Name]
[Subtitle: Target Company / Fund / Line of Business]

[Date]
[Confidential / Internal Use Only]
```

**Standard Content Slide:**
```
[Slide Title — one clear message]

[Content area: chart, table, or text]

Source: [Provider], [Date]
```

**Section Divider:**
```
[Section Number]
[Section Title]
[Brief description of what's in this section]
```

### Chart Standards

**Colors:**
```
Series 1 (Primary):   #2563EB (blue-600)
Series 2 (Secondary): #059669 (green-600)
Series 3 (Tertiary):  #D97706 (amber-600)
Series 4 (Quaternary):#7C3AED (violet-600)
Negative/Benchmark:   #6B7280 (gray-500)
Target/Highlight:     #DC2626 (red-600)
```

**Chart Types:**
```
Data Type              | Chart Type           | When to Use
-----------------------|----------------------|---------------------------—
Composition            | Pie chart or stacked bar | Sector allocation, revenue breakdown
Time series            | Line chart           | Return trends, financial metrics over time
Comparison             | Grouped bar chart    | Peer comparison, before/after
Distribution           | Histogram or box plot| Return distribution, valuation range
Relationship           | Scatter plot         | Risk vs return, correlation
Flow                   | Waterfall chart      | EBITDA bridge, attribution breakdown
Heat map               | Conditional format   | Link ratio triangle, correlation matrix
```

**Chart Rules:**
- Title: describe the insight, not the data ("Tech outperformed by 250bps" not "Sector Returns")
- Axis labels: include units (%, $, x)
- Legend: only if 2+ series, position at bottom
- Data labels: only on key points (min, max, target)
- Gridlines: light gray, horizontal only (for bar/line charts)

### Text Standards

**Font:**
- Title: 24pt, bold
- Section header: 18pt, bold
- Body: 14pt, regular
- Footnote: 10pt, regular, gray
- Font family: Calibri or Arial (consistent throughout)

**Bullet Points:**
- Maximum 6 bullets per slide
- Maximum 2 lines per bullet
- Use parallel structure (all start with verb, or all noun phrases)
- Indent sub-bullets one level, smaller font (12pt)

**Tables in PowerPoint:**
- Header row: dark background, white text
- Alternating row colors: white and light gray
- Right-align numbers, left-align text
- Minimum font size: 10pt
- Maximum rows: 15 (split to next slide if more)

### Source Attribution in Decks

**Every data slide must have:**
```
Source: [Provider], [Date]
```

**Format:**
- Bottom-left or bottom-right of slide
- 10pt, gray text
- Include date of data retrieval

**If multiple sources:**
```
Sources: FactSet (prices), S&P Capital IQ (fundamentals), Author calculations
```

**For calculated values:**
```
Source: Author calculations based on [inputs]. See Appendix for details.
```

## Delivery Checklist

Before delivering any financial output:

**Excel:**
- [ ] All number formats consistent
- [ ] Color coding applied per standard
- [ ] Freeze panes set on all tabs
- [ ] Tab names follow convention
- [ ] Sources tab included
- [ ] Input cells distinguished from calculations
- [ ] Negative values in parentheses
- [ ] No #REF!, #VALUE!, #N/A errors (unless intentionally handled)

**PowerPoint:**
- [ ] Title slide with date and confidentiality notice
- [ ] One message per slide
- [ ] Source attribution on every data slide
- [ ] Consistent fonts and colors
- [ ] Charts follow type and color standards
- [ ] No orphan slides (every slide has context)
- [ ] Appendix for detailed supporting data
