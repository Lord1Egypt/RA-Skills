## Description:

将研发支出资本化披露整理为逐项附有原文、定位锚点和来源的台账，覆盖研发投入、开发支出、阶段划分、资本化条件及无形资产摊销与减值。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

面向整理年报和研发专项披露的财务人员与研究者，将研发投入、开发支出、资本化条件及摊销减值整理成可回查的逐项台账；阶段与条件照录披露，不替代专业判断或投资建议。

### Deployment Geography for Use:

Global (Chinese-language corporate disclosures)

## Known Risks and Mitigations:

Risk: Security evidence flags external service discovery and MCP requests that may carry an API key; the scan summary does not establish malicious intent.

Mitigation: Review the live catalog routing and requested tools before connecting, and keep the API key in the intended environment variable rather than in documents or prompts.

Risk: The security guidance identifies third-party document parsing as a concern when handling annual reports or disclosure files.

Mitigation: Send only documents approved for that service, and confirm the service's handling terms before submitting sensitive material.

Risk: The skill documentation says the first run writes a local usage marker under ~/.cue-usage/.

Mitigation: Inform users of this local marker and remove it if local usage tracking is not wanted.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huhoo/skills/cue-cn-rd-capitalization-cn)
- [CUE MCP setup](https://cuecue.cn/hub/mcp)
- [CUE Omni Reader setup](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Chinese Markdown disclosure register with quoted source text, location anchors, source IDs, and validation findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keeps disclosed figures separate, records missing items explicitly, and leaves investment and accounting judgments to the reader.]

## Skill Version(s):

0.1.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
