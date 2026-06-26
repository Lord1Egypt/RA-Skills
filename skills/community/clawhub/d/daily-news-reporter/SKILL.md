---
name: daily-news-reporter
description: |
  An AI-assisted international news reporting tool that helps generate professional daily reports 
  through structured workflows and multi-source verification frameworks.
  
  IMPORTANT: This is NOT a fully automated/unattended system. It requires an AI agent (like Claude, 
  GPT, or WorkBuddy) to execute the core information gathering steps using web search tools.
  
  The bundled scripts provide:
  - Structured data models for source tiering and verification
  - PDF report generation from Markdown
  - Report templates and formatting utilities
  - Source directory references
  
  Use this skill when you need:
  - Structured workflows for international news reporting
  - Multi-tier source verification frameworks (Tier 1-4)
  - Professional PDF report generation
  - Standardized templates for daily news summaries
  
  Requires: AI agent with web search capabilities for data collection
---

# Daily News Reporter

**AI-Assisted** international news reporting toolkit with structured workflows and multi-source verification.

## ⚠️ Important Clarification

This skill is **NOT a fully automated/unattended system**. It operates as an **AI-assisted workflow toolkit**:

| Component | What It Does | Who/What Executes |
|-----------|--------------|-------------------|
| `news_collector.py` | Data models, source classification, verification logic | AI Agent uses these structures |
| `generate_pdf.py` | Converts Markdown reports to PDF | Runs automatically |
| `SKILL.md` | Workflow instructions for AI | AI follows these guidelines |
| **Web Search** | Actual information gathering | **AI Agent executes via search tools** |
| **Analysis** | Content analysis and insight generation | **AI Agent performs** |

**Bottom line**: This skill provides the *framework and tools* for professional news reporting, but requires an AI agent with web search capabilities to perform the actual data collection and analysis.

## Overview

This skill provides structured workflows and utilities for generating professional daily international affairs reports:

1. **Structured Information Collection** - Tiered source system and verification frameworks
2. **Source Verification Guidelines** - Cross-reference methodologies and reliability indicators  
3. **Content Analysis Framework** - Impact assessment and trend analysis guidelines
4. **Report Generation Tools** - Markdown-to-PDF conversion and templates

## When to Use

Use this skill when:
- You need structured workflows for international news reporting
- You want consistent multi-tier source verification (Tier 1-4 system)
- You need professional PDF report generation from Markdown
- You want standardized templates for daily news summaries
- You're an AI agent helping a user generate news reports

**Do NOT expect**: Fully automated, unattended 24/7 news monitoring without AI involvement.

## Core Workflow (AI-Executed)

### Step 1: Information Collection (AI Agent Executes)

The AI agent performs web searches using the tiered source guidance:

**Search Guidance for AI:**
- Use web search tools to query current news
- Prioritize Tier 1 sources when available
- Collect 6-10 sources across different tiers
- Document source URLs and timestamps

**Tier 1 - Official/International Organizations (Reliability: 5/5)**
- UN News (news.un.org)
- International Maritime Organization (imo.org)
- Central bank official statements (federalreserve.gov, etc.)
- Government foreign ministry statements

**Tier 2 - Professional Financial Media (Reliability: 4-5/5)**
- Bloomberg, Reuters, CNBC
- Trading Economics
- 金十数据 (for Chinese market perspective)

**Tier 3 - Mainstream International Media (Reliability: 4/5)**
- CNN, BBC, AP News
- Major national news outlets

**Tier 4 - Regional/Industry Sources (Reliability: 2-3/5)**
- Local news for specific regions
- Industry publications
- Use with caution, require verification

**Recommended Search Queries:**
```
"[Date] international news global hot topics"
"[Organization] latest statement [topic]"
"[Market/commodity] price [date] latest"
"site:un.org [topic]"  # For official sources
"site:federalreserve.gov latest"
```

### Step 2: Information Processing (AI Agent Executes)

**Source Verification (AI performs):**
- Cross-reference key facts across minimum 2 independent sources
- Prioritize Tier 1 sources for critical information
- Flag information from Tier 3-4 sources with reliability indicators
- Use `news_collector.py` data structures to organize sources

**Structured Information Format:**
```
Event:
  - Time: [timestamp with timezone]
  - Location: [specific location]
  - Key Actors: [entities involved]
  - Verified Facts: [from Tier 1-2 sources]
  - Context: [background from multiple sources]
  - Impact: [market/geopolitical analysis]
```

### Step 3: Content Analysis (AI Agent Executes)

**Impact Assessment Framework:**
| Severity | Criteria | Examples |
|----------|----------|----------|
| ⭐⭐⭐⭐⭐ | Global impact, major powers involved, market shock | War escalation, central bank policy shifts |
| ⭐⭐⭐⭐ | Regional impact, economic consequences | Energy supply disruptions, trade conflicts |
| ⭐⭐⭐ | Localized but significant | National policy changes, major corporate events |
| ⭐⭐ | Limited impact | Routine diplomatic activities |
| ⭐ | Minor interest | Local news, minor incidents |

**Trend Analysis Guidelines:**
- Identify patterns across multiple events
- Compare with historical precedents
- Assess trajectory (escalating/stable/de-escalating)

### Step 4: Report Generation (AI + Scripts)

**AI Actions:**
1. Populate report template with collected data
2. Apply source attribution tags ([Official], [Professional], etc.)
3. Write analysis and insights
4. Save as Markdown file

**Automated Script Execution:**
```bash
# Convert Markdown to PDF (runs automatically)
python scripts/generate_pdf.py --input report.md --output report.pdf
```

