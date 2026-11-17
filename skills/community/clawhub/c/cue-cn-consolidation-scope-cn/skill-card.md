## Description:

把一份财报的合并范围读成逐条挂源表：纳入与退出、持股与表决权、未合并理由。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

面向阅读中文上市公司财报的外部用户，用于登记合并范围变动、持股与表决权及未合并理由，并为每条记录保留披露原句、定位锚点和来源编号。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can send confidential financial attachments or credentials to external document and data services.

Mitigation: Review and trust the service destinations before use; do not send confidential attachments or credentials until their handling is acceptable.

Risk: Reported weaknesses in the financial accuracy checks could leave consolidation-register entries inaccurate or misleading.

Mitigation: Verify each entry, quotation, percentage, and control statement against the cited original disclosure before relying on the register.

Risk: Security inspection was incomplete, so unreported behavior has not been fully assessed.

Mitigation: Review the skill and its behavior before installation, accounting for the incomplete scan coverage.

## Reference(s):

- [ClawHub release](https://clawhub.ai/huhoo/skills/cue-cn-consolidation-scope-cn)
- [Cue MCP configuration](https://cuecue.cn/hub/mcp)
- [Cue Omni Reader](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [七节中文逐条挂源登记表]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [每条发现附逐字原句、定位锚点和来源编号；缺失信息明确列为“未取到”。]

## Skill Version(s):

0.1.0 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
