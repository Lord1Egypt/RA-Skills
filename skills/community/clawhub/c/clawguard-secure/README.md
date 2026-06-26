# ClawGuard Security Assistant

Security assistant skill that helps you understand and act on [ClawGuard](https://clawguardsecurity.ai) scan reports — parsing, explaining, impact analysis, and guided remediation.

## What It Does

- **Reads and summarizes** exported JSON/Markdown scan reports
- **Explains findings** in clear, causal-chain language — deeper than the web UI
- **Analyzes fix impact** — checks whether a fix will break your existing skills or hooks
- **Guides remediation** — shows diffs, creates backups, applies fixes with your confirmation
- **Guides you through scanning** on clawguardsecurity.ai if you don't have a report yet

## Install

**With the OpenClaw CLI:**

```bash
openclaw skills install clawguard-security-assistant
```

**Or with ClawHub:**

```bash
clawhub install clawguard-security-assistant
```

**Manual:**

Copy this repo into your OpenClaw skills directory:

```bash
git clone https://github.com/R0llcre/clawguard-skill.git ~/.openclaw/skills/clawguard
```

Then start a new OpenClaw session.

## Usage

Just talk to your OpenClaw agent naturally:

- "Help me check my OpenClaw security"
- "Read this report ~/Downloads/clawguard-report.json"
- "Analyze this CLAWGUARD_ANALYSIS_V1 handoff from clawguardsecurity.ai"
- "What does OC-001 mean?"
- "Will fixing this break my Slack integration?"
- "Fix OC-001 for me"
- "Compare my old and new scan reports"

## What's Inside

```
SKILL.md                          — Module router and global rules
references/
  finding-catalog.md              — 116 rules from rulepack v2
  rule-deep-explainers.md         — Deep explanations for 33 L1 rules
  finding-explain.md              — Explanation templates and terminology
  report-parsing.md               — Report schema and summary templates
  impact-analysis.md              — Fix impact analysis workflow
  fix-procedures.md               — Step-by-step fix guidance
  fix-impact-patterns.md          — Common fix/breakage patterns
  scan-guide.md                   — How to scan on the website
scripts/
  parse-report.py                 — Report pre-processor for large scans
```

## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw) installed and running
- A ClawGuard scan report (get one at [clawguardsecurity.ai](https://clawguardsecurity.ai))

## License

MIT