## Source Reliability Framework

### Tier 1 - Official/International (Reliability: 5/5)
- **Use for:** Critical facts, official statements, verified data
- **Examples:** UN agencies, central banks, government statements
- **Attribution tag:** [Official], [Organization name]

### Tier 2 - Professional Financial (Reliability: 4-5/5)
- **Use for:** Market data, economic analysis, policy interpretation
- **Examples:** Bloomberg, Reuters, Trading Economics
- **Attribution tag:** [Professional], [Source name]

### Tier 3 - Mainstream Media (Reliability: 4/5)
- **Use for:** Event coverage, general news, context
- **Examples:** CNN, BBC, major national outlets
- **Attribution tag:** [International], [Source name]

### Tier 4 - Regional/Industry (Reliability: 2-3/5)
- **Use for:** Supplementary context, specific angles
- **Examples:** Local news, industry blogs
- **Attribution tag:** [Regional/Industry], [Source name], verification recommended

## Scripts and Utilities

### news_collector.py
**Purpose:** Data models and structures for source management
**Usage:**
```python
from scripts.news_collector import NewsCollector, NewsItem, NewsSource

collector = NewsCollector()
sources = collector.get_sources_by_topic('energy')
# Use data structures to organize collected information
```
**Note:** This is a data structure utility, NOT an automated web scraper.

### generate_pdf.py
**Purpose:** Convert Markdown reports to professionally formatted PDF
**Usage:**
```bash
python scripts/generate_pdf.py --input report.md --output report.pdf
```
**Note:** This runs automatically, no AI involvement required.

### Source Directory (references/source_directory.md)
**Purpose:** Reference list of recommended information sources
**Usage:** AI consults this when planning search strategy

## Report Templates

Templates available in `assets/templates/`:
- `daily_report_template.md` - Standard daily report format with placeholders
- Use as starting point, AI fills in content

## Best Practices for AI Agents

1. **Always verify critical information** across at least 2 Tier 1-2 sources
2. **Timestamp all data** with timezone and source publication time
3. **Distinguish facts from analysis** - clearly label opinions/forecasts
4. **Include contradictory information** when sources disagree, with attribution
5. **Update risk assessments** based on new developments
6. **Archive sources** - maintain links/references for fact-checking
7. **Be honest about limitations** - acknowledge when information is incomplete

## Quality Checklist

Before finalizing report:
- [ ] All Tier 1 facts verified with official sources
- [ ] Market data from Tier 2 financial sources
- [ ] Impact ratings justified with evidence
- [ ] Contradictory information noted
- [ ] Source attribution complete with tier tags
- [ ] Timestamps accurate
- [ ] PDF generated successfully
- [ ] No placeholder text remaining
- [ ] Clear distinction between facts and AI analysis

## Limitations and Disclaimers

### System Limitations
- **NOT unattended/fully automated** - Requires AI agent for data collection
- Information delayed by search indexing (typically 1-2 hours)
- Cannot access paywalled content
- Language limitations for non-English/non-Chinese sources

### Content Limitations
- Analysis based on publicly available information
- Predictions subject to rapid change in volatile situations
- No real-time data feeds - relies on search tools
- Source availability depends on search engine indexing

### Appropriate Use
- ✅ AI-assisted research and reporting
- ✅ Structured news summaries
- ✅ Educational/analytical purposes
- ✅ Personal information aggregation

### Inappropriate Use
- ❌ Unattended automated news service
- ❌ Real-time trading decisions without verification
- ❌ Replacement for professional journalism
- ❌ Source of truth for critical decisions without human review

## Example Usage

**User Request:** "Generate today's international news report"

**AI Agent Execution:**
1. Read SKILL.md to understand workflow
2. Use web search tools to query current news (6-10 sources)
3. Apply tiered verification framework
4. Structure information using news_collector.py patterns
5. Write analysis following impact assessment guidelines
6. Generate Markdown using template
7. Run generate_pdf.py to create PDF
8. Present both formats to user

**Output:** Professional daily report in Markdown and PDF formats

## Technical Requirements

### For AI Agent
- Web search capability (web_search tool or equivalent)
- Ability to read and execute Python scripts
- Markdown processing capability
- PDF viewing/verification capability

### For Script Execution
- Python 3.8+
- reportlab library (`pip install reportlab`)
- Standard library only for news_collector.py

## Files Included

```
daily-news-reporter/
├── SKILL.md                          # This file - workflow instructions
├── scripts/
│   ├── news_collector.py            # Data structures (not a scraper)
│   └── generate_pdf.py              # PDF generation tool
├── references/
│   └── source_directory.md          # Source reference list
└── assets/
    └── templates/
        └── daily_report_template.md # Report template
```

## License and Attribution

This skill provides frameworks and tools for news reporting.
Users are responsible for:
- Verifying information accuracy
- Complying with source website terms of service
- Proper attribution of quoted sources
- Responsible use of generated content

## Summary

| Feature | Status | Notes |
|---------|--------|-------|
| Automated PDF generation | ✅ Yes | `generate_pdf.py` |
| Structured workflows | ✅ Yes | SKILL.md guidelines |
| Source tiering framework | ✅ Yes | Tier 1-4 system |
| **Automated web scraping** | ❌ **No** | **AI performs searches** |
| **Unattended 24/7 operation** | ❌ **No** | **Requires AI agent** |
| Real-time data feeds | ❌ No | Search-based only |

**Bottom line:** This is an AI-assisted toolkit, not a fully autonomous news bot.
