# Data Analysis & Reporting

Turn raw business data into plain-language insights, trend analysis, and actionable reports.

## Status

v0.1.0 — Board-approved for publication. 43/45 QA score across 12 test cases.

## Structure

```
data-analysis-reporting/
├── README.md                          # This file
├── SKILL.md                           # Skill definition (triggers, workflow, output structure)
├── data-analysis-reporting-spec.md    # Full spec (purpose, capabilities, boundaries, market context)
└── references/
    ├── business-metrics.md            # Standard business metrics: formulas, interpretation, benchmarks
    ├── data-quality-checks.md         # Pre-analysis data validation checklist
    ├── report-templates.md            # 5 output templates (executive, detailed, comparison, trend, health check)
    └── test-prompts.md                # 12 test cases (4 happy, 4 normal, 4 edge)
```

## Key Design Decisions

- **Clarify first, analyze second.** The skill asks what decision the analysis supports before touching the data.
- **Data quality before results.** Every analysis starts with a quality check and reports issues upfront.
- **Insights over numbers.** Output leads with "what this means" not "what the number is."
- **Confidence labeling.** Every claim gets High/Moderate/Low/Flagged confidence.
- **Honest about limits.** Small samples, poor data quality, and insufficient evidence get clear warnings — not padding.

## Differentiator

Feels like a sharp junior analyst on staff, not a statistics engine. Asks clarifying questions, proposes an analysis plan, and surfaces follow-up questions the user hasn't thought to ask.

## License

Published by NorthlineAILabs.
