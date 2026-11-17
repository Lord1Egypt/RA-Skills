## Description:

Alpha Pulse provides a China A-share T+1 short-term signal scaffold for scanning the market, ranking Top 30 next-day candidates, and generating signal reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[77spongebob](https://clawhub.ai/user/77spongebob)

### License/Terms of Use:


## Use Case:

Developers and market-analysis users use this skill to scaffold daily post-close A-share screening, next-day short-term signal ranking, and Markdown/CSV/chart report generation. Outputs should be treated as informational market-analysis material, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned Python dependencies and market-data packages may change behavior over time.

Mitigation: Install dependencies in an isolated virtual environment and pin package versions before operational use.

Risk: Generated reports, CSV files, or charts could overwrite or add files in a workspace.

Mitigation: Review generated file paths and contents before overwriting existing workspace files.

Risk: Optional market-data tokens may be stored or used by configuration and data-fetching flows.

Mitigation: Avoid entering optional tokens unless their storage location and use are understood.

Risk: Stock predictions can be mistaken for financial advice.

Mitigation: Treat all predictions and rankings as informational market-analysis outputs.

## Reference(s):

- [Alpha Pulse on ClawHub](https://clawhub.ai/77spongebob/skills/alpha-pulse)
- [Publisher profile: 77spongebob](https://clawhub.ai/user/77spongebob)

## Skill Output:

**Output Type(s):** [Text, Markdown, CSV, Charts, Shell commands, Configuration]

**Output Format:** [Markdown reports, CSV exports, chart files, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include desktop notification guidance; generated files should be reviewed before overwriting workspace content.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-03-08)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
