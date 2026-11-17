## Description:

Chief Data & Insight Officer provides bilingual business data analysis, dashboard-style visualization, KPI diagnosis, quadrant positioning, ROI attribution, and strategic recommendations from structured or fragmented business inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[web-seeker](https://clawhub.ai/user/web-seeker)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external business users, and analysts use this skill to turn sales, advertising, operations, user, or other business data into charts, structured diagnosis, first-principles insight, and action recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may activate the skill in general data-analysis conversations where the user did not expect the full dashboard workflow.

Mitigation: Enable it for business KPI, ROI, dashboard, and visualization contexts, and review activation behavior during deployment.

Risk: Rendered charts may load Chart.js from a public CDN.

Mitigation: Confirm that external CDN loading is allowed in the deployment environment, or replace it with an approved internal or bundled chart runtime.

Risk: Business recommendations can be misleading when source data is incomplete, incorrectly parsed, or missing context.

Mitigation: Require users or reviewers to validate extracted metrics, assumptions, and recommendations before operational or financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/web-seeker/skills/data-visualization-analyst)
- [Chart.js UMD runtime](https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js)
- [WorkBuddy platform](https://www.codebuddy.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown analysis report with embedded HTML and JavaScript chart widgets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual output follows the user's input language; chart labels and report text are expected to match that language.]

## Skill Version(s):

2.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
