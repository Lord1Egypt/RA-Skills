# Capability Match

Intelligent skill routing for OpenClaw. Automatically discovers your installed skills and recommends the perfect one for any task.

## Quick Start

```bash
# Use capability-match (any of these):
use capability-match to: "your task here"
capability-match: "your task here"
what skill should i use for "your task"
```

## How It Works

1. Scans all installed skills (`skills/*/SKILL.md`)
2. Analyzes capabilities, triggers, and descriptions
3. Matches your natural language request to relevant skills
4. Returns top 3 recommendations with confidence scores
5. You choose which skill to use

## Example

**You:** `capability-match: create a dashboard from my CSV data`

**Response:**
```
🎯 Best match: data-analysis (Score: 94%)
   ↳ Analyzes, visualizes, and generates reports from data
   Commands: "analyze this data", "create a dashboard", "generate report"

🔹 Also consider: excel-xlsx (Score: 87%)
   ↳ Create and edit Excel workbooks with formulas and charts
   Commands: "create spreadsheet", "excel chart"

🔹 Also consider: powerpoint-pptx (Score: 76%)
   ↳ Create presentations with data charts and visualizations
   Commands: "make powerpoint", "create slides"

👉 Say "use data-analysis" to proceed.
```

## Installation

```bash
# Copy capability-match folder to:
~/.openclaw-autoclaw/skills/

# Or use ClawHub:
clawdhub install capability-match
```

## Configuration

Environment variables:
- `CAPABILITY_MATCH_THRESHOLD` - Minimum confidence (default: 30)
- `CAPABILITY_MATCH_MAX_RESULTS` - Max results (default: 3)

## Requirements

- OpenClaw with skills directory
- Node.js 18+

## License

MIT - Free to use, modify, redistribute.