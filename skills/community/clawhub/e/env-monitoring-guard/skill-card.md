## Description:

环境监测报告合规护栏，在环境监测报告、污染源监督性监测报告、环境质量报告发布前，检测是否符合中国环境监测相关法律、管理办法和HJ系列技术规范要求，拦截不合规内容并给出修改建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[1003429073](https://clawhub.ai/user/1003429073)

### License/Terms of Use:

MIT-0

## Use Case:

Environmental monitoring staff, report reviewers, and compliance teams use this skill to review Chinese environmental monitoring reports and related public materials before release. It checks required report elements, qualification signals, monitoring methods, data authenticity, quality control, conclusions, and sensitive wording, then returns a structured compliance review with blocking issues and suggested revisions.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill is scoped to China-specific environmental monitoring compliance workflows and may be misapplied to other jurisdictions or report languages.

Mitigation: Use it for Chinese environmental monitoring review by default; request a jurisdiction- or language-specific review when the report is outside that scope.

Risk: Compliance checks may become incomplete if cited laws, management measures, or monitoring standards change after the skill release.

Mitigation: Review outputs against current authoritative regulations and standards before publication or enforcement decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1003429073/skills/env-monitoring-guard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown compliance review report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes counts of compliant, warning, and non-compliant items, issue details, cited violated clauses when available, revision suggestions, and a pass or fail conclusion.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
