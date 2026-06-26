# Web Research Skill

**Version:** 2.1.0
**Author:** Claw 🦾
**Purpose:** Generate structured research reports with source citations, quality scoring, and automated follow-ups.

---

## Overview

The web-research skill automates end-to-end research: parse question → generate diverse queries → search → fetch → follow-up → deduplicate → synthesize → report.

**Key improvements over v1:**
- **Automated follow-up queries** — 2 rounds of follow-ups based on initial findings
- **Quality scoring** — each source scored (0-1) on content depth, URL, title, date
- **Source deduplication** — remove duplicate sources, keep the most detailed
- **Batch research mode** — process multiple topics in one session
- **Multiple output formats** — markdown (default), JSON, HTML
- **Topic extraction** — intelligent keyword extraction from natural language questions

---

## How to Use

### Basic Usage

```bash
# Single research question
python3 scripts/research.py "What is the state of AI regulation in the EU for 2026?"

# With more follow-up rounds
python3 scripts/research.py --followups 5 "Market analysis for renewable energy in Czech Republic"

# JSON output
python3 scripts/research.py --format json "Cryptocurrency regulation 2026"

# HTML output
python3 scripts/research.py --format html "Competition in cloud computing market"

# Custom source limit
python3 scripts/research.py --sources 15 "Best pricing for SaaS tools small business"
```

### Batch Mode

Create a JSON file (`questions.json`):
```json
{
  "questions": [
    "State of AI regulation in the EU for 2026",
    "Best SaaS tools for small business automation",
    "Cryptocurrency regulation trends 2026"
  ]
}
```

Then run:
```bash
python3 scripts/research.py --batch questions.json
```

---

## Pipeline Steps

### Step 1: Parse Question
Extract meaningful topic keywords from natural language question. Removes stop words, keeps entities and key terms.

### Step 2: Generate Queries
Create 5 diverse query variants:
- Exact match
- Broad match
- Time-aware (2025/2026)
- Analytical
- Market data focused

### Step 3: Execute Searches
Run web_search for each query variant. Collect results with title, URL, snippet.

### Step 4: Fetch Content
Use web_fetch to extract content from top URLs. Store full text for synthesis.

### Step 5: Follow-up Queries (v2)
Based on initial findings, generate 2 rounds of follow-up searches:
- Look for emerging themes in findings
- Add time-aware follow-ups
- Fill information gaps
- Increase coverage and accuracy

### Step 6: Deduplicate & Score
Remove duplicate sources by URL. Score each source (0-1) based on:
- Has URL (+0.2), has title (+0.15), has details (+0.3)
- Content length > 100 chars (+0.2), has date (+0.15)

### Step 7: Synthesize & Report
Combine findings into structured report with:
- Executive summary
- Numbered key findings with quality tags
- Quality assessment table
- Limitations and methodology
- Source citations

---

## Report Formats

### Markdown (default)
Rich text with headings, tables, bullet lists. Suitable for reading and sharing.

### JSON
Structured data output. Suitable for programmatic processing, APIs, dashboards.

### HTML
Self-contained styled report. Suitable for web viewing, email attachments.

---

## Output Files

Reports saved to: `workspace/research/web-research-YYYY-MM-DD-<topic>.md`

JSON reports: `workspace/research/web-research-YYYY-MM-DD-<topic>.json`

HTML reports: `workspace/research/web-research-YYYY-MM-DD-<topic>.html`

---

## Quality Rules

1. **Cross-reference** — at least 2 sources per major claim
2. **Flag outdated info** — >2 years old for fast-moving topics
3. **Distinguish opinion vs data** — clearly mark analytical content
4. **Cite every source** — URL for every factual claim
5. **Note conflicts** — when sources disagree, document both views
6. **Score sources** — low-quality sources flagged in report

---

## Skill Dependencies

- `web_search` — search the web via SearXNG
- `web_fetch` — fetch and extract content from URLs
- `write` — generate and save reports
- `exec` — run pipeline scripts

---

## Pricing

| Tier | Price | Description |
|------|-------|-------------|
| Single report | €25-50 | One research question, full pipeline |
| Batch research | €50-100 | Multiple questions (up to 5) |
| Deep dive | €75-150 | Extended follow-ups, expert sources |
| Retainer | €100-300/mo | Ongoing research, weekly reports |

---

## File Structure

```
web-research/
  SKILL.md                              — This file
  scripts/
    research.py                         — Research pipeline v2.1.0
  references/
    synthesis-framework.md              — How to synthesize findings
    report_template.md                  — Standard report structure
    search-strategies.md                — Query generation best practices
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-19 | Initial release |
| 2.0.0 | 2026-04-27 | Follow-up queries, quality scoring, batch mode, multiple formats |
| 2.1.0 | 2026-04-27 | HTML output, improved topic extraction, deduplication |
