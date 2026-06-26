# Daily News Reporter

**AI-Assisted International News Reporting Toolkit**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ⚠️ Critical Clarification

**This is NOT a fully automated, unattended news bot.**

This skill provides structured workflows, data models, and utilities to help **AI agents** (like Claude, GPT, or WorkBuddy) generate professional news reports. The actual data collection requires an AI agent with web search capabilities.

### What This Skill Actually Does

| Component | Function | Automation Level |
|-----------|----------|------------------|
| `SKILL.md` | Workflow instructions for AI agents | Manual (AI follows) |
| `news_collector.py` | Data structures for organizing sources | Utility library |
| `generate_pdf.py` | Markdown to PDF conversion | **Fully automated** |
| `source_directory.md` | Reference list of news sources | Reference material |
| **Web search** | Actual information gathering | **AI agent performs** |

### Key Point

```
User Request → AI Agent Reads SKILL.md → AI Performs Web Searches → 
AI Structures Data → AI Writes Report → Script Generates PDF → Output
     ↑_________________ AI does this ___________________↑
                                     ↑___ Script does this ___↑
```

## Features

### ✅ Included
- **Structured workflows** for professional news reporting
- **Multi-tier source verification** framework (Tier 1-4)
- **PDF report generation** from Markdown
- **Report templates** for consistent formatting
- **Source classification** utilities

### ❌ Not Included
- **Automated web scraping** - AI performs searches
- **Real-time data feeds** - Search-based only
- **Unattended 24/7 operation** - Requires AI agent
- **Independent news monitoring** - Needs AI involvement

## Installation

### For AI Platforms (WorkBuddy, OpenClaw, etc.)

```bash
# Clone or copy skill to your AI platform's skills directory

# WorkBuddy
cp -r daily-news-reporter ~/.workbuddy/skills/

# OpenClaw
cp -r daily-news-reporter ~/.openclaw/skills/
```

### Python Dependencies

```bash
pip install reportlab
```

## Usage

### As an AI Agent

When a user asks for a news report:

1. **Read SKILL.md** to understand the workflow
2. **Use web search** to collect current news (following Tier 1-4 guidance)
3. **Apply verification** - cross-reference key facts
4. **Structure information** using `news_collector.py` patterns
5. **Generate Markdown** using the template
6. **Create PDF** by running `generate_pdf.py`
7. **Present results** to user

### As a User

Simply ask your AI assistant:

> "Generate today's international news report"

The AI will:
- Follow the structured workflow
- Collect information from multiple sources
- Apply source verification
- Generate professional PDF report

## Source Tier System

| Tier | Type | Reliability | Use For |
|------|------|-------------|---------|
| 1 | Official/International | 5/5 | Critical facts, official statements |
| 2 | Professional Financial | 4-5/5 | Market data, economic analysis |
| 3 | Mainstream Media | 4/5 | Event coverage, general news |
| 4 | Regional/Industry | 2-3/5 | Supplementary context (verify first) |

## Example Output

The skill generates professional reports including:

- 📌 Executive Summary (5 key events)
- 🔥 Detailed Coverage (event analysis)
- 📊 Market Data (energy, equities, forex)
- 💡 Key Insights (trend analysis)
- ⚠️ Risk Assessment (high/medium/low)
- 📎 Source Attribution (with tier tags)

## Technical Details

### File Structure

```
daily-news-reporter/
├── SKILL.md                     # Main workflow instructions
├── README.md                    # This file
├── scripts/
│   ├── news_collector.py       # Data structures (not a scraper!)
│   └── generate_pdf.py         # PDF generation tool
├── references/
│   └── source_directory.md     # Source reference list
└── assets/
    └── templates/
        └── daily_report_template.md
```

### Requirements

- **AI Agent with web search capability** (required for data collection)
- Python 3.8+ (for PDF generation)
- reportlab library

## Limitations

1. **Not Unattended**: Requires AI agent for data collection
2. **Search-Based**: Information delayed by search indexing (1-2 hours)
3. **No Real-Time Feeds**: No direct API connections to news services
4. **Language Limited**: Optimized for English and Chinese sources
5. **No Paywall Access**: Cannot access subscription-only content

## Use Cases

### ✅ Appropriate
- AI-assisted news research and summarization
- Structured daily news briefings
- Educational/analytical purposes
- Personal information aggregation
- Learning journalism best practices

### ❌ Inappropriate
- Fully automated news service without oversight
- Real-time trading decisions
- Replacement for professional journalism
- Unattended monitoring system

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please ensure:
- Clear documentation of what is/isn't automated
- Honest representation of capabilities
- No claims of full automation when AI involvement is required

## Acknowledgments

This skill was developed to demonstrate structured AI-assisted workflows for professional reporting. It showcases how AI agents and utility scripts can work together effectively.

---

**Remember**: This is a toolkit for AI agents, not a standalone automation system.
