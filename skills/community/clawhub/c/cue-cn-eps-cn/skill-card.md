## Description:

每股收益逐条挂源：基本与稀释每股收益、加权平均股数、股数调整与追溯列报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

中文财报分析人员可用它把年报、半年报或公告中的每股收益披露整理为逐条可回查的登记表，保留原句、定位锚点和来源编号；它不预测每股收益、不估值或给出评级。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Use may involve external CUE services and optional API credentials; the security assessment flags unclear external destinations, token handling, and document transfers, with incomplete scanner coverage.

Mitigation: Before use, confirm the service destinations, credential handling, and document transfer behavior; send only financial documents approved for those services.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huhoo/skills/cue-cn-eps-cn)
- [CUE MCP setup](https://cuecue.cn/hub/mcp)
- [CUE Omni Reader setup](https://cuecue.cn/hub/omni-reader)
- [CUE API key information](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Seven-section Markdown register with quoted disclosure passages, location anchors, and source IDs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output; disclosed figures are transcribed, missing items are identified, and calculations or investment judgments are left to the user.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata, artifact/SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
