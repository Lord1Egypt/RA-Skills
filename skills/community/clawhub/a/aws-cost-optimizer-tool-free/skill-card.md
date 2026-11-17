## Description:

AWS成本分析工具，支持支出概览、服务与区域成本分解、闲置资源识别和基础优化建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, independent builders, startup teams, and operations users use this skill to review AWS spending, break down costs by service or region, identify idle resources, and generate basic savings recommendations and reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to AWS billing data and AWS credentials.

Mitigation: Use a read-only IAM user or profile limited to Cost Explorer and related describe/list permissions, and avoid root, administrator, or long-lived credentials.

Risk: The skill can ask the agent to run local shell commands.

Mitigation: Review commands before execution and keep activity within expected AWS cost-analysis commands and report exports.

Risk: The reviewed security summary flags broad and inconsistent instructions.

Mitigation: Treat modify, reset, import, or non-AWS data-analysis actions as outside the reviewed safe scope unless separately reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/aws-cost-optimizer-tool-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown with inline shell commands, YAML configuration examples, and optional CSV or JSON report exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose AWS Cost Explorer and describe/list-style analysis using user-provided AWS credentials; the free edition is scoped to single-account, basic recommendations.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
