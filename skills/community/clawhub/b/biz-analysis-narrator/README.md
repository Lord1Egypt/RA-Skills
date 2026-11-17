# Business Analysis Narrator

> Turn financial and operating spreadsheets into judgment-rich narratives for management — variance attribution (price vs. volume), trend interpretation, three-line risk warnings, and action recommendations with owners and verification metrics.

**Category:** business-intelligence  |  **License:** CC-BY-4.0  |  **Version:** 1.0.0
**Price:** Free on GitHub & skills.sh (CC BY 4.0). Curated bundle on Gumroad: $29 (Pro $79).

## What it does

Executives can read a spreadsheet; they can't read what the spreadsheet means. Finance and ops burn 10+ hours a month copying numbers into slides and still can't write the 'why' and the 'so what'.

Turns tables into reports with judgment using a four-question narrative framework: what happened, why (variance attribution), where's the risk, so what (recommendations).

## What you get

- Variance attribution in three moves: price vs. volume decomposition, mix shift, one-off stripping.
- Three-line risk warnings: cash runway < 3 months, single-customer concentration > 30%, fixed-cost share jumping MoM.
- Recommendations: 2-3 executable items, each tagged with expected impact + owner role + verification metric.
- Outputs: one-page boss summary (5 sentences + 3 numbers + 1 decision request) and a full report with chart suggestions and detail annexes.

## How to use

- **As an agent skill:** drop `SKILL.md` into your agent's skills folder, or install from the GitHub repo below.
- **As a prompt pack:** open `SKILL.md` and follow the workflow section step by step.
- Works with any agent that reads `SKILL.md` (Claude Code, OpenCode, Cursor, Gemini CLI, Cline, and more).

## Install

```bash
# skills.sh / ClawHub
npx skills add https://github.com/chinabizskills/biz-analysis-narrator
# ClawHub (after publish)
openclaw skills install @chinabizskills/biz-analysis-narrator
```

Or clone: `git clone https://github.com/chinabizskills/biz-analysis-narrator.git`

## Pricing & license

Licensed under **CC BY 4.0** — free to use, share, and adapt (attribution required). A curated, expanded bundle (with the Pro templates) is sold on Gumroad for $29 (Pro $79). The free GitHub/skills.sh version is the complete, working skill.

## Tags

finance, business-analysis, management-reporting, data-storytelling, kpi

## Contents

- `SKILL.md` — the skill definition / prompt library (this is the product).
- `README.md` — this file.
- `skill-card.md` — ClawHub metadata card.
- `RELEASE_NOTES.md` — version history.

---

Part of the **China-Biz Skills** collection by RAY — practical AI agent skills for business, e-commerce, support, legal triage, and content.
