## Description:

Generate structured competitive analysis reports with feature comparisons, pricing analysis, SWOT, and strategic recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoliuzhu](https://clawhub.ai/user/chaoliuzhu)

### License/Terms of Use:

MIT-0

## Use Case:

Business, marketing, product, and strategy teams use this skill to research public competitor information and produce client-ready competitive intelligence reports with feature, pricing, SWOT, and recommendation sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad shell access for a report-generation workflow.

Mitigation: Review before installing when the target agent can run shell commands; remove or tightly scope Bash access if it is not required.

Risk: The skill may overwrite report artifacts in its output directory.

Mitigation: Check for existing output files before writing or keep versioned output directories for each report run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chaoliuzhu/skills/delonix-competitor-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown report, HTML report, Markdown executive summary, and CSV feature matrix]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill asks the agent to save report artifacts under output/competitor-analysis/.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
