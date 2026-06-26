---
name: crypto-paper
description: "Research, analyze, and summarize cryptocurrency whitepapers and research papers. Locate papers via web_search, fetch/extract with web_fetch, apply structured checklist (tokenomics, team, tech, risks), generate reports/investment memos. Use when: reviewing crypto projects ('analyze Solana whitepaper'), tokenomics breakdowns, due diligence, investment thesis on niche cryptos."
---

# Crypto Paper Analyzer

## Overview
Streamlined analysis of crypto whitepapers. Source papers, extract content, evaluate via proven checklist, output structured reports.

## Quick Start
```
1. web_search \"{project} whitepaper pdf\" count=5
2. web_fetch best URL maxChars=100000 extractMode=markdown
3. Apply checklist from references/whitepaper-checklist.md
4. Generate markdown report
```

## Analysis Workflow
1. **Source Paper**: Prioritize official GitHub/docs/project.site whitepapers.
2. **Extract Sections**: Use headings/keywords for problem/tech/token/team/roadmap.
3. **Evaluate**: Score vs checklist.
4. **Synthesize**: Pros/cons, investment score (1-10), key quotes.

## Tasks
### Whitepaper Summary
Concise 500-word overview + key metrics table.

### Tokenomics Audit
Pie chart (text), vesting risks, utility assessment.

### Investment Memo
1-pager: Thesis, bull/bear, allocation rec.

### Multi-Project Compare
Side-by-side on tokenomics/team/innovation.

## Resources
### references/whitepaper-checklist.md
Detailed evaluation framework.

### assets/report-template.md
Markdown template for reports.