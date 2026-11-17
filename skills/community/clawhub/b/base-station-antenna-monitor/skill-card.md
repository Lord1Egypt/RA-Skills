## Description:

Monitors recent base station antenna patents from core companies, classifies results into vibrator, radome, and reflector technical branches, and generates a structured HTML report with patent lists and technical summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and patent-analysis teams use this skill to monitor base station antenna patent activity across selected companies, categorize results by technical branch, and produce an HTML report for competitive tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can include unescaped patent data and unsafe links that may execute browser script when opened.

Mitigation: Use only trusted patent data sources, write reports to a controlled directory, and review generated reports before opening or sharing them.

Risk: The skill depends on configured patent data access; without that configuration, outputs may be limited to an analysis framework rather than live database conclusions.

Mitigation: Confirm Zhihuiya MCP authorization and tool availability before relying on generated monitoring results.

## Reference(s):

- [Zhihuiya Open Platform](https://open.zhihuiya.com/)
- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/base-station-antenna-monitor)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Analysis]

**Output Format:** [HTML report plus Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports configurable monitoring period, search limits, and output path; live patent retrieval requires configured Zhihuiya MCP access.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
