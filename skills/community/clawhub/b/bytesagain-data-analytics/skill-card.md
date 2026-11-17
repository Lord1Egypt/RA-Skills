## Description:

Analyze CSV files with statistical summaries, correlations, pivot tables, value rankings, trend charts, and data quality reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to explore local CSV exports, inspect data quality, compare numeric columns, summarize top values, and build quick pivot-style summaries from the terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper reads local CSV files selected by the user, so sensitive dataset contents may be processed in the agent environment.

Mitigation: Run it only on CSV files you intend the agent environment to inspect, and avoid using confidential exports unless the environment is approved for that data.

Risk: The security evidence notes limited script quality, which could produce unreliable analysis for important decisions.

Mitigation: Review command output before relying on it, and validate important statistics with a trusted analysis tool.

Risk: The skill does not clearly declare its tool scope in the provided metadata.

Mitigation: Confirm that bash and python3 execution are acceptable before installation or use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/skills/bytesagain-data-analytics)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the selected CSV file, command, and column arguments; analysis runs locally through bash and python3.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
