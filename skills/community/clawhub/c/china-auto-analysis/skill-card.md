## Description:

Generates China auto market dashboard visualizations from akshare CPCA manufacturer ranking data, covering production, wholesale sales, retail sales, and year-over-year comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuehengzhang10-hub](https://clawhub.ai/user/xuehengzhang10-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and developers use this skill to run a Python dashboard generator for China passenger-vehicle manufacturer rankings, comparing production, wholesale sales, retail sales, KPI summaries, and prior-year performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bottom comparison chart can include generated wholesale and retail values that may appear to come from the stated CPCA market source.

Mitigation: Review the generated chart before use, disclose synthetic comparison values, or replace them with verified CPCA-sourced series before relying on the output.

Risk: Dependency versions are not locked, so output behavior may vary as akshare, pandas, matplotlib, or numpy change.

Mitigation: Pin and test dependency versions in the execution environment used for release or business analysis.

Risk: The dashboard may be used for business, market, or financial decisions despite source and methodology limitations.

Mitigation: Validate chart values against official releases and treat the generated dashboard as reference material, not decision authority.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuehengzhang10-hub/skills/china-auto-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash examples and a generated PNG dashboard file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python dependencies including akshare, pandas, matplotlib, and numpy; data retrieval depends on akshare CPCA interface availability.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
