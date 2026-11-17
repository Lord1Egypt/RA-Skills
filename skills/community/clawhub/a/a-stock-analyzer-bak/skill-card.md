## Description:

Analyzes China A-share stocks with technical and financial filters and generates market summaries, stock recommendations, buy ranges, target prices, stop-loss levels, and position sizing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nowly-echo](https://clawhub.ai/user/nowly-echo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to run A-share market screening workflows and produce Markdown reports with candidate stocks, reasons, and trade-planning levels. Outputs should be reviewed as financial analysis rather than treated as verified investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce concrete buy, sell, stop-loss, and allocation suggestions.

Mitigation: Treat financial outputs as unverified analysis, review recommendations manually, and do not execute trades without independent validation.

Risk: The artifact may use cached, default, or simulated financial data when live data is unavailable.

Mitigation: Confirm data freshness and source quality before relying on a generated report.

Risk: Configured webhook delivery can send generated reports outside the local machine.

Mitigation: Disable webhook push unless external delivery is intended and verify webhook destinations before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nowly-echo/skills/a-stock-analyzer-bak)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with console text, Python scripts, shell command examples, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write timestamped Markdown reports under reports/ and may send reports to configured webhooks.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 2.1.0 and artifact _meta.json lists 2.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
