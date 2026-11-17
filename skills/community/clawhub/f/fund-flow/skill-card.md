## Description:

Fund Flow analyzes local Chinese A-share fund-flow CSV data to rank main-force and retail flows, detect trends, aggregate sectors, compare index flows, and export reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cqdev-ai](https://clawhub.ai/user/cqdev-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Fund Flow to inspect local Chinese A-share fund-flow CSV files for main-force inflow rankings, sector aggregation, trend detection, timeframe summaries, and index comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSV values such as stock or sector names are printed directly to the terminal.

Mitigation: Use trusted or redacted CSV files when terminal output may be logged or shared.

Risk: The optional JSON export writes to the user-provided output path.

Mitigation: Choose an output path where replacing an existing JSON report is acceptable.

Risk: Fund-flow analysis can be mistaken for investment advice.

Mitigation: Treat the reports as analytical reference material and review decisions independently.

## Reference(s):

- [Fund Flow on ClawHub](https://clawhub.ai/cqdev-ai/skills/fund-flow)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Terminal text reports with optional JSON export and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local CSV input and can write a JSON report when an output path is supplied.]

## Skill Version(s):

1.1.0 (source: CHANGELOG.md and package.json; ClawHub release metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
