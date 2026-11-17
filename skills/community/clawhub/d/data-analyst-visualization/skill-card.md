## Description:

LLM-powered intelligent data analysis assistant supporting natural language queries, SQL generation, visualization, and multi-turn conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Business analysts, data teams, and developers use this skill to query databases or local tabular files in natural language, generate read-only SQL, summarize results, and create charts for reporting and exploration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle real company or personal data through database connections, local files, row previews, and generated reports.

Mitigation: Use least-privilege read-only database accounts, avoid entering production passwords in chat, mask or exclude sensitive fields, and review file previews before sharing outputs.

Risk: Generated SQL may be incorrect, overly broad, or unsuitable for the intended data scope.

Mitigation: Inspect generated SQL before execution and apply table whitelists, LIMIT clauses, and time-range constraints for large or sensitive datasets.

Risk: Generated HTML reports are persistent files and may execute third-party JavaScript from a CDN when opened.

Mitigation: Store reports in approved locations, avoid embedding sensitive data unless appropriate, and review CDN use before opening or distributing generated HTML.

## Reference(s):

- [Data Source Configuration & Connection](references/data-sources.md)
- [HTML Visualization Page Template](references/visualization-template.md)
- [ClawHub Skill Page](https://clawhub.ai/openlark/skills/data-analyst-visualization)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with generated SQL snippets, ASCII trends, analysis notes, and optional standalone HTML visualization files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use configured databases or local files; generated SQL is intended to be read-only SELECT; generated HTML reports can load Chart.js from a CDN.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
