## Description:

数据分析与反馈 collects advertising performance data, analyzes campaign and material metrics, and returns reports and optimization feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeyeshield](https://clawhub.ai/user/jeyeshield)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators and developers use this skill to ingest advertising performance data, generate campaign and material reports, review insights, and receive optimization suggestions for future model or creative iterations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSV exports may be unsafe when material IDs can come from untrusted sources.

Mitigation: Treat exported CSV files as untrusted, avoid opening them directly in spreadsheet software, and add CSV escaping or formula neutralization before operational use.

Risk: Operators may not be prepared for Chinese-language commands and output.

Mitigation: Install only where Chinese-language operator workflows are acceptable, or localize command descriptions and returned messages before deployment.

Risk: Building from source with unpinned development dependencies can reduce reproducibility in controlled environments.

Mitigation: Pin development dependencies and build from a reviewed lockfile when using this package in controlled release pipelines.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, CSV, guidance]

**Output Format:** [Command responses containing structured JSON objects, Chinese-language status text, analytics reports, feedback suggestions, and CSV export text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated from in-memory campaign, material, performance, report, and alert data handled by the skill.]

## Skill Version(s):

1.0.0 (source: server release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
