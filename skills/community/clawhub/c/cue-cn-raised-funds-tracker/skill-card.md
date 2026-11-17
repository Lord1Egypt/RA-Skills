## Description:

把募集资金存续期台账逐条挂源：专户余额、投入进度、变更与置换、结项节余，进度只认披露写的。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

面向整理 A 股公司募集资金存续期披露的分析人员：将专项报告中的专户余额、项目投入进度、变更与置换事项整理成逐条引用原文的台账，并标明未取到的信息。

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: ClawScan reports network discovery and local usage tracking that conflict with the documented offline ledger purpose; inspection was partial, with 14 of 16 components fully inspected.

Mitigation: Review the suspicious verdict before installing, keeping in mind that the scanners do not establish malicious intent and the available evidence does not show financial records or credentials being transmitted.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huhoo/skills/cue-cn-raised-funds-tracker)
- [Cue MCP catalog](https://cuecue.cn/api/mcp-catalog)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown ledger with source quotations and anchors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Entries cite disclosure text; progress percentages are copied from disclosures rather than calculated.]

## Skill Version(s):

0.1.1 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
